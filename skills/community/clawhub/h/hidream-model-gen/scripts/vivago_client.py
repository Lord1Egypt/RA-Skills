#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vivago AI API Client - v0.3.1
支持层级架构：一级功能 -> 二级端口
"""

import json
import os
import time
import uuid
import logging
import warnings
import tempfile
from typing import Optional, Dict, Any, List, Tuple
import requests

from .enums import TaskStatus, AspectRatio, PortCategory, PortName, ModuleName
from .exceptions import (
    VivagoAPIError, InvalidPortError, MissingCredentialError,
    TaskFailedError, TaskRejectedError, TaskTimeoutError, ImageUploadError
)
from .config_loader import load_ports_config
from .image_processor import ImageProcessor

logger = logging.getLogger(__name__)

# 视频模板支持的宽高比
SUPPORTED_RATIOS = ["16:9", "1:1", "9:16", "4:3", "3:4"]

def parse_ratio(ratio_str: str) -> float:
    """解析宽高比字符串，返回宽/高的数值"""
    try:
        w, h = ratio_str.split(":")
        return float(w) / float(h)
    except:
        return 1.0

def find_closest_ratio(image_ratio: float) -> str:
    """找到与图片比例最接近的支持的宽高比"""
    min_diff = float('inf')
    closest = "1:1"
    
    for ratio in SUPPORTED_RATIOS:
        r = parse_ratio(ratio)
        diff = abs(image_ratio - r)
        if diff < min_diff:
            min_diff = diff
            closest = ratio
    
    return closest


class VivagoClient:
    """
    Vivago AI API Client
    
    层级架构：
    - 一级功能：text_to_image, image_to_video, image_to_image 等
    - 二级端口：kling-image, v3Pro, img2img 等具体API端点
    """
    
    def __init__(
        self, 
        token: str, 
        ports_config_path: Optional[str] = None
    ):
        """
        Initialize Vivago client.
        
        Args:
            token: Vivago API Bearer token
            ports_config_path: Path to api_ports.json (optional)
        """
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}",
            "X-accept-language": "en",
        }
        
        # Load ports configuration
        self.ports_config = self._load_ports_config(ports_config_path)
        self.base_url = self.ports_config.get("base_url", "https://vivago.ai/api/gw")
    
    
    def _load_ports_config(self, config_path: Optional[str] = None) -> Dict:
        """Load API ports configuration
        
        优先使用新的分体式配置加载器，支持 config/ 目录或回退到 api_ports.json
        """
        try:
            # 使用新的配置加载器
            if config_path:
                # 如果指定了路径，使用旧的方式加载
                with open(config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # 使用新的分体式配置加载
                return load_ports_config()
        except Exception as e:
            logger.warning(f"Failed to load ports config: {e}, using defaults")
            return self._default_ports_config()
    
    def _default_ports_config(self) -> Dict:
        """Default ports configuration"""
        return {
            "base_url": "https://vivago.ai/api/gw",
            "categories": {
                "text_to_image": {
                    "default_port": "kling-image",
                    "ports": {
                        "kling-image": {
                            "endpoint": "/v3/image/image_gen_kling/async",
                            "result_endpoint": "/v3/image/txt2img/async/results",
                            "version": "kling-image-o1"
                        }
                    }
                },
                "image_to_video": {
                    "default_port": "v3Pro",
                    "ports": {
                        "v3Pro": {
                            "endpoint": "/v3/video/video_diffusion_img2vid/async",
                            "result_endpoint": "/v3/video/video_diffusion/async/results",
                            "version": "v3Pro"
                        }
                    }
                }
            }
        }
    
    def _get_port_config(self, category: str, port: Optional[str] = None) -> Tuple[Dict, str]:
        """
        Get port configuration for a category.
        
        Args:
            category: 一级功能名称，如 "text_to_image"
            port: 二级端口名称，如 "kling-image" (None则使用默认)
            
        Returns:
            (port_config, port_name)
        """
        cat_config = self.ports_config.get("categories", {}).get(category)
        if not cat_config:
            raise InvalidPortError(f"Unknown category: {category}")
        
        ports = cat_config.get("ports", {})
        
        if port is None:
            port = cat_config.get("default_port")
            if not port:
                raise InvalidPortError(f"No default port for category: {category}")
        
        if port not in ports:
            available = list(ports.keys())
            raise InvalidPortError(port, category, available)
        
        return ports[port], port
    
    def list_categories(self) -> Dict[str, Dict[str, Any]]:
        """List all available categories (一级功能)"""
        categories = {}
        for cat_id, config in self.ports_config.get("categories", {}).items():
            categories[cat_id] = {
                "name": config.get("name", cat_id),
                "name_en": config.get("name_en", cat_id),
                "status": config.get("status", "unknown"),
                "default_port": config.get("default_port"),
                "description": config.get("description", "")
            }
        return categories
    
    def list_ports(self, category: str) -> Dict[str, Any]:
        """List all available ports for a category (二级端口)"""
        cat_config = self.ports_config.get("categories", {}).get(category)
        if not cat_config:
            raise InvalidPortError(f"Unknown category: {category}")
        
        ports = {}
        for port_id, config in cat_config.get("ports", {}).items():
            ports[port_id] = {
                "name": config.get("name", port_id),
                "display_name": config.get("display_name", port_id),
                "status": config.get("status", "unknown"),
                "tested": config.get("tested", False),
                "speed": config.get("speed", "unknown"),
                "quality": config.get("quality", "unknown"),
                "notes": config.get("notes", "")
            }
        return ports
    
    # ==================== File Upload ====================
    
    def upload_image(self, image_path: str, max_side: int = 1024, quality: int = 80) -> str:
        """
        上传图片到 Vivago 存储 (默认使用 v2 方式)
        
        这是新的默认实现，使用预签名 URL 方式上传。
        旧版 S3 上传方式仍可通过 upload_image_legacy 访问，但已标记为废弃。
        
        Args:
            image_path: 图片文件路径
            max_side: 图片最大边长，超过则缩放 (默认1024)
            quality: JPEG 压缩质量 (默认80)
            
        Returns:
            image_uuid: 上传后的图片 UUID (格式: j_xxxx)
            
        Raises:
            ImageUploadError: 上传失败
        """
        return self.upload_image_v2(image_path, max_side, quality)
    
    def upload_image_v2(self, image_path: str, max_side: int = 1024, quality: int = 80) -> str:
        """
        上传图片到 Vivago 存储 (v2 - 新方式，使用预签名 URL)
        
        新流程:
        1. GET /prod-api/user/google_key/hidreamai-image → 获取预签名 URL
        2. PUT 预签名 URL + 图片二进制数据 → 完成上传
        
        Args:
            image_path: 图片文件路径
            max_side: 图片最大边长，超过则缩放 (默认1024)
            quality: JPEG 压缩质量 (默认80)
            
        Returns:
            image_uuid: 上传后的图片 UUID (格式: j_xxxx)
            
        Raises:
            ImageUploadError: 上传失败
        """
        # 生成唯一的图片 UUID
        image_uuid = f"j_{uuid.uuid4()}"
        logger.info(f"Uploading image {image_path} -> {image_uuid} (v2)")
        
        # 步骤1: 处理图片
        try:
            image_data = ImageProcessor.process_for_upload(image_path, max_side, quality)
        except Exception as e:
            raise ImageUploadError(image_path, str(e))
        
        # 步骤2: 获取预签名上传 URL
        base_url = "https://vivago.ai"
        endpoint = "/prod-api/user/google_key/hidreamai-image"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "filename": image_uuid,
            "content_type": "image/jpeg"
        }
        
        try:
            response = requests.get(
                f"{base_url}{endpoint}",
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            if result.get('code') != 0:
                raise ImageUploadError(
                    image_path, 
                    f"Failed to get upload URL: {result.get('message')}"
                )
            
            presigned_url = result.get('result')
            if not presigned_url:
                raise ImageUploadError(image_path, "No presigned URL in response")
            
            logger.info(f"Got presigned URL (length: {len(presigned_url)})")
            
        except requests.RequestException as e:
            raise ImageUploadError(image_path, f"Failed to get upload URL: {e}")
        
        # 步骤3: 使用预签名 URL 上传图片
        try:
            upload_response = requests.put(
                presigned_url,
                data=image_data,
                headers={"Content-Type": "image/jpeg"},
                timeout=60
            )
            upload_response.raise_for_status()
            
            logger.info(f"Image uploaded successfully: {image_uuid}")
            return image_uuid
            
        except requests.RequestException as e:
            raise ImageUploadError(image_path, f"Failed to upload image: {e}")
    
    def preprocess_image_for_template(self, image_path: str, target_ratio: str = None) -> Tuple[str, str]:
        """
        为视频模板预处理图片
        
        1. 检测图片实际比例
        2. 如果图片比例在支持列表中，直接使用
        3. 如果不在，裁剪到最近的支持比例
        4. 上传处理后的图片 (使用新的 v2 上传方式)
        
        Args:
            image_path: 原始图片路径
            target_ratio: 指定的目标比例（可选），如果为None则自动检测
            
        Returns:
            (image_uuid, actual_wh_ratio): 上传后的图片UUID和实际使用的宽高比
        """
        # 读取图片比例
        actual_ratio = ImageProcessor.get_image_ratio(image_path)
        
        # 如果指定了目标比例，使用它；否则找到最接近的支持比例
        if target_ratio and target_ratio in SUPPORTED_RATIOS:
            closest_ratio = target_ratio
        else:
            closest_ratio = find_closest_ratio(actual_ratio)
        
        # 由于 ImageProcessor 目前不支持复杂裁剪，这里简化处理：
        # 直接上传并让后端/模板处理，或者后续在 ImageProcessor 中添加裁剪逻辑
        # 目前直接调用 upload_image_v2，它会进行缩放但不会裁剪
        
        # TODO: 在 ImageProcessor 中实现 crop_to_ratio
        
        image_uuid = self.upload_image_v2(image_path)
        logger.info(f"Uploaded image {image_path} -> {image_uuid} (ratio: {closest_ratio})")
            
        return image_uuid, closest_ratio
    
    # ==================== Core API Call ====================
    
    # 默认超时配置：30分钟（1800秒），防止重复计费
    DEFAULT_MAX_RETRIES = 360  # 30分钟 / 5秒 = 360次
    DEFAULT_RETRY_DELAY = 5    # 5秒轮询间隔
    
    def call_api(
        self,
        endpoint: str,
        data: Dict[str, Any],
        result_endpoint: str,
        max_retries: int = None,
        retry_delay: int = None
    ) -> Optional[List[Dict]]:
        # 使用默认超时配置
        if max_retries is None:
            max_retries = self.DEFAULT_MAX_RETRIES
        if retry_delay is None:
            retry_delay = self.DEFAULT_RETRY_DELAY
        """
        Generic API call with async task submission and polling.
        
        Args:
            endpoint: API submission endpoint
            data: Request body
            result_endpoint: Result polling endpoint
            max_retries: Maximum polling attempts
            retry_delay: Delay between polls (seconds)
        """
        try:
            url = f"{self.base_url}{endpoint}"
            headers_post = {**self.headers, "Content-Type": "application/json"}
            
            response = requests.post(url, json=data, headers=headers_post, timeout=1800)  # 30分钟
            
            if response.status_code != 200:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return None
            
            result = response.json()
            
            if result.get("code") != 0:
                logger.error(f"API error: {result.get('message')}")
                return result
            
            task_id = result.get("result", {}).get("task_id")
            if not task_id:
                logger.error("No task_id in response")
                return None
            
            logger.info(f"Task submitted: {task_id}")
            
            return self._poll_results(task_id, result_endpoint, max_retries, retry_delay)
            
        except Exception as e:
            logger.error(f"API call error: {e}")
            return None
    
    def _poll_results(
        self,
        task_id: str,
        result_endpoint: str,
        max_retries: int = None,
        retry_delay: int = None
    ) -> Optional[List[Dict]]:
        """Poll for task completion"""
        # 使用默认超时配置
        if max_retries is None:
            max_retries = self.DEFAULT_MAX_RETRIES
        if retry_delay is None:
            retry_delay = self.DEFAULT_RETRY_DELAY
        
        url = f"{self.base_url}{result_endpoint}?task_id={task_id}"
        headers_get = {"Authorization": self.headers["Authorization"]}
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers_get, timeout=1800)  # 30分钟
                
                if response.status_code != 200:
                    logger.warning(f"Poll failed: {response.status_code}")
                    time.sleep(retry_delay)
                    continue
                
                result = response.json()
                
                if result.get("code") != 0:
                    logger.error(f"API error: {result.get('message')}")
                    return None
                
                sub_results = result.get("result", {}).get("sub_task_results", [])
                
                # 使用TaskStatus枚举代替魔法数字
                if sub_results and all(
                    r.get("task_status") in {
                        TaskStatus.COMPLETED.value,
                        TaskStatus.FAILED.value,
                        TaskStatus.REJECTED.value
                    } for r in sub_results
                ):
                    status = sub_results[0].get("task_status")
                    if status == TaskStatus.COMPLETED.value:
                        logger.info(f"Task completed: {task_id}")
                    elif status == TaskStatus.FAILED.value:
                        logger.warning(f"Task failed: {task_id}")
                        raise TaskFailedError(task_id)
                    elif status == TaskStatus.REJECTED.value:
                        logger.warning(f"Task rejected: {task_id}")
                        raise TaskRejectedError(task_id)
                    return sub_results
                
                logger.debug(f"Task {task_id} processing (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)
                
            except Exception as e:
                logger.warning(f"Poll error: {e}")
                time.sleep(retry_delay)
        
        logger.error(f"Task timeout after {max_retries * retry_delay}s: {task_id}")
        raise TaskTimeoutError(task_id, max_retries * retry_delay)
    
    # ==================== Text to Image ====================
    
    def text_to_image(
        self,
        prompt: str,
        port: Optional[str] = None,
        negative_prompt: str = "",
        wh_ratio: str = "16:9",
        batch_size: int = 1,
        **kwargs
    ) -> Optional[List[Dict]]:
        """
        文生图 - 支持多端口选择
        
        Args:
            prompt: 提示词
            port: 二级端口 (None=使用默认)
            negative_prompt: 负面提示词
            wh_ratio: 宽高比
            batch_size: 生成数量 (1-4)
            **kwargs: 额外参数
        """
        port_config, port_name = self._get_port_config("text_to_image", port)
        
        # 根据端点推断 module 名称
        endpoint = port_config["endpoint"]
        if "image_gen_kling" in endpoint:
            module = "image_gen_kling"
        elif "image_gen_std" in endpoint:
            module = "image_gen_std"
        else:
            module = "txt2img"
        
        display_name = port_config.get("display_name", port_name)
        
        # 构建参数
        params = {
            "batch_count": 1,
            "batch_size": batch_size,
            "guidance_scale": kwargs.get("guidance_scale", 7.5),
            "height": kwargs.get("height", 512),
            "image_guidance_scale": kwargs.get("image_guidance_scale", 1.5),
            "sample_steps": kwargs.get("sample_steps", 40),
            "sampler": kwargs.get("sampler", "Euler a"),
            "seed": kwargs.get("seed", -1),
            "strength": kwargs.get("strength", 0.8),
            "style": kwargs.get("style", "default"),
            "wh_ratio": wh_ratio,
            "width": kwargs.get("width", 512),
            "relevance": kwargs.get("relevance", []),
            "custom_params": {
                "wh_ratio": wh_ratio
            }
        }
        
        # Nano Banana 2 特殊参数
        is_nano_banana = "image_gen_std" in endpoint
        if is_nano_banana:
            params["mode"] = kwargs.get("mode", "2K")
        
        data = {
            "app": None,
            "image": None,
            "mask": None,
            "module": module,
            "negative_prompt": negative_prompt,
            "prompt": prompt,
            "params": params,
            "role": kwargs.get("role", "general"),
            "images": [],
            "magic_prompt": kwargs.get("magic_prompt", prompt if is_nano_banana else ""),
            "audios": [],
            "videos": [],
            "request_id": str(uuid.uuid4())
        }
        
        # 设置 version 参数 (Kling 需要，Nano Banana 不需要，HiDream 也需要)
        if not is_nano_banana:
            # 如果 kwargs 中提供了 version，优先使用；否则使用配置中的默认值
            data["version"] = kwargs.get("version") or port_config.get("version", "kling-image-o1")
        
        logger.info(f"Using port: {port_name} ({display_name})")
        
        # 使用默认30分钟超时配置（防止重复计费）
        return self.call_api(
            endpoint=port_config["endpoint"],
            data=data,
            result_endpoint=port_config["result_endpoint"]
        )
    
    # ==================== Image to Video ====================
    
    def image_to_video(
        self,
        prompt: str,
        image_uuid: str,
        port: Optional[str] = None,
        wh_ratio: str = "16:9",
        duration: int = 5,
        mode: str = "Slow",
        fast_mode: bool = False,
        **kwargs
    ) -> Optional[List[Dict]]:
        """
        图生视频 - 支持多端口选择
        
        ⚠️ 注意：视频生成需要 2-3 分钟，请谨慎调用
        
        Args:
            prompt: 视频动作描述
            image_uuid: 参考图片UUID
            port: 二级端口 (v3Pro/v3L/kling-video, None=使用默认)
            wh_ratio: 宽高比
            duration: 视频时长 (5或10秒)
            mode: 生成模式 (Slow/Fast)
            fast_mode: 快速模式
            **kwargs: 额外参数
        """
        port_config, port_name = self._get_port_config("image_to_video", port)
        
        display_name = port_config.get("display_name", port_name)
        
        data = {
            "image": None,
            "module": "video_diffusion_img2vid",
            "params": {
                "batch_size": 1,
                "guidance_scale": kwargs.get("guidance_scale", 7),
                "sample_steps": kwargs.get("sample_steps", 80),
                "width": kwargs.get("width", 1920),
                "height": kwargs.get("height", 1080),
                "fast_mode": fast_mode,
                "frame_num": kwargs.get("frame_num", 16),
                "seed": kwargs.get("seed", -1),
                "motion_strength": kwargs.get("motion_strength", 9),
                "max_width": kwargs.get("max_width", 1024),
                "wh_ratio": "keep",
                "cm_x": kwargs.get("cm_x", 0),
                "cm_y": kwargs.get("cm_y", 0),
                "cm_d": kwargs.get("cm_d", 0),
                "custom_params": {
                    "wh_ratio": wh_ratio
                },
                "mode": mode,
                "duration": duration,
                "x": kwargs.get("x", 0),
                "y": kwargs.get("y", 0),
                "z": kwargs.get("z", 0),
                "style": kwargs.get("style", "default")
            },
            "prompt": prompt,
            "negative_prompt": kwargs.get("negative_prompt", ""),
            "role": kwargs.get("role", "general"),
            "style": kwargs.get("style", "default"),
            "wh_ratio": wh_ratio,
            "version": port_config.get("version", "v3Pro"),
            "magic_prompt": kwargs.get("magic_prompt", ""),
            "images": [image_uuid],
            "videos": [],
            "audios": [],
            "request_id": str(uuid.uuid4())
        }
        
        logger.info(f"Using port: {port_name} ({display_name}) ⚠️ 2-3 minutes")
        
        # 使用默认30分钟超时配置（防止重复计费）
        return self.call_api(
            endpoint=port_config["endpoint"],
            data=data,
            result_endpoint=port_config["result_endpoint"]
        )
    
    # ==================== Text to Video ====================
    
    def text_to_video(
        self,
        prompt: str,
        port: Optional[str] = None,
        wh_ratio: str = "16:9",
        duration: int = 5,
        mode: str = "Slow",
        fast_mode: bool = False,
        **kwargs
    ) -> Optional[List[Dict]]:
        """
        文生视频 - 从文本描述生成视频
        
        ⚠️ 注意：视频生成需要 2-3 分钟，请谨慎调用
        
        Args:
            prompt: 视频内容描述
            port: 二级端口 (v3Pro/v3L/kling-video, None=使用默认)
            wh_ratio: 宽高比 (1:1, 4:3, 3:4, 16:9, 9:16)
            duration: 视频时长 (5或10秒)
            mode: 生成模式 (Slow/Fast)
            fast_mode: 快速模式
            **kwargs: 额外参数
            
        Returns:
            List of generated video results
        """
        port_config, port_name = self._get_port_config("text_to_video", port)
        
        display_name = port_config.get("display_name", port_name)
        
        # 根据 endpoint 确定 module
        endpoint = port_config["endpoint"]
        if "gen2vid" in endpoint:
            module = "video_diffusion_gen2vid"
        else:
            module = "video_diffusion"
        
        data = {
            "image": None,
            "module": module,
            "params": {
                "batch_size": 1,
                "guidance_scale": kwargs.get("guidance_scale", 7),
                "sample_steps": kwargs.get("sample_steps", 80),
                "width": kwargs.get("width", 1920),
                "height": kwargs.get("height", 1080),
                "fast_mode": fast_mode,
                "frame_num": kwargs.get("frame_num", 16),
                "seed": kwargs.get("seed", -1),
                "motion_strength": kwargs.get("motion_strength", 9),
                "max_width": kwargs.get("max_width", 1024),
                "wh_ratio": wh_ratio,
                "cm_x": kwargs.get("cm_x", 0),
                "cm_y": kwargs.get("cm_y", 0),
                "cm_d": kwargs.get("cm_d", 0),
                "custom_params": {},
                "mode": mode,
                "duration": duration,
                "x": kwargs.get("x", 0),
                "y": kwargs.get("y", 0),
                "z": kwargs.get("z", 0),
                "style": kwargs.get("style", "default")
            },
            "prompt": prompt,
            "negative_prompt": kwargs.get("negative_prompt", ""),
            "role": kwargs.get("role", "general"),
            "style": kwargs.get("style", "default"),
            "wh_ratio": wh_ratio,
            "version": port_config.get("version", "v3Pro"),
            "magic_prompt": kwargs.get("magic_prompt", ""),
            "images": [],
            "videos": [],
            "audios": [],
            "request_id": str(uuid.uuid4())
        }
        
        logger.info(f"Using port: {port_name} ({display_name}) ⚠️ 2-3 minutes")
        
        # 使用默认30分钟超时配置（防止重复计费）
        return self.call_api(
            endpoint=port_config["endpoint"],
            data=data,
            result_endpoint=port_config["result_endpoint"]
        )
    
    # ==================== Keyframe to Video ====================
    
    def keyframe_to_video(
        self,
        prompt: str,
        start_image_uuid: str,
        end_image_uuid: str,
        port: Optional[str] = None,
        wh_ratio: str = "keep",
        duration: int = 5,
        mode: str = "Fast",
        fast_mode: bool = True,
        **kwargs
    ) -> Optional[List[Dict]]:
        """
        视频首尾帧 - 根据首尾帧生成过渡视频
        
        使用首尾两张图片生成从首帧到尾帧的过渡视频
        
        Args:
            prompt: 视频内容描述
            start_image_uuid: 起始帧图片UUID
            end_image_uuid: 结束帧图片UUID
            port: 二级端口 (v3L/v3Pro, 默认 v3L)
            wh_ratio: 宽高比 (keep/1:1/4:3/3:4/16:9/9:16)
            duration: 视频时长 (5或10秒)
            mode: 生成模式 (Fast/Slow)
            fast_mode: 快速模式
            **kwargs: 额外参数
            
        Returns:
            List of generated video results
        """
        port_config, port_name = self._get_port_config("keyframe_to_video", port or "v3L")
        
        display_name = port_config.get("display_name", port_name)
        
        # 构建 custom_params
        custom_params = {"wh_ratio": wh_ratio}
        if wh_ratio != "keep":
            # 解析 wh_ratio 为 width:height
            try:
                w, h = wh_ratio.split(":")
                custom_params["wh_ratio"] = f"{w}:{h}"
            except:
                custom_params["wh_ratio"] = "16:9"
        
        data = {
            "image": None,
            "module": "video_diffusion_keyframes",
            "params": {
                "batch_size": 1,
                "guidance_scale": kwargs.get("guidance_scale", 7),
                "sample_steps": kwargs.get("sample_steps", 80),
                "width": kwargs.get("width", 1360),
                "height": kwargs.get("height", 768),
                "fast_mode": fast_mode,
                "frame_num": kwargs.get("frame_num", 16),
                "seed": kwargs.get("seed", -1),
                "motion_strength": kwargs.get("motion_strength", 9),
                "max_width": kwargs.get("max_width", 1024),
                "wh_ratio": wh_ratio,
                "cm_x": kwargs.get("cm_x", 0),
                "cm_y": kwargs.get("cm_y", 0),
                "cm_d": kwargs.get("cm_d", 0),
                "custom_params": custom_params,
                "mode": mode,
                "duration": duration,
                "x": kwargs.get("x", 0),
                "y": kwargs.get("y", 0),
                "z": kwargs.get("z", 0),
                "style": kwargs.get("style", "default")
            },
            "prompt": prompt,
            "negative_prompt": kwargs.get("negative_prompt", ""),
            "role": kwargs.get("role", "general"),
            "style": kwargs.get("style", "default"),
            "wh_ratio": wh_ratio if wh_ratio != "keep" else custom_params.get("wh_ratio", "16:9"),
            "version": port_config.get("version", "v3L"),
            "magic_prompt": kwargs.get("magic_prompt", ""),
            "images": [start_image_uuid, end_image_uuid],  # 首尾帧图片
            "videos": [],
            "upstream_id": end_image_uuid,  # 根据抓包，与第二张图片相同
            "audios": [],
            "request_id": str(uuid.uuid4())
        }
        
        logger.info(f"Using port: {port_name} ({display_name}) with 2 keyframes ⚠️ 2-3 minutes")
        
        # 使用默认30分钟超时配置（防止重复计费）
        return self.call_api(
            endpoint=port_config["endpoint"],
            data=data,
            result_endpoint=port_config["result_endpoint"]
        )
    
    # ==================== Template to Video ====================
    
    def template_to_video(
        self,
        image_input: str = None,
        template: str = "renovation_old_photos",
        wh_ratio: str = None,
        image_uuid: str = None,
        **kwargs
    ) -> Optional[List[Dict]]:
        """
        视频模板 - 特定类型视频特效
        
        使用预定义模板生成特效视频，支持动态加载模板配置
        
        Args:
            image_input: 输入图片路径或已上传的UUID (以 'j_' 开头的UUID)
            template: 模板名称 (renovation_old_photos, barbie, ash_out 等)
            wh_ratio: 宽高比 (16:9, 1:1, 9:16, 3:4, 4:3)，None则自动检测并裁剪
            image_uuid: 兼容参数，与 image_input 相同
            **kwargs: 额外参数
            
        Returns:
            List of generated video results
        """
        # 处理参数兼容性：支持 image_input 或 image_uuid
        if image_input is None and image_uuid is None:
            raise ValueError("必须提供 image_input 或 image_uuid 参数")
        
        # 优先使用 image_input，如果为空则使用 image_uuid
        actual_input = image_input if image_input is not None else image_uuid
        
        # 将 actual_input 赋值给 image_input 以便后续代码使用
        image_input = actual_input
        # 使用模板管理器获取配置
        from .template_manager import get_template_manager
        
        manager = get_template_manager()
        template_config = manager.get_template(template)
        
        if not template_config:
            # 回退到 api_ports.json 配置
            port_config, port_name = self._get_port_config("template_to_video", template)
            display_name = port_config.get("display_name", port_name)
            endpoint = port_config["endpoint"]
            result_endpoint = port_config["result_endpoint"]
            template_id = port_config.get("template_id")
            module = port_config.get("algo_type", "proto_transformer")
            version = port_config.get("version", "v1")
        else:
            # 使用模板管理器的配置
            display_name = template_config['name']
            endpoint = template_config['endpoint']
            result_endpoint = template_config['result_endpoint']
            template_id = template_config['template_id']
            module = template_config['module']
            version = template_config['version']
            port_name = template
        
        # 判断输入是本地图片路径还是已上传的UUID
        if image_input.startswith('j_') and len(image_input) < 50:
            # 是已上传的UUID
            input_uuid = image_input
            logger.info(f"Using existing image UUID: {input_uuid}")
        else:
            # 是本地图片路径，需要预处理和上传
            logger.info(f"Preprocessing image: {image_input}")
            input_uuid, detected_ratio = self.preprocess_image_for_template(image_input, wh_ratio)
            logger.info(f"Preprocessed with ratio: {detected_ratio}")
        
        # 检查模板是否有比例限制
        restricted_ratio = template_config.get('restricted_ratio', False) if template_config else False
        
        if restricted_ratio:
            # 强制使用 1:1 比例
            actual_wh_ratio = "1:1"
            logger.warning(f"Template '{template}' is restricted to 1:1 ratio only (API limitation)")
        else:
            # 使用指定比例或默认 1:1
            actual_wh_ratio = wh_ratio if wh_ratio else "1:1"
        
        # 如果需要不同比例，重新预处理图片
        if restricted_ratio and wh_ratio != "1:1":
            logger.info(f"Re-processing image to 1:1 ratio...")
            if not image_input.startswith('j_') or len(image_input) >= 50:
                # 是本地路径，重新处理
                input_uuid, _ = self.preprocess_image_for_template(image_input, "1:1")
            # 如果是UUID，需要重新上传（简化处理：提示用户）
        
        image_uuid = input_uuid
        
        # 构建请求数据
        try:
            data = manager.build_request_data(template, image_uuid, wh_ratio=actual_wh_ratio, **kwargs)
        except ValueError:
            # 如果模板管理器中没有，使用默认构建逻辑
            data = self._build_default_template_data(
                image_uuid, template, actual_wh_ratio, module, version, template_id, **kwargs
            )
        
        logger.info(f"Using template: {port_name} ({display_name}) with ratio {actual_wh_ratio} ⚠️ 2-3 minutes")
        
        # 使用默认30分钟超时配置（防止重复计费）
        return self.call_api(
            endpoint=endpoint,
            data=data,
            result_endpoint=result_endpoint
        )
    
    def _build_default_template_data(
        self, image_uuid: str, template: str, wh_ratio: str,
        module: str, version: str, template_id: str, **kwargs
    ) -> Dict[str, Any]:
        """构建默认的模板请求数据"""
        return {
            "module": module,
            "version": version,
            "prompt": kwargs.get("prompt", ""),
            "images": [image_uuid],
            "masks": [],
            "videos": [],
            "audios": [],
            "params": {
                "mode": kwargs.get("mode", "Fast"),
                "style": kwargs.get("style", "default"),
                "height": kwargs.get("height", -1),
                "width": kwargs.get("width", -1),
                "seed": kwargs.get("seed", -1),
                "duration": kwargs.get("duration", 5),
                "motion": kwargs.get("motion", 0),
                "x": kwargs.get("x", 0),
                "y": kwargs.get("y", 0),
                "z": kwargs.get("z", 0),
                "reserved_str": kwargs.get("reserved_str", ""),
                "batch_size": 1,
                "wh_ratio": wh_ratio,
                "custom_params": {
                    "prompts": kwargs.get("prompts", []),
                    "master_template_id": template_id
                }
            },
            "en_prompt": kwargs.get("en_prompt", ""),
            "negative_prompt": kwargs.get("negative_prompt", ""),
            "en_negative_prompt": kwargs.get("en_negative_prompt", ""),
            "magic_prompt": kwargs.get("magic_prompt", ""),
            "template_id": template_id,
            "upstream_id": kwargs.get("upstream_id", ""),
            "pipeline_id": kwargs.get("pipeline_id", ""),
            "request_id": str(uuid.uuid4())
        }
    
    def download_image(self, image_id: str, output_path: Optional[str] = None) -> str:
        """
        下载图片到本地
        
        Args:
            image_id: 图片ID (如 "p_xxxxx")
            output_path: 保存路径，默认保存到 /tmp/
            
        Returns:
            本地文件路径，如果下载失败返回空字符串
        """
        if output_path is None:
            output_path = f"/tmp/{image_id}.png"
        
        # 使用正确的 storage URL 格式
        urls_to_try = [
            f"https://storage.vivago.ai/image/{image_id}.jpg",
            f"https://storage.vivago.ai/image/{image_id}.png",
        ]
        
        for url in urls_to_try:
            try:
                resp = requests.get(url, headers=self.headers, timeout=1800, allow_redirects=True)  # 30分钟
                if resp.status_code == 200 and len(resp.content) > 1000:
                    with open(output_path, 'wb') as f:
                        f.write(resp.content)
                    logger.info(f"Image downloaded: {output_path}")
                    return output_path
            except Exception as e:
                logger.debug(f"Failed to download from {url}: {e}")
                continue
        
        return ""
    
    def download_video(self, video_id: str, output_path: Optional[str] = None) -> str:
        """
        下载视频到本地
        
        Args:
            video_id: 视频文件名 (如 "xxxxxx.mp4")
            output_path: 保存路径，默认保存到 /tmp/
            
        Returns:
            本地文件路径，如果下载失败返回空字符串
        """
        if output_path is None:
            output_path = f"/tmp/{video_id}"
        
        # 使用正确的 media URL 格式 (不需要认证)
        url = f"https://media.vivago.ai/{video_id}"
        
        try:
            # 视频下载不需要 Authorization header
            resp = requests.get(url, timeout=1800, allow_redirects=True)  # 30分钟
            if resp.status_code == 200 and len(resp.content) > 10000:  # 视频至少 10KB
                with open(output_path, 'wb') as f:
                    f.write(resp.content)
                logger.info(f"Video downloaded: {output_path}")
                return output_path
        except Exception as e:
            logger.debug(f"Failed to download video: {e}")
        
        return ""
    
    # ==================== Image to Image ====================
    
    def image_to_image(
        self,
        prompt: str,
        image_uuids: List[str],
        port: Optional[str] = None,
        wh_ratio: str = "16:9",
        strength: float = 0.8,
        relevance: Optional[List[float]] = None,
        **kwargs
    ) -> Optional[List[Dict]]:
        """
        图生图 - 支持多图输入 (Nano Banana 2 / Kling O1)
        
        支持 Nano Banana 2 和 Kling O1 模型，支持多张参考图片融合生成
        
        Args:
            prompt: 图像描述
            image_uuids: 参考图片UUID列表 (最多5张)
            port: 二级端口 (nano-banana/kling-image, 默认 nano-banana)
            wh_ratio: 宽高比 (1:1, 4:3, 3:4, 16:9, 9:16)
            strength: 变化强度 (0.0-1.0, 默认0.8)
            relevance: 每张图片的参考权重列表 (默认每张0.9)
            **kwargs: 额外参数
            
        Returns:
            List of generated image results
        """
        port_config, port_name = self._get_port_config("image_to_image", port or "nano-banana")
        
        display_name = port_config.get("display_name", port_name)
        version = port_config.get("version", "nano-banana-2")
        
        # 根据端口确定 module
        if "kling" in port_name:
            module = "image_gen_kling"
        else:
            module = "image_gen_std"
        
        # 设置默认 relevance
        if relevance is None:
            relevance = [0.9] * len(image_uuids)
        
        # 确保 relevance 长度与 image_uuids 一致
        if len(relevance) != len(image_uuids):
            logger.warning(f"relevance length ({len(relevance)}) != image count ({len(image_uuids)}), adjusting...")
            relevance = [0.9] * len(image_uuids)
        
        # 构建 custom_params
        custom_params = {"wh_ratio": wh_ratio}
        if "kling" in port_name:
            custom_params["enhance"] = "2k"
        
        data = {
            "app": None,
            "image": image_uuids,  # 多图输入数组
            "mask": kwargs.get("mask"),
            "module": module,
            "negative_prompt": kwargs.get("negative_prompt", ""),
            "prompt": prompt,
            "params": {
                "batch_count": kwargs.get("batch_count", 1),
                "batch_size": kwargs.get("batch_size", 1),
                "guidance_scale": kwargs.get("guidance_scale", 7.5),
                "height": kwargs.get("height", 512),
                "image_guidance_scale": kwargs.get("image_guidance_scale", 1.5),
                "sample_steps": kwargs.get("sample_steps", 40),
                "sampler": kwargs.get("sampler", "Euler a"),
                "seed": kwargs.get("seed", -1),
                "strength": strength,
                "style": kwargs.get("style", "default"),
                "wh_ratio": wh_ratio,
                "width": kwargs.get("width", 512),
                "relevance": relevance,  # 每张图的权重
                "custom_params": custom_params
            },
            "role": kwargs.get("role", "general"),
            "images": [],  # 根据抓包，这里为空数组
            "magic_prompt": kwargs.get("magic_prompt", ""),
            "audios": [],
            "videos": [],
            "request_id": str(uuid.uuid4())
        }
        
        # Kling 需要 version 参数，Nano Banana 不需要
        if "kling" in port_name:
            data["version"] = version
        
        # Nano Banana 2 需要 mode 参数
        if "nano" in port_name:
            data["params"]["mode"] = "2K"
        
        logger.info(f"Using port: {port_name} ({display_name}) with {len(image_uuids)} images")
        
        # 使用默认30分钟超时配置（防止重复计费）
        return self.call_api(
            endpoint=port_config["endpoint"],
            data=data,
            result_endpoint=port_config["result_endpoint"]
        )
    
    def get_image_result(self, image_id: str) -> dict:
        """
        获取图片结果信息
        
        Returns:
            包含图片信息的字典
        """
        return {
            "image_id": image_id,
            "vivago_url": f"https://vivago.ai/history/image",
            "direct_url": f"https://storage.vivago.ai/image/{image_id}.jpg",
            "note": "图片可直接通过 direct_url 下载"
        }
    
    def get_video_result(self, video_id: str) -> dict:
        """
        获取视频结果信息
        
        Returns:
            包含视频信息的字典
        """
        return {
            "video_id": video_id,
            "vivago_url": f"https://vivago.ai/history/video",
            "direct_url": f"https://media.vivago.ai/{video_id}.mp4",
            "note": "视频可直接通过 direct_url 下载"
        }


def create_client(
    token: Optional[str] = None,
    ports_config_path: Optional[str] = None
) -> VivagoClient:
    """
    Create Vivago client from environment or parameters.
    
    Environment variables:
        HIDREAM_AUTHORIZATION: API token (required, fallback to HIDREAM_TOKEN)
    """
    token = token or os.environ.get("HIDREAM_AUTHORIZATION") or os.environ.get("HIDREAM_TOKEN")
    
    if not token:
        raise MissingCredentialError(
            "API token required. Set HIDREAM_AUTHORIZATION env var or pass token parameter."
        )
    
    return VivagoClient(token, ports_config_path)


if __name__ == "__main__":
    # 示例：查看可用端口
    logging.basicConfig(level=logging.INFO)
    
    try:
        client = create_client()
        
        print("\n=== 可用一级功能 ===")
        for cat_id, info in client.list_categories().items():
            print(f"{cat_id}: {info['name']} ({info['name_en']}) - {info['status']}")
        
        print("\n=== 文生图可用端口 ===")
        for port_id, info in client.list_ports("text_to_image").items():
            print(f"  {port_id}: {info['name']} - {'✅' if info['tested'] else '⏳'}")
        
        print("\n=== 图生视频可用端口 ===")
        for port_id, info in client.list_ports("image_to_video").items():
            print(f"  {port_id}: {info['name']} - {'✅' if info['tested'] else '⏳'}")
            
    except MissingCredentialError:
        print("请设置 HIDREAM_TOKEN 环境变量以运行示例")

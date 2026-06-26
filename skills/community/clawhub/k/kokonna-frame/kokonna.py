"""
KoKonna 画框控制库

用法：
    from kokonna import KoKonnaFrame
    
    frame = KoKonnaFrame(device="living_room")
    frame.upload_image("/path/to/image.jpg")
    info = frame.get_device_info()
"""

import base64
import os
from io import BytesIO
from pathlib import Path
from typing import Optional, Dict, Any

import requests
from PIL import Image

# 默认 API 地址
DEFAULT_API_BASE_URL = "https://api.galaxyguide.cn/openapi"

# 配置文件路径
CONFIG_PATHS = [
    Path.home() / ".openclaw" / "skills" / "kokonna-frame" / "config.yaml",
    Path.home() / ".openclaw" / "skills" / "kokonna-frame" / "config.yml",
    Path.cwd() / "config.yaml",
]


def load_config() -> Dict[str, Any]:
    """从配置文件加载配置"""
    import yaml
    
    for config_path in CONFIG_PATHS:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
    
    # 没有配置文件，返回空配置
    return {}


def get_api_base_url() -> str:
    """获取 API Base URL"""
    config = load_config()
    return config.get("api_base_url", DEFAULT_API_BASE_URL)


def get_device_config(device_name: str) -> Dict[str, Any]:
    """获取指定设备的配置"""
    config = load_config()
    devices = config.get("devices", {})
    
    if device_name not in devices:
        available = list(devices.keys())
        if available:
            raise ValueError(f"未知设备: {device_name}，可用设备: {available}")
        else:
            raise ValueError(f"未知设备: {device_name}，未配置任何设备。请在 config.yaml 中添加设备配置。")
    
    device_config = devices[device_name]
    
    # device_config 应该是 API Key 字符串，或者是包含详细配置的字典
    if isinstance(device_config, str):
        return {"api_key": device_config}
    else:
        return device_config


def generate_filename(image_source=None, name_hint: str = None) -> str:
    """生成有意义的文件名"""
    from datetime import datetime
    import re
    
    if name_hint:
        # 如果提供了名称提示，使用它
        # 清理文件名：只保留中文、英文、数字、下划线、连字符
        clean_name = re.sub(r'[^\w\u4e00-\u9fff\-]', '_', name_hint)
        clean_name = re.sub(r'_+', '_', clean_name).strip('_')
        if clean_name:
            return f"{clean_name}.jpg"
    
    # 从原文件名提取有意义部分
    if image_source and isinstance(image_source, (str, Path)):
        basename = Path(image_source).name
        name_without_ext = Path(image_source).stem
        # 去掉时间戳类的后缀
        clean_name = re.sub(r'[_\-]?\d{6,}[_\-]?\d*$', '', name_without_ext)
        clean_name = re.sub(r'[_\-]?\d{10,}', '', clean_name)
        if clean_name and len(clean_name) > 2:
            return f"{clean_name}.jpg"
    
    # 默认使用时间戳
    return datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"


class KoKonnaFrame:
    """KoKonna 画框控制类"""
    
    def __init__(self, device: str, width: int = None, height: int = None):
        """
        初始化画框
        
        Args:
            device: 设备名称（在 config.yaml 中配置）
            width: 画框宽度（可选，如未配置会自动从设备获取）
            height: 画框高度（可选，如未配置会自动从设备获取）
        """
        self.device_key = device
        self.api_base_url = get_api_base_url()
        device_config = get_device_config(device)
        
        self.api_key = device_config.get("api_key")
        if not self.api_key:
            raise ValueError(f"设备 {device} 未配置 api_key")
        
        self.width = width or device_config.get("width")
        self.height = height or device_config.get("height")
        
        # 如果没有配置尺寸，尝试从设备获取
        if not self.width or not self.height:
            info = self.get_device_info()
            if info:
                # 根据旋转角度确定实际显示尺寸
                rotation = info.get("rotation", 0)
                screen_width = info.get("screen_width", 480)
                screen_height = info.get("screen_height", 800)
                
                if rotation in [90, 270]:
                    self.width = screen_height
                    self.height = screen_width
                else:
                    self.width = screen_width
                    self.height = screen_height
    
    def _resize_image(self, image_source) -> bytes:
        """调整图片尺寸"""
        if isinstance(image_source, (str, Path)):
            img = Image.open(image_source)
        else:
            img = Image.open(image_source)
        
        # 转换颜色模式
        if img.mode == "RGBA":
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")
        
        # 如果没有尺寸信息，直接返回原图
        if not self.width or not self.height:
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=95)
            return buffer.getvalue()
        
        # 裁剪到目标比例
        target_ratio = self.width / self.height
        w, h = img.size
        current_ratio = w / h
        
        if current_ratio > target_ratio:
            # 图片太宽，裁剪两边
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            img = img.crop((left, 0, left + new_w, h))
        elif current_ratio < target_ratio:
            # 图片太高，裁剪上下
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            img = img.crop((0, top, w, top + new_h))
        
        # 缩放到目标尺寸
        img = img.resize((self.width, self.height), Image.LANCZOS)
        
        # 保存为 JPEG
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=95)
        return buffer.getvalue()
    
    def get_device_info(self) -> Optional[Dict]:
        """获取设备信息"""
        url = f"{self.api_base_url}/device"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.post(url, headers=headers, json={}, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取设备信息失败: {e}")
            return None
    
    def upload_image(self, image_source, name: str = None) -> Dict:
        """
        上传图片到画框
        
        Args:
            image_source: 图片路径或文件对象
            name: 图片名称（可选）
        
        Returns:
            API 响应
        """
        # 生成文件名
        filename = generate_filename(image_source, name)
        
        # 处理图片
        image_data = self._resize_image(image_source)
        base64_data = base64.b64encode(image_data).decode('utf-8')
        
        # 上传
        url = f"{self.api_base_url}/upload"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "base64": base64_data,
            "name": filename,
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()


# 便捷函数
def upload_to_device(device: str, image_path: str, name: str = None) -> Dict:
    """上传图片到指定设备"""
    frame = KoKonnaFrame(device=device)
    return frame.upload_image(image_path, name=name)


def get_device_info(device: str) -> Optional[Dict]:
    """获取指定设备信息"""
    frame = KoKonnaFrame(device=device)
    return frame.get_device_info()

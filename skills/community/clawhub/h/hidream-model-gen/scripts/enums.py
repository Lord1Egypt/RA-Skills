#!/usr/bin/env python3
"""
Type definitions and enums for Vivago AI Skill
"""
from enum import IntEnum
from typing import TypedDict, Optional, List, Dict, Any
from dataclasses import dataclass


class TaskStatus(IntEnum):
    """任务状态码枚举"""
    PENDING = 0      # 等待中
    COMPLETED = 1    # 已完成
    PROCESSING = 2   # 处理中
    FAILED = 3       # 失败
    REJECTED = 4     # 被拒绝（内容审核）


class AspectRatio(str):
    """宽高比常量"""
    RATIO_1_1 = "1:1"
    RATIO_4_3 = "4:3"
    RATIO_3_4 = "3:4"
    RATIO_16_9 = "16:9"
    RATIO_9_16 = "9:16"
    RATIO_KEEP = "keep"


class VideoDuration(int):
    """视频时长常量"""
    SHORT = 5    # 5秒
    LONG = 10    # 10秒


class VideoMode(str):
    """视频生成模式"""
    SLOW = "Slow"
    FAST = "Fast"


class PortCategory(str):
    """一级功能分类"""
    TEXT_TO_IMAGE = "text_to_image"
    IMAGE_TO_VIDEO = "image_to_video"
    TEXT_TO_VIDEO = "text_to_video"
    IMAGE_TO_IMAGE = "image_to_image"
    KEYFRAME_TO_VIDEO = "keyframe_to_video"
    TEMPLATE_TO_VIDEO = "template_to_video"


class PortName(str):
    """二级端口名称"""
    # 文生图
    KLING_IMAGE = "kling-image"
    HIDREAM_TXT2IMG = "hidream-txt2img"
    NANO_BANANA = "nano-banana"
    # 视频
    V3PRO = "v3Pro"
    V3L = "v3L"
    KLING_VIDEO = "kling-video"


class ModuleName(str):
    """API模块名称"""
    TXT2IMG = "txt2img"
    IMAGE_GEN_KLING = "image_gen_kling"
    IMAGE_GEN_STD = "image_gen_std"
    VIDEO_DIFFUSION = "video_diffusion"
    VIDEO_DIFFUSION_IMG2VID = "video_diffusion_img2vid"
    VIDEO_DIFFUSION_KEYFRAMES = "video_diffusion_keyframes"
    VIDEO_DIFFUSION_GEN2VID = "video_diffusion_gen2vid"
    PROTO_TRANSFORMER = "proto_transformer"


@dataclass
class GenerationResult:
    """生成结果数据类"""
    task_id: str
    status: TaskStatus
    urls: List[str]
    message: Optional[str] = None
    
    @property
    def is_success(self) -> bool:
        return self.status == TaskStatus.COMPLETED
    
    @property
    def is_failed(self) -> bool:
        return self.status in (TaskStatus.FAILED, TaskStatus.REJECTED)


class TaskResultDict(TypedDict):
    """任务结果字典类型"""
    task_status: int
    result: List[str]
    task_id: str


# JSON类型别名
JSONDict = Dict[str, Any]

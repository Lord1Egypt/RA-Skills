"""
GUI Agent 抽象基类

定义 GUI 自动化 Agent 的接口规范，支持多种多模态模型实现。
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from PIL import Image
from enum import Enum


class ActionType(Enum):
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    RIGHT_CLICK = "right_click"
    TYPE = "type"
    SCROLL = "scroll"
    DRAG = "drag"
    HOTKEY = "hotkey"
    WAIT = "wait"


@dataclass
class GUIAction:
    action_type: ActionType
    x: Optional[int] = None
    y: Optional[int] = None
    text: Optional[str] = None
    direction: Optional[str] = None
    start_x: Optional[int] = None
    start_y: Optional[int] = None
    end_x: Optional[int] = None
    end_y: Optional[int] = None
    keys: Optional[List[str]] = None
    duration_ms: Optional[int] = None
    description: Optional[str] = None


@dataclass
class GUIAgentResult:
    success: bool
    actions: List[GUIAction]
    reasoning: Optional[str] = None
    error: Optional[str] = None


class BaseGUIAgent(ABC):
    """
    GUI Agent 抽象基类
    
    所有 GUI 自动化模型都需要实现此接口。
    """
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, **kwargs):
        self.api_key = api_key
        self.base_url = base_url
        self.config = kwargs
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def provider(self) -> str:
        pass
    
    @abstractmethod
    def analyze(
        self,
        screenshot: Image.Image,
        instruction: str,
        **kwargs
    ) -> GUIAgentResult:
        """
        分析截图并返回操作指令
        
        Args:
            screenshot: PIL Image 格式的截图
            instruction: 自然语言指令（如 "点击登录按钮"）
        
        Returns:
            GUIAgentResult 包含操作列表
        """
        pass
    
    def find_element(
        self,
        screenshot: Image.Image,
        element_description: str,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        查找指定元素的位置
        
        Args:
            screenshot: PIL Image 格式的截图
            element_description: 元素描述（如 "登录按钮"）
        
        Returns:
            {'x': 中心点X, 'y': 中心点Y, 'width': 宽度, 'height': 高度} 或 None
        """
        result = self.analyze(screenshot, f"找到{element_description}的位置", **kwargs)
        
        if result.success and result.actions:
            for action in result.actions:
                if action.action_type in (ActionType.CLICK, ActionType.DOUBLE_CLICK):
                    if action.x is not None and action.y is not None:
                        return {
                            'x': action.x,
                            'y': action.y,
                            'description': action.description
                        }
        
        return None
    
    def click_element(
        self,
        screenshot: Image.Image,
        element_description: str,
        **kwargs
    ) -> GUIAgentResult:
        """
        点击指定元素
        
        Args:
            screenshot: PIL Image 格式的截图
            element_description: 元素描述（如 "登录按钮"）
        
        Returns:
            GUIAgentResult 包含点击操作
        """
        return self.analyze(screenshot, f"点击{element_description}", **kwargs)
    
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> 'BaseGUIAgent':
        """
        从配置字典创建 Agent 实例
        """
        return cls(**config)

"""
阿里云 GUI-Plus Agent 实现

使用阿里云百炼平台的 GUI-Plus 多模态模型实现 GUI 自动化。
"""
import os
import json
import base64
import re
from io import BytesIO
from typing import Optional, List, Dict, Any
from PIL import Image

from .base import BaseGUIAgent, GUIAgentResult, GUIAction, ActionType


SYSTEM_PROMPT_PC = """# Tools

You may call one function to assist you with the computer.

{"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer. Use this tool to interact with the computer. The screen resolution is 1920x1080. All coordinates you provide must be within this resolution range (x: 0-1919, y: 0-1079).", "parameters": {"properties": {"action": {"description": "The action to perform", "enum": ["click", "double_click", "type", "key_press", "scroll", "drag", "wait"], "type": "string"}, "coordinate": {"description": "The [x, y] pixel coordinates on a 1920x1080 screen. x must be 0-1919, y must be 0-1079.", "items": {"format": "integer", "type": "integer"}, "type": "array"}, "text": {"type": "string"}, "key": {"type": "string"}, "direction": {"enum": ["up", "down", "left", "right"], "type": "string"}, "start_coordinate": {"items": {"format": "integer", "type": "integer"}, "type": "array"}, "end_coordinate": {"items": {"format": "integer", "type": "integer"}, "type": "array"}, "duration_ms": {"format": "integer", "type": "integer"}}, "required": ["action"], "type": "object"}}

# Important Coordinate Instructions
- The screenshot is exactly 1920 pixels wide and 1080 pixels tall
- All click coordinates MUST be within this range: x (0-1919), y (0-1079)
- The origin (0,0) is at the TOP-LEFT corner of the screenshot
- x increases to the right, y increases downward
- DO NOT return coordinates outside the 1920x1080 range

# Role

You are a GUI operation assistant. When performing operations:
1. Analyze the screenshot carefully to find the target element
2. Return coordinates that are within 0-1919 for x and 0-1079 for y
3. Describe the result to the user"""


class AliyunGUIAgent(BaseGUIAgent):
    """
    阿里云 GUI-Plus Agent
    
    使用阿里云百炼平台的 GUI-Plus 多模态模型。
    """
    
    DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    DEFAULT_MODEL = "gui-plus-2026-02-26"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        **kwargs
    ):
        super().__init__(api_key, base_url, **kwargs)
        self.api_key = api_key or os.environ.get("DASHSCOPE_API_KEY")
        self.base_url = base_url or self.DEFAULT_BASE_URL
        self.model = model or self.DEFAULT_MODEL
        self._client = None
    
    @property
    def name(self) -> str:
        return self.model
    
    @property
    def provider(self) -> str:
        return "aliyun"
    
    def _get_client(self):
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.api_key,
                    base_url=self.base_url
                )
            except ImportError:
                raise ImportError("请安装 openai 库: pip install openai")
        return self._client
    
    def _image_to_base64(self, image: Image.Image) -> str:
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    def _parse_actions(self, tool_calls: List) -> List[GUIAction]:
        actions = []
        for tool_call in tool_calls:
            if tool_call.function.name == "computer_use":
                try:
                    args = json.loads(tool_call.function.arguments)
                    action = self._parse_single_action(args)
                    if action:
                        actions.append(action)
                except json.JSONDecodeError:
                    continue
        return actions
    
    def _parse_single_action(self, args: Dict[str, Any]) -> Optional[GUIAction]:
        action_type_str = args.get("action", "")
        
        action_map = {
            "click": ActionType.CLICK,
            "double_click": ActionType.DOUBLE_CLICK,
            "type": ActionType.TYPE,
            "key_press": ActionType.HOTKEY,
            "scroll": ActionType.SCROLL,
            "drag": ActionType.DRAG,
            "wait": ActionType.WAIT,
        }
        
        action_type = action_map.get(action_type_str)
        if not action_type:
            return None
        
        action = GUIAction(action_type=action_type)
        
        if action_type in (ActionType.CLICK, ActionType.DOUBLE_CLICK):
            coord = args.get("coordinate", [])
            if len(coord) >= 2:
                action.x = int(coord[0])
                action.y = int(coord[1])
        
        if action_type == ActionType.TYPE:
            action.text = args.get("text")
        
        if action_type == ActionType.SCROLL:
            action.direction = args.get("direction")
            coord = args.get("coordinate", [])
            if len(coord) >= 2:
                action.x = int(coord[0])
                action.y = int(coord[1])
        
        if action_type == ActionType.DRAG:
            start = args.get("start_coordinate", [])
            end = args.get("end_coordinate", [])
            if len(start) >= 2:
                action.start_x = int(start[0])
                action.start_y = int(start[1])
            if len(end) >= 2:
                action.end_x = int(end[0])
                action.end_y = int(end[1])
        
        if action_type == ActionType.WAIT:
            action.duration_ms = args.get("duration_ms")
        
        if action_type == ActionType.HOTKEY:
            action.keys = [args.get("key")] if args.get("key") else None
        
        return action
    
    def _get_system_prompt(self, width: int, height: int) -> str:
        return f"""# Tools

You may call one function to assist you with the computer.

{{"name": "computer_use", "description": "Use a mouse and keyboard to interact with a computer. The screen resolution is {width}x{height}. All coordinates you provide must be within this resolution range (x: 0-{width-1}, y: 0-{height-1}).", "parameters": {{"properties": {{"action": {{"description": "The action to perform", "enum": ["click", "double_click", "type", "key_press", "scroll", "drag", "wait"], "type": "string"}}, "coordinate": {{"description": "The [x, y] pixel coordinates on a {width}x{height} screen. x must be 0-{width-1}, y must be 0-{height-1}.", "items": {{"format": "integer", "type": "integer"}}, "type": "array"}}, "text": {{"type": "string"}}, "key": {{"type": "string"}}, "direction": {{"enum": ["up", "down", "left", "right"], "type": "string"}}, "start_coordinate": {{"items": {{"format": "integer", "type": "integer"}}, "type": "array"}}, "end_coordinate": {{"items": {{"format": "integer", "type": "integer"}}, "type": "array"}}, "duration_ms": {{"format": "integer", "type": "integer"}}}}, "required": ["action"], "type": "object"}}}}

# Important Coordinate Instructions
- The screenshot is exactly {width} pixels wide and {height} pixels tall
- All click coordinates MUST be within this range: x (0-{width-1}), y (0-{height-1})
- The origin (0,0) is at the TOP-LEFT corner of the screenshot
- x increases to the right, y increases downward
- DO NOT return coordinates outside the {width}x{height} range

# Role

You are a GUI operation assistant. When performing operations:
1. Analyze the screenshot carefully to find the target element
2. Return coordinates that are within 0-{width-1} for x and 0-{height-1} for y
3. Describe the result to the user"""
    
    def analyze(
        self,
        screenshot: Image.Image,
        instruction: str,
        **kwargs
    ) -> GUIAgentResult:
        if not self.api_key:
            return GUIAgentResult(
                success=False,
                actions=[],
                error="未配置 API Key，请设置 DASHSCOPE_API_KEY 环境变量或在配置文件中配置"
            )
        
        try:
            client = self._get_client()
            
            width, height = screenshot.size
            system_prompt = self._get_system_prompt(width, height)
            
            base64_image = self._image_to_base64(screenshot)
            
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        },
                        {
                            "type": "text",
                            "text": instruction
                        }
                    ]
                }
            ]
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "computer_use",
                        "description": "Use a mouse and keyboard to interact with a computer",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "action": {
                                    "type": "string",
                                    "enum": ["click", "double_click", "type", "key_press", "scroll", "drag", "wait"]
                                },
                                "coordinate": {
                                    "type": "array",
                                    "items": {"type": "integer"}
                                },
                                "text": {"type": "string"},
                                "key": {"type": "string"},
                                "direction": {
                                    "type": "string",
                                    "enum": ["up", "down", "left", "right"]
                                },
                                "start_coordinate": {
                                    "type": "array",
                                    "items": {"type": "integer"}
                                },
                                "end_coordinate": {
                                    "type": "array",
                                    "items": {"type": "integer"}
                                },
                                "duration_ms": {"type": "integer"}
                            },
                            "required": ["action"]
                        }
                    }
                }],
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            actions = []
            if message.tool_calls:
                actions = self._parse_actions(message.tool_calls)
            
            return GUIAgentResult(
                success=len(actions) > 0,
                actions=actions,
                reasoning=message.content
            )
            
        except Exception as e:
            return GUIAgentResult(
                success=False,
                actions=[],
                error=str(e)
            )

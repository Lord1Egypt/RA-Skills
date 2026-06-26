#!/usr/bin/env python3
"""
视觉识别模块
通过 AI 视觉模型识别屏幕内容，定位交互目标
"""

import os
import base64
import json
import argparse
from typing import Optional, Tuple, List, Dict, Any
from pathlib import Path


class VisionRecognizer:
    """屏幕视觉识别器"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
    
    def _encode_image(self, image_path: str) -> str:
        """将图片编码为 base64"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    
    def analyze_screen(
        self, 
        image_path: str, 
        task: str,
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        分析屏幕截图
        
        Args:
            image_path: 截图路径
            task: 分析任务描述
            
        Returns:
            分析结果字典
        """
        import subprocess
        
        api_key = api_key or self.api_key
        if not api_key:
            return {"error": "需要 OpenAI API Key"}
        
        # 读取截图
        if not os.path.exists(image_path):
            return {"error": f"截图文件不存在: {image_path}"}
        
        base64_image = self._encode_image(image_path)
        
        # 调用 GPT-4V
        prompt = f"""你是一个 Windows 桌面助手。请分析这张截图：

{task}

请以 JSON 格式返回分析结果，包含：
- elements: 识别的可交互元素列表 [{name, type, bounds, description}]
- next_action: 建议的下一步操作
- reasoning: 分析推理过程
"""
        
        try:
            result = subprocess.run(
                [
                    "curl", "-s", "-X", "POST",
                    "https://api.openai.com/v1/chat/completions",
                    "-H", f"Authorization: Bearer {api_key}",
                    "-H", "Content-Type: application/json",
                    "-d", json.dumps({
                        "model": self.model,
                        "messages": [
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": prompt},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        "max_tokens": 2000
                    })
                ],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            response = json.loads(result.stdout)
            
            if "error" in response:
                return {"error": response["error"].get("message", "Unknown error")}
            
            content = response["choices"][0]["message"]["content"]
            
            # 尝试解析 JSON
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"raw": content}
                
        except subprocess.TimeoutExpired:
            return {"error": "API 请求超时"}
        except Exception as e:
            return {"error": str(e)}
    
    def find_click_target(
        self,
        image_path: str,
        target_description: str,
        api_key: Optional[str] = None
    ) -> Optional[Tuple[int, int]]:
        """
        查找点击目标位置
        
        Args:
            image_path: 截图路径
            target_description: 目标描述，如 "下载按钮"、"下一步"
            
        Returns:
            (x, y) 坐标，或 None
        """
        result = self.analyze_screen(
            image_path,
            f"找到 '{target_description}' 的位置，返回其中心点坐标",
            api_key
        )
        
        if "error" in result:
            print(f"分析错误: {result['error']}")
            return None
        
        # 解析坐标
        if "elements" in result:
            for elem in result.get("elements", []):
                bounds = elem.get("bounds", {})
                if "x" in bounds and "y" in bounds:
                    return (bounds["x"], bounds["y"])
        
        # 尝试从原始输出中提取坐标
        raw = result.get("raw", "")
        import re
        coords = re.findall(r"(\d+),\s*(\d+)", raw)
        if coords:
            return (int(coords[0][0]), int(coords[0][1]))
        
        return None
    
    def describe_ui(
        self,
        image_path: str,
        api_key: Optional[str] = None
    ) -> str:
        """
        描述 UI 界面
        """
        result = self.analyze_screen(
            image_path,
            "描述这个界面的主要内容，列出所有可交互元素",
            api_key
        )
        
        if "error" in result:
            return f"分析错误: {result['error']}"
        
        if "raw" in result:
            return result["raw"]
        
        # 格式化输出
        lines = ["界面分析结果:", "=" * 50]
        
        if "elements" in result:
            lines.append("\n可交互元素:")
            for elem in result["elements"]:
                lines.append(f"  - {elem.get('name', '未命名')}")
                lines.append(f"    类型: {elem.get('type', '未知')}")
                lines.append(f"    描述: {elem.get('description', '无')}")
        
        if "next_action" in result:
            lines.append(f"\n建议操作: {result['next_action']}")
        
        if "reasoning" in result:
            lines.append(f"\n推理过程: {result['reasoning']}")
        
        return "\n".join(lines)


class LocalOCRecognizer:
    """本地 OCR 识别器（使用 EasyOCR 或 PaddleOCR）"""
    
    def __init__(self):
        self._ensure_dependencies()
    
    def _ensure_dependencies(self):
        """确保依赖已安装"""
        import subprocess
        try:
            import easyocr
        except ImportError:
            print("正在安装 EasyOCR...")
            subprocess.run(["pip", "install", "easyocr"], check=True)
    
    def read_text(self, image_path: str, languages: List[str] = ["en", "ch_sim"]) -> List[Dict]:
        """读取图片中的文字"""
        import easyocr
        
        reader = easyocr.Reader(languages)
        results = reader.readtext(image_path)
        
        text_blocks = []
        for (bbox, text, confidence) in results:
            if confidence > 0.5:
                text_blocks.append({
                    "text": text,
                    "confidence": confidence,
                    "bounds": bbox
                })
        
        return text_blocks
    
    def find_text_position(self, image_path: str, target_text: str) -> Optional[Tuple[int, int]]:
        """查找文字在图片中的位置"""
        blocks = self.read_text(image_path)
        
        for block in blocks:
            if target_text.lower() in block["text"].lower():
                # 返回中心点
                bounds = block["bounds"]
                x = int((bounds[0][0] + bounds[2][0]) / 2)
                y = int((bounds[0][1] + bounds[2][1]) / 2)
                return (x, y)
        
        return None
    
    def find_all_buttons(self, image_path: str) -> List[Dict]:
        """查找所有按钮"""
        blocks = self.read_text(image_path)
        
        buttons = []
        for block in blocks:
            text = block["text"].lower()
            # 常见的按钮文本
            if any(kw in text for kw in ["ok", "cancel", "next", "back", "save", 
                                         "确定", "取消", "下一步", "上一步", "保存",
                                         "install", "setup", "finish", "close"]):
                buttons.append(block)
        
        return buttons


def interactive_analyze(image_path: str, api_key: Optional[str] = None):
    """交互式屏幕分析"""
    print("=" * 60)
    print("屏幕视觉分析 - 交互模式")
    print("=" * 60)
    print(f"截图: {image_path}")
    print()
    
    recognizer = VisionRecognizer(api_key=api_key)
    
    while True:
        task = input("\n请输入分析任务 (q 退出): ").strip()
        
        if task.lower() in ["q", "quit", "exit"]:
            break
        
        if not task:
            continue
        
        print("\n分析中...")
        result = recognizer.analyze_screen(image_path, task)
        
        print("\n" + "=" * 60)
        if "error" in result:
            print(f"错误: {result['error']}")
        elif "raw" in result:
            print(result["raw"])
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="屏幕视觉识别")
    parser.add_argument("--image", "-i", required=True, help="截图路径")
    parser.add_argument("--task", "-t", help="分析任务")
    parser.add_argument("--find", "-f", help="查找目标")
    parser.add_argument("--describe", "-d", action="store_true", help="描述界面")
    parser.add_argument("--api-key", help="OpenAI API Key")
    parser.add_argument("--local", action="store_true", help="使用本地 OCR")
    parser.add_argument("--interactive", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    if args.interactive:
        interactive_analyze(args.image, args.api_key)
    elif args.describe:
        recognizer = VisionRecognizer(api_key=args.api_key)
        result = recognizer.describe_ui(args.image, args.api_key)
        print(result)
    elif args.find:
        recognizer = VisionRecognizer(api_key=args.api_key)
        pos = recognizer.find_click_target(args.image, args.find, args.api_key)
        if pos:
            print(f"找到目标 '{args.find}': 坐标 ({pos[0]}, {pos[1]})")
        else:
            print(f"未找到目标 '{args.find}'")
    elif args.task:
        recognizer = VisionRecognizer(api_key=args.api_key)
        result = recognizer.analyze_screen(args.image, args.task, args.api_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 默认描述界面
        recognizer = VisionRecognizer(api_key=args.api_key)
        result = recognizer.describe_ui(args.image, args.api_key)
        print(result)

#!/usr/bin/env python3
"""
本地模型API翻译模块 - 独立的翻译功能
"""

import sys
import time
import requests
from typing import Dict

from config import get_api_config, get_translation_config, parse_direction, get_language_name


class LocalTranslator:
    """本地模型翻译器"""
    
    def __init__(self, api_url: str = None, api_key: str = None, model: str = None):
        """
        初始化翻译器
        
        Args:
            api_url: API地址
            api_key: API密钥
            model: 模型名称
        """
        # 延迟导入config避免循环依赖
        from config import get_api_config
        api_config = get_api_config()
        
        self.api_url = api_url or api_config["api_url"]
        self.api_key = api_key or api_config["api_key"]
        self.model = model or api_config["model"]
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def check_connection(self) -> bool:
        """检查API连接"""
        try:
            models_url = self.api_url.replace("/chat/completions", "/models")
            resp = requests.get(models_url, headers=self.headers, timeout=5)
            return resp.status_code == 200
        except Exception as e:
            print(f"Connection failed: {e}", file=sys.stderr)
            return False
    
    def translate(self, text: str, direction: str = "en2zh", 
                  depth: str = "standard", context: str = "") -> str:
        """
        翻译文本
        
        Args:
            text: 要翻译的文本
            direction: 翻译方向，如 en2zh/zh2en/zh2ja/ja2en 等任意语言组合
            depth: 深度 quick/standard/full
            context: 上下文
        
        Returns:
            翻译后的文本
        """
        trans_config = get_translation_config()
        
        system_prompt = self._build_system_prompt(direction, depth)
        user_prompt = self._build_user_prompt(text, context, direction)
        
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": trans_config["temperature"],
            "max_tokens": trans_config["max_tokens"],
            "stream": False
        }
        
        if self.model:
            payload["model"] = self.model
        
        try:
            resp = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=120
            )
            resp.raise_for_status()
            result = resp.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Translation API failed: {e}", file=sys.stderr)
            return f"[Translation failed: {e}]"
    
    def _build_system_prompt(self, direction: str, depth: str) -> str:
        """构建系统提示（支持任意支持的翻译方向组合）"""
        try:
            src, tgt = parse_direction(direction)
            src_name = get_language_name(src, "en")
            tgt_name = get_language_name(tgt, "en")
            src_cn = get_language_name(src, "zh")
            tgt_cn = get_language_name(tgt, "zh")
        except ValueError as e:
            print(f"Warning: {e}", file=sys.stderr)
            src_name, tgt_name, src_cn, tgt_cn = "English", "Chinese", "英语", "中文"

        base = (
            f"You are a professional academic translator. "
            f"Translate {src_name} to {tgt_name}."
            f" (Source language: {src_cn}, Target language: {tgt_cn})\n\n"
            "Principles:\n"
            "1. Faithful to original meaning\n"
            "2. Use standard academic expressions in the target language\n"
            "3. Keep technical terms with target-language explanation when needed\n"
            "4. Preserve formulas, citations, numbers\n"
            "5. Maintain paragraph structure"
        )

        depth_map = {
            "quick": "\n- Quick translation, keep original meaning only",
            "standard": "\n- Standard: literal + reflection, ensure academic quality",
            "full": "\n- Full: literal + reflection + polish, achieve publication quality"
        }

        return base + depth_map.get(depth, "")

    def _build_user_prompt(self, text: str, context: str, direction: str = "en2zh") -> str:
        """构建用户提示"""
        try:
            src, tgt = parse_direction(direction)
            tgt_name = get_language_name(tgt, "en")
        except ValueError:
            tgt_name = "Chinese" if direction == "en2zh" else "English"

        prompt = ""
        if context:
            prompt += f"Context:\n{context[:500]}\n\n---\n\n"
        prompt += f"Translate the following into {tgt_name}:\n\n{text}"
        return prompt
    
    def translate_segment(self, text: str, direction: str = "en2zh",
                         depth: str = "standard", context: str = "") -> Dict:
        """
        翻译单个段落，返回带元数据的结果
        
        Returns:
            dict: {original, translated, direction, depth, time_seconds}
        """
        start_time = time.time()
        translated = self.translate(text, direction, depth, context)
        elapsed = time.time() - start_time
        
        return {
            "original": text,
            "translated": translated,
            "direction": direction,
            "depth": depth,
            "time_seconds": round(elapsed, 2),
            "chars_per_second": len(translated) / elapsed if elapsed > 0 else 0
        }


def main():
    """CLI入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Local Model Translation')
    parser.add_argument('--input', '-i', help='Input text file (or stdin)')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--text', '-t', help='Direct text input')
    parser.add_argument('--direction', default='en2zh',
                        help='Direction like en2zh/zh2ja/ja2en (default: en2zh)')
    parser.add_argument('--depth', choices=['quick', 'standard', 'full'], default='standard')
    parser.add_argument('--check', action='store_true', help='Check connection only')
    
    args = parser.parse_args()
    
    # Validate direction
    try:
        from config import parse_direction
        parse_direction(args.direction)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    translator = LocalTranslator()
    
    if args.check:
        if translator.check_connection():
            print("[OK] API connected successfully")
            sys.exit(0)
        else:
            print("[FAIL] API connection failed", file=sys.stderr)
            sys.exit(1)
    
    # Get input text
    if args.text:
        text = args.text
    elif args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = sys.stdin.read()
    
    if not text.strip():
        print("Error: Empty input", file=sys.stderr)
        sys.exit(1)
    
    # Translate
    result = translator.translate_segment(text, args.direction, args.depth)
    
    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result["translated"])
        print(f"Saved to: {args.output}", file=sys.stderr)
    else:
        print(result["translated"])
    
    print(f"\nStats: {result['time_seconds']}s, {result['direction']}, {result['depth']}", 
          file=sys.stderr)


if __name__ == "__main__":
    main()

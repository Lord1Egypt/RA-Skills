#!/usr/bin/env python3
"""
象寄文本翻译脚本

使用方法:
    python text_translate.py --api-key YOUR_KEY --texts "你好" --source-language CHS --target-language ENG
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

API_URL = "https://api.tosoiot.com/task/v1/text/translate"


def translate_text(api_key: str, texts: list, source_language: str, target_language: str, vendor: str = None) -> dict:
    """
    调用文本翻译API
    
    Args:
        api_key: 文本翻译密钥 (TextTransKey)
        texts: 要翻译的文本列表
        source_language: 源语言代码
        target_language: 目标语言代码
        vendor: 翻译引擎 (Aliyun, Google, Papago, Baidu, DeepL, Chatgpt, GoogleLLM)
    
    Returns:
        API响应字典
    """
    payload = {
        "texts": texts,
        "source_language": source_language,
        "target_language": target_language
    }
    
    if vendor:
        payload["translation_vendor"] = vendor
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        return {"code": e.code, "message": f"HTTP Error: {e.code} {e.reason}", "error_body": error_body}
    except urllib.error.URLError as e:
        return {"code": -1, "message": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"code": -1, "message": f"Error: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(description="象寄文本翻译")
    parser.add_argument("--api-key", required=True, help="文本翻译密钥 (TextTransKey)")
    parser.add_argument("--texts", nargs="+", required=True, help="要翻译的文本（可多个）")
    parser.add_argument("--source-language", required=True, help="源语言代码 (如 CHS, ENG, JPN)")
    parser.add_argument("--target-language", required=True, help="目标语言代码 (如 CHS, ENG, JPN)")
    parser.add_argument("--vendor", choices=["Aliyun", "Google", "Papago", "Baidu", "DeepL", "Chatgpt", "GoogleLLM"],
                        help="翻译引擎")
    
    args = parser.parse_args()
    
    result = translate_text(
        api_key=args.api_key,
        texts=args.texts,
        source_language=args.source_language,
        target_language=args.target_language,
        vendor=args.vendor
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 检查是否成功
    if result.get("code") == 0 or result.get("data", {}).get("result", {}).get("code") == 0:
        translated_texts = result.get("data", {}).get("result", {}).get("texts", [])
        if translated_texts:
            print("\n翻译结果:")
            for i, (original, translated) in enumerate(zip(args.texts, translated_texts), 1):
                print(f"  {i}. {original} -> {translated}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

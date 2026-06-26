#!/usr/bin/env python3
"""
Food packaging OCR for Health Coach.
Supports multiple engines: macOS Vision (local), custom cloud Vision (API).
"""

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import yaml
from typing import Dict, Any, Optional


def get_config_path() -> str:
    """Get user config file path."""
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(skill_dir, 'data', 'user_config.yaml')


def load_user_config() -> Dict[str, Any]:
    """Load user configuration from YAML file."""
    config_path = get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception:
            pass
    return {}


def get_vision_api_key() -> Optional[str]:
    """
    Get Vision API key from environment or config file.
    Priority: env var > config file > None
    """
    # Priority 1: Environment variable
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("CUSTOM_VISION_API_KEY")
    if api_key:
        return api_key
    
    # Priority 2: Config file
    config = load_user_config()
    vision_config = config.get('vision', {})
    return vision_config.get('api_key')


def get_vision_base_url() -> str:
    """Get Vision API base URL."""
    # Priority 1: Environment variable
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        return base_url
    
    # Priority 2: Config file
    config = load_user_config()
    vision_config = config.get('vision', {})
    return vision_config.get('base_url', 'https://api.moonshot.cn/v1')


def get_vision_model() -> str:
    """Get Vision model name."""
    # Priority 1: Environment variable
    model = os.environ.get("VISION_MODEL")
    if model:
        return model
    
    # Priority 2: Config file
    config = load_user_config()
    vision_config = config.get('vision', {})
    return vision_config.get('model', 'kimi-k2.5')


def encode_image(image_path: str) -> str:
    """Encode image to base64."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def ocr_macos_vision(image_path: str) -> Dict[str, Any]:
    """
    Use macOS built-in Vision framework via Shortcuts or command line.
    Falls back to basic text extraction.
    """
    try:
        # Try using macOS Vision via Shortcuts CLI
        # This requires a pre-made shortcut named "OCR Image"
        result = subprocess.run(
            ["shortcuts", "run", "OCR Image", "-i", image_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            text = result.stdout.strip()
            return {
                "status": "success",
                "engine": "macos_vision",
                "text": text,
                "structured": None  # macOS Vision doesn't structure automatically
            }
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    # Fallback: try using tesseract if available
    try:
        result = subprocess.run(
            ["tesseract", image_path, "stdout", "-l", "chi_sim+eng"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return {
                "status": "success",
                "engine": "tesseract",
                "text": result.stdout.strip(),
                "structured": None
            }
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    return {
        "status": "error",
        "engine": "macos_vision",
        "error": "macOS Vision OCR not available. Install Tesseract or create Shortcuts workflow.",
        "text": None
    }


def ocr_custom_vision(image_path: str, api_key: str) -> Dict[str, Any]:
    """
    Use custom cloud Vision API for OCR.
    Supports OpenAI-compatible APIs (e.g., Kimi, OpenAI, etc.)
    Requires OPENAI_API_KEY or CUSTOM_VISION_API_KEY environment variable.
    """
    try:
        import openai
    except ImportError:
        return {
            "status": "error",
            "engine": "custom",
            "error": "openai package not installed. Run: pip install openai",
            "text": None
        }
    
    # Determine base URL and model from config
    base_url = get_vision_base_url()
    model = get_vision_model()
    
    try:
        client = openai.OpenAI(api_key=api_key, base_url=base_url)
        
        # Encode image
        base64_image = encode_image(image_path)
        
        # Call Vision API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """识别这张食品包装图片，提取以下信息：
1. 商品名称（包装正面大字）
2. 品牌名称
3. 净含量/规格
4. 营养成分表（每100g的含量）
5. 条形码（如果有）
6. 保质期/到期日（如：6个月、12个月、2025-12-31等）
7. 储存条件（如：常温、冷藏、冷冻、避光等）

请返回严格的JSON格式：
{
    "product_name": "商品名称",
    "brand": "品牌",
    "net_weight": "净含量",
    "barcode": "条形码",
    "nutrition_per_100g": {
        "calories": 热量(千卡),
        "protein": 蛋白质(克),
        "carbs": 碳水化合物(克),
        "fat": 脂肪(克),
        "fiber": 膳食纤维(克),
        "sodium": 钠(毫克)
    },
    "shelf_life": "保质期",
    "storage_method": "储存条件",
    "confidence": "识别置信度(high/medium/low)"
}"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        # Parse response
        content = response.choices[0].message.content
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            try:
                structured = json.loads(json_match.group())
                return {
                    "status": "success",
                    "engine": "custom",
                    "text": content,
                    "structured": structured
                }
            except json.JSONDecodeError:
                pass
        
        # Return raw text if JSON parsing fails
        return {
            "status": "success",
            "engine": "custom",
            "text": content,
            "structured": None,
            "warning": "Could not parse structured data from response"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "engine": "custom",
            "error": str(e),
            "text": None
        }


def parse_nutrition_text(text: str) -> Dict[str, Any]:
    """
    Parse nutrition information from raw OCR text.
    Fallback when structured extraction fails.
    """
    result = {
        "product_name": None,
        "brand": None,
        "net_weight": None,
        "barcode": None,
        "nutrition_per_100g": {
            "calories": None,
            "protein": None,
            "carbs": None,
            "fat": None,
            "fiber": None
        }
    }
    
    # Extract barcode (13 or 8 digits)
    barcode_match = re.search(r'(\d{13}|\d{8})', text)
    if barcode_match:
        result["barcode"] = barcode_match.group(1)
    
    # Extract net weight
    weight_patterns = [
        r'(\d+)\s*[g克]',
        r'净含量[:：]?\s*(\d+)',
        r'规格[:：]?\s*(\d+)'
    ]
    for pattern in weight_patterns:
        match = re.search(pattern, text)
        if match:
            result["net_weight"] = match.group(1) + "g"
            break
    
    # Extract nutrition values
    # Calories
    cal_patterns = [
        r'能量[:：]?\s*(\d+)\s*[千k]?[卡cal]',
        r'热量[:：]?\s*(\d+)',
        r'(\d+)\s*[千k]?[卡cal]\s*/\s*100[g克]'
    ]
    for pattern in cal_patterns:
        match = re.search(pattern, text)
        if match:
            result["nutrition_per_100g"]["calories"] = float(match.group(1))
            break
    
    # Protein
    protein_match = re.search(r'蛋白质[:：]?\s*(\d+\.?\d*)\s*[g克]', text)
    if protein_match:
        result["nutrition_per_100g"]["protein"] = float(protein_match.group(1))
    
    # Carbs
    carbs_match = re.search(r'碳水化合物[:：]?\s*(\d+\.?\d*)\s*[g克]', text)
    if carbs_match:
        result["nutrition_per_100g"]["carbs"] = float(carbs_match.group(1))
    
    # Fat
    fat_match = re.search(r'脂肪[:：]?\s*(\d+\.?\d*)\s*[g克]', text)
    if fat_match:
        result["nutrition_per_100g"]["fat"] = float(fat_match.group(1))
    
    # Fiber
    fiber_match = re.search(r'膳食纤维[:：]?\s*(\d+\.?\d*)\s*[g克]', text)
    if fiber_match:
        result["nutrition_per_100g"]["fiber"] = float(fiber_match.group(1))
    
    return result


def recognize(args) -> Dict[str, Any]:
    """Main OCR function."""
    image_path = args.image
    
    if not os.path.exists(image_path):
        return {
            "status": "error",
            "error": "file_not_found",
            "message": f"Image not found: {image_path}"
        }
    
    # Choose engine
    engine = args.engine
    
    if engine == "auto":
        # Check if user has configured custom API key (env var or config file)
        custom_key = args.api_key or get_vision_api_key()
        if custom_key:
            # User has configured API key, use cloud OCR
            result = ocr_custom_vision(image_path, custom_key)
        else:
            # No API key configured, use local macOS Vision directly
            result = ocr_macos_vision(image_path)
    elif engine == "custom":
        # User explicitly wants custom/cloud OCR
        custom_key = args.api_key or get_vision_api_key()
        if not custom_key:
            return {
                "status": "error",
                "error": "api_key_required",
                "message": "Cloud OCR requires API key. Set OPENAI_API_KEY environment variable, or create data/user_config.yaml, or use --engine macos for local recognition."
            }
        result = ocr_custom_vision(image_path, custom_key)
    elif engine == "macos":
        result = ocr_macos_vision(image_path)
    else:
        return {
            "status": "error",
            "error": "invalid_engine",
            "message": f"Unknown engine: {engine}. Valid options: auto, macos, custom"
        }
    
    # If OCR succeeded but no structured data, try to parse
    if result["status"] == "success" and result.get("structured") is None and result.get("text"):
        result["structured"] = parse_nutrition_text(result["text"])
        result["parsed_from_text"] = True
    
    return result


def main():
    parser = argparse.ArgumentParser(description='Food packaging OCR')
    parser.add_argument('--image', required=True, help='Image file path')
    parser.add_argument('--engine', choices=['auto', 'custom', 'macos'], default='auto',
                       help='OCR engine: auto (uses custom if API key set, else macOS), custom (cloud API, requires key), macos (local, free). Default: auto')
    parser.add_argument('--api-key', help='API key for Kimi (or set OPENAI_API_KEY env)')
    parser.add_argument('--raw', action='store_true', help='Output raw text only')
    
    args = parser.parse_args()
    
    result = recognize(args)
    
    if args.raw and result.get("text"):
        print(result["text"])
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    sys.exit(0 if result["status"] == "success" else 1)


if __name__ == '__main__':
    main()

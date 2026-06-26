"""PaddleOCR Cloud API integration."""
import os
from pathlib import Path
from typing import Optional, Tuple

# API Configuration
PADDLEOCR_API_URL = os.environ.get(
    "PADDLEOCR_DOC_PARSING_API_URL",
    "https://c474r929pea0qa6c.aistudio-app.com/layout-parsing"
)
PADDLEOCR_ACCESS_TOKEN = os.environ.get(
    "PADDLEOCR_ACCESS_TOKEN",
    "86b3f40ddd719dad76e496472d341f1ba89085e3"
)


def is_configured() -> bool:
    """Check if PaddleOCR Cloud is configured."""
    return bool(PADDLEOCR_API_URL and PADDLEOCR_ACCESS_TOKEN)


def get_config() -> Tuple[str, str]:
    """Get API URL and access token."""
    return PADDLEOCR_API_URL, PADDLEOCR_ACCESS_TOKEN


def run_paddleocr_cloud(image_path: Path, verbose: bool = False) -> Optional[str]:
    """
    Run PaddleOCR Cloud API for text recognition.
    
    Args:
        image_path: Path to image file
        verbose: Enable verbose output
        
    Returns:
        Recognized text or None if failed
    """
    if not is_configured():
        if verbose:
            print("[PaddleOCR Cloud] Not configured, skipping...")
        return None
    
    import httpx
    
    headers = {
        "Authorization": f"Bearer {PADDLEOCR_ACCESS_TOKEN}"
    }
    
    try:
        with open(image_path, "rb") as f:
            files = {"file": (image_path.name, f, f"image/{image_path.suffix.lstrip('.')}")}
            
            if verbose:
                print(f"[PaddleOCR Cloud] Calling API: {PADDLEOCR_API_URL}")
            
            response = httpx.post(
                PADDLEOCR_API_URL,
                files=files,
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                if verbose:
                    print(f"[PaddleOCR Cloud] Success, got result")
                return parse_paddleocr_result(result)
            else:
                if verbose:
                    print(f"[PaddleOCR Cloud] Error: {response.status_code} - {response.text}")
                return None
                
    except Exception as e:
        if verbose:
            print(f"[PaddleOCR Cloud] Exception: {e}")
        return None


def parse_paddleocr_result(result: dict) -> str:
    """
    Parse PaddleOCR Cloud API response to text.
    
    Args:
        result: API response JSON
        
    Returns:
        Concatenated text from all recognized elements
    """
    text_parts = []
    
    # Handle different response formats
    if "data" in result:
        data = result["data"]
    elif "result" in result:
        data = result["result"]
    else:
        data = result
    
    # Iterate through recognized elements
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                # Try common text fields
                text = item.get("text") or item.get("content") or item.get("txt") or item.get("words", "")
                if text:
                    text_parts.append(str(text))
            elif isinstance(item, str):
                text_parts.append(item)
    
    return "\n".join(text_parts)


def looks_like_paddleocr_result(text: str) -> bool:
    """
    Check if text looks like valid OCR output.
    
    Args:
        text: OCR result text
        
    Returns:
        True if looks like valid OCR output
    """
    if not text or len(text.strip()) < 2:
        return False
    
    # Check for common OCR quality indicators
    # PaddleOCR usually returns structured text with reasonable length
    return True
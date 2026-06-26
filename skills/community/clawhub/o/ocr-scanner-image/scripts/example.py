#!/usr/bin/env python3
"""
OCR helper script for the ocr skill.
Uses the free demo API from ocr.space (apikey=helloworld).
Supports image URLs or local image files (jpg, png, bmp, gif, tiff).
Returns the extracted plain text or an error message.
"""

import sys
import os
import requests

API_URL = "https://api.ocr.space/parse/image"
DEMO_KEY = "helloworld"

def perform_ocr(source, language="eng"):
    """Perform OCR on an image.
    Args:
        source (str): URL or local file path to the image.
        language (str): OCR language code (default 'eng').
    Returns:
        str: Extracted text or error description.
    """
    files = {}
    data = {
        "apikey": DEMO_KEY,
        "language": language,
        "isOverlayRequired": "false",
    }
    if source.startswith("http://") or source.startswith("https://"):
        data["url"] = source
    else:
        if not os.path.isfile(source):
            return f"Error: file not found – {source}"
        files["file"] = open(source, "rb")
    try:
        resp = requests.post(API_URL, data=data, files=files, timeout=30)
    finally:
        if files:
            files["file"].close()
    if resp.status_code != 200:
        return f"Error: HTTP {resp.status_code} from OCR service"
    result = resp.json()
    if result.get("IsErroredOnProcessing"):
        return f"Error: {result.get('ErrorMessage', ['unknown error'])[0]}"
    parsed = result.get("ParsedResults", [])
    if not parsed:
        return "Error: No parsed results returned"
    return parsed[0].get("ParsedText", "")

def main():
    if len(sys.argv) < 2:
        print("Usage: example.py <image_path_or_url> [language]")
        sys.exit(1)
    source = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "eng"
    text = perform_ocr(source, language)
    print(text)

if __name__ == "__main__":
    main()

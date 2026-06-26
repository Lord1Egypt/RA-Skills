import os
import asyncio
import base64
from typing import Optional, Dict, Any

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


class AIImageClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    async def generate(self, prompt: str, model: str = "dall-e-3", size: str = "1024x1024") -> Dict[str, Any]:
        import requests
        if not requests:
            return {"success": False, "error": "requests not available"}
        
        url = "https://api.openai.com/v1/images/generations"
        payload = {"prompt": prompt, "model": model, "size": size, "n": 1}
        try:
            loop = asyncio.get_event_loop()
            resp = await loop.run_in_executor(None, lambda: requests.post(url, headers=self.headers, json=payload, timeout=60))
            data = resp.json()
            if resp.status_code == 200:
                return {"success": True, "url": data.get("data", [{}])[0].get("url")}
            return {"success": False, "error": data.get("error", {}).get("message", "Error")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def edit_image(self, image_path: str, prompt: str) -> Dict[str, Any]:
        import requests
        if not requests:
            return {"success": False, "error": "requests not available"}
        
        url = "https://api.openai.com/v1/images/edits"
        with open(image_path, "rb") as img:
            files = {"image": img}
            data = {"prompt": prompt}
            try:
                loop = asyncio.get_event_loop()
                resp = await loop.run_in_executor(None, lambda: requests.post(url, files=files, data=data, timeout=60))
                if resp.status_code == 200:
                    return {"success": True, "url": resp.json().get("data", [{}])[0].get("url")}
                return {"success": False, "error": "Error"}
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def variations(self, image_path: str, n: int = 1) -> Dict[str, Any]:
        import requests
        if not requests:
            return {"success": False, "error": "requests not available"}
        
        url = "https://api.openai.com/v1/images/variations"
        with open(image_path, "rb") as img:
            files = {"image": img}
            data = {"n": n}
            try:
                loop = asyncio.get_event_loop()
                resp = await loop.run_in_executor(None, lambda: requests.post(url, files=files, data=data, timeout=60))
                if resp.status_code == 200:
                    return {"success": True, "urls": [d.get("url") for d in resp.json().get("data", [])]}
                return {"success": False, "error": "Error"}
            except Exception as e:
                return {"success": False, "error": str(e)}


_client = None

def _get_client():
    global _client
    if not _client and OPENAI_API_KEY:
        _client = AIImageClient(OPENAI_API_KEY)
    return _client


async def ai_generate_image(prompt: str, model: str = "dall-e-3", size: str = "1024x1024") -> Dict[str, Any]:
    client = _get_client()
    if not client:
        return {"success": False, "error": "OPENAI_API_KEY not configured"}
    return await client.generate(prompt, model, size)


async def ai_edit_image(image_path: str, prompt: str) -> Dict[str, Any]:
    client = _get_client()
    if not client:
        return {"success": False, "error": "OPENAI_API_KEY not configured"}
    return await client.edit_image(image_path, prompt)


async def ai_image_variations(image_path: str, n: int = 1) -> Dict[str, Any]:
    client = _get_client()
    if not client:
        return {"success": False, "error": "OPENAI_API_KEY not configured"}
    return await client.variations(image_path, n)


TOOLS = [
    {"name": "ai_generate_image", "description": "Generate an image from text prompt", "input_schema": {"type": "object", "properties": {"prompt": {"type": "string", "description": "Image description"}, "model": {"type": "string", "description": "Model (dall-e-2 or dall-e-3)"}, "size": {"type": "string", "description": "Image size"}}, "required": ["prompt"]}},
    {"name": "ai_edit_image", "description": "Edit an existing image", "input_schema": {"type": "object", "properties": {"image_path": {"type": "string", "description": "Path to image file"}, "prompt": {"type": "string", "description": "Edit description"}}, "required": ["image_path", "prompt"]}},
    {"name": "ai_image_variations", "description": "Generate variations of an image", "input_schema": {"type": "object", "properties": {"image_path": {"type": "string", "description": "Path to image file"}, "n": {"type": "integer", "description": "Number of variations"}}}},
]


if __name__ == "__main__":
    print("AI Image Skill loaded")
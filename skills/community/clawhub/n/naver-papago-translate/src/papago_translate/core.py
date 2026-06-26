import os
import requests
from typing import Optional, Dict, Any

PAPAGO_TRANSLATE_URL = "https://openapi.naver.com/v1/papago/n2mt"
PAPAGO_DETECT_URL = "https://openapi.naver.com/v1/papago/detectLangs"

class PapagoError(Exception):
    pass

class PapagoClient:
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None, timeout: float = 15.0):
        self.client_id = client_id or os.environ.get("NAVER_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("NAVER_CLIENT_SECRET")
        if not self.client_id or not self.client_secret:
            raise PapagoError("Missing NAVER_CLIENT_ID or NAVER_CLIENT_SECRET. Set env vars or pass to PapagoClient().")
        self.timeout = timeout

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret,
        }

    def translate(self, source: Optional[str], target: str, text: str) -> Dict[str, Any]:
        if not target:
            raise PapagoError("Target language is required")
        data = {"target": target, "text": text}
        if source:
            data["source"] = source
        resp = requests.post(PAPAGO_TRANSLATE_URL, headers=self._headers(), data=data, timeout=self.timeout)
        if resp.status_code != 200:
            raise PapagoError(f"Papago translate failed: {resp.status_code} {resp.text}")
        return resp.json()

    def detect(self, text: str) -> str:
        resp = requests.post(PAPAGO_DETECT_URL, headers=self._headers(), data={"query": text}, timeout=self.timeout)
        if resp.status_code != 200:
            raise PapagoError(f"Papago detect failed: {resp.status_code} {resp.text}")
        js = resp.json()
        # docs: returns {"langCode": "ko"}
        return js.get("langCode", "")

def translate_text(source: Optional[str], target: str, text: str, *, client_id: Optional[str] = None, client_secret: Optional[str] = None, timeout: float = 15.0) -> str:
    client = PapagoClient(client_id=client_id, client_secret=client_secret, timeout=timeout)
    result = client.translate(source, target, text)
    # Expected schema: {"message":{"result":{"translatedText":"..."}}}
    try:
        return result["message"]["result"]["translatedText"]
    except Exception:
        raise PapagoError(f"Unexpected response: {result}")

def detect_language(text: str, *, client_id: Optional[str] = None, client_secret: Optional[str] = None, timeout: float = 15.0) -> str:
    client = PapagoClient(client_id=client_id, client_secret=client_secret, timeout=timeout)
    return client.detect(text)

import numpy as np
import requests

from config import get_config


def _mock_vector(text: str):
    np.random.seed(sum(ord(c) for c in text) % (2**32))
    return np.random.rand(1024).astype("float32").tolist()


def _openai_embeddings(text: str, api_key: str, base_url: str, model: str, timeout_sec: float):
    if not api_key:
        return _mock_vector(text)
    base = base_url.rstrip("/")
    if not base.endswith("/v1"):
        base = f"{base}/v1"
    url = f"{base}/embeddings"
    r = requests.post(
        url,
        json={"model": model, "input": text},
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        timeout=(3, timeout_sec),
    )
    r.raise_for_status()
    return r.json()["data"][0]["embedding"]


def _ollama_embeddings(text: str, base_url: str, model: str, timeout_sec: float):
    url = f"{base_url.rstrip('/')}/api/embeddings"
    r = requests.post(url, json={"model": model, "prompt": text}, timeout=(3, timeout_sec))
    r.raise_for_status()
    return r.json()["embedding"]


def get_embedding(text: str):
    cfg = get_config()
    emb = cfg.get("embedding") or {}
    provider = emb.get("provider") or "siliconflow"
    model = emb.get("model") or "BAAI/bge-m3"
    api_key = emb.get("api_key") or ""
    base_url = emb.get("base_url") or ""
    timeout_sec = float(emb.get("timeout_sec") or 15)
    max_input_chars = int(emb.get("max_input_chars") or 2000)
    text_for_embedding = text or ""
    if max_input_chars > 0 and len(text_for_embedding) > max_input_chars:
        text_for_embedding = text_for_embedding[:max_input_chars]

    try:
        if provider in ("siliconflow", "openai"):
            if provider == "openai" and not base_url:
                base_url = "https://api.openai.com/v1"
            if provider == "siliconflow" and not base_url:
                base_url = "https://api.siliconflow.cn/v1"
            return _openai_embeddings(text_for_embedding, api_key, base_url, model, timeout_sec)
        if provider == "ollama":
            if not base_url:
                base_url = "http://localhost:11434"
            return _ollama_embeddings(text_for_embedding, base_url, model, timeout_sec)
        if provider == "local_mock":
            return _mock_vector(text_for_embedding)
        return _mock_vector(text_for_embedding)
    except Exception:
        return _mock_vector(text_for_embedding)

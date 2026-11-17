"""lunheng 统一配置模块

所有外部服务配置通过环境变量加载，支持任何 OpenAI 兼容的 LLM 提供商。
无硬编码密钥、无个人路径引用、无 Gateway 依赖。

用法：
    from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL

环境变量：
    LH_LLM_API_KEY      — LLM API 密钥（必填）
    LH_LLM_BASE_URL     — API 地址（默认 https://api.openai.com/v1）
    LH_LLM_MODEL        — 模型名（默认 gpt-4o-mini）
    LH_LLM_ZERO_RETENTION — 启用零留存通道（默认 false）
    LH_LLM_LOCAL        — 启用本地模型模式（Ollama/vLLM，默认 false）
    LH_IMA_API_KEY      — IMA 知识库密钥（可选，仅中国用户）
    LH_IMA_CLIENT_ID    — IMA 客户端 ID（可选）

支持私有化部署：
    export LH_LLM_LOCAL=true
    export LH_LLM_BASE_URL="http://localhost:11434/v1"  # Ollama
    export LH_LLM_MODEL="qwen2.5:7b"
"""

import os


# ═══ LLM 提供商（OpenAI 兼容）══════════════════════
LLM_API_KEY: str = os.environ.get("LH_LLM_API_KEY", "")
LLM_BASE_URL: str = os.environ.get("LH_LLM_BASE_URL", "https://api.openai.com/v1")
LLM_MODEL: str = os.environ.get("LH_LLM_MODEL", "gpt-4o-mini")

# ═══ 零留存模式（Task 4.1）═══════════════════════
# 启用后，API 调用使用独立的零留存端点（需 provider 支持）
LLM_ZERO_RETENTION: bool = os.environ.get("LH_LLM_ZERO_RETENTION", "false").lower() == "true"

# ═══ 本地模型模式（Task 4.1）══════════════════════
# 启用后，指向本地 Ollama/vLLM 实例，数据不出本机
LLM_LOCAL: bool = os.environ.get("LH_LLM_LOCAL", "false").lower() == "true"

# ═══ IMA 知识库（可选，仅中国用户）════════════════
IMA_API_KEY: str = os.environ.get("LH_IMA_API_KEY", "")
IMA_CLIENT_ID: str = os.environ.get("LH_IMA_CLIENT_ID", "")


# ═══ API 请求代理（Task 4.1）══════════════════════
import json
import urllib.request
from typing import Optional


class LLMProxy:
    """统一 LLM API 请求代理，支持零留存通道和本地模型无缝切换"""

    def __init__(self):
        self.base_url = LLM_BASE_URL
        self.api_key = LLM_API_KEY
        self.model = LLM_MODEL
        self.zero_retention = LLM_ZERO_RETENTION
        self.local = LLM_LOCAL

    @property
    def resolved_base_url(self) -> str:
        """根据模式解析实际的 API 地址"""
        if self.local:
            # 本地模式（Ollama/vLLM）：全部走本地
            return self.base_url
        if self.zero_retention:
            # 零留存模式：使用独立端点（需 provider 支持）
            return os.environ.get("LH_LLM_ZR_URL", self.base_url)
        return self.base_url

    def chat(self, messages: list, temperature: float = 0.1,
             max_tokens: int = 4000, timeout: int = 120) -> Optional[str]:
        """发送聊天请求，返回响应文本"""
        if not self.api_key and not self.local:
            return None

        headers = {"Content-Type": "application/json"}
        if not self.local:
            headers["Authorization"] = f"Bearer {self.api_key}"

        body = json.dumps({
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{self.resolved_base_url}/chat/completions",
            data=body,
            headers=headers,
            method="POST",
        )

        try:
            resp = urllib.request.urlopen(req, timeout=timeout)
            data = json.loads(resp.read())
            return data["choices"][0]["message"]["content"]
        except Exception:
            return None

    def to_dict(self) -> dict:
        """脱敏状态报告"""
        return {
            "mode": "local" if self.local else ("zero_retention" if self.zero_retention else "standard"),
            "model": self.model,
            "base_url": self.base_url.replace(self.api_key, "***") if self.api_key else self.base_url,
        }


# 全局默认代理实例
DEFAULT_PROXY = LLMProxy()

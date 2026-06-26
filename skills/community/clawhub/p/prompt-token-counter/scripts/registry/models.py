"""Model registry for scripts.

Defines a canonical model registry with metadata needed for provider detection,
OpenAI encoding selection, approximate token formulas, and pricing lookup.
"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional


@dataclass(frozen=True)
class ModelInfo:
    name: str
    provider: str
    encoding: Optional[str] = None
    formula: Optional[str] = None
    pricing_id: Optional[str] = None
    aliases: Optional[List[str]] = None


def normalize_model_name(model: str) -> str:
    return model.strip().lower()


MODELS: Dict[str, ModelInfo] = {
    # OpenAI
    "gpt-4": ModelInfo("gpt-4", "openai", encoding="cl100k_base", pricing_id="gpt-4"),
    "gpt-4-0314": ModelInfo("gpt-4-0314", "openai", encoding="cl100k_base", pricing_id="gpt-4"),
    "gpt-4-0613": ModelInfo("gpt-4-0613", "openai", encoding="cl100k_base", pricing_id="gpt-4"),
    "gpt-4-32k": ModelInfo("gpt-4-32k", "openai", encoding="cl100k_base", pricing_id="gpt-4-32k"),
    "gpt-4-32k-0314": ModelInfo("gpt-4-32k-0314", "openai", encoding="cl100k_base", pricing_id="gpt-4-32k"),
    "gpt-4-32k-0613": ModelInfo("gpt-4-32k-0613", "openai", encoding="cl100k_base", pricing_id="gpt-4-32k"),
    "gpt-4-1106-preview": ModelInfo("gpt-4-1106-preview", "openai", encoding="cl100k_base"),
    "gpt-4-0125-preview": ModelInfo("gpt-4-0125-preview", "openai", encoding="cl100k_base"),
    "gpt-4-turbo-preview": ModelInfo("gpt-4-turbo-preview", "openai", encoding="cl100k_base"),
    "gpt-4-vision-preview": ModelInfo("gpt-4-vision-preview", "openai", encoding="cl100k_base"),
    "gpt-4-turbo": ModelInfo("gpt-4-turbo", "openai", encoding="cl100k_base", pricing_id="gpt-4-turbo"),
    "gpt-4-turbo-2024-04-09": ModelInfo("gpt-4-turbo-2024-04-09", "openai", encoding="cl100k_base", pricing_id="gpt-4-turbo"),
    "gpt-4o": ModelInfo("gpt-4o", "openai", encoding="cl100k_base", pricing_id="gpt-4o"),
    "gpt-4o-2024-05-13": ModelInfo("gpt-4o-2024-05-13", "openai", encoding="cl100k_base", pricing_id="gpt-4o"),
    "gpt-4o-mini": ModelInfo("gpt-4o-mini", "openai", encoding="cl100k_base", pricing_id="gpt-4o-mini"),
    "gpt-4o-mini-2024-07-18": ModelInfo("gpt-4o-mini-2024-07-18", "openai", encoding="cl100k_base", pricing_id="gpt-4o-mini"),
    "gpt-4o-2024-08-06": ModelInfo("gpt-4o-2024-08-06", "openai", encoding="cl100k_base", pricing_id="gpt-4o"),
    "gpt-4o-2024-11-20": ModelInfo("gpt-4o-2024-11-20", "openai", encoding="cl100k_base", pricing_id="gpt-4o"),
    "gpt-4-1106-vision-preview": ModelInfo("gpt-4-1106-vision-preview", "openai", encoding="cl100k_base"),
    "gpt-3.5-turbo": ModelInfo("gpt-3.5-turbo", "openai", encoding="cl100k_base", pricing_id="gpt-3.5-turbo"),
    "gpt-3.5-turbo-0301": ModelInfo("gpt-3.5-turbo-0301", "openai", encoding="cl100k_base", pricing_id="gpt-3.5-turbo"),
    "gpt-3.5-turbo-0613": ModelInfo("gpt-3.5-turbo-0613", "openai", encoding="cl100k_base", pricing_id="gpt-3.5-turbo"),
    "gpt-3.5-turbo-1106": ModelInfo("gpt-3.5-turbo-1106", "openai", encoding="cl100k_base", pricing_id="gpt-3.5-turbo"),
    "gpt-3.5-turbo-0125": ModelInfo("gpt-3.5-turbo-0125", "openai", encoding="cl100k_base", pricing_id="gpt-3.5-turbo"),
    "gpt-3.5-turbo-16k": ModelInfo("gpt-3.5-turbo-16k", "openai", encoding="cl100k_base", pricing_id="gpt-3.5-turbo-16k"),
    "gpt-3.5-turbo-16k-0613": ModelInfo("gpt-3.5-turbo-16k-0613", "openai", encoding="cl100k_base", pricing_id="gpt-3.5-turbo-16k"),
    "gpt-3.5-turbo-instruct": ModelInfo("gpt-3.5-turbo-instruct", "openai", encoding="cl100k_base"),
    "text-davinci-003": ModelInfo("text-davinci-003", "openai", encoding="p50k_base"),
    "text-davinci-002": ModelInfo("text-davinci-002", "openai", encoding="p50k_base"),
    "text-curie-001": ModelInfo("text-curie-001", "openai", encoding="r50k_base"),
    "text-babbage-001": ModelInfo("text-babbage-001", "openai", encoding="r50k_base"),
    "text-ada-001": ModelInfo("text-ada-001", "openai", encoding="r50k_base"),
    "davinci": ModelInfo("davinci", "openai", encoding="r50k_base"),
    "curie": ModelInfo("curie", "openai", encoding="r50k_base"),
    "babbage": ModelInfo("babbage", "openai", encoding="r50k_base"),
    "ada": ModelInfo("ada", "openai", encoding="r50k_base"),
    "gpt-3": ModelInfo("gpt-3", "openai", encoding="r50k_base"),
    "text-embedding-ada-002": ModelInfo("text-embedding-ada-002", "openai", encoding="cl100k_base"),
    "text-embedding-3-small": ModelInfo("text-embedding-3-small", "openai", encoding="cl100k_base"),
    "text-embedding-3-large": ModelInfo("text-embedding-3-large", "openai", encoding="cl100k_base"),
    "gpt-4-base": ModelInfo("gpt-4-base", "openai", encoding="cl100k_base"),
    "gpt-3.5-turbo-instruct-0914": ModelInfo("gpt-3.5-turbo-instruct-0914", "openai", encoding="cl100k_base"),
    "o1-preview": ModelInfo("o1-preview", "openai", encoding="cl100k_base"),
    "o1-mini": ModelInfo("o1-mini", "openai", encoding="cl100k_base"),
    "o1-preview-2024-09-12": ModelInfo("o1-preview-2024-09-12", "openai", encoding="cl100k_base"),
    "o1-mini-2024-09-12": ModelInfo("o1-mini-2024-09-12", "openai", encoding="cl100k_base"),
    "gpt-5.2-codex": ModelInfo("gpt-5.2-codex", "openai", encoding="cl100k_base"),
    "gpt-4-vision": ModelInfo("gpt-4-vision", "openai", encoding="cl100k_base"),
    "gpt-4-vision-preview-0409": ModelInfo("gpt-4-vision-preview-0409", "openai", encoding="cl100k_base"),
    "gpt-4-vision-preview-1106": ModelInfo("gpt-4-vision-preview-1106", "openai", encoding="cl100k_base"),
    "text-similarity-ada-001": ModelInfo("text-similarity-ada-001", "openai", encoding="r50k_base"),
    "text-similarity-babbage-001": ModelInfo("text-similarity-babbage-001", "openai", encoding="r50k_base"),
    "text-similarity-curie-001": ModelInfo("text-similarity-curie-001", "openai", encoding="r50k_base"),
    "text-similarity-davinci-001": ModelInfo("text-similarity-davinci-001", "openai", encoding="r50k_base"),

    # Anthropic
    "claude-3-opus-20240229": ModelInfo("claude-3-opus-20240229", "anthropic", formula="anthropic", pricing_id="claude-3-opus-20240229"),
    "claude-3-sonnet-20240229": ModelInfo("claude-3-sonnet-20240229", "anthropic", formula="anthropic", pricing_id="claude-3-sonnet-20240229"),
    "claude-3-haiku-20240307": ModelInfo("claude-3-haiku-20240307", "anthropic", formula="anthropic", pricing_id="claude-3-haiku-20240307"),
    "claude-3.5-sonnet-20240620": ModelInfo("claude-3.5-sonnet-20240620", "anthropic", formula="anthropic", pricing_id="claude-3.5-sonnet-20240620"),
    "claude-3.5-sonnet-20241022": ModelInfo("claude-3.5-sonnet-20241022", "anthropic", formula="anthropic", pricing_id="claude-3.5-sonnet-20241022"),
    "claude-3.5-haiku-20241022": ModelInfo("claude-3.5-haiku-20241022", "anthropic", formula="anthropic", pricing_id="claude-3.5-haiku-20241022"),
    "claude-3-5-sonnet-20240620": ModelInfo("claude-3-5-sonnet-20240620", "anthropic", formula="anthropic", pricing_id="claude-3.5-sonnet-20240620"),
    "claude-3-opus": ModelInfo("claude-3-opus", "anthropic", formula="anthropic", pricing_id="claude-3-opus-20240229"),
    "claude-3-sonnet": ModelInfo("claude-3-sonnet", "anthropic", formula="anthropic", pricing_id="claude-3-sonnet-20240229"),
    "claude-3-haiku": ModelInfo("claude-3-haiku", "anthropic", formula="anthropic", pricing_id="claude-3-haiku-20240307"),
    "claude-2.1": ModelInfo("claude-2.1", "anthropic", formula="anthropic"),
    "claude-2.0": ModelInfo("claude-2.0", "anthropic", formula="anthropic"),
    "claude-instant-1.2": ModelInfo("claude-instant-1.2", "anthropic", formula="anthropic"),
    "claude-instant-1.1": ModelInfo("claude-instant-1.1", "anthropic", formula="anthropic"),
    "claude-instant-1.0": ModelInfo("claude-instant-1.0", "anthropic", formula="anthropic"),
    "claude-instant": ModelInfo("claude-instant", "anthropic", formula="anthropic"),
    "claude-1": ModelInfo("claude-1", "anthropic", formula="anthropic"),
    "claude-1.3": ModelInfo("claude-1.3", "anthropic", formula="anthropic"),
    "claude-1.3-100k": ModelInfo("claude-1.3-100k", "anthropic", formula="anthropic"),
    "claude-3-5-haiku-20241022": ModelInfo("claude-3-5-haiku-20241022", "anthropic", formula="anthropic", pricing_id="claude-3.5-haiku-20241022"),
    "claude-3-5-sonnet-20241022": ModelInfo("claude-3-5-sonnet-20241022", "anthropic", formula="anthropic"),
    "claude-3.5-sonnet-computer-use": ModelInfo("claude-3.5-sonnet-computer-use", "anthropic", formula="anthropic"),
    "claude-2.1-200k": ModelInfo("claude-2.1-200k", "anthropic", formula="anthropic"),
    "claude-2.1-100k": ModelInfo("claude-2.1-100k", "anthropic", formula="anthropic"),
    "claude-instant-2": ModelInfo("claude-instant-2", "anthropic", formula="anthropic"),
    "claude-instant-2.0": ModelInfo("claude-instant-2.0", "anthropic", formula="anthropic"),
    "claude-3-opus-latest": ModelInfo("claude-3-opus-latest", "anthropic", formula="anthropic", pricing_id="claude-3-opus-20240229"),
    "claude-3-sonnet-latest": ModelInfo("claude-3-sonnet-latest", "anthropic", formula="anthropic", pricing_id="claude-3-sonnet-20240229"),
    "claude-sonnet-4-6": ModelInfo("claude-sonnet-4-6", "anthropic", formula="anthropic"),
    "claude-sonnet-4-5": ModelInfo("claude-sonnet-4-5", "anthropic", formula="anthropic"),
    "claude-opus-4.6": ModelInfo("claude-opus-4.6", "anthropic", formula="anthropic"),

    # Google
    "gemini-pro": ModelInfo("gemini-pro", "google", formula="google"),
    "gemini-pro-vision": ModelInfo("gemini-pro-vision", "google", formula="google"),
    "gemini-1.5-pro": ModelInfo("gemini-1.5-pro", "google", formula="google"),
    "gemini-1.5-flash": ModelInfo("gemini-1.5-flash", "google", formula="google"),
    "gemini-1.5-pro-latest": ModelInfo("gemini-1.5-pro-latest", "google", formula="google"),
    "gemini-1.5-flash-latest": ModelInfo("gemini-1.5-flash-latest", "google", formula="google"),
    "gemini-1.0-pro": ModelInfo("gemini-1.0-pro", "google", formula="google"),
    "gemini-1.0-pro-vision": ModelInfo("gemini-1.0-pro-vision", "google", formula="google"),
    "gemini-ultra": ModelInfo("gemini-ultra", "google", formula="google"),
    "gemini-2.0-flash-exp": ModelInfo("gemini-2.0-flash-exp", "google", formula="google"),
    "gemini-2.0-flash": ModelInfo("gemini-2.0-flash", "google", formula="google"),
    "gemini-exp-1206": ModelInfo("gemini-exp-1206", "google", formula="google"),
    "gemini-exp-1121": ModelInfo("gemini-exp-1121", "google", formula="google"),
    "palm-2": ModelInfo("palm-2", "google", formula="google"),
    "palm-2-chat": ModelInfo("palm-2-chat", "google", formula="google"),
    "palm-2-codechat": ModelInfo("palm-2-codechat", "google", formula="google"),
    "gemini-1.0-pro-001": ModelInfo("gemini-1.0-pro-001", "google", formula="google"),
    "gemini-1.0-pro-latest": ModelInfo("gemini-1.0-pro-latest", "google", formula="google"),
    "gemini-1.0-pro-vision-latest": ModelInfo("gemini-1.0-pro-vision-latest", "google", formula="google"),
    "gemini-3.1-pro-preview": ModelInfo("gemini-3.1-pro-preview", "google", formula="google"),

    # Meta
    "llama-2-7b": ModelInfo("llama-2-7b", "meta", formula="meta"),
    "llama-2-13b": ModelInfo("llama-2-13b", "meta", formula="meta"),
    "llama-2-70b": ModelInfo("llama-2-70b", "meta", formula="meta"),
    "llama-3-8b": ModelInfo("llama-3-8b", "meta", formula="meta"),
    "llama-3-70b": ModelInfo("llama-3-70b", "meta", formula="meta"),
    "llama-3.1-8b": ModelInfo("llama-3.1-8b", "meta", formula="meta"),
    "llama-3.1-70b": ModelInfo("llama-3.1-70b", "meta", formula="meta"),
    "llama-3.1-405b": ModelInfo("llama-3.1-405b", "meta", formula="meta"),
    "llama-3.2-1b": ModelInfo("llama-3.2-1b", "meta", formula="meta"),
    "llama-3.2-3b": ModelInfo("llama-3.2-3b", "meta", formula="meta"),
    "llama-3.3-70b": ModelInfo("llama-3.3-70b", "meta", formula="meta"),
    "llama-3.3-70b-instruct": ModelInfo("llama-3.3-70b-instruct", "meta", formula="meta"),
    "llama-2-7b-chat": ModelInfo("llama-2-7b-chat", "meta", formula="meta"),
    "llama-2-13b-chat": ModelInfo("llama-2-13b-chat", "meta", formula="meta"),
    "llama-2-70b-chat": ModelInfo("llama-2-70b-chat", "meta", formula="meta"),
    "llama-2-7b-chat-hf": ModelInfo("llama-2-7b-chat-hf", "meta", formula="meta"),
    "llama-2-13b-chat-hf": ModelInfo("llama-2-13b-chat-hf", "meta", formula="meta"),
    "llama-2-70b-chat-hf": ModelInfo("llama-2-70b-chat-hf", "meta", formula="meta"),
    "llama-3-8b-instruct": ModelInfo("llama-3-8b-instruct", "meta", formula="meta"),
    "llama-3-70b-instruct": ModelInfo("llama-3-70b-instruct", "meta", formula="meta"),
    "llama-3.1-8b-instruct": ModelInfo("llama-3.1-8b-instruct", "meta", formula="meta"),
    "llama-3.1-70b-instruct": ModelInfo("llama-3.1-70b-instruct", "meta", formula="meta"),
    "llama-3.1-405b-instruct": ModelInfo("llama-3.1-405b-instruct", "meta", formula="meta"),
    "llama-3.2-1b-instruct": ModelInfo("llama-3.2-1b-instruct", "meta", formula="meta"),
    "llama-3.2-3b-instruct": ModelInfo("llama-3.2-3b-instruct", "meta", formula="meta"),

    # Mistral
    "mistral-7b": ModelInfo("mistral-7b", "mistral", formula="mistral"),
    "mistral-8x7b": ModelInfo("mistral-8x7b", "mistral", formula="mistral"),
    "mistral-large": ModelInfo("mistral-large", "mistral", formula="mistral"),
    "mistral-medium": ModelInfo("mistral-medium", "mistral", formula="mistral"),
    "mistral-small": ModelInfo("mistral-small", "mistral", formula="mistral"),
    "mistral-tiny": ModelInfo("mistral-tiny", "mistral", formula="mistral"),
    "mixtral-8x7b": ModelInfo("mixtral-8x7b", "mistral", formula="mistral"),
    "mixtral-8x22b": ModelInfo("mixtral-8x22b", "mistral", formula="mistral"),
    "mistral-large-2": ModelInfo("mistral-large-2", "mistral", formula="mistral"),
    "mistral-large-2407": ModelInfo("mistral-large-2407", "mistral", formula="mistral"),
    "mistral-7b-instruct": ModelInfo("mistral-7b-instruct", "mistral", formula="mistral"),
    "mistral-7b-instruct-v0.1": ModelInfo("mistral-7b-instruct-v0.1", "mistral", formula="mistral"),
    "mistral-7b-instruct-v0.2": ModelInfo("mistral-7b-instruct-v0.2", "mistral", formula="mistral"),
    "mistral-7b-instruct-v0.3": ModelInfo("mistral-7b-instruct-v0.3", "mistral", formula="mistral"),
    "mixtral-8x7b-instruct": ModelInfo("mixtral-8x7b-instruct", "mistral", formula="mistral"),
    "mixtral-8x22b-instruct": ModelInfo("mixtral-8x22b-instruct", "mistral", formula="mistral"),

    # Cohere
    "command": ModelInfo("command", "cohere", formula="cohere"),
    "command-light": ModelInfo("command-light", "cohere", formula="cohere"),
    "command-nightly": ModelInfo("command-nightly", "cohere", formula="cohere"),
    "command-r": ModelInfo("command-r", "cohere", formula="cohere"),
    "command-r-plus": ModelInfo("command-r-plus", "cohere", formula="cohere"),
    "command-r-08-2024": ModelInfo("command-r-08-2024", "cohere", formula="cohere"),
    "command-r-plus-08-2024": ModelInfo("command-r-plus-08-2024", "cohere", formula="cohere"),
    "command-r-plus-04-2024": ModelInfo("command-r-plus-04-2024", "cohere", formula="cohere"),

    # Perplexity
    "pplx-7b-online": ModelInfo("pplx-7b-online", "perplexity", formula="perplexity"),
    "pplx-70b-online": ModelInfo("pplx-70b-online", "perplexity", formula="perplexity"),
    "pplx-7b-chat": ModelInfo("pplx-7b-chat", "perplexity", formula="perplexity"),
    "pplx-70b-chat": ModelInfo("pplx-70b-chat", "perplexity", formula="perplexity"),
    "codellama-34b-instruct": ModelInfo("codellama-34b-instruct", "perplexity", formula="perplexity"),

    # HuggingFace
    "microsoft/DialoGPT-medium": ModelInfo("microsoft/DialoGPT-medium", "huggingface", formula="huggingface"),
    "microsoft/DialoGPT-large": ModelInfo("microsoft/DialoGPT-large", "huggingface", formula="huggingface"),
    "facebook/blenderbot-400M-distill": ModelInfo("facebook/blenderbot-400M-distill", "huggingface", formula="huggingface"),
    "facebook/blenderbot-1B-distill": ModelInfo("facebook/blenderbot-1B-distill", "huggingface", formula="huggingface"),
    "facebook/blenderbot-3B": ModelInfo("facebook/blenderbot-3B", "huggingface", formula="huggingface"),

    # AI21
    "j2-light": ModelInfo("j2-light", "ai21", formula="ai21"),
    "j2-mid": ModelInfo("j2-mid", "ai21", formula="ai21"),
    "j2-ultra": ModelInfo("j2-ultra", "ai21", formula="ai21"),
    "j2-jumbo-instruct": ModelInfo("j2-jumbo-instruct", "ai21", formula="ai21"),

    # Together
    "togethercomputer/RedPajama-INCITE-Chat-3B-v1": ModelInfo("togethercomputer/RedPajama-INCITE-Chat-3B-v1", "together", formula="together"),
    "togethercomputer/RedPajama-INCITE-Chat-7B-v1": ModelInfo("togethercomputer/RedPajama-INCITE-Chat-7B-v1", "together", formula="together"),
    "NousResearch/Nous-Hermes-Llama2-13b": ModelInfo("NousResearch/Nous-Hermes-Llama2-13b", "together", formula="together"),

    # xAI
    "grok-1": ModelInfo("grok-1", "xai", formula="xai"),
    "grok-1.5": ModelInfo("grok-1.5", "xai", formula="xai"),
    "grok-2": ModelInfo("grok-2", "xai", formula="xai"),
    "grok-beta": ModelInfo("grok-beta", "xai", formula="xai"),

    # Alibaba
    "qwen-1.5-0.5b": ModelInfo("qwen-1.5-0.5b", "alibaba", formula="alibaba"),
    "qwen-1.5-1.8b": ModelInfo("qwen-1.5-1.8b", "alibaba", formula="alibaba"),
    "qwen-1.5-4b": ModelInfo("qwen-1.5-4b", "alibaba", formula="alibaba"),
    "qwen-1.5-7b": ModelInfo("qwen-1.5-7b", "alibaba", formula="alibaba"),
    "qwen-1.5-14b": ModelInfo("qwen-1.5-14b", "alibaba", formula="alibaba"),
    "qwen-1.5-32b": ModelInfo("qwen-1.5-32b", "alibaba", formula="alibaba"),
    "qwen-1.5-72b": ModelInfo("qwen-1.5-72b", "alibaba", formula="alibaba"),
    "qwen-1.5-110b": ModelInfo("qwen-1.5-110b", "alibaba", formula="alibaba"),
    "qwen-2-0.5b": ModelInfo("qwen-2-0.5b", "alibaba", formula="alibaba"),
    "qwen-2-1.5b": ModelInfo("qwen-2-1.5b", "alibaba", formula="alibaba"),
    "qwen-2-7b": ModelInfo("qwen-2-7b", "alibaba", formula="alibaba"),
    "qwen-2-57b": ModelInfo("qwen-2-57b", "alibaba", formula="alibaba"),
    "qwen-2-72b": ModelInfo("qwen-2-72b", "alibaba", formula="alibaba"),
    "qwen-vl": ModelInfo("qwen-vl", "alibaba", formula="alibaba"),
    "qwen-vl-chat": ModelInfo("qwen-vl-chat", "alibaba", formula="alibaba"),
    "qwen-vl-plus": ModelInfo("qwen-vl-plus", "alibaba", formula="alibaba"),
    "qwen-2.5-72b": ModelInfo("qwen-2.5-72b", "alibaba", formula="alibaba"),
    "qwen-2.5-32b": ModelInfo("qwen-2.5-32b", "alibaba", formula="alibaba"),
    "qwen-2.5-14b": ModelInfo("qwen-2.5-14b", "alibaba", formula="alibaba"),
    "qwen-2.5-7b": ModelInfo("qwen-2.5-7b", "alibaba", formula="alibaba"),

    # Baidu
    "ernie-4.0": ModelInfo("ernie-4.0", "baidu", formula="baidu"),
    "ernie-3.5": ModelInfo("ernie-3.5", "baidu", formula="baidu"),
    "ernie-3.0": ModelInfo("ernie-3.0", "baidu", formula="baidu"),
    "ernie-speed": ModelInfo("ernie-speed", "baidu", formula="baidu"),
    "ernie-lite": ModelInfo("ernie-lite", "baidu", formula="baidu"),
    "ernie-tiny": ModelInfo("ernie-tiny", "baidu", formula="baidu"),
    "ernie-bot": ModelInfo("ernie-bot", "baidu", formula="baidu"),
    "ernie-bot-4": ModelInfo("ernie-bot-4", "baidu", formula="baidu"),

    # Huawei
    "pangu-alpha-2.6b": ModelInfo("pangu-alpha-2.6b", "huawei", formula="huawei"),
    "pangu-alpha-13b": ModelInfo("pangu-alpha-13b", "huawei", formula="huawei"),
    "pangu-alpha-200b": ModelInfo("pangu-alpha-200b", "huawei", formula="huawei"),
    "pangu-coder": ModelInfo("pangu-coder", "huawei", formula="huawei"),
    "pangu-coder-15b": ModelInfo("pangu-coder-15b", "huawei", formula="huawei"),

    # Yandex
    "yalm-100b": ModelInfo("yalm-100b", "yandex", formula="yandex"),
    "yalm-200b": ModelInfo("yalm-200b", "yandex", formula="yandex"),
    "yagpt": ModelInfo("yagpt", "yandex", formula="yandex"),
    "yagpt-2": ModelInfo("yagpt-2", "yandex", formula="yandex"),

    # Stability
    "stablelm-alpha-3b": ModelInfo("stablelm-alpha-3b", "stability", formula="stability"),
    "stablelm-alpha-7b": ModelInfo("stablelm-alpha-7b", "stability", formula="stability"),
    "stablelm-base-alpha-3b": ModelInfo("stablelm-base-alpha-3b", "stability", formula="stability"),
    "stablelm-base-alpha-7b": ModelInfo("stablelm-base-alpha-7b", "stability", formula="stability"),
    "stablelm-tuned-alpha-3b": ModelInfo("stablelm-tuned-alpha-3b", "stability", formula="stability"),
    "stablelm-tuned-alpha-7b": ModelInfo("stablelm-tuned-alpha-7b", "stability", formula="stability"),
    "stablelm-zephyr-3b": ModelInfo("stablelm-zephyr-3b", "stability", formula="stability"),

    # TII
    "falcon-7b": ModelInfo("falcon-7b", "tii", formula="tii"),
    "falcon-7b-instruct": ModelInfo("falcon-7b-instruct", "tii", formula="tii"),
    "falcon-40b": ModelInfo("falcon-40b", "tii", formula="tii"),
    "falcon-40b-instruct": ModelInfo("falcon-40b-instruct", "tii", formula="tii"),
    "falcon-180b": ModelInfo("falcon-180b", "tii", formula="tii"),
    "falcon-180b-chat": ModelInfo("falcon-180b-chat", "tii", formula="tii"),

    # EleutherAI
    "gpt-neo-125m": ModelInfo("gpt-neo-125m", "eleutherai", formula="eleutherai"),
    "gpt-neo-1.3b": ModelInfo("gpt-neo-1.3b", "eleutherai", formula="eleutherai"),
    "gpt-neo-2.7b": ModelInfo("gpt-neo-2.7b", "eleutherai", formula="eleutherai"),
    "gpt-neox-20b": ModelInfo("gpt-neox-20b", "eleutherai", formula="eleutherai"),
    "pythia-70m": ModelInfo("pythia-70m", "eleutherai", formula="eleutherai"),
    "pythia-160m": ModelInfo("pythia-160m", "eleutherai", formula="eleutherai"),
    "pythia-410m": ModelInfo("pythia-410m", "eleutherai", formula="eleutherai"),
    "pythia-1b": ModelInfo("pythia-1b", "eleutherai", formula="eleutherai"),
    "pythia-1.4b": ModelInfo("pythia-1.4b", "eleutherai", formula="eleutherai"),
    "pythia-2.8b": ModelInfo("pythia-2.8b", "eleutherai", formula="eleutherai"),
    "pythia-6.9b": ModelInfo("pythia-6.9b", "eleutherai", formula="eleutherai"),
    "pythia-12b": ModelInfo("pythia-12b", "eleutherai", formula="eleutherai"),

    # MosaicML
    "mpt-7b": ModelInfo("mpt-7b", "mosaicml", formula="mosaicml"),
    "mpt-7b-chat": ModelInfo("mpt-7b-chat", "mosaicml", formula="mosaicml"),
    "mpt-7b-instruct": ModelInfo("mpt-7b-instruct", "mosaicml", formula="mosaicml"),
    "mpt-30b": ModelInfo("mpt-30b", "mosaicml", formula="mosaicml"),
    "mpt-30b-chat": ModelInfo("mpt-30b-chat", "mosaicml", formula="mosaicml"),
    "mpt-30b-instruct": ModelInfo("mpt-30b-instruct", "mosaicml", formula="mosaicml"),

    # Replit
    "replit-code-v1-3b": ModelInfo("replit-code-v1-3b", "replit", formula="replit"),
    "replit-code-v1.5-3b": ModelInfo("replit-code-v1.5-3b", "replit", formula="replit"),
    "replit-code-v2-3b": ModelInfo("replit-code-v2-3b", "replit", formula="replit"),

    # MiniMax
    "abab5.5-chat": ModelInfo("abab5.5-chat", "minimax", formula="minimax"),
    "abab5.5s-chat": ModelInfo("abab5.5s-chat", "minimax", formula="minimax"),
    "abab6-chat": ModelInfo("abab6-chat", "minimax", formula="minimax"),
    "abab6.5-chat": ModelInfo("abab6.5-chat", "minimax", formula="minimax"),
    "abab6.5s-chat": ModelInfo("abab6.5s-chat", "minimax", formula="minimax"),
    "minimax-m2.5": ModelInfo("minimax-m2.5", "minimax", formula="minimax_m25"),

    # Aleph Alpha
    "luminous-base": ModelInfo("luminous-base", "aleph_alpha", formula="aleph_alpha"),
    "luminous-extended": ModelInfo("luminous-extended", "aleph_alpha", formula="aleph_alpha"),
    "luminous-supreme": ModelInfo("luminous-supreme", "aleph_alpha", formula="aleph_alpha"),
    "luminous-supreme-control": ModelInfo("luminous-supreme-control", "aleph_alpha", formula="aleph_alpha"),

    # DeepSeek
    "deepseek-coder-1.3b": ModelInfo("deepseek-coder-1.3b", "deepseek", formula="deepseek"),
    "deepseek-coder-6.7b": ModelInfo("deepseek-coder-6.7b", "deepseek", formula="deepseek"),
    "deepseek-coder-33b": ModelInfo("deepseek-coder-33b", "deepseek", formula="deepseek"),
    "deepseek-coder-instruct": ModelInfo("deepseek-coder-instruct", "deepseek", formula="deepseek"),
    "deepseek-vl-1.3b": ModelInfo("deepseek-vl-1.3b", "deepseek", formula="deepseek"),
    "deepseek-vl-7b": ModelInfo("deepseek-vl-7b", "deepseek", formula="deepseek"),
    "deepseek-llm-7b": ModelInfo("deepseek-llm-7b", "deepseek", formula="deepseek"),
    "deepseek-llm-67b": ModelInfo("deepseek-llm-67b", "deepseek", formula="deepseek"),
    "deepseek-v3": ModelInfo("deepseek-v3", "deepseek", formula="deepseek"),
    "deepseek-v3-base": ModelInfo("deepseek-v3-base", "deepseek", formula="deepseek"),
    "deepseek-v3.2": ModelInfo("deepseek-v3.2", "deepseek", formula="deepseek"),

    # Tsinghua
    "chatglm-6b": ModelInfo("chatglm-6b", "tsinghua", formula="tsinghua"),
    "chatglm2-6b": ModelInfo("chatglm2-6b", "tsinghua", formula="tsinghua"),
    "chatglm3-6b": ModelInfo("chatglm3-6b", "tsinghua", formula="tsinghua"),
    "glm-4": ModelInfo("glm-4", "tsinghua", formula="tsinghua"),
    "glm-4v": ModelInfo("glm-4v", "tsinghua", formula="tsinghua"),
    "glm-5": ModelInfo("glm-5", "tsinghua", formula="glm5"),

    # Volcengine (Doubao)
    "doubao-seed-2-0-pro": ModelInfo("doubao-seed-2-0-pro", "volcengine", formula="volcengine"),

    # Moonshot (Kimi)
    "kimi-k2.5": ModelInfo("kimi-k2.5", "moonshot", formula="moonshot"),

    # RWKV
    "rwkv-4-169m": ModelInfo("rwkv-4-169m", "rwkv", formula="rwkv"),
    "rwkv-4-430m": ModelInfo("rwkv-4-430m", "rwkv", formula="rwkv"),
    "rwkv-4-1b5": ModelInfo("rwkv-4-1b5", "rwkv", formula="rwkv"),
    "rwkv-4-3b": ModelInfo("rwkv-4-3b", "rwkv", formula="rwkv"),
    "rwkv-4-7b": ModelInfo("rwkv-4-7b", "rwkv", formula="rwkv"),
    "rwkv-4-14b": ModelInfo("rwkv-4-14b", "rwkv", formula="rwkv"),
    "rwkv-5-world": ModelInfo("rwkv-5-world", "rwkv", formula="rwkv"),

    # Community
    "vicuna-7b": ModelInfo("vicuna-7b", "community", formula="community"),
    "vicuna-13b": ModelInfo("vicuna-13b", "community", formula="community"),
    "vicuna-33b": ModelInfo("vicuna-33b", "community", formula="community"),
    "alpaca-7b": ModelInfo("alpaca-7b", "community", formula="community"),
    "alpaca-13b": ModelInfo("alpaca-13b", "community", formula="community"),
    "wizardlm-7b": ModelInfo("wizardlm-7b", "community", formula="community"),
    "wizardlm-13b": ModelInfo("wizardlm-13b", "community", formula="community"),
    "wizardlm-30b": ModelInfo("wizardlm-30b", "community", formula="community"),
    "orca-mini-3b": ModelInfo("orca-mini-3b", "community", formula="community"),
    "orca-mini-7b": ModelInfo("orca-mini-7b", "community", formula="community"),
    "orca-mini-13b": ModelInfo("orca-mini-13b", "community", formula="community"),
    "zephyr-7b-alpha": ModelInfo("zephyr-7b-alpha", "community", formula="community"),
    "zephyr-7b-beta": ModelInfo("zephyr-7b-beta", "community", formula="community"),

    # Microsoft
    "phi-3-mini": ModelInfo("phi-3-mini", "microsoft", formula="microsoft"),
    "phi-3-small": ModelInfo("phi-3-small", "microsoft", formula="microsoft"),
    "phi-3-medium": ModelInfo("phi-3-medium", "microsoft", formula="microsoft"),
    "phi-3.5-mini": ModelInfo("phi-3.5-mini", "microsoft", formula="microsoft"),

    # Amazon
    "titan-text-express": ModelInfo("titan-text-express", "amazon", formula="amazon"),
    "titan-text-lite": ModelInfo("titan-text-lite", "amazon", formula="amazon"),
    "titan-embed-text": ModelInfo("titan-embed-text", "amazon", formula="amazon"),

    # Nvidia
    "nemotron-4-340b": ModelInfo("nemotron-4-340b", "nvidia", formula="nvidia"),
    "nemotron-3-8b": ModelInfo("nemotron-3-8b", "nvidia", formula="nvidia"),

    # IBM
    "granite-13b-chat": ModelInfo("granite-13b-chat", "ibm", formula="ibm"),
    "granite-13b-instruct": ModelInfo("granite-13b-instruct", "ibm", formula="ibm"),
    "granite-20b-code": ModelInfo("granite-20b-code", "ibm", formula="ibm"),

    # Salesforce
    "codegen-16b": ModelInfo("codegen-16b", "salesforce", formula="salesforce"),
    "codegen-6b": ModelInfo("codegen-6b", "salesforce", formula="salesforce"),
    "codegen-2b": ModelInfo("codegen-2b", "salesforce", formula="salesforce"),

    # BigCode
    "starcoder": ModelInfo("starcoder", "bigcode", formula="bigcode"),
    "starcoder2-15b": ModelInfo("starcoder2-15b", "bigcode", formula="bigcode"),
    "starcoderbase": ModelInfo("starcoderbase", "bigcode", formula="bigcode"),
    "starcoder2-3b": ModelInfo("starcoder2-3b", "bigcode", formula="bigcode"),
    "starcoder2-7b": ModelInfo("starcoder2-7b", "bigcode", formula="bigcode"),
    "starcoder-plus": ModelInfo("starcoder-plus", "bigcode", formula="bigcode"),
    "starcoderbase-1b": ModelInfo("starcoderbase-1b", "bigcode", formula="bigcode"),
    "starcoderbase-3b": ModelInfo("starcoderbase-3b", "bigcode", formula="bigcode"),
    "starcoderbase-7b": ModelInfo("starcoderbase-7b", "bigcode", formula="bigcode"),

    # Databricks
    "dbrx": ModelInfo("dbrx", "databricks", formula="databricks"),
    "dbrx-instruct": ModelInfo("dbrx-instruct", "databricks", formula="databricks", pricing_id="dbrx-instruct"),
    "dbrx-base": ModelInfo("dbrx-base", "databricks", formula="databricks", pricing_id="dbrx-base"),
    "dolly-v2-12b": ModelInfo("dolly-v2-12b", "databricks", formula="databricks", pricing_id="dolly-v2-12b"),
    "dolly-v2-7b": ModelInfo("dolly-v2-7b", "databricks", formula="databricks", pricing_id="dolly-v2-7b"),
    "dolly-v2-3b": ModelInfo("dolly-v2-3b", "databricks", formula="databricks", pricing_id="dolly-v2-3b"),

    # Voyage
    "voyage-2": ModelInfo("voyage-2", "voyage", formula="voyage", pricing_id="voyage-2"),
    "voyage-large-2": ModelInfo("voyage-large-2", "voyage", formula="voyage", pricing_id="voyage-large-2"),
    "voyage-code-2": ModelInfo("voyage-code-2", "voyage", formula="voyage", pricing_id="voyage-code-2"),
    "voyage-finance-2": ModelInfo("voyage-finance-2", "voyage", formula="voyage", pricing_id="voyage-finance-2"),
    "voyage-law-2": ModelInfo("voyage-law-2", "voyage", formula="voyage", pricing_id="voyage-law-2"),
    "voyage-multilingual-2": ModelInfo("voyage-multilingual-2", "voyage", formula="voyage", pricing_id="voyage-multilingual-2"),
}


def _build_alias_map(models: Iterable[ModelInfo]) -> Dict[str, str]:
    alias_map: Dict[str, str] = {}
    for model in models:
        if model.aliases:
            for alias in model.aliases:
                alias_map[normalize_model_name(alias)] = model.name
    return alias_map


ALIASES: Dict[str, str] = _build_alias_map(MODELS.values())
MODEL_LOOKUP: Dict[str, ModelInfo] = {normalize_model_name(k): v for k, v in MODELS.items()}
MODEL_LOOKUP.update({alias: MODELS[target] for alias, target in ALIASES.items()})

# All normalized model names for fuzzy matching
_ALL_NORMALIZED_NAMES: List[str] = list(MODEL_LOOKUP.keys())


def _extract_model_part(name: str) -> str:
    """Extract model part from 'provider/model' or 'provider:model' format."""
    name = name.strip()
    for sep in ("/", ":"):
        if sep in name:
            return name.split(sep, 1)[-1].strip()
    return name


def _fuzzy_match_model(model_name: str) -> Optional[ModelInfo]:
    """Fuzzy match model name when exact lookup fails."""
    normalized = normalize_model_name(model_name)
    model_part = normalize_model_name(_extract_model_part(model_name))

    # 1. Try model part only (e.g. anthropic/claude-sonnet-4-6 -> claude-sonnet-4-6)
    if model_part != normalized:
        info = MODEL_LOOKUP.get(model_part)
        if info:
            return info

    # 2. Substring match: input contains a known model, or known model contains input
    for key, info in MODEL_LOOKUP.items():
        if model_part in key or key in model_part:
            return info

    # 3. difflib fuzzy match (cutoff 0.5 = 50% similarity)
    candidates = difflib.get_close_matches(model_part, _ALL_NORMALIZED_NAMES, n=1, cutoff=0.5)
    if candidates:
        return MODEL_LOOKUP.get(candidates[0])

    # 4. Relaxed: match key parts (e.g. claude-sonnet-4 matches claude-3.5-sonnet)
    model_tokens = set(re.split(r"[-_.]", model_part)) - {""}
    for key in _ALL_NORMALIZED_NAMES:
        key_tokens = set(re.split(r"[-_.]", key)) - {""}
        overlap = len(model_tokens & key_tokens) / max(len(model_tokens), 1)
        if overlap >= 0.6:
            return MODEL_LOOKUP.get(key)

    return None


def get_model_info(model_name: str) -> Optional[ModelInfo]:
    info = MODEL_LOOKUP.get(normalize_model_name(model_name))
    if info:
        return info
    return _fuzzy_match_model(model_name)


def get_all_supported_models() -> List[str]:
    return sorted(set(MODELS.keys()))


def get_supported_models_by_provider() -> Dict[str, List[str]]:
    models_by_provider: Dict[str, List[str]] = {}
    for model in MODELS.values():
        models_by_provider.setdefault(model.provider, []).append(model.name)
    for provider, models in models_by_provider.items():
        models_by_provider[provider] = sorted(set(models))
    return dict(sorted(models_by_provider.items()))

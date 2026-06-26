# LLM interface — depends on core
import json
import re
import subprocess
import urllib.request
from pathlib import Path
from typing import Optional

from .core import *


def get_openclaw_llm_config() -> dict:
    """Read LLM config from openclaw models.json."""
    config = {
        "api_key": "",
        "base_url": "",
        "model": "MiniMax-M2",
    }
    # Check environment overrides
    import os
    for key in ("MINIMAX_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"):
        if os.environ.get(key):
            config["api_key"] = os.environ[key]
    for key in ("MINIMAX_BASE_URL", "OPENAI_BASE_URL", "ANTHROPIC_BASE_URL"):
        if os.environ.get(key):
            config["base_url"] = os.environ[key]
    for key in ("MINIMAX_MODEL", "OPENAI_MODEL", "ANTHROPIC_MODEL"):
        if os.environ.get(key):
            config["model"] = os.environ[key]
    # Read from models.json
    models_file = Path.home() / ".openclaw" / "agents" / "main" / "agent" / "models.json"
    if models_file.exists():
        try:
            data = json.loads(models_file.read_text())
            providers = data.get("providers", {})
            for pkey in ("minimax", "openai", "anthropic"):
                prov = providers.get(pkey, {})
                if prov.get("apiKey"):
                    config["api_key"] = prov["apiKey"]
                if prov.get("baseUrl"):
                    config["base_url"] = prov["baseUrl"]
                    if not config["base_url"].endswith("/"):
                        config["base_url"] += "/"
                if prov.get("model"):
                    config["model"] = prov["model"]
        except Exception:
            pass
    return config


def call_llm(prompt: str, system: str = "", model: str = "",
              base_url: str = "", api_key: str = "",
              temperature: float = 0.3) -> str:
    """Call LLM API (Anthropic/OpenAI compatible)."""
    if not base_url or not api_key:
        config = get_openclaw_llm_config()
        base_url = base_url or config["base_url"]
        api_key = api_key or config["api_key"]
        model = model or config.get("model", "MiniMax-M2")
    if not base_url or not api_key:
        return ""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = json.dumps({
        "model": model or "MiniMax-M2",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 16000,
    }).encode("utf-8")
    endpoint = base_url.rstrip("/") + "/v1/messages"
    try:
        req = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if "anthropic" in endpoint:
                text_blocks = [
                    b.get("text", "") for b in data.get("content", [])
                    if b.get("type") == "text" and b.get("text", "").strip()
                ]
                if text_blocks:
                    content = max(text_blocks, key=len)
                else:
                    thinking_blocks = [
                        b.get("thinking", "") for b in data.get("content", [])
                        if b.get("type") == "thinking" and b.get("thinking", "").strip()
                    ]
                    content = "\n".join(thinking_blocks)
            else:
                content = (
                    data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                )
            return _strip_code_fences(content)
    except Exception:
        return ""


def _strip_code_fences(text: str) -> str:
    """
    Strip markdown code fences and prose from LLM output.
    
    Handles cases where LLM returns prose instead of code. Uses statistical
    detection (code-like line ratio) and pattern matching.
    """
    if not text:
        return ""
    lines = text.strip().split("\n")
    # Remove leading/trailing fence lines
    while lines and "```" in lines[0]:
        lines = lines[1:]
    while lines and "```" in lines[-1]:
        lines = lines[:-1]
    content = "\n".join(lines).strip()
    if not content:
        return ""
    code_indicators = [
        "def ", "class ", "import ", "from ", "if ", "else:",
        "return ", "for ", "while ", "async ", "@",
        "const ", "let ", "function ", "fn ", "func ",
        "package ", "export ", "module ",
    ]
    non_empty_lines = [l for l in lines if l.strip()]
    # If less than 30% of non-empty lines are code-like, try to find code start
    prose_lines = sum(
        1 for l in non_empty_lines
        if not any(l.strip().startswith(ind) for ind in code_indicators)
    )
    total = len(non_empty_lines)
    if total > 5 and (total - prose_lines) / total < 0.3:
        for i, line in enumerate(non_empty_lines):
            stripped = line.strip()
            if any(stripped.startswith(ind) for ind in code_indicators):
                # Take from first code line onward, then re-check ratio
                code_block = "\n".join(non_empty_lines[i:]).strip()
                block_lines = [l for l in code_block.splitlines() if l.strip()]
                if not block_lines:
                    return ""
                block_prose = sum(
                    1 for l in block_lines
                    if not any(l.strip().startswith(ind) for ind in code_indicators)
                )
                # If more than 50% of the "code block" is prose, reject
                if block_prose / len(block_lines) > 0.5:
                    return ""
                return code_block
        return ""
    return content


def call_llm_with_retry(
    prompt: str,
    system: str = "",
    model: str = "",
    base_url: str = "",
    api_key: str = "",
    temperature: float = 0.3,
    max_retries: int = 2,
) -> str:
    """
    Call LLM with retry on prose/empty response.
    
    Retries once with a stricter system prompt if the first response
    appears to be prose rather than code.
    """
    for attempt in range(max_retries):
        result = call_llm(
            prompt=prompt,
            system=system,
            model=model,
            base_url=base_url,
            api_key=api_key,
            temperature=temperature,
        )
        if result.strip() and result.strip() != "EMPTY":
            return result
        if attempt == 0:
            # Retry with stricter system prompt
            strict_system = (
                (system + "\n\n" if system else "")
                + "CRITICAL: You must output ONLY code. "
                "Start with 'def ' or 'class ' or equivalent. "
                "Do not write any explanation or description."
            )
            system = strict_system
    return ""


def analyze_with_llm(code_snippet: str, context: str, repo_path: str = "") -> dict:
    """Analyze code snippet and return suggestion via LLM."""
    config = get_openclaw_llm_config()
    if not config["api_key"] or not config["base_url"]:
        return {"suggestion": "", "risk_level": "medium",
                "implementation_hint": "", "available": False}
    # Detect language from file path
    lang = "python"
    if repo_path:
        ext = Path(repo_path).suffix.lower()
        lang_map = {".py": "python", ".js": "javascript", ".ts": "typescript",
                    ".go": "go", ".rs": "rust", ".java": "java",
                    ".cpp": "cpp", ".c": "c", ".cs": "csharp"}
        lang = lang_map.get(ext, "text")
    system = (
        "You are a senior code reviewer. Return valid JSON with keys: "
        "suggestion, risk_level, implementation_hint. Only JSON."
    )
    prompt = (
        "Context: " + context + "\n\nCode:\n```" + lang + "\n"
        + code_snippet[:2000] + "\n```"
    )
    result = call_llm(prompt=prompt, system=system, model=config["model"],
                     base_url=config["base_url"], api_key=config["api_key"])
    if not result:
        return {"suggestion": "", "risk_level": "medium",
                "implementation_hint": "", "available": False}
    try:
        parsed = json.loads(result)
        parsed["available"] = True
        return parsed
    except json.JSONDecodeError:
        m = re.search(r'\{[^{}]*\}', result, re.DOTALL)
        if m:
            try:
                parsed = json.loads(m.group())
                parsed["available"] = True
                return parsed
            except Exception:
                pass
        return {"suggestion": result.strip()[:200], "risk_level": "medium",
                "implementation_hint": "", "available": True}

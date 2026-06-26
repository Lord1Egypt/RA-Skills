#!/usr/bin/env python3
"""
批量测试多个模型的 token 与文字比例。
- API 模式：通过请求模型 API 获取 token 数（需配置 API_KEY、BASE_URL）
- 本地模式（--local）：使用本项目的 TokenCounter 近似计算，无需 API
"""
import argparse
import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# 测试文本：包含中文、英文、符号（使用 r 前缀避免 \U \u 等被当作转义）
SAMPLE_TEXT = r"""
---
name: prompt-token-counter
description: "Count tokens and estimate costs for 300+ LLM models. Primary use: audit OpenClaw workspace token consumption (memory, persona, skills)."
trigger: "token count, cost estimate, prompt length, API cost, OpenClaw audit, workspace token usage, memory/persona/skills tokens, context window limit"
---

# Prompt Token Counter (toksum)

> **First load reminder:** This skill provides the `scripts` CLI (toksum). Use it when the user asks to count tokens, estimate API costs, or **audit OpenClaw component token consumption** (memory, persona, skills).

## Primary Use: OpenClaw Token Consumption Audit

**Goal:** Help users identify which OpenClaw components consume tokens and how much.

### 1. Memory & Persona Files

These files are injected into sessions and consume tokens. Search and count them:

| File | Purpose | Typical Location |
|------|---------|------------------|
| `AGENTS.md` | Operating instructions, workflow, priorities | `~/.openclaw/workspace/` |
| `SOUL.md` | Persona, tone, values, behavioral guidelines | `~/.openclaw/workspace/` |
| `IDENTITY.md` | Name, role, goals, visual description | `~/.openclaw/workspace/` |
| `USER.md` | User preferences, communication style | `~/.openclaw/workspace/` |
| `MEMORY.md` | Long-term memory, persistent facts | `~/.openclaw/workspace/` |
| `TOOLS.md` | Tool quirks, path conventions | `~/.openclaw/workspace/` |
| `HEARTBEAT.md` | Periodic maintenance checklist | `~/.openclaw/workspace/` |
| `BOOT.md` | Startup ritual (when hooks enabled) | `~/.openclaw/workspace/` |
| `memory/YYYY-MM-DD.md` | Daily memory logs | `~/.openclaw/workspace/memory/` |

**Workspace path:** Default `~/.openclaw/workspace`; may be overridden in `~/.openclaw/openclaw.json` via `agent.workspace`.

### 2. Skill Files (SKILL.md)

Skills are loaded per session. Count each `SKILL.md`:

| Location | Scope |
|----------|-------|
| `~/.openclaw/skills/*/SKILL.md` | OpenClaw managed skills |
| `~/.openclaw/workspace/skills/*/SKILL.md` | Workspace-specific skills (override) |

### 3. Audit Workflow

1. **Locate workspace:** Resolve `~/.openclaw/workspace` (or config override).
2. **Collect files:** List all memory/persona files and `SKILL.md` paths above.
3. **Count tokens:** For each file, run `python -m scripts.cli -f <path> -m <model> -c`.
4. **Summarize:** Group by category (memory, persona, skills), report total and per-file.

**Example audit command (PowerShell):**
```powershell
$ws = "$env:USERPROFILE\.openclaw\workspace"
python -m scripts.cli -m gpt-4o -c -f "$ws\AGENTS.md" -f "$ws\SOUL.md" -f "$ws\USER.md" -f "$ws\IDENTITY.md" -f "$ws\MEMORY.md" -f "$ws\TOOLS.md"
```

**Example audit (Bash):**
```bash
WS=~/.openclaw/workspace
python -m scripts.cli -m gpt-4o -c -f "$WS/AGENTS.md" -f "$WS/SOUL.md" -f "$WS/USER.md" -f "$WS/IDENTITY.md" -f "$WS/MEMORY.md" -f "$WS/TOOLS.md"
```

---

## Project Layout

```
prompt_token_counter/
├── SKILL.md
├── package.json                # npm package (OpenClaw skill)
├── publish_npm.py               # Publish to npm; syncs version
└── scripts/                    # Python package, CLI + examples
    ├── cli.py                  # Entry point
    ├── core.py                 # TokenCounter, estimate_cost
    ├── registry/
    │   ├── models.py           # 300+ models
    │   └── pricing.py          # Pricing data
    └── examples/               # Script examples
        ├── count_prompt.py
        ├── estimate_cost.py
        ├── batch_compare.py
        └── benchmark_token_ratio.py
```

Invoke: `python -m scripts.cli` from project root.

### Version Sync (publish_npm.py)

When publishing to npm, `publish_npm.py` bumps the patch version and syncs it to:

- `package.json` — `version`
- `SKILL.md` — frontmatter `version`
- `scripts/__init__.py` — `__version__`

Run: `python publish_npm.py` (after `npm login`).

---

## Runtime Dependencies

- **Python 3** — required
- **tiktoken** (optional) — `pip install tiktoken` for exact OpenAI counts

---

## Language Rule

**Respond in the user's language.** Match the user's language (e.g. Chinese if they write in Chinese, English if they write in English).

---

## URL Usage — Mandatory Agent Rule

**Before using `-u` / `--url` to fetch content from any URL, you MUST:**

1. **Explicitly warn the user** that the CLI will make an outbound HTTP/HTTPS request to the given URL.
2. **Confirm the URL is trusted** — tell the user: "Only use URLs you fully trust. Untrusted URLs may expose your IP, leak data, or be used for SSRF. Do you confirm this URL is safe?"
3. **Prefer alternatives** — if the user can provide the content via `-f` (local file) or inline text, suggest that instead of URL fetch.
4. **Never auto-fetch** — do not invoke `-u` without the user having explicitly provided the URL and acknowledged the risk.

**If the user insists on using a URL:** Proceed only after they confirm. State clearly: "I will fetch from [URL] to count tokens. Proceed?"

---

## Model Name — Mandatory Agent Rule

**Before invoking the CLI, you MUST have a concrete model name from the user.**

1. **Require explicit model** — `-m` / `--model` is required. Do not guess or assume; the user must provide the exact name (e.g. gpt-4o, claude-3-5-sonnet-20241022).
2. **If unclear, ask** — if the user says "GPT" or "Claude" or "the latest model" without a specific name, ask: "Please specify the exact model name (e.g. gpt-4o, claude-3-5-sonnet-20241022). Run `python -m scripts.cli -l` to list supported models."
3. **Do not auto-pick** — never substitute a model on behalf of the user without their confirmation.
4. **Validate when possible** — if the model name seems ambiguous, offer `-l` output or confirm: "I'll use [model]. Is that correct?"

---

## CLI Usage

```bash
python -m scripts.cli [OPTIONS] [TEXT ...]
```

| Option | Short | Description |
|--------|-------|-------------|
| `--model` | `-m` | Model name (required unless `--list-models`) — **Agent must obtain exact name from user; ask if unclear** |
| `--file` | `-f` | Read from file (repeatable) |
| `--url` | `-u` | Read from URL (repeatable) — **Agent must warn user before use; only trusted URLs** |
| `--list-models` | `-l` | List supported models |
| `--cost` | `-c` | Show cost estimate |
| `--output-tokens` | | Use output token pricing |
| `--currency` | | USD or INR |
| `--verbose` | `-v` | Detailed output |

### Examples

```bash
# Inline text
python -m scripts.cli -m gpt-4 "Hello, world!"

# File with cost
python -m scripts.cli -f input.txt -m claude-3-opus -c

# Multiple files (OpenClaw audit)
python -m scripts.cli -v -c -f AGENTS.md -f SOUL.md -f MEMORY.md -m gpt-4o

# List models
python -m scripts.cli -l

# Run bundled example scripts
python scripts/examples/count_prompt.py "Hello, world!" gpt-4
python scripts/examples/estimate_cost.py "Your text" gpt-4
python scripts/examples/batch_compare.py "Compare text" gpt-4 claude-3-opus
```

---

## Python API

```python
from scripts import TokenCounter, count_tokens, estimate_cost, get_supported_models

tokens = count_tokens("Hello!", "gpt-4")
counter = TokenCounter("claude-3-opus")
tokens = counter.count_messages([
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
])
cost = estimate_cost(tokens, "gpt-4", input_tokens=True)
```

---

## Supported Models

300+ models across 34+ providers: OpenAI, Anthropic, Google, Meta, Mistral, Cohere, xAI, DeepSeek, etc. Use `python -m scripts.cli -l` for full list.

- **OpenAI:** exact via tiktoken
- **Others:** ~85–95% approximation

---

## Common Issues

| Issue | Action |
|-------|--------|
| "tiktoken is required" | `pip install tiktoken` |
| UnsupportedModelError | Use `-l` for valid names |
| Cost "NA" | Model has no pricing; count still valid |
| User provides URL | **Agent must warn:** outbound request, SSRF risk, only trusted URLs; confirm before `-u` |
| Model unclear / vague | **Agent must ask:** user to specify exact model name; offer `-l` to list; do not guess |

---

## When to Trigger This Skill

Activate this skill when the user:

| Trigger | Example phrases |
|---------|-----------------|
| **Token count** | "How many tokens?", "Count tokens in this prompt", "Token length of X" |
| **Cost estimate** | "Estimate API cost", "How much for this text?", "Cost for GPT-4" |
| **Prompt size** | "Check prompt length", "Is this too long?", "Context window limit" |
| **OpenClaw audit** | "How many tokens does my workspace use?", "Audit OpenClaw memory/persona/skills", "Which components consume tokens?", "Token usage of AGENTS.md / SOUL.md / skills" |
| **Model comparison** | "Compare token cost across models", "Which model is cheaper?" |

Also trigger when the agent needs to count tokens or estimate cost before/after generating content.

---

## Quick Reference

| Item | Command |
|------|---------|
| Invoke | `python -m scripts.cli` |
| List models | `python -m scripts.cli -l` |
| Cost | `-c` (input) / `--output-tokens` (output) |
| Currency | `--currency USD` or `INR` |
"""

# 待测试的模型列表（可按需修改）
MODELS = [
    "anthropic/claude-sonnet-4-6",
    "anthropic/claude-sonnet-4-5",
    "anthropic/claude-opus-4.6",
    "openai/gpt-5.2-codex",
    "google/gemini-3.1-pro-preview",
    "z-ai/glm-5",
    "volcengine/doubao-seed-2-0-pro",
    "moonshot/kimi-k2.5",
    "minimax/MiniMax-M2.5",
    "deepseek-v3.2",
]

# API 配置（与 skill_executor 保持一致，API 模式时使用）
API_KEY = ""
BASE_URL = ""


def get_token_count_local(model: str, text: str) -> dict:
    """使用本项目的 TokenCounter 本地近似计算 token 数。"""
    try:
        from scripts.core import TokenCounter

        counter = TokenCounter(model)
        token_count = counter.count(text)
    except Exception as e:
        return {
            "model": model,
            "success": False,
            "error": str(e),
            "char_count": len(text),
            "token_count": None,
            "ratio": None,
        }

    char_count = len(text)
    ratio = char_count / token_count if token_count > 0 else 0

    return {
        "model": model,
        "success": True,
        "char_count": char_count,
        "token_count": token_count,
        "ratio": round(ratio, 4),
        "ratio_desc": f"1 token ≈ {ratio:.4f} 字符",
    }


async def get_token_count_api(model: str, text: str) -> dict:
    """
    请求模型 API，获取输入文本的 token 数。
    使用 chat completion，从 response.usage.prompt_tokens 获取。
    依赖: pip install openai
    """
    try:
        import openai

        client = openai.AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)

        messages = [{"role": "user", "content": text}]
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=8 * 1024,  # 部分 API 要求 >= 16，只关心 prompt_tokens
            temperature=0,
        )

        usage = getattr(response, "usage", None)
        if usage is None:
            return {
                "model": model,
                "success": False,
                "error": "API 响应中无 usage 字段",
                "char_count": len(text),
                "token_count": None,
                "ratio": None,
            }

        prompt_tokens = getattr(usage, "prompt_tokens", None)
        if prompt_tokens is None:
            prompt_tokens = getattr(usage, "total_tokens", None)

        if prompt_tokens is None:
            return {
                "model": model,
                "success": False,
                "error": "usage 中无 prompt_tokens/total_tokens",
                "char_count": len(text),
                "token_count": None,
                "ratio": None,
            }

        char_count = len(text)
        ratio = char_count / prompt_tokens if prompt_tokens > 0 else 0

        return {
            "model": model,
            "success": True,
            "char_count": char_count,
            "token_count": prompt_tokens,
            "ratio": round(ratio, 4),
            "ratio_desc": f"1 token ≈ {ratio:.4f} 字符",
        }
    except Exception as e:
        return {
            "model": model,
            "success": False,
            "error": str(e),
            "char_count": len(text),
            "token_count": None,
            "ratio": None,
        }


async def batch_test_api(models: list[str], text: str) -> list[dict]:
    """批量异步请求所有模型（API 模式）。"""
    tasks = [get_token_count_api(m, text) for m in models]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    out = []
    for i, r in enumerate(results):
        if isinstance(r, Exception):
            out.append(
                {
                    "model": models[i],
                    "success": False,
                    "error": str(r),
                    "char_count": len(text),
                    "token_count": None,
                    "ratio": None,
                }
            )
        else:
            out.append(r)
    return out


def batch_test_local(models: list[str], text: str) -> list[dict]:
    """批量测试所有模型（本地模式）。"""
    return [get_token_count_local(m, text) for m in models]


def write_report(results: list[dict], text: str, output_path: Path, mode: str) -> None:
    """将测试结果写入 Markdown 文档。"""
    mode_label = "API" if mode == "api" else "本地近似"
    lines = [
        "# 模型 Token 与文字比例测试报告",
        "",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**测试字符数**: {len(text)}",
        f"**模式**: {mode_label}",
        "",
        "| 模型 | 字符数 | Token 数 | 1 token ≈ 多少字符 | 状态 |",
        "|------|--------|----------|-------------------|------|",
    ]

    for r in results:
        model = r.get("model", "-")
        char_count = r.get("char_count") or "-"
        token_count = r.get("token_count") if r.get("token_count") is not None else "-"
        ratio = r.get("ratio")
        ratio_str = f"{ratio:.4f}" if isinstance(ratio, (int, float)) else "-"
        status = "✓" if r.get("success") else f"✗ {r.get('error', '')}"
        lines.append(f"| {model} | {char_count} | {token_count} | {ratio_str} | {status} |")

    lines.extend(
        [
            "",
            "## 说明",
            "",
            "- **1 token ≈ 多少字符**：字符数 / token 数，数值越大表示 1 个 token 能表示更多文字",
            "- 中文通常比英文消耗更多 token",
            "- 不同模型使用不同 tokenizer，比例会有差异",
            "",
        ]
    )

    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"报告已保存: {output_path}")


def main(
    text: Optional[str] = None,
    text_file: Optional[Path] = None,
    models: Optional[list[str]] = None,
    output_path: Optional[Path] = None,
    use_local: bool = False,
) -> list[dict]:
    """
    主流程：批量测试并输出报告。

    Args:
        text: 测试文本，默认使用 SAMPLE_TEXT
        text_file: 从文件读取测试文本（覆盖 text）
        models: 模型列表，默认使用 MODELS
        output_path: 输出文件路径，默认 token_ratio_report.md
        use_local: True 使用本地 TokenCounter，False 使用 API
    """
    if text_file and text_file.exists():
        text = text_file.read_text(encoding="utf-8")
    elif text is None:
        text = SAMPLE_TEXT

    models = models or MODELS

    if output_path is None:
        output_path = Path(__file__).parent / "token_ratio_report.md"

    mode = "local" if use_local else "api"

    if use_local:
        print(f"本地模式：测试 {len(models)} 个模型，文本长度 {len(text)} 字符...")
        results = batch_test_local(models, text)
    else:
        try:
            import openai  # noqa: F401
        except ImportError:
            print("API 模式需要 openai: pip install openai")
            print("或使用 --local 进行本地近似测试")
            return []
        if not API_KEY or not BASE_URL:
            print("API 模式需在脚本中设置 API_KEY 和 BASE_URL")
            print("或使用 --local 进行本地近似测试")
            return []
        print(f"API 模式：测试 {len(models)} 个模型，文本长度 {len(text)} 字符...")
        results = asyncio.run(batch_test_api(models, text))

    for r in results:
        if r.get("success"):
            print(f"  {r['model']}: {r['token_count']} tokens, 1 token ≈ {r['ratio']:.4f} 字符")
        else:
            print(f"  {r['model']}: 失败 - {r.get('error', '')}")

    write_report(results, text, output_path, mode)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="批量测试模型 token 与文字比例")
    parser.add_argument("--local", action="store_true", help="使用本地 TokenCounter 近似（无需 API）")
    parser.add_argument("--text-file", "-f", type=Path, help="从文件读取测试文本")
    parser.add_argument("--output", "-o", type=Path, help="输出报告路径")
    args = parser.parse_args()

    # 确保从项目根目录运行时可导入 scripts
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    main(text_file=args.text_file, output_path=args.output, use_local=args.local)

#!/usr/bin/env python3
"""LLM 接入层（零内部依赖）。

三条原则
--------
1. 优先用 openai SDK；缺失时降级到标准库 urllib，协议完全一致
2. **配置只有一个文件：`~/.jubensha/config.json`**；没写的键用 DEFAULTS 补齐
3. 用量保险丝：只限单局调用次数（不限制单次输出，避免复杂回答被截断）

配置键名 = `DEFAULTS` 里的名字，不做别名兼容（写错就当没写，用默认值）。

用法
----
    python scripts/llm.py init      # 交互式写入 ~/.jubensha/config.json
    python scripts/llm.py show      # 打印当前生效配置（key 打码）
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request

DEFAULTS = {
    "base_url": "https://api.deepseek.com/v1",
    "api_key": "",
    "model": "deepseek-flash",
    "temperature_actor": 0.8,
    "temperature_router": 0.0,
    "timeout": 20,
    "retries": 2,
    "max_calls_per_game": 400,
}

# 不设 max_tokens：复杂问答（多问一答、长口径复述）需要输出空间，限长会截断。
# 用量控制只靠 max_calls_per_game。

# 唯一的配置文件。没写的键用 DEFAULTS 补齐。
USER_CFG = "~/.jubensha/config.json"

PRESETS = [
    ("DeepSeek", "https://api.deepseek.com/v1", "deepseek-flash", "推荐，最便宜"),
    ("OpenAI", "https://api.openai.com/v1", "gpt-4o-mini", ""),
    ("通义千问", "https://dashscope.aliyuncs.com/compatible-mode/v1", "qwen-plus", ""),
    ("Moonshot", "https://api.moonshot.cn/v1", "moonshot-v1-8k", ""),
    ("本地 Ollama", "http://localhost:11434/v1", "qwen2.5:7b", "免费，key 随便填"),
    ("自定义", "", "", "自己填 base_url"),
]


class BudgetExceeded(RuntimeError):
    pass


# ---------------------------------------------------------------- 配置


def _read_json(path: str) -> dict:
    try:
        with open(os.path.expanduser(path), encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def load_config() -> dict | None:
    """读 `~/.jubensha/config.json`；缺的键用 DEFAULTS 补齐。

    键名必须与 DEFAULTS 一致——不认识的键直接忽略（不做别名兼容）。
    没有 api_key 时返回 None，由调用方触发降级。
    """
    cfg = dict(DEFAULTS)
    for key, val in _read_json(USER_CFG).items():
        if key in DEFAULTS and val not in (None, ""):
            cfg[key] = val
    return cfg if cfg.get("api_key") else None


def unknown_keys() -> list[str]:
    """配置文件里不认识的键（给 show 提示用，不影响运行）。"""
    return sorted(k for k in _read_json(USER_CFG) if k not in DEFAULTS)


def config_status() -> tuple[bool, str]:
    """检查配置是否可用，返回 (ok, 原因)。用于启动时给用户明确提示。"""
    path = os.path.expanduser(USER_CFG)
    if not os.path.exists(path):
        return False, f"没有找到配置文件 {USER_CFG}"
    raw = _read_json(USER_CFG)
    if not str(raw.get("api_key") or "").strip():
        return False, f"{USER_CFG} 里缺少 api_key（当前只有：{', '.join(sorted(raw)) or '空'}）"
    # base_url 可不写，未写时用 DEFAULTS 里的默认值
    return True, "ok"


def setup_hint(reason: str) -> str:
    """未配置时的引导文案：告诉用户差什么、怎么补、以及可以先离线玩。"""
    return (
        "\n[需要先配置 LLM] " + reason + "\n\n"
        "（1）需要一份 OpenAI 兼容配置，只写这三个键就够：\n"
        "    ~/.jubensha/config.json\n"
        "    {\n"
        '      "base_url": "https://api.deepseek.com/v1",\n'
        '      "api_key": "sk-xxxxxxxx",\n'
        '      "model": "deepseek-flash"\n'
        "    }\n\n"
        "（2）两种补法：\n"
        "    python scripts/llm.py init        # 交互式生成（会试连通）\n"
        "    或手动创建上面的文件，然后 chmod 600 ~/.jubensha/config.json\n\n"
        "（3）暂时不想配 key：加 --mock 可以离线跑完一整局（不调用任何模型）。\n"
        "    检查当前配置：python scripts/llm.py show\n"
    )


def save_config(cfg: dict) -> str:
    path = os.path.expanduser(USER_CFG)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {k: cfg[k] for k in DEFAULTS if k in cfg}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.chmod(path, 0o600)
    return path


def mask(secret: str) -> str:
    s = str(secret or "")
    if len(s) <= 8:
        return "*" * len(s)
    return s[:4] + "*" * (len(s) - 8) + s[-4:]


# ---------------------------------------------------------------- 客户端


class ChatClient:
    """OpenAI 兼容客户端，自动在 SDK / urllib 之间切换。"""

    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.calls = 0
        self.mode = "sdk"
        # 有些兼容端点不支持 response_format，踩一次就不能再白付一次钱
        self.json_mode_supported = True
        try:
            from openai import OpenAI  # type: ignore

            self._sdk = OpenAI(
                base_url=cfg["base_url"],
                api_key=cfg["api_key"],
                timeout=cfg["timeout"],
                # 重试由我们自己的循环控制，否则 SDK 的 2 次重试会×超时
                # 叠加成几十秒到几分钟的等待（实测踩过：单轮跑到 16 分钟）
                max_retries=0,
            )
        except ImportError:
            self._sdk = None
            self.mode = "urllib"

    # -- 底层：一次 HTTP 调用 -------------------------------------
    def _post(self, payload: dict) -> dict:
        url = self.cfg["base_url"].rstrip("/") + "/chat/completions"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.cfg['api_key']}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.cfg["timeout"]) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _call_sdk(self, payload: dict) -> dict:
        resp = self._sdk.chat.completions.create(**payload)
        out = {
            "choices": [{"message": {"content": resp.choices[0].message.content}}],
            "usage": {},
        }
        usage = getattr(resp, "usage", None)
        if usage:
            out["usage"] = {
                "prompt_tokens": getattr(usage, "prompt_tokens", 0) or 0,
                "completion_tokens": getattr(usage, "completion_tokens", 0) or 0,
            }
        return out

    # -- 对外：文本 -----------------------------------------------
    def chat(
        self,
        messages: list[dict],
        temperature: float | None = None,
        max_tokens: int | None = None,
        json_mode: bool = False,
    ) -> str:
        if self.calls >= self.cfg["max_calls_per_game"]:
            raise BudgetExceeded(f"本局调用已达上限 {self.cfg['max_calls_per_game']} 次，已停止")

        payload = {
            "model": self.cfg["model"],
            "messages": messages,
            "temperature": (self.cfg["temperature_actor"] if temperature is None else temperature),
        }
        if max_tokens:  # 仅显式传入时才限制（默认不截断）
            payload["max_tokens"] = max_tokens
        if json_mode and self.json_mode_supported:
            payload["response_format"] = {"type": "json_object"}

        last_err = None
        for attempt in range(self.cfg["retries"] + 1):
            try:
                data = self._sdk_to_dict(payload)
                break
            except Exception as err:  # noqa: BLE001 - 网络/鉴权/限流统一重试
                last_err = err
                # JSON mode 不被支持时摘掉参数，并记住这一点不再重试
                if json_mode and "response_format" in payload:
                    self.json_mode_supported = False
                    payload.pop("response_format")
                    continue
                if attempt < self.cfg["retries"]:
                    time.sleep(1.5 * (attempt + 1))
        else:
            raise RuntimeError(f"LLM 调用失败：{last_err}")

        self.calls += 1
        try:
            return data["choices"][0]["message"]["content"] or ""
        except (KeyError, IndexError) as err:
            raise RuntimeError(f"响应格式异常：{data}") from err

    def _sdk_to_dict(self, payload: dict) -> dict:
        if self._sdk is not None:
            return self._call_sdk(payload)
        return self._post(payload)

    # -- 对外：JSON（三级降级） -----------------------------------
    def chat_json(
        self,
        messages: list[dict],
        schema_hint: str = "",
        max_tokens: int | None = None,
    ) -> dict:
        text = self.chat(messages, json_mode=True, max_tokens=max_tokens)
        for _ in range(2):
            data = _extract_json(text)
            if data is not None:
                return data
            text = self.chat(
                messages
                + [
                    {"role": "assistant", "content": text},
                    {
                        "role": "user",
                        "content": f"上面的输出不是合法 JSON。请只输出 JSON，不要解释。{schema_hint}",
                    },
                ]
            )
        return {}  # 解析失败 → 空对象，由调用方当作"没有内容"

    def ping(self) -> float:
        start = time.time()
        self.chat([{"role": "user", "content": "ping"}], max_tokens=8)
        return time.time() - start


def _extract_json(text: str) -> dict | None:
    text = (text or "").strip()
    if not text:
        return None
    fence = text.find("```")
    if fence >= 0:
        body = text[fence + 3 :]
        body = body[body.find("\n") + 1 :] if "\n" in body else body
        end = body.find("```")
        text = body[:end] if end >= 0 else body
    lo, hi = text.find("{"), text.rfind("}")
    if lo < 0 or hi <= lo:
        return None
    try:
        data = json.loads(text[lo : hi + 1])
        return data if isinstance(data, dict) else None
    except ValueError:
        return None


# ---------------------------------------------------------------- init


def cmd_init() -> int:
    cfg = load_config() or dict(DEFAULTS)
    if cfg.get("api_key"):
        print(f"已有配置：{os.path.expanduser(USER_CFG)}（继续会覆盖）\n")

    print("请选择服务商：\n")
    for idx, (name, url, model, note) in enumerate(PRESETS, 1):
        tail = f"  （{note}）" if note else ""
        print(f"  {idx}) {name:<10} {url or '—'}{tail}")
    raw = input("\n> ").strip() or "1"
    try:
        name, base_url, model, _ = PRESETS[int(raw) - 1]
    except (ValueError, IndexError):
        print("无效选择")
        return 1

    if not base_url:
        base_url = input("base_url: ").strip()
    cfg["base_url"] = base_url
    cfg["model"] = input(f"模型名 [{model}]: ").strip() or model
    key = input("API Key（输入不回显）: ").strip()
    if name == "本地 Ollama" and not key:
        key = "ollama"
    cfg["api_key"] = key

    print("试连通性 ...", end=" ", flush=True)
    try:
        latency = ChatClient(cfg).ping()
    except Exception as err:  # noqa: BLE001
        print(f"失败：{err}")
        print("配置未保存。请检查 base_url / api key / 网络。")
        return 1
    print(f"ok（延迟 {latency * 1000:.0f}ms）")

    path = save_config(cfg)
    print(f"已保存到 {path}（权限 600）")
    return 0


def cmd_show() -> int:
    cfg = load_config()
    if cfg is None:
        print(f"未检测到 LLM 配置（{os.path.expanduser(USER_CFG)} 不存在或缺 api_key）")
        print("运行：python scripts/llm.py init")
        return 1
    print(f"配置文件：{os.path.expanduser(USER_CFG)}\n")
    for key, val in DEFAULTS.items():
        shown = mask(cfg[key]) if key == "api_key" else cfg[key]
        print(f"  {key:<22} {shown}")

    extra = unknown_keys()
    if extra:
        print(f"\n忽略的未知键（键名需与上面一致）：{', '.join(extra)}")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["init"]:
        sys.exit(cmd_init())
    if args[:1] == ["show"]:
        sys.exit(cmd_show())
    sys.exit(0)

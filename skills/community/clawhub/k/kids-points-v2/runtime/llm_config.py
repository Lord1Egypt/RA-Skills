"""kids-points LLM 配置 — 统一从 config.yaml + auth.json 读取。

外部只需要这一个导入点：

    from llm_config import LLM_API_KEY, LLM_API_URL, LLM_MODEL, call_llm

或者：

    from llm_config import get_llm_config, call_llm
    cfg = get_llm_config()
"""

import json
import os
import time
import urllib.request
from pathlib import Path

import yaml

# ─── 路径 ────────────────────────────────────────────────────────────────────

_PROJECT_ROOT = Path(__file__).parent
_CONFIG_PATH = _PROJECT_ROOT / "config.yaml"
_HERMES_AUTH_PATH = Path.home() / ".hermes" / "auth.json"
_HERMES_ENV_PATH = Path.home() / ".hermes" / ".env"


# ─── ~/.hermes/.env 自动加载 ─────────────────────────────────────────────────
# Hermes 把真实 API key 存在 ~/.hermes/.env；auth.json 的 credential_pool
# 条目通过 source: "env:<YOUR_API_KEY_VAR>" 引用它。本项目代码在普通 shell
# 下不会自动 source 这个文件，所以在 import 时主动把里面声明的 KEY 类变量
# 注入到 os.environ（已存在的不覆盖，行为和 source 接近）。
def _load_hermes_env(path: Path) -> None:
    if not path.exists():
        return
    try:
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            # 已设置的不覆盖（让 KIDS_POINTS_LLM_KEY 这种 mock 通道优先）
            if k and k not in os.environ:
                os.environ[k] = v
    except OSError:
        # .env 读取失败不应让 import 崩溃 — 走原 KeyError 路径更清晰
        pass


_load_hermes_env(_HERMES_ENV_PATH)


# ─── 配置加载 ────────────────────────────────────────────────────────────────

def _load_config() -> dict:
    if not _CONFIG_PATH.exists():
        raise FileNotFoundError(f"配置文件不存在: {_CONFIG_PATH}")
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _resolve_api_key(cfg: dict) -> str:
    """从配置指定的来源解析 API key。

    优先级：
    1. 环境变量 KIDS_POINTS_LLM_KEY（测试 mock 用，覆盖一切）
    2. 配置指定的 key_source：
       - "env:XXX"   — 直接读 os.environ["XXX"]
       - "auth_json" — 从 ~/.hermes/auth.json 的 credential_pool 读
                       条目的 source 可能是 "env:XXX"，这种情况下
                       走和上面 "env:XXX" 一样的逻辑（依赖 _load_hermes_env
                       把 ~/.hermes/.env 注入好了），或者直接读 access_token
    """
    # 1. 测试/调试：环境变量覆盖
    env_key = os.environ.get("KIDS_POINTS_LLM_KEY")
    if env_key:
        return env_key

    llm_cfg = cfg.get("llm", {})
    key_source = llm_cfg.get("key_source", "auth_json")

    if key_source.startswith("env:"):
        env_var = key_source[4:]
        key = os.environ.get(env_var)
        if key:
            return key
        # 模板占位符（config.yaml 未编辑）→ 返回空字符串，测试用 mock.patch 覆盖
        if env_var.startswith("<") and env_var.endswith(">"):
            return ""
        raise KeyError(f"环境变量 {env_var} 未设置")

    if key_source == "auth_json":
        pool_name = llm_cfg.get("credential_pool", "minimax-cn")
        if not _HERMES_AUTH_PATH.exists():
            raise FileNotFoundError(
                f"Hermes auth.json 不存在: {_HERMES_AUTH_PATH}"
            )
        with open(_HERMES_AUTH_PATH, "r", encoding="utf-8") as f:
            auth = json.load(f)
        pool = auth.get("credential_pool", {}).get(pool_name, [])
        if not pool:
            raise KeyError(
                f"auth.json 中找不到 credential_pool.{pool_name}"
            )
        # 取优先级最高的
        pool_sorted = sorted(pool, key=lambda x: x.get("priority", 0))
        entry = pool_sorted[0]

        # 真实 key 的实际位置由 entry.source 决定
        entry_source = entry.get("source", "")
        if entry_source.startswith("env:"):
            env_var = entry_source[4:]
            key = os.environ.get(env_var)
            if key:
                return key
            raise KeyError(
                f"auth.json credential_pool.{pool_name} 指向 env:{env_var}，"
                f"但该环境变量未设置（请检查 ~/.hermes/.env）"
            )

        # 非 env: 来源 — 兼容老的 access_token 直存格式
        token = entry.get("access_token", "")
        if token:
            return token
        raise KeyError(
            f"auth.json credential_pool.{pool_name} 既无 access_token，"
            f"也无法从 source 解析 key"
        )

    raise ValueError(f"未知的 key_source: {key_source}")


# ─── 模块级导出 ──────────────────────────────────────────────────────────────

_CONFIG = _load_config()

LLM_API_URL = _CONFIG.get("llm", {}).get(
    "api_url", "https://api.minimaxi.com/v1/chat/completions"
)
LLM_API_KEY = _resolve_api_key(_CONFIG)
LLM_MODEL = _CONFIG.get("llm", {}).get("model", "MiniMax-M2.7")
LLM_TIMEOUT = _CONFIG.get("llm", {}).get("timeout", 30)
# 全局节流 (秒) — 防触发 429。envvar LLM_THROTTLE_SEC 可临时调
LLM_THROTTLE_SEC = float(os.environ.get("LLM_THROTTLE_SEC", "0") or "0")
AGENT_VERSION = _CONFIG.get("app", {}).get("agent_version", "dev")
DB_PATH = _PROJECT_ROOT / _CONFIG.get("db", {}).get("path", "data/kids_points.db")

# 兼容外部访问
KIDS_POINTS_LLM_KEY = LLM_API_KEY
KIDS_POINTS_AGENT_VERSION = AGENT_VERSION


def get_llm_config() -> dict:
    """返回完整配置字典（用于需要更多字段的场景）。"""
    return dict(_CONFIG)


# ─── LLM 调用 ────────────────────────────────────────────────────────────────

def _extract_json(text: str) -> str:
    """从任意格式的 LLM 输出中提取 JSON 内容。

    处理场景：
    - 标准 JSON：{"intent":"record"}
    - 代码块包裹：```json {...} ```
    - think 标签：<think> ... {JSON} （MiniMax 2.7 强制 deep thinking）
    - 前缀语言：以下是 JSON：{...}
    - 后缀解释：{...} （以上即结果）
    """
    if not text:
        return ""

    # 1. 先去 think 标签，取最后一个 之后的内容
    THINK_CLOSE = "</think>"
    if THINK_CLOSE in text:
        after = text.rsplit(THINK_CLOSE, 1)[-1].strip()
        if after:
            text = after
        else:
            # 尝试从 think 内部提取最后一个 {...} 块
            THINK_OPEN = "<think>"
            inner = text.split(THINK_OPEN, 1)[-1]
            inner = inner.rsplit(THINK_CLOSE, 1)[0] if THINK_CLOSE in inner else inner
            start = inner.rfind("{")
            end = inner.rfind("}") + 1
            if start >= 0 and end > start:
                text = inner[start:end]

    # 2. 去掉代码块包裹
    if "```" in text:
        lines = text.split("\n")
        in_block = False
        block_lines = []
        for line in lines:
            if line.strip().startswith("```"):
                in_block = not in_block
                continue
            if in_block:
                block_lines.append(line)
        if block_lines:
            text = "\n".join(block_lines)

    # 3. 去掉常见语言前缀
    prefixes = [
        "以下是JSON：", "以下是结果：", "JSON结果：", "结果：",
        "根据分析：", "分析结果：", "返回如下：",
    ]
    for p in prefixes:
        if text.strip().startswith(p):
            text = text.strip()[len(p):]

    # 4. 找第一个 { 到最后一个 } 作为 JSON 块
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace >= 0 and last_brace > first_brace:
        text = text[first_brace:last_brace + 1]
        return _try_repair_json_quotes(text)

    # 5. 找 JSON 数组 [ 到 ]
    first_bracket = text.find("[")
    last_bracket = text.rfind("]")
    if first_bracket >= 0 and last_bracket > first_bracket:
        text = text[first_bracket:last_bracket + 1]
        return _try_repair_json_quotes(text)

    return text.strip()


def _try_repair_json_quotes(text: str) -> str:
    """如果 text 是合法 JSON,直接返回。否则尝试修复字符串值内未转义的双引号(V2-007)。

    LLM 偶尔会在 reasoning/description 等字段里把用户原文用裸双引号包裹,
    直接破坏 JSON 字符串(例: {"reasoning":"用户说"海苔卷"没听清金额"})。
    这个函数识别字符串边界,把内部多余的双引号转义为 \\\",让 json.loads 能解析。
    """
    if not text:
        return text
    try:
        json.loads(text)
        return text  # 已合法,直接返回
    except json.JSONDecodeError:
        pass
    repaired = _repair_json_quotes(text)
    try:
        json.loads(repaired)
        return repaired
    except json.JSONDecodeError:
        return text  # 修复失败,原样返回让 caller 处理


def _repair_json_quotes(text: str) -> str:
    """State machine 修复 JSON 字符串值内未转义的双引号。

    算法:
    - 正常字符直接通过
    - 遇到 \\\\: 跳过下一字符(保留转义)
    - 遇到 ": 状态切换:
        - 不在字符串内 → 进入字符串
        - 在字符串内 → 看下一个非空白字符:
            - 是 JSON 分隔符(, } ] :) → 字符串正常结束
            - 否则 → 字符串内的多余引号,转义为 \\"
    """
    out = []
    in_string = False
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        # 保留已有转义
        if c == '\\' and i + 1 < n:
            out.append(c)
            out.append(text[i + 1])
            i += 2
            continue
        if c == '"':
            if not in_string:
                in_string = True
                out.append(c)
                i += 1
                continue
            # 在字符串内:判断是结束还是内部多余
            j = i + 1
            while j < n and text[j] in ' \t\n\r':
                j += 1
            if j >= n or text[j] in ',:}]:':
                in_string = False
                out.append(c)
            else:
                out.append('\\"')  # 内部多余引号,转义
            i += 1
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def call_llm(prompt: str, *, retry_count: int = 2, retry_base_delay: float = 2.0) -> str:
    """调用 MiniMax Chat Completions API，返回文本响应。

    MiniMax 支持 OpenAI 兼容的 Chat Completions 格式：
        POST {api_url}
        { model, messages: [{role, content}], ... }
        → choices[0].message.content

    内置重试 + JSON 提取：
    - 每次失败重试，最多重试 retry_count 次
    - 指数退避：1次失败等 2s，2次失败等 4s
    - 返回前自动从任意格式（think 标签、代码块、前缀）中提取纯 JSON
    """
    last_error = None

    for attempt in range(retry_count + 1):
        # 全局节流 — 防止触发服务端速率限制 (e.g. 429)
        # 默认 0 = 不节流;测试场景设 LLM_THROTTLE_SEC=2
        if LLM_THROTTLE_SEC > 0:
            time.sleep(LLM_THROTTLE_SEC)
        try:
            # 关掉 M3 deep thinking — 实测 5/5 稳定,官方+relay 都 OK,total 省 25%
            # 备选方法 /no_think prompt 后缀不稳 (3/5 仍触发),enable_thinking=False 完全无效
            body = json.dumps({
                "model": LLM_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "thinking": {"type": "disabled"},
            }).encode("utf-8")

            req = urllib.request.Request(LLM_API_URL, data=body, method="POST")
            req.add_header("Authorization", f"Bearer {LLM_API_KEY}")
            req.add_header("Content-Type", "application/json")

            with urllib.request.urlopen(req, timeout=LLM_TIMEOUT) as resp:
                data = json.loads(resp.read().decode("utf-8"))

            choices = data.get("choices", [])
            if not (choices and choices[0].get("message", {}).get("content")):
                raise RuntimeError(f"LLM 返回格式异常: {json.dumps(data, ensure_ascii=False)[:200]}")

            raw_content = choices[0]["message"]["content"]
            if raw_content is None:
                raise RuntimeError(f"LLM content 为 null: {json.dumps(data, ensure_ascii=False)[:200]}")
            content = raw_content.strip()

            # JSON 鲁棒提取
            return _extract_json(content)

        except Exception as e:
            last_error = e
            if attempt < retry_count:
                delay = retry_base_delay * (2 ** attempt)  # 2s, 4s
                # 短暂的 HTTPError 可以重试，网络不可达就算了
                if isinstance(e, urllib.error.HTTPError) and e.code >= 500:
                    time.sleep(delay)
                    continue
                elif isinstance(e, urllib.error.HTTPError):
                    # 4xx 不重试
                    break
                else:
                    time.sleep(delay)
                    continue

    # 所有重试失败
    raise last_error


def call_llm_raw(prompt: str) -> str:
    """调用 LLM，返回原始文本（不过滤 JSON）。用于调试。"""
    body = json.dumps({
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request(LLM_API_URL, data=body, method="POST")
    req.add_header("Authorization", f"Bearer {LLM_API_KEY}")
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req, timeout=LLM_TIMEOUT) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    choices = data.get("choices", [])
    if not (choices and choices[0].get("message", {}).get("content")):
        raise RuntimeError(f"LLM 返回格式异常: {json.dumps(data, ensure_ascii=False)[:200]}")

    return choices[0]["message"]["content"].strip()


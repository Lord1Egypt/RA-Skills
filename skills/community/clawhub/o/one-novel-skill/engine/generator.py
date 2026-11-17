#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generator.py — 零配置自适应 LLM 生成器

特性:
  - 统一 OpenAI-compatible HTTP 接口，所有 provider 共用一套通信协议
  - 自动扫描环境变量发现可用 provider，无需手动配置 API Key
  - 支持: Ollama / OpenClaw / DeepSeek / OpenAI / Claude / Gemini / 通义千问 / 智谱 / 月之暗面 / 百川 / 任意 OpenAI-compatible 端点
  - Ollama 支持任意本地模型（不限于 qwen3）
  - provider 健康检查 + 自动排序 + 智能 fallback
  - 保留 SessionProvider（CodeBuddy Skill 文件通信协议）
"""

import os, json, re, subprocess, logging, threading, sys, time
from pathlib import Path

logger = logging.getLogger("generator")

# ============================================================
# 零配置 Provider 注册表
# ============================================================
# 每个 provider 定义:
#   name: 名称
#   env_key: 环境变量（API Key）
#   env_base: 环境变量（Base URL，可选）
#   default_base: 默认 Base URL
#   default_model: 默认模型
#   models: 已知模型列表（自动选第一个可用）
#   priority: 优先级（越小越优先，自动检测成功的按 priority 排序）

PROVIDER_REGISTRY = [
    # ── 本地 ──
    {
        "name": "ollama",
        "env_key": None,  # Ollama 不需要 API Key
        "default_base": "http://127.0.0.1:11434",
        "default_model": "",  # 自动检测
        "priority": 1,
        "note": "本地 Ollama 服务",
    },
    {
        "name": "openclaw",
        "env_key": "OPENCLAW_TOKEN",
        "default_base": "",  # 从 openclaw.json 自动读取
        "default_model": "openclaw",
        "priority": 2,
        "note": "OpenClaw Gateway（自动检测 ~/.openclaw/openclaw.json）",
    },
    # ── 国产大模型 ──
    {
        "name": "deepseek",
        "env_key": "DEEPSEEK_API_KEY",
        "default_base": "https://api.deepseek.com",
        "default_model": "deepseek-chat",
        "priority": 3,
        "note": "DeepSeek API",
    },
    {
        "name": "zhipu",
        "env_key": "ZHIPU_API_KEY",
        "default_base": "https://open.bigmodel.cn/api/paas/v4",
        "default_model": "glm-4-flash",
        "priority": 4,
        "note": "智谱 GLM（ChatGLM）",
    },
    {
        "name": "qwen",
        "env_key": "DASHSCOPE_API_KEY",
        "default_base": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen-plus",
        "priority": 4,
        "note": "通义千问（阿里云 DashScope）",
    },
    {
        "name": "moonshot",
        "env_key": "MOONSHOT_API_KEY",
        "default_base": "https://api.moonshot.cn",
        "default_model": "moonshot-v1-8k",
        "priority": 4,
        "note": "月之暗面 Kimi",
    },
    {
        "name": "baichuan",
        "env_key": "BAICHUAN_API_KEY",
        "default_base": "https://api.baichuan-ai.com",
        "default_model": "Baichuan4",
        "priority": 5,
        "note": "百川大模型",
    },
    {
        "name": "ernie",
        "env_key": "ERNIE_API_KEY",
        "default_base": "",  # 需要特殊处理（非标准 OpenAI 接口）
        "default_model": "ernie-4.0-turbo-8k",
        "priority": 5,
        "note": "文心一言（百度千帆）",
    },
    # ── 国际大模型 ──
    {
        "name": "openai",
        "env_key": "OPENAI_API_KEY",
        "default_base": "https://api.openai.com",
        "default_model": "gpt-4o-mini",
        "priority": 5,
        "note": "OpenAI API",
    },
    {
        "name": "claude",
        "env_key": "ANTHROPIC_API_KEY",
        "default_base": "https://api.anthropic.com",
        "default_model": "claude-3-5-sonnet-20241022",
        "priority": 5,
        "note": "Anthropic Claude（需 x-api-key header）",
    },
    {
        "name": "gemini",
        "env_key": "GEMINI_API_KEY",
        "default_base": "https://generativelanguage.googleapis.com/v1beta/openai",
        "default_model": "gemini-2.0-flash",
        "priority": 5,
        "note": "Google Gemini（OpenAI 兼容端点）",
    },
    # ── 通用 OpenAI-compatible ──
    {
        "name": "custom",
        "env_key": "OPENAI_API_KEY",  # 复用
        "env_base": "CUSTOM_LLM_BASE",
        "env_model": "CUSTOM_LLM_MODEL",
        "default_base": "",  # 必须通过环境变量设置
        "default_model": "gpt-3.5-turbo",
        "priority": 99,
        "note": "自定义 OpenAI-compatible 端点（设置 CUSTOM_LLM_BASE + CUSTOM_LLM_MODEL）",
    },
]

# ============================================================
# Provider 自动检测器
# ============================================================

def _detect_ollama_model(base_url="http://127.0.0.1:11434") -> str:
    """自动检测 Ollama 已安装的模型，返回最佳模型名"""
    try:
        r = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=5, encoding="utf-8"
        )
        if r.returncode != 0:
            return ""
        lines = r.stdout.strip().split("\n")[1:]  # 跳过表头
        models = []
        for line in lines:
            parts = line.split()
            if parts:
                models.append(parts[0])
        if not models:
            return ""
        # 优先级: qwen系列 > deepseek系列 > llama系列 > 其他 > 第一个
        for prefix in ["qwen3", "qwen2.5", "qwen2", "qwen", "deepseek-r1", "deepseek",
                        "llama3.2", "llama3.1", "llama3", "llama2", "mistral", "gemma2", "phi"]:
            for m in models:
                if m.startswith(prefix):
                    return m
        return models[0]
    except Exception:
        return ""

def _detect_openclaw_config() -> dict:
    """自动检测 OpenClaw Gateway 配置"""
    result = {"base": "", "token": ""}
    oc_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(oc_path):
        try:
            with open(oc_path, encoding="utf-8") as f:
                oc = json.load(f)
            gw = oc.get("gateway", {})
            port = gw.get("port", 3839)
            result["base"] = f"http://127.0.0.1:{port}"
            result["token"] = gw.get("auth", {}).get("token", "")
        except Exception:
            pass
    # 也检查环境变量
    if not result["token"]:
        result["token"] = os.environ.get("OPENCLAW_TOKEN", "")
    if not result["base"]:
        result["base"] = os.environ.get("OPENCLAW_BASE", "")
    return result

def discover_providers() -> list:
    """零配置自动发现所有可用 provider。

    返回按优先级排序的可用 provider 列表，每个包含:
      name, base_url, api_key, model, priority
    """
    available = []

    for entry in PROVIDER_REGISTRY:
        name = entry["name"]
        base_url = entry["default_base"]
        api_key = ""
        model = entry["default_model"]
        priority = entry["priority"]

        # ── Ollama: 检测本地服务 + 自动选模型 ──
        if name == "ollama":
            try:
                r = subprocess.run(
                    ["ollama", "list"], capture_output=True, text=True, timeout=3, encoding="utf-8"
                )
                if r.returncode == 0:
                    detected_model = _detect_ollama_model(base_url)
                    if detected_model:
                        model = detected_model
                        available.append({
                            "name": "ollama",
                            "base_url": base_url,
                            "api_key": "",
                            "model": model,
                            "priority": priority,
                            "note": f"本地 Ollama / 模型: {model}",
                        })
                        continue
            except Exception:
                pass
            # Ollama 不在 PATH 中，尝试直接 HTTP 检测
            try:
                import urllib.request
                req = urllib.request.Request(f"{base_url}/api/tags", method="GET")
                urllib.request.urlopen(req, timeout=3)
                # HTTP 可达但没有 ollama CLI，使用默认模型
                available.append({
                    "name": "ollama",
                    "base_url": base_url,
                    "api_key": "",
                    "model": model or "qwen3:latest",
                    "priority": priority,
                    "note": "Ollama HTTP 服务（模型未自动检测）",
                })
                continue
            except Exception:
                pass
            continue

        # ── OpenClaw: 自动检测 openclaw.json ──
        if name == "openclaw":
            oc = _detect_openclaw_config()
            if oc["base"]:
                available.append({
                    "name": "openclaw",
                    "base_url": oc["base"],
                    "api_key": oc["token"],
                    "model": model,
                    "priority": priority,
                    "note": "OpenClaw Gateway",
                })
            continue

        # ── Custom: 需要 CUSTOM_LLM_BASE 环境变量 ──
        if name == "custom":
            custom_base = os.environ.get(entry.get("env_base", ""), "")
            custom_model = os.environ.get(entry.get("env_model", ""), model)
            if custom_base:
                available.append({
                    "name": "custom",
                    "base_url": custom_base,
                    "api_key": os.environ.get(entry["env_key"], ""),
                    "model": custom_model,
                    "priority": priority,
                    "note": f"自定义端点: {custom_base}",
                })
            continue

        # ── 标准 API Key provider ──
        if entry["env_key"]:
            api_key = os.environ.get(entry["env_key"], "")
            # 也检查对应的 *_API_BASE 环境变量
            env_base_name = f"{name.upper()}_API_BASE"
            if os.environ.get(env_base_name):
                base_url = os.environ[env_base_name]
            if api_key:
                available.append({
                    "name": name,
                    "base_url": base_url,
                    "api_key": api_key,
                    "model": model,
                    "priority": priority,
                    "note": entry.get("note", name),
                })

    # 按 priority 排序
    available.sort(key=lambda x: x["priority"])
    return available

# ============================================================
# 统一 OpenAI-compatible Provider
# ============================================================

class UnifiedProvider:
    """统一的 OpenAI-compatible HTTP Provider。

    支持所有 OpenAI-compatible API（DeepSeek/智谱/通义千问/月之暗面/百川/Gemini/OpenAI/自定义端点）。
    Claude 使用 x-api-key header（Anthropic 特有）。
    文心一言使用千帆特殊鉴权（非标准）。
    """

    def __init__(self, name: str, base_url: str, api_key: str, model: str):
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def available(self) -> bool:
        return bool(self.base_url)

    def _build_url(self) -> str:
        """构建 API URL"""
        # Gemini 的 OpenAI 兼容端点
        if "generativelanguage.googleapis.com" in self.base_url:
            return f"{self.base_url}/chat/completions"
        # Claude 使用 Messages API（非标准 OpenAI 路径）
        if "anthropic.com" in self.base_url:
            return f"{self.base_url}/v1/messages"
        # 文心一言使用千帆 API
        if self.name == "ernie":
            return f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{self.model}"
        # 标准 OpenAI-compatible
        return f"{self.base_url}/v1/chat/completions"

    def _build_headers(self) -> dict:
        """构建请求头"""
        headers = {"Content-Type": "application/json"}
        if self.name == "claude":
            headers["x-api-key"] = self.api_key
            headers["anthropic-version"] = "2023-06-01"
        elif self.name == "ernie":
            headers["Content-Type"] = "application/json"
            # 千帆需要先获取 access_token
            pass
        else:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _build_payload(self, system: str, user: str, temperature: float) -> dict:
        """构建请求体"""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})

        if self.name == "claude":
            return {
                "model": self.model,
                "max_tokens": 4096,
                "temperature": temperature,
                "system": system,
                "messages": [{"role": "user", "content": user}],
            }

        return {
            "model": self.model,
            "messages": messages,
            "max_tokens": 4096,
            "temperature": temperature,
        }

    def _parse_response(self, data: dict) -> str:
        """解析响应体"""
        if self.name == "claude":
            # Claude Messages API 响应格式
            content = data.get("content", [])
            if content and isinstance(content, list):
                return content[0].get("text", "")
            return ""
        # 标准 OpenAI-compatible 响应
        choices = data.get("choices", [])
        if choices:
            return choices[0].get("message", {}).get("content", "")
        return ""

    def generate(self, system: str, user: str, temperature: float = 0.7) -> str:
        """发送生成请求"""
        if not self.base_url:
            return ""

        import requests
        url = self._build_url()
        headers = self._build_headers()
        payload = self._build_payload(system, user, temperature)

        max_retries = 3
        for attempt in range(max_retries):
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=60)
                if r.status_code == 200:
                    return self._parse_response(r.json())
                # 可重试的错误
                if r.status_code in (429, 502, 503, 504) and attempt < max_retries - 1:
                    delay = (2 ** attempt) + __import__("random").uniform(0, 1)
                    logger.debug(f"{self.name}: HTTP {r.status_code}, retry {attempt+1}/{max_retries}")
                    time.sleep(delay)
                    continue
                logger.warning(f"{self.name}: HTTP {r.status_code}, body={r.text[:300]}")
                return ""
            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                logger.warning(f"{self.name}: {type(e).__name__}: {e}")
                return ""
            except Exception as e:
                logger.warning(f"{self.name}: {type(e).__name__}: {e}")
                return ""
        return ""

# ============================================================
# Ollama Provider（本地 subprocess 调用）
# ============================================================

class OllamaProvider:
    """Ollama 本地 Provider。

    优先使用 subprocess 调用（更快、更可靠），
    如果 ollama CLI 不在 PATH 则回退到 HTTP API。
    """

    def __init__(self, model: str, base_url: str = "http://127.0.0.1:11434"):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self._use_http = False

    def available(self) -> bool:
        # 尝试 CLI
        try:
            r = subprocess.run(
                ["ollama", "list"], capture_output=True, text=True, timeout=3, encoding="utf-8"
            )
            if r.returncode == 0:
                return True
        except Exception:
            pass
        # 回退 HTTP
        try:
            import urllib.request
            req = urllib.request.Request(f"{self.base_url}/api/tags", method="GET")
            urllib.request.urlopen(req, timeout=3)
            self._use_http = True
            return True
        except Exception:
            return False

    def generate(self, system: str, user: str, temperature: float = 0.7) -> str:
        if self._use_http:
            return self._generate_http(system, user, temperature)
        return self._generate_cli(system, user, temperature)

    def _generate_cli(self, system: str, user: str, temperature: float = 0.7) -> str:
        prompt = system + "\n\n" + user
        try:
            r = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=180,
                encoding="utf-8",
            )
            return r.stdout.strip() if r.returncode == 0 else ""
        except Exception as e:
            logger.warning(f"Ollama CLI failed: {e}, falling back to HTTP")
            return self._generate_http(system, user, temperature)

    def _generate_http(self, system: str, user: str, temperature: float = 0.7) -> str:
        import requests
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": user})
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature},
        }
        try:
            r = requests.post(
                f"{self.base_url}/api/chat", json=payload, timeout=120
            )
            if r.status_code == 200:
                return r.json().get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"Ollama HTTP failed: {e}")
        return ""

# ============================================================
# Session Provider（CodeBuddy Skill 文件通信协议）
# ============================================================

class SessionProvider:
    """CodeBuddy Skill 环境下的文件通信 Provider。

    协议:
    1. 写入 _llm_session/request_{uid}.json
    2. 轮询 _llm_session/response_{uid}.json（最长 300s）
    3. 返回响应文本
    """

    _SESSION_DIR = "_llm_session"

    def __init__(self):
        pass

    def available(self) -> bool:
        return os.path.isdir(self._SESSION_DIR)

    def generate(self, system: str, user: str, temperature: float = 0.7) -> str:
        try:
            uid = str(int(time.time() * 1000))
            req_dir = self._SESSION_DIR
            os.makedirs(req_dir, exist_ok=True)

            req_path = os.path.join(req_dir, f"request_{uid}.json")
            resp_path = os.path.join(req_dir, f"response_{uid}.json")

            req = {
                "system": system,
                "user": user,
                "temperature": temperature,
                "timestamp": uid,
            }
            with open(req_path, "w", encoding="utf-8") as f:
                json.dump(req, f, ensure_ascii=False, indent=2)

            deadline = time.time() + 300
            while time.time() < deadline:
                if os.path.exists(resp_path):
                    try:
                        with open(resp_path, "r", encoding="utf-8") as f:
                            resp = json.load(f)
                        text = resp.get("text", "")
                        if text and len(text) > 50:
                            os.remove(req_path)
                            os.remove(resp_path)
                            return text
                    except (json.JSONDecodeError, OSError):
                        pass
                time.sleep(0.5)

            logger.error(f"SessionProvider: timeout waiting for {uid}")
            return ""
        except Exception as e:
            logger.error(f"SessionProvider failed: {e}")
            return ""

# ============================================================
# Prompt 定义（保持不变）
# ============================================================

DEFAULT_CONFIG = {
    "temperature": 0.7,
    "max_tokens": 8192,
}

def load_config(path=None):
    config = dict(DEFAULT_CONFIG)
    if path:
        p = Path(path)
        if p.exists():
            try:
                user = json.loads(p.read_text(encoding="utf-8"))
                for k, v in user.items():
                    if isinstance(v, dict) and k in config and isinstance(config[k], dict):
                        config[k].update(v)
                    else:
                        config[k] = v
            except Exception:
                pass
    return config

class PromptLoader:
    _cache = {}

    @classmethod
    def get(cls, category, key, fallback=""):
        import pathlib as _p
        if category not in cls._cache:
            path = _p.Path(__file__).parent.parent / "templates" / "prompts" / (category + ".yaml")
            if path.exists():
                try:
                    text = path.read_text(encoding="utf-8")
                    data = {}
                    current_key = None
                    current_val = []
                    for line in text.split("\n"):
                        if ":" in line and not line.startswith(" ") and not line.startswith("  "):
                            if current_key:
                                data[current_key] = "\n".join(current_val).strip()
                            parts = line.split(":", 1)
                            current_key = parts[0].strip()
                            rest = parts[1].strip()
                            if rest.startswith("|-"):
                                current_val = []
                            else:
                                current_val = [rest]
                        elif current_key and line.strip():
                            current_val.append(line.rstrip())
                    if current_key:
                        data[current_key] = "\n".join(current_val).strip()
                    cls._cache[category] = data
                except Exception:
                    cls._cache[category] = {}
            else:
                cls._cache[category] = {}
        return cls._cache[category].get(key, fallback)

PLATFORM_IDENTITIES = {
    "番茄": "你扮演的身份（不是我）——番茄小说网写作超过十年以上的殿堂金番作家，熟知番茄小说网各个题材写作方法及技巧，更清楚番茄小说网读者的各个喜好，累计写作字数超过10亿以上，发布过各个题材长篇完结小说、未完结新书，并时常霸榜各个榜单前几名，尤其是新书发布方面，更有独一无二的断层领先，禁止私自切换身份。",
    "起点": "你是在起点小说网写作超过二十年以上的大神俱乐部作家及作家指数排行第一，熟知起点小说网各个题材写作方法及技巧，更清楚起点小说网读者的各个喜好，累计写作字数超过20亿以上，发布过各个题材长篇完结小说、未完结新书，并时常霸榜各个榜单前几名，尤其是新书发布方面，更有独一无二的断层领先，禁止私自切换身份。",
    "晋江": "你是在晋江文学城写作超过十五年以上的殿堂级作家，熟知晋江各个题材写作方法及技巧，更清楚晋江读者的各个喜好，累计写作字数超过15亿以上，发布过各个题材长篇完结小说、未完结新书，并时常霸榜各大榜单前几名，尤其是新书发布方面，有独一无二的断层领先，禁止私自切换身份。",
    "七猫": "你是在七猫小说平台写作超过十年以上的白金作家，熟知七猫平台各个题材写作方法及技巧，更清楚七猫读者的各个喜好，累计写作字数超过8亿以上，发布过各个题材长篇完结小说，并时常霸榜各大榜单前几名，禁止私自切换身份。",
    "飞卢": "你是在飞卢小说网写作超过十年以上的大神作家，熟知飞卢各个题材写作方法及技巧，更清楚飞卢读者的各个喜好，累计写作字数超过12亿以上，发布过各个题材长篇完结小说，并时常霸榜各大榜单前几名，禁止私自切换身份。",
}

def get_writer_identity(platform: str) -> str:
    from_yaml = PromptLoader.get("platform_identities", platform)
    return from_yaml or PLATFORM_IDENTITIES.get(platform, PLATFORM_IDENTITIES.get("番茄", ""))

GENRE_PROMPTS = {
    "修仙": "【修仙文要点】\n- 境界体系清晰（练气→筑基→金丹→元婴），每次突破有代价\n- 修炼资源（丹药/灵石/功法）驱动情节\n- 斗法描写要有层次感：起手式→招式碰撞→胜负揭晓\n- 宗门势力和派系斗争作为长线背景\n- 天道/因果/劫数元素增加深度\n- 反派不能无脑送，每次冲突都要有算计\n- 详见 references/original/xianxia-writing-guide.md",
    "仙侠": "【仙侠文要点】\n- 境界体系清晰（练气→筑基→金丹→元婴），每次突破有代价\n- 修炼资源（丹药/灵石/功法）驱动情节\n- 斗法描写要有层次感：起手式→招式碰撞→胜负揭晓\n- 宗门势力和派系斗争作为长线背景\n- 天道/因果/劫数元素增加深度\n- 反派不能无脑送，每次冲突都要有算计\n- 详见 references/original/xianxia-writing-guide.md",
    "悬疑": "【悬疑文要点】\n- 开场必须埋下核心谜题（死者/失踪/怪事）\n- 线索分批释放，每章至少1个新线索+1个反转\n- 红鲱鱼（false lead）必须出现至少2次\n- 节奏控制：平静收集线索→突然发现→紧张追逐→短暂喘息→更大危机\n- 逻辑闭环：结尾要能回推所有关键线索\n- 每次揭秘带来更大的谜团\n- 详见 references/original/xuanyi-writing-guide.md",
    "都市": "【都市文要点】\n- 快节奏，前三章必出核心冲突/金手指\n- 社会阶层对抗（底层→中层→上层→顶层）\n- 日常生活细节增加真实感（房租/通勤/外卖）\n- 装逼打脸要有合理性，不被碾压\n- 人际关系网逐步展开\n- 每章至少1个爽点或反转",
    "历史": "【历史文要点】\n- 穿越后首章必须确认时代背景和身份\n- 利用现代知识改变历史进程，但不能过度开挂\n- 历史人物出场要做考据，不能OOC\n- 制度/技术/文化细节增加沉浸感\n- 政治斗争和军事描写要合理\n- 详见 references/original/lishi-writing-guide.md",
    "言情": "【言情文要点】\n- 感情线必须有障碍（身份差距/误会/第三者/家族反对）\n- 两人关系推进要有事件触发\n- 误会不能靠巧合解开，要靠人物主动选择\n- 配角感情线作为调剂但不能抢主线\n- 进度合理：前30%暧昧期，中40%波折期，后30%甜蜜/决裂",
    "科幻": "【科幻文要点】\n- 科技设定要内恰\n- 科幻框架下讲人的故事，不是技术说明书\n- 未来社会结构和伦理矛盾是核心\n- 外星文明/AI/超人类题材注意世界观极限\n- 详见 references/original/kehuan-writing-guide.md",
    "游戏": "【游戏文要点】\n- 游戏系统数值要自洽（等级/装备/技能）\n- 现实与游戏世界的互动是核心爽点\n- 副本/任务/Boss战设计要有层次\n- 玩家间的竞争和合作推动情节\n- 注意平衡「现实世界」和「游戏世界」的篇幅",
}

STYLE_DEFINITIONS = {
    "default": "标准叙事风格，客观中带情绪",
    "快节奏": "短句为主，段落紧凑，对话占比高",
    "细腻": "环境描写丰富，心理活动详实，节奏舒缓",
    "冷峻": "简练，少修辞，对话干练，留白多",
    "热血": "感叹号高频，动作描写密集，情绪渲染强",
    "悬疑": "信息分批释放，多用省略号和短句制造紧迫感",
    "幽默": "口语化，反讽，吐槽式内心独白",
    "文艺": "比喻丰富，句式优美，意象化描写",
}

def get_style_guide(style: str) -> str:
    from_yaml = PromptLoader.get("style_definitions", style)
    return from_yaml or STYLE_DEFINITIONS.get(style, STYLE_DEFINITIONS["default"])

def get_genre_prompt(genre: str) -> str:
    from_yaml = PromptLoader.get("genre_prompts", genre)
    return from_yaml or GENRE_PROMPTS.get(genre, "")

LOCAL_PROMPTS = {
    "write_chapter": {
        "system": (
            "你扮演的身份（不是我）——番茄小说网写作超过十年以上的殿堂金番作家，熟知番茄小说网各个题材写作方法及技巧，更清楚番茄小说网读者的各个喜好，累计写作字数超过10亿以上，发布过各个题材长篇完结小说、未完结新书，并时常霸榜各个榜单前几名，尤其是新书发布方面，更有独一无二的断层领先，禁止私自切换身份。\n\n每章输出前严格执行以下14条要求：\n(1)平稳叙事，精准细化每个情节，拒绝非必要拓展。增加日常章节的\"微冲突\"，丰富人物互动模式。禁止过快推进情节。锁死题材，只按前文和大纲续写。禁止新增无关设定。\n(2)对话自然度审查。情绪铺垫和转换必须自然。高频替换场景和对话标签词。\n(3)严丝合缝的前后衔接，逻辑自洽。剧情逻辑推衍统一自审。严格控制场景描写使用频率。不脱离主线大纲细纲，遵循\"一卷一主线、一章一核心\"的叙事逻辑。每章首尾句式多样化。明确章节定位，前置核对大纲，确保事件不重复、逻辑连贯。\n(4)读者黏性设计。合理安排章节内容悬念、章节钩子。从增强读者代入感角度分析内容。以世界级网文总编辑兼作家角度认真写作。\n(5)正文排版清晰，段落分明，自然过渡。无需附加任何解释性前言或后记。独立通读、联接通读、首尾比对均流畅。\n(6)自查AI通病：缺乏真实语境中的犹豫词与个性化停顿、专业术语堆砌但缺乏具体案例支撑、句号不分段、情感浓度偏低且难以体现个体经验痕迹等。\n(7)语言表达、语气、思维逻辑和细节把握须符合人类创作习惯。表达模式和语境禁止与AI文本相似。\n(8)故事性增强，增强读者代入感，增强文章人情味。情感色彩增强，对话情绪描写增强，环境描写增强，心理描写增强。拒绝流水账文章。\n(9)建立创作资料库并整理记录后进行思考及推衍。建立场景复用检测机制。严格控制\"日常过渡章节\"的数量。标记重复段落。\n(10)动作描写细腻，事件叙述有力，人物刻画立体，主题深刻。故事转折自然，景物描写有层次感。对话语言流畅，简化复杂概念表达。开篇吸引力强，情感共鸣深。回忆叙述有温暖感，逻辑结构严谨。战斗场面有震撼力。文章节奏流畅，小说氛围感强，故事叙述有层次感，情节反转合理。杜绝重复句式，审视句式结构，规范使用标点符号。全文取消破折号出现，以其他标点符号替代。\n(11)细节描绘增强代入感，分段解构分发好奇心。运用拟人手法，多元化表达。多感官描述，精确用词，制造矛盾冲突。使用隐喻，建立悬念，营造紧迫感，引导情绪波动。设置开放式结尾，强化视觉效果。利用短句制造冲击，使用铺垫层层递进。\n(12)使文章内容具有画面感，层次分明，修复剧情逻辑断层。运用各种语言技巧、表现手法、表达方式、叙事风格、角色视角。按照设定让章节之间的阅读体验行云流水，逻辑自洽，情感饱满，具备已出版实体书世界名著级别的阅读质感。\n(13)严格按照设定、世界观、角色、主线、支线、分卷、大纲、细纲、章纲。回顾前置所有剧情。每章正文2500-3500字。突出本章的主要内容和目标。\n(14)自行审查检查并修改完善，在章节末尾继续审核本章及前置章节。\n\n【5条反AI人味技巧——每章输出前逐条自检】\n[人味1] 剥离官样话术：不用\"值得一提的是\"\"毋庸置疑\"\"不可否认\"\"总而言之\"等公文腔，用短句大白话，像聊天一样自然。\n[人味2] 注入个人故事和真实感：每章至少1处让角色回忆起具体经历（不是泛泛的\"曾经\"，而是具体时间地点和细节），和读者建立情感连接。\n[人味3] 打磨行文节奏：段落衔接自然，不跳脱。检查每段首尾是否流畅。\n[人味4] 修正AI通病：检查并修正重复句式（连续两句同主语开头）、滥用过渡词（\"然而\"\"但是\"\"不过\"每段不超过1次）。\n[人味5] 独特个性语气：每个角色说话要有区分度，主角的内心独白要有个人风格，不要让所有角色共用一种\"标准网文腔\"。\n\n【反派智商与冲突烈度】\n- 反派智商必须在线。主角与反派的每次对决，主角不能碾压，需要勉强胜出或付出代价。\n- 每次冲突要体现反派的计划和反制手段，主角赢的每一场都要有合理的智力/资源/代价支撑。\n\n禁止使用AI高频词。只写正文，不写章节标题。用动作展示情绪，不说情绪词。每章前300字必须有钩子。场景写具体：用看到的、听到的、闻到的、摸到的感官细节。角色思考过程让读者看到，不要直接给结论。结尾必须在高潮或悬念处切断，不要写总结式结尾。"
        ),
        "user": "【前情】\n{context}\n\n【章节】\n第{chapter}章 - {chapter_title}\n字数：{word_count}字\n\n【核心情节】\n{plot_points}\n\n【关键场景】\n{key_scenes}\n\n【结尾钩子】\n{ending_hook}\n\n【新伏笔】\n{new_hooks}\n\n【角色状态】\n{characters}\n\n【风格约束】\n{style_lock}\n\n【写作指导】\n{writing_notes}\n\n### 请写正文 ###",
    },
    "review_outline": {
        "system": "你是有20年经验的网文总编辑。对大纲做全面审查。",
        "user": "审查以下大纲。回答：1)核心卖点是什么？爽点是什么？给读者什么快乐？2)一句话概括这个故事。3)这个故事的戏剧空间有多大？4)开局所有设定的因果线是否完整？每个设定后面是否能讲成一个闭环故事？5)按照问题→条件→解决的步骤，理清主角的目标、计划、阻扰因素。\n\n大纲：{outline_text}",
    },
    "review_chapter": {
        "system": "你是有20年经验的网文总编辑。对已完成章节进行逐章审查，检查语言、故事逻辑、角色一致性。",
        "user": "审查以下章节正文。列出所有需要修改的地方，然后输出修改后的版本。\n\n章节：第{chapter}章\n正文：{text}",
    },
    "generate_细纲": {
        "system": "你是有20年经验的网文大纲规划师。根据大纲和人物设定生成细纲。",
        "user": "根据以下大纲和人物脸谱生成细纲。每章2500-3500字。合理分配章节数和情节分布。\n\n大纲：{outline_text}\n人物：{characters}",
    },
    "generate_章纲": {
        "system": "你是有20年经验的网文章节规划师。生成全书章纲。",
        "user": "根据细纲生成全书章纲。每章包含标题和主要内容。\n\n细纲：{outline_text}",
    },
    "full_dimension_review": {
        "system": "你是有20年经验的网文总编辑+反AI审查专家。对全书做全维度深层审查。",
        "user": "对以下项目做全维度深层审查，内容包括：\n- 设定、世界观、主线、支线、人物一致性校验\n- 伏笔埋设和回收逻辑\n- 反派智商在线的全方位检查（反派必须有计划、有反制手段、主角不能碾压）\n- AI去痕处理（识别并标记所有AI痕迹段落）\n- 番茄小说网风格适配、读者喜好方向审查\n- 分析项目现状，拓展后续章节建议\n- 更新项目目录结构建议\n- 更新全书所有维度资料\n\n项目资料：{project_data}",
    },
    "proposition_review": {
        "system": "你是20年经验的网文创作者。执行问题→条件→解决三要素分析。",
        "user": "对以下故事设定执行三要素分析：\n1）核心问题是什么（开场阶段主角面临的根本困境）\n2）可用条件是什么（金手指、人脉、资源、知识）\n3）解决方案是什么（短期目标、中期计划、终极目标）\n4）阻扰因素是什么（反派、环境局限、资源匮乏、自身缺陷）\n\n设定：{setting}",
    },
    "director_approve": {
        "system": "你是资深网文AI导演。在写每一章之前，审查规划方案是否合理。如果发现规划有问题，指出风险。",
        "user": "审查以下章节规划方案：\n第{chapter}章\n题材：{genre}\n平台：{platform}\n规划摘要：{plan_summary}\n\n请判断：1）本章规划是否服务于主线 2）是否存在逻辑风险 3）需要调整的地方",
    },
    "chapter_acceptance": {
        "system": "你是严格的验收编辑。评估本章是否达到交付标准。",
        "user": "验收以下章节：\n第{chapter}章\n平台：{platform}\n题材：{genre}\n正文开头：{text}\n\n检测问题：{issues}\n\n请判断：通过或拒绝。如果拒绝，说明具体原因。",
    },
    "outline": {
        "system": "你是网文大纲规划师。生成清晰的分卷大纲。",
        "user": "题材：{genre}\n平台：{platform}\n章节：{chapters}\n情绪：{emotion}\n\n生成大纲：",
    },
    "character": {
        "system": "生成结构化角色档案：姓名、身份、外貌、性格、背景、目标、缺陷、成长弧。",
        "user": "角色：{name}\n类型：{role_type}\n世界观：{world}\n\n生成档案：",
    },
    "rewrite": {
        "system": "你是一名中文网文编辑。修改以下文本中的AI痕迹问题。保持原意和风格。",
        "user": "【原文】\n{text}\n\n【问题】\n{issues}\n\n请修改：",
    },
    "hook_planning": {
        "system": "你是有经验的网文伏笔规划师。根据已写内容和待回收伏笔，规划下一阶段伏笔埋设方案。",
        "user": "已写章节范围：{written}\n大纲概要：{outline}\n待规划伏笔：{pending_hooks}\n\n请规划本阶段伏笔埋设方案：",
    },
}

CHINESE_KEY_MAP = {
    "大纲": "outline", "人物卡": "character", "写作": "write_chapter",
    "修改": "rewrite", "章节": "write_chapter", "伏笔规划": "hook_planning",
    "大纲审查": "review_outline", "章节审查": "review_chapter",
    "细纲": "generate_细纲", "章纲": "generate_章纲",
    "全维度审查": "full_dimension_review", "三要素分析": "proposition_review",
    "导演审批": "director_approve", "章节验收": "chapter_acceptance",
}

# ============================================================
# TextGenerator — 自适应多 Provider 生成器
# ============================================================

class TextGenerator:
    """零配置自适应生成器。

    启动时自动扫描环境，发现所有可用 provider。
    生成时按优先级自动选择，支持 L3 三段温度震荡。
    """

    def __init__(self, config=None, provider=None):
        self.config = config or load_config()
        self._providers = self._init_providers(provider)
        self._provider_info = self._get_provider_info()

    def _init_providers(self, preferred=None):
        """自动发现 + 初始化所有可用 provider"""
        discovered = discover_providers()
        providers = []

        # 1. SessionProvider（CodeBuddy Skill 环境）
        session = SessionProvider()
        if session.available():
            providers.append(("session", session))

        # 2. 自动发现的 provider
        for info in discovered:
            if info["name"] == "ollama":
                ollama = OllamaProvider(info["model"], info["base_url"])
                if ollama.available():
                    providers.append(("ollama", ollama))
            else:
                p = UnifiedProvider(
                    info["name"], info["base_url"], info["api_key"], info["model"]
                )
                if p.available():
                    providers.append((info["name"], p))

        if not providers:
            logger.warning(
                "TextGenerator: 未发现任何可用 LLM provider。\n"
                "  请设置以下任一环境变量：\n"
                "  - DEEPSEEK_API_KEY\n"
                "  - OPENAI_API_KEY\n"
                "  - DASHSCOPE_API_KEY（通义千问）\n"
                "  - ZHIPU_API_KEY（智谱）\n"
                "  - MOONSHOT_API_KEY（月之暗面）\n"
                "  - 或安装 Ollama：ollama pull qwen3"
            )

        return providers

    def _get_provider_info(self) -> str:
        """获取可用 provider 信息摘要"""
        if not self._providers:
            return "无可用 provider"
        names = [f"{n}({p.model if hasattr(p, 'model') else 'session'})" for n, p in self._providers]
        return f"可用: {', '.join(names)}"

    @property
    def available_providers(self) -> list:
        return [name for name, _ in self._providers]

    def generate(self, task, **kwargs):
        """按优先级自动选择 provider 生成内容"""
        task = CHINESE_KEY_MAP.get(task, task)
        prompt_def = LOCAL_PROMPTS.get(task)
        if not prompt_def:
            return ""

        system = prompt_def["system"]
        template = prompt_def["user"]
        placeholders = set(re.findall(r"\{(\w+)\}", template))
        provided = set(kwargs.keys())
        missing = placeholders - provided
        if missing:
            logger.warning(f"generate: 模板缺少参数: {sorted(missing)}, task={task}")
            return ""

        try:
            user = template.format(**kwargs)
        except KeyError as e:
            logger.warning(f"generate: 模板缺少参数 {e}")
            return ""

        # 注入 writing_notes
        wn = kwargs.get("writing_notes")
        if wn and isinstance(wn, list) and task == "write_chapter":
            user += "\n\n[写作指导]\n" + "\n".join(f"- {note}" for note in wn)

        errors = []
        for name, prov in self._providers:
            try:
                result = prov.generate(system, user)
                if result and len(result) > 20:
                    logger.info(f"generate({task}): {name} 成功 ({len(result)} chars)")
                    return result
            except Exception as e:
                msg = f"{name}: {e}"
                logger.warning(f"generate({task}): {msg}")
                errors.append(msg)
                continue

        error_msg = "; ".join(errors) if errors else "所有 provider 返回空或短文本"
        logger.error(f"generate({task}): 所有生成器失败 - {error_msg}")
        return ""

    def generate_l3(self, task, **kwargs):
        """L3 三段温度震荡生成（角色坍缩防护）"""
        task = CHINESE_KEY_MAP.get(task, task)
        system, user = self._build_l3_prompt(task, **kwargs)
        if not system or not user:
            return self.generate(task, **kwargs)

        base_temp = self.config.get("temperature", 0.7)
        temps = [base_temp - 0.05, base_temp + 0.15, base_temp - 0.15]
        n_temps = len(temps)

        n_segments = 3
        seg_labels = [
            "请写本章开头（开场切入，300字内埋钩子）",
            "请写本章中段（展开情节，推进矛盾，深化冲突）",
            "请写本章结尾（铺垫高潮，收束留悬念钩子）",
        ]
        results = []
        seg_users = []
        for i in range(n_segments):
            seg_user = f"{user}\n\n【第{i+1}/{n_segments}段】\n{seg_labels[i]}"
            seg_users.append(seg_user)
            temp = temps[i % n_temps]
            for name, prov in self._providers:
                try:
                    result = prov.generate(system, seg_user, temperature=temp)
                    if result and len(result) > 10:
                        results.append(result)
                        break
                except Exception:
                    continue

        if len(results) >= 2:
            smoothed = [results[0]]
            for i in range(1, len(results)):
                prev_end = results[i-1][-80:].rstrip()
                if not prev_end.endswith(("。", "！", "？", '"', "」")):
                    smoothed.append("\n\n")
                elif not results[i][:10].lstrip().startswith(("但", "可", "而", "这", "他", "她")):
                    smoothed.append("\n他顿了顿，继续往下想。\n\n")
                else:
                    smoothed.append("\n\n")
                smoothed.append(results[i])
            full = "".join(smoothed)
        else:
            full = "\n\n".join(results) if results else ""

        # 角色一致性校验
        if len(results) >= 2:
            from collections import Counter as _Counter
            main_chars = {}
            _noise = {"什么", "怎么", "这样", "那样", "自己", "这个", "那个", "可以", "没有",
                       "不是", "因为", "所以", "如果", "虽然", "但是", "而且", "或者", "还是",
                       "只是", "就是", "可是", "然而", "于是", "然后", "可能", "应该", "能够",
                       "需要", "知道", "觉得", "看见", "听见", "回到", "来到", "跟着", "看着",
                       "想着", "说道", "问道", "喊道"}
            for seg_idx, seg in enumerate(results):
                early_text = seg[:max(300, len(seg)//3)]
                names = re.findall(r"[一-鿿]{2,4}", early_text)
                cnts = _Counter()
                for n in names:
                    if n not in _noise:
                        cnts[n] += 1
                top2 = cnts.most_common(2) if cnts else []
                main_chars[seg_idx] = [n for n, c in top2 if c >= 3]
            if 0 in main_chars and main_chars[0]:
                ref = set(main_chars[0])
                for seg_idx in range(1, len(results)):
                    if seg_idx not in main_chars or not main_chars[seg_idx]:
                        continue
                    seg_set = set(main_chars[seg_idx])
                    if ref & seg_set:
                        continue
                    prev_temp = temps[(seg_idx-1) % n_temps]
                    seg_prompt = seg_users[seg_idx] if seg_idx < len(seg_users) else seg_users[-1]
                    for name, prov in self._providers:
                        try:
                            r2 = prov.generate(system, seg_prompt, temperature=prev_temp)
                            if r2 and len(r2) > 10:
                                n2 = re.findall(r"[一-鿿]{2,4}", r2[:200])
                                c2 = _Counter(n for n in n2 if n not in _noise)
                                new_top = [n for n, _ in c2.most_common(2) if c2[n] >= 3]
                                if ref & set(new_top):
                                    results[seg_idx] = r2
                                    break
                        except Exception:
                            continue

        return full if len(full) > 150 else self.generate(task, **kwargs)

    def _build_l3_prompt(self, task, **kwargs):
        prompt_def = LOCAL_PROMPTS.get(task)
        if not prompt_def:
            return None, None
        platform = kwargs.get("platform", "")
        writer_id = get_writer_identity(platform)
        if writer_id and task == "write_chapter":
            base_system = prompt_def["system"]
            prompt_def = dict(prompt_def)
            prompt_def["system"] = writer_id + "\n\n" + base_system
        genre = kwargs.get("genre", "")
        genre_prompt = get_genre_prompt(genre)
        if genre_prompt and task == "write_chapter":
            if not isinstance(prompt_def, dict):
                prompt_def = dict(prompt_def)
            prompt_def["system"] = prompt_def["system"] + "\n\n" + genre_prompt
        if task == "write_chapter":
            exp_techniques = "\n【期待感技法】\n- 每章结尾必须是新问题而非旧答案（痒的法则）\n- 承诺要兑现：前面描写的伏笔和悬念必须在后续有回应\n- 读者预期管理：给一点不满足，再给更多，循环递进\n- 角色关系期待：让读者想知道「接下来会怎么样」\n- 反转频率：每3-5章至少1次有效反转\n【内容扩展技法】\n- 如果某段只有概述，展开为具体场景（时间/地点/人物/对话/动作）\n- 单段不超过3句，太长的拆开\n- 关键情节点用感官细节填充（看到的+听到的+感受到的）\n- 对话互动至少要有「问-答-反应」三步\n- 战斗/对抗场景用短句交替推进节奏"
            if not isinstance(prompt_def, dict):
                prompt_def = dict(prompt_def)
            prompt_def["system"] += exp_techniques
        L3_CONSTRAINTS = "\n\n" + "\n".join([
            "[去痕约束]",
            "- 禁止使用：毋庸置疑、不可否认、值得一提的是、总而言之",
            "- 每段不超过3句，句长18-48字混合",
            "- 至少1处用具体身体动作替代心理描写",
            '- 对话用动作标签，不用"说"字',
            "- 禁止模板结尾：他终于明白了/更大的挑战还在后面",
            "",
            "[角色限定]",
            "- 以该章主角的第三人称有限视角写作，不使用上帝视角",
            "- 只描写主角能看见、听见、感受到的东西",
            "- 如果主角无法判断的事情，直接写不知道或猜测",
            "",
            "[思维暴露]",
            "- 每表达一个观点前，先写1-2句思考过程",
            "- 不要只给结论，要让读者看到主角得出结论的过程",
        ])
        system = prompt_def["system"] + L3_CONSTRAINTS
        try:
            user = prompt_def["user"].format(**kwargs)
        except KeyError:
            return None, None
        user += "\n\n" + "\n".join([
            "[自反驳结构]",
            "- 对每个主要情节点：先写陈述，再写但这里有问题，再写重新考虑后认为",
            "",
            "[统计签名]",
            "- 每500字插入1处口语化表达（啧、得嘞、靠等）",
            "- 刻意控制句长方差大于8（长短交替）",
        ])
        return system, user

    @staticmethod
    def style_lock(platform):
        locks = {
            "番茄": "极快节奏,短段,40%对话,章末钩子",
            "起点": "质量优先,世界观深",
            "七猫": "情感线优先",
            "飞卢": "500字内给系统",
        }
        return locks.get(platform, "正常节奏")

    @staticmethod
    def save_config(path, config):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

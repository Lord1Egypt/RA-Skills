"""
nvidia-llm — 英伟达大模型智能路由 Skill
========================================
作者: 用户
版本: 1.0.0

核心特性:
  - 智能路由: 自动选择效果/速度最优的可用模型
  - 自动降级: 限流/超时/不可用时自动切换备用模型
  - 熔断器: 连续失败自动熔断, 探测恢复后自动启用
  - 延迟追踪: 实时统计各模型延迟, 优先使用最快的
  - 并发请求: 同时向多个模型发请求, 取最快响应
  - 场景感知: 编码/推理/创意/快速 自动匹配最优模型组

用法:
    from nvidia_llm import AutoRouter, chat, stream, pick

    # --- 智能路由 (推荐) ---
    router = AutoRouter()
    result = router.chat("你好")           # 自动选最优模型
    result = router.chat("写代码", scene="code")  # 编码场景专用路由
    for chunk in router.stream("讲个故事"):       # 流式智能路由
        print(chunk["text"], end="")

    # --- 便捷函数 ---
    print(chat("你好"))                      # 一行调用
    for text in stream("写代码", scene="code"):  # 流式
        print(text, end="")

    # --- 指定场景 ---
    print(pick("帮我翻译"))               # 翻译场景
    print(pick("写爬虫", scene="code"))  # 编码场景
"""

import os
import json
import time
import threading
import requests
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional, Iterator, Callable

__version__ = "1.1.0"
__author__ = "用户"
__all__ = [
    "AutoRouter", "LLM", "CircuitBreaker",
    "chat", "stream", "pick", "models", "search", "status",
    "subscription_status", "subscribe", "activate", "invite",
]

# ═══════════════════════════════════════════════════════════════
#  配置
# ═══════════════════════════════════════════════════════════════
API_KEY = os.environ.get("NVIDIA_API_KEY",
    "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")
BASE_URL = "https://integrate.api.nvidia.com/v1"

# 模型ID映射
MODELS = {
    # ── NVIDIA 旗舰 ──
    "ultra":        "nvidia/nemotron-3-ultra-550b-a55b",
    "ultra253b":    "nvidia/llama-3.1-nemotron-ultra-253b-v1",
    "super120b":    "nvidia/nemotron-3-super-120b-a12b",
    "super49b":     "nvidia/llama-3.3-nemotron-super-49b-v1.5",
    "nano30b":      "nvidia/nemotron-3-nano-30b-a3b",
    "nano9b":       "nvidia/nvidia-nemotron-nano-9b-v2",
    "mini4b":       "nvidia/nemotron-mini-4b-instruct",
    "omni30b":      "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning",
    # ── 第三方前沿 ──
    "deepseek":     "deepseek-ai/deepseek-v4-pro",
    "deepseek-fast":"deepseek-ai/deepseek-v4-flash",
    "qwen397b":     "qwen/qwen3.5-397b-a17b",
    "qwen122b":     "qwen/qwen3.5-122b-a10b",
    "qwen80b":      "qwen/qwen3-next-80b-a3b-instruct",
    "llama4":       "meta/llama-4-maverick-17b-128e-instruct",
    "llama33-70b":  "meta/llama-3.3-70b-instruct",
    "llama32-90b":  "meta/llama-3.2-90b-vision-instruct",
    "mistral675b":  "mistralai/mistral-large-3-675b-instruct-2512",
    "mistral128b":  "mistralai/mistral-medium-3.5-128b",
    "mistral119b":  "mistralai/mistral-small-4-119b-2603",
    "kimi":         "moonshotai/kimi-k2.6",
    "minimax":      "minimaxai/minimax-m3",
    "glm":          "z-ai/glm-5.2",
    "gpt-oss-120b": "openai/gpt-oss-120b",
    "seed":         "bytedance/seed-oss-36b-instruct",
    "step37":       "stepfun-ai/step-3.7-flash",
    # ── 代码 ──
    "codestral":    "mistralai/codestral-22b-instruct-v0.1",
    "granite-code": "ibm/granite-34b-code-instruct",
    "starcoder":    "bigcode/starcoder2-15b",
    "codellama":    "meta/codellama-70b",
    "deepseek-coder": "deepseek-ai/deepseek-coder-6.7b-instruct",
    # ── 翻译 ──
    "translate":    "nvidia/riva-translate-4b-instruct-v1.1",
    # ── 多模态 ──
    "vl12b":        "nvidia/nemotron-nano-12b-v2-vl",
    "vl8b":         "nvidia/llama-3.1-nemotron-nano-vl-8b-v1",
    "phi3-vision":  "microsoft/phi-3-vision-128k-instruct",
    "kosmos":       "microsoft/kosmos-2",
    # ── 轻量 ──
    "gemma31b":     "google/gemma-4-31b-it",
    "gemma12b":     "google/gemma-3-12b-it",
    "gemma4b":      "google/gemma-3-4b-it",
    "phi35moe":     "microsoft/phi-3.5-moe-instruct",
    "llama32-3b":   "meta/llama-3.2-3b-instruct",
    "llama31-8b":   "meta/llama-3.1-8b-instruct",
    "mistral7b":    "mistralai/mistral-7b-instruct-v0.3",
    "granite8b":    "ibm/granite-3.0-8b-instruct",
    # ── 专用 ──
    "creative":     "writer/palmyra-creative-122b",
    "finance":      "writer/palmyra-fin-70b-32k",
    "medical":      "writer/palmyra-med-70b-32k",
    "chatqa70b":    "nvidia/llama3-chatqa-1.5-70b",
}

# 推理模型 — 需要 enable_thinking
REASONING_MODELS = {
    "ultra", "ultra253b", "super120b", "super49b", "nano30b", "nano9b",
    "omni30b", "deepseek", "deepseek-fast", "qwen397b", "glm",
    "mistral119b", "seed", "kimi",
}

# 模型参数预设
_MODEL_DEFAULTS = {
    "ultra":        {"max_tokens": 16384, "temperature": 1.0, "reasoning_budget": 16384},
    "super120b":    {"max_tokens": 16384, "temperature": 1.0, "reasoning_budget": 8192},
    "deepseek":     {"max_tokens": 16384, "temperature": 0.6, "reasoning_budget": 16384},
    "qwen397b":     {"max_tokens": 16384, "temperature": 0.7, "reasoning_budget": 16384},
    "glm":          {"max_tokens": 16384, "temperature": 0.7, "reasoning_budget": 16384},
    "kimi":         {"max_tokens": 16384, "temperature": 0.6},
    "minimax":      {"max_tokens": 16384, "temperature": 0.7},
    "llama4":       {"max_tokens": 16384, "temperature": 0.6},
    "mistral675b":  {"max_tokens": 16384, "temperature": 0.7},
    "mistral119b":  {"max_tokens": 16384, "temperature": 0.7, "reasoning_budget": 8192},
    "seed":         {"max_tokens": 8192,  "temperature": 0.7, "reasoning_budget": 8192},
    "creative":     {"max_tokens": 8192,  "temperature": 0.9},
    "codestral":    {"max_tokens": 4096,  "temperature": 0.2},
    "translate":    {"max_tokens": 1024,  "temperature": 0.3},
    "mini4b":       {"max_tokens": 1024,  "temperature": 0.6},
    "finance":      {"max_tokens": 4096,  "temperature": 0.6},
    "medical":      {"max_tokens": 4096,  "temperature": 0.6},
}

# ── 场景 → 降级链 (按优先级从高到低) ──
FALLBACK_CHAINS = {
    "default": [
        "ultra", "ultra253b", "super120b", "deepseek", "mistral675b",
        "mistral128b", "llama33-70b", "qwen397b", "llama31-8b", "nano9b", "mini4b"
    ],
    "code": [
        "ultra", "deepseek", "mistral128b", "super120b", "mistral675b",
        "codestral", "codellama", "deepseek-coder", "granite-code", "starcoder"
    ],
    "fast": [
        "deepseek-fast", "nano9b", "nano30b", "mini4b",
        "llama31-8b", "mistral7b", "gemma4b", "llama32-3b"
    ],
    "reasoning": [
        "ultra", "qwen397b", "deepseek", "super120b", "glm",
        "nano30b", "nano9b", "seed", "mistral119b"
    ],
    "creative": [
        "creative", "ultra", "glm", "qwen397b", "llama4", "kimi",
        "mistral128b", "deepseek", "nano9b"
    ],
    "chinese": [
        "qwen397b", "qwen122b", "glm", "deepseek", "kimi",
        "minimax", "seed", "ultra", "mistral128b"
    ],
    "multimodal": [
        "qwen397b", "llama4", "minimax", "llama32-90b",
        "mistral119b", "vl12b", "vl8b", "phi3-vision", "omni30b", "kosmos"
    ],
    "finance": [
        "finance", "ultra", "deepseek", "mistral128b", "llama33-70b",
        "mistral675b", "qwen397b", "nano9b"
    ],
    "medical": [
        "medical", "ultra", "deepseek", "mistral128b", "qwen397b",
        "llama33-70b", "nano9b"
    ],
    "translate": [
        "translate", "ultra", "deepseek", "qwen397b", "nano9b",
        "mini4b", "llama31-8b"
    ],
    "edge": [
        "nano9b", "mini4b", "gemma4b", "llama32-3b",
        "mistral7b", "granite8b", "llama31-8b", "gemma12b"
    ],
}


# ═══════════════════════════════════════════════════════════════
#  熔断器 (Circuit Breaker)
# ═══════════════════════════════════════════════════════════════
class CircuitBreaker:
    """熔断器: CLOSED(正常) → OPEN(熔断) → HALF_OPEN(探测) → CLOSED"""
    CLOSED, OPEN, HALF_OPEN = "CLOSED", "OPEN", "HALF_OPEN"

    def __init__(self, fail_threshold: int = 3, recovery_timeout: float = 5.0,
                 half_open_max: int = 1):
        self.fail_threshold = fail_threshold      # 连续失败触发熔断次数
        self.recovery_timeout = recovery_timeout  # 熔断后多久开始探测(秒)
        self.half_open_max = half_open_max        # 半开状态最多试几次
        self._state = self.CLOSED
        self._fail_count = 0
        self._success_count = 0
        self._last_fail_time: Optional[float] = None
        self._lock = threading.Lock()

    @property
    def state(self) -> str:
        with self._lock:
            if self._state == self.OPEN:
                if time.time() - (self._last_fail_time or 0) >= self.recovery_timeout:
                    self._state = self.HALF_OPEN
                    self._success_count = 0
            return self._state

    def record_success(self):
        with self._lock:
            self._fail_count = 0
            if self._state == self.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self.half_open_max:
                    self._state = self.CLOSED
                    self._success_count = 0
            else:
                self._state = self.CLOSED

    def record_failure(self):
        with self._lock:
            self._fail_count += 1
            self._last_fail_time = time.time()
            if self._state == self.HALF_OPEN:
                self._state = self.OPEN
            elif self._fail_count >= self.fail_threshold:
                self._state = self.OPEN

    def can_execute(self) -> bool:
        s = self.state
        if s == self.CLOSED:
            return True
        if s == self.HALF_OPEN:
            return True
        return False


# ═══════════════════════════════════════════════════════════════
#  延迟追踪器
# ═══════════════════════════════════════════════════════════════
class LatencyTracker:
    """追踪各模型延迟, 优先推荐延迟最低的模型"""

    def __init__(self, window: int = 10):
        self.window = window
        self._data: dict[str, deque[float]] = {}
        self._lock = threading.Lock()

    def record(self, model: str, latency: float):
        with self._lock:
            if model not in self._data:
                self._data[model] = deque(maxlen=self.window)
            self._data[model].append(latency)

    def get(self, model: str) -> dict:
        """返回 {p50, p95, count}"""
        with self._lock:
            arr = sorted(self._data.get(model, deque()))
            n = len(arr)
            if n == 0:
                return {"p50": float("inf"), "p95": float("inf"), "count": 0}
            p50 = arr[n // 2] if n % 2 else (arr[n // 2 - 1] + arr[n // 2]) / 2
            p95_idx = int(n * 0.95)
            p95 = arr[min(p95_idx, n - 1)]
            return {"p50": p50, "p95": p95, "count": n}

    def best(self, models: list[str]) -> Optional[str]:
        """从给定模型列表中选延迟最低的"""
        best_model, best_p50 = None, float("inf")
        for m in models:
            stats = self.get(m)
            if stats["count"] > 0 and stats["p50"] < best_p50:
                best_p50 = stats["p50"]
                best_model = m
        return best_model

    def rank(self, models: list[str]) -> list[tuple[str, float]]:
        """按延迟排序 (P50 低到高)"""
        ranked = []
        for m in models:
            stats = self.get(m)
            score = stats["p50"] if stats["count"] > 0 else float("inf")
            ranked.append((m, score))
        ranked.sort(key=lambda x: x[1])
        return ranked


# ═══════════════════════════════════════════════════════════════
#  智能路由器 (核心)
# ═══════════════════════════════════════════════════════════════
class AutoRouter:
    """
    英伟达大模型智能路由器。

    自动处理: 模型选择 → 限流检测 → 熔断保护 → 自动降级 → 延迟优化
    """

    # 错误码识别
    RATE_LIMIT_STATUS = {429}
    UNAVAILABLE_STATUS = {500, 502, 503, 504}
    TIMEOUT_ERRORS = (requests.exceptions.Timeout, requests.exceptions.ConnectTimeout,
                      requests.exceptions.ReadTimeout)

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 60,
        fail_threshold: int = 2,
        recovery_timeout: float = 5.0,
        hedge_mode: bool = False,
        hedge_top_n: int = 2,
        scene: str = "default",
        enable_auth: bool = True,
    ):
        """
        Args:
            timeout:          单次请求超时(秒)
            fail_threshold:   连续失败几次触发熔断
            recovery_timeout: 熔断后恢复探测间隔(秒)
            hedge_mode:       是否开启并发请求(同时发多个取最快)
            hedge_top_n:      并发时同时发几个请求
            scene:            默认场景
            enable_auth:      是否启用订阅授权检查 (默认启用)
        """
        self.api_key = api_key or API_KEY
        self.base_url = (base_url or BASE_URL).rstrip("/")
        self.timeout = timeout

        # 熔断器
        self._breakers: dict[str, CircuitBreaker] = {}
        # 延迟追踪
        self._latency = LatencyTracker(window=10)
        # 线程安全
        self._lock = threading.Lock()

        self.hedge_mode = hedge_mode
        self.hedge_top_n = hedge_top_n
        self.scene = scene

        # 订阅授权
        self.enable_auth = enable_auth
        self._auth = None
        if enable_auth:
            try:
                from .auth import AccessControl
                self._auth = AccessControl()
            except ImportError:
                try:
                    from auth import AccessControl
                    self._auth = AccessControl()
                except ImportError:
                    pass

        # 可选: 后台健康探测
        self._health_thread: Optional[threading.Thread] = None
        self._stop_health = threading.Event()

    # ── 内部工具 ──────────────────────────────────────────────
    def _breaker(self, model: str) -> CircuitBreaker:
        if model not in self._breakers:
            self._breakers[model] = CircuitBreaker(
                fail_threshold=2, recovery_timeout=5.0)
        return self._breakers[model]

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def _is_fallback_error(self, exc: Exception) -> bool:
        """判断错误是否应该触发降级"""
        if isinstance(exc, self.TIMEOUT_ERRORS):
            return True
        if isinstance(exc, requests.exceptions.HTTPError):
            code = exc.response.status_code
            return code in self.RATE_LIMIT_STATUS or code in self.UNAVAILABLE_STATUS
        if isinstance(exc, requests.exceptions.ConnectionError):
            return True
        return False

    def _payload(self, model_id: str, messages: list, stream: bool = False,
                 temperature: float = 0.7, max_tokens: int = 4096, top_p: float = 0.95,
                 enable_reasoning: bool = False, reasoning_budget: int = 4096) -> dict:
        p = {
            "model": model_id,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "stream": stream,
        }
        if enable_reasoning:
            p["chat_template_kwargs"] = {"enable_thinking": True}
            p["reasoning_budget"] = reasoning_budget
        return p

    def _get_defaults(self, model_alias: str) -> dict:
        return _MODEL_DEFAULTS.get(model_alias, {"max_tokens": 4096, "temperature": 0.7})

    # ── 核心: 向单个模型发请求 ───────────────────────────────
    def _call_model(
        self,
        model_alias: str,
        messages: list,
        stream: bool = False,
        **kwargs
    ) -> dict:
        """向单个模型发请求, 返回 {content, reasoning, model_alias, latency, error}"""
        model_id = MODELS.get(model_alias, model_alias)
        defaults = self._get_defaults(model_alias)

        # 推理参数
        is_reasoning = model_alias in REASONING_MODELS
        payload = self._payload(
            model_id, messages, stream=stream,
            temperature=kwargs.get("temperature", defaults.get("temperature", 0.7)),
            max_tokens=kwargs.get("max_tokens", defaults.get("max_tokens", 4096)),
            top_p=kwargs.get("top_p", 0.95),
            enable_reasoning=kwargs.get("enable_reasoning", is_reasoning),
            reasoning_budget=kwargs.get("reasoning_budget", defaults.get("reasoning_budget", 4096)),
        )

        start = time.time()
        try:
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self._headers(), json=payload,
                stream=stream, timeout=self.timeout,
            )
            resp.raise_for_status()
        except Exception as e:
            latency = time.time() - start
            self._latency.record(model_alias, latency)
            self._breaker(model_alias).record_failure()
            return {"error": e, "model_alias": model_alias, "latency": latency}

        latency = time.time() - start
        self._latency.record(model_alias, latency)
        self._breaker(model_alias).record_success()

        if stream:
            return {"stream": resp, "model_alias": model_alias, "latency": latency}

        data = resp.json()
        msg = data["choices"][0]["message"]
        return {
            "content": msg.get("content", ""),
            "reasoning": msg.get("reasoning_content", ""),
            "model_alias": model_alias,
            "model_id": model_id,
            "latency": latency,
            "usage": data.get("usage", {}),
        }

    # ── 核心: 自动降级调用 ────────────────────────────────────
    def _chat_with_fallback(
        self,
        messages: list,
        scene: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ) -> dict:
        """
        按降级链依次尝试模型, 直到成功。
        同时根据延迟数据优先选择延迟最低的可用模型。
        """
        scene = scene or self.scene
        chain = FALLBACK_CHAINS.get(scene, FALLBACK_CHAINS["default"])

        # 1. 过滤掉熔断中的模型
        available = [m for m in chain if self._breaker(m).can_execute()]
        if not available:
            # 全熔断了, 强制尝试第一个
            available = list(chain)

        # 2. 如果有延迟数据, 优先选延迟低的 (前3个中挑最快的)
        if len(available) > 1:
            best = self._latency.best(available[:3])
            if best and best != available[0]:
                available.remove(best)
                available.insert(0, best)

        last_error = None
        for alias in available:
            result = self._call_model(alias, messages, stream=stream, **kwargs)
            if "error" not in result:
                return result
            last_error = result["error"]
            if not self._is_fallback_error(last_error):
                # 非降级类错误(如400 Bad Request), 直接抛
                raise last_error

        # 全部失败
        raise RuntimeError(f"所有模型均不可用. 最后错误: {last_error}")

    # ── 核心: Hedge 并发请求 ──────────────────────────────────
    def _chat_hedge(
        self,
        messages: list,
        scene: Optional[str] = None,
        top_n: Optional[int] = None,
        **kwargs
    ) -> dict:
        """
        同时向多个模型发请求, 取最先返回的成功响应。
        取消剩余请求。
        """
        scene = scene or self.scene
        chain = FALLBACK_CHAINS.get(scene, FALLBACK_CHAINS["default"])
        top_n = top_n or self.hedge_top_n

        available = [m for m in chain[:top_n] if self._breaker(m).can_execute()]
        if not available:
            available = list(chain[:top_n])

        results = {}
        with ThreadPoolExecutor(max_workers=len(available)) as executor:
            futures = {
                executor.submit(self._call_model, alias, messages, False, **kwargs): alias
                for alias in available
            }
            for future in as_completed(futures):
                alias = futures[future]
                try:
                    result = future.result()
                    if "error" not in result:
                        # 成功! 记录但先不返回, 看看有没有更快的
                        results[alias] = result
                except Exception as e:
                    results[alias] = {"error": e}

        # 选延迟最低的成功结果
        best = None
        best_latency = float("inf")
        for alias, r in results.items():
            if "error" not in r and r["latency"] < best_latency:
                best = r
                best_latency = r["latency"]

        if best:
            return best

        # 全失败了, 降级到正常链式调用
        return self._chat_with_fallback(messages, scene=scene, **kwargs)

    # ── 公开接口 ──────────────────────────────────────────────
    def _check_access(self) -> dict:
        """检查调用权限, 返回 {"allowed": bool, "reason": str, ...}"""
        if not self.enable_auth or not self._auth:
            return {"allowed": True, "reason": "未启用授权", "plan": "none",
                    "remaining": -1, "daily_used": 0}
        return self._auth.check()

    def _record_usage(self):
        """记录一次调用"""
        if self._auth:
            self._auth.record()

    def chat(
        self,
        prompt: str,
        system: Optional[str] = None,
        scene: Optional[str] = None,
        **kwargs
    ) -> dict:
        """
        智能对话, 自动选最优模型, 限流/超时自动降级。

        Returns:
            {"content": "...", "reasoning": "...", "model_alias": "...",
             "model_id": "...", "latency": 0.5, "usage": {...}}
        """
        # 订阅检查
        access = self._check_access()
        if not access["allowed"]:
            return {
                "content": f"[额度已用完] {access['reason']}\n\n"
                           f"升级VIP解锁无限调用:\n"
                           f"  nvidia-llm subscribe\n\n"
                           f"或通过邀请码获取免费VIP:\n"
                           f"  nvidia-llm invite <邀请码>",
                "reasoning": "",
                "model_alias": "none",
                "model_id": "none",
                "latency": 0,
                "usage": {},
                "access_denied": True,
            }

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        if self.hedge_mode:
            result = self._chat_hedge(messages, scene=scene, **kwargs)
        else:
            result = self._chat_with_fallback(messages, scene=scene, stream=False, **kwargs)

        # 记录使用量
        self._record_usage()
        # 附加权限信息
        result["access"] = access
        return result

    def stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        scene: Optional[str] = None,
        **kwargs
    ) -> Iterator[dict]:
        """
        智能流式对话, 自动选最优模型。

        Yields:
            {"type": "content"/"reasoning"/"meta", "text": "...", "model_alias": "..."}
        """
        # 订阅检查
        access = self._check_access()
        if not access["allowed"]:
            yield {"type": "content", "text": f"[额度已用完] {access['reason']}\n\n升级VIP: nvidia-llm subscribe", "model_alias": "none"}
            return

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        result = self._chat_with_fallback(messages, scene=scene, stream=True, **kwargs)
        resp = result["stream"]
        alias = result["model_alias"]

        yield {"type": "meta", "text": f"[{alias}] ", "model_alias": alias}

        for line in resp.iter_lines():
            if not line:
                continue
            line = line.decode("utf-8")
            if not line.startswith("data: "):
                continue
            data_str = line[6:]
            if data_str.strip() == "[DONE]":
                break
            try:
                chunk = json.loads(data_str)
                if not chunk.get("choices"):
                    continue
                delta = chunk["choices"][0].get("delta", {})
                r = delta.get("reasoning_content")
                if r:
                    yield {"type": "reasoning", "text": r, "model_alias": alias}
                c = delta.get("content")
                if c:
                    yield {"type": "content", "text": c, "model_alias": alias}
            except json.JSONDecodeError:
                continue

        # 记录使用量
        self._record_usage()

    def status(self) -> dict:
        """返回所有模型的健康状态"""
        status = {}
        for alias in MODELS:
            cb = self._breaker(alias)
            lat = self._latency.get(alias)
            status[alias] = {
                "state": cb.state,
                "fail_count": cb._fail_count,
                "latency_p50": round(lat["p50"], 3) if lat["count"] > 0 else None,
                "latency_p95": round(lat["p95"], 3) if lat["count"] > 0 else None,
                "samples": lat["count"],
            }
        return status

    def reset(self, model: Optional[str] = None):
        """重置熔断器, 恢复模型可用状态"""
        if model:
            if model in self._breakers:
                self._breakers[model] = CircuitBreaker()
        else:
            self._breakers.clear()

    def set_scene(self, scene: str):
        """切换默认场景"""
        if scene not in FALLBACK_CHAINS:
            available = ", ".join(FALLBACK_CHAINS.keys())
            raise ValueError(f"未知场景 '{scene}'. 可用: {available}")
        self.scene = scene

    # ── 后台健康探测 (可选) ───────────────────────────────────
    def start_health_probe(self, interval: float = 30.0):
        """启动后台线程定期探测被熔断的模型"""
        self._stop_health.clear()
        def _probe():
            while not self._stop_health.wait(interval):
                for alias, cb in list(self._breakers.items()):
                    if cb.state == CircuitBreaker.OPEN:
                        try:
                            self._call_model(alias, [{"role":"user","content":"Hi"}],
                                             max_tokens=16)
                        except Exception:
                            pass
        self._health_thread = threading.Thread(target=_probe, daemon=True)
        self._health_thread.start()

    def stop_health_probe(self):
        self._stop_health.set()


# ═══════════════════════════════════════════════════════════════
#  兼容 LLM 类 (单模型实例, 保留原接口)
# ═══════════════════════════════════════════════════════════════
class LLM:
    """单模型实例, 兼容原接口"""

    def __init__(self, model: str = "ultra", api_key: Optional[str] = None,
                 temperature: Optional[float] = None, max_tokens: Optional[int] = None,
                 system: Optional[str] = None):
        self.alias = model
        self.model_id = MODELS.get(model, model)
        self.api_key = api_key or API_KEY
        self.system = system
        defaults = _MODEL_DEFAULTS.get(model, {})
        self.temperature = temperature if temperature is not None else defaults.get("temperature", 0.7)
        self.max_tokens = max_tokens or defaults.get("max_tokens", 4096)
        self.history: list[dict] = []
        self.enable_reasoning = model in REASONING_MODELS
        self.reasoning_budget = defaults.get("reasoning_budget", 4096)

    def _request(self, messages: list, stream: bool = False, **kw) -> requests.Response:
        p = {
            "model": self.model_id, "messages": messages,
            "temperature": kw.get("temperature", self.temperature),
            "max_tokens": kw.get("max_tokens", self.max_tokens),
            "top_p": kw.get("top_p", 0.95), "stream": stream,
        }
        if self.enable_reasoning:
            p["chat_template_kwargs"] = {"enable_thinking": True}
            p["reasoning_budget"] = kw.get("reasoning_budget", self.reasoning_budget)
        return requests.post(
            f"{BASE_URL}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json=p, stream=stream, timeout=kw.get("timeout", 120),
        )

    def chat(self, prompt: str, system: Optional[str] = None, **kw) -> dict:
        msgs = []
        if system or self.system:
            msgs.append({"role": "system", "content": system or self.system})
        msgs.append({"role": "user", "content": prompt})
        r = self._request(msgs, **kw)
        r.raise_for_status()
        d = r.json()
        m = d["choices"][0]["message"]
        return {"content": m.get("content", ""), "reasoning": m.get("reasoning_content", ""),
                "usage": d.get("usage", {})}

    def stream(self, prompt: str, system: Optional[str] = None, **kw) -> Iterator[dict]:
        msgs = []
        if system or self.system:
            msgs.append({"role": "system", "content": system or self.system})
        msgs.append({"role": "user", "content": prompt})
        resp = self._request(msgs, stream=True, **kw)
        resp.raise_for_status()
        for line in resp.iter_lines():
            if not line: continue
            line = line.decode("utf-8")
            if not line.startswith("data: "): continue
            ds = line[6:]
            if ds.strip() == "[DONE]": break
            try:
                c = json.loads(ds)
                if not c.get("choices"): continue
                d = c["choices"][0].get("delta", {})
                if d.get("reasoning_content"):
                    yield {"type": "reasoning", "text": d["reasoning_content"]}
                if d.get("content"):
                    yield {"type": "content", "text": d["content"]}
            except: pass

    def say(self, prompt: str, **kw) -> dict:
        self.history.append({"role": "user", "content": prompt})
        msgs = list(self.history)
        if self.system and (not msgs or msgs[0]["role"] != "system"):
            msgs = [{"role": "system", "content": self.system}] + msgs
        r = self._request(msgs, **kw)
        r.raise_for_status()
        d = r.json()
        m = d["choices"][0]["message"]
        self.history.append({"role": "assistant", "content": m.get("content", "")})
        return {"content": m.get("content", ""), "reasoning": m.get("reasoning_content", ""),
                "usage": d.get("usage", {})}

    def clear(self):
        self.history = []


# ═══════════════════════════════════════════════════════════════
#  便捷函数 (模块级)
# ═══════════════════════════════════════════════════════════════
_router: Optional[AutoRouter] = None

def _get_router() -> AutoRouter:
    global _router
    if _router is None:
        _router = AutoRouter()
    return _router


def chat(prompt: str, system: Optional[str] = None, scene: Optional[str] = None, **kw) -> str:
    """一行调用, 返回纯文本 (智能路由 + 自动降级)"""
    return _get_router().chat(prompt, system=system, scene=scene, **kw)["content"]


def stream(prompt: str, system: Optional[str] = None, scene: Optional[str] = None, **kw) -> Iterator[str]:
    """流式调用, yield 纯文本 (自动过滤推理过程)"""
    for chunk in _get_router().stream(prompt, system=system, scene=scene, **kw):
        if chunk["type"] == "content":
            yield chunk["text"]


def pick(scene: str, **kw) -> str:
    """根据场景智能调用, 返回纯文本"""
    router = _get_router()
    router.set_scene(scene)
    return router.chat(kw.get("prompt", ""), **kw)["content"]


def models(tag: Optional[str] = None) -> dict:
    """列出模型, 可选按 tag 筛选"""
    tag_map = {
        "flagship": ["ultra", "ultra253b"],
        "reasoning": list(REASONING_MODELS),
        "code": ["codestral", "granite-code", "starcoder", "codellama", "deepseek-coder"],
        "edge": ["mini4b", "gemma4b", "llama32-3b", "mistral7b", "granite8b", "llama31-8b"],
        "multimodal": ["qwen397b", "qwen122b", "llama4", "minimax", "llama32-90b", "vl12b", "vl8b", "phi3-vision", "kosmos", "omni30b", "mistral119b"],
        "fast": ["deepseek-fast", "step37", "nano9b", "nano30b", "mini4b"],
        "chinese": ["qwen397b", "qwen122b", "glm", "deepseek", "kimi", "minimax", "seed"],
    }
    if tag and tag in tag_map:
        return {k: MODELS[k] for k in tag_map[tag] if k in MODELS}
    return dict(MODELS)


def search(keyword: str) -> dict:
    keyword = keyword.lower()
    return {a: m for a, m in MODELS.items() if keyword in a.lower() or keyword in m.lower()}


def status() -> dict:
    """查看当前路由器所有模型的健康状态"""
    return _get_router().status()


# ═══════════════════════════════════════════════════════════════
#  订阅 & 授权 (便捷函数)
# ═══════════════════════════════════════════════════════════════
def subscription_status() -> str:
    """显示当前会员状态"""
    try:
        from .auth import AccessControl
    except ImportError:
        from auth import AccessControl
    ac = AccessControl()
    return ac.show_status()


def subscribe(plan: str = "") -> str:
    """显示微信支付订阅界面"""
    try:
        from .payment import show_wechat_payment
    except ImportError:
        from payment import show_wechat_payment
    return show_wechat_payment(plan)


def activate(code: str) -> bool:
    """通过激活码激活VIP"""
    try:
        from .auth import AccessControl
    except ImportError:
        from auth import AccessControl
    ac = AccessControl()
    ok = ac.license.activate_by_code(code)
    if ok:
        print(f"✅ VIP激活成功! 方案: {ac.license.plan}, 剩余: {ac.license.days_remaining}天")
    else:
        print(f"❌ 激活码无效或已过期")
    return ok


def invite(invite_code: str) -> bool:
    """使用邀请码注册 (获得VIP奖励)"""
    try:
        from .auth import AccessControl
    except ImportError:
        from auth import AccessControl
    ac = AccessControl()
    ok = ac.license.activate_by_invite_code(invite_code)
    if ok:
        days = ac.license.days_remaining
        print(f"✅ 邀请成功! 获得 {days} 天 VIP 体验")
        print(f"你的邀请码: {ac.license.invite_code}")
        print(f"分享给朋友 → 双方各得30天VIP")
    else:
        print(f"❌ 邀请码无效")
    return ok


def my_invite_code() -> str:
    """获取我的邀请码"""
    try:
        from .auth import AccessControl
    except ImportError:
        from auth import AccessControl
    ac = AccessControl()
    return ac.license.invite_code

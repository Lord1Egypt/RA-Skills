#!/usr/bin/env python3
"""
F3: 隐私模式模块
- normal / strict 两种模式切换
- strict 模式下仅允许隐私友好引擎（含本地 SearXNG）
- 强制 DNT=1、无 Cookie、无 Referrer
- HTTP 头清理与隐私保护

V1.2 变更：
    1. 本模块此前未被 search.py 引用，隐私头配置实际未生效；
       现由 http_client 统一出口调用，配置真正作用于每一次请求。
    2. 引擎清单改为引用 engines_registry，不再本地硬编码
       （此前 all_engines 仅有 6 个，缺少 V1.1 新增的四个引擎，
        导致隐私报告中"被屏蔽引擎"统计不准）。
    3. 支持 User-Agent 池轮换与代理配置。
"""

import json
import os
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import yaml

sys.dont_write_bytecode = True

try:
    from engines_registry import (
        all_engine_names,
        strict_allowed_engines,
        strict_fallback_engines,
    )
except ImportError:  # 以包方式导入时
    from .engines_registry import (
        all_engine_names,
        strict_allowed_engines,
        strict_fallback_engines,
    )

# ============================================================
# 数据结构
# ============================================================

@dataclass
class PrivacyConfig:
    """
    隐私配置

    引擎清单默认值统一来自 engines_registry，避免多处硬编码不同步。
    user_agent 留空时由 UA 池随机轮换（V1.2 新增）。
    """
    mode: str = "strict"  # normal | strict
    strict_allowed_engines: List[str] = field(default_factory=strict_allowed_engines)
    strict_fallback_engines: List[str] = field(default_factory=strict_fallback_engines)
    dnt: bool = True
    no_cookie: bool = True
    no_referrer: bool = True
    user_agent: str = ""       # 空字符串表示启用 UA 池轮换
    proxy: str = ""            # http:// 或 socks5:// 代理地址，空表示直连


@dataclass
class PrivacyReport:
    """隐私保护报告"""
    mode: str
    blocked_engines: List[str]
    http_headers_cleaned: List[str]
    timestamp: datetime
    recommendations: List[str] = field(default_factory=list)


# ============================================================
# 隐私管理器
# ============================================================

class PrivacyManager:
    """隐私模式管理器"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        privacy_cfg = config.get("privacy", {})
        strict_cfg = privacy_cfg.get("strict", {})

        # 未配置时使用注册表默认值（十引擎单一真相源）
        allowed = strict_cfg.get("allowed_engines") or strict_allowed_engines()
        fallback = strict_cfg.get("fallback_engines") or strict_fallback_engines()

        # proxy 同时接受 privacy.strict.proxy 与 privacy.proxy 两种写法
        # 文档与配置模板均以 privacy.strict.proxy 为准，故优先取该位置；
        # 若只认一处，用户按文档配置后代理静默失效，会误以为 IP 已隐藏
        proxy = strict_cfg.get("proxy") or privacy_cfg.get("proxy") or ""

        # 模式键同时接受 default_mode 与 mode。
        # 只认 default_mode 时，用户误写 privacy.mode: strict 会静默落回
        # normal，自以为开启了严格模式，查询词却照常发往国内引擎——
        # 这种失败方向对隐私工具不可接受，故两种写法都识别。
        raw_mode = privacy_cfg.get("default_mode") or privacy_cfg.get("mode") or "normal"
        mode = str(raw_mode).strip().lower()
        # 配置警告留给上层展示，避免本模块直接向 stdout 输出干扰 JSON 结果
        self.config_warnings: List[str] = []
        if mode not in ("normal", "strict"):
            self.config_warnings.append(
                "隐私模式配置值 %r 无法识别，已按 normal 处理；"
                "可选值为 normal 或 strict" % raw_mode)
            mode = "normal"

        self.privacy_config = PrivacyConfig(
            mode=mode,
            strict_allowed_engines=list(allowed),
            strict_fallback_engines=list(fallback),
            dnt=strict_cfg.get("dnt", True),
            no_cookie=strict_cfg.get("no_cookie", True),
            no_referrer=strict_cfg.get("no_referrer", True),
            user_agent=strict_cfg.get("user_agent", "") or "",
            proxy=str(proxy).strip(),
        )

    def get_mode(self) -> str:
        """获取当前隐私模式"""
        return self.privacy_config.mode

    def set_mode(self, mode: str) -> bool:
        """
        切换隐私模式（带提示输出）

        Args:
            mode: "normal" 或 "strict"
        Returns:
            是否切换成功
        """
        if not self.set_mode_silent(mode):
            print(f"未知模式: {mode}，可选: normal / strict")
            return False
        print(f"已切换到 {mode} 模式")
        return True

    def set_mode_silent(self, mode: str) -> bool:
        """
        切换隐私模式（不输出提示）

        供搜索流程内部调用，避免每次搜索都打印模式信息。
        """
        if mode not in ("normal", "strict"):
            return False
        self.privacy_config.mode = mode
        return True

    def get_allowed_engines(self) -> List[str]:
        """获取当前模式允许的引擎列表"""
        if self.privacy_config.mode == "strict":
            return self.privacy_config.strict_allowed_engines
        # normal 模式返回配置中的所有默认引擎
        return self.config.get("search", {}).get("default_engines", ["baidu", "bing", "duckduckgo", "searxng"])

    def get_blocked_engines(self) -> List[str]:
        """
        获取当前模式被屏蔽的引擎列表

        引擎全集取自 engines_registry，确保新增引擎后统计自动跟随。
        """
        allowed = set(self.get_allowed_engines())
        return [e for e in all_engine_names() if e not in allowed]

    def build_headers(self, extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """
        构建隐私安全的 HTTP 请求头

        user_agent 未配置时从 UA 池随机取，降低指纹一致性。

        Args:
            extra: 额外的请求头
        Returns:
            清理后的请求头
        """
        # UA 池 = 用户追加（config.yaml） + 内置默认池
        from http_client import get_user_agent_pool, pick_user_agent
        ua_pool = get_user_agent_pool(self.config)
        headers = {
            "User-Agent": pick_user_agent(self.privacy_config.user_agent, pool=ua_pool),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
        }

        # strict 模式隐私头
        if self.privacy_config.mode == "strict":
            if self.privacy_config.dnt:
                headers["DNT"] = "1"
            if self.privacy_config.no_referrer:
                headers["Referrer-Policy"] = "no-referrer"

        # 合并额外请求头
        if extra:
            headers.update(extra)

        # strict 模式下移除敏感头
        if self.privacy_config.mode == "strict":
            headers.pop("Cookie", None)
            if self.privacy_config.no_referrer:
                headers.pop("Referer", None)

        return headers

    def build_request_context(
        self,
        timeout: int = 15,
        retry_max: int = 2,
        verbose: bool = False,
    ):
        """
        构建统一请求上下文（V1.2 新增）

        这是隐私配置真正作用于网络请求的入口：
        search.py 通过本方法取得 RequestContext 后交给 http_client，
        所有引擎共用同一份隐私策略、代理与重试配置。

        Args:
            timeout: 请求超时（秒）
            retry_max: 网络错误重试次数
            verbose: 是否输出重试过程

        Returns:
            http_client.RequestContext
        """
        try:
            from http_client import RequestContext, RetryPolicy
        except ImportError:
            from .http_client import RequestContext, RetryPolicy

        return RequestContext(
            headers=self.build_headers(),
            proxy=self.privacy_config.proxy or None,
            timeout=timeout,
            retry=RetryPolicy(max_retries=retry_max),
            verbose=verbose,
        )

    def generate_report(self) -> PrivacyReport:
        """生成隐私保护报告"""
        blocked = self.get_blocked_engines()
        headers_cleaned = ["Cookie", "Referer"] if self.privacy_config.mode == "strict" else []
        recommendations = []

        if self.privacy_config.mode == "strict":
            allowed = self.get_allowed_engines()
            recommendations = [
                f"当前为 strict 模式，可用引擎：{', '.join(allowed)}",
                "已禁用 Cookie 和 Referrer，启用 DNT",
                "SearXNG 仅绑定 127.0.0.1，不暴露到外网",
            ]
            if self.privacy_config.proxy:
                recommendations.append(f"已启用代理：{self.privacy_config.proxy}，出口 IP 由代理决定")
            else:
                recommendations.append("提示：strict 模式不隐藏 IP，可在配置中设置 proxy 或配合 VPN")
            if not self.privacy_config.user_agent:
                recommendations.append("User-Agent 已启用随机轮换，降低指纹一致性")
        else:
            recommendations = [
                "当前为 normal 模式，搜索引擎可能记录您的 IP 和搜索历史",
                "建议切换到 strict 模式以获得更佳隐私保护",
            ]

        return PrivacyReport(
            mode=self.privacy_config.mode,
            blocked_engines=blocked,
            http_headers_cleaned=headers_cleaned,
            timestamp=datetime.now(),
            recommendations=recommendations,
        )

    def check_engine_allowed(self, engine: str) -> bool:
        """检查引擎是否在当前模式下可用"""
        return engine in self.get_allowed_engines()


# ============================================================
# CLI 入口
# ============================================================

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """加载配置文件"""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def main():
    import argparse

    parser = argparse.ArgumentParser(description="隐私模式管理")
    parser.add_argument("action", choices=["mode", "status", "report"], help="操作")
    parser.add_argument("--set", choices=["normal", "strict"], help="设置模式")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")

    args = parser.parse_args()

    # 加载配置
    config = load_config(args.config)
    manager = PrivacyManager(config)

    if args.action == "mode":
        if args.set:
            success = manager.set_mode(args.set)
            if not success:
                sys.exit(1)
        else:
            mode = manager.get_mode()
            print(f"当前模式: {mode}")
            print(f"可用引擎: {', '.join(manager.get_allowed_engines())}")
            print(f"被屏蔽引擎: {', '.join(manager.get_blocked_engines())}")

    elif args.action == "status":
        if args.json:
            output = {
                "mode": manager.get_mode(),
                "allowed_engines": manager.get_allowed_engines(),
                "blocked_engines": manager.get_blocked_engines(),
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(f"模式: {manager.get_mode()}")
            print(f"可用引擎: {', '.join(manager.get_allowed_engines())}")
            print(f"被屏蔽引擎: {', '.join(manager.get_blocked_engines())}")

    elif args.action == "report":
        report = manager.generate_report()
        if args.json:
            output = {
                "mode": report.mode,
                "blocked_engines": report.blocked_engines,
                "http_headers_cleaned": report.http_headers_cleaned,
                "timestamp": report.timestamp.isoformat(),
                "recommendations": report.recommendations,
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔒 隐私保护报告 ({report.timestamp.strftime('%Y-%m-%d %H:%M:%S')})")
            print(f"   模式: {report.mode}")
            print(f"   被屏蔽引擎: {', '.join(report.blocked_engines)}")
            print(f"   清理的 HTTP 头: {', '.join(report.http_headers_cleaned)}")
            print(f"\n   建议:")
            for rec in report.recommendations:
                print(f"   • {rec}")


if __name__ == "__main__":
    import sys
    main()

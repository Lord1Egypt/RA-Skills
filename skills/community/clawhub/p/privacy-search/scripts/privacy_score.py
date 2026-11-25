#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
隐私量化报告（V2.1.0 新增）

功能：
- 隐私分数：每次搜索输出量化指标（引擎隐私评级加权分 / 代理 / 缓存 / 外发请求数 /
  cookie 残留自检），累计成「隐私档案」周报。
- strict 强化：DNS 泄露提示（系统 DNS 与隐私 DNS 不一致时警告）、cookie 零残留自证。
- 权重 YAML 可调。

设计原则（死规则）：
- 死规则 9：纯本地计算，DNS 检测用标准库读取系统 DNS 配置，无外部 API。
- 死规则 10：检测只读本地配置，开销可忽略。
- 死规则 13：不生成 __pycache__。

隐私分数构成（0-100，越高越隐私）：
    引擎评级分（0-50）：参与引擎的隐私评级加权平均 × 50
    代理加分（0-20）：配置代理 +20，否则 0
    缓存加分（0-10）：写入本地缓存 +10（查询词不出本机复用）
    外发请求扣分（-30~0）：外发请求数越多扣越多
    cookie 自检（0-10）：无 cookie 残留 +10

normal 模式典型分：引擎评级低（国内引擎）+ 无代理 + 外发多 → 约 20-40
strict 模式典型分：引擎评级高 + 代理 + 少外发 → 约 60-90
两种模式分差需 >30（验收标准）
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

sys.dont_write_bytecode = True

try:
    from engines_registry import get_engine_privacy_level
except ImportError:
    try:
        from .engines_registry import get_engine_privacy_level
    except ImportError:
        def get_engine_privacy_level(name: str) -> str:
            return "low"

# 隐私等级 → 数值
_LEVEL_SCORE = {"high": 1.0, "medium": 0.6, "low": 0.2}

_DEFAULT_WEIGHTS = {
    "engine_weight": 50.0,     # 引擎评级满分
    "proxy_bonus": 20.0,       # 代理加分
    "cache_bonus": 10.0,       # 缓存加分
    "cookie_bonus": 10.0,      # 无 cookie 残留加分
    "request_penalty": 3.0,    # 每个外发请求扣分
    "request_penalty_cap": 30.0,  # 外发扣分上限
}

_DEFAULT_PRIVACY_DNS = ["1.1.1.1", "8.8.8.8", "9.9.9.9", "223.5.5.5", "119.29.29.29"]


# ============================================================
# DNS 泄露检测
# ============================================================

def read_system_dns() -> List[str]:
    """读取系统 DNS 服务器（跨平台，纯标准库）"""
    servers: List[str] = []
    # Linux/macOS
    if os.path.exists("/etc/resolv.conf"):
        try:
            with open("/etc/resolv.conf", "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    m = re.match(r"\s*nameserver\s+(\S+)", line)
                    if m:
                        servers.append(m.group(1))
        except OSError:
            pass
    # Windows: 用 ipconfig /all 解析（只读，不修改系统）
    if os.name == "nt" and not servers:
        try:
            import subprocess
            # ipconfig 在中文 Windows 输出为 GBK，按 UTF-8 解会抛 UnicodeDecodeError。
            # 死规则：中文环境不能出现解码崩溃，显式指定 errors=ignore 兜底。
            result = subprocess.run(
                ["ipconfig", "/all"], capture_output=True, timeout=10
            )
            output = result.stdout.decode("utf-8", errors="ignore")
            if "DNS" not in output or not output.strip():
                output = result.stdout.decode("gbk", errors="ignore")
            for line in output.splitlines():
                # 中文系统显示为「DNS 服务器」，英文为「DNS Servers」，用 DNS 关键字匹配 IP
                m = re.search(r"DNS[^\n:]*?[:\s]((?:[0-9]{1,3}\.){3}[0-9]{1,3})", line, re.I)
                if m:
                    servers.append(m.group(1).strip())
        except Exception:
            pass
    return servers


def check_dns_leak(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    检测 DNS 泄露：系统 DNS 与配置的隐私 DNS 不一致时给出警告。

    strict 模式核心客群需要可验证的细节——DNS 是否走隐私 DNS 是其中一环。
    """
    cfg = (config or {}).get("privacy", {}).get("strict", {}) or {}
    privacy_dns = cfg.get("dns_servers") or _DEFAULT_PRIVACY_DNS
    system_dns = read_system_dns()

    # 判断系统 DNS 是否都属于隐私 DNS 列表
    if not system_dns:
        return {
            "leak": False,
            "system_dns": [],
            "privacy_dns": privacy_dns,
            "warning": "无法读取系统 DNS 配置（仅限提示，不影响搜索）",
            "checked": False,
        }

    non_private = [d for d in system_dns if d not in privacy_dns]
    leak = bool(non_private)
    warning = ""
    if leak:
        warning = (
            f"DNS 泄露提示：系统 DNS ({', '.join(non_private)}) 不在隐私 DNS 列表，"
            f"strict 模式下查询词经域名解析时可能被 ISP 记录。"
            f"建议将系统 DNS 改为隐私 DNS：{', '.join(privacy_dns[:3])}"
        )
    return {
        "leak": leak,
        "system_dns": system_dns,
        "privacy_dns": privacy_dns,
        "warning": warning,
        "checked": True,
    }


# ============================================================
# cookie 残留自检
# ============================================================

def check_cookie_residue(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    cookie 零残留自证：确认隐私策略配置为无 cookie，且无残留 cookie 文件。

    内存 cookie 策略（no_cookie=True）已有，此处补自检报告。
    """
    cfg = (config or {}).get("privacy", {}).get("strict", {}) or {}
    no_cookie = bool(cfg.get("no_cookie", True))
    mode = (config or {}).get("privacy", {}).get("default_mode", "normal")

    # 检查常见 cookie 残留文件（skill 输出目录内）
    residue_files: List[str] = []
    output_dir = os.path.expanduser("~/.workbuddy/output")
    cookie_patterns = ["*cookies*.txt", "*cookie*.jar", "*.pytube.cookie"]
    if os.path.isdir(output_dir):
        for pattern in cookie_patterns:
            import glob
            residue_files.extend(glob.glob(os.path.join(output_dir, pattern)))

    clean = no_cookie and not residue_files
    return {
        "clean": clean,
        "no_cookie_config": no_cookie,
        "mode": mode,
        "residue_files": residue_files,
        "evidence": (
            "cookie 零残留自证：strict 模式强制不发送 Cookie，"
            "本次自检未发现输出目录内 cookie 文件。"
            if clean else
            f"cookie 自检发现风险：配置 no_cookie={no_cookie}，"
            f"残留文件 {residue_files or '无'}"
        ),
    }


# ============================================================
# 隐私分数计算
# ============================================================

@dataclass
class PrivacyScore:
    """单次搜索的隐私分数"""
    total: int
    mode: str
    engine_score: float
    has_proxy: bool
    cache_written: bool
    outbound_requests: int
    cookie_clean: bool
    breakdown: Dict[str, float]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "mode": self.mode,
            "engine_score": round(self.engine_score, 2),
            "has_proxy": self.has_proxy,
            "cache_written": self.cache_written,
            "outbound_requests": self.outbound_requests,
            "cookie_clean": self.cookie_clean,
            "breakdown": self.breakdown,
            "timestamp": self.timestamp,
        }


def compute_privacy_score(
    engines_used: List[str],
    mode: str,
    config: Optional[Dict[str, Any]] = None,
    has_proxy: Optional[bool] = None,
    cache_written: bool = False,
    outbound_requests: Optional[int] = None,
    cookie_clean: Optional[bool] = None,
) -> PrivacyScore:
    """
    计算隐私分数（0-100）。

    Args:
        engines_used: 本次参与搜索的引擎列表
        mode: normal / strict
        config: 配置（privacy_score 权重段）
        has_proxy: 是否走代理；None 时从配置推断
        cache_written: 是否写入缓存
        outbound_requests: 外发请求数；None 时按引擎数估算
        cookie_clean: cookie 是否无残留；None 时自动检测
    """
    cfg = (config or {}).get("privacy_score", {}) or {}
    weights = dict(_DEFAULT_WEIGHTS)
    for k in weights:
        if k in cfg:
            try:
                weights[k] = float(cfg[k])
            except (TypeError, ValueError):
                pass

    # 引擎评级加权分
    if engines_used:
        level_scores = [_LEVEL_SCORE.get(get_engine_privacy_level(e), 0.2) for e in engines_used]
        engine_avg = sum(level_scores) / len(level_scores)
    else:
        engine_avg = 0.2
    engine_score = engine_avg * weights["engine_weight"]

    # 代理
    if has_proxy is None:
        strict_cfg = (config or {}).get("privacy", {}).get("strict", {}) or {}
        has_proxy = bool(strict_cfg.get("proxy") or (config or {}).get("privacy", {}).get("proxy"))
    proxy_bonus = weights["proxy_bonus"] if has_proxy else 0.0

    # 缓存
    cache_bonus = weights["cache_bonus"] if cache_written else 0.0

    # 外发请求扣分
    if outbound_requests is None:
        outbound_requests = len(engines_used) * 2  # 估算：每引擎约 2 次外发（搜索+资源）
    request_penalty = min(
        outbound_requests * weights["request_penalty"],
        weights["request_penalty_cap"],
    )

    # cookie 自检
    if cookie_clean is None:
        cookie_clean = check_cookie_residue(config)["clean"]
    cookie_bonus = weights["cookie_bonus"] if cookie_clean else 0.0

    total = int(max(0, min(100, round(
        engine_score + proxy_bonus + cache_bonus - request_penalty + cookie_bonus
    ))))

    breakdown = {
        "engine_score": round(engine_score, 2),
        "proxy_bonus": proxy_bonus,
        "cache_bonus": cache_bonus,
        "request_penalty": -round(request_penalty, 2),
        "cookie_bonus": cookie_bonus,
    }

    return PrivacyScore(
        total=total,
        mode=mode,
        engine_score=engine_score,
        has_proxy=has_proxy,
        cache_written=cache_written,
        outbound_requests=outbound_requests,
        cookie_clean=cookie_clean,
        breakdown=breakdown,
    )


# ============================================================
# 隐私档案周报
# ============================================================

_PROFILE_PATH = os.path.expanduser("~/.workbuddy/output/privacy-search-profile.jsonl")


def record_score(score: PrivacyScore, path: Optional[str] = None) -> bool:
    """记录一次隐私分数到档案（JSONL 追加）"""
    path = path or _PROFILE_PATH
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(score.to_dict(), ensure_ascii=False) + "\n")
        return True
    except OSError:
        return False


def weekly_report(path: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    生成隐私档案周报：过去 7 天的分数统计。
    """
    path = path or _PROFILE_PATH
    entries: List[Dict[str, Any]] = []
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            entries.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue
        except OSError:
            pass

    cutoff = datetime.now() - timedelta(days=7)
    week_entries = []
    for e in entries:
        try:
            ts = datetime.fromisoformat(e.get("timestamp", ""))
            if ts >= cutoff:
                week_entries.append(e)
        except (ValueError, TypeError):
            continue

    if not week_entries:
        return {
            "period": "过去 7 天",
            "total_searches": 0,
            "message": "暂无本周隐私档案数据，进行一次搜索后开始记录。",
        }

    scores = [e.get("total", 0) for e in week_entries]
    strict_scores = [e.get("total", 0) for e in week_entries if e.get("mode") == "strict"]
    normal_scores = [e.get("total", 0) for e in week_entries if e.get("mode") == "normal"]

    return {
        "period": "过去 7 天",
        "total_searches": len(week_entries),
        "avg_score": round(sum(scores) / len(scores), 1),
        "max_score": max(scores),
        "min_score": min(scores),
        "strict_avg": round(sum(strict_scores) / len(strict_scores), 1) if strict_scores else None,
        "normal_avg": round(sum(normal_scores) / len(normal_scores), 1) if normal_scores else None,
        "proxy_usage_rate": round(
            sum(1 for e in week_entries if e.get("has_proxy")) / len(week_entries) * 100, 1
        ),
        "dns_check": check_dns_leak(config),
        "cookie_check": check_cookie_residue(config),
    }


def format_score(score: PrivacyScore) -> str:
    """格式化单次隐私分数为可读文本"""
    lines = [
        f"🔒 隐私分数：{score.total}/100（{score.mode} 模式）",
        f"   引擎评级：{score.engine_score:.1f}/50",
        f"   代理：{'已启用' if score.has_proxy else '未启用'}",
        f"   缓存写入：{'是' if score.cache_written else '否'}",
        f"   外发请求：{score.outbound_requests} 次",
        f"   cookie 残留：{'无（自检通过）' if score.cookie_clean else '有风险'}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    test_cfg = {"privacy": {"strict": {"proxy": ""}}}
    s = compute_privacy_score(["baidu", "bing"], "normal", test_cfg, cache_written=True)
    print(format_score(s))
    s2 = compute_privacy_score(["searxng", "yandex", "startpage"], "strict", test_cfg, has_proxy=True, cache_written=True)
    print()
    print(format_score(s2))
    print(f"\n分差: {s2.total - s.total}（需 >30）")

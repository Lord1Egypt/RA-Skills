#!/usr/bin/env python3
"""
token_budget.py - Token预算管理工具
参考Claude Code的token预算机制实现

功能：
1. Token使用追踪（累计/本次/剩余）
2. 预算配置（总预算/警告阈值/危险阈值）
3. 预算状态报告
4. 自动触发压缩建议
5. 预算重置和续期

用法：
    python3 scripts/token_budget.py status          # 查看当前预算状态
    python3 scripts/token_budget.py record 1500     # 记录本次使用1500 tokens
    python3 scripts/token_budget.py check           # 检查是否需要警告/压缩
    python3 scripts/token_budget.py reset           # 重置本期预算
    python3 scripts/token_budget.py continue        # 续期（增加预算）
    python3 scripts/token_budget.py report          # 生成详细报告
    python3 scripts/token_budget.py --test          # 运行测试模式
"""

import json
import sys
import os
import argparse
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum


class BudgetStatus(Enum):
    """预算状态枚举"""
    NORMAL = "normal"           # 正常
    WARNING = "warning"         # 警告（>75%）
    DANGER = "danger"           # 危险（>90%）
    EXHAUSTED = "exhausted"     # 耗尽
    CONTINUED = "continued"     # 已续期


@dataclass
class BudgetConfig:
    """预算配置"""
    total_budget: int = 500_000                # 总预算
    warning_threshold: float = 0.75            # 警告阈值（75%）
    danger_threshold: float = 0.90             # 危险阈值（90%）
    auto_compact_threshold: float = 0.85       # 自动压缩阈值（85%）
    continuation_budget: int = 200_000         # 每次续期增加的预算
    max_continuations: int = 5                 # 最大续期次数

    @classmethod
    def from_file(cls, config_path: str) -> "BudgetConfig":
        """从配置文件加载"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            budget_data = data.get("budget", {})
            return cls(
                total_budget=budget_data.get("total_budget", 500_000),
                warning_threshold=budget_data.get("warning_threshold", 0.75),
                danger_threshold=budget_data.get("danger_threshold", 0.90),
                auto_compact_threshold=budget_data.get("auto_compact_threshold", 0.85),
                continuation_budget=budget_data.get("continuation_budget", 200_000),
                max_continuations=budget_data.get("max_continuations", 5),
            )
        except (FileNotFoundError, json.JSONDecodeError):
            return cls()


@dataclass
class TokenRecord:
    """单次Token使用记录"""
    tokens: int
    timestamp: str
    description: str = ""


@dataclass
class BudgetState:
    """预算状态"""
    total_budget: int = 500_000
    used_tokens: int = 0
    remaining_tokens: int = 500_000
    current_session_tokens: int = 0
    continuation_count: int = 0
    status: str = "normal"
    period_start: str = ""
    period_end: Optional[str] = None
    last_compact_suggestion: Optional[str] = None
    history: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BudgetState":
        return cls(
            total_budget=data.get("total_budget", 500_000),
            used_tokens=data.get("used_tokens", 0),
            remaining_tokens=data.get("remaining_tokens", 500_000),
            current_session_tokens=data.get("current_session_tokens", 0),
            continuation_count=data.get("continuation_count", 0),
            status=data.get("status", "normal"),
            period_start=data.get("period_start", ""),
            period_end=data.get("period_end"),
            last_compact_suggestion=data.get("last_compact_suggestion"),
            history=data.get("history", []),
        )


class TokenBudget:
    """Token预算管理器"""

    CONFIG_FILE = "token_budget_config.json"
    DEFAULT_STATE_FILE = "logs/token_budget_state.json"
    HISTORY_SIZE = 100

    def __init__(self, config_path: Optional[str] = None, state_file: Optional[str] = None):
        # 确定项目根目录
        self.root_dir = Path(__file__).resolve().parent.parent
        self.config_path = config_path or str(self.root_dir / self.CONFIG_FILE)
        self.config = BudgetConfig.from_file(self.config_path)

        # 加载或初始化状态
        self.state_file = state_file or str(self.root_dir / self.DEFAULT_STATE_FILE)
        self.state = self._load_state()

    def _load_state(self) -> BudgetState:
        """加载状态文件"""
        try:
            with open(self.state_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return BudgetState.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError):
            now = datetime.now().isoformat()
            return BudgetState(
                total_budget=self.config.total_budget,
                remaining_tokens=self.config.total_budget,
                period_start=now,
            )

    def _save_state(self):
        """保存状态文件"""
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state.to_dict(), f, indent=2, ensure_ascii=False)

    def _update_status(self):
        """更新预算状态"""
        usage_ratio = self.state.used_tokens / self.state.total_budget if self.state.total_budget > 0 else 1.0

        if usage_ratio >= 1.0:
            self.state.status = BudgetStatus.EXHAUSTED.value
        elif usage_ratio >= self.config.danger_threshold:
            self.state.status = BudgetStatus.DANGER.value
        elif usage_ratio >= self.config.warning_threshold:
            self.state.status = BudgetStatus.WARNING.value
        else:
            self.state.status = BudgetStatus.NORMAL.value

        self.state.remaining_tokens = max(0, self.state.total_budget - self.state.used_tokens)

    # ── 核心 API ──────────────────────────────────────────────

    def record(self, tokens: int, description: str = "") -> Dict[str, Any]:
        """记录token使用"""
        self.state.used_tokens += tokens
        self.state.current_session_tokens += tokens

        record = TokenRecord(
            tokens=tokens,
            timestamp=datetime.now().isoformat(),
            description=description,
        )
        self.state.history.append(asdict(record))
        # 保持历史记录大小
        if len(self.state.history) > self.HISTORY_SIZE:
            self.state.history = self.state.history[-self.HISTORY_SIZE:]

        self._update_status()
        self._save_state()

        return self._build_result(f"已记录 {tokens} tokens")

    def status(self) -> Dict[str, Any]:
        """获取当前预算状态"""
        self._update_status()
        usage_ratio = self.state.used_tokens / self.state.total_budget if self.state.total_budget > 0 else 0
        return {
            "status": self.state.status,
            "total_budget": self.state.total_budget,
            "used_tokens": self.state.used_tokens,
            "remaining_tokens": self.state.remaining_tokens,
            "current_session_tokens": self.state.current_session_tokens,
            "usage_ratio": round(usage_ratio, 4),
            "usage_percent": f"{usage_ratio * 100:.1f}%",
            "continuation_count": self.state.continuation_count,
            "max_continuations": self.config.max_continuations,
            "period_start": self.state.period_start,
        }

    def check(self) -> Dict[str, Any]:
        """检查是否需要警告或压缩"""
        self._update_status()
        usage_ratio = self.state.used_tokens / self.state.total_budget if self.state.total_budget > 0 else 1.0

        result: Dict[str, Any] = {
            "status": self.state.status,
            "usage_ratio": round(usage_ratio, 4),
            "actions": [],
        }

        # 自动压缩建议
        if usage_ratio >= self.config.auto_compact_threshold:
            now = datetime.now().isoformat()
            result["actions"].append({
                "type": "auto_compact",
                "message": f"⚡ Token使用率 {usage_ratio*100:.1f}% 已超过自动压缩阈值 {self.config.auto_compact_threshold*100:.0f}%，建议立即压缩上下文",
                "priority": "high",
            })
            self.state.last_compact_suggestion = now

        # 危险警告
        if usage_ratio >= self.config.danger_threshold:
            result["actions"].append({
                "type": "danger",
                "message": f"🚨 Token使用率 {usage_ratio*100:.1f}% 已超过危险阈值 {self.config.danger_threshold*100:.0f}%，剩余 {self.state.remaining_tokens} tokens",
                "priority": "critical",
            })

        # 警告
        elif usage_ratio >= self.config.warning_threshold:
            result["actions"].append({
                "type": "warning",
                "message": f"⚠️ Token使用率 {usage_ratio*100:.1f}% 已超过警告阈值 {self.config.warning_threshold*100:.0f}%，剩余 {self.state.remaining_tokens} tokens",
                "priority": "medium",
            })

        # 预算耗尽
        if self.state.remaining_tokens <= 0:
            if self.state.continuation_count < self.config.max_continuations:
                result["actions"].append({
                    "type": "budget_exhausted",
                    "message": f"🔴 Token预算已耗尽！已续期 {self.state.continuation_count}/{self.config.max_continuations} 次，可继续续期",
                    "priority": "critical",
                    "can_continue": True,
                })
            else:
                result["actions"].append({
                    "type": "budget_exhausted",
                    "message": f"🔴 Token预算已耗尽！已达最大续期次数 {self.config.max_continuations}",
                    "priority": "critical",
                    "can_continue": False,
                })

        self._save_state()
        return result

    def reset(self) -> Dict[str, Any]:
        """重置预算"""
        now = datetime.now().isoformat()
        self.state = BudgetState(
            total_budget=self.config.total_budget,
            remaining_tokens=self.config.total_budget,
            period_start=now,
        )
        self._save_state()
        return self._build_result("预算已重置")

    def continue_budget(self) -> Dict[str, Any]:
        """续期预算（参考 incrementBudgetContinuationCount）"""
        if self.state.continuation_count >= self.config.max_continuations:
            return {
                "success": False,
                "message": f"已达最大续期次数 {self.config.max_continuations}",
                "continuation_count": self.state.continuation_count,
            }

        self.state.continuation_count += 1
        self.state.total_budget += self.config.continuation_budget
        self.state.remaining_tokens += self.config.continuation_budget
        self.state.status = BudgetStatus.CONTINUED.value
        self._save_state()

        return self._build_result(
            f"已续期 #{self.state.continuation_count}，增加 {self.config.continuation_budget} tokens"
        )

    def report(self) -> Dict[str, Any]:
        """生成详细报告"""
        status = self.status()
        check = self.check()

        # 计算使用趋势
        recent_history = self.state.history[-20:] if self.state.history else []
        total_recent = sum(r["tokens"] for r in recent_history)
        avg_per_record = total_recent / len(recent_history) if recent_history else 0

        return {
            **status,
            "check": check,
            "trend": {
                "recent_records": len(recent_history),
                "recent_total_tokens": total_recent,
                "avg_tokens_per_record": round(avg_per_record, 1),
                "estimated_records_remaining": (
                    int(self.state.remaining_tokens / avg_per_record)
                    if avg_per_record > 0 else "N/A"
                ),
            },
            "config": {
                "warning_threshold": f"{self.config.warning_threshold*100:.0f}%",
                "danger_threshold": f"{self.config.danger_threshold*100:.0f}%",
                "auto_compact_threshold": f"{self.config.auto_compact_threshold*100:.0f}%",
                "continuation_budget": self.config.continuation_budget,
                "max_continuations": self.config.max_continuations,
            },
            "recommendations": self._get_recommendations(check, status),
        }

    def _get_recommendations(self, check: Dict, status: Dict) -> List[str]:
        """生成推荐建议"""
        recs = []
        ratio = status["usage_ratio"]

        if ratio >= 0.95:
            recs.append("🚨 立即执行上下文压缩（microcompact/autocompact）")
            recs.append("💡 考虑使用 budget continue 续期")
        elif ratio >= 0.85:
            recs.append("⚡ 建议执行上下文压缩")
            recs.append("📝 减少不必要的工具调用")
        elif ratio >= 0.75:
            recs.append("⚠️ 关注token消耗，准备压缩")
        else:
            recs.append("✅ 预算充足，正常使用")

        if self.state.continuation_count > 0:
            recs.append(f"📊 已续期 {self.state.continuation_count} 次")

        return recs

    def _build_result(self, message: str) -> Dict[str, Any]:
        """构建返回结果"""
        return {
            "success": True,
            "message": message,
            "status": self.state.status,
            "used_tokens": self.state.used_tokens,
            "remaining_tokens": self.state.remaining_tokens,
            "total_budget": self.state.total_budget,
            "usage_percent": f"{(self.state.used_tokens/self.state.total_budget)*100:.1f}%",
        }

    # ── CLI 格式化输出 ─────────────────────────────────────────

    @staticmethod
    def format_status(data: Dict[str, Any]) -> str:
        """格式化状态输出"""
        status_emoji = {
            "normal": "🟢",
            "warning": "⚠️",
            "danger": "🚨",
            "exhausted": "🔴",
            "continued": "🔄",
        }
        emoji = status_emoji.get(data.get("status", ""), "❓")

        lines = [
            f"\n{'='*50}",
            f"  {emoji} Token 预算状态",
            f"{'='*50}",
            f"  状态:       {data.get('status', 'N/A').upper()}",
            f"  总预算:     {data.get('total_budget', 0):,} tokens",
            f"  已使用:     {data.get('used_tokens', 0):,} tokens",
            f"  剩余:       {data.get('remaining_tokens', 0):,} tokens",
            f"  使用率:     {data.get('usage_percent', '0%')}",
            f"  本次会话:   {data.get('current_session_tokens', 0):,} tokens",
            f"  续期次数:   {data.get('continuation_count', 0)}/{data.get('max_continuations', 5)}",
            f"  周期开始:   {data.get('period_start', 'N/A')[:19]}",
            f"{'='*50}",
        ]
        return "\n".join(lines)

    @staticmethod
    def format_check(data: Dict[str, Any]) -> str:
        """格式化检查结果"""
        lines = [f"\n{'='*50}", f"  🔍 Token 预算检查", f"{'='*50}"]

        actions = data.get("actions", [])
        if not actions:
            lines.append("  ✅ 一切正常，无需操作")
        else:
            for action in actions:
                lines.append(f"  {action['message']}")

        lines.append(f"{'='*50}")
        return "\n".join(lines)

    @staticmethod
    def format_report(data: Dict[str, Any]) -> str:
        """格式化详细报告"""
        status_emoji = {
            "normal": "🟢",
            "warning": "⚠️",
            "danger": "🚨",
            "exhausted": "🔴",
            "continued": "🔄",
        }
        emoji = status_emoji.get(data.get("status", ""), "❓")
        trend = data.get("trend", {})
        config = data.get("config", {})
        recs = data.get("recommendations", [])

        lines = [
            f"\n{'='*55}",
            f"  {emoji} Token 预算详细报告",
            f"{'='*55}",
            f"\n📊 预算概况",
            f"  总预算:         {data.get('total_budget', 0):,} tokens",
            f"  已使用:         {data.get('used_tokens', 0):,} tokens",
            f"  剩余:           {data.get('remaining_tokens', 0):,} tokens",
            f"  使用率:         {data.get('usage_percent', '0%')}",
            f"  本次会话使用:   {data.get('current_session_tokens', 0):,} tokens",
            f"  续期次数:       {data.get('continuation_count', 0)}/{data.get('max_continuations', 5)}",
            f"\n📈 使用趋势",
            f"  近期记录数:     {trend.get('recent_records', 0)}",
            f"  近期总消耗:     {trend.get('recent_total_tokens', 0):,} tokens",
            f"  平均每次消耗:   {trend.get('avg_tokens_per_record', 0)} tokens",
            f"  预计剩余次数:   {trend.get('estimated_records_remaining', 'N/A')}",
            f"\n⚙️ 配置参数",
            f"  警告阈值:       {config.get('warning_threshold', '75%')}",
            f"  危险阈值:       {config.get('danger_threshold', '90%')}",
            f"  自动压缩阈值:   {config.get('auto_compact_threshold', '85%')}",
            f"  续期预算:       {config.get('continuation_budget', 200000):,} tokens",
            f"  最大续期次数:   {config.get('max_continuations', 5)}",
            f"\n💡 建议",
        ]
        for rec in recs:
            lines.append(f"  {rec}")

        lines.append(f"{'='*55}")
        return "\n".join(lines)


# ── 测试套件 ──────────────────────────────────────────────────

def run_tests() -> bool:
    """运行测试"""
    import tempfile
    import shutil

    passed = 0
    failed = 0
    tests: List[tuple] = []

    def test(name: str):
        def decorator(fn):
            tests.append((name, fn))
        return decorator

    tmp_dir = tempfile.mkdtemp()

    try:
        # 准备测试配置
        test_config = {
            "budget": {
                "total_budget": 10000,
                "warning_threshold": 0.5,
                "danger_threshold": 0.8,
                "auto_compact_threshold": 0.7,
                "continuation_budget": 5000,
                "max_continuations": 3,
            }
        }
        config_path = os.path.join(tmp_dir, "config.json")
        with open(config_path, 'w') as f:
            json.dump(test_config, f)

        @test("初始状态正确")
        def test_initial_status():
            tb = TokenBudget(config_path=config_path, state_file=os.path.join(tmp_dir, "state.json"))
            s = tb.status()
            assert s["total_budget"] == 10000, f"Expected 10000, got {s['total_budget']}"
            assert s["used_tokens"] == 0
            assert s["remaining_tokens"] == 10000
            assert s["status"] == "normal"

        @test("记录token使用")
        def test_record():
            tb = TokenBudget(config_path=config_path, state_file=os.path.join(tmp_dir, "state2.json"))
            result = tb.record(3000, "test record")
            assert result["success"]
            assert result["used_tokens"] == 3000
            assert result["remaining_tokens"] == 7000

        @test("警告阈值触发")
        def test_warning_threshold():
            tb = TokenBudget(config_path=config_path, state_file=os.path.join(tmp_dir, "state3.json"))
            tb.record(6000, "test")  # 60% > 50% warning
            check = tb.check()
            assert check["status"] == "warning"
            assert any(a["type"] == "warning" for a in check["actions"])

        @test("危险阈值触发")
        def test_danger_threshold():
            tb = TokenBudget(config_path=config_path, state_file=os.path.join(tmp_dir, "state4.json"))
            tb.record(8500, "test")  # 85% > 80% danger
            check = tb.check()
            assert check["status"] == "danger"

        @test("自动压缩建议触发")
        def test_auto_compact():
            tb = TokenBudget(config_path=config_path, state_file=os.path.join(tmp_dir, "state5.json"))
            tb.record(7500, "test")  # 75% > 70% compact threshold
            check = tb.check()
            assert any(a["type"] == "auto_compact" for a in check["actions"])

        @test("预算耗尽")
        def test_exhausted():
            tb = TokenBudget(config_path=config_path, state_file=os.path.join(tmp_dir, "state6.json"))
            tb.record(10000, "test")
            check = tb.check()
            assert check["status"] == "exhausted"
            assert any(a["type"] == "budget_exhausted" for a in check["actions"])

        @test("预算续期")
        def test_continue():
            tb = TokenBudget(config_path=config_path, state_file=os.path.join(tmp_dir, "state7.json"))
            tb.record(10000, "test")
            result = tb.continue_budget()
            assert result["success"]
            assert result["remaining_tokens"] == 5000
            assert result["total_budget"] == 15000

        @test("续期上限")
        def test_max_continuations():
            tb = TokenBudget(config_path=config_path, state_file=os.path.join(tmp_dir, "state8.json"))
            tb.record(10000, "test")
            for _ in range(3):
                tb.continue_budget()
            result = tb.continue_budget()
            assert not result["success"]
            assert "最大续期" in result["message"]

        @test("预算重置")
        def test_reset():
            tb = TokenBudget(config_path=config_path, state_file=os.path.join(tmp_dir, "state9.json"))
            tb.record(8000, "test")
            result = tb.reset()
            assert result["success"]
            assert result["used_tokens"] == 0
            assert result["remaining_tokens"] == 10000

        @test("详细报告")
        def test_report():
            tb = TokenBudget(config_path=config_path, state_file=os.path.join(tmp_dir, "state10.json"))
            tb.record(3000, "test1")
            tb.record(2000, "test2")
            report = tb.report()
            assert "trend" in report
            assert "config" in report
            assert "recommendations" in report
            assert report["trend"]["recent_total_tokens"] == 5000

        @test("历史记录限制")
        def test_history_limit():
            tb = TokenBudget(config_path=config_path, state_file=os.path.join(tmp_dir, "state11.json"))
            # 写入超过限制的记录
            for i in range(150):
                tb.record(10, f"record {i}")
            assert len(tb.state.history) == tb.HISTORY_SIZE

        @test("状态持久化")
        def test_persistence():
            state_path = os.path.join(tmp_dir, "state12.json")
            tb1 = TokenBudget(config_path=config_path, state_file=state_path)
            tb1.record(4000, "save test")

            # 重新加载
            tb2 = TokenBudget(config_path=config_path, state_file=state_path)
            assert tb2.state.used_tokens == 4000
            assert tb2.state.remaining_tokens == 6000

        # 执行所有测试
        print(f"\n🧪 运行 {len(tests)} 个测试...\n")
        for name, fn in tests:
            try:
                fn()
                print(f"  ✅ {name}")
                passed += 1
            except Exception as e:
                print(f"  ❌ {name}: {e}")
                failed += 1

        print(f"\n{'='*40}")
        print(f"  通过: {passed}  失败: {failed}  总计: {len(tests)}")
        print(f"{'='*40}\n")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    return failed == 0


# ── CLI 入口 ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Token预算管理工具 - 参考Claude Code token budget机制",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 scripts/token_budget.py status          # 查看当前状态
  python3 scripts/token_budget.py record 1500     # 记录1500 tokens
  python3 scripts/token_budget.py record 500 -d "工具调用"  # 带描述
  python3 scripts/token_budget.py check           # 检查是否需要警告
  python3 scripts/token_budget.py reset           # 重置预算
  python3 scripts/token_budget.py continue        # 续期预算
  python3 scripts/token_budget.py report          # 详细报告
  python3 scripts/token_budget.py --test          # 运行测试
        """,
    )

    parser.add_argument(
        "command",
        nargs="?",
        choices=["status", "record", "check", "reset", "continue", "report"],
        default="status",
        help="操作命令",
    )
    parser.add_argument(
        "tokens",
        nargs="?",
        type=int,
        help="记录的token数量（record命令需要）",
    )
    parser.add_argument(
        "-d", "--description",
        default="",
        help="使用描述（record命令可选）",
    )
    parser.add_argument(
        "--config",
        help="指定配置文件路径",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以JSON格式输出",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="运行测试模式",
    )

    args = parser.parse_args()

    # 测试模式
    if args.test:
        success = run_tests()
        sys.exit(0 if success else 1)

    # 正常命令模式
    tb = TokenBudget(config_path=args.config)

    if args.command == "status":
        result = tb.status()
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(TokenBudget.format_status(result))

    elif args.command == "record":
        if args.tokens is None:
            print("❌ 错误: record 命令需要指定 token 数量")
            print("用法: python3 scripts/token_budget.py record <tokens> [-d 描述]")
            sys.exit(1)
        result = tb.record(args.tokens, args.description)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"✅ {result['message']}")
            print(f"   已用: {result['used_tokens']:,} | 剩余: {result['remaining_tokens']:,} | 使用率: {result['usage_percent']}")

    elif args.command == "check":
        result = tb.check()
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(TokenBudget.format_check(result))

    elif args.command == "reset":
        result = tb.reset()
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"✅ {result['message']}")
            print(f"   预算: {result['total_budget']:,} tokens | 已用: {result['used_tokens']:,}")

    elif args.command == "continue":
        result = tb.continue_budget()
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if result["success"]:
                print(f"✅ {result['message']}")
                print(f"   总预算: {result['total_budget']:,} | 剩余: {result['remaining_tokens']:,}")
            else:
                print(f"❌ {result['message']}")

    elif args.command == "report":
        result = tb.report()
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(TokenBudget.format_report(result))


if __name__ == "__main__":
    main()

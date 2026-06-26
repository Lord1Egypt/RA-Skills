#!/usr/bin/env python3
"""Imperial Orchestrator · 全自动编排器

完整闭环: 路由 → 执行 → 审核 → 反馈 → 输出
一条命令，全部自动化。

用法:
  # 基础执行
  python3 scripts/orchestrator.py --task "用 Go 写一个令牌桶限流器"

  # 指定最大预算
  python3 scripts/orchestrator.py --task "..." --max-cost 0.05

  # 带审核的严格模式
  python3 scripts/orchestrator.py --task "..." --strict

  # 多轮对话（带 session）
  python3 scripts/orchestrator.py --task "..." --session my-project

  # 查看成本统计
  python3 scripts/orchestrator.py --stats

  # 查看最近操作审计日志
  python3 scripts/orchestrator.py --audit-tail 10
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from lib import (
    AuditLog,
    Registry,
    calculate_cost,
    count_healthy_models,
    estimate_tokens,
    load_json,
    now_ts,
    read_openclaw_config,
    refresh_group_summaries,
    save_json,
)


# ── Session 管理 ──────────────────────────────────────────────────────

class Session:
    """多轮对话的会话管理。"""

    def __init__(self, session_dir: Path, session_id: str):
        self.session_dir = session_dir
        self.session_id = session_id
        self.session_file = session_dir / f"{session_id}.json"
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        if self.session_file.exists():
            self._data = load_json(self.session_file)
        else:
            self._data = {
                "session_id": self.session_id,
                "created_at": now_ts(),
                "messages": [],
                "total_cost_usd": 0,
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "turns": 0,
            }

    def save(self) -> None:
        self.session_dir.mkdir(parents=True, exist_ok=True)
        save_json(self.session_file, self._data)

    @property
    def messages(self) -> List[Dict[str, str]]:
        return self._data.get("messages", [])

    def add_turn(
        self,
        user_msg: str,
        assistant_msg: str,
        model: str,
        cost: float,
        input_tokens: int,
        output_tokens: int,
    ) -> None:
        self._data["messages"].append({"role": "user", "content": user_msg})
        self._data["messages"].append({"role": "assistant", "content": assistant_msg})
        self._data["total_cost_usd"] = round(self._data.get("total_cost_usd", 0) + cost, 6)
        self._data["total_input_tokens"] = self._data.get("total_input_tokens", 0) + input_tokens
        self._data["total_output_tokens"] = self._data.get("total_output_tokens", 0) + output_tokens
        self._data["turns"] = self._data.get("turns", 0) + 1
        self._data["last_model"] = model
        self._data["last_active"] = now_ts()

    def context_window_tokens(self) -> int:
        """估算当前会话占用的 token 数。"""
        return sum(estimate_tokens(m.get("content", "")) for m in self.messages)

    def trim_to_budget(self, max_tokens: int = 16000) -> None:
        """裁剪早期消息，保持 token 预算内。保留 system prompt 和最近的消息。"""
        msgs = self._data["messages"]
        if not msgs:
            return
        while self.context_window_tokens() > max_tokens and len(msgs) > 4:
            # 保留第一条（可能是 system）和最后几条
            if msgs[0].get("role") == "system":
                msgs.pop(1)  # 删除第二条
            else:
                msgs.pop(0)  # 删除第一条

    @property
    def stats(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "turns": self._data.get("turns", 0),
            "total_cost_usd": self._data.get("total_cost_usd", 0),
            "total_input_tokens": self._data.get("total_input_tokens", 0),
            "total_output_tokens": self._data.get("total_output_tokens", 0),
            "context_tokens": self.context_window_tokens(),
        }


# ── 编排主逻辑 ────────────────────────────────────────────────────────

def run_pipeline(
    task: str,
    reg: Registry,
    cfg: Dict[str, Any],
    state: Dict[str, Any],
    audit: AuditLog,
    session: Optional[Session] = None,
    max_cost: float = 1.0,
    max_tokens: int = 4096,
    timeout: int = 120,
    strict: bool = False,
    no_review: bool = False,
    benchmark_file: Optional[Path] = None,
) -> Dict[str, Any]:
    """完整的编排流水线。"""
    from router import (
        candidate_models_for_role,
        choose_with_cross_provider,
        determine_role,
        load_benchmark_scores,
        maybe_degrade,
        survival_model,
    )
    from executor import execute_with_fallback, run_review

    providers_cfg = cfg.get("models", {}).get("providers", {})
    bench_scores = load_benchmark_scores(benchmark_file) if benchmark_file else {}
    pipeline_start = time.monotonic()

    # ── Step 1: 路由 ─────────────────────────────────────────────────
    lead_role, review_roles, mode = determine_role(reg, task)
    degraded = maybe_degrade(reg, state)

    if degraded:
        mode = "degraded"
        review_roles = []
        lead_role = "emergency-scribe" if candidate_models_for_role(reg, state, "emergency-scribe", bench_scores) else "router-chief"

    if no_review:
        review_roles = []

    lead_candidates = candidate_models_for_role(reg, state, lead_role, bench_scores)
    selected_model, fallback_chain = choose_with_cross_provider(lead_candidates)

    if not selected_model:
        role_cfg = reg.roles_cfg.get("roles", {}).get(lead_role, {})
        for fallback_role in role_cfg.get("fallback_roles", []):
            cands = candidate_models_for_role(reg, state, fallback_role, bench_scores)
            selected_model, fallback_chain = choose_with_cross_provider(cands)
            if selected_model:
                lead_role = fallback_role
                break

    survive = survival_model(state)
    if not selected_model and survive:
        selected_model = survive
        lead_role = "emergency-scribe"
        mode = "degraded"

    if not selected_model:
        return {"success": False, "error": "No models available", "phase": "routing"}

    # ── Step 2: 预算检查 ──────────────────────────────────────────────
    input_est = estimate_tokens(task) + (session.context_window_tokens() if session else 0)
    system_prompt = reg.get_system_prompt(lead_role) or ""
    input_est += estimate_tokens(system_prompt)
    estimated_cost = calculate_cost(selected_model, input_est, max_tokens)

    if estimated_cost > max_cost:
        return {
            "success": False,
            "error": f"Estimated cost ${estimated_cost:.4f} exceeds budget ${max_cost:.4f}",
            "phase": "budget_check",
            "estimated_cost": estimated_cost,
        }

    audit.log(
        "orchestrate_start",
        task=task[:200],
        lead_role=lead_role,
        mode=mode,
        selected_model=selected_model,
        estimated_cost=round(estimated_cost, 6),
    )

    # ── Step 3: 构建消息 ──────────────────────────────────────────────
    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    # 注入会话上下文
    if session:
        session.trim_to_budget(max_tokens=16000)
        for msg in session.messages:
            if msg.get("role") != "system":
                messages.append(msg)

    messages.append({"role": "user", "content": task})

    # ── Step 4: 执行 ─────────────────────────────────────────────────
    model_chain: List[str] = [selected_model] + fallback_chain
    if survive and survive not in model_chain:
        model_chain.append(survive)

    exec_result = execute_with_fallback(
        model_chain, messages, providers_cfg, state, audit,
        max_tokens=max_tokens, timeout=timeout,
    )

    if not exec_result["success"]:
        audit.log("orchestrate_fail", error=exec_result.get("error", ""), phase="execution")
        return {
            "success": False,
            "error": exec_result.get("error", "execution failed"),
            "errors": exec_result.get("errors", []),
            "phase": "execution",
        }

    # ── Step 5: 审核 ─────────────────────────────────────────────────
    review_result = None
    if review_roles and not no_review:
        review_prompts = {}
        for r in review_roles:
            rp = reg.get_system_prompt(r)
            if rp:
                review_prompts[r] = rp

        if review_prompts:
            review_result = run_review(
                exec_result["content"], task, review_roles, review_prompts,
                state, providers_cfg, reg, audit,
            )

            # strict 模式下 reject → 自动重试一次（换模型）
            if strict and review_result.get("verdict") == "reject" and len(model_chain) > 1:
                audit.log("strict_retry", reason="review rejected, trying next model")
                retry_chain = model_chain[1:]  # 跳过第一个模型
                exec_result = execute_with_fallback(
                    retry_chain, messages, providers_cfg, state, audit,
                    max_tokens=max_tokens, timeout=timeout,
                )
                if exec_result["success"]:
                    review_result = run_review(
                        exec_result["content"], task, review_roles, review_prompts,
                        state, providers_cfg, reg, audit,
                    )

    # ── Step 6: 汇总 ─────────────────────────────────────────────────
    pipeline_ms = (time.monotonic() - pipeline_start) * 1000

    total_cost = exec_result.get("cost_usd", 0)
    total_input = exec_result.get("input_tokens", 0)
    total_output = exec_result.get("output_tokens", 0)

    if review_result:
        for rv in review_result.get("reviews", {}).values():
            total_cost += rv.get("cost_usd", 0)
            total_input += rv.get("input_tokens", 0)
            total_output += rv.get("output_tokens", 0)

    # 更新 session
    if session and exec_result["success"]:
        session.add_turn(
            task, exec_result["content"],
            exec_result.get("model_used", "?"),
            total_cost, total_input, total_output,
        )
        session.save()

    role_meta = reg.get_role_metadata(lead_role)

    output = {
        "success": True,
        "content": exec_result.get("content", ""),
        "routing": {
            "lead_role": lead_role,
            "lead_title": role_meta.get("title", lead_role),
            "mode": mode,
            "degraded": degraded,
        },
        "execution": {
            "model_used": exec_result.get("model_used"),
            "attempt": exec_result.get("attempt", 1),
            "fallback_used": exec_result.get("fallback_used", False),
            "latency_ms": exec_result.get("latency_ms", 0),
        },
        "review": {
            "verdict": review_result.get("verdict") if review_result else "skip",
            "details": review_result,
        } if review_result or review_roles else None,
        "tokens": {
            "input": total_input,
            "output": total_output,
            "total": total_input + total_output,
        },
        "cost": {
            "execution_usd": exec_result.get("cost_usd", 0),
            "review_usd": round(total_cost - exec_result.get("cost_usd", 0), 6),
            "total_usd": round(total_cost, 6),
        },
        "pipeline_ms": round(pipeline_ms, 1),
    }

    if session:
        output["session"] = session.stats

    audit.log(
        "orchestrate_complete",
        model=exec_result.get("model_used"),
        role=lead_role,
        mode=mode,
        total_cost_usd=round(total_cost, 6),
        total_tokens=total_input + total_output,
        review_verdict=review_result.get("verdict") if review_result else None,
        pipeline_ms=round(pipeline_ms, 1),
    )

    return output


# ── CLI ───────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Imperial Orchestrator 全自动编排: 路由→执行→审核→反馈",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--task", type=str, help="任务文本")
    p.add_argument("--openclaw-config", type=Path, default=None)
    p.add_argument("--state-file", type=Path, default=Path(".imperial_state.json"))
    p.add_argument("--benchmark-file", type=Path, default=Path(".imperial_benchmark.json"))
    p.add_argument("--audit-file", type=Path, default=Path(".imperial_audit.json"))
    p.add_argument("--session", type=str, default=None, help="会话 ID（多轮对话）")
    p.add_argument("--session-dir", type=Path, default=Path(".imperial_sessions"))
    p.add_argument("--max-cost", type=float, default=1.0, help="单次预算上限(USD)")
    p.add_argument("--max-tokens", type=int, default=4096)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--strict", action="store_true", help="审核不通过自动重试")
    p.add_argument("--no-review", action="store_true", help="跳过审核")
    p.add_argument("--json", action="store_true", help="JSON 格式输出")
    p.add_argument("--stats", action="store_true", help="显示累计统计")
    p.add_argument("--audit-tail", type=int, default=None, help="显示最近 N 条审计日志")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    reg = Registry(root)
    audit = AuditLog(args.audit_file)

    # 统计模式
    if args.stats:
        stats = audit.stats()
        print(f"\n{'🏯 Imperial Orchestrator 累计统计':^50}")
        print(f"{'═' * 50}")
        print(f"  总调用次数:   {stats['total_entries']}")
        print(f"  总成本:       ${stats['total_cost_usd']:.4f}")
        print(f"  总 token:     {stats['total_input_tokens']} 入 / {stats['total_output_tokens']} 出")
        print(f"\n  事件统计:")
        for ev, cnt in sorted(stats.get("by_event", {}).items()):
            print(f"    {ev:30s} {cnt:>5d}")
        print(f"\n  模型使用:")
        for model, cnt in sorted(stats.get("model_usage", {}).items(), key=lambda x: -x[1]):
            print(f"    {model:40s} {cnt:>5d}")
        print()
        return 0

    # 审计日志
    if args.audit_tail is not None:
        entries = audit.recent(args.audit_tail)
        for e in entries:
            ts = time.strftime("%m-%d %H:%M:%S", time.localtime(e.get("ts", 0)))
            event = e.get("event", "?")
            model = e.get("model", "")
            cost = e.get("cost_usd") or e.get("total_cost_usd") or 0
            extra = ""
            if cost:
                extra += f" ${cost:.4f}"
            if e.get("error"):
                extra += f" ERR: {e['error'][:60]}"
            if e.get("verdict"):
                extra += f" verdict={e['verdict']}"
            print(f"  [{ts}] {event:25s} {model:30s}{extra}")
        return 0

    if not args.task:
        print("❌ 需要 --task 参数", file=sys.stderr)
        return 1

    # 加载配置
    cfg = read_openclaw_config(args.openclaw_config)
    if not cfg:
        print("❌ 找不到 openclaw.json", file=sys.stderr)
        return 1

    from lib import build_initial_state
    if args.state_file.exists():
        state = load_json(args.state_file)
    else:
        state = build_initial_state(reg, cfg)
    refresh_group_summaries(state)

    # Session
    session = None
    if args.session:
        session = Session(args.session_dir, args.session)

    # 执行完整流水线
    result = run_pipeline(
        task=args.task,
        reg=reg,
        cfg=cfg,
        state=state,
        audit=audit,
        session=session,
        max_cost=args.max_cost,
        max_tokens=args.max_tokens,
        timeout=args.timeout,
        strict=args.strict,
        no_review=args.no_review,
        benchmark_file=args.benchmark_file if args.benchmark_file.exists() else None,
    )

    # 持久化
    save_json(args.state_file, state)
    audit.flush()

    # 输出
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result["success"]:
            print(result["content"])
            print(f"\n{'─' * 60}", file=sys.stderr)
            routing = result.get("routing", {})
            execution = result.get("execution", {})
            tokens = result.get("tokens", {})
            cost = result.get("cost", {})

            role_line = f"{routing.get('lead_title', '?')}({routing.get('lead_role', '?')})"
            model_line = execution.get("model_used", "?")
            token_line = f"{tokens.get('input', 0)}→{tokens.get('output', 0)} ({tokens.get('total', 0)} total)"
            cost_line = f"${cost.get('total_usd', 0):.4f}"
            latency_line = f"{execution.get('latency_ms', 0):.0f}ms"
            pipeline_line = f"{result.get('pipeline_ms', 0):.0f}ms"

            print(f"🏯 {role_line} → {model_line}", file=sys.stderr)
            print(f"📊 tokens: {token_line} | cost: {cost_line}", file=sys.stderr)
            print(f"⏱️  model: {latency_line} | pipeline: {pipeline_line}", file=sys.stderr)

            if execution.get("fallback_used"):
                print(f"⚠️  使用了 fallback (第 {execution.get('attempt', '?')} 个模型)", file=sys.stderr)

            review = result.get("review")
            if review and review.get("verdict") != "skip":
                v = review["verdict"]
                icon = {"pass": "✅", "revise": "⚠️", "reject": "❌"}.get(v, "❓")
                print(f"🔍 审核: {icon} {v}", file=sys.stderr)

            if session:
                sess = result.get("session", {})
                print(f"💬 会话: {sess.get('session_id', '?')} | 轮次: {sess.get('turns', 0)} | 累计: ${sess.get('total_cost_usd', 0):.4f}", file=sys.stderr)
        else:
            phase = result.get("phase", "unknown")
            error = result.get("error", "unknown")
            print(f"❌ [{phase}] {error}", file=sys.stderr)
            if result.get("errors"):
                for e in result["errors"]:
                    print(f"   • {e.get('model', '?')}: {e.get('error', '?')}", file=sys.stderr)

    return 0 if result.get("success") else 1


if __name__ == "__main__":
    raise SystemExit(main())

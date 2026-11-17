#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端到端编排（M8）——一轮对话的完整流水线

这是 v2 唯一需要 Agent 记住的入口。在线只做三件事：
1. prepare()   回复**之前**：把各离线模块的产出压缩拼进上下文（≤500 Token）
2. after_reply() 回复**之后**：一致性自检 + AI 腔守门 + 把新素材丢进离线队列
3. proactive() 空闲时：判断该不该主动开口 / 发图

铁律：
- 任何模块抛异常都不得中断对话——离线模块出问题，最多是这一轮少一点料
- 总 Token 预算是硬约束，由 injector 兜底，本模块不绕过
- 模块开关尊重用户设置（panel.controls）
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 允许 `python scripts/pipeline/orchestrator.py` 直接跑（此时 sys.path[0] 是脚本所在目录）
_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.core import settings as core_settings  # noqa: E402
from scripts.pipeline.injector import Injector  # noqa: E402

DEFAULT_DATA_DIR = "~/.love-companion/data"
ENV_DATA_DIR = "LOVE_COMPANION_DATA_DIR"


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


class Session:
    """一轮对话的编排"""

    def __init__(self, slug: str = "", data_dir: Optional[str] = None):
        self.data_dir = str(core_settings.resolve_data_dir(data_dir))
        self.slug = slug

    # ---------- 内部小工具 ----------

    def _controls(self):
        from scripts.panel.controls import Controls
        return Controls(self.data_dir)

    def _on(self, module: str, default: bool = True) -> bool:
        try:
            return self._controls().enabled(module)
        except Exception:  # noqa: BLE001 - 设置读不出来按默认开
            return default

    # ---------- 1. 回复之前 ----------

    def prepare(self, user_message: str, conversation_id: str = "",
                include_care: bool = False) -> Dict[str, Any]:
        """构建本轮注入上下文

        Returns:
            {
              "sections": {...},     # 实际注入的各段
              "render":   str,       # 可直接拼进 System Prompt 的文本
              "tokens":   {...},     # 各段估算 Token
              "total_tokens": int,
              "budget": int,
              "truncated": [...], "dropped": [...],
              "evidence": {...},     # 可解释面板依据
              "memory_ids": [...],   # 被召回的记忆 id（用于 mark）
            }
        """
        # 预算真读 settings.json：用户在「控制与安全感」里调过的额度会生效
        caps = core_settings.budget_map(self.data_dir)

        # 合规闸门（v2.1）：《人工智能拟人化互动服务管理暂行办法》禁止向未成年人
        # 提供虚拟伴侣等虚拟亲密关系服务。未确认「已满 18 周岁」时不注入任何
        # 恋人上下文，只返回合规提示，由 Agent 先完成年龄确认。
        if not core_settings.age_confirmed(self.data_dir):
            notice = (
                "【合规提示】Love Companion 为 AI 角色扮演 / 虚拟伴侣类服务，"
                "依据《人工智能拟人化互动服务管理暂行办法》，不得向未成年人提供。"
                "请先向用户确认其已年满 18 周岁；用户确认后，在 settings.json 的"
                "「合规.已满18周岁确认」置为 true 方可启用恋人模式。"
                "本轮未注入人格、记忆等任何恋人上下文。"
            )
            return {
                "sections": {}, "render": notice, "tokens": {},
                "total_tokens": 0, "budget": int(caps["合计上限"]),
                "truncated": [], "dropped": [], "evidence": {},
                "memory_ids": [], "age_gate": True,
            }

        inj = Injector(total_budget=int(caps["合计上限"]), caps=caps)
        memory_ids: List[int] = []

        # 记忆片段（M2）：语义 + 时间 + 重要性 + 关系路径 四路打分取 Top-3
        if self._on("记忆系统"):
            try:
                from scripts.memory.retrieve import render as render_mem, top_k
                from scripts.memory.store import MemoryStore
                store = MemoryStore(self.data_dir)
                picked = top_k(store.all(), user_message or "", k=3)
                memory_ids = [int(m.get("id")) for m in picked if m.get("id") is not None]
                if picked:
                    inj.add("记忆片段", render_mem(picked))
                    store.recall(memory_ids)
            except Exception:  # noqa: BLE001
                pass

        # 人格指令（M3a）：蒸馏过素材用人格库，否则直接用当前 v1 人设
        # （含 8 套预设）——没蒸馏的用户不该拿到空的人设
        if self._on("人格克隆"):
            try:
                from scripts.persona.adapt import from_v1_file
                from scripts.persona.library import PersonaLibrary
                summary = ""
                if self.slug:
                    summary = PersonaLibrary(self.data_dir).compile_summary(self.slug)
                if not summary:
                    summary = from_v1_file(self.data_dir)
                if summary:
                    inj.add("人格指令", summary)
            except Exception:  # noqa: BLE001
                pass

        # 相处指南（M3b）：先套用户手动权重，再编译
        if self._on("用户理解"):
            try:
                from scripts.user.guide import compile_guide
                from scripts.user.profile import UserProfileStore
                controls = self._controls()
                persona = controls.apply_weights(UserProfileStore(self.data_dir).get())
                guide = compile_guide(persona, budget=int(caps["相处指南"]))
                if guide:
                    inj.add("相处指南", guide)
            except Exception:  # noqa: BLE001
                pass

        # 趋势调味料（M7a）：默认关闭，开了才注入
        if self._on("趋势感知", default=False):
            try:
                from scripts.trends.store import TrendStore
                seasoning = TrendStore(self.data_dir).seasoning()
                if seasoning:
                    inj.add("趋势调味料", seasoning)
            except Exception:  # noqa: BLE001
                pass

        # 关怀话术（M6）：只有触发了才占这个位置
        if include_care and self._on("主动关怀"):
            care = self.proactive().get("care") or {}
            if care.get("text"):
                inj.add("关怀话术", care["text"])

        built = inj.build()

        # 可解释面板（M7c）：记录依据，只存引用不存原文
        evidence: Dict[str, List[str]] = {}
        if self._on("可解释面板"):
            try:
                from scripts.panel.explain import ExplainPanel, build_evidence
                evidence = build_evidence(built["sections"], self.data_dir, self.slug)
                ExplainPanel(self.data_dir).record(built["sections"], evidence, slug=self.slug)
            except Exception:  # noqa: BLE001
                pass

        return {
            "sections": built["sections"],
            "render": inj.render(),
            "tokens": built["tokens"],
            "total_tokens": built["total_tokens"],
            "budget": built["budget"],
            "truncated": built["truncated"],
            "dropped": built["dropped"],
            "evidence": evidence,
            "memory_ids": memory_ids,
        }

    # ---------- 2. 回复之后 ----------

    def after_reply(self, reply: str, user_message: str = "",
                    conversation_id: str = "", mood: Optional[str] = None,
                    max_tasks: int = 8) -> Dict[str, Any]:
        """回复后处理：自检 + 入队 + 跑离线任务

        Returns:
            {"consistency": {"ok": bool, "issues": [...]},
             "humanizer": {...}, "events": [...], "idle": {...}}
        """
        report: Dict[str, Any] = {"consistency": {}, "humanizer": {}, "events": [], "idle": {}}

        # 跨角色一致性（M5）：回复跑偏出人设，记下来供下次纠偏
        if self.slug:
            try:
                from scripts.persona.mirror import MirrorModel
                ok, issues = MirrorModel(self.data_dir).consistency(reply or "", self.slug)
                report["consistency"] = {"ok": ok, "issues": issues}
            except Exception:  # noqa: BLE001
                report["consistency"] = {"ok": True, "issues": []}

        # AI 腔守门（M4）：离线跑，不占主生成 Token
        if self._on("语气后处理"):
            try:
                from scripts.style.humanizer import scan
                report["humanizer"] = scan(reply or "")
            except Exception:  # noqa: BLE001
                pass

        # 用户信号与记忆采集：丢进离线队列，不让它在对话里占时间
        # （隐私.采集开关在 runner 的 memory.extract 里把关）
        try:
            from scripts.pipeline.queue import TaskQueue
            queue = TaskQueue(self.data_dir)
            if user_message:
                queue.enqueue("memory.extract",
                              {"text": user_message, "conversation_id": conversation_id or self.slug})
            if mood and self.slug:
                queue.enqueue("mirror.record", {"slug": self.slug, "kind": mood})
            report["events"] = [user_message and "memory.extract", mood and "mirror.record"]
            report["events"] = [e for e in report["events"] if e]
        except Exception:  # noqa: BLE001
            pass

        # 对话间隙：排空离线队列
        try:
            from scripts.pipeline.runner import run_idle
            report["idle"] = run_idle(self.data_dir, max_tasks=max_tasks)
        except Exception as exc:  # noqa: BLE001
            report["idle"] = {"error": f"{type(exc).__name__}: {exc}"}

        return report

    # ---------- 3. 空闲时 ----------

    def proactive(self, now: Optional[datetime] = None) -> Dict[str, Any]:
        """主动关怀 + 主动发图判定（是否真能发出去取决于通道能力）"""
        out: Dict[str, Any] = {"care": None, "image": None}

        if self._on("主动关怀"):
            try:
                from scripts.care.templates import compose
                from scripts.care.trigger import CareTrigger
                trigger = CareTrigger(self.data_dir)
                verdict = trigger.evaluate(now)
                if verdict.get("should"):
                    text = compose(verdict["kind"], self.slug, self.data_dir)
                    if not text.get("text"):
                        out["care"] = {"should": False,
                                       "reason": f"无可用话术（kind={verdict['kind']}）"}
                    else:
                        trigger.mark_sent(verdict["kind"], now)
                        out["care"] = {"kind": verdict["kind"], "reason": verdict.get("reason", ""),
                                       "hint": verdict.get("next_hint", ""), "text": text["text"],
                                       "tokens": text["tokens"]}
                else:
                    out["care"] = {"should": False, "reason": verdict.get("reason", ""),
                                   "next_eligible": trigger.next_eligible(now)}
            except Exception as exc:  # noqa: BLE001
                out["care"] = {"error": f"{type(exc).__name__}: {exc}"}

        if self._on("多模态", default=False):
            try:
                from scripts.multimodal.image_plan import ImagePlanner
                out["image"] = ImagePlanner(self.data_dir).plan(
                    self.slug, mood="日常", now=now, data_dir=self.data_dir)
            except Exception as exc:  # noqa: BLE001
                out["image"] = {"error": f"{type(exc).__name__}: {exc}"}

        return out

    # ---------- 便捷：一句话状态 ----------

    def status(self) -> Dict[str, Any]:
        """给「你现在是怎么理解我的」这类问题用"""
        status: Dict[str, Any] = {"slug": self.slug}
        try:
            status["settings"] = self._controls().status()
        except Exception:  # noqa: BLE001
            pass
        try:
            from scripts.memory.store import MemoryStore
            status["memory"] = MemoryStore(self.data_dir).stats()
        except Exception:  # noqa: BLE001
            pass
        if self.slug:
            try:
                from scripts.persona.mirror import MirrorModel
                status["relation"] = MirrorModel(self.data_dir).face(self.slug)
            except Exception:  # noqa: BLE001
                pass
        return status


def run_round(slug: str, user_message: str, reply: str,
              data_dir: Optional[str] = None, conversation_id: str = "") -> Dict[str, Any]:
    """一轮完整流程（给 CLI 与测试用）"""
    session = Session(slug, data_dir)
    before = session.prepare(user_message, conversation_id)
    after = session.after_reply(reply, user_message, conversation_id)
    return {"prepare": before, "after": after}


if __name__ == "__main__":
    import argparse
    import json

    ap = argparse.ArgumentParser(description="Love Companion v2 端到端编排")
    ap.add_argument("--slug", default="", help="伴侣人格 slug")
    ap.add_argument("--data-dir", default=os.environ.get(ENV_DATA_DIR, DEFAULT_DATA_DIR))
    ap.add_argument("--msg", default="", help="用户这句话")
    ap.add_argument("--reply", default="", help="待自检的回复")
    ap.add_argument("--status", action="store_true", help="输出当前状态")
    args = ap.parse_args()

    s = Session(args.slug, args.data_dir)
    if args.status:
        print(json.dumps(s.status(), ensure_ascii=False, indent=2))
    elif args.msg:
        out = s.prepare(args.msg)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(s.proactive(), ensure_ascii=False, indent=2))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对话间隙调度器（M1）——方案确认的触发方式：**对话间隙自动跑**

用法（由 Agent 在每轮回复后调用，或由系统任务定时调用）：
    python scripts/pipeline/runner.py --data-dir ~/.love-companion/data
    python scripts/pipeline/runner.py --max-tasks 5

设计约束：
- 单次调用有上限（默认 8 个任务），绝不让离线工作拖慢对话
- 每个任务可重试，超过次数进死信，不阻塞后续任务
- 只依赖标准库

新模块接入：
    from scripts.pipeline.runner import register

    @register("memory.extract")
    def handle(payload, ctx):
        ...        # ctx 提供 data_dir、queue 等
        return {...}   # 返回值写入 task["result"]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.pipeline.queue import TaskQueue  # noqa: E402

# kind -> handler(payload, ctx) -> result
HANDLERS: Dict[str, Callable[[Dict[str, Any], Dict[str, Any]], Any]] = {}


def register(kind: str) -> Callable:
    """注册任务处理器"""
    def deco(fn: Callable) -> Callable:
        HANDLERS[kind] = fn
        return fn
    return deco


def run_idle(data_dir: Optional[str] = None, max_tasks: int = 8) -> Dict[str, Any]:
    """排空待执行任务（对话间隙调用）

    Returns:
        {"picked": n, "done": n, "failed": n, "skipped": n, "errors": [...]}
    """
    queue = TaskQueue(data_dir)
    ctx = {"data_dir": str(queue.data_dir), "queue": queue}
    report: Dict[str, Any] = {"picked": 0, "done": 0, "failed": 0, "skipped": 0, "errors": []}

    for task in queue.pending(limit=max_tasks):
        kind = task.get("kind")
        if kind not in HANDLERS:
            report["skipped"] += 1
            queue.fail(task["id"], f"未注册的任务类型：{kind}")
            continue
        claimed = queue.claim(task["id"])
        if not claimed:
            continue
        report["picked"] += 1
        try:
            result = HANDLERS[kind](claimed.get("payload") or {}, ctx)
            queue.complete(claimed["id"], result)
            report["done"] += 1
        except Exception as exc:  # noqa: BLE001 - 离线任务失败不得影响对话
            queue.fail(claimed["id"], f"{type(exc).__name__}: {exc}")
            report["failed"] += 1
            report["errors"].append(f"{kind}: {exc}")

    return report


# ==================== 内置任务 ====================

@register("memory.extract")
def _task_memory_extract(payload: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    """从一段对话文本中无感采集记忆（离线，不占对话 Token）"""
    from scripts.core import settings as core_settings
    from scripts.memory.store import MemoryStore
    from scripts.memory.extract import extract_memories

    # 隐私.采集开关：用户关了就一条不采（数据主权）
    if not core_settings.collection_enabled(ctx["data_dir"]):
        return {"added": 0, "reason": "采集开关已关闭"}

    text = payload.get("text", "")
    if not text:
        return {"added": 0, "reason": "空文本"}
    store = MemoryStore(ctx["data_dir"])
    candidates = extract_memories(text, conversation_id=payload.get("conversation_id", ""))
    added = []
    for c in candidates:
        entry = store.add(
            content=c["content"],
            memory_type=c["type"],
            source=c.get("source", ""),
            importance=c.get("importance", 0.5),
            valence=c.get("valence", 0.0),
            conversation_id=payload.get("conversation_id", ""),
        )
        added.append(entry["id"])
    return {"added": len(added), "ids": added}


@register("memory.decay")
def _task_memory_decay(payload: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    """长期记忆重要性衰减（每日一次即可）"""
    from scripts.memory.store import MemoryStore
    store = MemoryStore(ctx["data_dir"])
    changed = store.decay()
    return {"decayed": changed}


@register("persona.build")
def _task_persona_build(payload: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    """从素材文件构建 / 增量合并伴侣人格（离线，重活不占对话）"""
    from scripts.persona import parser, extract, library

    name = payload.get("name") or payload.get("speaker") or "对方"
    nickname = payload.get("nickname") or name
    corpus: List[Dict[str, Any]] = []
    prints: List[str] = []

    files = payload.get("files") or []
    if files:
        corpus, prints = parser.parse_many(files, default_speaker=name)
    for item in payload.get("corpus") or []:
        corpus.append({
            "speaker": item.get("speaker", name),
            "text": item.get("text", ""),
            "ts": item.get("ts", ""),
            "redacted": [],
        })

    if payload.get("speaker"):
        corpus = parser.only(corpus, payload["speaker"])
    if not corpus:
        return {"ok": False, "reason": "无有效语料"}

    persona = extract.extract_persona(corpus, name=name, nickname=nickname, source_prints=prints)
    lib = library.PersonaLibrary(ctx["data_dir"])
    slug = payload.get("slug") or library.slugify(nickname)
    if lib.exists(slug):
        lib.merge(slug, persona)
        action = "merged"
    else:
        lib.create(persona, slug)
        action = "created"
    return {"ok": True, "action": action, "slug": slug, "语料量": len(corpus),
            "版本": (lib.get(slug) or {}).get("版本")}


@register("persona.correct")
def _task_persona_correct(payload: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    """对话纠偏：写入即生效（离线落盘，下次编译摘要自动带上）"""
    from scripts.persona.library import PersonaLibrary
    lib = PersonaLibrary(ctx["data_dir"])
    lib.correct(payload["slug"], payload["wrong"], payload.get("right", ""))
    return {"ok": True, "corrections": len(lib.corrections(payload["slug"]))}


@register("mirror.record")
def _task_mirror_record(payload: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    """记录一次关系事件（亲密/冲突/里程碑/和解），驱动关系演化建模"""
    from scripts.persona.mirror import MirrorModel
    m = MirrorModel(ctx["data_dir"])
    m.record(payload["slug"], payload.get("kind", "日常"),
             payload.get("note", ""), payload.get("delta"))
    return {"ok": True, "stage": m.stage(payload["slug"]),
            "亲密度": m.intimacy(payload["slug"])}


@register("care.evaluate")
def _task_care_evaluate(payload: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    """判定是否该主动关怀，若该则一并生成话术（话术也走离线，不占主生成）"""
    from scripts.care.templates import compose
    from scripts.care.trigger import CareTrigger

    t = CareTrigger(ctx["data_dir"], config=payload.get("config"))
    # payload.now 便于手动触发与测试；不传就用真实时刻（静默时段照常生效）
    now = None
    if payload.get("now"):
        try:
            now = datetime.fromisoformat(payload["now"])
        except (TypeError, ValueError):
            now = None
    verdict = t.evaluate(now)
    if not verdict.get("should"):
        return {"should": False, "reason": verdict.get("reason", "")}

    slug = payload.get("slug", "")
    out = compose(verdict["kind"], slug, ctx["data_dir"], detail=payload.get("detail", ""))
    if not out.get("text"):
        # 未知类型等原因产不出话术：不发送、不消耗冷却额度
        return {"should": False, "reason": f"无可用话术（kind={verdict['kind']}）"}
    t.mark_sent(verdict["kind"], now)
    return {"should": True, "kind": verdict["kind"], "reason": verdict.get("reason", ""),
            "hint": verdict.get("next_hint", ""), "text": out["text"], "tokens": out["tokens"]}


@register("trends.plan")
def _task_trends_plan(payload: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    """产出抓取计划（primary + fallback 链）；payload.failed 用于上报上一个源挂了"""
    from scripts.trends.sources import SourceRouter
    router = SourceRouter(ctx["data_dir"])
    if payload.get("failed"):
        router.mark(payload["failed"], False)
    return router.plan(payload.get("topic", ""), payload.get("keyword"))


@register("trends.ingest")
def _task_trends_ingest(payload: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    """把抓回来的原文离线提炼成要点入库（原文不进上下文）"""
    from scripts.trends.sources import SourceRouter
    from scripts.trends.store import TrendStore

    source = payload.get("source", "")
    result = TrendStore(ctx["data_dir"]).ingest(
        payload.get("raw", ""), payload.get("topic", ""), source)
    # 抓到了算成功，一条都提炼不出来算这个源挂了（影响下次排程）
    if source:
        SourceRouter(ctx["data_dir"]).mark(source, bool(result.get("added")))
    return result


@register("image.plan")
def _task_image_plan(payload: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    """产出配图计划（时机 + 风格 + 衔接话术），不实际生成图片"""
    from scripts.multimodal.image_plan import ImagePlanner
    planner = ImagePlanner(ctx["data_dir"], config=payload.get("config"))
    out = planner.plan(payload.get("slug", ""), mood=payload.get("mood", "日常"),
                       data_dir=ctx["data_dir"])
    if out.get("should") and not payload.get("dry_run"):
        planner.mark_sent(payload.get("mood", "日常"), out.get("caption", ""))
    else:
        planner.tick(False)
    return out


@register("panel.explain")
def _task_panel_explain(payload: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
    """记录本轮注入了什么、依据是什么（只存引用关系，不存原文）"""
    from scripts.panel.explain import ExplainPanel
    panel = ExplainPanel(ctx["data_dir"])
    entry = panel.record(payload.get("sections") or {}, slug=payload.get("slug", ""))
    return {"ok": True, "sections": sorted(entry["sections"]), "evidence": entry["evidence"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="对话间隙离线任务调度")
    parser.add_argument("--data-dir", default=os.environ.get("LOVE_COMPANION_DATA_DIR", "~/.love-companion/data"))
    parser.add_argument("--max-tasks", type=int, default=8)
    parser.add_argument("--enqueue", nargs=2, metavar=("KIND", "PAYLOAD_JSON"),
                        help="入队一个任务，例：--enqueue memory.extract '{\"text\":\"我喜欢三分糖\"}'")
    args = parser.parse_args()

    if args.enqueue:
        kind, payload_raw = args.enqueue
        try:
            payload = json.loads(payload_raw)
        except json.JSONDecodeError as exc:
            print(f"payload 不是合法 JSON：{exc}")
            return 1
        task_id = TaskQueue(args.data_dir).enqueue(kind, payload)
        print(json.dumps({"enqueued": task_id}, ensure_ascii=False))
        return 0

    report = run_idle(args.data_dir, max_tasks=args.max_tasks)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

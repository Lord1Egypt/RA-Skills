#!/usr/bin/env python3
"""
infoseek_report.py — 采集结果报告生成器 + 治理反馈

从 infoseek_pipeline.py 的输出生成人类可读报告，
并将失败记录反馈到治理系统。

用法:
  python3 infoseek_report.py --input outputs/infoseek_report_20260726.json
  python3 infoseek_report.py --failure-log  # 查看失败模式库
"""

import json, os, sys
from datetime import datetime
from typing import Optional


# ═══════════════════════════════════════════════════════════════
# 报告生成
# ═══════════════════════════════════════════════════════════════

def generate_markdown_report(pipeline_result: dict) -> str:
    """从管道输出生成 Markdown 报告"""
    stats = pipeline_result.get("stats", {})
    details = pipeline_result.get("details", [])
    
    lines = []
    lines.append(f"# infoseek 采集报告")
    lines.append(f"**管道版本:** 1.0.0 | **执行时间:** {pipeline_result.get('timestamp','?')}")
    lines.append(f"")
    lines.append(f"## 执行总览")
    lines.append(f"")
    
    # 统计摘要
    total = stats.get("total", 0)
    success = stats.get("success", 0)
    partial = stats.get("partial", 0)
    search = stats.get("needs_search", 0)
    dead = stats.get("dead_link", 0)
    skipped = stats.get("skipped", 0)
    failed = stats.get("failed", 0)
    
    lines.append(f"| 指标 | 数值 |")
    lines.append(f"|------|:----:|")
    lines.append(f"| 总锚点数 | **{total}** |")
    lines.append(f"| ✅ 采集成功 | **{success}** |")
    lines.append(f"| ⚠️ 部分成功(需降级) | **{partial}** |")
    lines.append(f"| 🔍 需搜索(名称类) | **{search}** |")
    lines.append(f"| 💀 死链 | **{dead}** |")
    lines.append(f"| ⏭️ 跳过(score<40) | **{skipped}** |")
    lines.append(f"| ❌ 失败 | **{failed}** |")
    lines.append(f"| 总耗时 | **{stats.get('total_elapsed_s','?')}s** |")
    lines.append(f"")

    # 成功率
    effective = total - skipped - failed
    if effective > 0:
        rate = (success / effective) * 100
        lines.append(f"**有效成功率:** {rate:.1f}%")
        lines.append(f"")

    lines.append(f"## 锚点详情")
    lines.append(f"")
    
    for i, r in enumerate(details):
        anchor = r.get("anchor", {})
        status = r.get("status", "?")
        elapsed = r.get("elapsed_s", 0)
        
        # 状态 emoji
        emoji = {"success": "✅", "partial": "⚠️", "needs_tier2": "🔽", 
                 "needs_search": "🔍", "dead_link": "💀", "skipped": "⏭️", "failed": "❌"}
        
        name = anchor.get("name", "?")
        platform = anchor.get("platform", "?")
        entry = anchor.get("entry", "?")
        
        lines.append(f"### {i+1}. {emoji.get(status, '❓')} {name}")
        lines.append(f"- **平台:** {platform} | **入口:** {entry} | **耗时:** {elapsed}s")
        lines.append(f"- **状态:** {status}")
        
        steps = r.get("steps", [])
        for s in steps:
            step_name = s.get("step", "")
            step_status = s.get("status", "")
            reason = s.get("reason", "")
            if step_status == "fail":
                lines.append(f"  - ❌ {step_name}: {reason}")
            elif step_status == "skip":
                lines.append(f"  - ⏭️ {step_name}: {reason}")
            elif step_name == "tier2_needed":
                lines.append(f"  - 🔽 需 Tier 2 降级: {reason}")
            elif step_name == "search_needed":
                lines.append(f"  - 🔍 需搜索: {s.get('entry','')} @ {s.get('platform','')}")
        
        output = r.get("output")
        if output:
            lines.append(f"  - 📄 标题: {output.get('title','?')}")
            lines.append(f"  - 📏 正文长度: {output.get('text_length',0)}字")
        
        lines.append(f"")
    
    lines.append(f"---")
    lines.append(f"*报告由 infoseek 自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 治理反馈: 失败记录 → 锚点降级建议
# ═══════════════════════════════════════════════════════════════

def generate_feedback(details: list) -> list:
    """治理反馈生成（v1.7.6 G2-1 单源收敛）。

    唯一真源 = infoseek_pipeline.generate_feedback；本函数委托之，
    消除历史口径漂移（failed 此前 pipeline=−10 而本模块=−20）。
    导入失败 → 内置同口径回退（不阻断报告 CLI）。
    """
    try:
        _here = os.path.dirname(os.path.abspath(__file__))
        if _here not in sys.path:
            sys.path.insert(0, _here)
        from infoseek_pipeline import generate_feedback as _gf
        return _gf(details)
    except Exception:
        feedbacks = []
        for r in details:
            status = r.get("status")
            if status in ("dead_link", "failed", "needs_tier2"):
                anchor = r.get("anchor", {})
                penalty = -20 if status == "dead_link" else -10
                feedbacks.append({
                    "feedback_type": "failure",
                    "anchor_name": anchor.get("name", "?"),
                    "anchor_platform": anchor.get("platform", "?"),
                    "anchor_entry": anchor.get("entry", "?"),
                    "original_score": anchor.get("score", 0),
                    "failure_type": status,
                    "failure_reason": (r.get("steps", [{}])[-1].get("reason", "")) if r.get("steps") else "",
                    "suggested_penalty": penalty,
                    "suggested_new_score": max(0, (anchor.get("score", 0) or 0) + penalty),
                })
        return feedbacks


# ═══════════════════════════════════════════════════════════════
# 统一调度器: 并发控制
# ═══════════════════════════════════════════════════════════════

class Dispatcher:
    """统一调度器 — 控制并发上限"""
    
    def __init__(self, max_playwright=1, max_api=3, max_video=1, max_total=6):
        self.limits = {
            "playwright": max_playwright,
            "api": max_api,
            "video": max_video,
            "total": max_total
        }
        self.running = {"playwright": 0, "api": 0, "video": 0, "total": 0}
    
    def can_dispatch(self, task_type: str) -> bool:
        """检查是否能下发新任务"""
        if self.running["total"] >= self.limits["total"]:
            return False
        specific_limit = self.limits.get(task_type, self.limits["total"])
        if self.running.get(task_type, 0) >= specific_limit:
            return False
        return True
    
    def dispatch(self, task_type: str):
        """下发任务"""
        self.running[task_type] = self.running.get(task_type, 0) + 1
        self.running["total"] += 1
    
    def complete(self, task_type: str):
        """完成任务"""
        self.running[task_type] = max(0, self.running.get(task_type, 0) - 1)
        self.running["total"] = max(0, self.running["total"] - 1)
    
    def status(self) -> dict:
        return {
            "limits": self.limits,
            "running": self.running,
            "available": {
                "playwright": self.limits["playwright"] - self.running["playwright"],
                "api": self.limits["api"] - self.running["api"],
                "video": self.limits["video"] - self.running["video"],
                "total": self.limits["total"] - self.running["total"]
            }
        }


# ═══════════════════════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="infoseek 报告生成器")
    parser.add_argument("--input", help="pipeline 输出 JSON 路径")
    parser.add_argument("--failure-log", action="store_true", help="仅输出失败治理反馈")
    args = parser.parse_args()
    
    if args.failure_log:
        print("# infoseek 治理反馈（演示）")
        demo_details = [
            {"status": "dead_link", "anchor": {"name":"死链测试","platform":"web","entry":"https://example.com/nonexistent","score":80}},
            {"status": "needs_tier2", "anchor": {"name":"SPA页面","platform":"web","entry":"https://www.toutiao.com/","score":85},
             "steps": [{"step":"tier2_needed","reason":"JS渲染/SPA页面"}]}
        ]
        feedbacks = generate_feedback(demo_details)
        print(json.dumps(feedbacks, ensure_ascii=False, indent=2))
    
    if args.input:
        with open(args.input) as f:
            data = json.load(f)
        report = generate_markdown_report(data)
        out_path = args.input.replace(".json", ".md")
        with open(out_path, "w") as f:
            f.write(report)
        print(f"报告已生成: {out_path}")
        
        # 同时输出治理反馈
        feedbacks = generate_feedback(data.get("details", []))
        if feedbacks:
            fb_path = args.input.replace(".json", "_feedback.json")
            with open(fb_path, "w") as f:
                json.dump(feedbacks, f, ensure_ascii=False, indent=2)
            print(f"治理反馈已保存: {fb_path}")

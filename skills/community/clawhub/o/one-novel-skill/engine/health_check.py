#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
health_check.py — 技能自检/健康报告

融合源: SkillOpt (技能性能自检) + superpowers (技能增强)
功能: 运行前检查所有依赖文件/配置/引擎状态，输出健康报告
"""

import json, importlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class HealthCheck:
    """技能健康检查器"""

    REQUIRED_DIRS = ["设定", "大纲", "规格", "正文", "追踪", "评审"]
    REQUIRED_ENGINE_MODULES = [
        "engine.novel_state", "engine.scheduler", "engine.generator",
        "engine.orchestrator", "engine.spec_builder", "engine.l2_modules",
        "engine.foreshadow_engine", "engine.timeline_builder",
        "engine.constitution_context", "engine.multi_view_review",
        "engine.user_preferences", "engine.task_decomposer",
        "engine.diagram_generator",
    ]
    REQUIRED_REFERENCES = [
        "references/de-ai/detection_config.yaml",
        "references/de-ai/ai-text-signals.md",
        "references/de-ai/baselines.json",
        "references/batch-writing/workflow-daily.md",
        "references/batch-writing/workflow-revision.md",
        "references/writing-techniques-allinone/emotion-first-methodology.md",
        "references/writing-techniques-allinone/mental-models-for-characters.md",
    ]

    def __init__(self, skill_dir: Optional[str] = None):
        self.skill_dir = Path(skill_dir) if skill_dir else Path(__file__).parent.parent
        self.results: Dict[str, dict] = {}

    def check_all(self) -> Dict[str, dict]:
        """运行全部检查"""
        self.results["directories"] = self.check_directories()
        self.results["engine_modules"] = self.check_engine_modules()
        self.results["references"] = self.check_references()
        self.results["providers"] = self.check_providers()
        self.results["templates"] = self.check_templates()
        return self.results

    def check_directories(self) -> dict:
        """检查项目目录结构"""
        ok, missing = 0, []
        for d in self.REQUIRED_DIRS:
            if (self.skill_dir / d).exists():
                ok += 1
            else:
                missing.append(d)
        return {"status": "green" if not missing else "yellow", "ok": ok, "missing": missing}

    def check_engine_modules(self) -> dict:
        """检查引擎模块可导入"""
        ok, failed = 0, []
        for mod_name in self.REQUIRED_ENGINE_MODULES:
            try:
                importlib.import_module(mod_name)
                ok += 1
            except ImportError:
                failed.append(mod_name)
        return {"status": "green" if not failed else "red", "ok": ok, "failed": failed}

    def check_references(self) -> dict:
        """检查参考文献文件是否存在"""
        ok, missing = 0, []
        for ref in self.REQUIRED_REFERENCES:
            if (self.skill_dir / ref).exists():
                ok += 1
            else:
                missing.append(ref)
        return {"status": "green" if not missing else "yellow", "ok": ok, "missing": missing}

    def check_providers(self) -> dict:
        """检查 LLM provider 可用性"""
        result = {"available": [], "unavailable": [], "status": "yellow"}
        # 检测 Ollama
        try:
            import urllib.request
            req = urllib.request.Request("http://127.0.0.1:11434/api/tags", method="GET")
            urllib.request.urlopen(req, timeout=2)
            result["available"].append("ollama")
        except Exception:
            result["unavailable"].append("ollama")
        # 检测 Gateway
        import os as _os
        if _os.environ.get("OPENCLAW_GATEWAY_TOKEN") or _os.environ.get("OPENCLAW_GATEWAY_URL"):
            result["available"].append("gateway")
        else:
            result["unavailable"].append("gateway (无token)")
        if result["available"]:
            result["status"] = "green"
        return result

    def check_templates(self) -> dict:
        """检查模板文件"""
        ok, missing = 0, []
        for t in ["chapter-spec.yaml", "chapter-template.txt", "character-card.md", "review-report.md"]:
            if (self.skill_dir / "templates" / t).exists():
                ok += 1
            else:
                missing.append(t)
        return {"status": "green" if not missing else "yellow", "ok": ok, "missing": missing}

    def summary(self) -> str:
        """输出健康摘要"""
        lines = [f"=== one-novel-skill 健康报告 ===", f"时间: {datetime.now().isoformat()[:19]}", ""]
        for name, data in self.results.items():
            status = data.get("status", "unknown")
            icon = {"green": "✅", "yellow": "🟡", "red": "🔴"}.get(status, "⚪")
            lines.append(f"{icon} {name}: {data.get('ok', 0)}/{data.get('ok', 0)+len(data.get('missing',[]) or data.get('failed',[])) or '-'}")
            for key in ["missing", "failed", "unavailable"]:
                if data.get(key):
                    lines.append(f"   ! {key}: {data[key]}")
        lines.append("")
        all_green = all(d.get("status") == "green" for d in self.results.values())
        lines.append(f"整体: {'✅ 正常' if all_green else '🟡 有警告'}")
        return "\n".join(lines)

#!/usr/bin/env python3
"""Run local release validation for One Person Company OS v1.0."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from common import (
    artifact_dir_path,
    reading_entry_path,
    reading_export_path,
    role_brief_path,
    root_doc_path,
    state_path,
    workspace_dir_path,
    workspace_file_path,
)


ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
RELEASE_ASSETS_DIR = ROOT / "release" / "assets"


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=True,
    )


def assert_exists(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"expected file not found: {path}")


def assert_not_exists(path: Path) -> None:
    if path.exists():
        raise AssertionError(f"unexpected path exists: {path}")


def assert_contains(text: str, *snippets: str) -> None:
    for snippet in snippets:
        if snippet not in text:
            raise AssertionError(f"expected snippet not found: {snippet}")


def assert_not_contains(text: str, *snippets: str) -> None:
    for snippet in snippets:
        if snippet in text:
            raise AssertionError(f"unexpected legacy snippet found: {snippet}")


def read_docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as archive:
        return archive.read("word/document.xml").decode("utf-8")


def assert_v1_state(company_dir: Path) -> dict[str, object]:
    payload = json.loads(state_path(company_dir).read_text(encoding="utf-8"))
    if payload.get("version") != "1.0":
        raise AssertionError(f"expected v1.0 state, got {payload.get('version')}")
    forbidden = {
        "stage_id",
        "stage_label",
        "current_round",
        "company_goal",
        "current_bottleneck",
        "target_user",
        "core_problem",
        "product_pitch",
    }
    leaked = sorted(forbidden.intersection(payload))
    if leaked:
        raise AssertionError(f"v1.0 state leaked old fields: {leaked}")
    for key in ("founder", "offer", "buyer", "pipeline", "product", "delivery", "cash", "learning", "assets", "risk", "decision", "visuals"):
        if key not in payload:
            raise AssertionError(f"missing v1.0 state section: {key}")
    return payload


def validate_python_compatibility_logic() -> None:
    from common import build_agent_action, is_python_version_supported
    from ensure_python_runtime import build_install_plan

    if not is_python_version_supported((3, 7, 0)):
        raise AssertionError("Python 3.7 should be supported")
    if is_python_version_supported((3, 6, 15)):
        raise AssertionError("Python 3.6 should not be supported")

    switch_action = build_agent_action(
        current_supported=False,
        compatible_runtime={"executable": "/opt/python3.11/bin/python3.11", "version": (3, 11, 9)},
        writable=True,
    )
    assert_contains(switch_action, "OpenClaw", "/opt/python3.11/bin/python3.11")

    mac_plan = build_install_plan(
        target_version="3.11",
        system_name="darwin",
        available_commands={"brew"},
    )
    if not mac_plan["supported"] or mac_plan["installer"] != "Homebrew":
        raise AssertionError("expected Homebrew install plan for macOS")


def validate_workspace_scripts() -> None:
    with tempfile.TemporaryDirectory(prefix="opc-v1-validate-") as tmp_dir:
        workspace = Path(tmp_dir)

        preflight = run(str(SCRIPTS_DIR / "preflight_check.py"), "--mode", "创建公司", "--company-dir", str(workspace / "北辰实验室"))
        assert_contains(preflight.stdout, "经营导航条:", "经营快照:", "python_supported")

        init = run(
            str(SCRIPTS_DIR / "init_business.py"),
            "北辰实验室",
            "--path",
            str(workspace),
            "--product-name",
            "北辰助手",
            "--target-user",
            "独立开发者",
            "--core-problem",
            "还没有一个真正能持续推进产品和成交的一人公司系统",
            "--product-pitch",
            "一个帮助独立开发者把产品做出来并卖出去的一人公司控制系统",
            "--confirmed",
        )
        assert_contains(init.stdout, "v1.0 经营闭环", "经营驾驶舱", "经营导航条")
        company_dir = workspace / "北辰实验室"
        assert_v1_state(company_dir)

        for legacy_dir in ("sales", "product", "delivery", "operations", "ops", "assets", "records", "roles", "flows", "automation", "artifacts", "visual-kit"):
            assert_not_exists(company_dir / legacy_dir)
        for key in (
            "dashboard",
            "founder_constraints",
            "offer",
            "pipeline",
            "product_status",
            "delivery_cash",
            "cash_health",
            "assets_automation",
            "risks",
            "week_focus",
            "today_action",
            "collaboration_memory",
            "session_handoff",
        ):
            assert_exists(root_doc_path(company_dir, key, "zh-CN"))
        assert_exists(reading_entry_path(company_dir, "zh-CN"))
        assert_exists(reading_export_path(company_dir, root_doc_path(company_dir, "dashboard", "zh-CN"), "zh-CN"))
        assert_exists(workspace_dir_path(company_dir, "visual_kit", "zh-CN") / "business-loop.svg")
        assert_exists(workspace_dir_path(company_dir, "visual_kit", "zh-CN") / "revenue-pipeline.svg")
        assert_exists(workspace_dir_path(company_dir, "visual_kit", "zh-CN") / "ai-image-prompts.md")
        assert_contains(reading_entry_path(company_dir, "zh-CN").read_text(encoding="utf-8"), "经营驾驶舱", "一人公司经营闭环", "当前成交图")
        assert_contains((workspace_dir_path(company_dir, "visual_kit", "zh-CN") / "ai-image-prompts.md").read_text(encoding="utf-8"), "AI 图片", "可选创作层")
        assert_exists(artifact_dir_path(company_dir, "delivery", "zh-CN") / "01-实际产出总表.docx")
        assert_contains(read_docx_text(artifact_dir_path(company_dir, "delivery", "zh-CN") / "01-实际产出总表.docx"), "实际产出总表")
        for generated_path in (
            workspace_file_path(company_dir, "role_index", "zh-CN"),
            role_brief_path(company_dir, "总控台", "zh-CN"),
            role_brief_path(company_dir, "创始人", "zh-CN"),
            role_brief_path(company_dir, "产品负责人", "zh-CN"),
            workspace_file_path(company_dir, "flow_bootstrap", "zh-CN"),
            workspace_file_path(company_dir, "automation_reminders", "zh-CN"),
            workspace_file_path(company_dir, "automation_scheduler", "zh-CN"),
        ):
            assert_not_contains(generated_path.read_text(encoding="utf-8"), "当前回合", "阶段切换", "当前阶段")
        assert_not_contains(read_docx_text(artifact_dir_path(company_dir, "delivery", "zh-CN") / "01-实际产出总表.docx"), "当前阶段", "当前回合", "本轮")
        if list(workspace_dir_path(company_dir, "artifacts_root", "zh-CN").rglob("*.md")):
            raise AssertionError("artifact directories should remain DOCX-only")
        for old_flow in ("推进回合流程.md", "校准回合流程.md", "阶段切换流程.md"):
            assert_not_exists(workspace_dir_path(company_dir, "flows", "zh-CN") / old_flow)

        focus_update = run(
            str(SCRIPTS_DIR / "update_focus.py"),
            str(company_dir),
            "--primary-goal",
            "把 MVP 推到可演示并拿到第一批对话",
            "--primary-bottleneck",
            "价值表达和产品演示都还不够可卖",
            "--primary-arena",
            "product",
            "--today-action",
            "先补 homepage hero 的价值表达和 CTA 路径",
            "--week-outcome",
            "拿到可演示的首版首页与注册入口",
        )
        assert_contains(focus_update.stdout, "经营快照", "更新主焦点")
        assert_v1_state(company_dir)

        doc = run(
            str(SCRIPTS_DIR / "generate_artifact_document.py"),
            str(company_dir),
            "--title",
            "首批用户访谈证据包",
            "--category",
            "business",
            "--summary",
            "记录首批用户访谈原话、证据和下一步动作。",
            "--evidence",
            "记录/推进日志",
        )
        assert_contains(doc.stdout, "生成正式交付文档", "DOCX")
        assert_exists(artifact_dir_path(company_dir, "business", "zh-CN") / "02-首批用户访谈证据包.docx")

        deprecated = run(str(SCRIPTS_DIR / "start_round.py"), check=False)
        if deprecated.returncode == 0:
            raise AssertionError("deprecated round command should not succeed")
        assert_contains(deprecated.stderr, "deprecated", "v1.0")

        english_workspace = workspace / "North Star Lab"
        en_init = run(
            str(SCRIPTS_DIR / "init_business.py"),
            "North Star Lab",
            "--path",
            str(workspace),
            "--product-name",
            "North Star Assistant",
            "--target-user",
            "independent builders",
            "--core-problem",
            "they need one visible loop for product, revenue, delivery, and cash",
            "--product-pitch",
            "a visual operating cockpit for one-person AI companies",
            "--language",
            "en-US",
            "--confirmed",
        )
        assert_contains(en_init.stdout, "Operating Navigation", "operating cockpit")
        assert_v1_state(english_workspace)
        assert_exists(reading_entry_path(english_workspace, "en-US"))
        assert_exists(workspace_dir_path(english_workspace, "visual_kit", "en-US") / "business-loop.svg")
        assert_not_exists(english_workspace / "阅读版")
        assert_not_exists(english_workspace / "视觉素材")
        for generated_path in (
            workspace_file_path(english_workspace, "role_index", "en-US"),
            role_brief_path(english_workspace, "control-tower", "en-US"),
            role_brief_path(english_workspace, "founder", "en-US"),
            role_brief_path(english_workspace, "product-strategist", "en-US"),
            workspace_file_path(english_workspace, "flow_bootstrap", "en-US"),
            workspace_file_path(english_workspace, "automation_reminders", "en-US"),
            workspace_file_path(english_workspace, "automation_scheduler", "en-US"),
        ):
            lower_text = generated_path.read_text(encoding="utf-8").lower()
            assert_not_contains(lower_text, "current round", "current stage", "stage-transition", "round-state")

        brief = run(
            str(SCRIPTS_DIR / "build_agent_brief.py"),
            "--role",
            "control-tower",
            "--primary-arena",
            "product",
            "--company-name",
            "North Star Lab",
            "--objective",
            "Tighten the sellable promise",
            "--current-bottleneck",
            "The homepage promise is not concrete enough",
            "--next-shortest-action",
            "Rewrite the first-screen promise and CTA",
            "--language",
            "en-US",
        )
        assert_contains(brief.stdout, "Operating Model", "Primary Arena", "Shortest Next Action")
        assert_not_contains(brief.stdout.lower(), "current round", "current stage", "stage transition", "round goal")


def validate_release_assets() -> None:
    for path in sorted(RELEASE_ASSETS_DIR.glob("*.svg")):
        ET.parse(path)
        text = path.read_text(encoding="utf-8")
        if "round-driven" in text.lower():
            raise AssertionError(f"release asset still mentions old round positioning: {path}")


def validate_public_docs() -> None:
    public_files = (
        "README.md",
        "README.zh-CN.md",
        "GUIDE.md",
        "GUIDE.zh-CN.md",
        "SKILL.md",
        "SAMPLE-OUTPUTS.md",
        "release/README.md",
        "release/README.zh-CN.md",
        "release/clawhub-listing.md",
        "release/sample-outputs.md",
        "release/github-announcement.md",
        "release/social-posts.md",
        "release/v1.0.3-github-release.md",
        "agents/openai.yaml",
    )
    forbidden_public = (
        "What Changed",
        "改了什么",
        "breaking architecture",
        "breaking product",
        "old stage",
        "old round",
        "legacy stage",
        "legacy round",
        "stage/round",
        "阶段/回合",
        "当前回合",
        "当前阶段",
        "阶段切换",
        "current round",
        "current stage",
        "stage transition",
    )
    for relative in public_files:
        text = (ROOT / relative).read_text(encoding="utf-8")
        if "v1.0" not in text:
            raise AssertionError(f"expected v1.0 positioning in {relative}")
        if "visual" not in text.lower() and "可视化" not in text:
            raise AssertionError(f"expected visual positioning in {relative}")
        assert_not_contains(text, *forbidden_public)
    listing = (ROOT / "release" / "clawhub-listing.md").read_text(encoding="utf-8")
    assert_contains(listing, "Operating Cockpit", "AI image")


def main() -> int:
    validate_python_compatibility_logic()
    validate_workspace_scripts()
    validate_release_assets()
    validate_public_docs()
    run(str(SCRIPTS_DIR / "validate_platforms.py"))
    print("release validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

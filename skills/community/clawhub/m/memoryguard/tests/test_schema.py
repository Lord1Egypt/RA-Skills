"""Schema 序列化往返测试。

验证意图: AGR/Finding/Report 的 to_dict/from_dict 必须无损往返，
这是后续规则引擎、报告生成、Provider API 能信任契约的基础。
"""

from __future__ import annotations

from pathlib import Path
import sys

# 让测试在未安装包时也能跑
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from memoryguard.schema import (  # noqa: E402
    AGR,
    AGRType,
    Change,
    ChangeStatus,
    Dimension,
    Finding,
    Location,
    Plan,
    Patch,
    Ref,
    RefRelation,
    Report,
    RiskLevel,
    Scope,
    Sensitivity,
    Severity,
    Surface,
    now_iso,
    sha256_text,
    stable_id,
)


def test_agr_roundtrip():
    agr = AGR(
        id="instruction-abc123",
        type=AGRType.INSTRUCTION,
        path="/tmp/AGENTS.md",
        scope=Scope.PROJECT,
        source="AGENTS.md",
        hash=sha256_text("hello"),
        mtime=now_iso(),
        sensitivity=Sensitivity.NONE,
        refs=[Ref(to="skill-xyz", relation=RefRelation.CITES)],
        metadata={"rel_path": "AGENTS.md", "invisible_reason": ""},
    )
    d = agr.to_dict()
    assert d["type"] == "instruction"
    assert d["refs"][0]["relation"] == "cites"
    agr2 = AGR.from_dict(d)
    assert agr2.type == AGRType.INSTRUCTION
    assert agr2.refs[0].relation == RefRelation.CITES
    assert agr2.id == agr.id


def test_finding_roundtrip():
    f = Finding(
        id="find-1",
        rule_id="instruction.conflict.override",
        severity=Severity.HIGH,
        dimension=Dimension.CONSISTENCY,
        surface=Surface.INSTRUCTION,
        location=Location(agr_id="instruction-abc", path="/tmp/AGENTS.md", span=(10, 20)),
        evidence="rule A overrides rule B",
        impact="Agent effective rules undecidable",
        suggestion="resolve override chain",
        confidence=0.85,
        verification="instruction.resolve_effective_rules",
        fixable=True,
        related_findings=["find-2"],
    )
    d = f.to_dict()
    assert d["severity"] == "high"
    assert d["location"]["span"] == [10, 20]
    f2 = Finding.from_dict(d)
    assert f2.severity == Severity.HIGH
    assert f2.location.span == (10, 20)
    assert f2.confidence == 0.85


def test_report_roundtrip():
    report = Report(
        workspace="/tmp",
        generated_at=now_iso(),
        duration_ms=42,
        health_score=75.0,
        objects=[
            AGR(id="i1", type=AGRType.INSTRUCTION, path="/tmp/AGENTS.md"),
        ],
        findings=[
            Finding(
                id="f1",
                rule_id="r1",
                severity=Severity.LOW,
                dimension=Dimension.VISIBILITY,
                surface=Surface.MEMORY,
                location=Location(agr_id="i1", path="/tmp/AGENTS.md"),
                evidence="e",
                impact="i",
                suggestion="s",
            )
        ],
        invisible=[{"path": "/tmp/secret", "type": "memory", "reason": "binary"}],
    )
    d = report.to_dict()
    assert d["summary"]["object_count"] == 1
    assert d["summary"]["invisible_count"] == 1
    report2 = Report.from_dict(d)
    assert len(report2.objects) == 1
    assert report2.objects[0].id == "i1"
    assert len(report2.findings) == 1
    assert report2.findings[0].severity == Severity.LOW
    assert report2.invisible[0]["reason"] == "binary"


def test_plan_change_roundtrip():
    plan = Plan(
        plan_id="plan-1",
        finding_ids=["f1"],
        intent="fix override cycle",
        risk_level=RiskLevel.LOW,
        patches=[
            Patch(path="/tmp/AGENTS.md", operation="replace", before_hash="abc", diff="-old\n+new")
        ],
        verification=["instruction.resolve_effective_rules"],
    )
    d = plan.to_dict()
    assert d["risk_level"] == "low"
    assert d["patches"][0]["operation"] == "replace"

    change = Change(
        change_id="change-1",
        plan_id="plan-1",
        applied_at=now_iso(),
        backup_paths=["/tmp/.memoryguard/backups/AGENTS.md"],
        changed_paths=["/tmp/AGENTS.md"],
        status=ChangeStatus.VERIFIED,
    )
    cd = change.to_dict()
    assert cd["status"] == "verified"


def test_stable_id_deterministic():
    a = stable_id("instruction", "AGENTS.md")
    b = stable_id("instruction", "AGENTS.md")
    assert a == b
    assert a.startswith("instruction-")


if __name__ == "__main__":
    # 手动运行：python tests/test_schema.py
    test_agr_roundtrip()
    test_finding_roundtrip()
    test_report_roundtrip()
    test_plan_change_roundtrip()
    test_stable_id_deterministic()
    print("all schema tests passed")

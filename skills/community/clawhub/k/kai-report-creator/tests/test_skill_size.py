from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_skill_md_stays_within_routing_budget():
    skill = ROOT / "SKILL.md"
    lines = skill.read_text(encoding="utf-8").splitlines()
    assert len(lines) <= 320, (
        "SKILL.md should stay a thin router. Move detailed contracts to references/ "
        f"instead of growing the hot-path prompt. Current lines: {len(lines)}"
    )

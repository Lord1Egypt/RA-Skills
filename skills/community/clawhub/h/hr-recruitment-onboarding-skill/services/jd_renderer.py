"""Markdown rendering for deterministic job-description output."""

from hr_recruitment_onboarding_skill.services.rule_based_extractor import (
    is_discriminatory_requirement,
    sanitize_requirements,
)


FOOTER = "请以实际工作需要为准，欢迎符合岗位能力要求的人才投递。"


def _safe_items(values: object) -> list[str]:
    if not isinstance(values, list):
        return []
    return [value for value in values if isinstance(value, str) and value and not is_discriminatory_requirement(value)]


def render_jd(position: dict) -> str:
    """Render a position and its requirements as compliant Markdown."""
    raw_requirements = position.get("requirements") or {}
    requirements = (
        sanitize_requirements(raw_requirements)
        if isinstance(raw_requirements, dict)
        else {}
    )
    lines = [f"# {position.get('job_title', '职位')}", "", "## 岗位职责", ""]

    for responsibility in _safe_items(requirements.get("responsibilities")):
        lines.append(f"- {responsibility}")

    lines.extend(["", "## 任职资格", ""])
    education = requirements.get("education")
    if education and not is_discriminatory_requirement(education):
        lines.append(f"- 学历：{education}")

    experience_years = requirements.get("experience_years")
    if experience_years:
        lines.append(f"- 经验：{experience_years}年以上经验")

    for label, key in (("必备技能", "required_skills"), ("加分技能", "preferred_skills")):
        skills = _safe_items(requirements.get(key))
        if skills:
            lines.append(f"- {label}：{'、'.join(skills)}")

    for item in _safe_items(requirements.get("other_requirements")):
        lines.append(f"- {item}")

    lines.extend(["", FOOTER])
    return "\n".join(lines)

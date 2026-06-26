from __future__ import annotations

from models import ReleaseItem, ReleaseSummary, RepoSpec


class TemplateError(ValueError):
    pass


SUPPORTED_LANGUAGES = {"zh", "en"}


COPY = {
    "zh": {
        "unknown": "未知",
        "single_title": "最新 Release",
        "multi_title": "新版本汇总（共 {count} 个）",
        "separator": "：",
        "published_at": "发布时间",
        "core_changes": "核心变化",
        "fixes_improvements": "修复/改进",
        "user_impact": "使用影响",
        "link": "链接",
    },
    "en": {
        "unknown": "Unknown",
        "single_title": "Latest Release",
        "multi_title": "Release Summary ({count} total)",
        "separator": ":",
        "published_at": "Published at",
        "core_changes": "Core changes",
        "fixes_improvements": "Fixes and improvements",
        "user_impact": "User impact",
        "link": "Link",
    },
}


def validate_template(template_name: str) -> str:
    template = (template_name or "default").strip() or "default"
    if template != "default":
        raise TemplateError(f"unsupported output template: {template}")
    return template


def validate_language(language: str | None) -> str:
    normalized = (language or "zh").strip().lower() or "zh"
    if normalized not in SUPPORTED_LANGUAGES:
        raise TemplateError(f"unsupported language: {normalized}")
    return normalized


def _release_lines(release: ReleaseItem, summary: ReleaseSummary, *, language: str) -> list[str]:
    copy = COPY[language]
    sep = copy["separator"]
    return [
        f"- {copy['published_at']}{sep} {release.published_at or copy['unknown']}",
        "",
        summary.markdown.strip(),
        "",
        f"- {copy['link']}{sep} {release.html_url}",
    ]


def format_single_release(repo: RepoSpec, release: ReleaseItem, summary: ReleaseSummary, *, language: str) -> str:
    copy = COPY[language]
    sep = copy["separator"]
    return "\n".join(
        [f"**{repo.slug} {copy['single_title']}{sep} {release.tag_name}**", "", *_release_lines(release, summary, language=language)]
    )


def format_multi_release(repo: RepoSpec, releases: list[ReleaseItem], summaries: list[ReleaseSummary], *, language: str) -> str:
    copy = COPY[language]
    lines = [f"**{repo.slug} {copy['multi_title'].format(count=len(releases))}**", ""]
    for index, (release, summary) in enumerate(zip(releases, summaries), start=1):
        lines.extend([f"**{index}. {release.tag_name}**", *_release_lines(release, summary, language=language), ""])
    return "\n".join(lines).rstrip()


def render_message(
    repo: RepoSpec,
    releases: list[ReleaseItem],
    summaries: list[ReleaseSummary],
    output_template: str = "default",
    language: str = "zh",
) -> str:
    validate_template(output_template)
    language = validate_language(language)
    if len(releases) != len(summaries):
        raise TemplateError("releases and summaries length mismatch")
    if not releases:
        raise TemplateError("nothing to render")
    if len(releases) == 1:
        return format_single_release(repo, releases[0], summaries[0], language=language)
    return format_multi_release(repo, releases, summaries, language=language)

"""Shared model and reader-facing summaries for discovery-stage CV matching.

Discovery cannot honestly promise an application outcome.  What it can do is
show, for a bounded set of full job descriptions, which stated requirements
have evidence in the candidate's frozen profile.  This module deliberately
shares count_coverage's unweighted accounting: a partial match is not silently
turned into a fraction of a match.
"""
from __future__ import annotations

import count_coverage as coverage
import report_locales as locales
import vocab


BASES = ("card", "detail_unmapped", "detail")
RECOMMENDATIONS = ("recommend", "review")

# A recommendation with a full description is more useful than an attractive
# card whose requirements are still unknown.  Within either group, retain the
# skill-wide verdict and effort ordering rather than inventing another score.
RECOMMENDATION_ORDER = {"recommend": 0, "review": 1}
VERDICT_ORDER = {value: index for index, value in enumerate(vocab.VERDICTS)}
EFFORT_ORDER = {value: index for index, value in enumerate(vocab.EFFORT)}
DEFAULT_RECOMMENDATION_VERDICTS = vocab.VERDICTS[:2]


MATCH_TEXT = {
    "zh": {
        "detail_unmapped": ("完整职位描述已核对；尚未逐项匹配简历，暂不作为推荐投递。"),
        "card": ("简历匹配：仅有职位卡，尚未读取完整要求；"
                 "这是一条待核实线索，不是推荐。"),
        "detail": ("简历匹配（已读取详情）：必备条件有充分证据 {strong} 项，共 {must_total} 项"
                   "（部分符合 {partial}，存在缺口 {gap}，无证据 {no_evidence}）；"
                   "核心职责已证实 {responsibilities} 项，共 {responsibility_total} 项。"),
    },
    "en": {
        "detail_unmapped": ("Full job description reviewed; the CV has not yet been mapped "
                            "requirement by requirement. Not a default recommendation."),
        "card": ("CV match: card data only; the full requirements were not read. "
                 "This is a lead to review, not a recommendation."),
        "detail": ("CV match (detail reviewed): {strong} of {must_total} must-haves "
                   "strongly evidenced (partial {partial}, gap {gap}, no evidence "
                   "{no_evidence}); {responsibilities} of {responsibility_total} core "
                   "responsibilities demonstrated."),
    },
    "ja": {
        "detail_unmapped": ("求人の全文を確認済みです。CVとの要件別の照合は未実施のため、"
                            "現時点では応募を推薦していません。"),
        "card": ("履歴書との照合：求人カードのみで、完全な要件は未確認です。"
                 "これは確認対象の候補であり、推薦ではありません。"),
        "detail": ("履歴書との照合（詳細確認済み）：必須条件の強い根拠は全{must_total}項目中"
                   "{strong}項目（部分的 {partial}、不足 {gap}、根拠なし {no_evidence}）；"
                   "裏付けのある主要業務は全{responsibility_total}項目中"
                   "{responsibilities}項目。"),
    },
    "ko": {
        "detail_unmapped": ("전체 채용 공고를 확인했습니다. 이력서와 요건별 대조는 아직 "
                            "진행하지 않았으므로 현재 지원 추천 대상은 아닙니다."),
        "card": ("이력서 대조: 채용 카드만 있으며 전체 요건은 읽지 않았습니다. "
                 "이는 확인할 후보일 뿐 추천이 아닙니다."),
        "detail": ("이력서 대조(상세 확인): 필수 요건의 강한 근거는 총 {must_total}개 중 "
                   "{strong}개(부분 충족 {partial}, 부족 {gap}, 근거 없음 "
                   "{no_evidence}); 근거가 확인된 핵심 업무는 총 "
                   "{responsibility_total}개 중 {responsibilities}개."),
    },
    "es": {
        "detail_unmapped": ("Descripción completa revisada; todavía no se ha contrastado "
                            "el CV requisito por requisito. No es una recomendación de candidatura."),
        "card": ("Correspondencia con el CV: solo hay datos de la ficha; no se han "
                 "leído los requisitos completos. Es una pista para revisar, no una "
                 "recomendación."),
        "detail": ("Correspondencia con el CV (detalle revisado): {strong} de "
                   "{must_total} requisitos obligatorios con evidencia sólida "
                   "(parcial {partial}, carencia {gap}, sin evidencia {no_evidence}); "
                   "{responsibilities} de {responsibility_total} funciones principales "
                   "acreditadas."),
    },
}


def requirement_counts(match: dict) -> dict:
    """Return the core-only, unweighted accounting used in discovery summaries.

    An advertised nice-to-have may be absent without blocking a recommendation.
    Counting it as a must-have in the reader-facing summary would contradict that
    rule, so it remains visible in the mapping but stays out of this core count.
    """
    requirements = [item for item in (match or {}).get("requirements") or []
                    if isinstance(item, dict)
                    and item.get("screening") in ("knockout", "weighted")]
    return coverage.coverage(requirements)


def has_hard_blocker(match: dict) -> bool:
    """Whether a stated knockout has no usable CV evidence."""
    for item in (match or {}).get("requirements") or []:
        if not isinstance(item, dict):
            continue
        if (item.get("screening") == "knockout"
                and effective_match(item) in ("gap", "no_evidence")):
            return True
    return False


def core_rows(match: dict) -> list[dict]:
    """Requirements that are eligibility-relevant rather than optional extras."""
    return [item for item in (match or {}).get("requirements") or []
            if isinstance(item, dict)
            and item.get("screening") in ("knockout", "weighted")]


def effective_match(item: dict) -> object:
    """Apply the shared recency rule before deciding recommendation readiness.

    ``count_coverage.coverage`` already treats a strong claim supported only by
    dated experience as partial. Discovery must use the same interpretation;
    otherwise its reader-facing count and its recommendation rule disagree.
    """
    item = item if isinstance(item, dict) else {}
    if item.get("match") == "strong" and item.get("recency") == "dated":
        return "partial"
    return item.get("match")


def recommendation_failures(row: dict, match: dict) -> list[str]:
    """Why a row cannot be a default recommendation.

    This is intentionally conservative without asking every candidate to meet
    every advertised preference.  Optional rows may be gaps.  Core rows need
    at least partial, evidenced support; a partial that takes days to close is
    not treated as ready merely because it contains a related keyword.
    """
    row = row if isinstance(row, dict) else {}
    match = match if isinstance(match, dict) else {}
    failures = []
    if match.get("basis") != "detail":
        failures.append("detail_required")
    if row.get("verdict") not in DEFAULT_RECOMMENDATION_VERDICTS:
        failures.append("verdict_not_default")
    requirements = [item for item in (match.get("requirements") or [])
                    if isinstance(item, dict)]
    if not requirements:
        failures.append("requirements_missing")
        return failures
    if has_hard_blocker(match):
        failures.append("hard_blocker")
    core = core_rows(match)
    if not core:
        failures.append("core_requirements_missing")
    for item in core:
        outcome = effective_match(item)
        if outcome in ("gap", "no_evidence"):
            failures.append("core_gap")
            break
        if item.get("screening") == "knockout" and outcome != "strong":
            failures.append("knockout_not_strong")
            break
        if outcome == "partial" and item.get("effort") in ("multi_day", "not_closable"):
            failures.append("costly_core_gap")
            break
    # A single directly evidenced keyword cannot carry a long list of core
    # duties. This is a count of quoted evidence, not a weighted fit score: it
    # permits small, closable gaps while requiring direct support for at least
    # half of what the employer actually treats as core.
    strong_core = sum(effective_match(item) == "strong" for item in core)
    if core and strong_core * 2 < len(core):
        failures.append("insufficient_strong_core_evidence")
    core_must = [item for item in core if item.get("kind") == "must_have"]
    if core_must and not any(effective_match(item) == "strong" for item in core_must):
        failures.append("no_strong_core_must_have")
    core_responsibilities = [item for item in core
                             if item.get("kind") == "responsibility"]
    if (core_responsibilities
            and not any(effective_match(item) == "strong"
                        for item in core_responsibilities)):
        failures.append("no_strong_core_responsibility")

    alignment = match.get("alignment") if isinstance(match.get("alignment"), dict) else {}
    domain = alignment.get("domain_fit")
    level = alignment.get("level_direction")
    if domain not in ("same_domain", "adjacent"):
        failures.append("domain_not_close")
    if level not in vocab.LEVEL_DIRECTION or level == "unclear":
        failures.append("level_not_assessed")
    if row.get("verdict") == vocab.VERDICTS[0]:
        if domain != "same_domain":
            failures.append("strong_requires_same_domain")
        if level == "step_up":
            failures.append("strong_requires_non_step_up")
        if any(effective_match(item) != "strong" for item in core):
            failures.append("strong_requires_core_strength")
    return failures


def render_summary(match: dict, lang: str) -> str:
    """Render one exact, localized match summary for shortlist.md.

    The caller selects the report language.  The five languages are the skill's
    existing native-report set; hosts without a localized report use English or
    Chinese by the surrounding report contract.
    """
    if lang not in locales.LANGUAGES:
        raise ValueError(f"unsupported report language: {lang!r}")
    match = match if isinstance(match, dict) else {}
    basis = match.get("basis")
    template = MATCH_TEXT[lang][basis if basis in BASES else "card"]
    if basis != "detail":
        return template
    counts = requirement_counts(match)
    return template.format(
        strong=counts["must_strong"],
        must_total=counts["must_total"],
        partial=counts["must_partial"],
        gap=counts["must_gap"],
        no_evidence=counts["must_no_evidence"],
        responsibilities=counts["resp_demonstrated"],
        responsibility_total=counts["resp_total"],
    )


def summaries(match: dict) -> tuple[str, ...]:
    """Every accepted localized rendering, for a gate reading user-facing text."""
    return tuple(render_summary(match, lang) for lang in locales.LANGUAGES)


def ordering_key(row: dict, match: dict) -> tuple[int, int, int]:
    """The transparent discovery order: verified recommendation, verdict, effort."""
    row = row if isinstance(row, dict) else {}
    match = match if isinstance(match, dict) else {}
    return (
        RECOMMENDATION_ORDER.get(match.get("recommendation"), len(RECOMMENDATIONS)),
        VERDICT_ORDER.get(row.get("verdict"), len(vocab.VERDICTS)),
        EFFORT_ORDER.get(row.get("effort"), len(vocab.EFFORT)),
    )

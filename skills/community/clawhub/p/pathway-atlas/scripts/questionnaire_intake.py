"""Host-facing normalization seam for the twenty-question intake.

Interactive users answer in ordinary language.  The host Agent segments those
answers and normalizes their explicit meaning into the bounded mapping accepted
by :func:`build_profile_from_questionnaire`; users never create JSON or files.
This module deliberately supplies only explicit ``unknown`` defaults for
profile fields the questionnaire did not establish.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime, timedelta, timezone
import re
from types import MappingProxyType
from typing import Any

if __package__:
    from .planning_profile import PlanningProfile, load_planning_profile
else:  # pragma: no cover - direct scripts-path compatibility
    from planning_profile import PlanningProfile, load_planning_profile


_QUESTION_NUMBERS = frozenset(range(1, 21))
_HEADER = re.compile(r"(?m)^\s*(?P<number>[1-9]|1[0-9]|20)[.．、:：]\s*")
_MAX_TRANSCRIPT_CHARS = 32_000
_Q20_KEYS = frozenset(
    {
        "budget",
        "institution_types",
        "service",
        "adjustment",
        "risk",
        "health",
        "school_vs_major",
        "pathways",
        "eligibility",
    }
)
_READINESS_KEYS = frozenset(
    {"english_readiness", "interview_readiness", "physical_readiness"}
)
_RANK_KEYS = frozenset({"rank", "cohort_size"})
_ADDITIONAL_RANK_KEYS = frozenset({"scope", "rank", "cohort_size", "source"})
_JOINT_RANK_SCOPES = frozenset({"city_joint", "province_joint"})


class QuestionnaireIntakeError(ValueError):
    """The host could not form one complete, anonymous twenty-answer set."""


def grade_year_options(*, as_of: date | None = None) -> dict[str, Any]:
    """Suggest current cohort labels; never rewrite a confirmed student profile."""
    if as_of is None:
        as_of = datetime.now(timezone(timedelta(hours=8))).date()
    if type(as_of) is not date:
        raise ValueError("as_of must be a calendar date")
    final_year_exam = as_of.year + (as_of.month >= 7)
    options = [
        {"grade": grade, "exam_year": final_year_exam + offset,
         "label": f"{grade}（预计{final_year_exam + offset}年高考）"}
        for grade, offset in (("高一", 2), ("高二", 1), ("高三", 0))
    ]
    options.append({"grade": "其他", "exam_year": None,
                    "label": "其他／不确定（如已参加高考、复读或社会考生，请补充）"})
    return {"as_of": as_of.isoformat(), "timezone": "Asia/Shanghai",
            "question": "孩子目前读几年级？（单选；暑假按即将升入的年级）",
            "options": options}


def parse_numbered_questionnaire(transcript: str) -> Mapping[int, str]:
    """Split a natural-language numbered reply without interpreting its meaning."""

    if not isinstance(transcript, str):
        raise QuestionnaireIntakeError("questionnaire reply must be text")
    if not transcript.strip() or len(transcript) > _MAX_TRANSCRIPT_CHARS or "\x00" in transcript:
        raise QuestionnaireIntakeError("questionnaire reply is empty or too large")
    matches = tuple(_HEADER.finditer(transcript))
    if not matches or transcript[: matches[0].start()].strip():
        raise QuestionnaireIntakeError("questionnaire reply must use numbered answers")
    answers: dict[int, str] = {}
    for index, match in enumerate(matches):
        number = int(match.group("number"))
        if number in answers:
            raise QuestionnaireIntakeError("questionnaire reply repeats a question")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(transcript)
        answer = transcript[match.end() : end].strip()
        if not answer:
            raise QuestionnaireIntakeError("every questionnaire item needs an answer")
        answers[number] = answer
    if set(answers) != _QUESTION_NUMBERS:
        raise QuestionnaireIntakeError("exactly twenty answered questions are required")
    return MappingProxyType({number: answers[number] for number in range(1, 21)})


def _exact_mapping(value: Any, name: str, keys: frozenset[str]) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != keys:
        raise QuestionnaireIntakeError(f"{name} normalization fields are invalid")
    return value


def _array(value: Any, name: str) -> list[Any]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise QuestionnaireIntakeError(f"{name} must be a normalized list")
    return list(value)


def build_profile_from_questionnaire(answers: Mapping[int, object]) -> PlanningProfile:
    """Build a v3 profile from host-normalized answers without filling gaps.

    The mapping is an internal Agent boundary, not a user-facing input format.
    Values absent from the questionnaire remain empty or ``unknown``; selected
    subjects are not silently relabelled as strengths, and an activity is not
    silently relabelled as research experience.
    """

    if not isinstance(answers, Mapping) or set(answers) != _QUESTION_NUMBERS:
        raise QuestionnaireIntakeError("exactly twenty normalized answers are required")
    try:
        location = _exact_mapping(
            answers[3], "question 3", frozenset({"city", "high_school"})
        )
        timing = _exact_mapping(
            answers[4], "question 4", frozenset({"grade", "exam_year"})
        )
        subjects = _exact_mapping(
            answers[6],
            "question 6",
            frozenset({"mode", "primary", "secondary", "score_basis"}),
        )
        exam = _exact_mapping(
            answers[7],
            "question 7",
            frozenset({"date", "scope", "score", "max_score", "source"}),
        )
        if not isinstance(answers[8], Mapping):
            raise QuestionnaireIntakeError("question 8 normalization fields are invalid")
        rank_keys = set(answers[8])
        if rank_keys == _RANK_KEYS:
            rank = answers[8]
            additional_ranks: list[Any] = []
        elif rank_keys == _RANK_KEYS | {"additional_observations"}:
            rank = answers[8]
            additional_ranks = _array(
                rank["additional_observations"],
                "question 8 additional observations",
            )
            if len(additional_ranks) > 4:
                raise QuestionnaireIntakeError(
                    "question 8 additional observations exceed the bounded intake"
                )
        else:
            raise QuestionnaireIntakeError("question 8 normalization fields are invalid")
        history = _exact_mapping(
            answers[9], "question 9", frozenset({"best_rank", "usual_rank"})
        )
        regions = _exact_mapping(
            answers[16], "question 16", frozenset({"targets", "excluded"})
        )
        constraints = answers[20]
        if not isinstance(constraints, Mapping):
            raise QuestionnaireIntakeError("question 20 normalization fields are invalid")
        extra_q20 = set(constraints) - (_Q20_KEYS | frozenset({"readiness"}))
        if not _Q20_KEYS <= set(constraints) or extra_q20:
            raise QuestionnaireIntakeError("question 20 normalization fields are invalid")
        if "readiness" in constraints:
            readiness = _exact_mapping(
                constraints["readiness"], "question 20 readiness", _READINESS_KEYS
            )
        else:
            readiness = {
                "english_readiness": "unknown",
                "interview_readiness": "unknown",
                "physical_readiness": "unknown",
            }

        award_answer = answers[10]
        if isinstance(award_answer, Mapping):
            award_mapping = _exact_mapping(
                award_answer,
                "question 10",
                frozenset({"subject_strengths", "awards"}),
            )
            subject_strengths = _array(
                award_mapping["subject_strengths"], "subject strengths"
            )
            awards = _array(award_mapping["awards"], "awards")
        else:
            subject_strengths = []
            awards = _array(award_answer, "awards")

        activity_answer = answers[11]
        if isinstance(activity_answer, Mapping):
            activity_mapping = _exact_mapping(
                activity_answer,
                "question 11",
                frozenset({"research_experiences", "activities"}),
            )
            research_experiences = _array(
                activity_mapping["research_experiences"], "research experiences"
            )
            activities = _array(activity_mapping["activities"], "activities")
        else:
            research_experiences = []
            activities = _array(activity_answer, "activities")

        observation_values = (
            exam["score"],
            exam["max_score"],
            rank["rank"],
            rank["cohort_size"],
        )
        observations = []
        if any(value is not None for value in observation_values):
            observations.append(
                {
                    "exam_date": exam["date"],
                    "scope": exam["scope"],
                    "score": exam["score"],
                    "max_score": exam["max_score"],
                    "rank": rank["rank"],
                    "cohort_size": rank["cohort_size"],
                    "source": exam["source"],
                }
            )
        for index, raw_additional in enumerate(additional_ranks, 1):
            additional = _exact_mapping(
                raw_additional,
                f"question 8 additional observation {index}",
                _ADDITIONAL_RANK_KEYS,
            )
            if (
                additional["scope"] not in _JOINT_RANK_SCOPES
                or additional["source"] != "joint_exam_report"
            ):
                raise QuestionnaireIntakeError(
                    "question 8 additional observations must be explicit joint-exam ranks"
                )
            observations.append(
                {
                    "exam_date": exam["date"],
                    "scope": additional["scope"],
                    "score": exam["score"],
                    "max_score": exam["max_score"],
                    "rank": additional["rank"],
                    "cohort_size": additional["cohort_size"],
                    "source": additional["source"],
                }
            )

        payload = {
            "schema_version": "3.0",
            "gender": answers[1],
            "province": answers[2],
            "city": location["city"],
            "high_school": location["high_school"],
            "grade": timing["grade"],
            "exam_year": timing["exam_year"],
            "class_level": answers[5],
            "subject_mode": subjects["mode"],
            "subject_group": subjects["primary"],
            "secondary_subjects": _array(subjects["secondary"], "secondary subjects"),
            "score_basis": subjects["score_basis"],
            "rank_observations": observations,
            "best_rank": history["best_rank"],
            "usual_rank": history["usual_rank"],
            "preparation_assets": {
                "subject_strengths": subject_strengths,
                "awards": awards,
                "research_experiences": research_experiences,
                "activities": activities,
                "english_readiness": readiness["english_readiness"],
                "interview_readiness": readiness["interview_readiness"],
                "physical_readiness": readiness["physical_readiness"],
            },
            "constraints": {
                "excluded_regions": _array(regions["excluded"], "excluded regions"),
                "budget_level": constraints["budget"],
                "institution_types": _array(
                    constraints["institution_types"], "institution types"
                ),
                "service_commitment": constraints["service"],
                "adjustment_preference": constraints["adjustment"],
                "risk_preference": constraints["risk"],
                "health_constraints": _array(
                    constraints["health"], "health constraints"
                ),
            },
            "priorities": {
                "school_vs_major": constraints["school_vs_major"],
                "target_schools": _array(answers[12], "target schools"),
                "target_majors": _array(answers[14], "target majors"),
                "target_regions": _array(regions["targets"], "target regions"),
                "future_plan": answers[17],
                "concerns": _array(answers[18], "concerns"),
                "desired_outcomes": _array(answers[19], "desired outcomes"),
            },
            "target_school_reasons": _array(
                answers[13], "target school reasons"
            ),
            "target_major_reasons": _array(answers[15], "target major reasons"),
            "pathway_preferences": dict(
                _exact_mapping(
                    constraints["pathways"],
                    "question 20 pathways",
                    frozenset(
                        {
                            "strong_foundation",
                            "comprehensive_evaluation",
                            "special_program",
                            "service_oriented",
                            "uniformed_service",
                            "cross_border",
                            "arts_sports",
                        }
                    ),
                )
            ),
            "eligibility_facts": _array(
                constraints["eligibility"], "eligibility facts"
            ),
        }
        return load_planning_profile(payload)
    except QuestionnaireIntakeError:
        raise
    except (KeyError, TypeError, ValueError) as error:
        raise QuestionnaireIntakeError(
            "normalized questionnaire answers do not match the profile contract"
        ) from error


__all__ = [
    "QuestionnaireIntakeError",
    "build_profile_from_questionnaire",
    "grade_year_options",
    "parse_numbered_questionnaire",
]


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Generate one date-aware grade question for the host.")
    parser.add_argument("--grade-options", action="store_true", required=True)
    parser.add_argument("--as-of", type=date.fromisoformat, help="Actual consultation date, YYYY-MM-DD; defaults to today in Shanghai.")
    args = parser.parse_args()
    # ASCII JSON also decodes reliably on hosts whose Windows console is GBK.
    print(json.dumps(grade_year_options(as_of=args.as_of), ensure_ascii=True))

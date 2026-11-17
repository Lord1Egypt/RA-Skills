#!/usr/bin/env python3
"""
career_match.py — honest interest/values/traits -> occupation congruence.

Computes how well a person's self-reported profile (a transparent RIASEC INTEREST
CHECK, plus optional Work Values and a light Big Five read) matches O*NET
occupations shipped in data/career/occupations.json. It emits COARSE BANDS
(Low / Moderate / Strong) with a CONFIDENCE NOTE — never a fabricated percentage,
salary, demand, or percentile. Raw floats are used only for internal ranking and
are kept OUT of the person-facing payload.

Design honesty rules baked in:
  * The person-side items are an interest CHECK grounded in Holland/RIASEC, NOT
    the O*NET Interest Profiler or any validated instrument (see assessment_items.json).
  * Occupations whose interest signal comes only from a 3-letter high-point code
    (riasec == null) are expanded with a coarse 3-2-1 rule and flagged
    lower-confidence. Since the O*NET 31.0 rebuild the shipped data has none.
  * All magic numbers (weights, band thresholds, the 3-2-1 expansion) are the
    disclosed constants below — auditable and tunable.

Pure standard library (no numpy) so it runs offline anywhere, matching the rest
of this skill's scripts; the linear algebra is trivial on 6-vectors.

Usage:
  python3 career_match.py --selftest
  python3 career_match.py --demo
  # or import: from career_match import score_person, rank_occupations, band, confidence
"""
import argparse
import json
import math
import os
import re

# ------------------------------------------------------------------ constants
# Order is fixed everywhere: Realistic, Investigative, Artistic, Social,
# Enterprising, Conventional.
RIASEC_ORDER = ("R", "I", "A", "S", "E", "C")

# High-point code expansion: 1st letter -> 3, 2nd -> 2, 3rd -> 1, others -> 0,
# then L1-normalized (divide by 6). A coarse reconstruction => lower confidence.
HIGHPOINT_RANK_WEIGHTS = (3, 2, 1)
HIGHPOINT_L1 = float(sum(HIGHPOINT_RANK_WEIGHTS))  # 6.0

# Blend weights over whichever components are present (renormalized). Disclosed.
DEFAULT_WEIGHTS = {"interests": 0.45, "values": 0.30, "traits": 0.25}

# Coarse band thresholds on a 0..1 fit. Design defaults, disclosed as tunable.
# Exhaustively verified over all 720 orderings of the six O*NET work values: the
# ipsative cosine's minimum (an exactly reversed ranking) is this value, not 0.
VALUES_COS_FLOOR = 0.615

BAND_LOW_MAX = 0.55       # score < 0.55 -> "Low"
BAND_MODERATE_MAX = 0.75  # 0.55 <= score < 0.75 -> "Moderate"; >= 0.75 -> "Strong"
# The interest fit is (r + 1) / 2, so on it these thresholds sit at r = 0.1 and r = 0.5.

INTEREST_ITEM_MAX = 4     # per-item liking response is stored 0..4
FULL_INTEREST_ITEMS = 21  # the full interest-check item bank size

# Canonical work-value order (for ipsative -> preference vector).
WORK_VALUES = ("Achievement", "Independence", "Recognition",
               "Relationships", "Support", "Working Conditions")

DATA_PATH_DEFAULT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "career", "occupations.json",
)

# ------------------------------------------------------------------ vec helpers
def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def _norm(a):
    return math.sqrt(sum(x * x for x in a))


# ------------------------------------------------------------------ interests
def expand_highpoint_code(code):
    """3-letter (or 1-2 letter) Holland high-point code -> normalized 6-vector.

    'IRC' -> I=3, R=2, C=1, others 0, then /6. Returns [R,I,A,S,E,C].
    """
    code = (code or "").strip().upper()
    vec = [0.0] * 6
    idx = {letter: i for i, letter in enumerate(RIASEC_ORDER)}
    for rank, letter in enumerate(code[:3]):
        if letter in idx:
            vec[idx[letter]] = HIGHPOINT_RANK_WEIGHTS[rank]
    return [v / HIGHPOINT_L1 for v in vec]


def interest_vector_from_ratings(ratings):
    """Six O*NET interest ratings on the 1-7 scale -> 0..1 via (x-1)/6.

    `ratings` is [R,I,A,S,E,C]. Returns a 6-vector.
    """
    return [(float(x) - 1.0) / 6.0 for x in ratings]


def occupation_interest_vector(occ):
    """Return (vector, from_code) for one occupation record.

    Uses six numeric interest ratings when present (occ['riasec'] is a list of
    6 numbers); otherwise expands the verified high_point_code and flags
    from_code=True (lower confidence).
    """
    riasec = occ.get("riasec")
    if isinstance(riasec, (list, tuple)) and len(riasec) == 6 \
            and all(isinstance(x, (int, float)) for x in riasec):
        return interest_vector_from_ratings(riasec), False
    return expand_highpoint_code(occ.get("high_point_code", "")), True


def response_discrimination(responses, scoring_key):
    """How much SHAPE the answers carry, as the spread of the six type means in [0,1].

    Answering the same value to every item yields the vector [k,k,k,k,k,k], which carries
    no information about the person. The cosine this fit used to be still produced a full
    188-occupation ranking from it, always topped by whichever occupation sits closest to
    the uniform direction. The correlation reads only shape, so it would stretch type means
    that barely differ into a full-strength shape. A flat answer set is a non-answer and has
    to be refused, not scored.
    """
    vec, _n = person_interest_vector(responses, scoring_key)
    # a type with no answers is unmeasured, not a zero: counting it as 0 read a skipped type
    # as strong dislike and gave the answers a shape they never had
    measured = [v for letter, v in zip(RIASEC_ORDER, vec)
                if _answered(responses, scoring_key, letter)]
    if not measured:
        return 0.0
    return max(measured) - min(measured)


# Below this spread the answers do not distinguish the six types at all.
MIN_DISCRIMINATION = 0.08
# assessment_items.json: the short form is two items per type. One answer is noise, and a type
# with none can't be read at all.
MIN_ITEMS_PER_TYPE = 2


def _answered(responses, scoring_key, letter):
    """How many of one type's items carry an answer (ids as int or str)."""
    return sum(1 for i in scoring_key.get(letter, [])
               if (responses[i] if i in responses else responses.get(str(i))) is not None)


def person_interest_vector(responses, scoring_key):
    """Interest-check responses -> normalized person vector [R,I,A,S,E,C].

    responses: dict mapping item_id (int or str) -> liking value 0..4.
    scoring_key: dict type_letter -> list of item_ids belonging to that type.
    Per-type raw = sum of that type's answered items; normalized by
    (n_answered_for_type * INTEREST_ITEM_MAX) so uneven item counts and skipped
    items don't bias the vector. Returns (vector, n_items_answered).
    """
    def get(item_id):
        if item_id in responses:
            return responses[item_id]
        return responses.get(str(item_id))

    vec = []
    total_answered = 0
    for letter in RIASEC_ORDER:
        ids = scoring_key.get(letter, [])
        answered = [(i, get(i)) for i in ids if get(i) is not None]
        if answered:
            raw = sum(float(v) for _, v in answered)
            vec.append(raw / (len(answered) * INTEREST_ITEM_MAX))
            total_answered += len(answered)
        else:
            vec.append(0.0)
    return vec, total_answered


def cosine_congruence(p, o):
    """Cosine similarity of two non-negative vectors -> [0,1], or None for an all-zero one.

    values_fit uses it, rescaled against its floor. It is no longer the interest fit: two
    non-negative profiles always point roughly the same way (see correlation_fit).
    """
    denom = _norm(p) * _norm(o)
    if denom == 0:
        return None
    return _dot(p, o) / denom


def correlation_fit(p, o):
    """Interest fit in [0,1]: (r + 1) / 2, r the Pearson correlation of the two profiles.

    Taking out each profile's own mean compares shape, not level. The cosine of the raw
    vectors used to be this fit, and every score here is non-negative, so any two profiles
    already pointed roughly the same way: answering all 21 items at random put a median of
    about 70% of the 188 occupations in Strong, against about 11% now, and a clear favourite
    read differently depending on how the other types were answered. Returns None for a flat
    profile (all six equal), which has no shape to compare.
    """
    if len(p) != len(o):
        raise ValueError(f"profiles of different lengths: {len(p)} and {len(o)}")
    mp, mo = sum(p) / len(p), sum(o) / len(o)
    dp, do = [x - mp for x in p], [y - mo for y in o]
    spread_p, spread_o = _norm(dp), _norm(do)
    if spread_p < 1e-9 or spread_o < 1e-9:
        return None
    r = max(-1.0, min(1.0, _dot(dp, do) / (spread_p * spread_o)))
    return (r + 1.0) / 2.0


def euclid_fit(p, o):
    """Documented alternative (selectable): 1 - ||p-o||2 / sqrt(6), in [0,1].

    Each vector lives in the unit 6-cube, so max L2 distance is sqrt(6).
    The default interest fit is correlation_fit.
    """
    d = math.sqrt(sum((x - y) ** 2 for x, y in zip(p, o)))
    return 1.0 - d / math.sqrt(6.0)


# ------------------------------------------------------------------ values / traits
# Case/spacing/underscore-tolerant lookup for the six canonical value names, so a
# ranking that says "Working_Conditions" or "working conditions" still resolves.
_VALUE_CANON = {w.lower(): w for w in WORK_VALUES}


def _norm_value_name(k):
    key = re.sub(r"\s+", " ", str(k).replace("_", " ").strip().lower())
    return _VALUE_CANON.get(key)  # canonical name, or None if unrecognized


def canonical_values_ranking(ranking):
    """Normalize a values ranking to {canonical_name: rank} covering ALL six,
    or return None if it can't (missing a value, unknown name, a rank that is not a finite
    number). A rank can be fractional: values an occupation rates equally share the average
    rank (2.5), and reading that as a whole number turned the tie back into an order.

    Returning None (rather than raising) is deliberate: an incomplete ranking — a
    form where the person left a value unranked — must DEGRADE the read to
    interests-only, never crash the whole scoring run. Accepts a dict or an ordered
    list (index 0 = most important)."""
    if isinstance(ranking, (list, tuple)):
        ranking = {name: i + 1 for i, name in enumerate(ranking)}
    if not isinstance(ranking, dict):
        return None
    norm = {}
    for k, v in ranking.items():
        name = _norm_value_name(k)
        if name is None:
            continue
        try:
            rank = float(v)
        except (TypeError, ValueError):
            return None
        if not math.isfinite(rank):
            return None
        norm[name] = int(rank) if rank.is_integer() else rank
    return norm if set(norm) == set(WORK_VALUES) else None


def person_values_ranking(values):
    """A person's work-values ranking as ({name: rank}, None), or (None, why not). Each of the
    six must appear once, ranked 1..6 once each: all six at 1, ranks such as 99 or -4, and a
    name given twice all used to count as a real ranking and moved occupations between bands.
    Takes the ordered list --values gives or the {name: rank} the career form stores. The
    occupations' own rankings go through canonical_values_ranking, which stays lenient."""
    if isinstance(values, (list, tuple)):
        names = [_norm_value_name(v) for v in values]
        if None in names or sorted(names) != sorted(WORK_VALUES):
            return None, ("the values ranking must name each of the six O*NET work values once, "
                          "most important first, so it was NOT used: this is an interests-only read")
        return {name: i + 1 for i, name in enumerate(names)}, None
    ranking = canonical_values_ranking(values)
    if ranking is None:
        return None, ("the values ranking does not name all six O*NET work values, so it was "
                      "NOT used: this is an interests-only read")
    if sorted(ranking.values()) != list(range(1, len(WORK_VALUES) + 1)):
        return None, ("the values ranking must rank the six values 1 to 6, each once, so it was "
                      "NOT used: this is an interests-only read")
    return ranking, None


def _pref_vec(norm):
    """Canonical complete ranking dict -> preference vector summing to 1."""
    denom = float(sum(range(1, len(WORK_VALUES) + 1)))  # 21 for 6 values
    return [(7 - norm[name]) / denom for name in WORK_VALUES]


def values_preference_vector(ranking):
    """Ipsative rank of the six work values -> preference vector summing to 1.

    ranking: dict value_name -> rank r in 1..6 (1 = most important), OR an ordered
    list of the six names. Rank r maps to (7 - r) -> 6..1, /21. Raises ValueError if
    the ranking doesn't cover all six values (strict; callers wanting graceful
    degradation should use `values_fit`, which returns None instead)."""
    norm = canonical_values_ranking(ranking)
    if norm is None:
        raise ValueError("values ranking must cover all six O*NET work values")
    return _pref_vec(norm)


def values_fit(person_ranking, occ_ranking):
    """Cosine of person vs occupation ipsative value-preference vectors -> [0,1].

    Returns None (not-scorable) if EITHER ranking can't be canonicalized — an
    incomplete/misspelled person ranking degrades this occupation to interests-only
    instead of crashing the run."""
    p = canonical_values_ranking(person_ranking)
    o = canonical_values_ranking(occ_ranking)
    if p is None or o is None:
        return None
    raw = cosine_congruence(_pref_vec(p), _pref_vec(o))
    if raw is None:
        return None
    # An ipsative rank vector cannot point anywhere near the origin, so this cosine
    # has a hard FLOOR: over all 6! = 720 orderings it never drops below
    # VALUES_COS_FLOOR. Feeding that straight into bands built for a [0,1] metric
    # meant the exactly-opposite ranking still read "Moderate" — the component could
    # not report a mismatch at all. Stretch the real range onto [0,1] so "opposite"
    # lands where it belongs. VALUES_COS_FLOOR is pinned by an exhaustive test. Tied
    # occupation ranks (2.5) keep that floor: an average-rank vector is the mean of the
    # orderings its ties allow, so its cosine with a ranking is at least the lowest of theirs.
    return max(0.0, (raw - VALUES_COS_FLOOR) / (1.0 - VALUES_COS_FLOOR))


def traits_fit(person_traits, occ_expectations):
    """Soft trait signal in [0,1]: 1 - mean(|person - expected|) over MAPPED traits.

    person_traits / occ_expectations: dict trait_name -> value in 0..1. Only
    traits present in BOTH are used; where no defensible occupation expectation
    exists the trait is simply absent. Returns None if nothing maps.
    """
    shared = [t for t in person_traits if t in occ_expectations]
    if not shared:
        return None
    diffs = [abs(float(person_traits[t]) - float(occ_expectations[t])) for t in shared]
    return 1.0 - sum(diffs) / len(diffs)


# ------------------------------------------------------------------ blend / band / confidence
def blended_fit(interest_fit, values_fit=None, traits_fit=None, weights=None):
    """Weighted blend over PRESENT components, renormalized to sum to 1.

    Returns (score, weights_applied). Interests-only -> weight 1.0.
    Interests+values -> 0.60/0.40 (0.45/0.75, 0.30/0.75).
    """
    weights = weights or DEFAULT_WEIGHTS
    parts = {"interests": interest_fit, "values": values_fit, "traits": traits_fit}
    present = {k: v for k, v in parts.items() if v is not None}
    if not present:
        return None, {}
    wsum = sum(weights[k] for k in present)
    applied = {k: round(weights[k] / wsum, 2) for k in present}
    score = sum(weights[k] / wsum * v for k, v in present.items())
    return score, applied


def band(score):
    """Coarse band. Never a number leaves here — this is the person-facing signal."""
    if score is None:
        return "Not scorable"
    if score < BAND_LOW_MAX:
        return "Low"
    if score < BAND_MODERATE_MAX:
        return "Moderate"
    return "Strong"


def confidence(n_interest_items, values_present, traits_present, occ_from_code):
    """Confidence note that shrinks on short / partial assessments and code-only occs."""
    score = 0.0
    score += min(n_interest_items / float(FULL_INTEREST_ITEMS), 1.0) * 0.5
    score += 0.25 if values_present else 0.0
    score += 0.15 if traits_present else 0.0
    score += 0.10 if not occ_from_code else 0.0
    if score >= 0.75:
        return "higher confidence"
    if score >= 0.45:
        return "moderate confidence"
    return "low confidence — treat as a rough sketch"


# ------------------------------------------------------------------ assembler
def _score_occupation(person_vec, n_interest_items, occ,
                      person_values=None, person_traits=None,
                      occ_expectations=None, weights=None):
    """Score one occupation. Returns (person_facing_payload, raw_overall_float).

    raw_overall_float is for INTERNAL ranking only and must not be surfaced.
    """
    o_vec, from_code = occupation_interest_vector(occ)
    i_fit = correlation_fit(person_vec, o_vec)

    v_fit = None
    if person_values is not None and occ.get("work_values"):
        v_fit = values_fit(person_values, occ["work_values"])

    t_fit = None
    if person_traits is not None and occ_expectations:
        t_fit = traits_fit(person_traits, occ_expectations)

    overall, applied = blended_fit(i_fit, v_fit, t_fit, weights)

    components = [k for k, v in (("interests", i_fit), ("values", v_fit),
                                 ("traits", t_fit)) if v is not None]
    notes = []
    if from_code:
        notes.append("occupation scored from 3-letter high-point code")

    payload = {
        "occupation": occ.get("title"),
        "onet_code": occ.get("soc_code"),
        "interest_band": band(i_fit),
        "overall_band": band(overall),
        "components_used": components,
        "weights_applied": applied,
        "confidence": confidence(n_interest_items,
                                 v_fit is not None, t_fit is not None, from_code),
        "notes": notes,
    }
    if occ.get("job_zone") is not None:
        payload["job_zone"] = occ["job_zone"]
    # raw float intentionally NOT in payload; returned separately for ranking.
    raw = overall if overall is not None else -1.0
    return payload, raw


def score_person(responses, scoring_key, occupations,
                 person_values=None, person_traits=None,
                 occ_expectations_by_soc=None, weights=None):
    """Score one person against every occupation. Returns list of payloads
    (person-facing; no raw floats), sorted best-first by the internal float."""
    person_vec, n_items = person_interest_vector(responses, scoring_key)
    occ_exp = occ_expectations_by_soc or {}
    scored = []
    for occ in occupations:
        payload, raw = _score_occupation(
            person_vec, n_items, occ,
            person_values=person_values, person_traits=person_traits,
            occ_expectations=occ_exp.get(occ.get("soc_code")), weights=weights)
        payload["data_quality"] = ("numeric-interests"
                                   if occ.get("riasec") is not None else "code-only")
        scored.append((raw, payload))
    scored.sort(key=lambda t: t[0], reverse=True)
    return [p for _, p in scored]


def score_person_grouped(responses, scoring_key, occupations, **kw):
    """The honest shape of this result: TWO lists, not one.

    Numeric O*NET interest ratings and a 3-letter high-point code reconstructed 3-2-1
    produce differently-shaped score distributions, so one shared band threshold does
    not mean the same thing in each: when 120 of the 188 occupations were code-only, one
    person's numeric set came out 63% "Strong" and the code-only set 20%. Since the
    O*NET 31.0 rebuild every shipped occupation is numeric and `code_only` is empty. It
    stays, so a code-only occupation can never be merged into the numeric ranking.

    Returns {"refused": …} | {"numeric_interests": [...], "code_only": [...], "_note": …}
    """
    thin = [f"{letter} {_answered(responses, scoring_key, letter)}/{len(scoring_key.get(letter, []))}"
            for letter in RIASEC_ORDER
            if _answered(responses, scoring_key, letter) < MIN_ITEMS_PER_TYPE]
    if thin:
        return {
            "refused": True,
            "reason": ("有的类型答得太少，测不出来：" + "、".join(thin)
                       + f"（每类至少 {MIN_ITEMS_PER_TYPE} 题）。跳过的题不是「不喜欢」，是没有信息。"),
            "_next": ("这不是「匹配度低」，是「测不出来」。请对方把没答的题补上（每类至少两题），或者"
                      "直接聊他实际做过什么、什么时候最投入。不要拿这份回答生成排名。"),
            "thin_types": thin,
        }
    disc = response_discrimination(responses, scoring_key)
    if disc < MIN_DISCRIMINATION:
        return {
            "refused": True,
            "reason": ("答案没有区分度：六个类型的得分几乎一样，说明这套回答没有指向性"
                       f"（类型间差 {disc:.3f} < {MIN_DISCRIMINATION}）。"),
            "_next": ("这不是「匹配度低」，是「测不出来」。请对方重做一次，明确区分"
                      "喜欢与不喜欢；或者直接聊他实际做过什么、什么时候最投入。"
                      "不要拿这份回答生成排名。"),
            "discrimination": round(disc, 3),
        }
    ranked = score_person(responses, scoring_key, occupations, **kw)
    code_only = [p for p in ranked if p.get("data_quality") == "code-only"]
    return {
        "numeric_interests": [p for p in ranked if p.get("data_quality") == "numeric-interests"],
        "code_only": code_only,
        "discrimination": round(disc, 3),
        "_note": ("两组分别排名。numeric_interests 用 O*NET 的数值兴趣分（O*NET 标注为模型估算）。"
                  + ("code_only 为空：现在每个职业都有数值兴趣分。" if not code_only else
                     "code_only 的兴趣信号是从三字母高点码 3-2-1 反推的，置信度更低。")
                  + "**两组的档位不可互相比较** —— 不要把它们并成一张表，也不要说某个 "
                  "code_only 职业比某个 numeric 职业更契合。"),
    }


def rank_occupations(responses, scoring_key, occupations, top_n=10, **kw):
    """Convenience wrapper: top-N person-facing payloads."""
    return score_person(responses, scoring_key, occupations, **kw)[:top_n]


# ------------------------------------------------------------------ title lookup
# Mode B (aspiration-job fit) starts from what the person SAYS — "产品经理", "MRI
# 算法工程师", "I want to do UX". Nothing connected those words to a SOC code, so the
# mapping happened by eyeballing a 3000-line JSON, and its failure mode was silent:
# score them against a plausible-looking wrong occupation and never mention it.
# This makes the mapping explicit, ranked, and refusable.

# Words that carry no signal for matching a job title.
_STOP = {"the", "a", "an", "of", "and", "or", "for", "in", "at", "to", "&",
         "工作", "职业", "岗位", "工程师", "师", "员", "人员", "专家", "做"}
# Seniority and standing say how far along someone is, not which job it is.
_MODIFIERS = ("资深", "高级", "中级", "初级", "首席", "副", "实习", "senior", "junior",
              "experienced", "intern")
# Chinese endings that only say a person does the work. 工程师 is not one of them: it says
# which kind of work, so it is an alias below and a title has to be one an engineer holds.
_GENERIC_SUFFIXES = {"人员", "专家", "师", "员", "家"}

# A small bridge from everyday words (incl. Chinese) to O*NET title vocabulary. It is
# deliberately small and visible rather than a fuzzy black box — an unmatched query
# must come back empty so the model asks, instead of quietly picking something near.
# Each alias names ALTERNATIVE phrases: 数据分析 is "data scientist" OR "operations research
# analyst". A title takes an alias only when one whole phrase fits it, so "research" from one
# and "scientist" from the other can't add up to a third title.
_ALIASES = {
    "产品经理": ("product manager",), "程序员": ("programmer", "software developer"),
    "软件工程师": ("software developer",),
    "算法": ("data scientist", "computer research scientist"),
    "机器学习": ("data scientist", "computer research scientist"),
    "人工智能": ("computer research scientist",),
    "数据": ("data scientist", "database"),
    "数据分析": ("data scientist", "operations research analyst"),
    "统计": ("statistician",),
    "医生": ("physician",), "护士": ("nurse",), "老师": ("teacher",), "教师": ("teacher",),
    "律师": ("lawyer",), "会计": ("accountant",), "设计师": ("designer",), "平面": ("graphic",),
    "记者": ("reporter", "journalist"), "翻译": ("interpreter", "translator"),
    "心理咨询": ("counseling psychologist", "counselor"), "社工": ("social worker",),
    "厨师": ("chef", "cook"), "摄影": ("photographer",), "建筑师": ("architect",),
    "护理": ("nurse",), "影像": ("imaging", "radiologic"), "放射": ("radiologic", "imaging"),
    "核磁": ("magnetic resonance imaging",), "磁共振": ("magnetic resonance imaging",),
    "mri": ("magnetic resonance imaging",),
    "理疗": ("physical therapist",), "药剂": ("pharmacist",), "销售": ("sales",),
    "市场": ("marketing", "market research"), "人力资源": ("human resources",),
    "运营": ("operations", "management"), "研究员": ("research scientist",),
    "教授": ("professor", "postsecondary teacher"), "咨询顾问": ("management analyst",),
    "ux": ("web digital interface",), "ui": ("web digital interface",),
    "product manager": ("management analyst", "project management"),
    # everyday words for occupations that ARE in the data and still found nothing
    "小学": ("elementary school",), "中学": ("secondary school",), "高中": ("secondary school",),
    "土木工程": ("civil engineer",), "电气工程": ("electrical engineer",),
    "电工": ("electrician",), "木工": ("carpenter",),
    "客服": ("customer service representative",),
    "司机": ("driver",), "卡车": ("truck",), "货车": ("truck",), "牙医": ("dentist",),
    "消防员": ("firefighter",), "兽医": ("veterinarian",), "物理治疗": ("physical therapist",),
    "前端": ("web developer",), "房地产经纪": ("real estate sales agent",),
    "房产中介": ("real estate sales agent",), "hr": ("human resources",),
    # the words that decide BETWEEN titles, now that a word the title leaves unexplained keeps
    # a hit weak: 数据库管理员 is a database administrator, not a data scientist
    "工程师": ("engineer", "developer", "programmer", "architect"),
    "技师": ("technologist", "technician"), "tech": ("technologist", "technician"),
    "数据库": ("database",), "管理员": ("administrator",), "生物统计": ("biostatistician",),
    "经理": ("manager",), "总监": ("manager",), "科学家": ("scientist",),
    "大学": ("postsecondary",), "college": ("postsecondary",),
    "professor": ("postsecondary teacher",), "high school": ("secondary school",),
    "软件": ("software developer",), "软体": ("software developer",), "开发": ("developer",),
    "经济学": ("economist",), "精算": ("actuary",), "地质": ("geoscientist",),
    "geologist": ("geoscientist",), "ceo": ("chief executive",),
    "首席执行官": ("chief executive",), "管理咨询": ("management analyst",),
    "调研": ("research analyst",), "厨师长": ("chef", "head cook"), "新闻": ("news",),
    "auto": ("automotive",), "sales associate": ("salesperson",),
}
# Aliases that point at NEIGHBOURS because O*NET has no such occupation. A hit that leans
# on one of these can open a conversation; it is never a strong mapping.
_APPROXIMATE = {"产品经理", "product manager", "运营", "研究员"}

_LATIN = re.compile(r"[a-z0-9]+")
_CJK = re.compile(r"[一-鿿]+")
_WORDLIKE = re.compile(r"[a-z0-9]+|[一-鿿]+")


def _fold_query(query):
    """What the person typed, in the form the aliases and titles are written in: NFKC for
    full-width letters (ＵＩ设计师), traditional folded to simplified (軟體工程師), lower case,
    and no space between two Chinese words (土木 工程师). Each of those found nothing."""
    import sys
    import unicodedata
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    from _zh import to_simplified
    text = to_simplified(unicodedata.normalize("NFKC", str(query))).lower()
    return re.sub(r"(?<=[一-鿿])\s+(?=[一-鿿])", "", text).strip()


def _words(s):
    """Latin and CJK runs as separate words, so 「MRI技师」 is mri + 技师, not one token."""
    s = s.lower()
    return [w for w in _LATIN.findall(s) + _CJK.findall(s)
            if w not in _STOP and not w.isdigit()]


def _alias_spans(key, text):
    # A Latin key must stand alone: as a bare substring, 「ui」 matched inside "equipment".
    # Chinese has no spaces between words, so a Chinese key matches anywhere, except that
    # the 工 of 电工 and 木工 also sits inside 工程: 「机电工程师」 is not an electrician.
    if key.isascii():
        return [m.span() for m in
                re.finditer(r"(?<![a-z0-9])" + re.escape(key) + r"(?![a-z0-9])", text)]
    return [m.span() for m in re.finditer(re.escape(key), text)
            if not (key.endswith("工") and text[m.end():m.end() + 1] == "程")]


def _alias_in(key, text):
    return bool(_alias_spans(key, text))


def _query_parts(query):
    """(folded query, its words plus every word its aliases stand for,
    [(alias, [its phrases as word lists], where it sits)], whether any of it leans on an
    approximate alias). Aliases expand the QUERY only — run over occupation titles as well,
    they turned "Agricultural Equipment Operators" into a designer."""
    text = _fold_query(query)
    aliases, expansions, approximate = [], [], False
    for key, phrases in _ALIASES.items():
        spans = _alias_spans(key, text)
        if spans:
            aliases.append((key, [_words(p) for p in phrases], spans))
            expansions.extend(phrases)
            approximate = approximate or key in _APPROXIMATE
    return text, set(_words(" ".join([text] + expansions))), aliases, approximate


def _query_words(query):
    """What the person said plus the O*NET words it stands for, and whether any of it
    leans on an approximate alias."""
    _text, words, _aliases, approximate = _query_parts(query)
    return words, approximate


# O*NET titles say who is left OUT after "Except" ("Elementary School Teachers, Except
# Special Education"), and a trailing ", General" only says the job is not a specialty.
# Counting those words inverted the answer: "special education teacher" came back as the
# one occupation that excludes it, labelled strong. They also made the real title too long
# to win, so 「建筑师」 ranked Database Architects above Architects, Except Landscape and Naval.
_EXCEPT = re.compile(r",?\s+except\s+(.*)$", re.I)
_GENERAL = re.compile(r",\s*general$", re.I)


def _title_words(title):
    """(words that name the occupation, words of the group it leaves out)"""
    m = _EXCEPT.search(title)
    named = set(_words(_GENERAL.sub("", title[:m.start()] if m else title)))
    return named, (set(_words(m.group(1))) - named if m else set())


def _title_heads(title):
    """The roles a title names: the word before " of " (First-Line Supervisors of Police and
    Detectives are supervisors); otherwise the last word of each "and" part before the first
    comma (Radiologic Technologists and Technicians), and the title's last word
    (Securities, Commodities, and Financial Services Sales Agents)."""
    base = _GENERAL.sub("", _EXCEPT.sub("", title)).lower()
    before_of = re.split(r"\s+of\s+", base, maxsplit=1)
    if len(before_of) == 2:
        return set(_words(before_of[0])[-1:])
    heads = set(_words(base)[-1:])
    for part in re.split(r"\s+and\s+", base.split(",", 1)[0]):
        heads |= set(_words(part)[-1:])
    return heads


def _same_word(a, b):
    """The same word, or one grammatical ending apart: "statistician" finds "Statisticians"
    and "actuary" finds "Actuaries". A bare prefix is not the same word: "special" is not
    "specialties", "tech" is neither "technicians" nor "technologists", and "market" is not
    "marketing"."""
    if a == b:
        return True
    short, long_ = sorted((a, b), key=len)
    return (long_ in (short + "s", short + "es")
            or (short.endswith("y") and long_ == short[:-1] + "ies"))


def _fits(words, title_words):
    return bool(words) and all(any(_same_word(a, b) for b in title_words) for a in words)


def _unexplained(text, aliases, title_words):
    """What the query says that this title doesn't account for: the parts no title word and
    no fitting alias covers, less seniority words, stop words and the endings that only say
    a person does the work. 「牙医助理」 leaves 助理 against Dentists; 「核磁共振工程师」 leaves
    工程师 against MRI technologists."""
    mask = [False] * len(text)
    for _key, phrases, spans in aliases:
        if any(_fits(p, title_words) for p in phrases):
            for start, end in spans:
                mask[start:end] = [True] * (end - start)
    for m in _LATIN.finditer(text):
        if any(_same_word(m.group(0), b) for b in title_words):
            mask[m.start():m.end()] = [True] * (m.end() - m.start())
    rest = "".join(" " if covered else ch for ch, covered in zip(text, mask))
    left = []
    for w in _WORDLIKE.findall(rest):
        if w.isascii():
            if not (w in _STOP or w in _MODIFIERS or w.isdigit()):
                left.append(w)
            continue
        for filler in _MODIFIERS + ("工作", "岗位", "做"):
            w = w.replace(filler, "")
        if w and w not in _GENERIC_SUFFIXES:
            left.append(w)
    return left


def _matching_parts(text, aliases, title_words):
    """How many separate parts of the query fit this title: each Latin word that is a title
    word, and each alias with a phrase that fits. One alias that happens to name two title
    words (工程师: engineer … architect) is still one part."""
    parts = {m.group(0) for m in _LATIN.finditer(text)
             if m.group(0) not in _STOP and any(_same_word(m.group(0), b) for b in title_words)}
    parts |= {key for key, phrases, _spans in aliases if any(_fits(p, title_words) for p in phrases)}
    return len(parts)


def find_occupations(query, occupations, limit=8):
    """Rank shipped occupations by how well their title matches `query`.

    Returns [{soc_code, title, job_zone, has_numeric_interests, has_work_values, score,
    match}], best first, and **an empty list when nothing matches** — that is the honest
    answer, not a reason to reach for the nearest title.

    `match` is "strong" for an exact title, or when all of these hold: the title explains
    everything the query says (「牙医助理」 leaves 助理 unexplained against Dentists), the
    title's own role is among the words matched (First-Line Supervisors of Police and
    Detectives are supervisors, not detectives), two separate parts of the query fit the
    title or the title is covered whole (「司机」 fits only "drivers" in Heavy and
    Tractor-Trailer Truck Drivers), and nothing leans on an approximate alias or asks for the
    group an "Except" clause leaves out. A title whose matched words another strong title
    covers and more is weak too. Strong hits sort first, and when more than one title is
    strong (and none is exact) they are all marked `tied`."""
    text, q, aliases, approximate = _query_parts(query)
    if not q:
        return []
    out, exact_titles = [], set()
    for o in occupations:
        title = o.get("title", "")
        t, excluded = _title_words(title)
        if not t:
            continue
        # count TITLE words covered, so "data" and "database" can't both count as one
        # shared word twice
        covered = {b for b in t if any(_same_word(a, b) for a in q)}
        if not covered:
            continue
        exact = text == title.lower()
        asks_for_excluded = any(_same_word(a, b) for a in q for b in excluded)
        strong = exact or (not approximate and not asks_for_excluded
                           and (_matching_parts(text, aliases, t) >= 2 or covered == t)
                           and bool(covered & _title_heads(title))
                           and not _unexplained(text, aliases, t))
        if exact:
            exact_titles.add(title)
        out.append({
            "soc_code": o.get("soc_code"), "title": title,
            "job_zone": o.get("job_zone"),
            "has_numeric_interests": o.get("riasec") is not None,
            "has_work_values": o.get("work_values") is not None,
            "score": 1.0 if exact else round(len(covered) / len(q | t), 3),
            "match": "strong" if strong else "weak",
            "matched_on": sorted(covered),
        })
    # A title whose matched words are a strict subset of another strong title's explains
    # less of what they said: for 「中学老师」, Elementary School Teachers shares only "school
    # teachers", which Secondary School Teachers covers along with "secondary".
    strong_sets = [set(r["matched_on"]) for r in out if r["match"] == "strong"]
    for r in out:
        if (r["match"] == "strong" and r["title"] not in exact_titles
                and any(set(r["matched_on"]) < s for s in strong_sets)):
            r["match"] = "weak"
    out.sort(key=lambda r: (r["match"] != "strong", -r["score"], r["title"]))
    # Every title still strong here explains the whole query, so none of them is the choice:
    # 「大学教授」 fits "Teachers, Postsecondary" in every subject, and 数据分析师 fits Data
    # Scientists and Operations Research Analysts on different words. An exact title wins.
    strong_hits = [r for r in out if r["match"] == "strong"]
    if len(strong_hits) > 1 and not exact_titles:
        for r in strong_hits:
            r["tied"] = True
    return out[:limit]


# ------------------------------------------------------------------ data loading
def load_occupations(path=DATA_PATH_DEFAULT):
    with open(path, "r", encoding="utf-8") as f:
        doc = json.load(f)
    return doc.get("occupations", []), doc.get("attribution", "")


def load_scoring_key(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(DATA_PATH_DEFAULT), "assessment_items.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f).get("scoring_key", {})


# ------------------------------------------------------------------ selftest / demo
def _selftest():
    ok = True

    def check(name, cond):
        nonlocal ok
        ok = ok and cond
        print(("  PASS " if cond else "  FAIL ") + name)

    # expansion
    v = expand_highpoint_code("IRC")  # I=3,R=2,C=1 -> /6
    check("expand IRC sums to 1", abs(sum(v) - 1.0) < 1e-9)
    check("expand IRC I>R>C ordering",
          v[RIASEC_ORDER.index("I")] > v[RIASEC_ORDER.index("R")] >
          v[RIASEC_ORDER.index("C")] > 0)
    check("expand single letter 'C'", abs(sum(expand_highpoint_code("C")) - 0.5) < 1e-9)

    # ratings rescale
    check("ratings 1->0 and 7->1",
          interest_vector_from_ratings([1, 7, 1, 1, 1, 1])[0] == 0.0 and
          interest_vector_from_ratings([1, 7, 1, 1, 1, 1])[1] == 1.0)

    # cosine bounds + degenerate
    check("cosine identical == 1", abs(cosine_congruence([0, 1, 0, 0, 0, 0],
                                                         [0, 2, 0, 0, 0, 0]) - 1.0) < 1e-9)
    check("cosine orthogonal == 0", abs(cosine_congruence([1, 0, 0, 0, 0, 0],
                                                          [0, 1, 0, 0, 0, 0])) < 1e-9)
    check("cosine degenerate -> None", cosine_congruence([0, 0, 0, 0, 0, 0],
                                                         [0, 1, 0, 0, 0, 0]) is None)

    # the interest fit: centered correlation, shape not level
    check("correlation same shape == 1", abs(correlation_fit(
        [0, 1, 0, 0, 0, 0], [0.1, 0.9, 0.1, 0.1, 0.1, 0.1]) - 1.0) < 1e-9)
    check("correlation opposite shape == 0", abs(correlation_fit(
        [1, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1])) < 1e-9)
    occ_shape = [0.8, 0.3, 0.2, 0.2, 0.5, 0.7]
    check("correlation ignores level", abs(
        correlation_fit([0.9, 0.2, 0.1, 0.4, 0.3, 0.6], occ_shape)
        - correlation_fit([0.65, 0.3, 0.25, 0.4, 0.35, 0.5], occ_shape)) < 1e-9)
    check("correlation flat -> None", correlation_fit([0.5] * 6, [0, 1, 0, 0, 0, 0]) is None)

    # person vector normalization (uneven item counts)
    key = {"R": [1, 2, 3, 4], "I": [5, 6, 7, 8], "A": [9, 10, 11, 12],
           "S": [13, 14, 15], "E": [16, 17, 18], "C": [19, 20, 21]}
    resp_all4 = {i: 4 for i in range(1, 22)}
    pv, n = person_interest_vector(resp_all4, key)
    check("all-max responses -> all 1.0", all(abs(x - 1.0) < 1e-9 for x in pv) and n == 21)

    # blend renormalization
    s, applied = blended_fit(0.8, 0.6, None)  # interests+values
    check("blend interests+values weights 0.60/0.40",
          applied == {"interests": 0.6, "values": 0.4})
    check("blend value 0.6*0.8+0.4*0.6", abs(s - (0.6 * 0.8 + 0.4 * 0.6)) < 1e-9)
    s1, a1 = blended_fit(0.9, None, None)
    check("interests-only weight 1.0", a1 == {"interests": 1.0} and abs(s1 - 0.9) < 1e-9)

    # bands
    check("band thresholds", band(0.54) == "Low" and band(0.6) == "Moderate"
          and band(0.9) == "Strong" and band(None) == "Not scorable")

    # confidence monotonicity
    lo = confidence(6, False, False, True)
    hi = confidence(21, True, True, False)
    check("confidence low on short+code-only", lo.startswith("low"))
    check("confidence higher on full battery", hi == "higher confidence")

    # values ipsative
    vv = values_preference_vector(list(WORK_VALUES))
    check("values vector sums to 1", abs(sum(vv) - 1.0) < 1e-9)
    check("values top == 6/21", abs(vv[0] - 6 / 21.0) < 1e-9)

    # values ranking robustness (the path #4 made live — must degrade, not crash)
    full = {"Achievement": 1, "Independence": 2, "Recognition": 3,
            "Relationships": 4, "Support": 5, "Working Conditions": 6}
    underscore = dict(full); underscore["Working_Conditions"] = underscore.pop("Working Conditions")
    check("underscore name normalizes", values_fit(underscore, full) is not None)
    incomplete = {k: full[k] for k in list(full)[:4]}  # only 4 of 6
    check("incomplete person ranking -> values_fit None (no crash)",
          values_fit(incomplete, full) is None)
    check("unknown value name -> None", canonical_values_ranking(
          {"Nope": 1, "Independence": 2, "Recognition": 3, "Relationships": 4,
           "Support": 5, "Working Conditions": 6}) is None)
    # an occupation with an incomplete work_values must not crash a scored run
    key6 = {"R": [1], "I": [2], "A": [3], "S": [4], "E": [5], "C": [6]}
    bad_occ = [{"soc_code": "x", "title": "X", "riasec": [4, 4, 4, 4, 4, 4],
                "work_values": {"Achievement": 1}}]  # malformed wv
    try:
        _ = score_person({1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 4}, key6, bad_occ,
                         person_values=full)
        check("malformed occ work_values degrades (no crash)", True)
    except Exception:
        check("malformed occ work_values degrades (no crash)", False)

    # end-to-end against shipped data (if present)
    try:
        occs, attr = load_occupations()
        check("attribution present", "O*NET" in attr and "CC BY 4.0" in attr)
        # An I-leaning person should surface an I-first occupation on top.
        resp = {i: (4 if i in (5, 6, 7, 8) else 1) for i in range(1, 22)}
        top = rank_occupations(resp, key, occs, top_n=5)
        check("ranking returns payloads without raw floats",
              top and all("_score" not in p and "overall_band" in p for p in top))
        check("top occupation is Investigative-first",
              any(o["soc_code"] == p["onet_code"] and o["high_point_code"][0] == "I"
                  for p in top[:1] for o in occs))
    except FileNotFoundError:
        print("  SKIP end-to-end (occupations.json not found)")

    print("SELFTEST:", "OK" if ok else "FAILURES")
    return ok


def _demo():
    key = load_scoring_key()
    occs, attr = load_occupations()
    # An Investigative+Conventional leaning person (data-science shape).
    resp = {i: 1 for i in range(1, 22)}
    for i in (5, 6, 7, 8, 19, 20, 21):
        resp[i] = 4
    print("Attribution:", attr[:80], "...\n")
    print("Top matches (interest-only run):")
    for p in rank_occupations(resp, key, occs, top_n=8):
        print(f"  {p['overall_band']:8s} | {p['confidence']:35s} | "
              f"{p['occupation']} ({p['onet_code']})")


def _yaml_module():
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    from _deps import ensure
    return ensure("PyYAML", "yaml")


def _cli_score(args):
    """Score one person from the command line. Returns an exit code.

    This is the supported way to score, and the only one the docs point at: it always goes
    through score_person_grouped, so an answer set with no shape is refused (exit 3) and
    the two occupation groups arrive apart. There used to be no command at all — career.md
    said to import the module and named `score_person`, which skips both guards, and a
    model following that line reported 'Strong' matches for someone who had answered
    'neutral' to all 21 items."""
    def emit(payload, code):
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return code

    if args.score_intake and args.answers is not None:
        return emit({"ok": False, "error": "pass --score-intake or --answers, not both"}, 2)
    values = [v.strip() for v in args.values.split(",") if v.strip()] if args.values else None
    if args.score_intake:
        home = os.path.abspath(args.home or os.environ.get("COMPANION_HOME")
                               or os.path.expanduser("~/.companion"))
        path = os.path.join(home, "state", "modules", "career_intake.yaml")
        latest = None
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    loaded = _yaml_module().safe_load(f) or {}
            except Exception as e:      # a hand edit or a half-written file
                return emit({"ok": False, "error": f"{path} can't be read: {e}",
                             "_next": ("Fix or delete that file, then run the career check again "
                                       "(form_server.py --form career).")}, 2)
            latest = loaded.get("latest") if isinstance(loaded, dict) else None
        if not isinstance(latest, dict) or not latest.get("answers"):
            return emit({"ok": False, "error": f"no career check on file in {home}",
                         "_next": ("Run `form_server.py --form career` and wait for the "
                                   "submit, or collect the 21 answers in chat and pass them "
                                   "with --answers.")}, 2)
        answers, source = latest["answers"], "career_intake"
        if values is None and latest.get("values_rank"):
            values = latest["values_rank"]
    else:
        try:
            answers = json.loads(args.answers)
        except ValueError as e:
            return emit({"ok": False, "error": f"--answers is not valid JSON: {e}"}, 2)
        source = "answers"

    if not isinstance(answers, dict) or not answers:
        return emit({"ok": False,
                     "error": "answers must be a non-empty {item_id: 0..4} object"}, 2)
    clean, bad, twice = {}, [], []
    for k, v in answers.items():
        # ASCII digits only: str.isdigit() accepts "²", which int() then rejects with a traceback
        ok = (not isinstance(v, bool) and re.fullmatch(r"[0-9]+", str(k).strip())
              and (isinstance(v, int) or (isinstance(v, str) and re.fullmatch(r"[0-9]+", v.strip()))))
        if ok:
            item, val = int(str(k).strip()), int(v)
            ok = 1 <= item <= FULL_INTEREST_ITEMS and 0 <= val <= INTEREST_ITEM_MAX
        if not ok:
            bad.append(f"{k}={v!r}")
            continue
        if item in clean:              # "1" and "01" are one item, and one answer was lost
            twice.append(str(item))
            continue
        clean[item] = val
    if bad:
        return emit({"ok": False,
                     "error": (f"answers must be item ids 1..{FULL_INTEREST_ITEMS} with values "
                               f"0..{INTEREST_ITEM_MAX}; got " + ", ".join(bad[:6]))}, 2)
    if twice:
        return emit({"ok": False,
                     "error": ("item " + ", ".join(twice) + " is answered more than once (for "
                               "example as \"1\" and \"01\"); give one answer per item")}, 2)

    person_values, values_problem = person_values_ranking(values) if values else (None, None)
    occupations, _attribution = load_occupations()
    result = score_person_grouped(clean, load_scoring_key(), occupations,
                                  person_values=person_values)
    if result.get("refused"):
        return emit(dict(result, ok=False, source=source), 3)
    payload = {"ok": True, "source": source, "answered": len(clean),
               "values_used": person_values is not None,
               "discrimination": result["discrimination"], "_note": result["_note"]}
    if values and person_values is None:
        payload["values_note"] = values_problem
    if args.soc:
        for group in ("numeric_interests", "code_only"):
            for row in result[group]:
                if row.get("onet_code") == args.soc:
                    payload["occupation"] = dict(row, group=group)
        if "occupation" not in payload:
            return emit({"ok": False,
                         "error": (f"{args.soc} is not one of the {len(occupations)} shipped "
                                   "occupations; get a code from --find")}, 2)
    else:
        top = max(1, args.top)
        payload["numeric_interests"] = result["numeric_interests"][:top]
        payload["code_only"] = result["code_only"][:top]
    return emit(payload, 0)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Honest career interest/values/traits matcher")
    ap.add_argument("--selftest", action="store_true", help="run internal checks")
    ap.add_argument("--demo", action="store_true", help="rank shipped occupations for a demo profile")
    ap.add_argument("--find", default=None, metavar="TITLE",
                    help="map what the person CALLS a job ('产品经理', 'MRI 技师') to the "
                         "shipped O*NET occupations, before scoring anything against it")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--score-intake", action="store_true",
                    help="score the career check the person submitted (state/modules/"
                         "career_intake.yaml, written by form_server.py --form career)")
    ap.add_argument("--answers", default=None, metavar="JSON",
                    help='score answers collected in chat: {"1": 0-4, ..., "21": 0-4}')
    ap.add_argument("--values", default=None, metavar="LIST",
                    help="work-values ranking, most important first, comma-separated")
    ap.add_argument("--soc", default=None, metavar="CODE",
                    help="with a score: report this one occupation (a code from --find)")
    ap.add_argument("--top", type=int, default=10, help="rows per group (default 10)")
    ap.add_argument("--home", default=None, help="override COMPANION_HOME")
    args = ap.parse_args()
    if args.selftest:
        raise SystemExit(0 if _selftest() else 1)
    if args.score_intake or args.answers is not None:
        raise SystemExit(_cli_score(args))
    if args.find is not None:
        occs, _ = load_occupations()
        if not args.find.strip():
            print(json.dumps({"ok": False, "error": "--find needs the words the person used "
                              "for the job, e.g. --find \"产品经理\""}, ensure_ascii=False))
            raise SystemExit(2)
        hits = find_occupations(args.find, occs)
        if not hits:
            note = (f"NO MATCH: no title among the {len(occs)} shipped occupations shares a word "
                    "with what they said. That is not proof the job is missing, so don't say it "
                    "is. Do NOT substitute the nearest title: ask what the work is day to day and "
                    "try --find with those words, ask which shipped occupation is closest in "
                    "day-to-day WORK, or give an interests-only read with no occupation "
                    "congruence at all.")
        elif all(h["match"] == "weak" for h in hits):
            note = ("Every candidate is a WEAK match: one shared word, or an alias that points "
                    "at neighbouring occupations because O*NET has no such job. Say plainly "
                    "that none of these is the job they named, ask which is closest in "
                    "day-to-day WORK, or give an interests-only read. Don't score a weak "
                    "match as if it were their job.")
        elif hits[0].get("tied"):
            note = ("Several titles fit everything they said equally well (" + "、".join(
                        h["title"] for h in hits if h.get("tied")) + "), so their order means "
                    "nothing. Ask which one is their actual work before scoring any of them.")
        else:
            note = ("Confirm the mapping with the person before scoring — «你说的X，我按 O*NET "
                    "的「<title>」来算，行吗?» Scoring them against a title they didn't mean is "
                    "a wrong answer that looks right. Only a `strong` candidate is the job "
                    "itself; a `weak` one is a neighbour.")
        payload = {"query": args.find, "matches": hits, "_note": note}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            if not hits:
                print(f"no match for {args.find!r} among the {len(occs)} shipped occupations.")
            for h in hits:
                flags = ("numeric-interests" if h["has_numeric_interests"] else "code-only") + \
                        (" +values" if h["has_work_values"] else "")
                print(f"  {h['score']:.2f}  {h['match']:6s} {h['title']} ({h['soc_code']}) "
                      f"[zone {h['job_zone']}, {flags}]")
            print("\n" + payload["_note"])
        raise SystemExit(0)
    if args.demo:
        _demo()
    else:
        ap.print_help()

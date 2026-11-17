"""Fast, source-linked planning references with a fixed family-facing layout.

This pure module does not certify a research receipt or predict admission.
The host supplies read public text; school-rank interpolation and selection are
deterministic, and the original evidence journal remains independent.
"""
from __future__ import annotations

from bisect import bisect_left
import math
import re
from statistics import median

from scripts.adapters.public_text import PublicTextAdapterError, PublicTextField, bind_public_text
from scripts.path_recommend import validate_public_output_text
from scripts.planning_profile import PlanningProfile
from scripts.opportunity_order import align_qualitative_pathways, reference_position, sort_reference
from scripts.exam_cutoffs import estimate_cutoff_score, rank_at_score


POLICY_VERSION = "planning-reference-v1"
TIERS = ("冲", "稳", "保")
ORDINARY_COUNTS = dict(zip(TIERS, (3, 4, 5)))
PATHWAY_NAMES = {
    "strong_foundation": "强基计划",
    "comprehensive_evaluation": "综合评价",
    "hong_kong_macao": "港澳升学",
}
INTRODUCTIONS = {
    "strong_foundation": (
        "是什么：面向基础学科等领域选拔培养人才的招生途径，适合对相关学科有持续兴趣的学生。",
        "培养模式：通常实行专门培养方案，重视基础研究及进一步深造；本研衔接、考核与转段按各校方案执行。",
    ),
    "comprehensive_evaluation": (
        "是什么：结合高考及其他考核信息进行选拔的招生方式；浙江三位一体属于相关选择，具体评价项目和权重因校而异。",
        "培养模式：录取后按所报专业或专项方案培养；综合评价主要是选拔方式，本身不等于保研或特殊学位。",
    ),
    "hong_kong_macao": (
        "是什么：申请香港、澳门高校的本科招生，可涉及内地统招或独立申请，须按具体院校区分。",
        "培养模式：按当地高校的本科课程和学位制度培养，授课语言、学制、通识与专业安排以项目说明为准。",
    ),
}
DISCLAIMER = "AI生成，仅供升学规划参考；不构成录取承诺，正式报考以当年官方要求为准。"


def _text(value, name, *, limit=400):
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"{name} requires concise nonempty text")
    value = value.strip()
    if "\n" in value or "\r" in value:
        raise ValueError(f"{name} must be one line")
    validate_public_output_text(value)
    return value


def _number(value, name, *, minimum=1, maximum=10000000):
    if type(value) not in (int, float) or not math.isfinite(value) or not minimum <= value <= maximum:
        raise ValueError(f"{name} is outside its numeric range")
    return value


def _year(value, research_year):
    if type(value) is not int or not research_year - 3 <= value <= research_year:
        raise ValueError("source year must be in the current four-year reference window")
    return value


class _Sources:
    def __init__(self, records, research_year):
        self.records = {}
        self.used = set()
        for raw in records:
            key = _text(raw["source_id"], "source_id", limit=100)
            if key in self.records:
                raise ValueError("duplicate source_id")
            _year(raw["year"], research_year)
            _text(raw["title"], "source title", limit=150)
            # PublicTextAdapter validates source IDs, public URLs and privacy.
            bind_public_text(source_id=key, url=raw["url"], text=raw["text"],
                             fields={"missing": PublicTextField.missing()})
            self.records[key] = dict(raw)

    def cite(self, record, values=(), *, year=None):
        citation = record["citation"]
        source = self.records.get(citation["source_id"])
        if source is None or (year is not None and source["year"] != year):
            raise ValueError("citation source or year does not match")
        bound = PublicTextField(value=list(values), quote=citation["quote"],
                               start=citation.get("start"), end=citation.get("end"))
        try:
            bind_public_text(source_id=source["source_id"], url=source["url"],
                             text=source["text"], fields={"claim": bound})
        except PublicTextAdapterError as error:
            raise ValueError("brief claim is not grounded in the saved public quote") from error
        self.used.add(source["source_id"])
        return f"[{source['year']}年材料]({source['url']})"

    def field(self, record, field, value, *, year):
        citation = record.get("citations", {}).get(field, record.get("citation"))
        if citation is None:
            raise ValueError(f"{field} requires a public citation")
        return self.cite({"citation": citation}, (value,), year=year)


def _interpolate(x, points):
    points = sorted(points)
    if len(points) < 2 or len({p[0] for p in points}) != len(points):
        raise ValueError("calibration requires at least two distinct rank anchors")
    if any(b[1] <= a[1] for a, b in zip(points, points[1:])):
        raise ValueError("rank anchors must be strictly monotone")
    # Do not silently extrapolate an unsupported part of the school cohort.
    if not points[0][0] <= x <= points[-1][0]:
        return None
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x0 <= x <= x1:
            return round(y0 + (x - x0) * (y1 - y0) / (x1 - x0))
    return None


def _score_rows(profile, table, sources, research_year):
    year = _year(table["year"], research_year)
    expected_group = profile.subject_group if profile.subject_mode == "3+1+2" else "综合"
    if table.get("subject_group") != expected_group:
        raise ValueError("score table subject group does not match the province examination system")
    rows, links = [], []
    for row in table["rows"]:
        score = _number(row["score"], "gaokao score", minimum=0, maximum=900)
        rank = _number(row["rank"], "gaokao rank", minimum=0)
        links.append(sources.cite(row, (score, rank), year=year))
        rows.append((rank, score))
    # Empty score bands have zero new candidates and legitimately repeat the
    # cumulative rank, including zero at the top. Keep these for score lookup;
    # rank lookup takes the highest score at a repeated cumulative boundary.
    rows.sort(key=lambda row: -row[1])
    if (len(rows) < 2 or len({score for _, score in rows}) != len(rows)
            or any(b[0] < a[0] for a, b in zip(rows, rows[1:]))):
        raise ValueError("score table must have distinct decreasing scores and nondecreasing cumulative ranks")
    return year, rows, links


def _school_report_estimate(profile, latest, model, payload, sources, research_year):
    """Turn reported cumulative counts into explicit planning scenarios.

    A retained social report is usable here without the deep consensus gate.
    Its counts are observations; the rank curve remains a disclosed estimate.
    """
    scenarios, links, gaps, seen_curves = [], [], [], set()
    tables = list(payload.get("historical_score_tables", []))
    if payload.get("score_table"):
        tables.append(payload["score_table"])
    expected_group = profile.subject_group if profile.subject_mode == "3+1+2" else "综合"
    kinds = {"school_publication": "学校发布", "third_party": "第三方转述",
             "social_video": "社交平台喜报", "user_material": "用户提供的公开喜报"}
    reports = model.get("reports", [])
    if len(reports) > 12:
        raise ValueError("use at most twelve retained school reports")
    for report in reports:
        year = _year(report["year"], research_year)
        school = _text(report["school"], "report school")
        if report["source_kind"] not in kinds:
            raise ValueError("school report source kind must describe its origin")
        comparison = report["comparability"]
        if comparison == "same_school":
            if school != profile.high_school:
                raise ValueError("school report belongs to another school")
        elif comparison == "regional_comparable":
            _text(report["comparability_reason"], "school proxy reason")
        else:
            raise ValueError("school report comparability must be explicit")
        if report["subject_group"] != expected_group:
            raise ValueError("school report cohort does not match the subject group")
        cohort = report.get("cohort_size")
        reported_school = _text(report.get("reported_school", school), "reported school name")
        if reported_school != school:
            _text(report.get("school_identity_basis"), "school alias identity basis")
        values = [reported_school]
        if cohort is not None:
            cohort = _number(cohort, "report cohort", maximum=100000)
            values.append(cohort)
        links.append(sources.cite(report, values, year=year))
        # Historical cohort changes are normalized by the student's percentile.
        scale = cohort / latest.cohort_size if cohort and latest.cohort_size else 1
        x = latest.rank * scale
        points, anchor_notes = [], []
        for metric in report.get("metrics", []):
            kind = metric["kind"]
            if kind == "top_score":
                sources.cite(metric, (metric["score"],), year=year)
                gaps.append("仅有最高分，继续寻找分数段人数、上线人数或同档学校喜报")
                continue
            if kind not in {"score_count", "score_rate", "tier_count", "tier_rate"}:
                raise ValueError("unsupported school report metric")
            if kind.endswith("_rate"):
                if cohort is None:
                    gaps.append("上线率缺同口径人数，保留为定性材料")
                    continue
                rate = _number(metric["rate_percent"], "report rate", maximum=100)
                count = cohort * rate / 100
                amount = rate
            else:
                count = _number(metric["count"], "cumulative count", maximum=100000)
                amount = count
            if cohort is not None and count > cohort:
                raise ValueError("report count exceeds the report cohort")
            if kind.startswith("score_"):
                score = _number(metric["score"], "report score", minimum=0, maximum=900)
                links.append(sources.cite(metric, (score, amount), year=year))
                matching = [table for table in tables if table["year"] == year]
                if len(matching) > 1:
                    raise ValueError("provide one score table per reference year")
                if not matching:
                    gaps.append(f"{year}年喜报等待同年一分一段表，学校和路径继续交付")
                    continue
                _, rows, table_links = _score_rows(profile, matching[0], sources, research_year)
                ranks = [rank for rank, row_score in rows if row_score == score]
                if not ranks or ranks[0] == 0:
                    gaps.append(f"已读表未覆盖喜报{score:g}分，保留其他锚点")
                    continue
                rank_values = ranks
                links.extend(table_links)
                note = f"{score:g}分累计{count:g}人"
            else:
                label = _text(metric["label"], "report tier label")
                links.append(sources.cite(metric, (label, amount), year=year))
                benchmark = metric["benchmark"]
                _text(benchmark["basis"], "tier benchmark basis")
                benchmark_year = _year(benchmark["year"], research_year)
                rank_values = []
                for row in benchmark["ranks"]:
                    rank = _number(row["province_rank"], "tier benchmark rank")
                    links.append(sources.cite(row, (rank,), year=benchmark_year))
                    rank_values.append(rank)
                if not rank_values:
                    gaps.append("层次人数缺代表校门槛参照，保留其他锚点")
                    continue
                note = f"{label}累计{count:g}人（层次位次为代表校参照）"
            points.append((count, median(rank_values), min(rank_values), max(rank_values)))
            anchor_notes.append(note)
        if not points:
            continue
        points.sort()
        if len({point[0] for point in points}) != len(points) or any(b[1] <= a[1] for a, b in zip(points, points[1:])):
            gaps.append("一份喜报的累计人数不单调或重叠，按独立口径整理后再用")
            continue
        signature = (year, school, cohort, tuple(points))
        if signature in seen_curves:
            continue
        seen_curves.add(signature)
        # One count boundary carries information about the cohort; top-score-only
        # input does not. Limit proportional/extrapolated scenarios to nearby ranks.
        curve = [(point[0], point[1]) for point in points]
        extrapolated = len(curve) == 1 or not curve[0][0] <= x <= curve[-1][0]
        if extrapolated:
            near = min(curve, key=lambda point: abs(point[0] - x))
            if near[0] <= 1 or not 0.5 <= x / near[0] <= 2:
                gaps.append("当前校排离现有喜报人数边界过远，继续用同档学校或目标梯度")
                continue
            if len(curve) == 1:
                center = round(near[1] * x / near[0])
                method = "单个累计人数锚点按校位比例作粗估"
            else:
                (x0, y0), (x1, y1) = curve[:2] if x < curve[0][0] else curve[-2:]
                center = round(y0 + (x - x0) * (y1 - y0) / (x1 - x0))
                method = "相邻人数锚点作有限外推"
        else:
            center = _interpolate(x, curve)
            method = "分数段/层次累计人数锚点插值"
        if center is None or center < 1:
            gaps.append("当前锚点无法形成正向省排估计")
            continue
        margin = _number(model.get("margin_fraction", 0.2), "planning margin", minimum=0.1, maximum=0.8)
        if (extrapolated or cohort is None or latest.cohort_size is None or comparison == "regional_comparable"
                or any(metric["kind"].startswith("tier_") for metric in report.get("metrics", []))):
            margin = max(margin, 0.5 if len(curve) == 1 else 0.4)
        spread = max(max(abs(p[1] - p[2]), abs(p[3] - p[1])) / p[1] for p in points)
        margin = max(margin, spread)
        bounds = [max(1, math.floor(center * (1 - margin))), math.ceil(center * (1 + margin))]
        for school_rank in (profile.best_rank, profile.usual_rank):
            if school_rank is not None and len(curve) > 1:
                rank = _interpolate(school_rank * scale, curve)
                if rank is not None:
                    bounds = [min(bounds[0], rank), max(bounds[1], rank)]
        cohort_note = "按历届与本届同组人数比例对齐校位" if cohort and latest.cohort_size else "历届人数未齐，暂按同规模假设"
        notes = [f"{year}年{kinds[report['source_kind']]}：" + "、".join(anchor_notes), method, cohort_note]
        if comparison == "regional_comparable":
            notes.append("同档学校代理：" + report["comparability_reason"])
        notes.append(f"±{margin:.0%}为规划浮动假设，不是统计置信区间")
        scenarios.append({"year": year, "school": school, "central_rank": center,
                          "rank_bounds": bounds, "basis": "；".join(notes)})
    if not scenarios:
        return {"basis": "；".join(dict.fromkeys(gaps)) or "尚无可用喜报人数锚点", "citations": list(dict.fromkeys(links))}
    newest = max(item["year"] for item in scenarios)
    active = [item for item in scenarios if item["year"] == newest]
    center = round(median(item["central_rank"] for item in active))
    bounds = [min(item["rank_bounds"][0] for item in scenarios), max(item["rank_bounds"][1] for item in scenarios)]
    basis = model["basis"] + "；" + active[0]["basis"]
    if len(scenarios) > 1:
        basis += "；不同年份或转述保留为独立情景，中心取最新年份情景中位数，范围覆盖全部情景，不合并成官方事实"
    return {"central_rank": center, "rank_bounds": bounds, "basis": basis,
            "scenarios": scenarios, "citations": list(dict.fromkeys(links))}


def _cutoff_position(profile, latest, model, payload, sources, research_year, result):
    exam = model.get("exam", {})
    group = profile.subject_group if profile.subject_mode == "3+1+2" else "综合"
    if (latest is None or latest.score is None or exam.get("confirmed") is not True
            or exam.get("province") != profile.province or exam.get("subject_group") != group
            or exam.get("date") != latest.exam_date or exam.get("scope") != latest.scope
            or exam.get("max_score") != latest.max_score
            or exam.get("score_basis") not in {"原始分", "赋分", "原始分与赋分"}
            or exam.get("score_basis") != profile.score_basis
            or model.get("gaokao_province") != profile.province
            or model.get("gaokao_subject_group") != group
            or model.get("gaokao_score_basis") != exam.get("score_basis")
            or model.get("gaokao_max_score") != latest.max_score):
        result["basis"] = "划线尚未确认，或考试、科类、满分、计分口径未对齐"
        return result
    name = _text(exam["name"], "cutoff exam name")
    origins = {"parent_image": "家长图片确认", "parent_text": "家长文字确认", "school_publication": "学校划线材料"}
    if exam.get("source_kind") not in origins:
        raise ValueError("cutoff source kind must identify its real origin")
    year = _year(model["year"], research_year)
    lines = {}
    for line in exam.get("lines", []):
        label = _text(line["label"], "exam cutoff label")
        if label in lines:
            raise ValueError("duplicate exam cutoff label")
        lines[label] = None if line.get("score") is None else _number(line["score"], "exam cutoff", minimum=0, maximum=latest.max_score)
        if exam["source_kind"] == "school_publication" and lines[label] is not None:
            result["citations"].append(sources.cite(line, (label, lines[label])))
    if len(lines) > 12 or len(model.get("anchors", [])) > 12:
        raise ValueError("use at most twelve total-score cutoffs")
    pairs, notes, seen = [], [], set()
    teacher_reported = False
    for anchor in model.get("anchors", []):
        label = _text(anchor["exam_label"], "exam cutoff label")
        if label in seen or label not in lines:
            raise ValueError("cutoff correspondence must name a unique recorded line")
        seen.add(label)
        if lines[label] is None:
            continue
        target_label = _text(anchor["gaokao_label"], "gaokao cutoff label")
        target = _number(anchor["gaokao_score"], "gaokao cutoff", minimum=0, maximum=model["gaokao_max_score"])
        basis = _text(anchor["basis"], "cutoff correspondence basis")
        kind = anchor["reference_kind"]
        if kind == "teacher_reported":
            statement = _text(anchor["parent_statement"], "parent-reported teacher statement")
            if ((label not in statement and target_label not in statement)
                    or re.search(r"(?<![\d.+\-−])" + re.escape(f"{target:g}") + r"(?![\d.])", statement) is None):
                raise ValueError("teacher statement must retain the reported reference score")
            teacher_reported = True
        elif kind in {"official_cutoff", "published_benchmark"}:
            result["citations"].append(sources.cite(anchor, (target_label, target), year=year))
        else:
            raise ValueError("cutoff reference kind must describe the correspondence")
        pairs.append((lines[label], target))
        notes.append(f"{label}{lines[label]:g}→{target_label}{target:g}分（{basis}）")
    estimate = estimate_cutoff_score(latest.score, pairs, latest.max_score, model.get("margin_points", 10))
    if estimate is None:
        result["basis"] = "划线缺少可对应的高考参照，或本次分数离已知线过远"
        return result
    result.update(score=estimate["score"], score_bounds=estimate["score_bounds"], reference_year=year,
                  method="exam_cutoffs", cutoff_calculation=estimate)
    result["basis"] = (f"{name}，{origins[exam['source_kind']]}；{estimate['calculation']}；"
                       + "、".join(notes) + f"；±{estimate['margin_points']:g}分为规划浮动假设，非统计置信区间")
    if teacher_reported:
        result["basis"] += "；含家长转述的老师对应参照，未独立核验"
    tables = list(payload.get("historical_score_tables", []))
    if payload.get("score_table"):
        tables.append(payload["score_table"])
    matching = [table for table in tables if table["year"] == year]
    if len(matching) > 1:
        raise ValueError("provide one score table per cutoff reference year")
    if matching:
        _, rows, links = _score_rows(profile, matching[0], sources, research_year)
        result["citations"].extend(links)
        center, approximated = rank_at_score(estimate["score"], rows)
        lower, lo_approx = rank_at_score(estimate["score_bounds"][1], rows)
        upper, hi_approx = rank_at_score(estimate["score_bounds"][0], rows)
        if center is not None:
            result["central_rank"] = center
            result["rank_bounds"] = [lower, upper]
            result["strategy_bounds"] = ([lower, upper] if lower is not None and upper is not None
                else [max(1, math.floor(center * 0.8)), math.ceil(center * 1.2)])
            if lower is None or upper is None:
                result["basis"] += "；表格未覆盖完整分数范围，选校暂用位次±20%规划窗口，不伪报范围位次"
        if approximated or lo_approx or hi_approx:
            result["basis"] += "；省排插值来自已读分数行，非官方精确同分位次"
    if result["central_rank"] is None:
        result["basis"] += f"；省排待{year}年同省同科类一分一段表覆盖"
    result["citations"] = list(dict.fromkeys(result["citations"]))
    return result


def _position(profile, payload, sources, research_year):
    observations = sorted(profile.rank_observations, key=lambda obs: obs.exam_date)
    latest = observations[-1] if observations else None
    model = payload.get("calibration", {"method": "unavailable", "basis": "暂无可比校准资料"})
    method = model["method"]
    if latest is not None and method in {"school_rank", "school_report"}:
        same_exam = [obs for obs in observations if obs.exam_date == latest.exam_date and obs.scope == "school"]
        if len(same_exam) == 1:
            latest = same_exam[0]
    result = {"exam_score": latest.score if latest else None,
              "exam_max_score": latest.max_score if latest else None,
              "central_rank": None, "rank_bounds": None,
              "strategy_bounds": None,
              "score": None, "score_bounds": None, "reference_year": None,
              "method": "unavailable", "basis": "暂无可比校准资料", "citations": []}
    if method not in {"school_rank", "school_report", "official_rank", "official_score", "exam_cutoffs", "unavailable"}:
        raise ValueError("unsupported calibration method")
    result["basis"] = _text(model["basis"], "calibration basis")
    if method == "unavailable":
        return result
    if method == "exam_cutoffs":
        # Additional joint ranks for the same exam must not hide its school row.
        exam = model.get("exam", {})
        matching = [obs for obs in observations if latest is not None
                    and obs.exam_date == latest.exam_date == exam.get("date")
                    and obs.scope == exam.get("scope")]
        if len(matching) == 1:
            latest = matching[0]
            result.update(exam_score=latest.score, exam_max_score=latest.max_score)
        result = _cutoff_position(profile, latest, model, payload, sources, research_year, result)
        fallback = payload.get("fallback_calibration")
        if result["score"] is None and fallback:
            if fallback["method"] not in {"school_rank", "school_report", "unavailable"}:
                raise ValueError("cutoff fallback must use school calibration or unavailable")
            alternative = _position(profile, {**payload, "calibration": fallback}, sources, research_year)
            alternative["basis"] = result["basis"] + "；已转用：" + alternative["basis"]
            return alternative
        return result
    if latest is None or (latest.rank is None and method != "official_score"):
        result["basis"] = "已有学校资料，但本次校排尚不明确；先给典型目标梯度"
        return result
    if method in {"official_rank", "official_score"}:
        if latest.scope != "province_official" or profile.exam_year != research_year:
            raise ValueError("official_rank requires the actual current gaokao rank")
        if method == "official_score":
            table = payload.get("score_table")
            if table is None or table["year"] != research_year:
                raise ValueError("official score mapping requires the matching current-year table")
            _, rows, _ = _score_rows(profile, table, sources, research_year)
            matches = [rank for rank, score in rows if score == latest.score]
            if len(matches) != 1 or matches[0] == 0:
                raise ValueError("the actual gaokao score has no exact row in the score table")
            center = matches[0]
        else:
            center = latest.rank
        bounds = [center, center]
        basis = "用户确认的当年正式高考位次" if method == "official_rank" else "用户确认的当年高考分数对应同分累计位次参考"
    elif method == "school_report":
        if latest.scope != "school":
            raise ValueError("school reports require a school-scope rank")
        estimate = _school_report_estimate(profile, latest, model, payload, sources, research_year)
        result.update(estimate)
        if estimate.get("central_rank") is None:
            return result
        center, bounds, basis = estimate["central_rank"], estimate["rank_bounds"], estimate["basis"]
    else:
        if latest.scope != "school":
            raise ValueError("school_rank requires a school-scope rank")
        comparability = model["comparability"]
        if comparability == "same_school":
            if model["school"] != profile.high_school:
                raise ValueError("calibration school does not match profile")
        elif comparability == "regional_comparable":
            _text(model["comparability_reason"], "regional comparability reason")
        else:
            raise ValueError("calibration must identify the comparable school cohort")
        year = _year(model["year"], research_year)
        points = []
        for anchor in model["anchors"]:
            x = _number(anchor["school_rank"], "school rank")
            y = _number(anchor["province_rank"], "province rank")
            result["citations"].append(sources.cite(anchor, (x, y), year=year))
            points.append((x, y))
        center = _interpolate(latest.rank, points)
        if center is None:
            result["basis"] = "本次校排超出已读取锚点范围；先按真实学校资料给目标梯度"
            return result
        margin = _number(model.get("margin_fraction", 0.2), "planning margin", minimum=0.1, maximum=0.5)
        bounds = [max(1, math.floor(center * (1 - margin))), math.ceil(center * (1 + margin))]
        for school_rank in (profile.best_rank, profile.usual_rank):
            if school_rank is not None:
                rank = _interpolate(school_rank, points)
                if rank is not None:
                    bounds = [min(bounds[0], rank), max(bounds[1], rank)]
        basis = (f"{year}年学校出口锚点按校排插值；{result['basis']}；"
                 f"上下浮动{margin:.0%}为规划敏感性假设，非统计置信区间，不假定未来成绩自动提高")
    strategy_bounds = bounds if method in {"school_rank", "school_report"} else [max(1, math.floor(center * 0.8)), math.ceil(center * 1.2)]
    result.update(central_rank=center, rank_bounds=bounds, strategy_bounds=strategy_bounds, method=method, basis=basis)
    table = payload.get("score_table")
    if table:
        year, rows, links = _score_rows(profile, table, sources, research_year)
        result["citations"] += links
        def score_at(rank):
            if not rows[0][0] <= rank <= rows[-1][0]:
                return None
            index = bisect_left([r for r, _ in rows], rank)
            return rows[index][1]
        result.update(score=score_at(center), reference_year=year)
        lo, hi = score_at(bounds[1]), score_at(bounds[0])
        if lo is not None and hi is not None:
            result["score_bounds"] = [lo, hi]
    result["citations"] = list(dict.fromkeys(result["citations"]))
    return result


def _candidates(profile, payload, sources, positioning, research_year):
    groups = {kind: {tier: [] for tier in TIERS} for kind in ("ordinary", *PATHWAY_NAMES)}
    alternatives = {kind: {tier: [] for tier in TIERS} for kind in PATHWAY_NAMES}
    selected_subjects = set(profile.subject_group.split("+")) | set(profile.secondary_subjects)
    center = positioning["central_rank"]
    for raw in payload.get("candidates", []):
        kind = raw["kind"]
        if kind not in groups:
            raise ValueError("unsupported candidate pathway")
        if raw["province"] != profile.province:
            raise ValueError("candidate admissions province differs from the profile")
        year = _year(raw["year"], research_year)
        if raw["fit"] not in {"matched", "conditional", "blocked"}:
            raise ValueError("candidate fit must be explicit")
        if raw["fit"] == "blocked" or (kind == "ordinary" and raw["location_province"] != profile.province):
            continue
        scope_link = None
        admissions_provinces = raw.get("admissions_provinces")
        if admissions_provinces is not None:
            if (not isinstance(admissions_provinces, list) or not admissions_provinces
                    or not all(isinstance(p, str) and p.strip() for p in admissions_provinces)):
                raise ValueError("admissions_provinces requires a nonempty source-bound province list")
            scope_link = sources.field(raw, "admissions_provinces", admissions_provinces, year=year)
            if profile.province not in admissions_provinces and "全国" not in admissions_provinces:
                continue
        preferences = raw["matches_preferences"]
        if not isinstance(preferences, list) or not set(preferences) <= set(profile.target_majors):
            raise ValueError("major preference matches must refer to the confirmed profile")
        if kind == "ordinary" and profile.target_majors and not preferences:
            continue
        required = raw.get("required_subjects")
        if required is not None and (not isinstance(required, list) or not all(isinstance(s, str) for s in required)):
            raise ValueError("required_subjects is an AND list, or null when unverified")
        if required is not None and not set(required) <= selected_subjects:
            continue
        fields = ("school", "major", "fit_reason", "cautions")
        item = {key: _text(raw[key], key) for key in fields}
        threshold = raw.get("threshold_rank")
        threshold_basis = raw.get("threshold_basis")
        if threshold_basis not in {"admission", "shortlist", "planning_benchmark", "unavailable"}:
            raise ValueError("candidate threshold basis must be explicit")
        links = [sources.field(raw, field, item[field], year=year) for field in ("school", "major")]
        if scope_link:
            links.append(scope_link)
        for field in ("cultivation", "selection"):
            if raw.get(field):
                item[field] = _text(raw[field], field)
                links.append(sources.field(raw, field, item[field], year=year))
            else:
                item[field] = "校级细则待核验，先按该路径的一般培养方式理解"
        if required is not None:
            links.append(sources.field(raw, "required_subjects", required, year=year))
        if threshold is not None:
            _number(threshold, "threshold rank")
            links.append(sources.field(raw, "threshold_rank", threshold, year=year))
        elif raw.get("threshold_score") is not None:
            score = _number(raw["threshold_score"], "admission score", minimum=0, maximum=900)
            links.append(sources.field(raw, "threshold_score", score, year=year))
            tables = list(payload.get("historical_score_tables", []))
            if payload.get("score_table"):
                tables.append(payload["score_table"])
            matching = [table for table in tables if table["year"] == year]
            if len(matching) > 1:
                raise ValueError("provide one score table per admission year")
            if matching:
                _, rows, table_links = _score_rows(profile, matching[0], sources, research_year)
                ranks = [rank for rank, value in rows if value == score]
                if ranks and ranks[0] > 0:
                    threshold = ranks[0]
                    links.extend(table_links)
        if threshold is not None and threshold_basis == "unavailable":
            raise ValueError("a threshold number requires its real basis")
        citation = " ".join(dict.fromkeys(links))
        target_tier = raw.get("benchmark_tier")
        tier_reason = _text(raw["tier_reason"], "pathway tier reason") if raw.get("tier_reason") else None
        reasoned_target = (kind != "ordinary" and threshold_basis == "planning_benchmark"
                           and target_tier in TIERS and tier_reason is not None)
        if reasoned_target:
            # Ordinary-admission benchmarks are not the pathway's own entry
            # thresholds; retain a disclosed comparative planning judgment.
            tier = target_tier
        elif center is not None and threshold is not None:
            lower, upper = positioning["strategy_bounds"]
            if threshold < lower:
                continue
            tier = "冲" if threshold < center else "稳" if threshold < upper else "保"
        else:
            tier = raw.get("benchmark_tier")
            if tier not in TIERS:
                raise ValueError("unpositioned examples require a target tier")
        item.update(threshold_rank=threshold, threshold_basis=threshold_basis,
                    fit="conditional" if required is None or (profile.target_majors and not preferences) else raw["fit"],
                    year=year, citation=citation, matches_preferences=list(preferences),
                    required_subjects=required, personal_tier=center is not None and threshold is not None and not reasoned_target,
                    location_province=_text(raw["location_province"], "school location"),
                    admissions_provinces=admissions_provinces,
                    tier_reason=tier_reason)
        groups[kind][tier].append(item)
    for kind in PATHWAY_NAMES:
        align_qualitative_pathways(kind, groups[kind])
    pools = {kind: dict(tiers) for kind, tiers in groups.items()}
    for kind, tiers in groups.items():
        seen = set()
        for tier, items in tiers.items():
            # Stable ties preserve the host's fit/priority ordering, including
            # qualitative targets without a numerical admission threshold.
            sort_reference(kind, items, center)
            chosen = []
            for item in items:
                if item["school"] not in seen:
                    seen.add(item["school"])
                    chosen.append(item)
                limit = ORDINARY_COUNTS[tier] if kind == "ordinary" else 1
                if len(chosen) == limit:
                    break
            tiers[tier] = chosen
        if kind in alternatives:
            # Reserve every primary before picking backups, so a duplicate in
            # one tier cannot consume another tier's primary or backup slot.
            for tier in TIERS:
                for item in pools[kind][tier]:
                    primary = tiers[tier][0] if tiers[tier] else None
                    if primary and not primary['personal_tier'] and not item['personal_tier']:
                        current = reference_position(kind, primary['school'], primary['major'])
                        backup = reference_position(kind, item['school'], item['major'])
                        if current and backup and current[0] != backup[0]:
                            continue
                    if item["school"] not in seen:
                        seen.add(item["school"])
                        alternatives[kind][tier].append(item)
                        break
    return groups, alternatives


def _threshold_text(item, *, pathway=False):
    basis = "历史专业录取参考" if item["threshold_basis"] == "admission" else "历史入围参考"
    if item["threshold_basis"] == "planning_benchmark":
        basis = "普通批参照，不能代表本路径入围线" if pathway else "目标参照"
    if item["threshold_rank"] is None:
        if item.get('reference_comparison'):
            return "按全国院校层次列为相对目标"
        return "按项目相对选拔难度列为目标梯度，历史门槛待补"
    return f"{basis}约{item['threshold_rank']}位"


def _render_pathway(kind, groups, alternatives, positioning, decision):
    """Show the opportunity ladder before the score rationale and suitability."""
    lines, displayed = [""], []
    for tier in TIERS:
        lines += [f"**{tier}1所**", ""]
        items = groups[tier]
        if items:
            item = items[0]
            lines.append(f"1. **{item['school']}｜{item['major']}**：{_threshold_text(item, pathway=True)}。{item['citation']}")
            displayed.append((tier, item))
        else:
            lines.append("本档已有0所，缺1所；本轮全国候选中尚未形成可列目标，继续保留其他档位。")
        for item in alternatives[tier]:
            lines.append(f"同档备选：**{item['school']}｜{item['major']}**，{_threshold_text(item, pathway=True)}。{item['citation']}")
            displayed.append((tier, item))
        lines.append("")
    center = positioning["central_rank"]
    if center is not None and displayed:
        score = positioning["score"]
        reference = (f"按{positioning['reference_year']}年口径大致{score}分、约{center}位" if score is not None
                     else f"当前省排参考约{center}位")
        assessment = f"以{reference}为当前规划位置，{PATHWAY_NAMES[kind]}可以纳入考虑，按上面的冲、稳、保梯度安排准备"
        if not all(item["personal_tier"] for _, item in displayed):
            assessment += "；部分档位结合项目相对选拔难度作比较判断，不等于已核实的个人入围线"
    elif displayed:
        assessment = "先按项目相对选拔难度列出冲、稳、保目标；个人分数定位补齐后复核分数匹配"
    else:
        assessment = "本轮未形成可列的项目目标，暂不认定分数已匹配该路径"
    lines += ["**分数判断**：" + assessment + "。保档表示相对下探的准备选择，不代表保录。", "",
              *INTRODUCTIONS[kind], "", "**适配与准备提醒**", "", _text(decision, "pathway decision").rstrip("。；") + "。"]
    for tier, item in displayed:
        explanation = item["fit_reason"].rstrip("。；")
        if item["tier_reason"]:
            explanation = item["tier_reason"].rstrip("。；") + "；" + explanation
        if not item["matches_preferences"]:
            explanation += "；该项目与已选专业方向的契合度需进一步比较"
        lines += [f"- **{item['school']}（{tier}）**：{explanation}。",
                  f"  培养：{item['cultivation'].rstrip('。；')}；选拔：{item['selection'].rstrip('。；')}。",
                  f"  需留意：{item['cautions'].rstrip('。；')}。"]
    lines.append("")
    return lines


def _render_groups(groups, *, counts, personal_rank, pathway=False):
    lines = [""]
    all_items = [item for items in groups.values() for item in items]
    repeated_caution = {item["cautions"] for item in all_items}
    common_caution = next(iter(repeated_caution)) if len(all_items) > 1 and len(repeated_caution) == 1 else None
    if common_caution:
        lines += [f"共同需留意：{common_caution}。", ""]
    for tier in TIERS:
        items = groups[tier]
        count = counts[tier]
        lines.append(f"**{tier}{count}所**")
        lines.append("")
        for index, item in enumerate(items, 1):
            threshold = _threshold_text(item, pathway=pathway) if item["threshold_rank"] is not None else "录取/入围门槛尚待补齐"
            conditional = "；条件待核实" if item["fit"] == "conditional" else ""
            if not personal_rank or not item["personal_tier"]:
                conditional += "；目标梯度，未判断个人录取把握"
            lines.append(f"{index}. **{item['school']}｜{item['major']}**：{item['fit_reason']}。{threshold}{conditional}。{item['citation']}。")
            if pathway:
                lines.append(f"   培养：{item['cultivation']}；选拔：{item['selection']}。")
            if not common_caution:
                lines.append(f"   需留意：{item['cautions']}。")
        if len(items) < count:
            lines.append(f"本档已有{len(items)}所，缺{count - len(items)}所符合当前地域、专业和已知条件的候选；先使用已列目标，扩大地域或新增公开材料后补足。")
        lines.append("")
    return lines


def _position_explanation(positioning):
    """Describe the route already calculated, without adding another estimate."""
    method = positioning["method"]
    if method == "exam_cutoffs" and positioning["score"] is not None:
        pairs = positioning["cutoff_calculation"]["used_pairs"]
        if len(pairs) == 2:
            left, right = pairs
            explanation = (f"本次考试的{left[0]:g}、{right[0]:g}分划线，分别对应高考参照的"
                           f"{left[1]:g}、{right[1]:g}分；保留孩子在两条线之间的相对位置来折算分数。")
        else:
            line, target = pairs[0]
            explanation = (f"先看本次成绩与{line:g}分划线相差多少，再把同样的分差加到对应的"
                           f"高考参照{target:g}分上。")
        if positioning["central_rank"] is None:
            return explanation + "省排还需同一年、本省同科类的一分一段表，现阶段先保留分数参考。"
        return explanation + "再由同一年、本省同科类的一分一段表查找或估算省排。"
    if method in {"school_rank", "school_report"} and positioning["central_rank"] is not None:
        explanation = "根据已读到的学校往年成绩与排名资料，估算这次校排大致对应的省排。"
        if positioning["score"] is None:
            return explanation + "高考参考分数还需对应年份、同一省份科类的一分一段表，先按省排研究学校。"
        return explanation + "参考分数再按注明年份、同一省份科类的一分一段表换算，未把本次校考分数直接当高考分。"
    return None


def build_planning_brief(profile: PlanningProfile, payload: dict, *, research_year: int) -> dict:
    """Produce a fixed planning reference from a confirmed profile and read sources."""
    if type(profile) is not PlanningProfile or payload.get("schema_version") != "1.0":
        raise ValueError("planning brief requires the supported profile and submission schema")
    if payload.get("profile_digest") != profile.digest:
        raise ValueError("brief submission belongs to a different confirmed profile")
    if (payload.get("province"), payload.get("subject_mode"), payload.get("research_year")) != (profile.province, profile.subject_mode, research_year):
        raise ValueError("brief province, subject mode or research year differs from the session")
    if set(payload.get("selection", [])) != {profile.subject_group, *profile.secondary_subjects}:
        raise ValueError("brief subject selection differs from the confirmed profile")
    sources = _Sources(payload.get("sources", []), research_year)
    positioning = _position(profile, payload, sources, research_year)
    groups, alternatives = _candidates(profile, payload, sources, positioning, research_year)
    score, maximum = positioning["exam_score"], positioning["exam_max_score"]
    lines = ["# 多元星途｜本次升学参考规划", "", "## 一、成绩定位", "",
             f"本次考试：{score if score is not None else '未提供'}/{maximum if maximum is not None else '未知满分'}分。"]
    center = positioning["central_rank"]
    if center is not None:
        lo, hi = positioning["rank_bounds"]
        if positioning["score"] is not None:
            year = positioning["reference_year"]
            lines.append(f"按{year}年已公布高考口径作规划参考：**对应高考大致约{positioning['score']}分，折合{profile.province}省排约{center}位**。")
            if positioning["score_bounds"]:
                rank_range = f"{lo}–{hi}位" if lo is not None and hi is not None else "表格尚未覆盖完整范围"
                lines.append(f"分数参考范围：{positioning['score_bounds'][0]}–{positioning['score_bounds'][1]}分；省排参考范围：{rank_range}。")
        else:
            lines.append(f"**折合省排中心参考约{center}位，范围{lo}–{hi}位**；对应分数待同口径一分一段表补齐，院校与路径先按位次推进。")
        lines.append(f"估算依据：{positioning['basis']}。" + " ".join(positioning["citations"]))
        if profile.exam_year != research_year:
            lines.append(f"这是现阶段用于选校和安排准备的历史口径定位，不是对{profile.exam_year}年实际高考结果的保证。")
    elif positioning["score"] is not None:
        lines.append(f"按{positioning['reference_year']}年参照划线折算：**对应高考大致约{positioning['score']}分**，参考范围{positioning['score_bounds'][0]}–{positioning['score_bounds'][1]}分；省排待同口径一分一段表补齐。")
        lines.append(f"估算依据：{positioning['basis']}。" + " ".join(positioning["citations"]))
        lines.append("以下先给有来源的学校目标梯度及路径，待省排补齐后更新个人冲稳保。")
    else:
        lines.append(f"个人高考分数和省排暂缺可比校准：{positioning['basis']}。下面先给有来源的典型学校目标梯度和路径；这些档位不是已测得的个人冲稳保，不把校内裸分直接当高考分。")
    explanation = _position_explanation(positioning)
    if explanation:
        lines.append("**怎样折算**：" + explanation)
    lines += ["", "## 二、本省普通批：冲3所、稳4所、保5所", "",
              "优先匹配已选专业与本省地域；以下档位用于规划，保档也不代表保证录取。"]
    if center is not None and any(item["personal_tier"] for items in groups["ordinary"].values() for item in items):
        lower, upper = positioning["strategy_bounds"]
        lines.append(f"**怎样分档**：位次数越小，通常要求的成绩越高。对有可比历史位次门槛的候选，本次把{lower:g}位至{center:g}位之前列为冲，"
                     f"{center:g}位至{upper:g}位之前列为稳，{upper:g}位及以后列为保；再按地域、专业和已知报考条件筛选。")
    if positioning["method"] in {"official_rank", "official_score"}:
        lines.append("已知高考位次不再估算；分档采用位次上下20%的规划窗口，不表示本人位次有20%误差。")
    lines += _render_groups(groups["ordinary"], counts=ORDINARY_COUNTS, personal_rank=center is not None)
    for numeral, (kind, title) in zip(("三", "四", "五"), PATHWAY_NAMES.items()):
        lines += [f"## {numeral}、{title}"]
        decision = payload.get("pathway_decisions", {}).get(kind, "先保留为准备方向，具体资格和投入顺序按已读项目判断")
        lines += _render_pathway(kind, groups[kind], alternatives[kind], positioning, decision)
    lines += ["## 六、其他路径", ""]
    others = payload.get("other_pathways", [])
    if not others:
        lines.append("专项计划、公费师范/定向培养、军警、艺体和中外合作按画像分别筛选；当前尚未取得支持新增可行项目的材料，先集中准备上面已列方向。")
    for item in others:
        name = _text(item["name"], "other pathway")
        description = _text(item["description"], "other pathway description")
        link = sources.cite(item, (name, description), year=_year(item["year"], research_year))
        lines.append(f"- **{name}**：{description}。本次建议：{_text(item['fit_reason'], 'pathway fit')}。{link}")
    lines += ["", "## 七、现阶段行动", ""]
    actions = payload.get("actions", [])
    if not 1 <= len(actions) <= 5:
        raise ValueError("brief requires one to five concrete current actions")
    lines += [f"{i}. {_text(action, 'action')}。" for i, action in enumerate(actions, 1)]
    lines += ["", DISCLAIMER]
    return {"policy_version": POLICY_VERSION, "profile_digest": profile.digest,
            "positioning": positioning, "ordinary": groups["ordinary"],
            "pathways": {kind: groups[kind] for kind in PATHWAY_NAMES},
            "pathway_alternatives": alternatives,
            "report_text": "\n".join(lines),
            "sources": [{key: source[key] for key in ("source_id", "url", "title", "year")}
                        for sid, source in sources.records.items() if sid in sources.used],
            "delivery": {"mode": "planning_reference", "authenticated_research": False,
                         "personal_positioning": center is not None}}

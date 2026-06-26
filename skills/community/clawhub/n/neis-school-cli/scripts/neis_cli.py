#!/usr/bin/env python3
"""CLI for querying the Korean NEIS OpenAPI for school info, meals, and timetables."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime
from html import unescape
from typing import Any, Callable, Iterable

API_BASE_URL = "https://open.neis.go.kr/hub"
CLI_NAME = "neis-school-cli"
CLI_VERSION = "0.2.1"
SUCCESS_CODE = "INFO-000"
NO_DATA_CODE = "INFO-200"
OUTPUT_TEXT = "text"
OUTPUT_JSON = "json"


class CliError(Exception):
    """Controlled user-facing failure."""

    def __init__(self, message: str, exit_code: int = 1) -> None:
        super().__init__(message)
        self.exit_code = exit_code


@dataclass(frozen=True)
class School:
    office_code: str
    office_name: str
    school_code: str
    school_name: str
    school_kind: str
    location_name: str

    @property
    def school_level(self) -> str:
        if "초등" in self.school_kind:
            return "elementary"
        if "중학" in self.school_kind:
            return "middle"
        if "고등" in self.school_kind:
            return "high"
        raise CliError(f"지원하지 않는 학교급입니다: {self.school_kind}", exit_code=1)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="neis-cli",
        description="학교 검색, 급식, 시간표를 NEIS OpenAPI로 조회합니다.",
    )
    subparsers = parser.add_subparsers(dest="command")

    school_parser = subparsers.add_parser("school", help="학교를 검색합니다.")
    school_subparsers = school_parser.add_subparsers(dest="school_command")
    school_search = school_subparsers.add_parser("search", help="학교명을 검색합니다.")
    school_search.add_argument("school_name", help="검색할 학교명")
    school_search.add_argument("--region", help="지역 또는 교육청 이름으로 후보를 좁힙니다.")
    school_search.add_argument("--json", action="store_true", help="JSON으로 출력합니다.")
    school_search.set_defaults(handler=handle_school_search)

    meal_parser = subparsers.add_parser("meal", help="급식을 조회합니다.")
    add_lookup_arguments(meal_parser)
    meal_parser.add_argument("--date", required=True, help="조회 날짜 (YYYY-MM-DD 또는 YYYYMMDD)")
    meal_parser.set_defaults(handler=handle_meal)

    timetable_parser = subparsers.add_parser("timetable", help="시간표를 조회합니다.")
    add_lookup_arguments(timetable_parser)
    timetable_parser.add_argument("--date", required=True, help="조회 날짜 (YYYY-MM-DD 또는 YYYYMMDD)")
    timetable_parser.add_argument("--grade", required=True, help="학년")
    timetable_parser.add_argument("--classroom", required=True, help="반")
    timetable_parser.set_defaults(handler=handle_timetable)

    return parser


def add_lookup_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--school", required=True, help="학교명")
    parser.add_argument("--region", help="지역 또는 교육청 이름으로 후보를 좁힙니다.")
    parser.add_argument("--json", action="store_true", help="JSON으로 출력합니다.")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not hasattr(args, "handler"):
        parser.print_help()
        return 0

    try:
        return args.handler(args)
    except CliError as exc:
        print(exc, file=sys.stderr)
        return exc.exit_code


def handle_school_search(args: argparse.Namespace) -> int:
    client = NeisClient()
    schools = search_schools(client, args.school_name, args.region)
    payload = json_envelope(
        command="school.search",
        endpoint="schoolInfo",
        query={"school_name": args.school_name, "region": args.region},
        data={"schools": [school_to_dict(item) for item in schools]},
    )
    payload["count"] = len(schools)
    return emit_output(payload, args.json, render_schools)


def handle_meal(args: argparse.Namespace) -> int:
    client = NeisClient(optional_api_key())
    school = resolve_school(client, args.school, args.region)
    day = normalize_date(args.date)
    meals = get_meals(client, school, day)
    payload = json_envelope(
        command="meal.lookup",
        endpoint="mealServiceDietInfo",
        query={"school_name": args.school, "region": args.region, "date": day.isoformat()},
        data={
            "school": school_to_dict(school),
            "date": day.isoformat(),
            "meals": meals,
        },
    )
    payload["count"] = len(meals)
    return emit_output(payload, args.json, render_meals)


def handle_timetable(args: argparse.Namespace) -> int:
    client = NeisClient(optional_api_key())
    school = resolve_school(client, args.school, args.region)
    day = normalize_date(args.date)
    timetable = get_timetable(client, school, day, args.grade, args.classroom)
    endpoint = endpoint_for_school_level(school.school_level)
    payload = json_envelope(
        command="timetable.lookup",
        endpoint=endpoint,
        query={
            "school_name": args.school,
            "region": args.region,
            "date": day.isoformat(),
            "grade": str(args.grade),
            "classroom": str(args.classroom),
        },
        data={
            "school": school_to_dict(school),
            "date": day.isoformat(),
            "grade": str(args.grade),
            "classroom": str(args.classroom),
            "timetable": timetable,
        },
    )
    payload["count"] = len(timetable)
    return emit_output(payload, args.json, render_timetable)


def emit_output(
    payload: dict[str, Any],
    as_json: bool,
    render_text: Callable[[dict[str, Any]], str],
) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(payload))
    return 0


def json_envelope(
    *,
    command: str,
    endpoint: str,
    query: dict[str, Any],
    data: dict[str, Any],
) -> dict[str, Any]:
    return {
        "ok": True,
        "cli": {"name": CLI_NAME, "version": CLI_VERSION},
        "provider": "neis",
        "command": command,
        "endpoint": endpoint,
        "query": query,
        "data": data,
    }


def optional_api_key() -> str | None:
    api_key = os.environ.get("NEIS_API_KEY", "").strip()
    return api_key or None


class NeisClient:
    def __init__(self, api_key: str | None = None, opener: Callable[[str], str] | None = None) -> None:
        self.api_key = api_key
        self._opener = opener or self._default_open

    def fetch(self, endpoint: str, params: dict[str, Any]) -> dict[str, Any]:
        query = {"Type": "json", "pIndex": 1, "pSize": 100}
        query.update({key: value for key, value in params.items() if value is not None and value != ""})
        if self.api_key:
            query["KEY"] = self.api_key
        url = f"{API_BASE_URL}/{endpoint}?{urllib.parse.urlencode(query)}"
        try:
            body = self._opener(url)
        except urllib.error.HTTPError as exc:
            raise CliError(f"NEIS API HTTP 오류: {exc.code}", exit_code=2) from exc
        except urllib.error.URLError as exc:
            raise CliError(f"NEIS API 연결 실패: {exc.reason}", exit_code=2) from exc

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise CliError("NEIS API 응답을 JSON으로 해석하지 못했습니다.", exit_code=2) from exc

    @staticmethod
    def _default_open(url: str) -> str:
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                return response.read().decode("utf-8")
        except urllib.error.URLError as exc:
            # Some local Python runtimes in macOS shells fail DNS resolution even though curl works.
            if not isinstance(exc.reason, OSError):
                raise
            try:
                result = subprocess.run(
                    ["curl", "-fsSL", url],
                    check=True,
                    capture_output=True,
                    text=True,
                )
            except FileNotFoundError as curl_exc:
                raise exc from curl_exc
            except subprocess.CalledProcessError as curl_exc:
                stderr = (curl_exc.stderr or "").strip()
                raise CliError(
                    f"NEIS API 호출 실패(curl): {stderr or '알 수 없는 오류'}",
                    exit_code=2,
                ) from curl_exc
            return result.stdout


def search_schools(client: NeisClient, school_name: str, region: str | None = None) -> list[School]:
    payload = client.fetch("schoolInfo", {"SCHUL_NM": school_name})
    rows = extract_rows(payload, "schoolInfo")
    schools = [school_from_row(row) for row in rows]
    if region:
        schools = [school for school in schools if region_matches(school, region)]
    if not schools:
        raise CliError("검색된 학교가 없습니다.", exit_code=1)
    return schools


def resolve_school(client: NeisClient, school_name: str, region: str | None = None) -> School:
    schools = search_schools(client, school_name, region)
    exact = [school for school in schools if school.school_name == school_name]
    if len(exact) == 1:
        return exact[0]
    if len(schools) == 1:
        return schools[0]
    preview = "\n".join(
        f"- {item.school_name} / {item.location_name} / {item.school_kind} / {item.office_code}:{item.school_code}"
        for item in schools[:10]
    )
    raise CliError(
        "학교명이 여러 개 검색되었습니다. --region을 추가하거나 더 구체적인 학교명을 입력하세요.\n"
        f"{preview}",
        exit_code=1,
    )


def get_meals(client: NeisClient, school: School, day: date) -> list[dict[str, Any]]:
    payload = client.fetch(
        "mealServiceDietInfo",
        {
            "ATPT_OFCDC_SC_CODE": school.office_code,
            "SD_SCHUL_CODE": school.school_code,
            "MLSV_YMD": day.strftime("%Y%m%d"),
        },
    )
    rows = extract_rows(payload, "mealServiceDietInfo")
    return [meal_from_row(row) for row in rows]


def get_timetable(
    client: NeisClient,
    school: School,
    day: date,
    grade: str,
    classroom: str,
) -> list[dict[str, Any]]:
    endpoint = endpoint_for_school_level(school.school_level)
    payload = client.fetch(
        endpoint,
        {
            "ATPT_OFCDC_SC_CODE": school.office_code,
            "SD_SCHUL_CODE": school.school_code,
            "ALL_TI_YMD": day.strftime("%Y%m%d"),
            "GRADE": grade,
            "CLASS_NM": classroom,
        },
    )
    rows = extract_rows(payload, endpoint)
    return [timetable_row_from_api(row) for row in sorted(rows, key=lambda item: int(item.get("PERIO", "0")))]


def extract_rows(payload: dict[str, Any], dataset_name: str) -> list[dict[str, Any]]:
    if "RESULT" in payload:
        result = payload["RESULT"]
        code = result.get("CODE", "")
        if code == NO_DATA_CODE:
            return []
        raise CliError(format_result_message(result), exit_code=2)

    dataset = payload.get(dataset_name)
    if not isinstance(dataset, list) or len(dataset) < 1:
        raise CliError("NEIS API 응답 구조가 예상과 다릅니다.", exit_code=2)

    head = dataset[0].get("head", [])
    result = find_result(head)
    if result:
        code = result.get("CODE", "")
        if code == SUCCESS_CODE:
            pass
        elif code == NO_DATA_CODE:
            return []
        else:
            raise CliError(format_result_message(result), exit_code=2)

    for section in dataset:
        rows = section.get("row")
        if isinstance(rows, list):
            return rows
    return []


def find_result(head_section: Iterable[Any]) -> dict[str, Any] | None:
    for item in head_section:
        if isinstance(item, dict) and "RESULT" in item:
            result = item["RESULT"]
            if isinstance(result, dict):
                return result
    return None


def format_result_message(result: dict[str, Any]) -> str:
    code = result.get("CODE", "UNKNOWN")
    message = result.get("MESSAGE", "알 수 없는 오류")
    return f"NEIS API 오류({code}): {message}"


def normalize_date(value: str) -> date:
    try:
        if "-" in value:
            return datetime.strptime(value, "%Y-%m-%d").date()
        return datetime.strptime(value, "%Y%m%d").date()
    except ValueError as exc:
        raise CliError("날짜 형식은 YYYY-MM-DD 또는 YYYYMMDD여야 합니다.", exit_code=1) from exc


def endpoint_for_school_level(level: str) -> str:
    mapping = {
        "elementary": "elsTimetable",
        "middle": "misTimetable",
        "high": "hisTimetable",
    }
    try:
        return mapping[level]
    except KeyError as exc:
        raise CliError(f"지원하지 않는 학교급입니다: {level}", exit_code=1) from exc


def region_matches(school: School, region: str) -> bool:
    normalized = region.replace(" ", "")
    return normalized in school.location_name.replace(" ", "") or normalized in school.office_name.replace(" ", "")


def school_from_row(row: dict[str, Any]) -> School:
    return School(
        office_code=str(row.get("ATPT_OFCDC_SC_CODE", "")).strip(),
        office_name=str(row.get("ATPT_OFCDC_SC_NM", "")).strip(),
        school_code=str(row.get("SD_SCHUL_CODE", "")).strip(),
        school_name=str(row.get("SCHUL_NM", "")).strip(),
        school_kind=str(row.get("SCHUL_KND_SC_NM", "")).strip(),
        location_name=str(row.get("LCTN_SC_NM", "")).strip(),
    )


def school_to_dict(school: School) -> dict[str, str]:
    return {
        "office_code": school.office_code,
        "office_name": school.office_name,
        "school_code": school.school_code,
        "school_name": school.school_name,
        "school_kind": school.school_kind,
        "school_level": school.school_level,
        "location_name": school.location_name,
    }


def meal_from_row(row: dict[str, Any]) -> dict[str, Any]:
    dishes = split_html_list(row.get("DDISH_NM", ""))
    return {
        "meal_name": str(row.get("MMEAL_SC_NM", "")).strip(),
        "date": format_compact_date(str(row.get("MLSV_YMD", "")).strip()),
        "calories": str(row.get("CAL_INFO", "")).strip(),
        "dishes": dishes,
        "origin_info": split_html_list(row.get("ORPLC_INFO", "")),
        "nutrition_info": split_html_list(row.get("NTR_INFO", "")),
    }


def timetable_row_from_api(row: dict[str, Any]) -> dict[str, str]:
    return {
        "period": str(row.get("PERIO", "")).strip(),
        "subject": str(row.get("ITRT_CNTNT", "")).strip() or "미정",
    }


def split_html_list(value: Any) -> list[str]:
    raw = str(value or "")
    if not raw.strip():
        return []
    parts = raw.replace("<br />", "<br/>").replace("<br>", "<br/>").split("<br/>")
    return [unescape(part).strip() for part in parts if part and part.strip()]


def format_compact_date(value: str) -> str:
    if len(value) == 8 and value.isdigit():
        return f"{value[:4]}-{value[4:6]}-{value[6:]}"
    return value


def render_schools(payload: dict[str, Any]) -> str:
    schools = payload["data"]["schools"]
    lines = [f"검색 결과: {len(schools)}건"]
    for item in schools:
        lines.append(
            f"- {item['school_name']} | {item['location_name']} | {item['school_kind']} | "
            f"{item['office_code']}:{item['school_code']}"
        )
    return "\n".join(lines)


def render_meals(payload: dict[str, Any]) -> str:
    school = payload["data"]["school"]
    meals = payload["data"]["meals"]
    lines = [f"{school['school_name']} ({payload['data']['date']})"]
    if not meals:
        lines.append("조회 결과 없음")
        return "\n".join(lines)
    for meal in meals:
        lines.append(f"[{meal['meal_name']}] {meal['calories']}")
        for dish in meal["dishes"]:
            lines.append(f"- {dish}")
    return "\n".join(lines)


def render_timetable(payload: dict[str, Any]) -> str:
    school = payload["data"]["school"]
    rows = payload["data"]["timetable"]
    lines = [
        f"{school['school_name']} {payload['data']['grade']}학년 {payload['data']['classroom']}반 "
        f"({payload['data']['date']})"
    ]
    if not rows:
        lines.append("조회 결과 없음")
        return "\n".join(lines)
    for row in rows:
        lines.append(f"{row['period']}교시: {row['subject']}")
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field


RemoteMode = Literal["remote", "hybrid", "office", "unknown"]
FitLabel = Literal["strong-match", "possible-match", "skip"]


class Vacancy(BaseModel):
    source: str
    source_url: str | None = None
    company: str | None = None
    title: str | None = None
    stack: list[str] = Field(default_factory=list)
    seniority: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_currency: str | None = None
    gross_or_net: str | None = None
    location: str | None = None
    remote_mode: RemoteMode = "unknown"
    employment_type: str | None = None
    visa_or_relocation: str | None = None
    english_level: str | None = None
    contact_name: str | None = None
    contact_url: str | None = None
    summary: str | None = None
    fit_score: int | None = None
    fit_label: FitLabel | None = None
    fit_reasons: list[str] = Field(default_factory=list)
    red_flags: list[str] = Field(default_factory=list)
    status: str | None = None
    raw_text: str | None = None


RU_MONTH = re.compile(r"(руб|₽|р\b|руб\.)", re.I)
USD_MONTH = re.compile(r"(usd|\$|долл)", re.I)
K_SUFFIX = re.compile(r"(\d+(?:[.,]\d+)?)\s*k\b", re.I)
RANGE_RE = re.compile(r"(?P<a>\d[\d\s.,]*)\s*(?:[-–—]|to|до)\s*(?P<b>\d[\d\s.,]*)", re.I)
SINGLE_RE = re.compile(r"(?P<a>\d[\d\s.,]*)")


KNOWN_STACK = [
    "python", "java", "kotlin", "go", "golang", "javascript", "typescript", "react", "vue",
    "angular", "node", "node.js", "django", "flask", "fastapi", "spring", "postgresql",
    "mysql", "redis", "kafka", "docker", "kubernetes", "aws", "gcp", "linux", "c#", ".net",
    "php", "laravel", "1c", "rust", "scala", "clickhouse", "airflow", "gitlab", "ci/cd",
]


SENIORITY_MAP = {
    "junior": "junior",
    "middle": "middle",
    "mid": "middle",
    "senior": "senior",
    "lead": "lead",
    "staff": "staff",
    "principal": "principal",
}


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def read_json(path: str) -> Any:
    return json.loads(read_text(path))


def dump_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def clean_num(s: str) -> int:
    s = s.replace(" ", "").replace(",", ".")
    return int(float(s))


def normalize_currency(text: str) -> str | None:
    if RU_MONTH.search(text):
        return "RUB"
    if USD_MONTH.search(text):
        return "USD"
    return None


def normalize_remote_mode(text: str) -> RemoteMode:
    t = text.lower()
    if any(x in t for x in ["удален", "remote", "дистанц"]):
        return "remote"
    if any(x in t for x in ["гибрид", "hybrid"]):
        return "hybrid"
    if any(x in t for x in ["офис", "office", "on-site", "onsite"]):
        return "office"
    return "unknown"


def normalize_seniority(text: str) -> str | None:
    t = text.lower()
    for key, value in SENIORITY_MAP.items():
        if key in t:
            return value
    return None


def extract_stack(text: str) -> list[str]:
    t = text.lower()
    found = []
    for item in KNOWN_STACK:
        if item in t:
            canonical = "Node.js" if item == "node.js" else item
            found.append(canonical)
    return sorted(dict.fromkeys(found), key=str.lower)


def normalize_salary_text(text: str) -> dict[str, Any]:
    t = text.strip()
    t = K_SUFFIX.sub(lambda m: str(float(m.group(1).replace(',', '.')) * 1000), t)
    currency = normalize_currency(t)
    gross_or_net = None
    low = high = None

    if "gross" in t.lower() or "до вычета" in t.lower() or "гряз" in t.lower():
        gross_or_net = "gross"
    elif "net" in t.lower() or "на руки" in t.lower() or "чист" in t.lower():
        gross_or_net = "net"

    m = RANGE_RE.search(t)
    if m:
        low = clean_num(m.group("a"))
        high = clean_num(m.group("b"))
    else:
        m = SINGLE_RE.search(t)
        if m:
            low = clean_num(m.group("a"))
            high = low

    return {
        "salary_min": low,
        "salary_max": high,
        "salary_currency": currency,
        "gross_or_net": gross_or_net,
    }


def vacancy_key(v: Vacancy) -> str:
    company = (v.company or "").strip().lower()
    title = (v.title or "").strip().lower()
    return f"{company}::{title}"

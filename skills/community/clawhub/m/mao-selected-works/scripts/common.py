#!/usr/bin/env python3

from __future__ import annotations

import json
import math
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = ROOT / "config" / "search.json"
EXAMPLE_CONFIG_PATH = ROOT / "config" / "search.example.json"
LOCAL_ENV_PATH = ROOT / ".env.local"


def load_local_env(path: Path = LOCAL_ENV_PATH) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_local_env()


@dataclass
class DocumentRecord:
    source_path: str
    volume: str | None
    volume_no: int | None
    article_no: int | None
    article_title: str
    aliases: list[str]
    date: str | None
    content: str


def slugify(text: str, fallback: str = "item") -> str:
    normalized = re.sub(r"\s+", "-", text.strip().lower())
    normalized = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "-", normalized)
    normalized = re.sub(r"-{2,}", "-", normalized).strip("-")
    return normalized or fallback


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_config(path: Path | None = None) -> dict[str, Any]:
    target = path or DEFAULT_CONFIG_PATH
    if target.exists():
        return load_json(target)
    return load_json(EXAMPLE_CONFIG_PATH)


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text

    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text

    raw = text[4:end].splitlines()
    body = text[end + 5 :]
    data: dict[str, Any] = {}
    current_key: str | None = None

    for line in raw:
        if not line.strip():
            continue
        if re.match(r"^[A-Za-z0-9_-]+:\s*", line):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                data[key] = _normalize_scalar(value)
                current_key = None
            else:
                data[key] = []
                current_key = key
            continue
        if current_key and line.lstrip().startswith("- "):
            data[current_key].append(_normalize_scalar(line.split("- ", 1)[1].strip()))
            continue
        current_key = None

    return data, body.lstrip()


def _normalize_scalar(value: str) -> str:
    value = value.strip()
    if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
        return value[1:-1]
    return value


def first_heading(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return None


def infer_volume(text: str, metadata: dict[str, Any]) -> str | None:
    if metadata.get("volume"):
        normalized = normalize_volume_label(str(metadata["volume"]).strip())
        return normalized or str(metadata["volume"]).strip()
    match = re.search(r"第[一二三四五六七八九十百0-9]+卷", text)
    if match:
        return match.group(0)
    return None


def chinese_numeral_to_int(text: str) -> int | None:
    digits = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
    units = {"十": 10, "百": 100}
    if not text:
        return None
    if text.isdigit():
        return int(text)
    total = 0
    current = 0
    for char in text:
        if char in digits:
            current = digits[char]
            continue
        unit = units.get(char)
        if unit is None:
            return None
        if current == 0:
            current = 1
        total += current * unit
        current = 0
    return total + current


def normalize_volume_label(value: str | None) -> str | None:
    if not value:
        return None
    text = str(value).strip()
    if not text:
        return None
    match = re.search(r"第([一二三四五六七八九十百0-9]+)卷", text)
    if match:
        number = chinese_numeral_to_int(match.group(1))
        if number is not None:
            return f"第{int_to_chinese(number)}卷"
        return text
    if text.isdigit():
        return f"第{int_to_chinese(int(text))}卷"
    number = chinese_numeral_to_int(text)
    if number is not None:
        return f"第{int_to_chinese(number)}卷"
    return text


def int_to_chinese(value: int) -> str:
    digits = "零一二三四五六七八九"
    if value < 10:
        return digits[value]
    if value < 20:
        return "十" + (digits[value % 10] if value % 10 else "")
    if value < 100:
        tens, ones = divmod(value, 10)
        return digits[tens] + "十" + (digits[ones] if ones else "")
    hundreds, remainder = divmod(value, 100)
    if remainder == 0:
        return digits[hundreds] + "百"
    if remainder < 10:
        return digits[hundreds] + "百零" + digits[remainder]
    return digits[hundreds] + "百" + int_to_chinese(remainder)


def infer_volume_number(metadata: dict[str, Any], source_name: str, text: str = "") -> int | None:
    if metadata.get("volume_no") is not None:
        try:
            return int(str(metadata["volume_no"]).strip())
        except ValueError:
            return None
    if metadata.get("volume"):
        normalized = normalize_volume_label(str(metadata["volume"]).strip())
        if normalized:
            match = re.search(r"第([一二三四五六七八九十百0-9]+)卷", normalized)
            if match:
                return chinese_numeral_to_int(match.group(1))
    match = re.match(r"^(\d{2})-(\d{2})-", source_name)
    if match:
        return int(match.group(1))
    match = re.search(r"第([一二三四五六七八九十百0-9]+)卷", text)
    if match:
        return chinese_numeral_to_int(match.group(1))
    return None


def infer_article_number(metadata: dict[str, Any], source_name: str) -> int | None:
    if metadata.get("article_no") is not None:
        try:
            return int(str(metadata["article_no"]).strip())
        except ValueError:
            return None
    match = re.match(r"^(\d{2})-(\d{2})-", source_name)
    if match:
        return int(match.group(2))
    return None


def infer_article_title(text: str, metadata: dict[str, Any], source_name: str) -> str:
    if metadata.get("article_title"):
        return str(metadata["article_title"]).strip()
    heading = first_heading(text)
    if heading:
        return heading
    return Path(source_name).stem


def normalize_aliases(metadata: dict[str, Any]) -> list[str]:
    raw = metadata.get("aliases", [])
    if isinstance(raw, list):
        values = [str(item).strip() for item in raw if str(item).strip()]
    elif isinstance(raw, str) and raw.strip():
        values = [raw.strip()]
    else:
        values = []
    seen: set[str] = set()
    aliases: list[str] = []
    for value in values:
        if value not in seen:
            aliases.append(value)
            seen.add(value)
    return aliases


def split_paragraphs(text: str) -> list[str]:
    text = re.sub(r"\r\n?", "\n", text)
    chunks = re.split(r"\n\s*\n", text)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def chunk_paragraphs(paragraphs: list[str], chunk_size: int, chunk_overlap: int) -> list[str]:
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = paragraph if not current else current + "\n\n" + paragraph
        if len(candidate) <= chunk_size:
            current = candidate
            continue
        if current:
            chunks.append(current)
        if len(paragraph) <= chunk_size:
            overlap = current[-chunk_overlap:] if current and chunk_overlap > 0 else ""
            current = (overlap + "\n\n" + paragraph).strip() if overlap else paragraph
            if len(current) > chunk_size:
                current = paragraph
            continue
        chunks.extend(_split_long_text(paragraph, chunk_size, chunk_overlap))
        current = ""

    if current:
        chunks.append(current)
    return chunks


def _split_long_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    pieces: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + chunk_size)
        pieces.append(text[start:end].strip())
        if end == len(text):
            break
        start = max(start + 1, end - chunk_overlap)
    return [piece for piece in pieces if piece]


def relative_to_root(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    numerator = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if not norm_a or not norm_b:
        return 0.0
    return numerator / (norm_a * norm_b)


def http_json(url: str, payload: dict[str, Any], api_key: str | None = None) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTP {exc.code} calling {url}: {detail}") from exc


def resolve_service_config(config: dict[str, Any], section: str) -> dict[str, Any]:
    rag_cfg = config.get("rag", {})
    api_cfg = rag_cfg.get("api", {})
    service_cfg = dict(rag_cfg.get(section, {}))

    if not service_cfg.get("base_url") and api_cfg.get("base_url"):
        service_cfg["base_url"] = api_cfg["base_url"]
    if not service_cfg.get("provider") and api_cfg.get("provider"):
        service_cfg["provider"] = api_cfg["provider"]

    api_key_env = service_cfg.get("api_key_env") or api_cfg.get("api_key_env")
    if api_key_env:
        service_cfg["api_key_env"] = str(api_key_env)
        service_cfg["api_key"] = os.environ.get(str(api_key_env), "")
    elif service_cfg.get("api_key"):
        pass
    elif api_cfg.get("api_key"):
        service_cfg["api_key"] = os.environ.get(str(api_cfg["api_key"]), "")

    return service_cfg


def embed_texts(texts: list[str], config: dict[str, Any]) -> list[list[float]]:
    embedding_cfg = resolve_service_config(config, "embedding")
    base_url = str(embedding_cfg.get("base_url", "")).rstrip("/")
    model = embedding_cfg.get("model")
    api_key = embedding_cfg.get("api_key")
    batch_size = int(embedding_cfg.get("batch_size") or config.get("embedding_batch_size", 64))
    if not base_url or not model:
        raise RuntimeError("Embedding configuration is incomplete.")
    if batch_size <= 0:
        batch_size = 64
    vectors: list[list[float]] = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        response = http_json(
            f"{base_url}/embeddings",
            {"input": batch, "model": model},
            api_key=api_key,
        )
        data = response.get("data", [])
        for item in data:
            vectors.append([float(value) for value in item.get("embedding", [])])
    return vectors


def rerank_documents(query: str, documents: list[str], config: dict[str, Any], top_n: int) -> list[dict[str, Any]]:
    rerank_cfg = resolve_service_config(config, "rerank")
    base_url = str(rerank_cfg.get("base_url", "")).rstrip("/")
    model = rerank_cfg.get("model")
    api_key = rerank_cfg.get("api_key")
    if not base_url or not model:
        raise RuntimeError("Rerank configuration is incomplete.")
    response = http_json(
        f"{base_url}/rerank",
        {
            "model": model,
            "query": query,
            "documents": documents,
            "top_n": top_n,
        },
        api_key=api_key,
    )
    results = response.get("results") or response.get("data") or []
    normalized: list[dict[str, Any]] = []
    for item in results:
        document_info = item.get("document") or {}
        index = int(item.get("index", document_info.get("index", -1)))
        score = item.get("relevance_score", item.get("score", 0.0))
        if index >= 0:
            normalized.append({"index": index, "score": float(score)})
    return normalized

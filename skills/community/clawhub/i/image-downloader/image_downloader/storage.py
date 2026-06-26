import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


def normalize_url_for_index(url):
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def _index_path(output_dir):
    return Path(output_dir) / "index.json"


def _metadata_path(output_dir):
    return Path(output_dir) / "metadata.json"


def load_index(output_dir):
    index_path = _index_path(output_dir)
    if not index_path.exists():
        return {"by_normalized_url": {}, "by_sha256": {}}

    return json.loads(index_path.read_text(encoding="utf-8"))


def save_index(output_dir, index):
    index_path = _index_path(output_dir)
    index_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_metadata(output_dir):
    metadata_path = _metadata_path(output_dir)
    if not metadata_path.exists():
        return []

    return json.loads(metadata_path.read_text(encoding="utf-8"))


def save_metadata(output_dir, metadata):
    metadata_path = _metadata_path(output_dir)
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def compute_file_hash(file_path):
    digest = hashlib.sha256()
    with Path(file_path).open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(8192), b""):
            if chunk:
                digest.update(chunk)
    return digest.hexdigest()


def record_download(candidate, image_path, output_dir):
    output_dir = Path(output_dir)
    image_path = Path(image_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    index = load_index(output_dir)
    metadata = load_metadata(output_dir)
    normalized_url = normalize_url_for_index(candidate.image_url)
    sha256 = compute_file_hash(image_path)

    record = {
        "source": candidate.source,
        "keyword": candidate.keyword,
        "image_url": candidate.image_url,
        "normalized_image_url": normalized_url,
        "page_url": candidate.page_url,
        "thumbnail_url": candidate.thumbnail_url,
        "title": candidate.title,
        "width": candidate.width,
        "height": candidate.height,
        "content_type": candidate.content_type,
        "source_rank": candidate.source_rank,
        "metadata": candidate.metadata,
        "file_name": image_path.name,
        "file_path": str(image_path),
        "sha256": sha256,
    }

    metadata.append(record)
    index["by_normalized_url"][normalized_url] = record["file_name"]
    index["by_sha256"][sha256] = record["file_name"]

    save_metadata(output_dir, metadata)
    save_index(output_dir, index)
    return record


def should_skip_candidate(candidate, output_dir):
    normalized_url = normalize_url_for_index(candidate.image_url)
    index = load_index(output_dir)
    return normalized_url in index["by_normalized_url"]

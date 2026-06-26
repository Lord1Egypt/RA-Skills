import argparse
import mimetypes
import os
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from image_downloader.reporting import build_run_report
from image_downloader.storage import record_download, should_skip_candidate
from image_downloader.sources.bing import BingSource, HEADERS, extract_image_urls
from image_downloader.sources.demo import DemoSource


SOURCE_REGISTRY = {
    "bing": BingSource,
    "demo": DemoSource,
}


def guess_extension(url, content_type=None):
    if content_type:
        extension = mimetypes.guess_extension(content_type.split(";")[0].strip())
        if extension == ".jpe":
            return ".jpg"
        if extension:
            return extension

    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"):
        if path.endswith(ext):
            return ".jpg" if ext == ".jpeg" else ext
    return ".jpg"


def download_images(urls, output_dir, limit=10, start_index=1):
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    saved_files = []

    for offset, url in enumerate(urls[:limit]):
        response = requests.get(url, headers=HEADERS, stream=True, timeout=15)
        response.raise_for_status()
        extension = guess_extension(url, response.headers.get("Content-Type"))
        filename = f"{start_index + offset:03d}{extension}"
        file_path = os.path.join(output_dir, filename)

        with open(file_path, "wb") as file_obj:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file_obj.write(chunk)

        saved_files.append(file_path)

    return saved_files


def get_next_image_index(output_dir):
    output_path = Path(output_dir)
    max_index = 0

    if not output_path.exists():
        return 1

    for child in output_path.iterdir():
        if not child.is_file():
            continue
        stem = child.stem
        if stem.isdigit():
            max_index = max(max_index, int(stem))

    return max_index + 1


def download_new_images(candidates, output_dir, limit, start_index):
    downloaded_count = 0
    skipped_count = 0
    next_index = start_index

    for candidate in candidates:
        if downloaded_count >= limit:
            break
        saved_path = download_candidate(candidate, output_dir, next_index)
        if saved_path:
            downloaded_count += 1
            next_index += 1
        else:
            skipped_count += 1

    return downloaded_count, skipped_count


def build_sources(source_names):
    return [SOURCE_REGISTRY[name]() for name in source_names]


def collect_candidates_from_sources(keyword, limit, pages, sources):
    candidates = []
    for source in sources:
        candidates.extend(source.collect(keyword, limit=limit, pages=pages))
    return candidates


def dedupe_candidates(candidates, limit):
    seen_urls = set()
    deduped = []

    for candidate in candidates:
        if candidate.image_url in seen_urls:
            continue
        seen_urls.add(candidate.image_url)
        deduped.append(candidate)
        if len(deduped) >= limit:
            break

    return deduped


def download_candidate(candidate, output_dir, index):
    if should_skip_candidate(candidate, output_dir):
        return None

    saved_files = download_images([candidate.image_url], output_dir, limit=1, start_index=index)
    if not saved_files:
        return None

    record_download(candidate, saved_files[0], output_dir)
    return saved_files[0]


def collect_image_urls(keyword, pages=1, target_count=None):
    source = BingSource()
    limit = target_count if target_count is not None else pages * 35
    candidates = source.collect(keyword, limit=limit, pages=pages)
    return [candidate.image_url for candidate in candidates]


def search_bing_images(keyword):
    return collect_image_urls(keyword, pages=1)


def main():
    parser = argparse.ArgumentParser(description="按关键词从 Bing 公开图片中下载图片")
    parser.add_argument("keyword", help="搜索关键词，例如 cat")
    parser.add_argument("--limit", type=int, default=10, help="下载数量，默认 10")
    parser.add_argument("--pages", type=int, default=5, help="最多抓取的 Bing 结果页数，默认 5")
    args = parser.parse_args()

    output_dir = os.path.join("downloads", args.keyword)
    sources = build_sources(["bing", "demo"])
    collected_candidates = collect_candidates_from_sources(
        keyword=args.keyword,
        limit=args.limit,
        pages=args.pages,
        sources=sources,
    )

    if not collected_candidates:
        print("没有提取到图片链接，请更换关键词后重试。")
        return

    unique_candidates = dedupe_candidates(collected_candidates, limit=len(collected_candidates))
    start_index = get_next_image_index(output_dir)
    downloaded_count = 0
    skipped_count = 0

    for candidate in unique_candidates:
        if downloaded_count >= args.limit:
            break
        try:
            saved_path = download_candidate(candidate, output_dir, start_index + downloaded_count)
            if saved_path:
                downloaded_count += 1
            else:
                skipped_count += 1
        except Exception as exc:
            skipped_count += 1
            print(f"下载失败: {candidate.image_url} -> {exc}")

    source_counts = dict(Counter(candidate.source for candidate in collected_candidates))
    report = build_run_report(
        keyword=args.keyword,
        requested_limit=args.limit,
        collected_count=len(collected_candidates),
        deduped_count=len(unique_candidates),
        downloaded_count=downloaded_count,
        skipped_count=skipped_count,
        output_dir=output_dir,
        source_counts=source_counts,
    )
    print(report)


if __name__ == "__main__":
    main()

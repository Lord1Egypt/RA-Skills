#!/usr/bin/env python3
"""从 linkfox-amazon-product-detail 落盘 JSON 提取爆款复刻参考图 URL。

合并 productImageUrls（主图+附图）与 productDescription 内嵌的 A+ 图 JSON。
解析逻辑与 agent-listing-result-html-skill/scripts/build-data-json.py 对齐。

用法:
    python extract_reference_images.py <detail-json路径> [--main-only]

输出 (stdout，一行 JSON):
    {
      "reference_images": ["https://...", ...],
      "main_count": 7,
      "aplus_count": 7,
      "include_aplus": true
    }
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any


def _normalize_url(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    url = value.strip()
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return None


def _parse_aplus_urls(product_description: Any) -> list[str]:
    """从 productDescription 字符串解析 A+ 图 URL，按 position 排序。"""
    if not isinstance(product_description, str) or not product_description.strip():
        return []

    try:
        pd_list = json.loads(product_description)
    except (json.JSONDecodeError, TypeError):
        return []

    if not isinstance(pd_list, list):
        return []

    items: list[tuple[int, str]] = []
    for idx, item in enumerate(pd_list):
        if not isinstance(item, dict):
            continue
        position = item.get("position")
        sort_key = position if isinstance(position, int) else idx

        image = _normalize_url(item.get("image"))
        if image:
            items.append((sort_key, image))

        carousel = item.get("carouselImages")
        if isinstance(carousel, list):
            for cidx, ci in enumerate(carousel):
                if not isinstance(ci, dict):
                    continue
                cpos = ci.get("position")
                csort = cpos if isinstance(cpos, int) else sort_key * 1000 + cidx
                cimage = _normalize_url(ci.get("image"))
                if cimage:
                    items.append((csort, cimage))

    items.sort(key=lambda pair: pair[0])
    seen: set[str] = set()
    urls: list[str] = []
    for _, url in items:
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def extract_reference_images(product: dict | None, *, include_aplus: bool = True) -> dict[str, Any]:
    p = product or {}
    seen: set[str] = set()
    main_urls: list[str] = []

    for raw in p.get("productImageUrls") or []:
        url = _normalize_url(raw)
        if url and url not in seen:
            seen.add(url)
            main_urls.append(url)

    aplus_urls: list[str] = []
    if include_aplus:
        for url in _parse_aplus_urls(p.get("productDescription")):
            if url not in seen:
                seen.add(url)
                aplus_urls.append(url)

    return {
        "reference_images": main_urls + aplus_urls,
        "main_count": len(main_urls),
        "aplus_count": len(aplus_urls),
        "include_aplus": include_aplus,
    }


def _load_product(json_path: str) -> dict[str, Any]:
    with open(json_path, encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("detail JSON 顶层必须是 object")
    products = data.get("products") or []
    if not products:
        return {}
    first = products[0]
    if not isinstance(first, dict):
        raise ValueError("products[0] 必须是 object")
    return first


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract listing reference images for bestseller replicate")
    parser.add_argument("json_path", help="linkfox-amazon-product-detail 落盘 JSON 路径")
    parser.add_argument(
        "--main-only",
        action="store_true",
        help="仅取 productImageUrls（主图+附图），不解析 productDescription 中的 A+ 图",
    )
    args = parser.parse_args()

    try:
        product = _load_product(args.json_path)
        result = extract_reference_images(product, include_aplus=not args.main_only)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()

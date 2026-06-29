#!/usr/bin/env python3
"""
Summarize defaults from plan-pack-resource-list JSON.

Usage:
  mws link plan-pack-resource-list --env ${MWS_ENV} --params '{"resourceType":"song","resourceIds":"108485"}' --format json \
    | python3 scripts/resource_defaults.py
"""
import json
import sys


def load_items():
    raw = sys.stdin.read().strip()
    if not raw:
        raise SystemExit("stdin is empty; pass plan-pack-resource-list JSON")
    payload = json.loads(raw)
    data = payload.get("data", payload) if isinstance(payload, dict) else payload
    if not isinstance(data, list) or not data:
        return []
    return data


def first_non_empty(*values):
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def is_http_url(value):
    text = str(value or "").strip()
    return text.startswith("http://") or text.startswith("https://")


def first_http_url(*values):
    for value in values:
        text = str(value or "").strip()
        if is_http_url(text):
            return text
    return ""


def summarize(item):
    composed = item.get("composedData") or {}
    common = composed.get("commonComposedData") or {}
    common_url = common.get("url")
    orpheus = item.get("orpheus")
    pc_url = item.get("pcUrl")
    producer_names = item.get("producerNames") or []
    producer = first_non_empty(
        "、".join(str(x) for x in producer_names if x),
        item.get("producerName"),
    )
    client_default_url = first_non_empty(common_url, orpheus)
    web_default_url = first_http_url(pc_url, common_url)
    client_warning = ""
    if not client_default_url:
        client_warning = "非 Web 默认跳转链接缺失：标准资源不能手拼 Web/PC 链接给移动端、PC、Mac、iPad 等端，请从 data-template-extract-private 的 preData/资源默认值中获取，或让用户提供明确的端维度链接。"
    web_warning = ""
    if not web_default_url:
        web_warning = "Web 默认跳转链接缺失：Web 端必须使用 http/https 链接，不能退化使用 orpheus，请让用户手工提供 Web 链接。"
    return {
        "exists": True,
        "resourceId": first_non_empty(item.get("resourceId"), common.get("id")),
        "resourceType": first_non_empty(item.get("resourceType")),
        "name": first_non_empty(item.get("name")),
        "producerName": producer,
        "defaultUrl": client_default_url,
        "clientDefaultUrl": client_default_url,
        "clientDefaultUrlMissing": not bool(client_default_url),
        "clientDefaultUrlWarning": client_warning,
        "webDefaultUrl": web_default_url,
        "webDefaultUrlMissing": not bool(web_default_url),
        "webDefaultUrlWarning": web_warning,
        "defaultBannerLabel": first_non_empty(common.get("bannerLabel")),
        "pcUrl": first_non_empty(pc_url),
        "orpheus": first_non_empty(orpheus, common_url),
    }


def main():
    items = load_items()
    if not items:
        warning = "资源可能不存在或未上线，无法取资源默认角标/跳转链接。用户确认仍要配置时，可以手工提供角标、跳转链接和素材后继续。"
        print(json.dumps({"exists": False, "warning": warning}, ensure_ascii=False, indent=2))
        print("")
        print(warning)
        return

    for item in items:
        summary = summarize(item)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        print("")
        if summary["name"] or summary["producerName"]:
            print("资源：{}{}".format(
                summary["name"] or summary["resourceId"],
                "，{}".format(summary["producerName"]) if summary["producerName"] else "",
            ))
        if summary["clientDefaultUrl"]:
            print("非 Web 默认跳转链接：{}".format(summary["clientDefaultUrl"]))
        elif summary["clientDefaultUrlWarning"]:
            print(summary["clientDefaultUrlWarning"])
        if summary["webDefaultUrl"]:
            print("Web 默认跳转链接：{}".format(summary["webDefaultUrl"]))
        elif summary["webDefaultUrlWarning"]:
            print(summary["webDefaultUrlWarning"])
        if summary["defaultBannerLabel"]:
            print("默认角标：{}".format(summary["defaultBannerLabel"]))


if __name__ == "__main__":
    main()

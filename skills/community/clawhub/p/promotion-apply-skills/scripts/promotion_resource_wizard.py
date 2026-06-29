#!/usr/bin/env python3
"""
Prepare promotion creative resource selection from promotion-detail JSON.

Usage:
  mws link promotion-detail --env ${MWS_ENV} --params '{"id":"1200000577803"}' --format json \
    | python3 promotion_resource_wizard.py choices

  mws link promotion-detail --env ${MWS_ENV} --params '{"id":"1200000577803"}' --format json \
    | python3 promotion_resource_wizard.py infer --resource-id 111

  mws link promotion-detail --env ${MWS_ENV} --params '{"id":"1200000577803"}' --format json \
    | python3 promotion_resource_wizard.py select --first standard --second song --resource-id 111

  # Direct update/material replacement should require the standard resource ID before template extraction.
  mws link promotion-detail --env ${MWS_ENV} --params '{"id":"1200000577803"}' --format json \
    | python3 promotion_resource_wizard.py select --first standard --second song --resource-id 111 --require-resource-id

This script is intentionally standalone so the skill can run without the H5 repo.
"""
import argparse
import json
import sys


POSITION_CONFIG = {
    "移动端(iPhone&Android)": {
        "positionCode": "PAGE_DISCOVERY_BANNER@mobile",
        "channelCode": "page_discovery_banner_channel",
    },
    "荣耀白牌": {
        "positionCode": "PAGE_DISCOVERY_BANNER@magios",
        "channelCode": "page_discovery_banner_channel_magios",
    },
    "PC": {
        "positionCode": "BANNER_PC_V2",
        "channelCode": "pc_banner_op_channel",
    },
    "Web": {
        "positionCode": "BANNER_WEB",
        "channelCode": "web_banner_op_channel",
    },
    "Mac": {
        "positionCode": "BANNER_MAC",
        "channelCode": "mac_banner_op_channel",
    },
    "iPad(新版)": {
        "positionCode": "PAGE_DISCOVERY_BANNER@newIpad",
        "channelCode": "page_discovery_banner_channel_new_ipad",
    },
    "AndroidPad": {
        "positionCode": "PAGE_DISCOVERY_BANNER@androidPad",
        "channelCode": "page_discovery_banner_channel_android_pad",
    },
    "iPadHD(旧版)": {
        "positionCode": "BANNER_IPAD_HD",
        "channelCode": "ipad_hd_banner_op_channel",
    },
}

DELIVERY_RESOURCE_CANDIDATES = {
    "mv": [("standard", "mv")],
    "album": [("standard", "album")],
    "专辑": [("standard", "album")],
    "digitalalbum": [("standard", "digitalAlbum"), ("standard", "digital_album")],
    "数字专辑": [("standard", "digitalAlbum"), ("standard", "digital_album")],
    "playlist": [("standard", "playlist"), ("standard", "songlist")],
    "歌单": [("standard", "playlist"), ("standard", "songlist")],
    "song": [("standard", "song")],
    "single": [("standard", "song")],
    "单曲": [("standard", "song")],
    "longaudio": [("standard", "longAudio"), ("standard", "audio")],
    "长音频": [("standard", "longAudio"), ("standard", "audio")],
    "live": [("standard", "live")],
    "直播": [("standard", "live")],
    "h5": [("nonstandard", "activity")],
    "other": [("nonstandard", "activity")],
    "其他": [("nonstandard", "activity")],
}


def load_json_from_stdin():
    raw = sys.stdin.read().strip()
    if not raw:
        raise SystemExit("stdin is empty; pass promotion-detail JSON")
    data = json.loads(raw)
    if isinstance(data, dict) and "data" in data and isinstance(data["data"], dict):
        return data["data"]
    return data


def delivery_options(detail):
    result = []
    for top in detail.get("deliveryResourceList") or []:
        top_code = top.get("code") or top.get("type")
        top_desc = top.get("desc") or top_code
        for sub in top.get("subResources") or []:
            sub_code = sub.get("code") or sub.get("type")
            sub_desc = sub.get("desc") or sub_code
            result.append(
                {
                    "first": top_code,
                    "firstName": top_desc,
                    "second": sub_code,
                    "secondName": sub_desc,
                    "needResourceId": top_code == "standard",
                }
            )
    return result


def find_option(detail, first, second):
    for option in delivery_options(detail):
        if option["first"] == first and option["second"] == second:
            return option
    return None


def delivery_resource_keys(detail):
    values = [
        detail.get("deliveryResource"),
        detail.get("deliveryResourceName"),
        detail.get("deliveryResourceDesc"),
    ]
    keys = []
    for value in values:
        if value is None:
            continue
        text = str(value).strip()
        if not text:
            continue
        keys.append(text)
        keys.append(text.lower())
    return keys


def infer_option(detail):
    resource_types = detail.get("resourceTypes") or []
    if resource_types and isinstance(resource_types, list) and resource_types[0]:
        first, second = resource_types[0][0], resource_types[0][1]
        option = find_option(detail, first, second)
        if option:
            return option, "detail.resourceTypes"

    for key in delivery_resource_keys(detail):
        for first, second in DELIVERY_RESOURCE_CANDIDATES.get(key, []):
            option = find_option(detail, first, second)
            if option:
                return option, "deliveryResource={}".format(key)
    return None, ""


def selected_aliases(detail):
    aliases = detail.get("positionAliasList") or []
    if aliases:
        return aliases
    codes = (detail.get("relatedPositionCodes") or "").split(",")
    code_to_alias = {v["positionCode"]: k for k, v in POSITION_CONFIG.items()}
    return [code_to_alias[c] for c in codes if c in code_to_alias]


def print_choices(detail):
    current_types = detail.get("resourceTypes") or []
    current_resource_info = detail.get("resourceInfo") or ""
    print("当前推广：{} ({})".format(detail.get("name", ""), detail.get("id", "")))
    print("当前投放端：{}".format("、".join(selected_aliases(detail)) or "未选择"))
    if current_types:
        print("当前已选投放资源：{}".format(json.dumps(current_types, ensure_ascii=False)))
        if current_resource_info:
            print("当前资源 ID：{}".format(current_resource_info))
    else:
        print("当前还没有选择投放资源，需要先让用户选择。")
    print("")
    print("可选投放资源：")
    for idx, option in enumerate(delivery_options(detail), 1):
        suffix = "，需要资源 ID" if option["needResourceId"] else "，通常不需要资源 ID"
        print(
            "{}. {} / {}（{} / {}）{}".format(
                idx,
                option["firstName"],
                option["secondName"],
                option["first"],
                option["second"],
                suffix,
            )
        )
    print("")
    print("选择后运行示例：")
    print("python3 scripts/promotion_resource_wizard.py select --first standard --second song --resource-id 111")
    print("python3 scripts/promotion_resource_wizard.py select --first nonstandard --second activity")


def print_select(detail, args):
    option = find_option(detail, args.first, args.second)
    if not option:
        raise SystemExit("投放资源不在当前推广可选列表中：{} / {}".format(args.first, args.second))
    if args.require_resource_id and option["needResourceId"] and not args.resource_id:
        raise SystemExit("标准资源必须先提供资源 ID，才能校验默认值、提取模板并继续素材交互。")
    aliases = selected_aliases(detail)
    missing_aliases = [a for a in aliases if a not in POSITION_CONFIG]
    if missing_aliases:
        raise SystemExit("以下投放端没有本地配置：{}".format("、".join(missing_aliases)))

    resource_info = args.resource_id or ""
    normalized = {
        "promotionId": detail.get("id"),
        "promotionName": detail.get("name"),
        "resourceTypePair": [args.first, args.second],
        "resourceType": args.second,
        "resourceTypes": [[args.first, args.second]],
        "resourceInfo": resource_info,
        "selectedAliases": aliases,
        "saveAliases": save_aliases(aliases),
    }
    print("已选择投放资源：{} / {}".format(option["firstName"], option["secondName"]))
    if resource_info:
        print("资源 ID：{}".format(resource_info))
    elif option["needResourceId"]:
        print("资源 ID：未提供。可以先提取模板；创建推广和最终保存前仍需补资源 ID。")
    print("")
    print("标准化结构：")
    print(json.dumps(normalized, ensure_ascii=False, indent=2))
    print("")

    if option["needResourceId"] and resource_info:
        print("先校验标准资源：")
        print(
            "mws link plan-pack-resource-list --env ${{MWS_ENV}} --params '{}'".format(
                json.dumps(
                    {"resourceType": args.second, "resourceIds": resource_info},
                    ensure_ascii=False,
                    separators=(",", ":"),
                )
            )
        )
        print("")
    elif option["needResourceId"]:
        print("标准资源 ID 未提供，暂不调用 plan-pack-resource-list；后续拿到资源 ID 后再校验资源并提取默认角标/跳转链接。")
        print("")

    print("按投放端提取模板：")
    for alias in aliases:
        cfg = POSITION_CONFIG[alias]
        params = {
            "positionCode": cfg["positionCode"],
            "channelCode": cfg["channelCode"],
            "firstResType": args.first,
            "resType": args.second,
        }
        if resource_info:
            params["resId"] = resource_info
        print(
            "mws link data-template-extract-private --env ${{MWS_ENV}} --params '{}'".format(
                json.dumps(params, ensure_ascii=False, separators=(",", ":"))
            )
        )
    if aliases != normalized["saveAliases"]:
        print("")
        print("保存 promotion-update-creative 时使用这些 positionAlias：")
        print("、".join(normalized["saveAliases"]))
        print("说明：移动端(iPhone&Android) 与荣耀白牌同时存在时，只提交移动端素材，荣耀白牌由服务端按移动端合并补齐。")


def print_infer(detail, args):
    option, source = infer_option(detail)
    if not option:
        print_choices(detail)
        raise SystemExit("无法从当前推广自动推断投放资源，请让用户从上面的资源类型中选择。")
    print("已自动推断投放资源来源：{}".format(source))
    select_args = argparse.Namespace(
        first=option["first"],
        second=option["second"],
        resource_id=args.resource_id or "",
        require_resource_id=False,
    )
    print_select(detail, select_args)


def save_aliases(aliases):
    result = []
    has_mobile = "移动端(iPhone&Android)" in aliases
    for alias in aliases:
        if alias == "荣耀白牌" and has_mobile:
            continue
        result.append(alias)
    return result


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("choices")
    infer = sub.add_parser("infer")
    infer.add_argument("--resource-id", default="")
    select = sub.add_parser("select")
    select.add_argument("--first", required=True)
    select.add_argument("--second", required=True)
    select.add_argument("--resource-id", default="")
    select.add_argument(
        "--require-resource-id",
        action="store_true",
        help="直接修改/补配/换物料标准资源素材时使用；标准资源缺资源 ID 时直接失败。",
    )
    args = parser.parse_args()

    detail = load_json_from_stdin()
    if args.cmd == "choices":
        print_choices(detail)
    elif args.cmd == "infer":
        print_infer(detail, args)
    elif args.cmd == "select":
        print_select(detail, args)


if __name__ == "__main__":
    main()

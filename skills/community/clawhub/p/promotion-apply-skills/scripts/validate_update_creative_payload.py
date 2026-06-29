#!/usr/bin/env python3
"""
Preflight check for link.promotion-update-creative payloads.

Usage:
  python3 scripts/validate_update_creative_payload.py /tmp/update-creative.json \
    --detail /tmp/promotion-detail.json \
    --resource-defaults /tmp/plan-pack-resource-list.json
"""
import argparse
import json
import sys
from typing import Any, Dict, List, Optional, Tuple


FORBIDDEN_TOP_LEVEL = {
    "op",
    "crowdIds",
    "forceSave",
    "crowdList",
    "relatedResourceTypes",
    "relatedResourceIds",
}

IMAGE_FIELD_KEYWORDS = (
    "pic",
    "image",
    "img",
    "cover",
    "poster",
)

URL_FIELD_KEYWORDS = (
    "url",
    "link",
    "jump",
    "href",
)

PLACEHOLDER_MARKERS = (
    "NOS_URL",
    "TODO",
    "{...",
    "...}",
    "// ...",
    "/tmp/",
    "~/",
)


def load_json(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise SystemExit(f"文件不存在：{path}")
    except json.JSONDecodeError as exc:
        raise SystemExit(f"JSON 解析失败：{path}:{exc.lineno}:{exc.colno} {exc.msg}")


def unwrap_mws(payload: Any) -> Any:
    if isinstance(payload, dict) and "data" in payload and ("code" in payload or "message" in payload):
        return payload.get("data")
    if isinstance(payload, dict) and isinstance(payload.get("data"), dict) and "promotionAliasTemplateList" in payload.get("data"):
        return payload.get("data")
    return payload


def as_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []


def get_first_string(obj: Dict[str, Any], keys: List[str]) -> str:
    for key in keys:
        value = obj.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def extract_detail_alias_templates(detail_payload: Any) -> List[Dict[str, str]]:
    detail = unwrap_mws(detail_payload)
    if not isinstance(detail, dict):
        return []
    raw_nodes = detail.get("promotionAliasTemplateList") or []
    result: List[Dict[str, str]] = []
    for node in as_list(raw_nodes):
        if not isinstance(node, dict):
            continue
        alias = get_first_string(node, ["positionAlias", "alias", "name"])
        show = get_first_string(node, ["positionAliasShow", "aliasShow", "positionAliasName", "showName"])
        if alias:
            result.append({"positionAlias": alias, "positionAliasShow": show or alias})
    return result


def is_image_field(key: str) -> bool:
    lower = key.lower()
    return any(word in lower for word in IMAGE_FIELD_KEYWORDS)


def looks_like_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def is_url_field(key: str) -> bool:
    lower = key.lower()
    return any(word in lower for word in URL_FIELD_KEYWORDS)


def is_music_web_url(value: str) -> bool:
    text = value.strip().lower()
    return text.startswith("http://music.163.com/") or text.startswith("https://music.163.com/")


def collect_strings(value: Any) -> List[str]:
    strings: List[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, dict):
        for item in value.values():
            strings.extend(collect_strings(item))
    elif isinstance(value, list):
        for item in value:
            strings.extend(collect_strings(item))
    return strings


def extract_resource_items(defaults_payload: Any) -> List[Dict[str, Any]]:
    data = unwrap_mws(defaults_payload)
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict):
        nested = data.get("data")
        if isinstance(nested, list):
            return [item for item in nested if isinstance(item, dict)]
    return []


def resource_item_id(item: Dict[str, Any]) -> str:
    composed = item.get("composedData") or {}
    common = composed.get("commonComposedData") or {}
    for key in ("resourceId", "id"):
        value = item.get(key)
        if value not in (None, ""):
            return str(value).strip()
    for key in ("resourceId", "id"):
        value = common.get(key)
        if value not in (None, ""):
            return str(value).strip()
    return ""


def validate_standard_resource_defaults(
    payload: Dict[str, Any],
    defaults_path: Optional[str],
    errors: List[str],
    warnings: List[str],
) -> None:
    resource_types = payload.get("resourceTypes") or []
    standard_resource = bool(
        isinstance(resource_types, list)
        and resource_types
        and isinstance(resource_types[0], list)
        and resource_types[0]
        and resource_types[0][0] == "standard"
    )
    if not standard_resource:
        return

    resource_info = str(payload.get("resourceInfo") or "").strip()
    if not defaults_path:
        errors.append(
            "标准资源保存前必须先调用 `mws link plan-pack-resource-list` 获取资源默认值，"
            "并把返回 JSON 通过 `--resource-defaults` 传给本预检脚本；禁止直接用资源 ID 手拼跳转链接。"
        )
        return

    items = extract_resource_items(load_json(defaults_path))
    if not items:
        resource_type = str(payload.get("resourceType") or "").strip()
        if resource_type == "song" and resource_info:
            warnings.append(
                "`--resource-defaults` 未解析到资源数据；当前是标准歌曲，可使用歌曲兜底链接："
                f"非 Web 端 `orpheus://song/{resource_info}`，Web 端 "
                f"`https://music.163.com/#/song?id={resource_info}`。"
                "仍需确认已实际调用 plan-pack-resource-list。"
            )
            return
        errors.append(
            "`--resource-defaults` 未解析到资源数据；除标准歌曲兜底外，标准资源无法确认默认角标/端维度跳转链接，"
            "请重新调用 plan-pack-resource-list，或让用户提供明确的端维度链接后再保存。"
        )
        return

    ids = [resource_item_id(item) for item in items if resource_item_id(item)]
    if resource_info and ids and resource_info not in ids:
        errors.append(
            f"`--resource-defaults` 中的资源 ID {ids} 与 payload.resourceInfo={resource_info} 不一致；"
            "必须用当前资源 ID 重新调用 plan-pack-resource-list。"
        )

    has_client_default = False
    has_web_default = False
    for item in items:
        composed = item.get("composedData") or {}
        common = composed.get("commonComposedData") or {}
        common_url = str(common.get("url") or "").strip()
        orpheus = str(item.get("orpheus") or "").strip()
        pc_url = str(item.get("pcUrl") or "").strip()
        if common_url or orpheus:
            has_client_default = True
        if looks_like_url(pc_url) or looks_like_url(common_url):
            has_web_default = True

    if not has_client_default:
        warnings.append(
            "标准资源默认值里没有客户端默认链接；非 Web 端不能用 music.163.com 手拼兜底，"
            "请优先从 data-template-extract-private 的 preData 获取，仍缺则让用户提供端维度链接。"
        )
    if not has_web_default:
        warnings.append(
            "标准资源默认值里没有 Web http/https 链接；Web 端必须让用户提供 http/https，不能用 orpheus 兜底。"
        )


def validate_resource_fields(payload: Dict[str, Any], errors: List[str]) -> None:
    for key in FORBIDDEN_TOP_LEVEL:
        if key in payload:
            errors.append(f"顶层字段 `{key}` 不属于 promotion-update-creative 当前 schema 或不应在素材阶段传，请删除。")

    full_type = payload.get("fullType")
    if full_type not in ("full", "nofull"):
        errors.append("`fullType` 必须传 `full` 或 `nofull`，不能缺失、为空或使用其它值。")

    resource_type = payload.get("resourceType")
    if not isinstance(resource_type, str) or not resource_type.strip():
        errors.append("`resourceType` 必须是二级资源类型字符串，例如 `song` 或 `activity`。")

    if "resourceInfo" not in payload:
        errors.append("`resourceInfo` 必须传；标准资源传资源 ID，非标活动传空字符串。")
    elif payload.get("resourceInfo") is None:
        errors.append("`resourceInfo` 不能是 null；非标活动请传空字符串。")

    resource_types = payload.get("resourceTypes")
    if not isinstance(resource_types, list) or not resource_types:
        errors.append("`resourceTypes` 必须是非空二维数组，例如 [[\"standard\",\"song\"]]。")
        return

    first = resource_types[0]
    if not isinstance(first, list) or len(first) < 2:
        errors.append("`resourceTypes[0]` 必须是至少两项的数组，例如 [\"standard\",\"song\"]。")
        return

    top_type = str(first[0])
    second_type = str(first[1])
    if resource_type and second_type != resource_type:
        errors.append(f"`resourceType` 必须等于 `resourceTypes[0][1]`；当前是 `{resource_type}` vs `{second_type}`。")

    resource_info = str(payload.get("resourceInfo") or "").strip()
    if top_type == "standard" and not resource_info:
        errors.append("标准资源的 `resourceInfo` 必须是资源 ID，不能空。")

    strategy_info = payload.get("strategyInfo")
    if full_type == "nofull":
        if not isinstance(strategy_info, str) or not strategy_info.strip():
            errors.append("非全量 `fullType=nofull` 时必须传 `strategyInfo` JSON 字符串。")
        else:
            try:
                parsed = json.loads(strategy_info)
            except json.JSONDecodeError as exc:
                errors.append(f"`strategyInfo` 必须是合法 JSON 字符串：{exc.msg}")
            else:
                crowd = parsed.get("crowd") if isinstance(parsed, dict) else None
                if not isinstance(crowd, dict):
                    errors.append("非全量 `strategyInfo` 中必须包含 `crowd` 对象。")
                elif crowd.get("op") not in ("contain", "notcontain"):
                    errors.append("`strategyInfo.crowd.op` 必须是 `contain` 或 `notcontain`。")


def parse_template_schema(value: Any, path: str, errors: List[str]) -> Optional[Dict[str, Any]]:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{path}.templateSchema 必须是完整模板对象的 JSON 字符串，不能缺失或为空。")
        return None
    for marker in ("{...", "...}"):
        if marker in value:
            errors.append(f"{path}.templateSchema 仍包含占位符 `{marker}`，必须替换为完整模板 JSON 字符串。")
            return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        errors.append(f"{path}.templateSchema 不是合法 JSON 字符串：{exc.msg}")
        return None
    if not isinstance(parsed, dict):
        errors.append(f"{path}.templateSchema 解析后必须是对象。")
        return None
    return parsed


def validate_image_and_placeholders(
    data: Any,
    path: str,
    errors: List[str],
    web_alias: bool = False,
    standard_resource: bool = False,
) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            child_path = f"{path}.{key}"
            if isinstance(value, str):
                for marker in PLACEHOLDER_MARKERS:
                    if marker in value:
                        errors.append(f"{child_path} 含占位或本地路径 `{marker}`，最终 payload 只能放真实值。")
                        break
                if value and is_image_field(key) and not looks_like_url(value):
                    errors.append(f"{child_path} 看起来是图片字段，必须是已上传后的 http/https URL。")
                if web_alias and value.strip() and is_url_field(key) and not looks_like_url(value.strip()):
                    errors.append(f"{child_path} 是 Web 端跳转链接字段，必须使用 http/https，不能使用 orpheus 或其它 scheme。")
                if (
                    standard_resource
                    and not web_alias
                    and value.strip()
                    and is_url_field(key)
                    and is_music_web_url(value)
                ):
                    errors.append(
                        f"{child_path} 是标准资源的非 Web 端跳转链接，不能手拼 music.163.com Web 链接。"
                        "请使用 plan-pack-resource-list / data-template-extract-private 返回的客户端默认链接"
                        "（如 commonComposedData.url 或 orpheus），Web 端才使用 http/https。"
                    )
            validate_image_and_placeholders(value, child_path, errors, web_alias, standard_resource)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            validate_image_and_placeholders(item, f"{path}[{index}]", errors, web_alias, standard_resource)


def validate_creative(
    creative: Any,
    path: str,
    seen_names: set,
    errors: List[str],
    web_alias: bool = False,
    standard_resource: bool = False,
) -> None:
    if not isinstance(creative, dict):
        errors.append(f"{path} 必须是对象。")
        return

    name = creative.get("name")
    if not isinstance(name, str) or not name.strip():
        errors.append(f"{path}.name 必须非空。")
    elif name in seen_names:
        errors.append(f"创意名称 `{name}` 在本次 payload 中重复；每个端必须唯一。")
    else:
        seen_names.add(name)

    if creative.get("tenant") != "music":
        errors.append(f"{path}.tenant 必须是 `music`。")

    data_template = creative.get("dataTemplate")
    template_id = None
    if not isinstance(data_template, dict) or data_template.get("id") in (None, ""):
        errors.append(f"{path}.dataTemplate.id 必须存在。")
    else:
        template_id = data_template.get("id")

    template = parse_template_schema(creative.get("templateSchema"), path, errors)
    if template is not None and template_id is not None:
        schema_id = template.get("id")
        if schema_id is not None and str(schema_id) != str(template_id):
            errors.append(f"{path}.dataTemplate.id 与 templateSchema.id 不一致：{template_id} vs {schema_id}。")

    detail = creative.get("creativeDetailDataVO")
    if not isinstance(detail, dict):
        errors.append(f"{path}.creativeDetailDataVO 必须是对象。")
        return
    children = detail.get("children")
    if not isinstance(children, list) or not children:
        errors.append(f"{path}.creativeDetailDataVO.children 必须是非空数组。")
        return

    for child_index, child in enumerate(children):
        child_path = f"{path}.creativeDetailDataVO.children[{child_index}]"
        if not isinstance(child, dict):
            errors.append(f"{child_path} 必须是对象。")
            continue
        if not child.get("code"):
            errors.append(f"{child_path}.code 必须存在，且等于模板节点 code。")
        data = child.get("data")
        if not isinstance(data, dict):
            errors.append(f"{child_path}.data 必须是对象。")
            continue
        if not any(str(value).strip() for value in collect_strings(data)):
            errors.append(f"{child_path}.data 中没有任何非空素材值，可能触发“素材不能为空”。")
        validate_image_and_placeholders(data, child_path + ".data", errors, web_alias, standard_resource)


def validate_alias_creatives(payload: Dict[str, Any], detail_aliases: List[Dict[str, str]], errors: List[str]) -> None:
    nodes = payload.get("promotionAliasCreativeList")
    if not isinstance(nodes, list) or not nodes:
        errors.append("`promotionAliasCreativeList` 必须是非空数组。")
        return

    if detail_aliases:
        expected_aliases = [item["positionAlias"] for item in detail_aliases]
        actual_aliases = [node.get("positionAlias") if isinstance(node, dict) else None for node in nodes]
        if len(nodes) != len(detail_aliases):
            errors.append(
                "`promotionAliasCreativeList` 节点数必须等于当前详情 `promotionAliasTemplateList` 节点数；"
                f"当前 payload={len(nodes)}，详情={len(detail_aliases)}。少传任一折叠端都会导致服务端把该端素材视为空，"
                "常见真实报错是“素材不能为空2”。"
            )
        if actual_aliases != expected_aliases:
            errors.append(
                "`promotionAliasCreativeList[].positionAlias` 必须按当前 `promotionAliasTemplateList` 顺序完整提交；"
                f"当前={actual_aliases}，期望={expected_aliases}。缺端、顺序错或把折叠端拆散，都可能触发“素材不能为空2”。"
            )

    seen_aliases = set()
    seen_names = set()
    resource_types = payload.get("resourceTypes") or []
    standard_resource = bool(
        isinstance(resource_types, list)
        and resource_types
        and isinstance(resource_types[0], list)
        and resource_types[0]
        and resource_types[0][0] == "standard"
    )
    for index, node in enumerate(nodes):
        node_path = f"promotionAliasCreativeList[{index}]"
        if not isinstance(node, dict):
            errors.append(f"{node_path} 必须是对象。")
            continue

        alias = node.get("positionAlias")
        if not isinstance(alias, str) or not alias.strip():
            errors.append(f"{node_path}.positionAlias 必须非空。")
        elif alias in seen_aliases:
            errors.append(f"`positionAlias` 重复：{alias}。")
        else:
            seen_aliases.add(alias)

        show = node.get("positionAliasShow")
        if not isinstance(show, str) or not show.strip():
            errors.append(f"{node_path}.positionAliasShow 必须非空，优先从同 alias 的 promotionAliasTemplateList 节点复制。")

        if detail_aliases and index < len(detail_aliases):
            expected = detail_aliases[index]
            if alias == expected["positionAlias"] and show != expected["positionAliasShow"]:
                errors.append(
                    f"{node_path}.positionAliasShow 应从详情同节点复制："
                    f"`{expected['positionAliasShow']}`，当前 `{show}`。"
                )

        creative_list = node.get("promotionCreativeList")
        if not isinstance(creative_list, list) or not creative_list:
            errors.append(f"{node_path}.promotionCreativeList 必须是非空数组。")
            continue

        for item_index, item in enumerate(creative_list):
            item_path = f"{node_path}.promotionCreativeList[{item_index}]"
            if not isinstance(item, dict):
                errors.append(f"{item_path} 必须是对象。")
                continue
            flattened_keys = {
                "name",
                "tenant",
                "dataTemplate",
                "templateSchema",
                "creativeDetailDataVO",
                "templateId",
                "resourceTypeCode",
                "data",
            } & set(item.keys())
            if flattened_keys and "creative" not in item:
                errors.append(
                    f"{item_path} 是拍平结构，字段 {sorted(flattened_keys)} 必须放进 "
                    "`creative.dataTemplate/templateSchema/creativeDetailDataVO`，并改成 {\"creative\": {...}} 包装。"
                )
                continue
            if "creative" not in item:
                errors.append(f"{item_path} 必须包含 `creative` 包装对象。")
                continue
            validate_creative(
                item.get("creative"),
                f"{item_path}.creative",
                seen_names,
                errors,
                isinstance(alias, str) and alias.strip().lower() == "web",
                standard_resource,
            )


def validate(payload_path: str, detail_path: Optional[str], defaults_path: Optional[str]) -> Tuple[List[str], List[str]]:
    payload = load_json(payload_path)
    warnings: List[str] = []
    errors: List[str] = []

    if not isinstance(payload, dict):
        return ["payload 顶层必须是 JSON 对象。"], warnings

    if payload.get("method") == "updateCreative" and isinstance(payload.get("param"), list):
        return [
            "payload 是 raw/mws_exec 风格包装 `{method:\"updateCreative\", param:[...]}`，不是 "
            "`mws link promotion-update-creative` 的正式 JSON 入参。禁止绕过本 skill 原样执行；"
            "请取 `param[0]` 中的业务输入，重新查 promotion-detail、提模板、组装创意并预检。"
        ], warnings

    for marker in PLACEHOLDER_MARKERS:
        if marker in json.dumps(payload, ensure_ascii=False):
            errors.append(f"payload 中包含占位或本地路径 `{marker}`，请替换为当前真实值。")

    if payload.get("id") in (None, ""):
        errors.append("`id` 推广 ID 必须存在。")

    validate_resource_fields(payload, errors)
    validate_standard_resource_defaults(payload, defaults_path, errors, warnings)

    detail_aliases: List[Dict[str, str]] = []
    if detail_path:
        detail_aliases = extract_detail_alias_templates(load_json(detail_path))
        if not detail_aliases:
            errors.append("未能从 detail 中解析 `promotionAliasTemplateList`，无法校验所有折叠端是否完整提交。")
    else:
        errors.append("必须传 `--detail`，否则无法校验所有折叠端是否完整提交，禁止调用 promotion-update-creative。")

    validate_alias_creatives(payload, detail_aliases, errors)
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate promotion-update-creative payload before MWS call.")
    parser.add_argument("payload", help="promotion-update-creative payload JSON file")
    parser.add_argument("--detail", required=True, help="promotion-detail JSON file used to verify folded aliases")
    parser.add_argument(
        "--resource-defaults",
        help="plan-pack-resource-list JSON. Required for standard resource payloads to prove default links were fetched.",
    )
    args = parser.parse_args()

    errors, warnings = validate(args.payload, args.detail, args.resource_defaults)
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        print("promotion-update-creative payload preflight failed:", file=sys.stderr)
        for index, error in enumerate(errors, 1):
            print(f"{index}. {error}", file=sys.stderr)
        return 1

    print("OK promotion-update-creative payload preflight passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())

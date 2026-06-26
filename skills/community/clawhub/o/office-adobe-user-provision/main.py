"""
Unified CLI entry for Office 365 and Adobe user management.

Usage examples:
    python main.py office365 init
    python main.py office365 create user01 --product O365_BUSINESS
    python main.py ps create user01
    python main.py adobe assign user01 --product 759801945
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

from app.core.logger import setup_logging
from app.core.prompt import choose_from_list
from app.core import state as state_helpers
from app.services import user_service
from app.services.provider_factory import canonical_name


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Office365 & Adobe 用户管理 CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("provider", help="Provider 标识，例如 office365、adobe、ps")

    subparsers = parser.add_subparsers(dest="action", required=True)

    init_parser = subparsers.add_parser("init", help="初始化并自检 API 连通性/产品列表")
    init_parser.add_argument("--force-default", action="store_true", help="强制重新选择默认产品")
    init_parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")

    products_parser = subparsers.add_parser("products", help="列出可用产品/授权")
    products_parser.add_argument("--refresh", action="store_true", help="强制从远端刷新产品信息")
    products_parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")

    create_parser = subparsers.add_parser("create", help="创建用户并授权")
    create_parser.add_argument("identifier", help="用户名或邮箱")
    create_parser.add_argument("--product", help="产品 Profile ID 或 SKU Part Number")
    create_parser.add_argument("--display-name", dest="display_name")
    create_parser.add_argument("--given-name", dest="givenName")
    create_parser.add_argument("--surname")
    create_parser.add_argument("--country", default="CN")
    create_parser.add_argument("--user-type", dest="user_type", default="federatedID")
    create_parser.add_argument("--force-change", dest="force_change_password", action="store_true", help="强制下次登录修改密码")
    create_parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")

    assign_parser = subparsers.add_parser("assign", help="为已有用户分配产品/授权")
    assign_parser.add_argument("identifier")
    assign_parser.add_argument("--product", required=True, help="产品 Profile ID 或 SKU Part Number")
    assign_parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")

    reset_parser = subparsers.add_parser("reset", help="重置密码")
    reset_parser.add_argument("identifier")
    reset_parser.add_argument("--new-password")
    reset_parser.add_argument("--no-force-change", dest="force_change_password", action="store_false", default=True,
                              help="重置后不强制修改密码（仅 Office 365）")
    reset_parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")

    delete_parser = subparsers.add_parser("delete", help="删除用户")
    delete_parser.add_argument("identifier")
    delete_parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")

    inspect_parser = subparsers.add_parser("inspect", help="查看用户详情")
    inspect_parser.add_argument("identifier")
    inspect_parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")

    alias_parser = subparsers.add_parser("alias", help="管理产品/授权别名")
    alias_parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    alias_sub = alias_parser.add_subparsers(dest="alias_action", required=True)

    alias_set = alias_sub.add_parser("set", help="设置别名")
    alias_set.add_argument("alias")
    alias_set.add_argument("product")

    alias_list = alias_sub.add_parser("list", help="查看所有别名")

    alias_remove = alias_sub.add_parser("remove", help="删除别名")
    alias_remove.add_argument("alias")

    selftest_parser = subparsers.add_parser("selftest", help="执行 provider 自检（创建/授权/重置/删除/导出）")
    selftest_parser.add_argument("--product", help="指定测试时使用的产品/许可证")
    selftest_parser.add_argument("--json", action="store_true", help="以 JSON 输出结果")

    return parser


def output_result(data: Any, as_json: bool = False) -> None:
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{key}: {value}")
    elif isinstance(data, list):
        for item in data:
            print(item)
    else:
        print(data)


def handle_init(provider: str, args) -> None:
    metadata = user_service.init_provider(provider)
    products = user_service.list_products(provider)

    if args.force_default or (sys.stdin.isatty() and products):
        maybe_set_default_product(provider, products, force_prompt=args.force_default)

    result = {
        "metadata": metadata,
        "products": products,
        "preferences": user_service.get_cached_state(provider).get("preferences", {})
    }
    output_result(result, args.json)


def handle_products(provider: str, args) -> None:
    cached = user_service.get_cached_state(provider)
    products: List[Dict[str, Any]] = cached.get("products", [])
    if args.refresh or not products:
        products = user_service.list_products(provider)
        cached = user_service.get_cached_state(provider)
    output_result(products, args.json)


def handle_create(provider: str, args) -> None:
    if args.product:
        product = resolve_product_token(provider, args.product)
    else:
        product = determine_product(provider)

    # Adobe 当前 org 默认用 adobeID（邀请模式），等价 Admin Console 邀请用户；
    # 仅当用户显式传 --user-type 时才使用其值（argparse 默认值是 "federatedID"）
    user_type = args.user_type
    if provider == "adobe" and user_type == "federatedID":
        user_type = "adobeID"

    payload = {
        "display_name": args.display_name,
        "givenName": args.givenName,
        "surname": args.surname,
        "country": args.country,
        "usageLocation": args.country,
        "user_type": user_type,
        "force_change_password": args.force_change_password if args.force_change_password else True,
    }
    # Remove None entries
    payload = {k: v for k, v in payload.items() if v not in (None, "")}

    result = user_service.create_user(provider, args.identifier, product=product, **payload)
    output_result(result, args.json)


def handle_assign(provider: str, args) -> None:
    product = resolve_product_token(provider, args.product)
    result = user_service.assign_product(provider, args.identifier, product)
    output_result(result, args.json)


def handle_reset(provider: str, args) -> None:
    result = user_service.reset_password(
        provider,
        args.identifier,
        new_password=args.new_password,
        force_change_password=args.force_change_password,
    )
    output_result(result, args.json)


def handle_delete(provider: str, args) -> None:
    result = user_service.delete_user(provider, args.identifier)
    output_result(result, args.json)


def handle_inspect(provider: str, args) -> None:
    result = user_service.describe_user(provider, args.identifier)
    output_result(result, args.json)


def handle_alias(provider: str, args) -> None:
    action = args.alias_action
    if action == "list":
        output_result(user_service.get_aliases(provider), args.json)
        return
    if action == "set":
        product_id = resolve_product_token(provider, args.product)
        aliases = user_service.set_alias(provider, args.alias, product_id)
        output_result({"alias": args.alias, "product": product_id, "aliases": aliases}, args.json)
        return
    if action == "remove":
        aliases = user_service.remove_alias(provider, args.alias)
        output_result({"alias": args.alias, "aliases": aliases}, args.json)
        return
    output_result({"message": f"未知别名操作: {action}"}, args.json)


def handle_self_test(provider: str, args) -> None:
    product = resolve_product_token(provider, args.product) if args.product else determine_product(provider)
    if not product:
        output_result({"error": "自检需要先设置默认产品或通过 --product 指定"}, args.json)
        return
    result = user_service.run_self_test(provider, product)
    output_result(result, args.json)


def maybe_set_default_product(provider: str, products: List[Dict[str, Any]], force_prompt: bool = False) -> None:
    cached = user_service.get_cached_state(provider)
    preferences = cached.get("preferences", {})

    if not products:
        return

    if not force_prompt and preferences.get("default_product_id"):
        return

    if not sys.stdin.isatty() and not force_prompt:
        return

    if not force_prompt:
        answer = input("是否设置默认产品/授权? (y/N): ").strip().lower()
        if answer not in ("y", "yes"):
            return

    selection = choose_from_list(products, label_key="name", allow_skip=False)
    if not selection:
        return
    selected_id = str(selection.get("id"))
    preferences["default_product_id"] = selected_id
    preferences["default_product_name"] = selection.get("name")
    cached["preferences"] = preferences
    state_helpers.write_state(canonical_name(provider), cached)
    print(f"默认产品已设置为: {preferences['default_product_name']} ({selected_id})")

    alias = input("为该产品设置别名/描述（可选，例如 ps / acrobat，回车跳过）: ").strip()
    if alias:
        aliases = user_service.set_alias(provider, alias, selected_id)
        print(f"别名已保存: {alias} -> {selected_id}")
        print(f"当前别名: {aliases}")


def determine_product(provider: str) -> Optional[str]:
    cached = user_service.get_cached_state(provider)
    preferences = cached.get("preferences", {})
    default_product = preferences.get("default_product_id")
    default_name = preferences.get("default_product_name")

    if default_product and str(default_product).lower() not in ("none", "null", ""):
        return str(default_product)

    if default_product and default_name:
        matched = _match_product_from_cache(provider, default_name, cached)
        if matched:
            preferences["default_product_id"] = matched
            cached["preferences"] = preferences
            state_helpers.write_state(canonical_name(provider), cached)
            return matched

    if not sys.stdin.isatty():
        return None

    products = cached.get("products")
    if not products:
        products = user_service.list_products(provider)
        cached = user_service.get_cached_state(provider)

    selection = choose_from_list(products, label_key="name", allow_skip=True)
    if selection:
        cached.setdefault("preferences", {})
        selected_id = str(selection.get("id"))
        cached["preferences"]["default_product_id"] = selected_id
        cached["preferences"]["default_product_name"] = selection.get("name")
        state_helpers.write_state(canonical_name(provider), cached)
        return selected_id

    return None


def resolve_product_token(provider: str, token: Optional[str]) -> Optional[str]:
    if not token:
        return None
    token_str = str(token).strip()
    cached = user_service.get_cached_state(provider)
    alias_map = {k.lower(): str(v) for k, v in cached.get("aliases", {}).items()}
    lower = token_str.lower()
    if lower in alias_map:
        return alias_map[lower]
    match = _match_product_from_cache(provider, token_str, cached)
    return match or token_str


def _match_product_from_cache(provider: str, token: str, cached: Optional[Dict[str, Any]] = None) -> Optional[str]:
    cached = cached or user_service.get_cached_state(provider)
    products = cached.get("products")
    if not products:
        products = user_service.list_products(provider)
        cached = user_service.get_cached_state(provider)
    token_lower = token.lower()
    for item in products or []:
        pid_raw = item.get("id")
        if pid_raw is None or str(pid_raw).lower() in ("none", "null", ""):
            continue
        pid = str(pid_raw)
        if token == pid:
            return pid
        name = (item.get("name") or "").lower()
        if token_lower == name:
            return pid
    return None


def main():
    parser = build_parser()
    args = parser.parse_args()

    setup_logging()

    try:
        provider = canonical_name(args.provider)
    except ValueError as exc:
        parser.error(str(exc))
        return

    action = args.action
    if action == "init":
        handle_init(provider, args)
    elif action == "products":
        handle_products(provider, args)
    elif action == "create":
        handle_create(provider, args)
    elif action == "assign":
        handle_assign(provider, args)
    elif action == "reset":
        handle_reset(provider, args)
    elif action == "delete":
        handle_delete(provider, args)
    elif action == "inspect":
        handle_inspect(provider, args)
    elif action == "alias":
        handle_alias(provider, args)
    elif action == "selftest":
        handle_self_test(provider, args)
    else:
        parser.error(f"未知操作: {action}")


if __name__ == "__main__":
    main()

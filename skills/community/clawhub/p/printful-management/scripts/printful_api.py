#!/usr/bin/env python3
import argparse
import csv
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterable, Optional

BASE_URL = "https://api.printful.com"


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def compact_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def load_json_file(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dump_json_file(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def _encode_query(pairs: Iterable[tuple[str, Any]]) -> str:
    cleaned = [(k, str(v)) for k, v in pairs if v is not None]
    return urllib.parse.urlencode(cleaned)


def with_query(path: str, **params: Any) -> str:
    query = _encode_query(params.items())
    if not query:
        return path
    joiner = "&" if "?" in path else "?"
    return f"{path}{joiner}{query}"


def resolve_token(args: argparse.Namespace) -> str:
    token = getattr(args, "api_key", None) or os.environ.get("PRINTFUL_API_KEY")
    if not token:
        eprint("Missing API token. Set PRINTFUL_API_KEY or pass --api-key.")
        sys.exit(2)
    return token


def resolve_store_id(args: argparse.Namespace) -> Optional[int]:
    return getattr(args, "store_id", None)


def add_common_auth(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--api-key", help="Printful private token; defaults to PRINTFUL_API_KEY env var")
    parser.add_argument("--language", help="Optional X-PF-Language value, e.g. en_US or de_DE")
    parser.add_argument("--output", help="Write response JSON to a file as well as stdout")


def add_paging(parser: argparse.ArgumentParser, default_limit: int = 20) -> None:
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=default_limit)


def add_store_context(parser: argparse.ArgumentParser, required: bool = False) -> None:
    parser.add_argument("--store-id", type=int, required=required, help="Store context. Sent via X-PF-Store-ID header.")


def maybe_output(args: argparse.Namespace, data: Any) -> None:
    print_json(data)
    if getattr(args, "output", None):
        dump_json_file(args.output, data)


def write_text_file(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def extract_product_rows(payload: Dict[str, Any]) -> list[Dict[str, Any]]:
    if isinstance(payload.get("result"), list):
        products = payload["result"]
    elif isinstance(payload.get("data"), dict) and isinstance(payload["data"].get("result"), list):
        products = payload["data"]["result"]
    else:
        products = []

    rows = []
    for item in products:
        rows.append(
            {
                "id": item.get("id"),
                "external_id": item.get("external_id"),
                "name": item.get("name"),
                "variants": item.get("variants"),
                "synced": item.get("synced"),
                "is_ignored": item.get("is_ignored"),
                "thumbnail_url": item.get("thumbnail_url"),
            }
        )
    return rows


def summarize_product_rows(rows: list[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(rows)
    synced_full = 0
    synced_partial = 0
    synced_zero = 0
    ignored = 0
    for row in rows:
        variants = row.get("variants") or 0
        synced = row.get("synced") or 0
        if row.get("is_ignored"):
            ignored += 1
        if synced == 0:
            synced_zero += 1
        elif variants and synced >= variants:
            synced_full += 1
        else:
            synced_partial += 1
    return {
        "total_products": total,
        "fully_synced": synced_full,
        "partially_synced": synced_partial,
        "zero_synced": synced_zero,
        "ignored": ignored,
    }


def format_products_markdown(rows: list[Dict[str, Any]], summary: Dict[str, Any], title: str = "Printful products") -> str:
    lines = [f"# {title}", "", "## Summary", ""]
    for key, value in summary.items():
        lines.append(f"- {key.replace('_', ' ')}: {value}")
    lines.extend(["", "## Products", ""])
    for row in rows:
        lines.append(
            f"- **{row['name']}** | id: `{row['id']}` | external_id: `{row['external_id']}` | variants: {row['variants']} | synced: {row['synced']} | ignored: {row['is_ignored']}"
        )
    lines.append("")
    return "\n".join(lines)


def write_csv(path: str, rows: list[Dict[str, Any]]) -> None:
    fieldnames = ["id", "external_id", "name", "variants", "synced", "is_ignored", "thumbnail_url"]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_body(args: argparse.Namespace) -> Optional[Any]:
    if getattr(args, "body_file", None):
        return load_json_file(args.body_file)
    if getattr(args, "body", None):
        return json.loads(args.body)
    return None


def request(
    method: str,
    path: str,
    token: str,
    *,
    body: Optional[Any] = None,
    language: Optional[str] = None,
    store_id: Optional[int] = None,
) -> Dict[str, Any]:
    if not path.startswith("/"):
        path = "/" + path
    url = BASE_URL + path
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    if language:
        headers["X-PF-Language"] = language
    if store_id is not None:
        headers["X-PF-Store-ID"] = str(store_id)

    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req) as resp:
            payload = resp.read().decode("utf-8", errors="replace")
            return json.loads(payload) if payload else {"code": resp.status, "result": None}
    except urllib.error.HTTPError as e:
        payload = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(payload) if payload else {}
        except json.JSONDecodeError:
            parsed = {"code": e.code, "error": {"message": payload or str(e)}}
        print_json(parsed)
        sys.exit(1)
    except urllib.error.URLError as e:
        print_json({"error": {"message": str(e)}})
        sys.exit(2)


def command_get(args: argparse.Namespace, path: str) -> None:
    data = request(
        "GET",
        path,
        resolve_token(args),
        language=args.language,
        store_id=resolve_store_id(args),
    )
    maybe_output(args, data)


def command_send(args: argparse.Namespace, method: str, path: str) -> None:
    data = request(
        method,
        path,
        resolve_token(args),
        body=load_body(args),
        language=args.language,
        store_id=resolve_store_id(args),
    )
    maybe_output(args, data)


def cmd_scopes(args: argparse.Namespace) -> None:
    command_get(args, "/oauth/scopes")


def cmd_stores(args: argparse.Namespace) -> None:
    command_get(args, "/stores")


def cmd_store(args: argparse.Namespace) -> None:
    command_get(args, f"/stores/{args.store_id}")


def cmd_sync_products(args: argparse.Namespace) -> None:
    path = with_query(args.path_style, offset=args.offset, limit=args.limit)
    command_get(args, path)


def detect_store_mode(token: str, store_id: int, language: Optional[str] = None) -> Dict[str, Any]:
    attempts = []
    for mode, path in (("connected", "/sync/products?limit=1&offset=0"), ("manual", "/store/products?limit=1&offset=0")):
        try:
            data = request("GET", path, token, language=language, store_id=store_id)
            return {
                "code": 200,
                "result": {
                    "store_id": store_id,
                    "mode": mode,
                    "path": path.split("?")[0],
                    "probe_count": len(data.get("result", [])) if isinstance(data.get("result"), list) else None,
                },
                "attempts": attempts,
            }
        except SystemExit as e:
            attempts.append({"mode": mode, "path": path, "exit_code": e.code})
            continue
    return {
        "code": 400,
        "result": "Unable to determine store mode from probe calls",
        "attempts": attempts,
    }


def cmd_detect_store_mode(args: argparse.Namespace) -> None:
    data = detect_store_mode(resolve_token(args), args.store_id, args.language)
    if data.get("code") != 200:
        print_json(data)
        sys.exit(1)
    maybe_output(args, data)


def cmd_products_auto(args: argparse.Namespace) -> None:
    token = resolve_token(args)
    detected = detect_store_mode(token, args.store_id, args.language)
    if detected.get("code") != 200:
        print_json(detected)
        sys.exit(1)
    mode = detected["result"]["mode"]
    path_style = "/sync/products" if mode == "connected" else "/store/products"
    path = with_query(path_style, offset=args.offset, limit=args.limit)
    data = request("GET", path, token, language=args.language, store_id=args.store_id)
    payload = {"detected_mode": detected["result"], "data": data}
    maybe_output(args, payload)


def cmd_export_products(args: argparse.Namespace) -> None:
    token = resolve_token(args)
    detected = detect_store_mode(token, args.store_id, args.language)
    if detected.get("code") != 200:
        print_json(detected)
        sys.exit(1)
    mode = detected["result"]["mode"]
    path_style = "/sync/products" if mode == "connected" else "/store/products"
    path = with_query(path_style, offset=args.offset, limit=args.limit)
    data = request("GET", path, token, language=args.language, store_id=args.store_id)
    rows = extract_product_rows(data)
    summary = summarize_product_rows(rows)
    title = args.title or f"Printful store {args.store_id} products"
    markdown = format_products_markdown(rows, summary, title)
    if args.format == "markdown":
        write_text_file(args.output_file, markdown)
    elif args.format == "csv":
        write_csv(args.output_file, rows)
    else:
        dump_json_file(args.output_file, {"detected_mode": detected["result"], "summary": summary, "products": rows})
    maybe_output(args, {"detected_mode": detected["result"], "summary": summary, "output_file": args.output_file, "format": args.format})


def cmd_sync_product(args: argparse.Namespace) -> None:
    command_get(args, f"{args.path_style}/{args.product_id}")


def cmd_sync_variant(args: argparse.Namespace) -> None:
    command_get(args, f"{args.path_style}/{args.variant_id}")


def cmd_create_sync_product(args: argparse.Namespace) -> None:
    command_send(args, "POST", args.path_style)


def cmd_update_sync_product(args: argparse.Namespace) -> None:
    command_send(args, "PUT", f"{args.path_style}/{args.product_id}")


def cmd_delete_sync_product(args: argparse.Namespace) -> None:
    command_send(args, "DELETE", f"{args.path_style}/{args.product_id}")


def cmd_create_sync_variant(args: argparse.Namespace) -> None:
    command_send(args, "POST", args.path_style)


def cmd_update_sync_variant(args: argparse.Namespace) -> None:
    command_send(args, "PUT", f"{args.path_style}/{args.variant_id}")


def cmd_delete_sync_variant(args: argparse.Namespace) -> None:
    command_send(args, "DELETE", f"{args.path_style}/{args.variant_id}")


def cmd_orders(args: argparse.Namespace) -> None:
    path = with_query("/orders", offset=args.offset, limit=args.limit, status=args.status)
    command_get(args, path)


def cmd_order(args: argparse.Namespace) -> None:
    command_get(args, f"/orders/{args.order_id}")


def cmd_create_order(args: argparse.Namespace) -> None:
    command_send(args, "POST", "/orders")


def cmd_update_order(args: argparse.Namespace) -> None:
    command_send(args, "PUT", f"/orders/{args.order_id}")


def cmd_cancel_order(args: argparse.Namespace) -> None:
    command_send(args, "DELETE", f"/orders/{args.order_id}")


def cmd_confirm_order(args: argparse.Namespace) -> None:
    command_send(args, "POST", f"/orders/{args.order_id}/confirm")


def cmd_estimate_order(args: argparse.Namespace) -> None:
    command_send(args, "POST", "/orders/estimate-costs")


def cmd_catalog_products(args: argparse.Namespace) -> None:
    path = with_query("/products", offset=args.offset, limit=args.limit, category_id=args.category_id)
    command_get(args, path)


def cmd_catalog_product(args: argparse.Namespace) -> None:
    command_get(args, f"/products/{args.product_id}")


def cmd_catalog_variant(args: argparse.Namespace) -> None:
    command_get(args, f"/products/variant/{args.variant_id}")


def cmd_categories(args: argparse.Namespace) -> None:
    command_get(args, "/categories")


def cmd_category(args: argparse.Namespace) -> None:
    command_get(args, f"/categories/{args.category_id}")


def cmd_size_guide(args: argparse.Namespace) -> None:
    command_get(args, f"/products/{args.product_id}/sizes")


def cmd_templates(args: argparse.Namespace) -> None:
    path = with_query("/product-templates", offset=args.offset, limit=args.limit)
    command_get(args, path)


def cmd_template(args: argparse.Namespace) -> None:
    command_get(args, f"/product-templates/{args.template_id}")


def cmd_delete_template(args: argparse.Namespace) -> None:
    command_send(args, "DELETE", f"/product-templates/{args.template_id}")


def cmd_files_get(args: argparse.Namespace) -> None:
    command_get(args, f"/files/{args.file_id}")


def cmd_files_add(args: argparse.Namespace) -> None:
    command_send(args, "POST", "/files")


def cmd_thread_colors(args: argparse.Namespace) -> None:
    command_send(args, "POST", "/thread-colors")


def cmd_shipping_rates(args: argparse.Namespace) -> None:
    command_send(args, "POST", "/shipping/rates")


def cmd_webhooks_get(args: argparse.Namespace) -> None:
    command_get(args, "/webhooks")


def cmd_webhooks_set(args: argparse.Namespace) -> None:
    command_send(args, "POST", "/webhooks")


def cmd_webhooks_delete(args: argparse.Namespace) -> None:
    command_send(args, "DELETE", "/webhooks")


def cmd_mockup_printfiles(args: argparse.Namespace) -> None:
    path = f"/mockup-generator/printfiles/{args.variant_id}"
    if args.technique:
        path = with_query(path, technique=args.technique)
    command_get(args, path)


def cmd_mockup_templates(args: argparse.Namespace) -> None:
    path = f"/mockup-generator/templates/{args.variant_id}"
    if args.technique:
        path = with_query(path, technique=args.technique)
    command_get(args, path)


def cmd_mockup_create(args: argparse.Namespace) -> None:
    command_send(args, "POST", "/mockup-generator/create-task")


def cmd_mockup_task(args: argparse.Namespace) -> None:
    command_get(args, f"/mockup-generator/task?task_key={urllib.parse.quote(str(args.task_key), safe='')}")


def cmd_warehouse_products(args: argparse.Namespace) -> None:
    path = with_query("/warehouse/products", offset=args.offset, limit=args.limit)
    command_get(args, path)


def cmd_warehouse_product(args: argparse.Namespace) -> None:
    command_get(args, f"/warehouse/products/{args.warehouse_product_id}")


def cmd_country_codes(args: argparse.Namespace) -> None:
    command_get(args, "/countries")


def cmd_tax_countries(args: argparse.Namespace) -> None:
    command_get(args, "/tax/countries")


def cmd_tax_rate(args: argparse.Namespace) -> None:
    command_send(args, "POST", "/tax/rates")


def cmd_statistics(args: argparse.Namespace) -> None:
    path = with_query("/reports/statistics", date_from=args.date_from, date_to=args.date_to)
    command_get(args, path)


def cmd_approval_sheets(args: argparse.Namespace) -> None:
    path = with_query("/approval-sheets", offset=args.offset, limit=args.limit)
    command_get(args, path)


def cmd_approve_design(args: argparse.Namespace) -> None:
    command_send(args, "POST", f"/approval-sheets/{args.sheet_id}/approve")


def cmd_submit_sheet_changes(args: argparse.Namespace) -> None:
    command_send(args, "POST", f"/approval-sheets/{args.sheet_id}/changes")


def normalize_raw_path(path: str) -> str:
    return path if path.startswith("/") else f"/{path}"


def cmd_raw(args: argparse.Namespace) -> None:
    command_send(args, args.method, normalize_raw_path(args.path))


def add_body_inputs(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--body", help="Inline JSON body")
    parser.add_argument("--body-file", help="Path to JSON body file")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Expanded Printful API helper")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("scopes", help="Get scopes available to the current token")
    add_common_auth(p)
    p.set_defaults(func=cmd_scopes)

    p = sub.add_parser("stores", help="List stores available to the token")
    add_common_auth(p)
    p.set_defaults(func=cmd_stores)

    p = sub.add_parser("store", help="Get one store")
    add_common_auth(p)
    p.add_argument("--store-id", required=True, type=int)
    p.set_defaults(func=cmd_store)

    p = sub.add_parser("detect-store-mode", help="Detect whether a store uses connected-platform sync endpoints or manual/API-store endpoints")
    add_common_auth(p)
    add_store_context(p, required=True)
    p.set_defaults(func=cmd_detect_store_mode)

    p = sub.add_parser("products-auto", help="List products after auto-detecting connected vs manual store mode")
    add_common_auth(p)
    add_store_context(p, required=True)
    add_paging(p, default_limit=20)
    p.set_defaults(func=cmd_products_auto)

    p = sub.add_parser("export-products", help="Auto-detect store mode and export product summary/report to markdown, csv, or json")
    add_common_auth(p)
    add_store_context(p, required=True)
    add_paging(p, default_limit=100)
    p.add_argument("--format", choices=["markdown", "csv", "json"], default="markdown")
    p.add_argument("--output-file", required=True)
    p.add_argument("--title", help="Optional markdown report title")
    p.set_defaults(func=cmd_export_products)

    for name, product_path, variant_path, help_prefix in [
        ("sync", "/sync/products", "/sync/variants", "Ecommerce-platform sync endpoints; best for Etsy and other connected stores"),
        ("manual", "/store/products", "/store/variants", "Manual/API store endpoints; best for API/manual-order stores"),
    ]:
        p = sub.add_parser(f"{name}-products", help=f"List {help_prefix.lower()}")
        add_common_auth(p)
        add_store_context(p, required=True)
        add_paging(p, default_limit=20)
        p.set_defaults(func=cmd_sync_products, path_style=product_path)

        p = sub.add_parser(f"{name}-product", help=f"Get one product via {help_prefix.lower()}")
        add_common_auth(p)
        add_store_context(p, required=True)
        p.add_argument("--product-id", required=True, type=int)
        p.set_defaults(func=cmd_sync_product, path_style=product_path)

        p = sub.add_parser(f"create-{name}-product", help=f"Create a product via {help_prefix.lower()}")
        add_common_auth(p)
        add_store_context(p, required=True)
        add_body_inputs(p)
        p.set_defaults(func=cmd_create_sync_product, path_style=product_path)

        p = sub.add_parser(f"update-{name}-product", help=f"Update a product via {help_prefix.lower()}")
        add_common_auth(p)
        add_store_context(p, required=True)
        p.add_argument("--product-id", required=True, type=int)
        add_body_inputs(p)
        p.set_defaults(func=cmd_update_sync_product, path_style=product_path)

        p = sub.add_parser(f"delete-{name}-product", help=f"Delete a product via {help_prefix.lower()}")
        add_common_auth(p)
        add_store_context(p, required=True)
        p.add_argument("--product-id", required=True, type=int)
        p.set_defaults(func=cmd_delete_sync_product, path_style=product_path)

        p = sub.add_parser(f"{name}-variant", help=f"Get one variant via {help_prefix.lower()}")
        add_common_auth(p)
        add_store_context(p, required=True)
        p.add_argument("--variant-id", required=True, type=int)
        p.set_defaults(func=cmd_sync_variant, path_style=variant_path)

        p = sub.add_parser(f"create-{name}-variant", help=f"Create a variant via {help_prefix.lower()}")
        add_common_auth(p)
        add_store_context(p, required=True)
        add_body_inputs(p)
        p.set_defaults(func=cmd_create_sync_variant, path_style=variant_path)

        p = sub.add_parser(f"update-{name}-variant", help=f"Update a variant via {help_prefix.lower()}")
        add_common_auth(p)
        add_store_context(p, required=True)
        p.add_argument("--variant-id", required=True, type=int)
        add_body_inputs(p)
        p.set_defaults(func=cmd_update_sync_variant, path_style=variant_path)

        p = sub.add_parser(f"delete-{name}-variant", help=f"Delete a variant via {help_prefix.lower()}")
        add_common_auth(p)
        add_store_context(p, required=True)
        p.add_argument("--variant-id", required=True, type=int)
        p.set_defaults(func=cmd_delete_sync_variant, path_style=variant_path)

    p = sub.add_parser("orders", help="List orders")
    add_common_auth(p)
    add_store_context(p)
    add_paging(p, default_limit=20)
    p.add_argument("--status", help="Optional status filter if supported by the API")
    p.set_defaults(func=cmd_orders)

    p = sub.add_parser("order", help="Get one order")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--order-id", required=True)
    p.set_defaults(func=cmd_order)

    p = sub.add_parser("create-order", help="Create a new order")
    add_common_auth(p)
    add_store_context(p)
    add_body_inputs(p)
    p.set_defaults(func=cmd_create_order)

    p = sub.add_parser("update-order", help="Update an order")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--order-id", required=True)
    add_body_inputs(p)
    p.set_defaults(func=cmd_update_order)

    p = sub.add_parser("cancel-order", help="Cancel an order")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--order-id", required=True)
    p.set_defaults(func=cmd_cancel_order)

    p = sub.add_parser("confirm-order", help="Confirm a draft order for fulfillment")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--order-id", required=True)
    p.set_defaults(func=cmd_confirm_order)

    p = sub.add_parser("estimate-order", help="Estimate order costs")
    add_common_auth(p)
    add_store_context(p)
    add_body_inputs(p)
    p.set_defaults(func=cmd_estimate_order)

    p = sub.add_parser("catalog-products", help="List catalog products")
    add_common_auth(p)
    add_store_context(p)
    add_paging(p, default_limit=20)
    p.add_argument("--category-id", type=int)
    p.set_defaults(func=cmd_catalog_products)

    p = sub.add_parser("catalog-product", help="Get one catalog product")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--product-id", required=True, type=int)
    p.set_defaults(func=cmd_catalog_product)

    p = sub.add_parser("catalog-variant", help="Get one catalog variant")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--variant-id", required=True, type=int)
    p.set_defaults(func=cmd_catalog_variant)

    p = sub.add_parser("size-guide", help="Get a catalog product size guide")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--product-id", required=True, type=int)
    p.set_defaults(func=cmd_size_guide)

    p = sub.add_parser("categories", help="List categories")
    add_common_auth(p)
    add_store_context(p)
    p.set_defaults(func=cmd_categories)

    p = sub.add_parser("category", help="Get one category")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--category-id", required=True, type=int)
    p.set_defaults(func=cmd_category)

    p = sub.add_parser("templates", help="List product templates")
    add_common_auth(p)
    add_store_context(p)
    add_paging(p, default_limit=20)
    p.set_defaults(func=cmd_templates)

    p = sub.add_parser("template", help="Get one product template")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--template-id", required=True, type=int)
    p.set_defaults(func=cmd_template)

    p = sub.add_parser("delete-template", help="Delete one product template")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--template-id", required=True, type=int)
    p.set_defaults(func=cmd_delete_template)

    p = sub.add_parser("file", help="Get one file by ID")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--file-id", required=True, type=int)
    p.set_defaults(func=cmd_files_get)

    p = sub.add_parser("add-file", help="Add a file to the Printful file library")
    add_common_auth(p)
    add_store_context(p)
    add_body_inputs(p)
    p.set_defaults(func=cmd_files_add)

    p = sub.add_parser("thread-colors", help="Suggest thread colors from an image URL payload")
    add_common_auth(p)
    add_store_context(p)
    add_body_inputs(p)
    p.set_defaults(func=cmd_thread_colors)

    p = sub.add_parser("shipping-rates", help="Calculate shipping rates")
    add_common_auth(p)
    add_store_context(p)
    add_body_inputs(p)
    p.set_defaults(func=cmd_shipping_rates)

    p = sub.add_parser("webhooks", help="Get webhook configuration")
    add_common_auth(p)
    add_store_context(p)
    p.set_defaults(func=cmd_webhooks_get)

    p = sub.add_parser("set-webhooks", help="Set webhook configuration")
    add_common_auth(p)
    add_store_context(p)
    add_body_inputs(p)
    p.set_defaults(func=cmd_webhooks_set)

    p = sub.add_parser("delete-webhooks", help="Disable webhook support")
    add_common_auth(p)
    add_store_context(p)
    p.set_defaults(func=cmd_webhooks_delete)

    p = sub.add_parser("mockup-printfiles", help="Get mockup printfiles for a variant")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--variant-id", required=True, type=int)
    p.add_argument("--technique")
    p.set_defaults(func=cmd_mockup_printfiles)

    p = sub.add_parser("mockup-templates", help="Get layout templates for a variant")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--variant-id", required=True, type=int)
    p.add_argument("--technique")
    p.set_defaults(func=cmd_mockup_templates)

    p = sub.add_parser("create-mockup-task", help="Create a mockup generation task")
    add_common_auth(p)
    add_store_context(p)
    add_body_inputs(p)
    p.set_defaults(func=cmd_mockup_create)

    p = sub.add_parser("mockup-task", help="Get a mockup generation task result")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--task-key", required=True)
    p.set_defaults(func=cmd_mockup_task)

    p = sub.add_parser("warehouse-products", help="List warehouse products")
    add_common_auth(p)
    add_store_context(p)
    add_paging(p, default_limit=20)
    p.set_defaults(func=cmd_warehouse_products)

    p = sub.add_parser("warehouse-product", help="Get one warehouse product")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--warehouse-product-id", required=True, type=int)
    p.set_defaults(func=cmd_warehouse_product)

    p = sub.add_parser("country-codes", help="List countries")
    add_common_auth(p)
    add_store_context(p)
    p.set_defaults(func=cmd_country_codes)

    p = sub.add_parser("tax-countries", help="List countries supported for tax calculation")
    add_common_auth(p)
    add_store_context(p)
    p.set_defaults(func=cmd_tax_countries)

    p = sub.add_parser("tax-rate", help="Calculate tax rate")
    add_common_auth(p)
    add_store_context(p)
    add_body_inputs(p)
    p.set_defaults(func=cmd_tax_rate)

    p = sub.add_parser("statistics", help="Get statistics report")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--date-from", help="Date or timestamp string if supported")
    p.add_argument("--date-to", help="Date or timestamp string if supported")
    p.set_defaults(func=cmd_statistics)

    p = sub.add_parser("approval-sheets", help="List approval sheets")
    add_common_auth(p)
    add_store_context(p)
    add_paging(p, default_limit=20)
    p.set_defaults(func=cmd_approval_sheets)

    p = sub.add_parser("approve-design", help="Approve a design on an approval sheet")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--sheet-id", required=True)
    add_body_inputs(p)
    p.set_defaults(func=cmd_approve_design)

    p = sub.add_parser("submit-sheet-changes", help="Submit changes to an approval sheet")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("--sheet-id", required=True)
    add_body_inputs(p)
    p.set_defaults(func=cmd_submit_sheet_changes)

    p = sub.add_parser("raw", help="Send an arbitrary Printful API request")
    add_common_auth(p)
    add_store_context(p)
    p.add_argument("method", choices=["GET", "POST", "PUT", "DELETE", "PATCH"])
    p.add_argument("path", help="API path like /stores or /sync/products?limit=10")
    add_body_inputs(p)
    p.set_defaults(func=cmd_raw)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import argparse
import csv
import http.server
import json
import os
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, Optional

AUTH_BASE = "https://miro.com/oauth/authorize"
TOKEN_URL = "https://api.miro.com/v1/oauth/token"
API_BASE = "https://api.miro.com/v2"


def print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: str, data: Any) -> None:
    p = Path(path)
    ensure_parent(p)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: str, text: str) -> None:
    p = Path(path)
    ensure_parent(p)
    p.write_text(text, encoding="utf-8")


def resolve_env_or_arg(args: argparse.Namespace, arg_name: str, env_name: str, required: bool = True) -> Optional[str]:
    value = getattr(args, arg_name, None) or os.environ.get(env_name)
    if required and not value:
        print(f"Missing {arg_name}. Pass --{arg_name.replace('_','-')} or set {env_name}.", file=sys.stderr)
        sys.exit(2)
    return value


def load_tokens(token_file: str) -> Dict[str, Any]:
    path = Path(token_file)
    if not path.exists():
        print(f"Token file not found: {token_file}", file=sys.stderr)
        sys.exit(2)
    return json.loads(path.read_text(encoding="utf-8"))


def save_tokens(token_file: str, data: Dict[str, Any]) -> None:
    write_json(token_file, data)


def resolve_access_token(args: argparse.Namespace) -> str:
    direct = getattr(args, "access_token", None) or os.environ.get("MIRO_ACCESS_TOKEN")
    if direct:
        return direct
    token_file = getattr(args, "token_file", None)
    if token_file:
        tokens = load_tokens(token_file)
        token = tokens.get("access_token")
        if token:
            return token
    print("Missing access token. Pass --access-token, set MIRO_ACCESS_TOKEN, or use --token-file.", file=sys.stderr)
    sys.exit(2)


def maybe_output(args: argparse.Namespace, data: Any) -> None:
    print_json(data)
    output = getattr(args, "output", None)
    if output:
        write_json(output, data)


def build_auth_url(client_id: str, redirect_uri: str) -> str:
    params = urllib.parse.urlencode({
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
    })
    return f"{AUTH_BASE}?{params}"


def token_request(params: Dict[str, str]) -> Dict[str, Any]:
    url = TOKEN_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body) if body else {"error": str(e)}
        except json.JSONDecodeError:
            parsed = {"error": body or str(e)}
        print_json(parsed)
        sys.exit(1)


def exchange_code(client_id: str, client_secret: str, redirect_uri: str, code: str) -> Dict[str, Any]:
    return token_request({
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    })


def refresh_token(client_id: str, client_secret: str, refresh_token_value: str) -> Dict[str, Any]:
    return token_request({
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token_value,
    })


def load_body(args: argparse.Namespace) -> Optional[Any]:
    if getattr(args, "body_file", None):
        return json.loads(Path(args.body_file).read_text(encoding="utf-8"))
    if getattr(args, "body", None):
        return json.loads(args.body)
    return None


def api_request(method: str, path: str, access_token: str, body: Optional[Any] = None) -> Dict[str, Any]:
    if not path.startswith("/"):
        path = "/" + path
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(API_BASE + path, headers=headers, data=data, method=method.upper())
    try:
        with urllib.request.urlopen(req) as resp:
            payload = resp.read().decode("utf-8", errors="replace")
            return json.loads(payload) if payload else {"status": resp.status}
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(body_text) if body_text else {"error": str(e)}
        except json.JSONDecodeError:
            parsed = {"error": body_text or str(e)}
        print_json(parsed)
        sys.exit(1)


def item_rows(items_payload: Dict[str, Any]) -> list[Dict[str, Any]]:
    rows = []
    for item in items_payload.get("data", []):
        data = item.get("data", {})
        position = item.get("position", {})
        geometry = item.get("geometry", {})
        rows.append({
            "id": item.get("id"),
            "type": item.get("type"),
            "content": data.get("content", ""),
            "title": data.get("title", ""),
            "shape": data.get("shape", ""),
            "x": position.get("x"),
            "y": position.get("y"),
            "width": geometry.get("width"),
            "height": geometry.get("height"),
        })
    return rows


def write_items_csv(path: str, rows: list[Dict[str, Any]]) -> None:
    p = Path(path)
    ensure_parent(p)
    with p.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "type", "content", "title", "shape", "x", "y", "width", "height"])
        writer.writeheader()
        writer.writerows(rows)


def write_items_markdown(path: str, board_id: str, rows: list[Dict[str, Any]]) -> None:
    lines = [f"# Miro board items: {board_id}", "", f"- Total items: {len(rows)}", "", "## Items", ""]
    for row in rows:
        label = row["content"] or row["title"] or "(no text)"
        lines.append(f"- **{row['type']}** `{row['id']}` at ({row['x']}, {row['y']}) — {label}")
    lines.append("")
    write_text(path, "\n".join(lines))


def cmd_auth_url(args: argparse.Namespace) -> None:
    client_id = resolve_env_or_arg(args, "client_id", "MIRO_CLIENT_ID")
    redirect_uri = resolve_env_or_arg(args, "redirect_uri", "MIRO_REDIRECT_URI")
    print(build_auth_url(client_id, redirect_uri))


def cmd_exchange_code(args: argparse.Namespace) -> None:
    client_id = resolve_env_or_arg(args, "client_id", "MIRO_CLIENT_ID")
    client_secret = resolve_env_or_arg(args, "client_secret", "MIRO_CLIENT_SECRET")
    redirect_uri = resolve_env_or_arg(args, "redirect_uri", "MIRO_REDIRECT_URI")
    data = exchange_code(client_id, client_secret, redirect_uri, args.code)
    if args.token_file:
        save_tokens(args.token_file, data)
    maybe_output(args, data)


def cmd_refresh_token(args: argparse.Namespace) -> None:
    client_id = resolve_env_or_arg(args, "client_id", "MIRO_CLIENT_ID")
    client_secret = resolve_env_or_arg(args, "client_secret", "MIRO_CLIENT_SECRET")
    tokens = load_tokens(args.token_file)
    data = refresh_token(client_id, client_secret, tokens["refresh_token"])
    save_tokens(args.token_file, data)
    maybe_output(args, data)


def cmd_whoami(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    maybe_output(args, api_request("GET", "/boards?limit=1", access_token))


def cmd_list_boards(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    path = f"/boards?limit={args.limit}"
    maybe_output(args, api_request("GET", path, access_token))


def cmd_get_board(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    maybe_output(args, api_request("GET", f"/boards/{args.board_id}", access_token))


def cmd_create_board(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    body = {"name": args.name}
    if args.description is not None:
        body["description"] = args.description
    maybe_output(args, api_request("POST", "/boards", access_token, body))


def cmd_list_board_items(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    path = f"/boards/{args.board_id}/items?limit={args.limit}"
    if args.type:
        path += f"&type={urllib.parse.quote(args.type, safe='')}"
    maybe_output(args, api_request("GET", path, access_token))


def cmd_export_board_items(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    path = f"/boards/{args.board_id}/items?limit={args.limit}"
    payload = api_request("GET", path, access_token)
    rows = item_rows(payload)
    if args.format == "json":
        write_json(args.output_file, payload)
    elif args.format == "csv":
        write_items_csv(args.output_file, rows)
    else:
        write_items_markdown(args.output_file, args.board_id, rows)
    maybe_output(args, {"board_id": args.board_id, "format": args.format, "output_file": args.output_file, "count": len(rows)})


def cmd_create_sticky_note(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    body = {
        "data": {"content": args.content},
        "style": {"fillColor": args.fill_color, "textAlign": "center", "textAlignVertical": "middle"},
        "position": {"x": args.x, "y": args.y, "origin": "center"},
        "geometry": {"width": args.width},
    }
    maybe_output(args, api_request("POST", f"/boards/{args.board_id}/sticky_notes", access_token, body))


def cmd_update_sticky_note(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    body: Dict[str, Any] = {}
    if args.content is not None:
        body["data"] = {"content": args.content}
    if args.fill_color is not None:
        body.setdefault("style", {})["fillColor"] = args.fill_color
    if args.x is not None or args.y is not None:
        body["position"] = {"x": args.x if args.x is not None else 0, "y": args.y if args.y is not None else 0, "origin": "center"}
    maybe_output(args, api_request("PATCH", f"/boards/{args.board_id}/sticky_notes/{args.item_id}", access_token, body))


def cmd_create_text(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    body = {
        "data": {"content": args.content},
        "position": {"x": args.x, "y": args.y, "origin": "center"},
        "geometry": {"width": args.width},
    }
    maybe_output(args, api_request("POST", f"/boards/{args.board_id}/texts", access_token, body))


def cmd_update_text(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    body: Dict[str, Any] = {}
    if args.content is not None:
        body["data"] = {"content": args.content}
    if args.x is not None or args.y is not None:
        body["position"] = {"x": args.x if args.x is not None else 0, "y": args.y if args.y is not None else 0, "origin": "center"}
    maybe_output(args, api_request("PATCH", f"/boards/{args.board_id}/texts/{args.item_id}", access_token, body))


def cmd_create_shape(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    body = {
        "data": {"shape": args.shape, "content": args.content},
        "style": {"fillColor": args.fill_color},
        "position": {"x": args.x, "y": args.y, "origin": "center"},
        "geometry": {"width": args.width, "height": args.height},
    }
    maybe_output(args, api_request("POST", f"/boards/{args.board_id}/shapes", access_token, body))


def cmd_update_shape(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    body: Dict[str, Any] = {}
    if args.content is not None or args.shape is not None:
        body["data"] = {}
        if args.content is not None:
            body["data"]["content"] = args.content
        if args.shape is not None:
            body["data"]["shape"] = args.shape
    if args.fill_color is not None:
        body.setdefault("style", {})["fillColor"] = args.fill_color
    if args.x is not None or args.y is not None:
        body["position"] = {"x": args.x if args.x is not None else 0, "y": args.y if args.y is not None else 0, "origin": "center"}
    maybe_output(args, api_request("PATCH", f"/boards/{args.board_id}/shapes/{args.item_id}", access_token, body))


def cmd_create_card(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    body = {
        "data": {"title": args.title, "description": args.description or ""},
        "position": {"x": args.x, "y": args.y, "origin": "center"},
        "geometry": {"width": args.width},
    }
    maybe_output(args, api_request("POST", f"/boards/{args.board_id}/cards", access_token, body))


def cmd_update_card(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    body: Dict[str, Any] = {"data": {}}
    if args.title is not None:
        body["data"]["title"] = args.title
    if args.description is not None:
        body["data"]["description"] = args.description
    if not body["data"]:
        body.pop("data")
    if args.x is not None or args.y is not None:
        body["position"] = {"x": args.x if args.x is not None else 0, "y": args.y if args.y is not None else 0, "origin": "center"}
    maybe_output(args, api_request("PATCH", f"/boards/{args.board_id}/cards/{args.item_id}", access_token, body))


def cmd_create_brainstorm_cluster(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    created = []
    spacing = args.spacing
    for idx, text in enumerate(args.notes):
        body = {
            "data": {"content": text},
            "style": {"fillColor": args.fill_color, "textAlign": "center", "textAlignVertical": "middle"},
            "position": {"x": args.x + (idx * spacing), "y": args.y, "origin": "center"},
            "geometry": {"width": args.width},
        }
        created.append(api_request("POST", f"/boards/{args.board_id}/sticky_notes", access_token, body))
    maybe_output(args, {"created": created, "count": len(created)})


def cmd_create_kanban_row(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    headers = []
    cards = []
    columns = [c.strip() for c in args.columns.split(",") if c.strip()]
    for idx, name in enumerate(columns):
        x = args.x + (idx * args.column_spacing)
        headers.append(api_request("POST", f"/boards/{args.board_id}/shapes", access_token, {
            "data": {"shape": "rectangle", "content": name},
            "style": {"fillColor": args.header_color},
            "position": {"x": x, "y": args.y, "origin": "center"},
            "geometry": {"width": args.header_width, "height": args.header_height},
        }))
        cards.append(api_request("POST", f"/boards/{args.board_id}/cards", access_token, {
            "data": {"title": f"{name} task", "description": ""},
            "position": {"x": x, "y": args.y + args.card_offset_y, "origin": "center"},
            "geometry": {"width": args.card_width},
        }))
    maybe_output(args, {"headers": headers, "cards": cards, "count": len(columns)})


def cmd_create_architecture_chain(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    labels = [c.strip() for c in args.labels.split(",") if c.strip()]
    shapes = []
    connectors = []
    prev_id = None
    for idx, label in enumerate(labels):
        x = args.x + (idx * args.spacing)
        shape = api_request("POST", f"/boards/{args.board_id}/shapes", access_token, {
            "data": {"shape": "rectangle", "content": label},
            "style": {"fillColor": args.fill_color},
            "position": {"x": x, "y": args.y, "origin": "center"},
            "geometry": {"width": args.width, "height": args.height},
        })
        shapes.append(shape)
        current_id = shape.get("id")
        if prev_id and current_id:
            connectors.append(api_request("POST", f"/boards/{args.board_id}/connectors", access_token, {
                "startItem": {"id": prev_id, "snapTo": "right"},
                "endItem": {"id": current_id, "snapTo": "left"},
                "style": {"strokeColor": args.stroke_color, "strokeStyle": "normal"},
            }))
        prev_id = current_id
    maybe_output(args, {"shapes": shapes, "connectors": connectors, "count": len(shapes)})


def cmd_delete_item(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    maybe_output(args, api_request("DELETE", f"/boards/{args.board_id}/{args.item_type}/{args.item_id}", access_token))


def cmd_list_board_members(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    path = f"/boards/{args.board_id}/members?limit={args.limit}"
    maybe_output(args, api_request("GET", path, access_token))


def cmd_create_connector(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    body = {
        "startItem": {"id": args.start_item_id, "snapTo": args.start_snap_to},
        "endItem": {"id": args.end_item_id, "snapTo": args.end_snap_to},
        "style": {"strokeColor": args.stroke_color, "strokeStyle": args.stroke_style},
    }
    maybe_output(args, api_request("POST", f"/boards/{args.board_id}/connectors", access_token, body))


def cmd_get_webhooks(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    maybe_output(args, api_request("GET", "/webhooks", access_token))


def cmd_create_webhook(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    body = load_body(args)
    maybe_output(args, api_request("POST", "/webhooks", access_token, body))


def cmd_delete_webhook(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    maybe_output(args, api_request("DELETE", f"/webhooks/{args.webhook_id}", access_token))


def cmd_preview_write(args: argparse.Namespace) -> None:
    body = load_body(args)
    preview = {
        "mode": "preview-only",
        "method": args.method,
        "path": args.path if args.path.startswith("/") else "/" + args.path,
        "body": body,
        "note": "This command does not send the request. It is for review before a live write.",
    }
    maybe_output(args, preview)


def cmd_raw(args: argparse.Namespace) -> None:
    access_token = resolve_access_token(args)
    maybe_output(args, api_request(args.method, args.path, access_token, load_body(args)))


def cmd_serve_oauth_callback(args: argparse.Namespace) -> None:
    client_id = resolve_env_or_arg(args, "client_id", "MIRO_CLIENT_ID")
    client_secret = resolve_env_or_arg(args, "client_secret", "MIRO_CLIENT_SECRET")
    redirect_uri = resolve_env_or_arg(args, "redirect_uri", "MIRO_REDIRECT_URI")
    parsed = urllib.parse.urlparse(redirect_uri)
    expected_path = parsed.path or "/"
    token_file = args.token_file
    result: Dict[str, Any] = {"done": False}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            url = urllib.parse.urlparse(self.path)
            if url.path != expected_path:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not found")
                return
            qs = urllib.parse.parse_qs(url.query)
            if "error" in qs:
                result["done"] = True
                result["error"] = qs.get("error", [""])[0]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Miro authorization returned an error. You can close this window.")
                return
            code = qs.get("code", [None])[0]
            if not code:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing code")
                return
            token_data = exchange_code(client_id, client_secret, redirect_uri, code)
            save_tokens(token_file, token_data)
            result["done"] = True
            result["token_data"] = token_data
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Miro authorization complete. Tokens saved. You can close this window.")

        def log_message(self, format, *args):
            return

    server = http.server.ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Listening on http://{args.host}:{args.port}{expected_path}")
    print("Open this URL in your browser:")
    print(build_auth_url(client_id, redirect_uri))

    def serve() -> None:
        while not result["done"]:
            server.handle_request()

    thread = threading.Thread(target=serve, daemon=True)
    thread.start()
    thread.join(timeout=args.timeout)
    if not result["done"]:
        print_json({"status": "timeout", "message": "OAuth callback not received before timeout"})
        sys.exit(1)
    print_json(result)


def add_access_args(parser: argparse.ArgumentParser, require_token_file: bool = False) -> None:
    parser.add_argument("--access-token", help="Direct Miro access token; defaults to MIRO_ACCESS_TOKEN env var")
    parser.add_argument("--token-file", required=require_token_file, help="Path to saved token JSON")
    parser.add_argument("--output", help="Write JSON response to a file as well")


def add_position_args(parser: argparse.ArgumentParser, *, defaults: bool = True) -> None:
    if defaults:
        parser.add_argument("--x", type=float, default=0)
        parser.add_argument("--y", type=float, default=0)
    else:
        parser.add_argument("--x", type=float)
        parser.add_argument("--y", type=float)


def add_body_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--body", help="Inline JSON body")
    parser.add_argument("--body-file", help="Path to JSON body file")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Expanded Miro REST API helper")
    sub = p.add_subparsers(dest="command", required=True)

    s = sub.add_parser("auth-url", help="Print the Miro OAuth authorization URL")
    s.add_argument("--client-id")
    s.add_argument("--redirect-uri")
    s.set_defaults(func=cmd_auth_url)

    s = sub.add_parser("serve-oauth-callback", help="Run a local callback server and exchange the returned code for tokens")
    s.add_argument("--client-id")
    s.add_argument("--client-secret")
    s.add_argument("--redirect-uri")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=4000)
    s.add_argument("--timeout", type=int, default=600)
    s.add_argument("--token-file", required=True)
    s.set_defaults(func=cmd_serve_oauth_callback)

    s = sub.add_parser("exchange-code", help="Exchange a copied authorization code for tokens")
    s.add_argument("code")
    s.add_argument("--client-id")
    s.add_argument("--client-secret")
    s.add_argument("--redirect-uri")
    s.add_argument("--token-file")
    s.add_argument("--output")
    s.set_defaults(func=cmd_exchange_code)

    s = sub.add_parser("refresh-token", help="Refresh access token using stored refresh token")
    s.add_argument("--client-id")
    s.add_argument("--client-secret")
    s.add_argument("--token-file", required=True)
    s.add_argument("--output")
    s.set_defaults(func=cmd_refresh_token)

    s = sub.add_parser("whoami", help="Test token access with a lightweight boards call")
    add_access_args(s)
    s.set_defaults(func=cmd_whoami)

    s = sub.add_parser("list-boards", help="List accessible boards")
    add_access_args(s)
    s.add_argument("--limit", type=int, default=20)
    s.set_defaults(func=cmd_list_boards)

    s = sub.add_parser("get-board", help="Get one board")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.set_defaults(func=cmd_get_board)

    s = sub.add_parser("create-board", help="Create a board")
    add_access_args(s)
    s.add_argument("name")
    s.add_argument("--description")
    s.set_defaults(func=cmd_create_board)

    s = sub.add_parser("list-board-items", help="List items on a board")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("--limit", type=int, default=50)
    s.add_argument("--type", help="Optional item type filter")
    s.set_defaults(func=cmd_list_board_items)

    s = sub.add_parser("export-board-items", help="Export board items to markdown, csv, or json")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("--limit", type=int, default=200)
    s.add_argument("--format", choices=["markdown", "csv", "json"], default="markdown")
    s.add_argument("--output-file", required=True)
    s.set_defaults(func=cmd_export_board_items)

    s = sub.add_parser("create-sticky-note", help="Create a sticky note")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("content")
    add_position_args(s)
    s.add_argument("--width", type=float, default=199)
    s.add_argument("--fill-color", default="light_yellow")
    s.set_defaults(func=cmd_create_sticky_note)

    s = sub.add_parser("update-sticky-note", help="Update a sticky note")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("--item-id", required=True)
    s.add_argument("--content")
    add_position_args(s, defaults=False)
    s.add_argument("--fill-color")
    s.set_defaults(func=cmd_update_sticky_note)

    s = sub.add_parser("create-text", help="Create a text item")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("content")
    add_position_args(s)
    s.add_argument("--width", type=float, default=320)
    s.set_defaults(func=cmd_create_text)

    s = sub.add_parser("update-text", help="Update a text item")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("--item-id", required=True)
    s.add_argument("--content")
    add_position_args(s, defaults=False)
    s.set_defaults(func=cmd_update_text)

    s = sub.add_parser("create-shape", help="Create a shape item")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("content")
    s.add_argument("--shape", default="rectangle")
    add_position_args(s)
    s.add_argument("--width", type=float, default=160)
    s.add_argument("--height", type=float, default=120)
    s.add_argument("--fill-color", default="light_blue")
    s.set_defaults(func=cmd_create_shape)

    s = sub.add_parser("update-shape", help="Update a shape item")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("--item-id", required=True)
    s.add_argument("--content")
    s.add_argument("--shape")
    add_position_args(s, defaults=False)
    s.add_argument("--fill-color")
    s.set_defaults(func=cmd_update_shape)

    s = sub.add_parser("create-card", help="Create a card item")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("title")
    s.add_argument("--description")
    add_position_args(s)
    s.add_argument("--width", type=float, default=256)
    s.set_defaults(func=cmd_create_card)

    s = sub.add_parser("update-card", help="Update a card item")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("--item-id", required=True)
    s.add_argument("--title")
    s.add_argument("--description")
    add_position_args(s, defaults=False)
    s.set_defaults(func=cmd_update_card)

    s = sub.add_parser("create-brainstorm-cluster", help="Create a row of sticky notes from multiple ideas")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("notes", nargs="+", help="Sticky note texts")
    add_position_args(s)
    s.add_argument("--spacing", type=float, default=240)
    s.add_argument("--width", type=float, default=199)
    s.add_argument("--fill-color", default="light_yellow")
    s.set_defaults(func=cmd_create_brainstorm_cluster)

    s = sub.add_parser("create-kanban-row", help="Create a simple kanban-style row with headers and seed cards")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("--columns", default="Backlog,Doing,Done")
    add_position_args(s)
    s.add_argument("--column-spacing", type=float, default=420)
    s.add_argument("--header-width", type=float, default=260)
    s.add_argument("--header-height", type=float, default=100)
    s.add_argument("--card-width", type=float, default=256)
    s.add_argument("--card-offset-y", type=float, default=180)
    s.add_argument("--header-color", default="light_blue")
    s.set_defaults(func=cmd_create_kanban_row)

    s = sub.add_parser("create-architecture-chain", help="Create connected architecture boxes from a comma-separated label list")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("--labels", required=True, help="Comma-separated labels, e.g. Client,API,DB")
    add_position_args(s)
    s.add_argument("--spacing", type=float, default=320)
    s.add_argument("--width", type=float, default=180)
    s.add_argument("--height", type=float, default=120)
    s.add_argument("--fill-color", default="light_green")
    s.add_argument("--stroke-color", default="black")
    s.set_defaults(func=cmd_create_architecture_chain)

    s = sub.add_parser("delete-item", help="Delete an item using its type path segment and item id")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("--item-type", required=True, help="Examples: sticky_notes, texts, shapes, cards")
    s.add_argument("--item-id", required=True)
    s.set_defaults(func=cmd_delete_item)

    s = sub.add_parser("list-board-members", help="List board members")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("--limit", type=int, default=50)
    s.set_defaults(func=cmd_list_board_members)

    s = sub.add_parser("create-connector", help="Create a connector between two board items")
    add_access_args(s)
    s.add_argument("--board-id", required=True)
    s.add_argument("--start-item-id", required=True)
    s.add_argument("--end-item-id", required=True)
    s.add_argument("--start-snap-to", default="auto")
    s.add_argument("--end-snap-to", default="auto")
    s.add_argument("--stroke-color", default="black")
    s.add_argument("--stroke-style", default="normal")
    s.set_defaults(func=cmd_create_connector)

    s = sub.add_parser("get-webhooks", help="List webhooks accessible to the token")
    add_access_args(s)
    s.set_defaults(func=cmd_get_webhooks)

    s = sub.add_parser("create-webhook", help="Create a webhook from a JSON body")
    add_access_args(s)
    add_body_args(s)
    s.set_defaults(func=cmd_create_webhook)

    s = sub.add_parser("delete-webhook", help="Delete a webhook by id")
    add_access_args(s)
    s.add_argument("--webhook-id", required=True)
    s.set_defaults(func=cmd_delete_webhook)

    s = sub.add_parser("preview-write", help="Preview a write request without sending it")
    s.add_argument("method", choices=["POST", "PATCH", "PUT", "DELETE"])
    s.add_argument("path")
    s.add_argument("--output", help="Write JSON response to a file as well")
    add_body_args(s)
    s.set_defaults(func=cmd_preview_write)

    s = sub.add_parser("raw", help="Send an arbitrary Miro API request")
    add_access_args(s)
    s.add_argument("method", choices=["GET", "POST", "PATCH", "PUT", "DELETE"])
    s.add_argument("path")
    add_body_args(s)
    s.set_defaults(func=cmd_raw)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

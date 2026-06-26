#!/usr/bin/env python3
"""
美团 AI CLI — 让 AI 完全操控美团 App
支持两种调用方式：
  1. 命令行直接调用（人类用）
  2. HTTP Server（AI Agent 通过 JSON API 调用）

用法（命令行）:
  python cli.py state                      # 查看当前 App 状态
  python cli.py screen                     # 查看当前屏幕所有元素
  python cli.py search "肯德基"            # 搜索餐厅
  python cli.py open 0                     # 进入第 0 家餐厅
  python cli.py waimai                     # 跳转到外卖点菜页
  python cli.py menu                       # 查看外卖菜单
  python cli.py add "香辣鸡腿堡"           # 加购物车
  python cli.py cart                       # 查看购物车
  python cli.py checkout                   # 去结算（停在确认页，不付款）
  python cli.py address                    # 查看收货地址
  python cli.py tap "外卖"                 # 点击任意文字元素
  python cli.py type "汉堡"               # 输入文字
  python cli.py swipe up                  # 滑动屏幕
  python cli.py back                       # 按返回键
  python cli.py serve                      # 启动 HTTP Server（供 AI 调用）

标准外卖工作流（AI 调用顺序）:
  /search?keyword=XX  →  /open?target=0  →  /waimai  →  /menu
  →  /add_to_cart?item=XX  →  /cart  →  /checkout  →  /address

用法（HTTP API，启动 serve 后）:
  GET  /state                              # 当前 App 状态（page/activity/texts）
  GET  /screen                             # 当前屏幕所有 UI 元素
  GET  /search?keyword=肯德基             # 搜索餐厅列表
  GET  /open?target=0                      # 进入第 N 家餐厅
  GET  /waimai                             # 在餐厅详情页进入外卖点菜
  GET  /menu                               # 获取外卖菜单
  GET  /add_to_cart?item=香辣鸡腿堡       # 加购物车（GET 或 POST 均可）
  POST /add_to_cart  body: {"item":"..."}  # 加购物车（POST 方式）
  GET  /cart                               # 查看购物车（菜品+总价）
  GET  /checkout                           # 去结算（返回地址/总价/时间）
  GET  /address                            # 查看当前收货地址
  GET  /food_channel?screens=4             # 浏览美食频道推荐餐厅
  GET  /tap?keyword=外卖                   # 点击元素
  POST /tap_xy       body: {"x":0,"y":0}  # 按坐标点击
  GET  /type?text=汉堡                    # 输入文字
  GET  /swipe?direction=up                 # 滑动（up/down/left/right）
  GET  /back                               # 返回键
  GET  /home                               # Home 键
  GET  /launch                             # 启动美团
  GET  /wait?keyword=外卖&timeout=10       # 等待元素出现

所有 HTTP 响应均为 JSON，格式：
  成功：{"ok": true, ...data}
  失败：{"ok": false, "error": "...", "suggestion": "..."}
"""
import sys
import json
import time
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, __file__.rsplit("/", 1)[0])

import device
import meituan


# ─── 命令行命令 ──────────────────────────────────────────────────────────────

def _out(args, data: dict):
    """统一输出：JSON 或人类可读"""
    if getattr(args, "json", False):
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        if data.get("ok") is False:
            print("ERROR:", data.get("error", "unknown"))
            if data.get("suggestion"):
                print("HINT:", data["suggestion"])
            return
        # 人类可读的简洁输出
        _print_human(data)


def _print_human(data: dict):
    keys = [k for k in data if k != "ok"]
    if not keys:
        print("OK")
        return
    for k in keys:
        v = data[k]
        if isinstance(v, list) and v and isinstance(v[0], dict):
            print(f"\n{k} ({len(v)} 项):")
            for i, item in enumerate(v):
                name = item.get("name") or item.get("text") or str(item)
                price = f"  ¥{item['price']:.1f}" if "price" in item else ""
                rating = f"  ⭐{item['rating']}" if item.get("rating") else ""
                dt = f"  {item['delivery_time']}" if item.get("delivery_time") else ""
                print(f"  [{i}] {name}{price}{rating}{dt}")
        elif isinstance(v, list) and v and isinstance(v[0], str):
            print(f"\n{k}:")
            for s in v:
                print(f"  - {s}")
        elif isinstance(v, dict):
            print(f"\n{k}:")
            for kk, vv in v.items():
                print(f"  {kk}: {vv}")
        else:
            print(f"{k}: {v}")


def cmd_state(args):
    """查看当前 App 状态"""
    data = meituan.get_app_state()
    data["ok"] = True
    _out(args, data)


def cmd_screen(args):
    """读取当前屏幕所有 UI 元素"""
    els = device.dump_screen()
    visible = [e for e in els if e.get("text") or e.get("desc")]
    if getattr(args, "json", False):
        print(json.dumps({"ok": True, "elements": visible, "count": len(visible)},
                         ensure_ascii=False, indent=2))
    else:
        print(f"当前屏幕共 {len(visible)} 个元素:\n")
        for e in visible:
            t = e.get("text") or e.get("desc")
            click = "●" if e["clickable"] else " "
            print(f"  {click} [{e['type']:20s}] {t[:40]:40s}  ({e['cx']},{e['cy']})")


def cmd_search(args):
    """搜索外卖餐厅"""
    try:
        results = meituan.search_restaurants(args.keyword)
        data = {"ok": True, "restaurants": results, "count": len(results)}
        _out(args, data)
    except RuntimeError as e:
        _out(args, {"ok": False, "error": str(e), "suggestion": "请在手机上手动完成验证后重试"})


def cmd_open(args):
    """进入餐厅（按序号或名字）"""
    try:
        target = int(args.target)
    except ValueError:
        target = args.target
    ok = meituan.open_restaurant(target)
    if ok:
        time.sleep(1)
        state = meituan.get_app_state()
        _out(args, {"ok": True, "message": "已进入餐厅", "current_page": state["page"]})
    else:
        _out(args, {"ok": False, "error": f"未找到: {args.target}",
                    "suggestion": "先用 search 搜索，再用 open 0 进入第一个结果"})


def cmd_menu(args):
    """查看当前餐厅菜单"""
    items = meituan.get_menu()
    if not items:
        _out(args, {"ok": False, "error": "未解析到菜单",
                    "suggestion": "先用 open 进入餐厅，确认当前在餐厅菜单页"})
        return
    _out(args, {"ok": True, "menu": items, "count": len(items)})


def cmd_add(args):
    """加入购物车"""
    ok = meituan.add_to_cart(args.item)
    if ok:
        _out(args, {"ok": True, "message": f"已加入购物车: {args.item}"})
    else:
        _out(args, {"ok": False, "error": f"未找到菜品: {args.item}",
                    "suggestion": "先用 menu 获取菜单，确认菜品名称"})


def cmd_cart(args):
    """查看购物车"""
    cart = meituan.view_cart()
    _out(args, {"ok": True, **cart})


def cmd_checkout(args):
    """去结算（停在确认订单页，不自动付款）"""
    res = meituan.go_to_checkout()
    if isinstance(res, dict) and not res.get("ok"):
        _out(args, res)
    else:
        _out(args, {"ok": True, "message": "已进入结算页，请在手机上确认付款", **(res if isinstance(res, dict) else {})})


def cmd_tap(args):
    """点击指定文字的元素"""
    els = device.dump_screen()
    ok = device.tap_element(els, args.keyword)
    if ok:
        time.sleep(0.5)
        _out(args, {"ok": True, "tapped": args.keyword})
    else:
        _out(args, {"ok": False, "error": f"未找到元素: {args.keyword}"})


def cmd_type(args):
    """输入文字"""
    device.type_text(args.text)
    _out(args, {"ok": True, "typed": args.text})


def cmd_swipe(args):
    """滑动屏幕"""
    device.swipe(args.direction, distance=int(args.distance))
    _out(args, {"ok": True, "direction": args.direction})


def cmd_back(args):
    """按返回键"""
    device.press_back()
    _out(args, {"ok": True, "action": "back"})


def cmd_launch(args):
    """启动美团"""
    device.launch_meituan()
    time.sleep(3)
    pkg = device.get_focused_app()
    ok = "meituan" in pkg
    _out(args, {"ok": ok, "focused_app": pkg})


# ─── HTTP Server（AI Agent 调用）────────────────────────────────────────────

def _make_error(msg: str, suggestion: str = "") -> dict:
    d = {"ok": False, "error": msg}
    if suggestion:
        d["suggestion"] = suggestion
    return d


class AIHandler(BaseHTTPRequestHandler):
    """AI 通过 HTTP 调用的接口"""

    def log_message(self, format, *args):
        pass  # 静默日志

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        result = self._dispatch(path, params)
        self._send_json(result)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            params = json.loads(body)
        except Exception:
            params = {}
        parsed = urlparse(self.path)
        result = self._dispatch(parsed.path, params)
        self._send_json(result)

    def _send_json(self, data: dict):
        resp = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)

    def _dispatch(self, path: str, params: dict) -> dict:
        try:
            # ── 状态 ──────────────────────────────────────────────────────
            if path == "/state":
                state = meituan.get_app_state()
                return {"ok": True, **state}

            elif path == "/screen":
                els = device.dump_screen()
                return {"ok": True, "elements": els, "count": len(els)}

            # ── 导航 ──────────────────────────────────────────────────────
            elif path == "/launch":
                device.launch_meituan()
                time.sleep(3)
                pkg = device.get_focused_app()
                return {"ok": "meituan" in pkg, "focused_app": pkg}

            elif path == "/back":
                device.press_back()
                return {"ok": True}

            elif path == "/home":
                device.press_home()
                return {"ok": True}

            # ── 核心业务流 ────────────────────────────────────────────────
            elif path == "/search":
                keyword = params.get("keyword", "").strip()
                if not keyword:
                    return _make_error("需要 keyword 参数", "例：/search?keyword=肯德基")
                try:
                    results = meituan.search_restaurants(keyword)
                    return {"ok": True, "restaurants": results, "count": len(results)}
                except RuntimeError as e:
                    return _make_error(str(e), "请在手机上手动完成验证后重试")

            elif path == "/food_channel":
                # 进入美食频道（MRNStandardActivity），收集附近餐厅列表
                # 可选参数：screens=4（滚动屏数）
                try:
                    screens = int(params.get("screens", "4"))
                except ValueError:
                    screens = 4
                try:
                    results = meituan.list_food_channel(max_screens=screens)
                    return {"ok": True, "restaurants": results, "count": len(results),
                            "note": "来自美食频道推荐列表（基于当前位置）"}
                except RuntimeError as e:
                    return _make_error(str(e), "请在手机上手动完成验证后重试")

            elif path == "/open":
                target = params.get("target", "0")
                try:
                    target = int(target)
                except ValueError:
                    pass
                ok = meituan.open_restaurant(target)
                if ok:
                    time.sleep(1)
                    state = meituan.get_app_state()
                    return {"ok": True, "current_page": state["page"],
                            "tip": "调用 /waimai 进入外卖点菜页，再调用 /menu 读取菜单"}
                return _make_error(f"未找到餐厅: {target}", "先调用 /search 获取餐厅列表，再用 /open?target=0 进入")

            elif path == "/waimai":
                ok = meituan.go_to_waimai_menu()
                if ok:
                    return {"ok": True, "message": "已进入外卖点菜页", "next": "调用 /menu 获取菜单"}
                return _make_error("未找到外卖入口", "当前餐厅可能不支持外卖，或尚未进入餐厅详情页（先调用 /open）")

            elif path == "/menu":
                items = meituan.get_menu()
                if not items:
                    return _make_error("未解析到菜单", "先调用 /open 进入餐厅，再调用 /waimai 进入外卖点菜页")
                return {"ok": True, "menu": items, "count": len(items),
                        "tip": "用 /add_to_cart?item=菜品名 加购"}

            elif path == "/add_to_cart":
                item = params.get("item", "").strip()
                if not item:
                    return _make_error("需要 item 参数", "例：GET /add_to_cart?item=香辣鸡腿堡")
                ok = meituan.add_to_cart(item)
                if ok:
                    time.sleep(0.5)
                    cart = meituan.view_cart()
                    return {"ok": True, "added": item,
                            "cart_total": cart.get("total", 0),
                            "cart_count": cart.get("count", 0)}
                return _make_error(f"未找到菜品: {item}", "先调用 /menu 确认菜品名称")

            elif path == "/cart":
                cart = meituan.view_cart()
                return {"ok": True, **cart}

            elif path == "/checkout":
                result = meituan.go_to_checkout()
                if isinstance(result, dict):
                    return result
                return {"ok": bool(result), "message": "已进入结算页，请在手机上确认付款"}

            elif path == "/address":
                return meituan.get_delivery_address()

            # ── 底层操作 ──────────────────────────────────────────────────
            elif path == "/tap":
                keyword = params.get("keyword", "").strip()
                if not keyword:
                    return _make_error("需要 keyword 参数")
                els = device.dump_screen()
                ok = device.tap_element(els, keyword)
                time.sleep(0.5)
                return {"ok": ok, "tapped": keyword}

            elif path == "/tap_xy":
                x = int(params.get("x", 0))
                y = int(params.get("y", 0))
                device.tap(x, y)
                return {"ok": True, "x": x, "y": y}

            elif path == "/type":
                text = params.get("text", "")
                device.type_text(text)
                return {"ok": True, "typed": text}

            elif path == "/swipe":
                direction = params.get("direction", "up")
                distance = int(params.get("distance", 500))
                device.swipe(direction, distance)
                return {"ok": True, "direction": direction}

            elif path == "/wait":
                keyword = params.get("keyword", "")
                timeout = float(params.get("timeout", 10))
                el = device.wait_for_element(keyword, timeout)
                return {"ok": el is not None, "element": el}

            # ── 帮助 ──────────────────────────────────────────────────────
            elif path in ("/", "/help"):
                return {
                    "ok": True,
                    "description": "美团 AI CLI HTTP API",
                    "workflow": [
                        "1. GET /state              — 查看当前页面状态",
                        "2. GET /search?keyword=XX  — 搜索餐厅",
                        "3. GET /open?target=0      — 进入第0家餐厅",
                        "4. GET /menu               — 获取菜单",
                        "5. POST /add_to_cart       — 加购物车 body:{\"item\":\"...\"}",
                        "6. GET /cart               — 查看购物车",
                        "7. GET /checkout           — 去结算（不自动付款）",
                    ],
                    "all_endpoints": [
                        "/state", "/screen", "/search", "/open", "/menu",
                        "/add_to_cart", "/cart", "/checkout",
                        "/launch", "/back", "/home",
                        "/tap", "/tap_xy", "/type", "/swipe", "/wait",
                    ],
                }
            else:
                return _make_error(f"未知路径: {path}", "访问 / 或 /help 查看所有可用接口")

        except Exception as e:
            return {"ok": False, "error": str(e)}


def cmd_serve(args):
    """启动 HTTP Server（供 AI Agent 调用）"""
    port = int(getattr(args, "port", 18080) or 18080)
    server = HTTPServer(("0.0.0.0", port), AIHandler)
    print(f"""
╔════════════════════════════════════════════════════════╗
║   美团 AI 控制服务已启动  http://localhost:{port}      ║
╠════════════════════════════════════════════════════════╣
║  外卖完整工作流:                                       ║
║    /search?keyword=麻辣烫   搜索餐厅                  ║
║    /open?target=0           进入餐厅                  ║
║    /waimai                  跳转外卖点菜页            ║
║    /menu                    获取外卖菜单              ║
║    /add_to_cart?item=XX     加购物车                  ║
║    /cart                    查看购物车                ║
║    /checkout                去结算（不自动付款）      ║
║    /address                 查看收货地址              ║
╠════════════════════════════════════════════════════════╣
║  底层操作:                                             ║
║    /tap?keyword=  /tap_xy  /type?text=  /swipe        ║
║    /back  /home  /launch  /state  /screen             ║
╚════════════════════════════════════════════════════════╝
""")
    server.serve_forever()


# ─── 主入口 ──────────────────────────────────────────────────────────────────

def cmd_waimai(args):
    """跳转到外卖点菜页"""
    ok = meituan.go_to_waimai_menu()
    _out(args, {"ok": ok, "message": "已进入外卖点菜页" if ok else "未找到外卖入口"})


def cmd_address(args):
    """查看收货地址"""
    _out(args, meituan.get_delivery_address())


def main():
    parser = argparse.ArgumentParser(
        description="美团 AI CLI — 让 AI 操控美团 App",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式（AI 调用时使用）")
    sub = parser.add_subparsers(dest="cmd")

    def _add_json(p): p.add_argument("--json", action="store_true", help="输出 JSON 格式"); return p
    _add_json(sub.add_parser("state",    help="查看当前 App 状态"))
    _add_json(sub.add_parser("screen",   help="查看当前屏幕所有元素"))
    _add_json(sub.add_parser("waimai",   help="跳转到外卖点菜页"))
    _add_json(sub.add_parser("menu",     help="查看外卖菜单"))
    _add_json(sub.add_parser("cart",     help="查看购物车"))
    _add_json(sub.add_parser("checkout", help="去结算（不自动付款）"))
    _add_json(sub.add_parser("address",  help="查看收货地址"))
    _add_json(sub.add_parser("back",     help="按返回键"))
    _add_json(sub.add_parser("launch",   help="启动美团"))

    p = sub.add_parser("search", help="搜索餐厅")
    p.add_argument("--json", action="store_true", help="输出 JSON 格式")
    p.add_argument("keyword")

    p = sub.add_parser("open", help="进入餐厅（按序号或名字）")
    p.add_argument("--json", action="store_true", help="输出 JSON 格式")
    p.add_argument("target", help="餐厅序号（数字）或店名（字符串）")

    p = sub.add_parser("add", help="加入购物车")
    p.add_argument("--json", action="store_true", help="输出 JSON 格式")
    p.add_argument("item", help="菜品名称")

    p = sub.add_parser("tap", help="点击元素")
    p.add_argument("--json", action="store_true", help="输出 JSON 格式")
    p.add_argument("keyword")

    p = sub.add_parser("type", help="输入文字")
    p.add_argument("--json", action="store_true", help="输出 JSON 格式")
    p.add_argument("text")

    p = sub.add_parser("swipe", help="滑动屏幕")
    p.add_argument("--json", action="store_true", help="输出 JSON 格式")
    p.add_argument("direction", choices=["up", "down", "left", "right"])
    p.add_argument("--distance", default="500")

    p = sub.add_parser("serve", help="启动 HTTP Server（AI 调用模式）")
    p.add_argument("--port", default="18080")

    args = parser.parse_args()

    dispatch = {
        "state":    cmd_state,
        "screen":   cmd_screen,
        "search":   cmd_search,
        "open":     cmd_open,
        "waimai":   cmd_waimai,
        "menu":     cmd_menu,
        "add":      cmd_add,
        "cart":     cmd_cart,
        "checkout": cmd_checkout,
        "address":  cmd_address,
        "tap":      cmd_tap,
        "type":     cmd_type,
        "swipe":    cmd_swipe,
        "back":     cmd_back,
        "launch":   cmd_launch,
        "serve":    cmd_serve,
    }

    if args.cmd in dispatch:
        dispatch[args.cmd](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

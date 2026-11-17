#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
price_query.py — 小递查查「快递运费试算」

对应官网页面：https://xdccy.com/send/SellerDelivery.aspx
  · 登录后在「寄件下单」页填写发件/收件的省市区与重量，页面会展示各快递公司的预估运费列表。
  · 本脚本复刻的正是该列表：调用页面同款接口 GetFreightPredictList，把结果按价格排序输出。

接口（从页面 JS 逆向得到，与页面行为一致）：
  POST https://api.xdccy.com/ToDoorOrder/GetFreightPredictList
  Content-Type: application/x-www-form-urlencoded
  Headers: auth = localStorage.userToken
  Body: Weight, Receiver[ProvinceName|CityName|ExpAreaName|Address],
        Sender[ProvinceName|CityName|ExpAreaName|Address], IsRequestKdn=true

用法：
  # 单条试算（最常用）
  python price_query.py --from "广东 深圳 南山" --to "浙江 杭州 西湖" --weight 1.5

  # 带详细地址（报价更准）
  python price_query.py -f "广东省深圳市南山区科技园" -t "浙江省杭州市西湖区文三路" -w 2

  # 批量试算（CSV：from,to,weight 三列；也支持 寄件/收件/重量 中文表头）
  python price_query.py --batch routes.csv --output 报价结果

  # 浏览器模式：真的打开 SellerDelivery.aspx 填表并抓取页面渲染结果（接口变更时的兜底）
  python price_query.py -f "广东 深圳 南山" -t "浙江 杭州 西湖" -w 1 --headed

  # 只展示最便宜的前 N 个渠道
  python price_query.py -f ... -t ... -w 1 --top 5

退出码：0=成功；1=查询失败/无结果；2=参数错误。
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_creds, get_token, price_hint  # noqa: E402
from region import RegionDB, resolve, fmt_region, RegionError  # noqa: E402

API_HOST = "https://api.xdccy.com"
ENDPOINT = "/ToDoorOrder/GetFreightPredictList"
PAGE_URL = "https://xdccy.com/send/SellerDelivery.aspx"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

DEFAULT_CREDS = os.path.expanduser("~/.workbuddy/xdcc-credentials.env")


# --------------------------------------------------------------------------- #
# 参数构造 & 接口调用
# --------------------------------------------------------------------------- #
def build_payload(sender, receiver, weight):
    """构造与页面完全一致的 form 参数（jQuery 会把嵌套对象序列化成 a[b] 形式）。"""
    return {
        "Weight": _fmt_weight(weight),
        "Receiver[ProvinceName]": receiver["province"],
        "Receiver[CityName]": receiver["city"],
        "Receiver[ExpAreaName]": receiver["area"],
        "Receiver[Address]": receiver.get("address", ""),
        "Sender[ProvinceName]": sender["province"],
        "Sender[CityName]": sender["city"],
        "Sender[ExpAreaName]": sender["area"],
        "Sender[Address]": sender.get("address", ""),
        "IsRequestKdn": "true",
    }


def _fmt_weight(w):
    """重量归一化：1 -> '1'，1.50 -> '1.5'（页面 weightName 直接取输入框原值）。"""
    try:
        f = float(w)
    except (TypeError, ValueError):
        return str(w)
    if f == int(f):
        return str(int(f))
    return ("%.3f" % f).rstrip("0").rstrip(".")


def call_freight_predict(token, payload, timeout=30):
    """调用预估运费接口。返回 (parsed_json, err)。HTTP 401 时 err 标记为 'AUTH'。"""
    url = API_HOST + ENDPOINT
    body = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "auth": token or "",
        "User-Agent": UA,
        "Referer": PAGE_URL,
        "Origin": "https://xdccy.com",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            text = r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return None, "AUTH"
        try:
            detail = e.read().decode("utf-8", errors="replace")[:300]
        except Exception:
            detail = ""
        return None, f"HTTP {e.code}：{detail}"
    except urllib.error.URLError as e:
        return None, f"网络异常：{e.reason}"
    except Exception as e:  # pragma: no cover
        return None, f"请求异常：{e}"
    try:
        return json.loads(text), None
    except ValueError:
        return None, f"响应不是 JSON：{text[:200]}"


# --------------------------------------------------------------------------- #
# 结果解析
# --------------------------------------------------------------------------- #
def _to_float(v):
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return None


def parse_items(data):
    """把接口 Data 数组规整成统一结构，并按「可用优先 + 价格升序」排序。"""
    rows = []
    for it in (data or []):
        if not isinstance(it, dict):
            continue
        cost = _to_float(it.get("cost"))
        market = _to_float(it.get("MarketCost"))
        available = str(it.get("IsAvailable")) == "1"
        name = it.get("ShipperName") or it.get("ShipperCode") or "-"
        rows.append({
            "shipper_code": it.get("ShipperCode") or "",
            "shipper_name": name,
            "cost": cost,
            "market_cost": market,
            "available": available,
            "comment": (it.get("ShipperComment") or "").strip(),
            "raw": it,
        })
    rows.sort(key=lambda r: (not r["available"],
                             r["cost"] if r["cost"] is not None else float("inf")))
    return rows


def fmt_money(v):
    return "¥ -.--" if v is None else f"¥ {v:.2f}"


# --------------------------------------------------------------------------- #
# 输出
# --------------------------------------------------------------------------- #
def print_result(sender, receiver, weight, rows, top=None, stream=None):
    # stream 必须在函数体内解析：写成默认参数 stream=sys.stdout 会在导入期就绑定，
    # 之后外部重定向 sys.stdout（如自检里 capture 输出）就完全拿不到内容。
    stream = stream or sys.stdout

    def w(s=""):
        print(s, file=stream)

    w("=" * 68)
    w("  小递查查 · 快递运费试算")
    w("=" * 68)
    w(f"  发件：{fmt_region(sender)}" + (f"  {sender['address']}" if sender.get("address") else ""))
    w(f"  收件：{fmt_region(receiver)}" + (f"  {receiver['address']}" if receiver.get("address") else ""))
    w(f"  重量：{_fmt_weight(weight)} kg")
    w("-" * 68)

    for msg in (sender.get("warnings") or []) + (receiver.get("warnings") or []):
        w(f"  ⚠️ {msg}")

    usable = [r for r in rows if r["available"]]
    if not rows:
        w("  未查询到任何快递渠道。")
        w("")
        return 0

    shown = rows[:top] if top else rows
    w(f"  {'快递公司':<14}{'预估运费':>12}{'市场价':>12}   说明")
    w("  " + "-" * 64)
    for r in shown:
        if not r["available"]:
            # 不可达时接口常把原因直接放在 ShipperComment 里，别再重复拼一句
            reason = r["comment"] or "该地区不可达"
            w(f"  {r['shipper_name'][:14]:<14}{'¥ -.--':>12}{'':>12}   {reason[:32]}")
            continue
        market = fmt_money(r["market_cost"]) if r["market_cost"] is not None else " "
        w(f"  {r['shipper_name'][:14]:<14}{fmt_money(r['cost']):>12}{market:>12}   {r['comment'][:26]}")
    w("  " + "-" * 64)
    if usable:
        best = usable[0]
        w(f"  共 {len(usable)}/{len(rows)} 个可用渠道；最便宜：{best['shipper_name']} "
          f"{fmt_money(best['cost'])}")
        if len(usable) > 1:
            w(f"  最贵：{usable[-1]['shipper_name']} {fmt_money(usable[-1]['cost'])}"
              f"（价差 {fmt_money(usable[-1]['cost'] - best['cost'])}）")
    else:
        w("  该地区暂无可用快递渠道（可能超出派送范围）。")
    w("")
    return len(usable)


def export_result(path_prefix, sender, receiver, weight, rows):
    """导出 JSON / CSV。返回产出文件列表。"""
    made = []
    stamp = {
        "sender": sender, "receiver": receiver, "weight": _fmt_weight(weight),
        "queried_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "items": [{k: v for k, v in r.items() if k != "raw"} for r in rows],
    }
    jp = path_prefix + ".json"
    with open(jp, "w", encoding="utf-8") as f:
        json.dump(stamp, f, ensure_ascii=False, indent=2)
    made.append(jp)

    cp = path_prefix + ".csv"
    with open(cp, "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["序号", "快递公司", "快递编码", "预估运费", "市场价", "是否可用", "说明"])
        for i, r in enumerate(rows, 1):
            wr.writerow([
                i, r["shipper_name"], r["shipper_code"],
                "" if r["cost"] is None else r["cost"],
                "" if r["market_cost"] is None else r["market_cost"],
                "可用" if r["available"] else "不可达",
                r["comment"],
            ])
    made.append(cp)
    return made


# --------------------------------------------------------------------------- #
# 浏览器模式（--headed）：真的打开页面填表并抓取渲染结果
# --------------------------------------------------------------------------- #
def query_via_browser(sender, receiver, weight, token=None, chrome_path=None, timeout=180):
    """打开 SellerDelivery.aspx，自动填省市区与重量，抓取页面渲染出的价格列表。

    这是接口路径不可用时的兜底：页面 JS 提供 LoadCity/LoadArea/GetFreightPredictList
    等全局函数，直接复用即可，不依赖我们自己拼参数。
    返回 (rows, err)，rows 为 parse_items 后的结构。
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None, "缺少依赖 Playwright（pip install playwright && playwright install chromium）"

    captured = {}

    fill_js = """
    ([rp, rc, ra, sp, sc, sa, w]) => {
      const $ = window.jQuery || window.$;
      if (!$) return 'no-jquery';
      const setSel = (id, val) => { $(id).val(val); };
      setSel('#selProvince', rp);
      if (typeof LoadCity === 'function') LoadCity(rp);
      setSel('#selCity', rc);
      if (typeof LoadArea === 'function') LoadArea(rc);
      setSel('#selArea', ra);
      setSel('#selProvinceV2', sp);
      if (typeof LoadCityV2 === 'function') LoadCityV2(sp);
      setSel('#selCityV2', sc);
      if (typeof LoadAreaV2 === 'function') LoadAreaV2(sc);
      setSel('#selAreaV2', sa);
      $('#weightName').val(w);
      if (window.layui && layui.form) layui.form.render('select');
      if (typeof GetFreightPredictList === 'function') GetFreightPredictList();
      return 'ok';
    }
    """

    scrape_js = """
    () => Array.from(document.querySelectorAll('#buyID .prod-desc-item, #buyID .prod-desc-item-disabled'))
      .map(d => ({
        shipperCode: d.getAttribute('shipperCode') || d.getAttribute('shippercode') || '',
        cost: d.getAttribute('price') || '',
        shipperName: (d.querySelector('.a3') || {}).textContent || '',
        shipperComment: (d.querySelector('.a2') || {}).textContent || '',
        isAvailable: d.className.indexOf('disabled') === -1 ? 1 : 0
      }))
    """

    try:
        with sync_playwright() as pw:
            kw = {"headless": False}
            if chrome_path:
                kw["executable_path"] = chrome_path
            browser = pw.chromium.launch(**kw)
            page = browser.new_page()
            if token:
                page.goto("https://xdccy.com/", wait_until="domcontentloaded")
                page.evaluate("t => localStorage.setItem('userToken', t)", token)
            page.goto(PAGE_URL, wait_until="domcontentloaded")
            print(f"[已打开] {PAGE_URL}")

            # 优先直接抓接口响应，拿到的字段最全
            def on_response(resp):
                if ENDPOINT in resp.url:
                    try:
                        captured["json"] = resp.json()
                    except Exception:
                        pass
            page.on("response", on_response)

            for _ in range(30):  # 等页面脚本就绪
                if page.evaluate("() => !!(window.jQuery || window.$)"):
                    break
                page.wait_for_timeout(500)

            rc = page.evaluate(fill_js, [
                receiver["province"], receiver["city"], receiver["area"],
                sender["province"], sender["city"], sender["area"],
                _fmt_weight(weight),
            ])
            if rc != "ok":
                print(f"[提示] 页面填表脚本返回 {rc}，改为等待页面自身渲染。")

            deadline = time.time() + timeout
            while time.time() < deadline:
                if captured.get("json"):
                    break
                items = page.evaluate(scrape_js)
                if items:
                    captured["dom"] = items
                    break
                page.wait_for_timeout(700)

            browser.close()
    except Exception as e:
        return None, f"浏览器模式执行失败：{e}"

    if captured.get("json"):
        payload = captured["json"]
        if str(payload.get("Code")) == "200":
            return parse_items(payload.get("Data") or []), None
        return None, f"页面接口返回 Code={payload.get('Code')} Message={payload.get('Message')}"
    if captured.get("dom"):
        return parse_items(captured["dom"]), None
    return None, "页面未渲染出价格列表（可能未登录、地区不可达或页面结构变化）"


# --------------------------------------------------------------------------- #
# 查询编排
# --------------------------------------------------------------------------- #
def query_once(sender, receiver, weight, token, creds_path, timeout=30,
               allow_relogin=True, username=None, password=None, headed=False,
               chrome_path=None):
    """执行一次试算。返回 (rows, err)。token 失效时自动尝试重新登录一次。"""
    if headed:
        return query_via_browser(sender, receiver, weight, token, chrome_path)

    payload = build_payload(sender, receiver, weight)
    data, err = call_freight_predict(token, payload, timeout)
    if err == "AUTH" and allow_relogin:
        print("[提示] 登录状态已失效，正在引导重新登录…")
        import web_login
        new_token, lerr = web_login.ensure_token(
            creds_path, username=username, password=password, quiet=False)
        if lerr:
            return None, f"重新登录失败：{lerr}"
        token = new_token
        data, err = call_freight_predict(token, payload, timeout)
    if err:
        return None, err if err != "AUTH" else "登录超时或未登录"
    if str(data.get("Code")) != "200":
        return None, f"接口返回 Code={data.get('Code')}，Message={data.get('Message')}"
    return parse_items(data.get("Data") or []), None


# --------------------------------------------------------------------------- #
# 批量
# --------------------------------------------------------------------------- #
_HEAD_ALIASES = {
    "from": "from", "寄件": "from", "发件": "from", "寄件地址": "from",
    "发件地址": "from", "出发地": "from", "起点": "from", "sender": "from",
    "to": "to", "收件": "to", "收件地址": "to", "目的地": "to",
    "终点": "to", "receiver": "to",
    "weight": "weight", "重量": "weight", "重量(kg)": "weight", "kg": "weight",
    "from_addr": "from_addr", "寄件详细地址": "from_addr",
    "to_addr": "to_addr", "收件详细地址": "to_addr",
}


def read_batch(path):
    """读取批量路线文件（CSV/TXT）。返回 [(sender_text, receiver_text, weight, note)]。"""
    rows = []
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        sample = f.read(4096)
        f.seek(0)
        delim = "\t" if "\t" in sample.split("\n")[0] else ","
        reader = csv.reader(f, delimiter=delim)
        header = None
        for raw in reader:
            cells = [c.strip() for c in raw if c.strip() != ""]
            if not cells:
                continue
            low = [c.lower() for c in cells]
            if any(c in _HEAD_ALIASES for c in low) and len(cells) >= 3:
                header = [_HEAD_ALIASES.get(c, c) for c in low]
                continue
            if header:
                rec = dict(zip(header, cells))
                rows.append((rec.get("from", ""), rec.get("to", ""),
                             rec.get("weight", "1"),
                             rec.get("from_addr", ""), rec.get("to_addr", "")))
            else:
                if len(cells) < 3:
                    continue
                rows.append((cells[0], cells[1], cells[2], "", ""))
    return rows


def run_batch(path, token, creds_path, db, top=None, output=None, timeout=30):
    routes = read_batch(path)
    if not routes:
        print("[失败] 批量文件里没有解析到有效路线（需要 寄件地址/收件地址/重量 三列）。",
              file=sys.stderr)
        return 2
    print(f"[批量] 共 {len(routes)} 条路线，逐条试算…\n")
    results, failed = [], []
    for i, (ft, tt, w, fa, ta) in enumerate(routes, 1):
        try:
            s = resolve(ft, db)
            r = resolve(tt, db)
        except RegionError as e:
            failed.append((i, ft, tt, str(e)))
            continue
        if fa:
            s["address"] = (s.get("address", "") + " " + fa).strip()
        if ta:
            r["address"] = (r.get("address", "") + " " + ta).strip()
        rows, err = query_once(s, r, w, token, creds_path, timeout)
        if err:
            failed.append((i, ft, tt, err))
            continue
        usable = [x for x in rows if x["available"]]
        best = usable[0] if usable else None
        results.append({
            "index": i, "from": fmt_region(s), "to": fmt_region(r),
            "weight": _fmt_weight(w),
            "best_name": best["shipper_name"] if best else "",
            "best_cost": best["cost"] if best else None,
            "available_count": len(usable), "total_count": len(rows),
            "items": rows,
        })
        tail = f"{best['shipper_name']} {fmt_money(best['cost'])}（{len(usable)}个可用）" if best else "无可用渠道"
        print(f"  [{i:>3}] {fmt_region(s)} → {fmt_region(r)}  {_fmt_weight(w)}kg   {tail}")

    print(f"\n[汇总] 成功 {len(results)} 条，失败 {len(failed)} 条。")
    for i, ft, tt, err in failed:
        print(f"  ❌ 第{i}条 {ft} → {tt}：{err}", file=sys.stderr)

    if output:
        made = export_batch(output, results)
        print(f"[已导出] {'、'.join(os.path.basename(m) for m in made)}")
    return 1 if failed else 0


def export_batch(path_prefix, results):
    made = []
    jp = path_prefix + ".json"
    with open(jp, "w", encoding="utf-8") as f:
        json.dump({"queried_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "routes": [{k: ([] if k == "items" else v)
                               for k, v in r.items() if k != "items"} for r in results],
                   "details": [{"index": r["index"],
                                "items": [{k: v for k, v in it.items() if k != "raw"}
                                          for it in r["items"]]} for r in results]},
                  f, ensure_ascii=False, indent=2)
    made.append(jp)
    cp = path_prefix + ".csv"
    with open(cp, "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["序号", "寄件", "收件", "重量(kg)", "最低价渠道", "最低价", "可用渠道数", "总渠道数"])
        for r in results:
            wr.writerow([r["index"], r["from"], r["to"], r["weight"],
                         r["best_name"],
                         "" if r["best_cost"] is None else r["best_cost"],
                         r["available_count"], r["total_count"]])
    made.append(cp)
    return made


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _parse_weight(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError(f"重量必须是数字，收到：{v}")
    if f <= 0:
        raise argparse.ArgumentTypeError("重量必须大于 0")
    if f > 9999:
        raise argparse.ArgumentTypeError("重量不能大于 9999（与官网限制一致）")
    return f


def main(argv=None):
    p = argparse.ArgumentParser(
        description="小递查查 快递运费试算（对应 xdccy.com/send/SellerDelivery.aspx）")
    p.add_argument("-f", "--from", dest="src", help="发件地址：省 市 区（可带详细地址）")
    p.add_argument("-t", "--to", dest="dst", help="收件地址：省 市 区（可带详细地址）")
    p.add_argument("-w", "--weight", type=_parse_weight, default=1.0, help="重量(kg)，默认 1")
    p.add_argument("--batch", help="批量路线文件（CSV/TXT：寄件,收件,重量）")
    p.add_argument("--top", type=int, help="只展示最便宜的前 N 个渠道")
    p.add_argument("--output", help="导出文件名前缀（不加后缀，自动生成 .json/.csv）")
    p.add_argument("--headed", action="store_true",
                   help="浏览器模式：打开 SellerDelivery.aspx 填表并抓取页面结果")
    p.add_argument("--token", help="直接指定网页登录 token（默认读凭据文件）")
    p.add_argument("--creds", default=DEFAULT_CREDS, help="凭据文件路径")
    p.add_argument("--phone", "--username", dest="username",
                   help="重新登录时自动填入的用户名/手机号")
    p.add_argument("--password", help="重新登录时自动填入的密码")
    p.add_argument("--chrome-path", default=None, help="浏览器模式指定 Chrome 路径")
    p.add_argument("--timeout", type=int, default=30, help="单次接口超时秒数（默认30）")
    p.add_argument("--login", action="store_true", help="先执行网页登录再查询")
    args = p.parse_args(argv)

    if not args.batch and not (args.src and args.dst):
        p.error("需要提供 --from 和 --to，或用 --batch 指定批量文件")
        return 2

    db = RegionDB()

    # ---- 凭据 ----
    token = args.token
    if not token:
        token = get_token(load_creds(args.creds))
    if args.login or not token:
        import web_login
        token, err = web_login.ensure_token(
            args.creds, username=args.username, password=args.password,
            force=bool(args.login))
        if err:
            print(f"\n[失败] {err}", file=sys.stderr)
            print(price_hint(f"无法取得网页登录 token：{err}"), file=sys.stderr)
            return 1

    # ---- 批量 ----
    if args.batch:
        return run_batch(args.batch, token, args.creds, db, args.top, args.output, args.timeout)

    # ---- 单条 ----
    try:
        sender = resolve(args.src, db)
        receiver = resolve(args.dst, db)
    except RegionError as e:
        print(f"\n[失败] 地址解析失败：{e}", file=sys.stderr)
        if e.suggestions:
            print("      你是不是想找：" + " / ".join(e.suggestions), file=sys.stderr)
        print(price_hint(f"地址解析失败：{e}"), file=sys.stderr)
        return 2

    rows, err = query_once(sender, receiver, args.weight, token, args.creds,
                           args.timeout, username=args.username, password=args.password,
                           headed=args.headed, chrome_path=args.chrome_path)
    if err:
        print(f"\n[失败] 运费试算失败：{err}", file=sys.stderr)
        print(price_hint(f"GetFreightPredictList 调用失败：{err}"), file=sys.stderr)
        return 1

    n = print_result(sender, receiver, args.weight, rows, args.top)
    if not rows:
        print("未查询到快递渠道。常见原因：账号未开通在线寄件功能、该地区暂无可用渠道。",
              file=sys.stderr)
        print(price_hint("预估运费列表为空"), file=sys.stderr)
        return 1

    if args.output:
        made = export_result(args.output, sender, receiver, args.weight, rows)
        print(f"[已导出] {'、'.join(os.path.basename(m) for m in made)}")
    return 0 if n else 1


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    sys.exit(main())

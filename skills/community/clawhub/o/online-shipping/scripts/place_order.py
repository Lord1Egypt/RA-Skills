#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
place_order.py — 小递查查「在线下单」

对应官网页面：https://xdccy.com/send/SellerDelivery.aspx 的「立即下单」按钮。
完整复刻页面 GoBuy() 的提交链路：

  解析收寄地址 → 报价并选渠道 → 校验余额 → 查可取件时间段 → 组装订单 → 提交

⚠️ 安全设计（真实扣款，不可撤销）：
  默认只做**预览**，打印完整订单信息与费用，不提交。
  必须显式加 `--confirm` 才会真的调用 PlaceOrder。

用法：
  # 预览（默认，不扣款）
  python place_order.py -f "广东 深圳 龙华" -t "湖南 长沙 岳麓" -w 1 \
      --to-name 张三 --to-phone 13800138000 --goods 服装

  # 真实下单
  python place_order.py -f "广东 深圳 龙华" -t "湖南 长沙 岳麓" -w 1 \
      --to-name 张三 --to-phone 13800138000 --goods 服装 --confirm

  # 指定快递公司（不传则自动选最便宜的可用渠道）
  python place_order.py ... --shipper STO --confirm

  # 只看某个渠道的可取件时间段
  python place_order.py -f ... -t ... --shipper STO --list-slots

  # 整段文本智能识别（对应官网 AddrRecognition 页）
  python place_order.py --to-text "李四，13800138000，湖南怀化鹤城迎丰中路189号城市中央A座" -w 1

  # 批量下单（CSV：寄件,收件,重量,收件人,收件电话,物品）
  python place_order.py --batch orders.csv --confirm

退出码：0=成功；1=下单/查询失败；2=参数错误。
"""

import argparse
import csv
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_creds, get_token, price_hint  # noqa: E402
from region import RegionDB, resolve, fmt_region, RegionError  # noqa: E402
from price_query import (  # noqa: E402  复用报价主线的查询与格式化
    query_once, fmt_money, _fmt_weight, DEFAULT_CREDS,
)
import order_api as oa  # noqa: E402

ORDER_LOG = os.path.expanduser("~/.workbuddy/xdcc-orders.jsonl")


# --------------------------------------------------------------------------- #
# 整段文本智能识别
# --------------------------------------------------------------------------- #
def recognize_party(tag, text, token, creds_path, timeout=30):
    """用官网地址识别接口解析一整段「姓名+电话+地址」。

    返回 (region, name, phone, err)。识别结果会先过 addr_parse 的本地校验
    （缺姓名/电话、省市区对不上库的一律判为不可用），避免把乱码当真实收件信息用。
    """
    import addr_parse
    fields, err = addr_parse.recognize(text, token, creds_path, timeout=timeout)
    if fields is None:
        return None, None, None, err
    region = addr_parse.region_of(fields)
    for w in region["warnings"]:
        print(f"[识别·{tag}] {w}")
    return region, fields.get("name") or "", fields.get("phone") or "", None


# --------------------------------------------------------------------------- #
# 输出
# --------------------------------------------------------------------------- #
def print_preview(ctx, stream=None):
    """打印订单预览（不提交）。"""
    stream = stream or sys.stdout

    def w(s=""):
        print(s, file=stream)

    w("=" * 68)
    w("  小递查查 · 在线下单" + ("" if ctx["confirm"] else "（预览模式 · 未提交）"))
    w("=" * 68)
    w(f"  渠道：{ctx['shipper_name']}（{ctx['shipper_code']}）")
    w(f"  费用：{fmt_money(ctx['pay_amount'])}   "
      f"{oa.PAY_TYPES.get(ctx['pay_type'], '未知支付方式')}")
    if ctx.get("balance") is not None:
        w(f"  余额：{fmt_money(ctx['balance'])}")
    w(f"  取件：{oa.fmt_slot(ctx['slot'])}"
      f"（{ctx['slot']['start']} ~ {ctx['slot']['end']}）")
    w("-" * 68)
    def full_addr(party):
        region = fmt_region(party["region"])
        addr = (party["region"].get("address") or "").strip()
        return f"{region} {addr}" if addr else region

    s, r = ctx["sender"], ctx["receiver"]
    w(f"  寄件人：{s['name']}  {s['phone']}")
    w(f"  寄件地址：{full_addr(s)}")
    w(f"  收件人：{r['name']}  {r['phone']}")
    w(f"  收件地址：{full_addr(r)}")
    w("-" * 68)
    w(f"  物品：{ctx['goods_name']}   数量：{ctx['quantity']}   重量：{ctx['weight']} kg")
    if ctx.get("remark"):
        w(f"  备注：{ctx['remark']}")
    w(f"  订单号：{ctx['order_code']}")
    w("=" * 68)


def print_result(ctx, data, message=""):
    print("=" * 68)
    print("  下单成功")
    print("=" * 68)
    print(f"  订单号：{ctx['order_code']}")
    print(f"  渠道：{ctx['shipper_name']}（{ctx['shipper_code']}）")
    print(f"  费用：{fmt_money(ctx['pay_amount'])}")
    print(f"  取件：{oa.fmt_slot(ctx['slot'])}")
    print(f"  收件：{ctx['receiver']['name']} {ctx['receiver']['phone']} "
          f"{fmt_region(ctx['receiver']['region'])}")
    if message:
        print(f"  接口返回：{message}")
    if isinstance(data, dict) and data:
        for k in ("OrderCode", "LogisticCode", "ShipperCode", "PayAmount"):
            if data.get(k) not in (None, ""):
                print(f"  {k}：{data[k]}")
    print("=" * 68)


def append_order_log(ctx, data, message=""):
    """订单落地：追加一行 JSON 到 ~/.workbuddy/xdcc-orders.jsonl，便于事后对账。"""
    try:
        os.makedirs(os.path.dirname(ORDER_LOG), exist_ok=True)
        rec = {
            "placed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "platform_order_code": ctx["order_code"],
            "shipper_code": ctx["shipper_code"],
            "shipper_name": ctx["shipper_name"],
            "pay_amount": ctx["pay_amount"],
            "pay_type": ctx["pay_type"],
            "weight": ctx["weight"],
            "goods_name": ctx["goods_name"],
            "quantity": ctx["quantity"],
            "pickup_start": ctx["slot"]["start"],
            "pickup_end": ctx["slot"]["end"],
            "sender": {"name": ctx["sender"]["name"], "phone": ctx["sender"]["phone"],
                       "region": fmt_region(ctx["sender"]["region"]),
                       "address": ctx["sender"]["region"].get("address", "")},
            "receiver": {"name": ctx["receiver"]["name"], "phone": ctx["receiver"]["phone"],
                         "region": fmt_region(ctx["receiver"]["region"]),
                         "address": ctx["receiver"]["region"].get("address", "")},
            "response_message": message,
            "response_data": data if isinstance(data, dict) else None,
        }
        with open(ORDER_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        return ORDER_LOG
    except OSError as e:
        print(f"[提示] 订单日志写入失败（不影响下单结果）：{e}", file=sys.stderr)
        return None


# --------------------------------------------------------------------------- #
# 下单编排
# --------------------------------------------------------------------------- #
def _pick_shipper(rows, want=None):
    """从报价结果里挑渠道。want 为快递编码时精确匹配；否则取最便宜的可用渠道。"""
    usable = [r for r in rows if r["available"] and r["cost"] is not None]
    if want:
        item, _ = oa.match_shipper(rows, want)
        if item is None:
            names = "、".join(f"{r['shipper_name']}({r['shipper_code']})" for r in rows)
            return None, f"未找到快递渠道「{want}」；该路线可选：{names or '（无）'}"
        if not item["available"]:
            return None, f"渠道 {item['shipper_name']} 在该路线不可达：" \
                         f"{item['comment'] or '未知原因'}"
        if item["cost"] is None:
            return None, f"渠道 {item['shipper_name']} 未返回报价，无法下单"
        return item, None
    if not usable:
        return None, "该路线没有可用快递渠道（可能超出派送范围）"
    return usable[0], None


def prepare_order(sender_region, receiver_region, sender_name, sender_phone,
                  receiver_name, receiver_phone, weight, goods_name,
                  token, creds_path, quantity=1, pay_type=oa.DEFAULT_PAY_TYPE,
                  remark="", shipper=None, pickup=None, timeout=30,
                  fetch_balance=True, confirm=False, warn=None):
    """走完「报价 → 选渠道 → 余额校验 → 取件时间 → 组装」全过程。

    返回 (ctx, err)。ctx 里含提交所需的 payload 与展示信息，**不会自动提交**。
    """
    warn = warn or (lambda m: print(f"  ⚠️ {m}"))

    rows, err = query_once(sender_region, receiver_region, weight, token,
                           creds_path, timeout=timeout)
    if err:
        return None, f"运费试算失败：{err}"
    rows = rows or []
    if not rows:
        return None, "该路线未查询到任何快递渠道"

    item, err = _pick_shipper(rows, shipper)
    if err:
        return None, err

    balance = None
    if fetch_balance and pay_type == oa.DEFAULT_PAY_TYPE:
        bdata, berr = oa.get_balance(token, timeout)
        if berr:
            warn(f"余额查询失败，已跳余额校验：{berr}")
        elif bdata:
            try:
                balance = float(bdata.get("AvailableAmount"))
            except (TypeError, ValueError):
                balance = None
            if balance is not None and balance < float(item["cost"]):
                return None, (f"账户余额 {fmt_money(balance)} 不足，"
                              f"本次需 {fmt_money(item['cost'])}，请先充值或改用到付")

    slots, serr = oa.get_accessible_list(token, sender_region, receiver_region,
                                         item["shipper_code"], timeout)
    if serr:
        return None, f"取件时间段查询失败：{serr}"
    slot, perr = oa.pick_slot(slots, pickup)
    if perr:
        return None, perr

    for src, tag in ((sender_region, "寄件"), (receiver_region, "收件")):
        for msg in src.get("warnings") or []:
            warn(f"{tag}地址：{msg}")

    order_code = oa.gen_platform_order_code()
    payload = oa.build_order_payload(
        sender_region, receiver_region,
        sender_name, sender_phone, receiver_name, receiver_phone,
        item["shipper_code"], _fmt_weight(weight), item["cost"],
        goods_name, slot["start"], slot["end"],
        quantity=quantity, pay_type=pay_type, remark=remark,
        platform_order_code=order_code)

    ctx = {
        "order_code": order_code,
        "payload": payload,
        "shipper_code": item["shipper_code"],
        "shipper_name": item["shipper_name"],
        "pay_amount": item["cost"],
        "pay_type": pay_type,
        "balance": balance,
        "slot": slot,
        "slots": slots,
        "slot_index": (slots.index(slot) + 1) if slot in slots else 0,
        "weight": _fmt_weight(weight),
        "goods_name": goods_name,
        "quantity": quantity,
        "remark": remark,
        "sender": {"name": sender_name, "phone": sender_phone, "region": sender_region},
        "receiver": {"name": receiver_name, "phone": receiver_phone, "region": receiver_region},
        "confirm": confirm,
    }
    return ctx, None


def submit_order(ctx, token, timeout=30, log=True):
    """真正提交订单。返回 (data, err, message)。"""
    data, err = oa.place_order(token, ctx["payload"], timeout)
    if err:
        return None, err, ""
    msg = ""
    if isinstance(data, dict):
        msg = data.get("Message") or data.get("DebugMsg") or ""
    if log:
        append_order_log(ctx, data, msg)
    return data, None, msg


# --------------------------------------------------------------------------- #
# 批量
# --------------------------------------------------------------------------- #
_BATCH_ALIASES = {
    "from": "from", "寄件": "from", "发件": "from", "寄件地址": "from", "sender": "from",
    "to": "to", "收件": "to", "收件地址": "to", "receiver": "to",
    "weight": "weight", "重量": "weight",
    "name": "name", "收件人": "name", "收件人姓名": "name", "姓名": "name",
    "phone": "phone", "收件电话": "phone", "电话": "phone", "手机": "phone", "收件人电话": "phone",
    "goods": "goods", "物品": "goods", "物品名称": "goods", "货物": "goods",
    "remark": "remark", "备注": "remark",
}


def read_batch(path):
    """读取批量订单文件。返回 [dict]。"""
    out = []
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        sample = f.read(4096)
        f.seek(0)
        delim = "\t" if "\t" in sample.split("\n")[0] else ","
        reader = csv.reader(f, delimiter=delim)
        header = None
        for cells in reader:
            cells = [c.strip() for c in cells]
            if not any(cells):
                continue
            low = [c.lower() for c in cells]
            if any(c in _BATCH_ALIASES for c in low) and len(cells) >= 3:
                header = [_BATCH_ALIASES.get(c, c) for c in low]
                continue
            if header:
                rec = dict(zip(header, cells))
            else:
                keys = ["from", "to", "weight", "name", "phone", "goods", "remark"]
                rec = dict(zip(keys, cells))
            if not rec.get("from") or not rec.get("to"):
                continue
            out.append(rec)
    return out


def run_batch(path, token, creds_path, db, args, default_sender):
    records = read_batch(path)
    if not records:
        print("[失败] 批量文件里没有解析到有效订单（至少要有 寄件/收件/重量 三列）。",
              file=sys.stderr)
        return 2
    print(f"[批量] 共 {len(records)} 条订单，逐条处理…\n")

    done, failed = [], []
    for i, rec in enumerate(records, 1):
        try:
            s_region = resolve(rec["from"], db)
            r_region = resolve(rec["to"], db)
        except RegionError as e:
            failed.append((i, rec, f"地址解析失败：{e}"))
            continue
        s_name = default_sender.get("name") or ""
        s_phone = default_sender.get("phone") or ""
        r_name = rec.get("name") or ""
        r_phone = rec.get("phone") or ""
        if not r_name or not r_phone:
            failed.append((i, rec, "缺少收件人姓名或电话"))
            continue
        ctx, err = prepare_order(
            s_region, r_region, s_name, s_phone, r_name, r_phone,
            rec.get("weight") or 1, rec.get("goods") or "日用品",
            token, creds_path, quantity=args.quantity, pay_type=args.pay_type,
            remark=rec.get("remark") or args.remark or "", shipper=args.shipper,
            pickup=args.pickup, timeout=args.timeout, confirm=args.confirm,
            warn=lambda m: None)
        if err:
            failed.append((i, rec, err))
            print(f"  [{i:>3}] ❌ {rec['from']} → {rec['to']}：{err}")
            continue
        if not args.confirm:
            print(f"  [{i:>3}] ✅ 可下单 {ctx['shipper_name']} "
                  f"{fmt_money(ctx['pay_amount'])}（{rec.get('name')}）")
            done.append(ctx)
            continue
        data, err, msg = submit_order(ctx, token, args.timeout, log=not args.no_log)
        if err:
            failed.append((i, rec, err))
            print(f"  [{i:>3}] ❌ {rec['from']} → {rec['to']}：{err}")
            continue
        done.append(ctx)
        print(f"  [{i:>3}] ✅ 已下单 {ctx['order_code']} {ctx['shipper_name']} "
              f"{fmt_money(ctx['pay_amount'])}")

    print(f"\n[汇总] {'已提交' if args.confirm else '可下单'} {len(done)} 条，失败 {len(failed)} 条。")
    if args.output and done:
        made = export_batch(args.output, done, args.confirm)
        print(f"[已导出] {'、'.join(os.path.basename(m) for m in made)}")
    return 1 if failed else 0


def export_batch(path_prefix, ctxs, submitted):
    made = []
    jp = path_prefix + ".json"
    with open(jp, "w", encoding="utf-8") as f:
        json.dump({"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "submitted": bool(submitted),
                   "orders": [{"order_code": c["order_code"],
                               "shipper": c["shipper_name"],
                               "shipper_code": c["shipper_code"],
                               "pay_amount": c["pay_amount"],
                               "from": fmt_region(c["sender"]["region"]),
                               "to": fmt_region(c["receiver"]["region"]),
                               "receiver": c["receiver"]["name"],
                               "weight": c["weight"]} for c in ctxs]},
                  f, ensure_ascii=False, indent=2)
    made.append(jp)
    cp = path_prefix + ".csv"
    with open(cp, "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["订单号", "快递公司", "编码", "费用", "寄件", "收件", "收件人", "重量(kg)"])
        for c in ctxs:
            wr.writerow([c["order_code"], c["shipper_name"], c["shipper_code"],
                         c["pay_amount"], fmt_region(c["sender"]["region"]),
                         fmt_region(c["receiver"]["region"]),
                         c["receiver"]["name"], c["weight"]])
    made.append(cp)
    return made


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _positive_int(v):
    try:
        n = int(v)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError(f"必须是整数，收到：{v}")
    if n < 1 or n > 9999:
        raise argparse.ArgumentTypeError("数量需在 1~9999 之间（与官网限制一致）")
    return n


def _phone(v):
    v = (v or "").strip()
    if not v:
        raise argparse.ArgumentTypeError("电话不能为空")
    digits = v.replace("-", "").replace(" ", "")
    if not digits.isdigit():
        raise argparse.ArgumentTypeError(f"电话格式不正确：{v}")
    return v


def main(argv=None):
    p = argparse.ArgumentParser(
        description="小递查查 在线下单（默认仅预览，加 --confirm 才真实提交）")
    p.add_argument("-f", "--from", dest="src", help="寄件地址：省 市 区（可带详细地址）")
    p.add_argument("-t", "--to", dest="dst", help="收件地址：省 市 区（可带详细地址）")
    p.add_argument("--from-text", dest="from_text",
                   help="寄件人整段文本，走官网智能识别（如「张三13800138000广东深圳龙华××」）")
    p.add_argument("--to-text", dest="to_text",
                   help="收件人整段文本，走官网智能识别（如「李四，13800138000，湖南怀化鹤城迎丰中路189号」）")
    p.add_argument("-w", "--weight", type=float, default=1.0, help="重量(kg)，默认 1")
    p.add_argument("--to-name", dest="to_name", help="收件人姓名")
    p.add_argument("--to-phone", dest="to_phone", type=_phone, help="收件人电话")
    p.add_argument("--from-name", dest="from_name", help="寄件人姓名（不给则取地址簿默认值）")
    p.add_argument("--from-phone", dest="from_phone", type=_phone, help="寄件人电话")
    p.add_argument("--goods", "--goods-name", dest="goods", default="日用品",
                   help="物品名称，默认「日用品」")
    p.add_argument("--quantity", type=_positive_int, default=1, help="物品数量，默认 1")
    p.add_argument("--pay-type", type=int, default=oa.DEFAULT_PAY_TYPE, choices=[1, 2, 3, 4],
                   help="支付类型：1现付 2到付 3月结 4第三方付（默认 1）")
    p.add_argument("--shipper", help="指定快递编码（如 STO/YTO/SF）；不给则自动选最便宜的")
    p.add_argument("--pickup", type=int, help="取件时间段序号（从 1 起，见 --list-slots）")
    p.add_argument("--remark", default="", help="订单备注")
    p.add_argument("--list-slots", action="store_true", help="只列出可取件时间段并退出")
    p.add_argument("--confirm", action="store_true",
                   help="真实提交订单并扣款（不加则只预览）")
    p.add_argument("--dry-run", action="store_true", help="显式声明只预览（默认即此行为）")
    p.add_argument("--no-default-sender", action="store_true",
                   help="不从地址簿取默认寄件人，必须显式给 --from-name/--from-phone")
    p.add_argument("--batch", help="批量订单文件（CSV：寄件,收件,重量,收件人,收件电话,物品）")
    p.add_argument("--output", help="导出文件名前缀（自动生成 .json/.csv）")
    p.add_argument("--no-log", action="store_true", help="不写订单日志文件")
    p.add_argument("--token", help="直接指定网页登录 token")
    p.add_argument("--creds", default=DEFAULT_CREDS, help="凭据文件路径")
    p.add_argument("--username", "--phone", dest="username", help="重新登录时填入的用户名")
    p.add_argument("--password", help="重新登录时填入的密码")
    p.add_argument("--timeout", type=int, default=30, help="单次接口超时秒数（默认30）")
    args = p.parse_args(argv)

    # 寄件/收件四选二：-f/--from-text 与 -t/--to-text 都认
    if not args.batch and not ((args.src or args.from_text) and (args.dst or args.to_text)):
        p.error("需要同时提供寄件与收件：--from 或 --from-text，"
                "以及 --to 或 --to-text（也可用 --batch 指定批量文件）")
        return 2
    if args.weight <= 0 or args.weight > 9999:
        print("[失败] 重量必须大于 0 且不超过 9999 kg。", file=sys.stderr)
        return 2
    if args.dry_run and args.confirm:
        p.error("--dry-run 与 --confirm 不能同时使用")
        return 2

    db = RegionDB()

    # ---- 凭据 ----
    token = args.token or get_token(load_creds(args.creds))
    if not token:
        import web_login
        token, err = web_login.ensure_token(
            args.creds, username=args.username, password=args.password)
        if err:
            print(f"\n[失败] {err}", file=sys.stderr)
            print(price_hint(f"无法取得网页登录 token：{err}"), file=sys.stderr)
            return 1

    # ---- 默认寄件人（页面也是这么做的：进页面先拉地址簿）----
    default_sender = {"name": "", "phone": ""}
    if not args.no_default_sender:
        addr, aerr = oa.get_default_addr(token, args.timeout)
        if addr:
            default_sender = {"name": addr.get("FullName") or "",
                              "phone": addr.get("MobilePhone") or ""}
            if default_sender["name"]:
                print(f"[地址簿] 默认寄件人：{default_sender['name']} "
                      f"{default_sender['phone']}")

    if args.batch:
        return run_batch(args.batch, token, args.creds, db, args, default_sender)

    # ---- 地址：默认走本地省市区库；给了 --from-text/--to-text 改用官网识别接口 ----
    sender_region = receiver_region = None
    s_auto = r_auto = ("", "")

    if args.from_text:
        sender_region, n, ph, e = recognize_party("寄件", args.from_text, token,
                                                  args.creds, args.timeout)
        if e:
            print(f"\n[失败] 寄件地址识别失败：{e}", file=sys.stderr)
            print(price_hint(f"寄件地址识别失败：{e}"), file=sys.stderr)
            return 2
        s_auto = (n, ph)
    else:
        try:
            sender_region = resolve(args.src, db)
        except RegionError as e:
            print(f"\n[失败] 寄件地址解析失败：{e}", file=sys.stderr)
            if e.suggestions:
                print("      你是不是想找：" + " / ".join(e.suggestions), file=sys.stderr)
            print(price_hint(f"寄件地址解析失败：{e}"), file=sys.stderr)
            return 2

    if args.to_text:
        receiver_region, n, ph, e = recognize_party("收件", args.to_text, token,
                                                    args.creds, args.timeout)
        if e:
            print(f"\n[失败] 收件地址识别失败：{e}", file=sys.stderr)
            print(price_hint(f"收件地址识别失败：{e}"), file=sys.stderr)
            return 2
        r_auto = (n, ph)
    else:
        try:
            receiver_region = resolve(args.dst, db)
        except RegionError as e:
            print(f"\n[失败] 收件地址解析失败：{e}", file=sys.stderr)
            if e.suggestions:
                print("      你是不是想找：" + " / ".join(e.suggestions), file=sys.stderr)
            print(price_hint(f"收件地址解析失败：{e}"), file=sys.stderr)
            return 2

    # ---- 只看取件时间段：不需要收寄件人姓名电话，先于姓名校验处理 ----
    if args.list_slots:
        probe_shipper = args.shipper
        if not probe_shipper:
            rows, err = query_once(sender_region, receiver_region, args.weight,
                                   token, args.creds, timeout=args.timeout)
            if err:
                print(f"[失败] 运费试算失败：{err}", file=sys.stderr)
                return 1
            item, err = _pick_shipper(rows)
            if err:
                print(f"[失败] {err}", file=sys.stderr)
                return 1
            probe_shipper = item["shipper_code"]
        slots, serr = oa.get_accessible_list(token, sender_region, receiver_region,
                                             probe_shipper, args.timeout)
        if serr:
            print(f"[失败] 取件时间段查询失败：{serr}", file=sys.stderr)
            return 1
        print(f"\n[{probe_shipper}] 可取件时间段共 {len(slots)} 段：")
        for i, s in enumerate(slots, 1):
            print(f"  [{i}] {oa.fmt_slot(s)}（{s['start']} ~ {s['end']}）")
        print("\n用 --pickup <序号> 指定，默认选最早的可用时段。")
        return 0

    # 姓名/电话优先级：显式参数 > 整段文本识别结果 > 地址簿默认值
    s_name = args.from_name or s_auto[0] or default_sender["name"]
    s_phone = args.from_phone or s_auto[1] or default_sender["phone"]
    r_name = args.to_name or r_auto[0]
    r_phone = args.to_phone or r_auto[1]
    if not s_name or not s_phone:
        print("[失败] 缺少寄件人姓名或电话：请用 --from-name/--from-phone 提供，"
              "或用 --from-text 智能识别，或在官网地址簿里设置默认寄件人。",
              file=sys.stderr)
        return 2
    if not r_name or not r_phone:
        print("[失败] 缺少收件人姓名或电话：请用 --to-name/--to-phone 提供，"
              "或用 --to-text 智能识别。", file=sys.stderr)
        return 2

    ctx, err = prepare_order(
        sender_region, receiver_region, s_name, s_phone,
        r_name, r_phone, args.weight, args.goods,
        token, args.creds, quantity=args.quantity, pay_type=args.pay_type,
        remark=args.remark, shipper=args.shipper, pickup=args.pickup,
        timeout=args.timeout, confirm=args.confirm)
    if err:
        print(f"\n[失败] {err}", file=sys.stderr)
        print(price_hint(f"下单准备失败：{err}"), file=sys.stderr)
        return 1

    print()
    print_preview(ctx)

    if not args.confirm:
        print("\n这是预览，未提交。确认无误后加 --confirm 提交（将从账户余额扣款，不可撤销）。")
        if ctx["slots"] and len(ctx["slots"]) > 1:
            print(f"可选取件时间段共 {len(ctx['slots'])} 段，"
                  f"当前第 {ctx['slot_index']} 段；用 --pickup N 切换，--list-slots 查看全部。")
        if args.output:
            made = export_batch(args.output, [ctx], False)
            print(f"[已导出] {'、'.join(os.path.basename(m) for m in made)}")
        return 0

    print("\n[提交中] 正在调用 PlaceOrder…")
    data, err, msg = submit_order(ctx, token, args.timeout, log=not args.no_log)
    if err:
        print(f"\n[失败] 下单失败：{err}", file=sys.stderr)
        print(price_hint(f"PlaceOrder 调用失败：{err}"), file=sys.stderr)
        return 1
    print()
    print_result(ctx, data, msg)
    if not args.no_log:
        print(f"  订单已记录到：{ORDER_LOG}")
    if args.output:
        made = export_batch(args.output, [ctx], True)
        print(f"[已导出] {'、'.join(os.path.basename(m) for m in made)}")
    return 0


if __name__ == "__main__":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    sys.exit(main())

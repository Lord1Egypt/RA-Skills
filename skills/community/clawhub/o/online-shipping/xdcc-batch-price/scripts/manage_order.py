#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
manage_order.py — 小递查查「我的寄件」：列表 / 详情 / 取消

对应官网页面：https://xdccy.com/send/DeliveryManage.aspx
逆向得到的接口（均在 /dist/js/config.js 里）：

  POST /ToDoorOrder/SearchOrderList   寄件列表（Data.ResultList）
  POST /ToDoorOrder/GetOrderDetail    订单详情（寄/收件人完整号码、取消原因）
  POST /ToDoorOrder/CancelOrder       取消寄件，请求体只有 {"OrderCode": "..."}

⚠️ 安全/预期管理：
  CancelOrder 没有预览态，调了就是真的取消。所以本脚本默认只做「预演」——
  把将要取消的订单完整列出来并要求显式 `--confirm`，才会真的调接口。
  与 place_order.py 的安全门是同一套思路。

用法：
  # 我的寄件列表（默认最近 50 条）
  python manage_order.py list

  # 只看可取消的（未取件前）
  python manage_order.py list --cancelable

  # 按单号/运单号查
  python manage_order.py list --keyword 260926000005

  # 只看已签收
  python manage_order.py list --order-status 8

  # 订单详情
  python manage_order.py show 260926000005

  # 取消寄件（预演：只打印不执行）
  python manage_order.py cancel 260926000005

  # 确认取消（真执行）
  python manage_order.py cancel 260926000005 --confirm

退出码：0=成功；1=操作失败；2=参数错误。
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_creds, get_token, price_hint  # noqa: E402
from price_query import DEFAULT_CREDS  # noqa: E402  与其它脚本共用同一份凭据路径
import order_api as oa  # noqa: E402

# OUT 只在调用时才解析成 sys.stdout：模块导入时绑定的话，
# 重定向 stdout 的测试（以及 place_order.py 踩过的同一个坑）就抓不到输出。
OUT_ALIAS = None


# --------------------------------------------------------------------------- #
# 输出助手
# --------------------------------------------------------------------------- #
def emit(text=""):
    print(text, file=OUT_ALIAS or sys.stdout)


def die(msg, code=1):
    emit(f"❌ {msg}")
    return code


def dump_json(obj):
    emit(json.dumps(obj, ensure_ascii=False, indent=2))


def _money(v):
    return f"¥{v:.2f}"


def print_order(row):
    """打印一行订单（对齐页面「寄件列表」的列）。"""
    flag = "✅可取消" if row["cancelable"] else "　不可取消"
    emit(f"· {row['order_code']}  {row['shipper']}")
    emit(f"    收件 {row['receiver']}（{row['receiver_mobile']}）{row['receiver_address']}")
    emit(f"    状态 {row['order_status']} / 物流 {row['logistics_status']} / 支付 {row['pay_status']}"
         f"   预估运费 {_money(row['predict_cost'])}   {flag}")
    emit(f"    下单 {row['create_time']}")
    if row["logistics_code"]:
        emit(f"    运单号 {row['logistics_code']}")


# --------------------------------------------------------------------------- #
# 子命令
# --------------------------------------------------------------------------- #
def cmd_list(args, token, creds_path):
    rows, total, err = oa.search_order_list(
        token,
        keyword=args.keyword,
        shipper_code=args.shipper,
        order_status=args.order_status if args.order_status is not None else "",
        receiver_mobile=args.phone,
        page_index=1,
        page_size=args.limit,
        timeout=args.timeout,
    )
    if err:
        msg = price_hint("网页登录已失效，请重新登录") if err == "AUTH" \
            else f"查询寄件列表失败：{err}"
        return die(msg)

    out_rows = []
    for r in (rows or []):
        row = oa.fmt_order_row(r)
        if args.cancelable and not row["cancelable"]:
            continue
        out_rows.append(row)

    if args.json:
        dump_json({"total": total, "returned": len(rows or []), "orders": out_rows})
        return 0

    if not out_rows:
        emit("📭 没有符合条件的寄件记录。")
        return 0

    emit(f"📦 全部 {total} 条寄件；接口一次只回最近 {len(rows or [])} 条，"
         f"这里显示 {len(out_rows)} 条\n")
    for row in out_rows:
        print_order(row)
        emit("")
    if len(out_rows) < len(rows or []):
        emit(f"… 已按 --limit={args.limit} 截断，去掉该参数可看完整 {len(rows or [])} 条")
    elif total > len(rows or []):
        emit(f"… 还有更早的 {total - len(rows or [])} 条：接口不认翻页参数，"
             f"请用 --keyword / --order-status 等条件收窄")
    return 0


def cmd_show(args, token, creds_path):
    data, err = oa.get_order_detail(token, args.order_code, timeout=args.timeout)
    if err:
        return die(price_hint("登录已失效，请重新登录") if err == "AUTH"
                   else f"查询订单详情失败：{err}")

    if args.json:
        dump_json(data)
        return 0

    sender = data.get("Sender") or {}
    receiver = data.get("Receiver") or {}
    cost = data.get("PredictCost") or 0
    emit(f"📄 订单 {data.get('OrderCode')}")
    emit(f"  快递公司   {data.get('ShipperName') or '-'}"
         f"（编码 {data.get('ShipperCode') or '-'}）")
    emit(f"  运单号     {data.get('LogisticsCode') or '尚未产生'}")
    emit(f"  运单状态   物流{oa.fmt_logistics_status(data.get('OrderStatus'), data.get('LogisticsStatus'))}"
         f" / 订单{oa.fmt_order_status(data.get('OrderStatus'))}"
         f" / 支付{oa.fmt_pay_status(data.get('PayStatus'))}")
    emit(f"  预估运费   {_money(float(cost or 0))}   物品：{data.get('GoodsName') or '-'}"
         f"   重量 {data.get('Weight') or '-'}kg")
    emit(f"  寄件人     {sender.get('FullName') or '-'} {sender.get('Mobile') or sender.get('Tel') or ''}")
    emit(f"            {_party_addr(sender)}")
    emit(f"  收件人     {receiver.get('FullName') or '-'} {receiver.get('Mobile') or receiver.get('Tel') or ''}")
    emit(f"            {_party_addr(receiver)}")
    if data.get("PickupCourier"):
        emit(f"  取件员     {data.get('PickupCourier')} {data.get('PickupCourierPhone') or ''}")
    if data.get("CancelTime"):
        emit(f"  取消时间   {data.get('CancelTime')}（{data.get('CancelType')}）")
    if data.get("PlaceOrderFailMsg"):
        emit(f"  失败原因   {data.get('PlaceOrderFailMsg')}")
    emit(f"  下单时间   {data.get('CreateTime') or '-'}")
    if oa.can_cancel(data):
        emit("\n✅ 该订单尚未取件，可执行 `cancel` 取消。")
    else:
        emit("\nℹ️ 该订单已离开可取消阶段（页面操作栏在 OrderStatus 为 1/2/3 时才显示取消）。")
    return 0


def _party_addr(party):
    parts = [party.get("ProvinceName") or "", party.get("CityName") or "",
             party.get("AreaName") or "", party.get("Address") or ""]
    return "".join(p for p in parts if p) or "-"


def cmd_cancel(args, token, creds_path):
    code = (args.order_code or "").strip()
    if not code:
        return die("请给出要取消的订单号", 2)

    # 先查详情，好判断是否还在可取消阶段、取消的是哪一笔
    data, err = oa.get_order_detail(token, code, timeout=args.timeout)
    if err:
        return die(price_hint("登录已失效，请重新登录") if err == "AUTH"
                   else f"查询订单失败（取消会中止）：{err}")

    order_status = oa._as_int(data.get("OrderStatus"))
    if not oa.can_cancel(data):
        emit(f"ℹ️ 订单 {code} 当前状态是「{oa.fmt_order_status(data.get('OrderStatus'))}」，"
             f"不属于可取消范围（仅下单成功/分配网点/分配快递员可取消），跳过。")
        return 0

    row = oa.fmt_order_row(data)
    if args.json:
        dump_json(row)
        return 0

    emit("⚠️ 即将取消以下寄件订单：")
    print_order(row)

    if not args.confirm:
        emit("\n🛑 这是预演，没有真的取消。确认要取消请加 --confirm：")
        emit(f"   python manage_order.py cancel {code} --confirm")
        return 0

    payload_data, err = oa.cancel_order(token, code, timeout=args.timeout)
    if err:
        return die(price_hint("登录已失效，请重新登录") if err == "AUTH"
                   else f"取消失败：{err}")
    emit(f"\n✅ 已取消订单 {code}（状态「{oa.fmt_order_status(order_status)}」→「"
         f"{oa.fmt_order_status(6)}」）。")
    return 0


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _positive_int(v):
    n = int(v)
    if n < 1:
        raise argparse.ArgumentTypeError("必须 >= 1")
    return n


def build_parser():
    p = argparse.ArgumentParser(
        prog="manage_order.py",
        description="小递查查 · 我的寄件（列表 / 详情 / 取消）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("list", help="寄件列表")
    sp.add_argument("--keyword", help="订单号或运单号关键字")
    sp.add_argument("--shipper", help="快递公司关键字（如 极兔 / 中通 / SF）")
    sp.add_argument("--order-status", type=int, help="订单状态：1下单成功 2分配网点 3分配快递员 "
                                                     "4已取件 5已揽件 6已取消 7在途中 8已签收 9已赔付 10下单失败")
    sp.add_argument("--phone", help="收件人手机号关键字")
    sp.add_argument("--cancelable", action="store_true", help="只看可取消的（未取件前）")
    sp.add_argument("--limit", type=_positive_int, default=50, help="每页条数，默认 50")
    sp.add_argument("--json", action="store_true", help="输出 JSON")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("show", help="订单详情")
    sp.add_argument("order_code", help="订单号")
    sp.add_argument("--json", action="store_true", help="输出 JSON")
    sp.set_defaults(func=cmd_show)

    sp = sub.add_parser("cancel", help="取消寄件（默认预演，需 --confirm 才真执行）")
    sp.add_argument("order_code", help="订单号")
    sp.add_argument("--confirm", action="store_true", help="确认执行取消")
    sp.add_argument("--json", action="store_true", help="输出 JSON")
    sp.set_defaults(func=cmd_cancel)

    for sp in (sub.choices.get("list"), sub.choices.get("show"), sub.choices.get("cancel")):
        if not sp:
            continue
        sp.add_argument("--token", help="直接指定网页登录 token")
        sp.add_argument("--creds", default=DEFAULT_CREDS, help="凭据文件路径")
        sp.add_argument("--timeout", type=int, default=30, help="接口超时秒数（默认30）")

    p.add_argument("--token", help="直接指定网页登录 token")
    p.add_argument("--creds", default=DEFAULT_CREDS, help="凭据文件路径")
    p.add_argument("--timeout", type=int, default=30, help="接口超时秒数（默认30）")
    return p


def main(argv=None):
    p = build_parser()
    args = p.parse_args(argv)
    if not getattr(args, "cmd", None):
        p.print_help()
        return 2

    token = args.token or get_token(load_creds(args.creds))
    if not token:
        emit("❌ 没有网页登录 token。先执行 `web_login.py` 登录后再试。")
        return 1
    return args.func(args, token, args.creds)


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ticket.py — 小递查查「工单」：查看 / 提交

对应官网页面：
  提交 https://xdccy.com/AddWorkOrder.html?type=3&SourcePage=1&orderCode=xxx
  列表 https://xdccy.com/WorkOrderManage.html
  入口寄件页：https://xdccy.com/send/DeliveryManage.aspx 的「提交工单/查看工单」
（注意：这两个页面在**根目录**下，不是 /send/ 下）

逆向得到的接口（/dist/js/config.js?v=19881）：

  POST /ToDoorOrder/GetWorkOrderCategoryList   工单类型树（空请求体）
  POST /ToDoorOrder/GetWorkOrderList           工单列表（Data.ResultList）
  POST /ToDoorOrder/GetWorkOrderDetail         工单详情 —— 参数是**内部自增 ID**
  POST /ToDoorOrder/AddWorkOrder               提交工单（type=3）
  POST /ToDoorOrder/WaybillIntercept           运单拦截（type=1 转寄 / 2 退回）

⚠️ 两个坑（都是实测踩出来的）：
  1) 工单详情要用 WorkOrderCode（如 260918000015）查不通，报「工单ID不能为空」，
     得用列表行里的内部自增 ID（如 819）。所以 `detail` 支持按工单号查，
     内部先去列表里把 ID 捞出来。
  2) type=3 的必填项由前端 workOrderTypeMap 控制（重量异常要反馈重量、
     破损/丢件/少件要商品价值、更改收件信息要新收件人三段），接口分类树
     GetWorkOrderCategoryList 不返回这些标记，脚本里内置了 WORK_ORDER_RULES。

⚠️ 安全设计：提交工单**默认只预览**（打印完整提交体），加 --confirm 才真的提交。

用法：
  # 工单类型（提交前先看有哪些可选）
  python ticket.py categories

  # 我的工单
  python ticket.py list
  python ticket.py list --status 0          # 只看待处理
  python ticket.py list --status 1 --json

  # 工单详情（工单号或内部 ID）
  python ticket.py detail 260918000015

  # 提交工单（预演）
  python ticket.py new --order-code 260926000005 --type 丢件 --content "包裹一直没到"
  python ticket.py new --order-code 260926000005 --type "投诉/快递员服务态度差" \
      --content "上门态度很差" --name 张三 --phone 13800138000 --confirm

  # 拦截转寄 / 拦截退回（type=1/2，必须带月结号）
  python ticket.py intercept --order-code 260926000005 --type 2 \
      --month-code 7890123 --name 张三 --phone 13800138000

退出码：0=成功；1=操作失败；2=参数错误。
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_creds, get_token, price_hint  # noqa: E402
from price_query import DEFAULT_CREDS  # noqa: E402
import order_api as oa  # noqa: E402

# 与 manage_order.py 同样的处理：OUT_ALIAS 由调用方注入，默认取当前 sys.stdout，
# 这样 contextlib.redirect_stdout 能抓到输出（导入期绑定 sys.stdout 会抓不到）。
OUT_ALIAS = None


def emit(text=""):
    print(text, file=OUT_ALIAS or sys.stdout)


def die(msg, code=1):
    emit(f"❌ {msg}")
    return code


def dump_json(obj):
    emit(json.dumps(obj, ensure_ascii=False, indent=2))


# --------------------------------------------------------------------------- #
# 子命令
# --------------------------------------------------------------------------- #
def cmd_categories(args, token, creds_path):
    groups, err = oa.get_work_order_categories(token, timeout=args.timeout)
    if err:
        return die(price_hint("网页登录已失效，请重新登录") if err == "AUTH"
                   else f"获取工单类型失败：{err}")
    if args.json:
        dump_json(groups)
        return 0

    flat = oa.flatten_work_order_categories(groups)
    extra = [{"code": 18, "name": "更改收件信息", "group": "其他"}]
    emit("🧾 可选工单类型（提交时 --type 可用名称、编码或 分组/类型）：\n")
    for g in groups:
        items = g.get("items") or []
        if not items:
            continue
        emit(f"【{g['group']}】")
        for it in items:
            emit(f"  {it['code']:<8} {it['name']}")
    emit("\n【其他（接口未返回，页面手工补充）】")
    emit(f"  {'18':<8} 更改收件信息")
    emit("\n提示：选「重量/运费异常」要填 --tel-weight，"
         "选「丢件/包裹破损/收到后少件/包裹收到错件」要填 --goods-value，"
         "选「更改收件信息」要填 --new-name/--new-phone/--new-address。")
    return 0


def cmd_list(args, token, creds_path):
    status = "" if args.status in (None, "all", "全部", "") else str(args.status)
    rows, total, err = oa.search_work_orders(
        token, status=status, page_size=args.limit, timeout=args.timeout)
    if err:
        return die(price_hint("网页登录已失效，请重新登录") if err == "AUTH"
                   else f"获取工单列表失败：{err}")

    out_rows = [oa.fmt_work_order_row(r) for r in (rows or [])]
    if args.json:
        dump_json({"total": total, "count": len(out_rows), "work_orders": out_rows})
        return 0
    if not out_rows:
        emit("📭 没有符合条件的工单。")
        return 0

    emit(f"🎫 工单共 {total} 条，这里显示 {len(out_rows)} 条\n")
    for r in out_rows:
        emit(f"· {r['work_order_code']}  [{r['type_name']}]  {r['status']}")
        emit(f"    关联订单 {r['order_code']}   快递 {r['shipper']}   运单 {r['logistics_code']}")
        content = r["content"].replace("\n", " / ")
        emit(f"    内容 {content or '-'}")
        emit(f"    提交 {r['create_time']}   回复 {r['reply_time']} {r['reply']}")
        emit("")
    return 0


def cmd_detail(args, token, creds_path):
    ident = (args.work_order or "").strip()
    if not ident:
        return die("请给出工单号或内部 ID", 2)

    # 接口只认内部自增 ID（传工单号会报「工单ID不能为空」），所以先按工单号
    # 在列表里把 ID 捞出来；如果用户直接给的就是内部 ID，这一趟捞不到，
    # 就原样当 ID 用。
    lists_err = None
    hit = None
    try:
        rows, _t, lists_err = oa.search_work_orders(token, page_size=args.limit,
                                                    timeout=args.timeout)
        for r in (rows or []):
            if (r.get("WorkOrderCode") or "") == ident:
                hit = r
                break
    except Exception:          # pragma: no cover
        rows = []
    real_id = (hit or {}).get("ID") or ident
    if hit and args.json:
        dump_json(hit)
        return 0
    if hit:
        emit(f"ℹ️ 内部 ID 是 {real_id}，正在用它拉取详情…\n")

    data, err = oa.get_work_order_detail(token, real_id, timeout=args.timeout)
    if err:
        if not hit and not lists_err:
            return die(f"工单号 {ident} 不在最近 {len(rows or [])} 条工单里，"
                       f"也可能它本身就不是内部 ID；试试列表里的 ID 字段")
        return die(f"查询工单详情失败（内部 ID={real_id}）：{err}")

    if args.json:
        dump_json(data)
        return 0

    emit(f"🎫 工单 {data.get('WorkOrderCode')}")
    emit(f"  关联订单 {data.get('OrderCode') or '-'}   快递 {data.get('ShipperName') or '-'}"
         f"   运单 {data.get('LogisticsCode') or '-'}")
    code = oa._as_int(data.get("WorkOrderType"))
    emit(f"  类型     {data.get('WorkOrderName') or oa.WORK_ORDER_TYPE_NAME.get(code, '-')}"
         f"（编码 {code}）")
    emit(f"  状态     {oa.fmt_work_order_status(data.get('WorkOrderStatus'))}"
         f"   提交 {data.get('CreateTime') or '-'}")
    emit(f"  内容     {(data.get('WorkOrderContent') or '-')}")
    reply = data.get("WorkOrderReplyList") or []
    if reply:
        emit("  处理记录：")
        for r in reply:
            emit(f"    - {r.get('ReplyDateTime') or '-'}  {(r.get('ReplyContent') or '').strip()}")
    else:
        emit("  处理记录：暂无")
    if data.get("ReplyContent"):
        emit(f"  最新回复 {data.get('ReplyDateTime') or ''} {data.get('ReplyContent')}")
    if data.get("ToKdnMsg"):
        emit(f"  快递100 {data.get('ToKdnMsg')}（状态 {data.get('ToKdnStatus')}）")
    images = data.get("OrderImages") or []
    if isinstance(images, str):
        try:
            images = json.loads(images)
        except (ValueError, TypeError):
            images = [images]
    if images:
        emit(f"  凭证     {len(images)} 张：{images[0]}")
    return 0


def cmd_new(args, token, creds_path):
    payload, wmsg, fatal = _build_payload(args, token, creds_path)
    if fatal:
        return die("；".join(fatal), 2)
    if wmsg:
        for w in wmsg:
            emit(f"⚠️ {w}")
        emit("")

    if args.json:
        dump_json(payload)
        return 0

    emit("🧾 即将提交以下工单（预览，未提交）：\n")
    _print_payload(payload)
    if not args.confirm:
        emit("\n🛑 确认无误后加 --confirm 再执行，例如：")
        emit(f"   python ticket.py new --order-code {payload.get('OrderCode')} "
             f"--type {payload.get('WorkOrderType')} --confirm")
        return 0


    data, err = oa.add_work_order(token, payload, timeout=args.timeout)
    if err:
        return die(price_hint("网页登录已失效，请重新登录") if err == "AUTH"
                   else f"提交工单失败：{err}")
    emit(f"\n✅ 工单提交成功。工单号 {data.get('WorkOrderCode') or '（稍后可在工单列表查看）'}")
    emit(f"   客服将在 1 小时内回复，可用 `ticket.py detail "
         f"{data.get('WorkOrderCode') or ''}` 跟踪。")
    return 0


def cmd_intercept(args, token, creds_path):
    """拦截转寄(1) / 拦截退回(2)：走 WaybillIntercept，必须带月结号。"""
    payload, wmsg, fatal = _build_payload(args, token, creds_path, intercept=True)
    if fatal:
        return die("；".join(fatal), 2)
    if wmsg:
        for w in wmsg:
            emit(f"⚠️ {w}")
        emit("")

    emit(f"🚧 即将提交运单拦截（type={payload.get('Type')}）：\n")
    _print_payload(payload)
    if not args.confirm:
        emit("\n🛑 确认无误后加 --confirm 再执行。")
        return 0

    data, err = oa.intercept_waybill(token, payload, timeout=args.timeout)
    if err:
        return die(price_hint("网页登录已失效，请重新登录") if err == "AUTH"
                   else f"提交拦截失败：{err}")
    emit(f"\n✅ 拦截申请已提交（工单号 {data.get('WorkOrderCode') or '-'}）。")
    return 0


def _build_payload(args, token, creds_path, intercept=False):
    """按参数组装提交体，顺带做本地校验。返回 (payload, warnings, fatal)。"""
    order_code = (args.order_code or "").strip()
    if not order_code:
        return {}, [], ["请给出 --order-code（工单必须关联某一笔寄件订单）"]

    # 联系人：优先显式参数，其次回落到地址簿默认寄件人（页面这两栏是空表单，
    # 用户得自己填；这里替他填一次更省事）
    name = (args.name or "").strip()
    phone = (args.phone or "").strip()
    warnings = []
    if not name or not phone:
        addr, err = oa.get_default_addr(token, timeout=args.timeout)
        if not err and addr:
            name = name or (addr.get("FullName") or "")
            phone = phone or (addr.get("MobilePhone") or addr.get("Mobile") or "")
        else:
            warnings.append("取默认寄件人失败，联系人字段可能为空（接口可能要求必填）")
    if not name:
        warnings.append("没有联系人姓名，建议用 --name 指定")

    if intercept:
        payload = oa.build_intercept_payload(
            order_code, args.intercept_type, args.month_code,
            name, phone,
            province=args.new_province or "", city=args.new_city or "",
            area=args.new_area or "", address=args.new_address or "")
        return payload, warnings, []

    # 先类型后内容：类型决定要不要附带反馈重量 / 商品价值 / 新收件信息
    if not args.type:
        return {}, warnings, ["请给出 --type（先用 `ticket.py categories` 看看有哪些类型）"]
    groups, err = oa.get_work_order_categories(token, timeout=args.timeout)
    if err:
        return {}, warnings, [f"获取工单类型失败：{err}"]
    cat, cerr = oa.match_work_order_category(groups, args.type)
    if cerr:
        return {}, warnings, [cerr.rstrip("，可用：") + "，可用：" +
                              "、".join(f"{c['name']}" for c in
                                        oa.flatten_work_order_categories(groups))]
    payload = oa.build_work_order_payload(
        order_code, cat["code"], args.content, name, phone,
        tel_weight=args.tel_weight, modity_value=args.goods_value,
        new_receiver_name=args.new_name, new_receiver_phone=args.new_phone,
        new_receiver_address=args.new_address)
    w2, fatal = oa.validate_work_order(payload)
    return payload, warnings + w2, fatal


def _print_payload(payload):
    labels = {
        "OrderCode": "订单号", "Type": "类型", "WorkOrderType": "工单类型编码",
        "WorkOrderContent": "问题描述", "LinkMan": "联系人", "MobilePhone": "联系电话",
        "Reason": "附言", "Role": "发起方", "PayMode": "付款方式",
        "SourcePage": "来源页", "ImageNameList": "凭证", "TelWeight": "反馈重量",
        "ModityValue": "商品价值", "NewReceiverName": "新收件人",
        "NewReceiverPhone": "新收件人电话", "NewReceiverAddress": "新收件地址",
    }
    type_map = {1: "1-拦截转寄", 2: "2-拦截退回", 3: "3-工单反馈"}
    for k, v in payload.items():
        if k == "ImageNameList":
            continue
        if k == "Type":
            v = f"{v}（{type_map.get(v, '')}）"
        emit(f"  {labels.get(k, k)}：{v}")
    emit("  ImageNameList：（本技能无图片上传能力，留空）")


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser():
    p = argparse.ArgumentParser(
        prog="ticket.py",
        description="小递查查 · 工单（查看 / 提交）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("categories", help="列出可选工单类型")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_categories)

    sp = sub.add_parser("list", aliases=["ls"], help="工单列表")
    sp.add_argument("--status", help="工单状态：0待处理 1已处理 2已关闭；不给查全部")
    sp.add_argument("--limit", type=int, default=50, help="显示条数，默认 50")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("detail", aliases=["show"], help="工单详情（工单号或内部 ID）")
    sp.add_argument("work_order", help="工单号（如 260918000015）或内部 ID（如 819）")
    sp.add_argument("--limit", type=int, default=50, help="查 ID 时看多少条工单，默认 50")
    sp.add_argument("--json", action="store_true")
    sp.set_defaults(func=cmd_detail)

    sp = sub.add_parser("new", help="提交工单（默认预览，--confirm 才提交）")
    sp.add_argument("--order-code", dest="order_code", required=True, help="关联寄件订单号")
    sp.add_argument("--type", dest="type", help='工单类型：编码 / 名称 / "分组/类型"')
    sp.add_argument("--content", dest="content", help="问题描述")
    sp.add_argument("--name", help="联系人姓名（不给则取地址簿默认寄件人）")
    sp.add_argument("--phone", help="联系电话")
    sp.add_argument("--tel-weight", dest="tel_weight", help="反馈重量（重量/运费异常必填，如 2.5kg）")
    sp.add_argument("--goods-value", dest="goods_value",
                    help="商品价值（丢件/破损/少件/错件必填，如 199.00）")
    sp.add_argument("--new-name", dest="new_name", help="新收件人姓名（更改收件信息必填）")
    sp.add_argument("--new-phone", dest="new_phone", help="新收件人电话（更改收件信息必填）")
    sp.add_argument("--new-address", dest="new_address",
                    help="新收件地址（更改收件信息必填，省市区+详细地址）")
    sp.add_argument("--json", action="store_true")
    sp.add_argument("--confirm", action="store_true", help="确认提交")
    sp.set_defaults(func=cmd_new)

    sp = sub.add_parser("intercept", help="运单拦截：1-转寄 2-退回（默认预览）")
    sp.add_argument("--order-code", dest="order_code", required=True, help="寄件订单号")
    sp.add_argument("--type", dest="intercept_type", type=int, default=2,
                    choices=[1, 2], help="1-拦截转寄，2-拦截退回（默认 2）")
    sp.add_argument("--month-code", dest="month_code", required=True, help="月结号（必填）")
    sp.add_argument("--name", help="联系人姓名")
    sp.add_argument("--phone", help="联系电话")
    sp.add_argument("--new-province", dest="new_province", help="新收件省份（type=1 必填）")
    sp.add_argument("--new-city", dest="new_city", help="新收件城市（type=1 必填）")
    sp.add_argument("--new-area", dest="new_area", help="新收件区县（type=1 必填）")
    sp.add_argument("--new-address", dest="new_address", help="新收件详细地址（type=1 必填）")
    sp.add_argument("--json", action="store_true")
    sp.add_argument("--confirm", action="store_true", help="确认提交")
    sp.set_defaults(func=cmd_intercept)

    # 注意：add_parser(aliases=[...]) 会把同一个 parser 注册到多个 choices 键下，
    # 直接遍历会重复加参数并报 conflicting option，这里按对象去重。
    seen = set()
    for sp in sub.choices.values():
        if id(sp) in seen:
            continue
        seen.add(id(sp))
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

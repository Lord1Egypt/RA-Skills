"""
Item Management CLI
Usage: python item_cli.py <command> [args]
Commands:
  add <name> [--brand B] [--qty N] [--unit S] [--prod YYYY-MM-DD] [--expiry YYYY-MM-DD]
             [--warranty YYYY-MM-DD] [--opened YYYY-MM-DD] [--location S] [--notes S]
             [--price N] [--tags A,B,C] [--image PATH]
  list [--sort name|brand|expiry_date|created_at|quantity] [--order asc|desc] [--tag T]
  get <id>
  update <id> [--name S] [--brand S] [--qty N] [--price N] [--expiry YYYY-MM-DD]
              [--warranty YYYY-MM-DD] [--opened YYYY-MM-DD] [--location S]
              [--notes S] [--tags A,B,C] [--status active|consumed|discarded]
  delete <id>
  sub-add <parent_id> <name> [--qty N] [--unit S] [--expiry YYYY-MM-DD] [--notes S]
  sub-list <parent_id>
  sub-update <sub_id> [--name S] [--qty N] [--status S] [--expiry YYYY-MM-DD] [--notes S]
  sub-delete <sub_id>
  history <item_id>
  expiring [--days N]
  expired
  stats
  search <query> [--field name|brand|location|tags|notes]
  export [--format csv|json|html] [--out PATH]
  report [--out PATH]
"""
import sys
import json
import csv
import os
import argparse
from datetime import date, datetime, timedelta

sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else __file__.rsplit("/", 1)[0])
import item_db

def _date_progress(expiry_str: str) -> dict:
    """Calculate days until expiry / days since expiry."""
    if not expiry_str:
        return {"expiry_str": None, "days_until": None, "status": "unknown"}
    try:
        expiry = date.fromisoformat(expiry_str)
        today = date.today()
        delta = (expiry - today).days
        return {
            "expiry_str": expiry_str,
            "days_until": delta,
            "status": "expired" if delta < 0 else ("expiring_soon" if delta <= 7 else "ok"),
            "expired_days": abs(delta) if delta < 0 else 0,
        }
    except Exception:
        return {"expiry_str": expiry_str, "days_until": None, "status": "unknown"}

def _daily_price(price: float, prod_date_str: str) -> float:
    """Calculate daily cost since purchase."""
    if not price or not prod_date_str:
        return None
    try:
        prod = date.fromisoformat(prod_date_str)
        today = date.today()
        days = (today - prod).days
        if days <= 0:
            return price  # bought today, full price is daily
        return price / days
    except Exception:
        return None

STATUS_MAP = {'': '—', 'active': '在用', 'consumed': '已用完', 'discarded': '已丢弃'}
def _status_display(status: str) -> str:
    return STATUS_MAP.get(status, status) or '—'

def _usage_time(prod_date_str: str) -> str:
    """Calculate and format usage time since purchase."""
    if not prod_date_str:
        return None
    try:
        prod = date.fromisoformat(prod_date_str)
        today = date.today()
        delta = (today - prod).days
        if delta < 0:
            return None  # future date, ignore
        if delta == 0:
            return "今天"
        elif delta == 1:
            return "1 天"
        elif delta < 30:
            return f"{delta} 天"
        elif delta < 365:
            months = delta // 30
            return f"{months} 个月"
        else:
            years = delta // 365
            months = (delta % 365) // 30
            if months > 0:
                return f"{years} 年 {months} 个月"
            else:
                return f"{years} 年"
    except Exception:
        return None

def _format_item(item: dict, show_progress: bool = True, compact: bool = False, index: int = None) -> str:
    """Format item for display. compact=True for list view, False for detail view."""
    dp = _daily_price(item.get("price"), item.get("production_date"))
    usage = _usage_time(item.get("production_date"))
    
    # Build expiry/warranty tag
    tag_line = ""
    if show_progress and item.get("expiry_date"):
        p = _date_progress(item["expiry_date"])
        if p["days_until"] is not None:
            if p["status"] == "expired":
                tag_line = f"  ⚠️ 已过期 {p['expired_days']} 天"
            elif p["status"] == "expiring_soon":
                tag_line = f"  ⏳ 还剩 {p['days_until']} 天"
            else:
                tag_line = f"  ✅ 剩余 {p['days_until']} 天到期"
    
    idx_str = f"#{index} " if index is not None else ""
    
    if compact:
        # Compact card format for list view
        brand = f" {item['brand']}" if item['brand'] else ""
        price_str = f"¥{item['price']:.0f}" if item['price'] else "—"
        dp_str = f"¥{dp:.2f}/天" if dp is not None else "—"
        date_str = item['production_date'] or "—"
        usage_str = f"已用 {usage}" if usage else "—"
        tags_str = f" 🏷️{' · '.join(item['tags'])}" if item['tags'] else ""
        status_icon = "✅" if item['status'] == 'active' else ("📦" if item['status'] == 'consumed' else "🗑️")
        
        info = f"💰 {price_str} ｜ 📅 {date_str}（{usage_str}） ｜ 📊 {dp_str} ｜ {status_icon}{_status_display(item['status'])}{tags_str}"
        lines = [
            f"  {idx_str}📌 {item['name']}{brand}",
            f"     {info}",
        ]
        if tag_line:
            lines.append(tag_line)
        return "\n".join(lines)
    else:
        # Full detail format — only show fields that have data
        lines = [f"📌 {item['name']}"]
        
        if item['brand']:
            lines.append(f"  品牌: {item['brand']}")
        lines.append(f"  数量: {item['quantity']} {item['unit']}")
        if item['price']:
            lines.append(f"  💰 单价: ¥{item['price']:.2f}")
        if dp is not None:
            lines.append(f"  📊 日均成本: ¥{dp:.2f}/天")
        if item['production_date']:
            lines.append(f"  📅 购入日期: {item['production_date']}（已用 {usage}）")
        if item['location']:
            lines.append(f"  📍 存放位置: {item['location']}")
        if item['opened_date']:
            lines.append(f"  🔓 开封日期: {item['opened_date']}")
        if item['expiry_date']:
            lines.append(f"  ⏰ 保质期至: {item['expiry_date']}")
        if item['warranty_date']:
            lines.append(f"  🔧 保修期至: {item['warranty_date']}")
        lines.append(f"  📌 状态: {_status_display(item['status'])}")
        if item['tags']:
            lines.append(f"  🏷️ 标签: {' · '.join(item['tags'])}")
        if item['notes']:
            lines.append(f"  📝 备注: {item['notes']}")
        
        if tag_line:
            lines.append(f"  {tag_line.strip()}")
        
        # Summary
        total_val = (item['price'] or 0) * (item['quantity'] or 1)
        summary_parts = []
        if item['price']:
            summary_parts.append(f"总价值 💰¥{total_val:,.0f}")
        if usage:
            summary_parts.append(f"已用 {usage}")
        if item['tags']:
            summary_parts.append(f"分类 🏷️{' · '.join(item['tags'])}")
        if summary_parts:
            lines.append(f"")
            lines.append(f"  📋 总结：{' ｜ '.join(summary_parts)}")
        
        return "\n".join(lines)

# ──────────────────────────────────────────────
# Commands
# ──────────────────────────────────────────────

def cmd_add(args):
    tags = args.tags.split(",") if args.tags else []
    item_id = item_db.add_item(
        name=args.name,
        brand=args.brand,
        quantity=args.qty,
        unit=args.unit,
        production_date=args.prod,
        expiry_date=args.expiry,
        warranty_date=args.warranty,
        opened_date=args.opened,
        location=args.location,
        notes=args.notes,
        price=args.price,
        tags=tags,
        image_path=args.image,
    )
    item = item_db.get_item(item_id)
    print(f"✅ 添加成功！\n{_format_item(item)}")
    print(f"\n💡 想备份数据防丢失？直接说「查看物品存储信息」")

def cmd_list(args):
    items = item_db.list_items(sort_by=args.sort, order=args.order, filter_tag=args.tag)
    if not items:
        print("🎒 哎呀，物品架空空如也！快去添加第一件宝贝吧～")
        return
    total_val = sum(it["price"] or 0 for it in items)
    print(f"🎉 我来啦我来啦，帮你找到了 {len(items)} 件宝贝！总价值约 ¥{total_val:,.0f}～\n")
    
    # Table header
    print(f"{'#':<4} {'名称':<10} {'品牌':<16} {'💰价格':<12} {'购入日期':<12} {'已用时间':<14} {'📊日均':<10} {'📌状态':<8} {'标签'}")
    print("─" * 115)
    
    for idx, item in enumerate(items, 1):
        dp = _daily_price(item.get("price"), item.get("production_date"))
        usage = _usage_time(item.get("production_date")) or "—"
        dp_str = f"¥{dp:.2f}" if dp is not None else "—"
        prod = item['production_date'] or "—"
        brand = item['brand'] or "—"
        name = item['name'][:8]
        status = _status_display(item['status'])
        tags = " · ".join(item['tags']) if item['tags'] else "—"
        price_str = f"¥{item['price']:,.0f}" if item['price'] else "—"
        
        # Add emojis to values
        status_emoji = "✅" if item['status'] == 'active' else ("📦" if item['status'] == 'consumed' else "🗑️")
        status_str = f"{status_emoji}{status}"
        price_emoji_str = f"💰{price_str}" if price_str != "—" else "—"
        dp_emoji_str = f"📊{dp_str}" if dp_str != "—" else "—"
        
        print(f"{idx:<4} {name:<10} {brand:<16} {price_emoji_str:<14} {prod:<12} {usage:<14} {dp_emoji_str:<12} {status_str:<10} {tags}")
    
    print("─" * 115)
    # Lively summary
    total_count = len(items)
    total_val = sum((it["price"] or 0) * (it["quantity"] or 1) for it in items)
    active_count = sum(1 for it in items if it["status"] == "active")
    all_tags = []
    for it in items:
        for t in it["tags"]:
            if t not in all_tags:
                all_tags.append(t)
    tag_str = " · ".join(all_tags) if all_tags else "还没分类~"
    
    summary_lines = [
        f"📊 共 {total_count} 件宝贝，总价值 💰¥{total_val:,.0f}，其中 {active_count} 件还在用～",
        f"🏷️ 已分类：{tag_str}"
    ]
    for line in summary_lines:
        print(f"  {line}")
    print("\n💡 想备份数据防丢失？直接说「查看物品存储信息」")

def cmd_get(args):
    item = item_db.get_item(args.id)
    if not item:
        print(f"❌ 未找到 id={args.id} 的物品。")
        return
    print(_format_item(item))
    subs = item_db.list_subitems(args.id)
    if subs:
        print(f"\n  ─── 子物品 ({len(subs)}件) ───")
        for s in subs:
            p = _date_progress(s.get("expiry_date"))
            expiry_tag = ""
            if p["days_until"] is not None:
                if p["status"] == "expired":
                    expiry_tag = f" ⚠️已过期{p['expired_days']}天"
                elif p["status"] == "expiring_soon":
                    expiry_tag = f" ⏳还剩{p['days_until']}天"
            print(f"  · {s['name']} ×{s['quantity']}{s['unit']}{expiry_tag}")

def cmd_update(args):
    fields = {}
    if args.name is not None: fields["name"] = args.name
    if args.brand is not None: fields["brand"] = args.brand
    if args.qty is not None: fields["quantity"] = args.qty
    if args.price is not None: fields["price"] = args.price
    if args.prod is not None: fields["production_date"] = args.prod
    if args.expiry is not None: fields["expiry_date"] = args.expiry
    if args.warranty is not None: fields["warranty_date"] = args.warranty
    if args.opened is not None: fields["opened_date"] = args.opened
    if args.location is not None: fields["location"] = args.location
    if args.notes is not None: fields["notes"] = args.notes
    if args.status is not None: fields["status"] = args.status
    if args.tags is not None: fields["tags"] = args.tags.split(",")
    if not fields:
        print("❌ 没有提供要更新的字段。")
        return
    ok = item_db.update_item(args.id, **fields)
    if ok:
        item = item_db.get_item(args.id)
        print(f"✅ 更新成功！\n{_format_item(item)}")
    else:
        print(f"❌ 未找到 id={args.id} 的物品。")

def cmd_delete(args):
    ok = item_db.delete_item(args.id)
    print(f"{'✅' if ok else '❌'} 物品 {'已删除' if ok else '未找到'}。")

def cmd_sub_add(args):
    item_db.add_subitem(
        parent_id=args.parent_id,
        name=args.name,
        quantity=args.qty,
        unit=args.unit,
        production_date=args.prod,
        expiry_date=args.expiry,
        opened_date=args.opened,
        notes=args.notes,
    )
    print(f"✅ 子物品添加成功！")

def cmd_sub_list(args):
    subs = item_db.list_subitems(args.parent_id)
    if not subs:
        print("📦 暂无子物品。")
        return
    print(f"📦 子物品 ({len(subs)}件)：\n")
    for s in subs:
        p = _date_progress(s.get("expiry_date"))
        tag = ""
        if p["days_until"] is not None:
            if p["status"] == "expired": tag = f" ⚠️已过期{p['expired_days']}天"
            elif p["status"] == "expiring_soon": tag = f" ⏳还剩{p['days_until']}天"
        print(f"  {s['name']} ×{s['quantity']}{s['unit']} {s['notes'] or ''}{tag}")

def cmd_sub_update(args):
    fields = {}
    if args.name is not None: fields["name"] = args.name
    if args.qty is not None: fields["quantity"] = args.qty
    if args.status is not None: fields["status"] = args.status
    if args.expiry is not None: fields["expiry_date"] = args.expiry
    if args.notes is not None: fields["notes"] = args.notes
    if not fields:
        print("❌ 没有提供要更新的字段。")
        return
    ok = item_db.update_subitem(args.sub_id, **fields)
    print(f"{'✅' if ok else '❌'} 子物品 {'已更新' if ok else '未找到'}。")
    print("\n💡 想备份数据防丢失？直接说「查看物品存储信息」")

def cmd_sub_delete(args):
    ok = item_db.delete_subitem(args.sub_id)
    print(f"{'✅' if ok else '❌'} 子物品 {'已删除' if ok else '未找到'}。")

def cmd_history(args):
    records = item_db.get_history(args.item_id)
    if not records:
        print("📋 暂无历史记录。")
        return
    print(f"📋 物品 #{args.item_id} 变更历史：\n")
    for r in records:
        t = r["changed_at"]
        print(f"  [{t}] 字段「{r['field']}」: {r['old_value']} → {r['new_value']}")

def cmd_expiring(args):
    days = args.days or 7
    items = item_db.get_expiring_items(days=days)
    if not items:
        print(f"✅ 未来 {days} 天内没有即将到期的物品。")
        return
    print(f"⏰ 未来 {days} 天内即将到期的物品 ({len(items)}件)：\n")
    for item in items:
        print(_format_item(item))
        print()
    print("\n💡 想备份数据防丢失？直接说「查看物品存储信息」")

def cmd_expired(args):
    items = item_db.get_expired_items()
    if not items:
        print("✅ 目前没有已过期的物品。")
        return
    print(f"⚠️ 已过期物品 ({len(items)}件)：\n")
    for item in items:
        print(_format_item(item))
        print()
    print("\n💡 想备份数据防丢失？直接说「查看物品存储信息」")

def cmd_stats(args):
    s = item_db.get_stats()
    print("📊 物品数据统计\n")
    print(f"  总物品数: {s['total_items']} 种，{s['total_quantity']} 件")
    print(f"  总估算价值: ¥{s['total_value']:.2f}")
    print(f"  子物品数: {s['total_subitems']} 件")
    print(f"  涉及品牌: {s['total_brands']} 个")
    if s["monthly_new_items"]:
        print(f"\n  近月新增物品：")
        for m in s["monthly_new_items"][:6]:
            print(f"    {m['month']}: {m['count']}件 (约¥{m['value'] or 0:.2f})")
    if s["recent_changes"]:
        print(f"\n  近月变更记录：")
        for c in s["recent_changes"][:6]:
            print(f"    {c['month']} {c['field']}: {c['count']}次")
    print("\n💡 想备份或换设备迁移？直接说「查看物品存储信息」")

def cmd_search(args):
    items = item_db.search_items(args.query, field=args.field)
    if not items:
        print("🔍 未找到匹配的物品。")
        return
    print(f"🔍 找到 {len(items)} 个匹配结果：\n")
    for item in items:
        print(_format_item(item))
        print()
    print("\n💡 想备份数据防丢失？直接说「查看物品存储信息」")

def _item_to_row(item: dict) -> dict:
    """Convert item dict to flat row dict for export."""
    return {
        "名称": item["name"],
        "品牌": item["brand"] or "",
        "数量": item["quantity"],
        "单位": item["unit"],
        "单价": item["price"] or "",
        "日均成本": f"{_daily_price(item.get('price'), item.get('production_date')):.2f}" if _daily_price(item.get('price'), item.get('production_date')) is not None else "",
        "购入日期": item["production_date"] or "",
        "存放位置": item["location"] or "",
        "开封日期": item["opened_date"] or "",
        "保质期至": item["expiry_date"] or "",
        "保修期至": item["warranty_date"] or "",
        "状态": _status_display(item["status"]),
        "标签": ",".join(item["tags"]) if item["tags"] else "",
        "备注": item["notes"] or "",
        "添加时间": item["created_at"],
    }

def cmd_export(args):
    fmt = (args.format or "csv").lower()
    items = item_db.list_items(sort_by="name")
    if not items:
        print("📦 没有可导出的物品。")
        return

    rows = [_item_to_row(it) for it in items]
    today = datetime.now().strftime("%Y%m%d")

    if fmt == "json":
        content = json.dumps(rows, ensure_ascii=False, indent=2)
        fname = args.out or f"物品架_{today}.json"
    elif fmt == "html":
        fname = args.out or f"物品架_{today}.html"
        content = _build_export_html(rows, today)
    else:
        fname = args.out or f"物品架_{today}.csv"
        import io as io_module
        buf = io_module.StringIO()
        if rows:
            w = csv.DictWriter(buf, fieldnames=rows[0].keys())
            w.writeheader()
            w.writerows(rows)
        content = buf.getvalue()

    os.makedirs(os.path.dirname(fname) or ".", exist_ok=True)
    with open(fname, "w", encoding="utf-8-sig" if fmt == "csv" else "utf-8") as f:
        f.write(content)
    print(f"✅ 已导出：{fname}（{len(rows)} 条记录）")

def _build_export_html(rows: list, today: str) -> str:
    total_val = sum(float(r["单价"]) for r in rows if r["单价"])
    total_qty = sum(r["数量"] for r in rows)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>物品架 {today}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
          background: #f5f6fa; color: #2c3e50; padding: 32px; }}
  .card {{ background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 20px;
           box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
  .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }}
  h1 {{ font-size: 22px; font-weight: 700; color: #1a1a2e; }}
  .date {{ color: #888; font-size: 13px; }}
  .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }}
  .stat {{ background: #fff; border-radius: 12px; padding: 20px; text-align: center;
           box-shadow: 0 2px 8px rgba(0,0,0,.08); }}
  .stat .num {{ font-size: 28px; font-weight: 700; color: #6c5ce7; }}
  .stat .lab {{ font-size: 12px; color: #888; margin-top: 4px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  th {{ background: #6c5ce7; color: #fff; padding: 12px 10px; text-align: left;
        font-weight: 600; border-radius: 8px 8px 0 0; }}
  td {{ padding: 11px 10px; border-bottom: 1px solid #f0f0f0; vertical-align: middle; }}
  tr:hover td {{ background: #f8f7ff; }}
  .status {{ display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
  .status-active {{ background: #d4f5e9; color: #00b894; }}
  .status-consumed {{ background: #ffeaa7; color: #d63031; }}
  .status-discarded {{ background: #dfe6e9; color: #636e72; }}
  .tag {{ display: inline-block; background: #e8e4ff; color: #6c5ce7; border-radius: 20px;
          padding: 2px 8px; font-size: 11px; margin: 1px; }}
  .expiry-warn {{ color: #e17055; font-weight: 600; }}
  .expiry-ok {{ color: #00b894; }}
  .footer {{ text-align: center; color: #aaa; font-size: 12px; margin-top: 24px; }}
  @media print {{
    body {{ background: #fff; padding: 0; }}
    .card {{ box-shadow: none; border: 1px solid #eee; }}
    .stat {{ border: 1px solid #eee; }}
    .no-print {{ display: none; }}
    @page {{ margin: 20mm; }}
  }}
</style>
</head>
<body>
<div class="card">
  <div class="header">
    <h1>📦 物品架</h1>
    <span class="date">导出时间：{today}</span>
  </div>
  <div class="stats">
    <div class="stat"><div class="num">{len(rows)}</div><div class="lab">物品种类</div></div>
    <div class="stat"><div class="num">{total_qty}</div><div class="lab">总件数</div></div>
    <div class="stat"><div class="num">¥{total_val:.0f}</div><div class="lab">总价值</div></div>
    <div class="stat"><div class="num">{sum(1 for r in rows if r.get('保质期至') and _is_expiring_soon(r['保质期至']))}</div><div class="lab">即将到期</div></div>
  </div>
</div>
<div class="card">
  <table>
    <thead>
      <tr>
        <th>名称</th><th>品牌</th><th>数量</th><th>单价</th><th>日均</th>
        <th>购入日期</th><th>保质期至</th><th>状态</th><th>标签</th><th>备注</th>
      </tr>
    </thead>
    <tbody>
      {''.join(_html_row(r) for r in rows)}
    </tbody>
  </table>
</div>
<div class="footer">物品架 · item-management · 自动生成</div>
</body>
</html>"""

def _is_expiring_soon(expiry_str: str) -> bool:
    if not expiry_str:
        return False
    try:
        delta = (date.fromisoformat(expiry_str) - date.today()).days
        return 0 <= delta <= 7
    except Exception:
        return False

def _is_expired(expiry_str: str) -> bool:
    if not expiry_str:
        return False
    try:
        return (date.fromisoformat(expiry_str) - date.today()).days < 0
    except Exception:
        return False

def _html_row(r: dict) -> str:
    exp = r.get("保质期至", "")
    expiry_cls = ""
    expiry_txt = exp
    if _is_expired(exp):
        expiry_cls = "expiry-warn"
        days = (date.today() - date.fromisoformat(exp)).days
        expiry_txt = f"⚠️ 已过期 {days} 天"
    elif _is_expiring_soon(exp):
        expiry_cls = "expiry-warn"
        days = (date.fromisoformat(exp) - date.today()).days
        expiry_txt = f"⏳ 还剩 {days} 天"
    status_cls = {"在用": "status-active", "已用完": "status-consumed", "已丢弃": "status-discarded"}.get(r.get("状态", ""), "")
    tags = "".join(f'<span class="tag">{t.strip()}</span>' for t in r.get("标签", "").split(",") if t.strip())
    return f"""<tr>
      <td><strong>{r['名称']}</strong></td>
      <td>{r['品牌'] or '—'}</td>
      <td>{r['数量']}{r['单位']}</td>
      <td>{'¥' + str(r['单价']) if r['单价'] else '—'}</td>
      <td>{'¥' + str(r['日均成本']) if r['日均成本'] else '—'}</td>
      <td>{r['购入日期'] or '—'}</td>
      <td class="{expiry_cls}">{expiry_txt}</td>
      <td><span class="status {status_cls}">{r.get('状态','—')}</span></td>
      <td>{tags or '—'}</td>
      <td>{r.get('备注','') or '—'}</td>
    </tr>"""

def cmd_report(args):
    """Generate a full HTML statistics report."""
    s = item_db.get_stats()
    items = item_db.list_items(sort_by="name")
    expiring = item_db.get_expiring_items(days=30)
    expired = item_db.get_expired_items()
    today_str = datetime.now().strftime("%Y-%m-%d")

    total_val = sum(it.get("price") or 0 for it in items)
    active_items = [it for it in items if it.get("status") == "active"]

    fname = args.out or f"物品报告_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>物品报告 {today_str}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
          background: #f0f2f5; color: #2c3e50; padding: 32px; }}
  h1 {{ font-size: 26px; font-weight: 800; color: #1a1a2e; margin-bottom: 6px; }}
  .subtitle {{ color: #888; font-size: 13px; margin-bottom: 28px; }}
  .grid-4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }}
  .card {{ background: #fff; border-radius: 16px; padding: 24px;
           box-shadow: 0 2px 12px rgba(0,0,0,.07); }}
  .big-num {{ font-size: 36px; font-weight: 800; color: #6c5ce7; line-height: 1; }}
  .big-num.yellow {{ color: #fdcb6e; }}
  .big-num.green {{ color: #00b894; }}
  .big-num.red {{ color: #e17055; }}
  .label {{ font-size: 13px; color: #888; margin-top: 6px; }}
  h2 {{ font-size: 16px; font-weight: 700; color: #2d3436; margin-bottom: 14px;
        padding-bottom: 8px; border-bottom: 2px solid #f0f2f5; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  th {{ background: #6c5ce7; color: #fff; padding: 10px 12px; text-align: left;
        font-weight: 600; }}
  td {{ padding: 10px 12px; border-bottom: 1px solid #f0f2f5; vertical-align: middle; }}
  tr:hover td {{ background: #f8f7ff; }}
  .tag {{ display: inline-block; background: #e8e4ff; color: #6c5ce7; border-radius: 20px;
          padding: 2px 8px; font-size: 11px; margin: 1px; }}
  .status {{ display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 12px; font-weight: 600; }}
  .status-active {{ background: #d4f5e9; color: #00b894; }}
  .status-consumed {{ background: #ffeaa7; color: #d63031; }}
  .status-discarded {{ background: #dfe6e9; color: #636e72; }}
  .expired {{ color: #e17055; font-weight: 600; }}
  .expiring {{ color: #e17055; }}
  .ok {{ color: #00b894; }}
  .section {{ margin-bottom: 24px; }}
  .row {{ display: flex; gap: 16px; }}
  .col {{ flex: 1; }}
  .badge {{ display: inline-block; background: #fff0f0; color: #e17055;
            border-radius: 20px; padding: 3px 10px; font-size: 12px; margin-left: 8px; }}
  .footer {{ text-align: center; color: #bbb; font-size: 12px; margin-top: 32px; }}
  @media print {{
    body {{ background: #fff; padding: 16px; }}
    .card {{ box-shadow: none; border: 1px solid #eee; }}
    @page {{ margin: 16mm; }}
  }}
</style>
</head>
<body>
<h1>📦 物品报告</h1>
<p class="subtitle">生成时间：{today_str}</p>

<div class="grid-4">
  <div class="card"><div class="big-num">{s['total_items']}</div><div class="label">物品种类</div></div>
  <div class="card"><div class="big-num">{s['total_quantity']}</div><div class="label">总件数</div></div>
  <div class="card"><div class="big-num yellow">¥{s['total_value']:.0f}</div><div class="label">总价值</div></div>
  <div class="card"><div class="big-num green">{s['total_brands']}</div><div class="label">涉及品牌</div></div>
</div>

<div class="row">
  <div class="col">
    <div class="card section">
      <h2>⚠️ 即将到期（30天内）{f'<span class="badge">{len(expiring)}件</span>' if expiring else ''}</h2>
      {"<table><tr><th>名称</th><th>保质期至</th><th>状态</th></tr>" + "".join(_report_exp_row(it) for it in expiring) + "</table>" if expiring else "<p style='color:#aaa;font-size:13px'>✅ 没有即将到期的物品</p>"}
    </div>
  </div>
  <div class="col">
    <div class="card section">
      <h2>❌ 已过期 {f'<span class="badge">{len(expired)}件</span>' if expired else ''}</h2>
      {"<table><tr><th>名称</th><th>保质期至</th><th>状态</th></tr>" + "".join(_report_exp_row(it) for it in expired) + "</table>" if expired else "<p style='color:#aaa;font-size:13px'>✅ 没有已过期的物品</p>"}
    </div>
  </div>
</div>

<div class="card section">
  <h2>📋 全部物品（{len(items)}件）</h2>
  {"<table><tr><th>名称</th><th>品牌</th><th>数量</th><th>单价</th><th>日均</th><th>购入日期</th><th>状态</th><th>标签</th></tr>" + "".join(_report_item_row(it) for it in items) + "</table>" if items else "<p style='color:#aaa;font-size:13px'>📦 暂无物品记录</p>"}
</div>

{"<div class='card section'><h2>📈 近月新增（价值趋势）</h2><table><tr><th>月份</th><th>新增件数</th><th>新增价值</th></tr>" + "".join(f"<tr><td>{m['month']}</td><td>{m['count']}件</td><td>¥{m['value'] or 0:.2f}</td></tr>" for m in s['monthly_new_items'][:6]) + "</table></div>" if s['monthly_new_items'] else ""}

<div class="footer">物品架 · item-management · 自动生成</div>
</body>
</html>"""

    os.makedirs(os.path.dirname(fname) or ".", exist_ok=True)
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 报告已生成：{fname}")
    print(f"   用浏览器打开后按 Ctrl+P 可打印为 PDF")

def _report_exp_row(it: dict) -> str:
    exp = it.get("expiry_date") or ""
    status = _status_display(it.get("status"))
    status_cls = {"在用": "status-active", "已用完": "status-consumed", "已丢弃": "status-discarded"}.get(status, "")
    try:
        delta = (date.fromisoformat(exp) - date.today()).days
        if delta < 0:
            exp_txt = f'<span class="expired">⚠️ 已过期 {abs(delta)} 天</span>'
        else:
            exp_txt = f'<span class="expiring">⏳ 还剩 {delta} 天</span>'
    except Exception:
        exp_txt = exp
    return f"<tr><td>{it['name']}</td><td>{exp_txt}</td><td><span class='status {status_cls}'>{status}</span></td></tr>"

def _report_item_row(it: dict) -> str:
    dp = _daily_price(it.get("price"), it.get("production_date"))
    status = _status_display(it.get("status"))
    status_cls = {"在用": "status-active", "已用完": "status-consumed", "已丢弃": "status-discarded"}.get(status, "")
    tags = "".join(f'<span class="tag">{t.strip()}</span>' for t in (it.get("tags") or []) if t.strip())
    return f"""<tr>
      <td><strong>{it['name']}</strong></td>
      <td>{it['brand'] or '—'}</td>
      <td>{it['quantity']}{it['unit']}</td>
      <td>{'¥' + str(it['price']) if it['price'] else '—'}</td>
      <td>{'¥' + f'{dp:.2f}' if dp is not None else '—'}</td>
      <td>{it['production_date'] or '—'}</td>
      <td><span class="status {status_cls}">{status}</span></td>
      <td>{tags or '—'}</td>
    </tr>"""

def cmd_backup(args):
    """Create a JSON backup of all data."""
    backup_path = item_db.auto_backup()
    size = os.path.getsize(backup_path)
    size_str = f"{size/1024:.1f}KB" if size > 1024 else f"{size}B"
    print(f"✅ 备份成功！")
    print(f"   路径: {backup_path}")
    print(f"   大小: {size_str}")
    print(f"\n💡 建议将此文件上传到云端（微云/网盘/邮箱）保存")

def cmd_restore(args):
    """Restore data from a JSON backup."""
    if args.file:
        backup_path = args.file
    else:
        backups = item_db.list_backups()
        if not backups:
            print("❌ 没有找到备份文件。请先用 `item backup` 创建备份。")
            return
        backup_path = backups[0]["path"]
        print(f"📋 使用最新备份: {backup_path}")
    
    if not os.path.exists(backup_path):
        print(f"❌ 找不到文件: {backup_path}")
        return
    
    try:
        with open(backup_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ 读取备份文件失败: {e}")
        return
    
    mode = "合并" if args.merge else "完整恢复"
    print(f"⚠️ 即将 {mode} 数据...")
    if not args.merge:
        print("   （完整恢复会清空现有数据）")
    
    stats = item_db.import_all_json(data, merge=args.merge)
    print(f"✅ 恢复完成！")
    print(f"   新增物品: {stats['added']} 件")
    print(f"   跳过（已存在）: {stats['skipped']} 件")
    if stats['errors']:
        print(f"   错误: {len(stats['errors'])} 条")
        for err in stats['errors'][:3]:
            print(f"     · {err}")

def cmd_info(args):
    """Show data storage information."""
    info = item_db.get_data_info()
    backups = item_db.list_backups()
    
    print(f"📂 数据存储信息\n")
    print(f"  数据库: {info['db_path']}")
    print(f"  状态: {'✅ 存在' if info['db_exists'] else '❌ 不存在'}")
    if info['db_size']:
        print(f"  大小: {info['db_size']/1024:.1f} KB")
    print(f"  备份目录: {info['backup_dir']}")
    print(f"  备份数量: {len(backups)} 个\n")
    
    if backups:
        print(f"  最近3个备份:")
        for b in backups[:3]:
            size = f"{b['size']/1024:.1f}KB" if b['size'] > 1024 else f"{b['size']}B"
            print(f"    · {b['name']}  ({b['mtime']}, {size})")
    else:
        print(f"  💡 还没有备份，用 `item backup` 创建第一个备份吧！")

# ──────────────────────────────────────────────
# Parser
# ──────────────────────────────────────────────

def _build_parser():
    parser = argparse.ArgumentParser(prog="item", description="物品管理")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("add", help="添加物品")
    p.add_argument("name")
    p.add_argument("--brand", default="")
    p.add_argument("--qty", type=int, default=1)
    p.add_argument("--unit", default="个")
    p.add_argument("--prod")
    p.add_argument("--expiry")
    p.add_argument("--warranty")
    p.add_argument("--opened")
    p.add_argument("--location", default="")
    p.add_argument("--notes", default="")
    p.add_argument("--price", type=float)
    p.add_argument("--tags")
    p.add_argument("--image")

    p = sub.add_parser("list", help="列出物品")
    p.add_argument("--sort", default="name", choices=["name","brand","expiry_date","created_at","quantity"])
    p.add_argument("--order", default="asc", choices=["asc","desc"])
    p.add_argument("--tag")

    p = sub.add_parser("get", help="查看物品详情")
    p.add_argument("id", type=int)

    p = sub.add_parser("update", help="更新物品")
    p.add_argument("id", type=int)
    p.add_argument("--name"); p.add_argument("--brand"); p.add_argument("--qty", type=int)
    p.add_argument("--price", type=float); p.add_argument("--prod"); p.add_argument("--expiry"); p.add_argument("--warranty")
    p.add_argument("--opened"); p.add_argument("--location"); p.add_argument("--notes")
    p.add_argument("--status"); p.add_argument("--tags")

    p = sub.add_parser("delete", help="删除物品")
    p.add_argument("id", type=int)

    p = sub.add_parser("sub-add", help="添加子物品")
    p.add_argument("parent_id", type=int); p.add_argument("name")
    p.add_argument("--qty", type=int, default=1); p.add_argument("--unit", default="个")
    p.add_argument("--prod"); p.add_argument("--expiry"); p.add_argument("--opened")
    p.add_argument("--notes", default="")

    p = sub.add_parser("sub-list", help="列出子物品")
    p.add_argument("parent_id", type=int)

    p = sub.add_parser("sub-update", help="更新子物品")
    p.add_argument("sub_id", type=int)
    p.add_argument("--name"); p.add_argument("--qty", type=int)
    p.add_argument("--status"); p.add_argument("--expiry"); p.add_argument("--notes")

    p = sub.add_parser("sub-delete", help="删除子物品")
    p.add_argument("sub_id", type=int)

    p = sub.add_parser("history", help="查看物品历史")
    p.add_argument("item_id", type=int)

    p = sub.add_parser("expiring", help="即将到期物品")
    p.add_argument("--days", type=int, default=7)

    sub.add_parser("expired", help="已过期物品")
    sub.add_parser("stats", help="数据统计")

    p = sub.add_parser("search", help="搜索物品")
    p.add_argument("query")
    p.add_argument("--field", choices=["name","brand","location","tags","notes"])

    p = sub.add_parser("export", help="导出物品")
    p.add_argument("--format", choices=["csv","json","html"])
    p.add_argument("--out")

    p = sub.add_parser("report", help="生成统计报告")
    p.add_argument("--out")

    p = sub.add_parser("backup", help="备份数据到JSON文件")
    p.add_argument("--path", help="指定备份文件保存路径（默认保存到数据目录）")

    p = sub.add_parser("restore", help="从JSON备份恢复数据")
    p.add_argument("file", nargs="?", help="备份文件路径（默认使用最新备份）")
    p.add_argument("--merge", action="store_true", help="合并模式：只添加不重复的物品")

    p = sub.add_parser("info", help="查看数据存储信息")

    return parser

if __name__ == "__main__":
    parser = _build_parser()
    args = parser.parse_args()
    if not args.cmd:
        parser.print_help()
        sys.exit(0)
    cmd_map = {
        "add": cmd_add, "list": cmd_list, "get": cmd_get, "update": cmd_update,
        "delete": cmd_delete, "sub-add": cmd_sub_add, "sub-list": cmd_sub_list,
        "sub-update": cmd_sub_update, "sub-delete": cmd_sub_delete,
        "history": cmd_history, "expiring": cmd_expiring, "expired": cmd_expired,
        "stats": cmd_stats, "search": cmd_search, "export": cmd_export, "report": cmd_report,
        "backup": cmd_backup, "restore": cmd_restore, "info": cmd_info,
    }
    cmd_map[args.cmd](args)

#!/usr/bin/env python3
"""
发票报销数据管理器 — 核心数据层
提供发票的增删改查、查重、导出功能
"""
import sqlite3
import os
import sys
import json
import csv
import argparse
from datetime import datetime, timedelta

# 数据库路径
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SKILL_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "invoices.db")

# 费用类别映射
CATEGORY_KEYWORDS = {
    "餐饮": ["餐饮", "食品", "外卖", "聚餐", "食堂", "饭店", "餐厅", "酒楼", "小吃", "快餐", "咖啡", "奶茶", "烘焙", "面包"],
    "交通": ["打车", "出租", "滴滴", "火车", "高铁", "机票", "航空", "加油", "停车", "公交", "地铁", "长途", "网约车", "T3", "曹操", "首汽"],
    "住宿": ["酒店", "宾馆", "旅馆", "民宿", "住宿", "客栈", "青年旅社"],
    "办公": ["文具", "打印", "耗材", "快递", "办公", "电脑", "纸张", "墨盒", "印章", "文件夹", "档案"],
    "通讯": ["话费", "网费", "宽带", "电信", "联通", "移动", "邮寄", "快递费"],
    "培训": ["培训", "课程", "学习", "考试", "认证", "教育", "书籍"],
    "差旅": ["差旅", "出差"],
    "医疗": ["医药", "医院", "诊所", "体检", "药品"],
    "租赁": ["租赁", "租金", "物业"],
    "维修": ["维修", "保养", "修理"],
}

CATEGORY_SELLER_KEYWORDS = {
    "餐饮": ["餐厅", "饭店", "酒楼", "小吃", "快餐", "咖啡", "奶茶", "烘焙", "面包", "食堂", "食品", "餐饮"],
    "交通": ["出租", "滴滴", "铁路", "航空", "机场", "加油站", "石化", "石油", "公交", "地铁", "高速"],
    "住宿": ["酒店", "宾馆", "旅馆", "民宿", "住宿"],
    "办公": ["文具", "办公", "京东", "天猫", "淘宝", "拼多多", "苏宁", "国美"],
    "通讯": ["电信", "联通", "移动", "邮局", "邮政", "中国邮政"],
}


def get_db():
    """获取数据库连接，自动创建表和目录"""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    _init_tables(conn)
    return conn


def _init_tables(conn):
    """初始化数据库表结构"""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_code TEXT DEFAULT '',
            invoice_number TEXT NOT NULL DEFAULT '',
            invoice_date TEXT DEFAULT '',
            invoice_type TEXT DEFAULT '其他',
            category TEXT DEFAULT '其他',
            amount REAL DEFAULT 0,
            tax_amount REAL DEFAULT 0,
            total_amount REAL DEFAULT 0,
            seller_name TEXT DEFAULT '',
            buyer_name TEXT DEFAULT '',
            items TEXT DEFAULT '[]',
            image_path TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            status TEXT DEFAULT 'pending',
            created_at TEXT DEFAULT (datetime('now','localtime')),
            updated_at TEXT DEFAULT (datetime('now','localtime'))
        );

        CREATE INDEX IF NOT EXISTS idx_invoice_number ON invoices(invoice_number);
        CREATE INDEX IF NOT EXISTS idx_invoice_date ON invoices(invoice_date);
        CREATE INDEX IF NOT EXISTS idx_category ON invoices(category);
        CREATE INDEX IF NOT EXISTS idx_status ON invoices(status);

        CREATE TABLE IF NOT EXISTS reimbursement_batches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            batch_name TEXT NOT NULL,
            invoice_ids TEXT NOT NULL DEFAULT '[]',
            total_amount REAL DEFAULT 0,
            status TEXT DEFAULT 'draft',
            created_at TEXT DEFAULT (datetime('now','localtime')),
            notes TEXT DEFAULT ''
        );
    """)


def suggest_category(seller_name="", items_str="", notes=""):
    """根据销售方名称和明细推测费用类别"""
    text = f"{seller_name} {items_str} {notes}".lower()
    
    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return category
    
    for category, keywords in CATEGORY_SELLER_KEYWORDS.items():
        for kw in keywords:
            if kw in seller_name:
                return category
    
    return "其他"


def add_invoice(data: dict) -> dict:
    """添加发票记录，自动查重和分类
    
    Args:
        data: {
            invoice_code, invoice_number, invoice_date, invoice_type,
            category, amount, tax_amount, total_amount,
            seller_name, buyer_name, items, image_path, notes
        }
    
    Returns:
        {"success": bool, "id": int, "duplicate": bool, "message": str}
    """
    conn = get_db()
    
    invoice_number = data.get("invoice_number", "").strip()
    invoice_code = data.get("invoice_code", "").strip()
    
    # 查重
    if invoice_number:
        existing = conn.execute(
            "SELECT id, invoice_date, seller_name, total_amount FROM invoices WHERE invoice_number=? AND invoice_code=?",
            (invoice_number, invoice_code)
        ).fetchone()
        
        if existing:
            conn.close()
            return {
                "success": False,
                "duplicate": True,
                "existing_id": existing["id"],
                "message": f"⚠️ 发票 {invoice_code}-{invoice_number} 已存在！\n"
                          f"  日期: {existing['invoice_date']}, "
                          f"销售方: {existing['seller_name']}, "
                          f"金额: ¥{existing['total_amount']:.2f}",
            }
    
    # 自动分类
    if not data.get("category") or data["category"] == "其他":
        data["category"] = suggest_category(
            data.get("seller_name", ""),
            data.get("items", ""),
            data.get("notes", "")
        )
    
    # 处理 items
    items = data.get("items", "[]")
    if isinstance(items, list):
        items = json.dumps(items, ensure_ascii=False)
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor = conn.execute("""
        INSERT INTO invoices 
        (invoice_code, invoice_number, invoice_date, invoice_type, category,
         amount, tax_amount, total_amount, seller_name, buyer_name,
         items, image_path, notes, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', ?, ?)
    """, (
        invoice_code,
        invoice_number,
        data.get("invoice_date", ""),
        data.get("invoice_type", "其他"),
        data.get("category", "其他"),
        data.get("amount", 0),
        data.get("tax_amount", 0),
        data.get("total_amount", data.get("amount", 0) + data.get("tax_amount", 0)),
        data.get("seller_name", ""),
        data.get("buyer_name", ""),
        items,
        data.get("image_path", ""),
        data.get("notes", ""),
        now, now,
    ))
    
    invoice_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {
        "success": True,
        "id": invoice_id,
        "duplicate": False,
        "category": data["category"],
        "message": f"✅ 发票 {invoice_number} 录入成功！ID: {invoice_id}, 类别: {data['category']}",
    }


def list_invoices(filters: dict = None) -> list:
    """查询发票列表
    
    Args:
        filters: {month, category, status, keyword, limit, offset}
    """
    conn = get_db()
    sql = "SELECT * FROM invoices WHERE 1=1"
    params = []
    
    if filters:
        if filters.get("month"):
            sql += " AND invoice_date LIKE ?"
            params.append(f"{filters['month']}%")
        if filters.get("category"):
            sql += " AND category=?"
            params.append(filters["category"])
        if filters.get("status"):
            sql += " AND status=?"
            params.append(filters["status"])
        if filters.get("keyword"):
            kw = f"%{filters['keyword']}%"
            sql += " AND (invoice_number LIKE ? OR seller_name LIKE ? OR notes LIKE ? OR items LIKE ?)"
            params.extend([kw, kw, kw, kw])
    
    sql += " ORDER BY invoice_date DESC, id DESC"
    
    if filters and filters.get("limit"):
        sql += " LIMIT ?"
        params.append(int(filters["limit"]))
        if filters.get("offset"):
            sql += " OFFSET ?"
            params.append(int(filters["offset"]))
    
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    
    return [dict(r) for r in rows]


def get_invoice(invoice_id: int) -> dict:
    """获取单条发票详情"""
    conn = get_db()
    row = conn.execute("SELECT * FROM invoices WHERE id=?", (invoice_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def update_invoice(invoice_id: int, data: dict) -> bool:
    """更新发票信息"""
    conn = get_db()
    fields = []
    params = []
    for key in ["category", "notes", "status", "invoice_type", "total_amount", 
                "amount", "tax_amount", "seller_name", "buyer_name", "invoice_date"]:
        if key in data:
            fields.append(f"{key}=?")
            params.append(data[key])
    
    if not fields:
        conn.close()
        return False
    
    fields.append("updated_at=?")
    params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    params.append(invoice_id)
    
    conn.execute(f"UPDATE invoices SET {', '.join(fields)} WHERE id=?", params)
    conn.commit()
    conn.close()
    return True


def delete_invoice(invoice_id: int) -> bool:
    """删除发票"""
    conn = get_db()
    conn.execute("DELETE FROM invoices WHERE id=?", (invoice_id,))
    conn.commit()
    affected = conn.total_changes
    conn.close()
    return affected > 0


def get_summary(month: str = None) -> dict:
    """获取汇总统计"""
    conn = get_db()
    
    if month:
        where = "WHERE invoice_date LIKE ?"
        param = (f"{month}%",)
    else:
        where = ""
        param = ()
    
    total = conn.execute(
        f"SELECT COUNT(*) as count, SUM(total_amount) as total FROM invoices {where}", param
    ).fetchone()
    
    by_category = conn.execute(
        f"SELECT category, COUNT(*) as count, SUM(total_amount) as total "
        f"FROM invoices {where} GROUP BY category ORDER BY total DESC", param
    ).fetchall()
    
    by_month = conn.execute(
        "SELECT substr(invoice_date,1,7) as month, COUNT(*) as count, "
        "SUM(total_amount) as total FROM invoices GROUP BY month ORDER BY month DESC LIMIT 12"
    ).fetchall()
    
    by_status = conn.execute(
        f"SELECT status, COUNT(*) as count FROM invoices {where} GROUP BY status", param
    ).fetchall()
    
    conn.close()
    
    return {
        "total_count": total["count"] if total else 0,
        "total_amount": total["total"] if total and total["total"] else 0,
        "by_category": [dict(r) for r in by_category],
        "by_month": [dict(r) for r in by_month],
        "by_status": [dict(r) for r in by_status],
    }


def export_csv(filepath: str, filters: dict = None) -> int:
    """导出CSV"""
    invoices = list_invoices(filters)
    
    fieldnames = [
        "id", "invoice_code", "invoice_number", "invoice_date", "invoice_type",
        "category", "amount", "tax_amount", "total_amount",
        "seller_name", "buyer_name", "items", "notes", "status", "created_at"
    ]
    
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for inv in invoices:
            row = dict(inv)
            # 清理 items 字段
            if row.get("items"):
                try:
                    items = json.loads(row["items"])
                    row["items"] = "、".join([i.get("name", "") for i in items])
                except:
                    pass
            writer.writerow(row)
    
    return len(invoices)


def search_invoices(query: str) -> list:
    """模糊搜索发票"""
    return list_invoices({"keyword": query, "limit": 50})


# CLI
def main():
    parser = argparse.ArgumentParser(description="发票报销数据管理器")
    subparsers = parser.add_subparsers(dest="command", help="操作命令")
    
    # add
    p_add = subparsers.add_parser("add", help="添加发票")
    p_add.add_argument("--code", default="", help="发票代码")
    p_add.add_argument("--number", required=True, help="发票号码")
    p_add.add_argument("--date", default="", help="开票日期 YYYY-MM-DD")
    p_add.add_argument("--type", default="其他", help="发票类型")
    p_add.add_argument("--category", default="", help="费用类别(留空自动识别)")
    p_add.add_argument("--amount", type=float, default=0, help="金额")
    p_add.add_argument("--tax", type=float, default=0, help="税额")
    p_add.add_argument("--total", type=float, default=0, help="价税合计")
    p_add.add_argument("--seller", default="", help="销售方名称")
    p_add.add_argument("--buyer", default="", help="购买方名称")
    p_add.add_argument("--items", default="[]", help="明细JSON")
    p_add.add_argument("--image", default="", help="发票图片路径")
    p_add.add_argument("--notes", default="", help="备注")
    p_add.add_argument("--force", action="store_true", help="强制录入(跳过查重)")
    
    # list
    p_list = subparsers.add_parser("list", help="查询发票")
    p_list.add_argument("--month", default="", help="月份 YYYY-MM")
    p_list.add_argument("--category", default="", help="费用类别")
    p_list.add_argument("--status", default="", help="状态")
    p_list.add_argument("--keyword", default="", help="关键字")
    p_list.add_argument("--limit", type=int, default=50, help="返回条数")
    
    # summary
    p_sum = subparsers.add_parser("summary", help="汇总统计")
    p_sum.add_argument("--month", default="", help="月份 YYYY-MM")
    
    # export
    p_exp = subparsers.add_parser("export", help="导出")
    p_exp.add_argument("--format", default="csv", help="导出格式")
    p_exp.add_argument("--output", default="invoices.csv", help="输出文件")
    p_exp.add_argument("--month", default="", help="月份筛选")
    p_exp.add_argument("--category", default="", help="类别筛选")
    
    # delete
    p_del = subparsers.add_parser("delete", help="删除发票")
    p_del.add_argument("--id", type=int, required=True, help="发票ID")
    
    # check
    p_chk = subparsers.add_parser("check", help="查重")
    p_chk.add_argument("--code", default="", help="发票代码")
    p_chk.add_argument("--number", required=True, help="发票号码")
    
    # search
    p_src = subparsers.add_parser("search", help="搜索")
    p_src.add_argument("query", help="搜索关键词")
    
    args = parser.parse_args()
    
    if args.command == "add":
        total = args.total or (args.amount + args.tax)
        data = {
            "invoice_code": args.code,
            "invoice_number": args.number,
            "invoice_date": args.date,
            "invoice_type": args.type,
            "category": args.category,
            "amount": args.amount,
            "tax_amount": args.tax,
            "total_amount": total,
            "seller_name": args.seller,
            "buyer_name": args.buyer,
            "items": args.items,
            "image_path": args.image,
            "notes": args.notes,
        }
        
        if args.force:
            conn = get_db()
            conn.execute("DELETE FROM invoices WHERE invoice_number=? AND invoice_code=?", 
                        (args.number, args.code))
            conn.commit()
            conn.close()
        
        result = add_invoice(data)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "list":
        filters = {}
        if args.month: filters["month"] = args.month
        if args.category: filters["category"] = args.category
        if args.status: filters["status"] = args.status
        if args.keyword: filters["keyword"] = args.keyword
        filters["limit"] = args.limit
        
        invoices = list_invoices(filters)
        print(f"共 {len(invoices)} 条记录:\n")
        for inv in invoices:
            print(f"  ID:{inv['id']:>4} | {inv['invoice_date']} | {inv['category']:4} | "
                  f"¥{inv['total_amount']:>10.2f} | {inv['seller_name'][:20]} | {inv['status']}")
        print(f"\n合计: ¥{sum(i['total_amount'] for i in invoices):.2f}")
    
    elif args.command == "summary":
        summary = get_summary(args.month)
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    
    elif args.command == "export":
        filters = {}
        if args.month: filters["month"] = args.month
        if args.category: filters["category"] = args.category
        count = export_csv(args.output, filters)
        print(f"✅ 已导出 {count} 条记录到 {args.output}")
    
    elif args.command == "delete":
        inv = get_invoice(args.id)
        if not inv:
            print(f"❌ 未找到ID={args.id}的发票")
            sys.exit(1)
        delete_invoice(args.id)
        print(f"✅ 已删除: {inv['invoice_number']} ({inv['seller_name']}, ¥{inv['total_amount']:.2f})")
    
    elif args.command == "check":
        conn = get_db()
        existing = conn.execute(
            "SELECT id, invoice_date, seller_name, total_amount FROM invoices WHERE invoice_number=? AND invoice_code=?",
            (args.number, args.code)
        ).fetchone()
        conn.close()
        if existing:
            print(f"⚠️ 重复: ID={existing['id']}, {existing['invoice_date']}, "
                  f"{existing['seller_name']}, ¥{existing['total_amount']:.2f}")
        else:
            print("✅ 未发现重复")
    
    elif args.command == "search":
        results = search_invoices(args.query)
        print(f"搜索 '{args.query}' 找到 {len(results)} 条:\n")
        for inv in results:
            print(f"  ID:{inv['id']:>4} | {inv['invoice_date']} | {inv['category']} | "
                  f"¥{inv['total_amount']:.2f} | {inv['seller_name'][:30]}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ops_db.py — 本体论智能体 · 本地数据层（数字孪生运营库）

把"资料库 4 核心表 + 扩展表"落地为本地 SQLite，作为数字公司（专家团）
对接真实系统前的**本地稳定数据层**。数据库默认落在：
    ~/.workbuddy/company-data/<slug>/ops.db
与 instance.yaml / company-memory.md 同目录（数字孪生持久层）。

设计原则：
  - 字段严格对齐《微数AI 数字公司平台 · 数据表 Schema》snake_case 约定；
  - 时间 TEXT 用 YYYY-MM-DD / YYYY-MM-DD HH:MM；金额 REAL 本期只填示例占位；
  - 提供专用 CRUD（核心4表）+ 通用 insert/select（扩展表）；
  - 真实资料库 API 对接通过 RemoteDatasource stub 端口预留，未配置时只打印提示、
    绝不发起真实网络请求，方便日后填入 WorkBuddy 资料库凭证即启用。
"""
import os
import re
import json
import sqlite3
import argparse
from datetime import datetime


# ── 路径推导 ────────────────────────────────────────────────────────
def slugify(text):
    s = re.sub(r"[^0-9a-zA-Z]+", "-", text or "").strip("-").lower()
    return s or "company"


def default_db_path(short_name=None):
    """默认库路径：~/.workbuddy/company-data/<slug>/ops.db；无简称则当前目录。"""
    slug = slugify(short_name) if short_name else ""
    base = os.path.join(os.path.expanduser("~"), ".workbuddy", "company-data", slug) if slug \
        else os.getcwd()
    return os.path.join(base, "ops.db")


# ── 表结构（对齐 Schema §2/§3）──────────────────────────────────────
CORE_TABLES = {
    "todos": """
        CREATE TABLE IF NOT EXISTS todos (
            id TEXT PRIMARY KEY,
            dept TEXT,
            title TEXT,
            priority TEXT,
            status TEXT,
            due_date TEXT,
            owner TEXT,
            source TEXT,
            related_project TEXT,
            note TEXT,
            created_at TEXT,
            completed_at TEXT
        )""",
    "departments": """
        CREATE TABLE IF NOT EXISTS departments (
            dept_code TEXT PRIMARY KEY,
            dept_name TEXT,
            lead_name TEXT,
            status TEXT,
            expert_team TEXT,
            agent_file TEXT,
            today_count INTEGER,
            note TEXT
        )""",
    "finance_tax": """
        CREATE TABLE IF NOT EXISTS finance_tax (
            id TEXT PRIMARY KEY,
            item TEXT,
            type TEXT,
            amount REAL,
            cycle TEXT,
            due_date TEXT,
            status TEXT,
            owner TEXT,
            note TEXT
        )""",
    "daily_report": """
        CREATE TABLE IF NOT EXISTS daily_report (
            date TEXT PRIMARY KEY,
            summary TEXT,
            completed TEXT,
            in_progress TEXT,
            overdue_alerts TEXT,
            dept_highlights TEXT,
            need_decide TEXT,
            generated_by TEXT
        )""",
}

EXT_TABLES = {
    "projects": """
        CREATE TABLE IF NOT EXISTS projects (
            id TEXT PRIMARY KEY, name TEXT, status TEXT, priority TEXT,
            owner_dept TEXT, start_date TEXT, target_date TEXT,
            milestone TEXT, note TEXT
        )""",
    "customers": """
        CREATE TABLE IF NOT EXISTS customers (
            id TEXT PRIMARY KEY, name TEXT, contact TEXT, source TEXT,
            stage TEXT, value REAL, owner TEXT, last_touch TEXT, note TEXT
        )""",
    "contracts": """
        CREATE TABLE IF NOT EXISTS contracts (
            id TEXT PRIMARY KEY, title TEXT, party TEXT, type TEXT,
            sign_date TEXT, expire_date TEXT, amount REAL,
            archive_path TEXT, status TEXT, note TEXT
        )""",
    "ip_assets": """
        CREATE TABLE IF NOT EXISTS ip_assets (
            id TEXT PRIMARY KEY, name TEXT, type TEXT, status TEXT,
            apply_date TEXT, grant_date TEXT, owner TEXT, note TEXT
        )""",
    "hr": """
        CREATE TABLE IF NOT EXISTS hr (
            id TEXT PRIMARY KEY, name TEXT, role TEXT, dept TEXT,
            onboard_date TEXT, status TEXT, note TEXT
        )""",
    "documents": """
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY, title TEXT, category TEXT, location TEXT,
            path TEXT, tags TEXT, updated_at TEXT, note TEXT
        )""",
    "decisions": """
        CREATE TABLE IF NOT EXISTS decisions (
            id TEXT PRIMARY KEY, topic TEXT, mode TEXT, date TEXT,
            participants TEXT, conclusion TEXT, need_decide TEXT, owner TEXT
        )""",
    "automations": """
        CREATE TABLE IF NOT EXISTS automations (
            id TEXT PRIMARY KEY, name TEXT, trigger TEXT, schedule TEXT,
            prompt TEXT, target_table TEXT, status TEXT, note TEXT
        )""",
    "policy_watch": """
        CREATE TABLE IF NOT EXISTS policy_watch (
            id TEXT PRIMARY KEY, topic TEXT, region TEXT, last_check TEXT,
            next_check TEXT, status TEXT, summary TEXT, note TEXT
        )""",
    "vendors": """
        CREATE TABLE IF NOT EXISTS vendors (
            id TEXT PRIMARY KEY, name TEXT, type TEXT, account TEXT,
            auth TEXT, expire_date TEXT, note TEXT
        )""",
    "content_calendar": """
        CREATE TABLE IF NOT EXISTS content_calendar (
            id TEXT PRIMARY KEY, title TEXT, channel TEXT, type TEXT,
            owner TEXT, plan_date TEXT, status TEXT, note TEXT
        )""",
    "revenue": """
        CREATE TABLE IF NOT EXISTS revenue (
            id TEXT PRIMARY KEY, date TEXT, type TEXT, category TEXT,
            amount REAL, related_project TEXT, note TEXT
        )""",
}

ALL_TABLES = {**CORE_TABLES, **EXT_TABLES}
# 通用方法允许写入的扩展表白名单
EXT_TABLE_NAMES = set(EXT_TABLES.keys())


class OpsDB:
    """本地运营库（SQLite）。与 instance.yaml 同目录，构成数字孪生持久层。"""

    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.init_schema()

    # ── 建表 ──
    def init_schema(self):
        cur = self.conn.cursor()
        for sql in ALL_TABLES.values():
            cur.execute(sql)
        self.conn.commit()

    def close(self):
        self.conn.close()

    # ── todos ──
    def add_todo(self, dept, title, priority, status="todo", due_date="",
                 owner="", source="手动", related_project="", note="",
                 created_at=None, todo_id=None):
        created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")
        if not todo_id:
            n = self.conn.execute("SELECT COUNT(*) c FROM todos").fetchone()["c"] + 1
            todo_id = f"T{n:04d}"
        self.conn.execute(
            "INSERT OR REPLACE INTO todos "
            "(id,dept,title,priority,status,due_date,owner,source,related_project,note,created_at,completed_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (todo_id, dept, title, priority, status, due_date, owner, source,
             related_project, note, created_at, ""))
        self.conn.commit()
        return todo_id

    def list_todos(self, status=None, dept=None):
        sql = "SELECT * FROM todos"
        conds, args = [], []
        if status:
            conds.append("status=?"), args.append(status)
        if dept:
            conds.append("dept=?"), args.append(dept)
        if conds:
            sql += " WHERE " + " AND ".join(conds)
        sql += " ORDER BY due_date, priority"
        return [dict(r) for r in self.conn.execute(sql, args).fetchall()]

    def update_todo_status(self, todo_id, status, completed_at=None):
        if status == "done" and not completed_at:
            completed_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.conn.execute(
            "UPDATE todos SET status=?, completed_at=? WHERE id=?",
            (status, completed_at or "", todo_id))
        self.conn.commit()

    def get_overdue(self):
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM todos WHERE status='overdue' ORDER BY due_date").fetchall()]

    # ── departments ──
    def upsert_department(self, dept_code, dept_name, lead_name, status="active",
                         expert_team="", agent_file="", today_count=0, note=""):
        self.conn.execute(
            "INSERT OR REPLACE INTO departments "
            "(dept_code,dept_name,lead_name,status,expert_team,agent_file,today_count,note) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (dept_code, dept_name, lead_name, status, expert_team, agent_file,
             today_count, note))
        self.conn.commit()

    def list_departments(self):
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM departments ORDER BY dept_code").fetchall()]

    # ── finance_tax ──
    def add_finance_item(self, item, ftype, cycle, due_date, status,
                        amount=0.0, owner="", note="", fin_id=None):
        if not fin_id:
            n = self.conn.execute("SELECT COUNT(*) c FROM finance_tax").fetchone()["c"] + 1
            fin_id = f"FT{n:03d}"
        self.conn.execute(
            "INSERT OR REPLACE INTO finance_tax "
            "(id,item,type,amount,cycle,due_date,status,owner,note) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (fin_id, item, ftype, amount, cycle, due_date, status, owner, note))
        self.conn.commit()
        return fin_id

    def list_finance(self, status=None):
        sql = "SELECT * FROM finance_tax"
        args = []
        if status:
            sql += " WHERE status=?", args.append(status)
        return [dict(r) for r in self.conn.execute(sql, args).fetchall()]

    def update_finance_status(self, fin_id, status):
        self.conn.execute("UPDATE finance_tax SET status=? WHERE id=?", (status, fin_id))
        self.conn.commit()

    # ── daily_report ──
    def save_daily_report(self, date, summary, completed="", in_progress="",
                         overdue_alerts="", dept_highlights=None,
                         need_decide="", generated_by="团长(自动化)"):
        dh = json.dumps(dept_highlights or {}, ensure_ascii=False)
        self.conn.execute(
            "INSERT OR REPLACE INTO daily_report "
            "(date,summary,completed,in_progress,overdue_alerts,dept_highlights,need_decide,generated_by) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (date, summary, completed, in_progress, overdue_alerts, dh,
             need_decide, generated_by))
        self.conn.commit()

    def get_daily_report(self, date):
        r = self.conn.execute("SELECT * FROM daily_report WHERE date=?", (date,)).fetchone()
        return dict(r) if r else None

    # ── 通用扩展表 ──
    def insert_row(self, table, **kwargs):
        if table not in EXT_TABLE_NAMES:
            raise ValueError(f"未知扩展表: {table}（仅允许 {sorted(EXT_TABLE_NAMES)}）")
        cols = list(kwargs.keys())
        ph = ",".join("?" for _ in cols)
        self.conn.execute(
            f"INSERT OR REPLACE INTO {table} ({','.join(cols)}) VALUES ({ph})",
            list(kwargs.values()))
        self.conn.commit()

    def select(self, table, **where):
        if table not in EXT_TABLE_NAMES:
            raise ValueError(f"未知扩展表: {table}")
        sql = f"SELECT * FROM {table}"
        args = []
        if where:
            sql += " WHERE " + " AND ".join(f"{k}=?" for k in where)
            args = list(where.values())
        return [dict(r) for r in self.conn.execute(sql, args).fetchall()]


class RemoteDatasource:
    """资料库在线主库对接端口（占位 stub）。

    配置：把下方 CREDENTIALS 的占位值替换为真实 WorkBuddy 资料库空间信息；
    未配置（含"填入"字样）时，所有 push/pull 仅打印提示、不发起网络请求。
    配置完成后，在 TODO 处接入真实资料库读写 API 即可启用双写。
    """

    CREDENTIALS = {
        "space_id": "填入资料库空间标识(如 workspace_weishu_company)",
        "api_token": "填入资料库 API token",
        "endpoint": "填入资料库 API 端点",
    }

    def __init__(self):
        self.configured = all(
            v and not str(v).startswith("填入") for v in self.CREDENTIALS.values()
        )

    def push(self, table, rows):
        if not self.configured:
            print(f"[stub] 未配置资料库 API，跳过 push({table})；"
                  f"请填入 RemoteDatasource.CREDENTIALS")
            return None
        # TODO: 接入真实资料库写入 API（按 WorkBuddy 资料库接口批量写入 rows）
        raise NotImplementedError("资料库 API 对接待实现：push 到在线主库")

    def pull(self, table):
        if not self.configured:
            print(f"[stub] 未配置资料库 API，跳过 pull({table})")
            return None
        # TODO: 接入真实资料库读取 API（按表拉取在线数据回写本地）
        raise NotImplementedError("资料库 API 对接待实现：pull 自在线主库")


# ── 示例数据（对齐 Schema §2 示例）─────────────────────────────────
def _demo_data(db):
    # todos
    db.add_todo("finance", "完成 8 月增值税申报", "P1", "overdue",
                due_date="2026-08-10", owner="费清算", source="派活")
    db.add_todo("rnd", "记忆笔精灵 V1.2 联调", "P1", "doing",
                due_date="2026-08-15", owner="柯工成", source="派活",
                related_project="记忆笔精灵")
    db.add_todo("market", "公众号周更草稿", "P2", "todo",
                due_date="2026-08-14", owner="温辞章", source="自动化")
    db.add_todo("legal", "软著实名认证跟进", "P2", "todo",
                due_date="2026-08-20", owner="范守规", source="手动")
    # departments（示例 4 个，完整 12 个由 instance 同步）
    for code, name, lead, team in [
        ("finance", "财务部", "费清算", "财税合规团"),
        ("rnd", "研发部", "柯工成", "研发提效团"),
        ("market", "市场图文部", "温辞章", "内容创作团"),
        ("legal", "法务部", "范守规", "法务合规团"),
    ]:
        db.upsert_department(code, name, lead, expert_team=team)
    # finance_tax
    db.add_finance_item("增值税及附加申报", "tax", "month", "2026-08-15",
                       "pending", amount=0.0, owner="费清算", note="一般纳税人月度")
    db.add_finance_item("个税代缴", "tax", "month", "2026-08-15", "pending")
    db.add_finance_item("社保费", "fee", "month", "2026-08-25", "upcoming")
    db.add_finance_item("企业所得税季报", "tax", "quarter", "2026-10-15", "upcoming")
    db.add_finance_item("年度预算", "budget", "year", "2026-12-31", "upcoming")
    # daily_report
    db.save_daily_report(
        "2026-08-12", "研发联调推进，财务申报临近",
        completed="- 记忆笔精灵联调\n- 周更草稿",
        in_progress="增值税申报准备",
        overdue_alerts="T0001 增值税申报逾期",
        dept_highlights={"rnd": "V1.2 联调 80%"},
        need_decide="记忆笔精灵是否做付费版")
    return db


def main():
    ap = argparse.ArgumentParser(description="本体论智能体本地数据层")
    ap.add_argument("--company", help="公司简称 slug（决定 company-data/<slug>/ops.db）")
    ap.add_argument("--db", help="显式指定数据库路径（优先于 --company）")
    ap.add_argument("--init", action="store_true", help="仅建表初始化")
    ap.add_argument("--demo", action="store_true", help="填充示例数据")
    ap.add_argument("--query", help="查询表名：todos/departments/finance_tax/daily_report")
    args = ap.parse_args()

    db_path = args.db or default_db_path(args.company)
    db = OpsDB(db_path)
    print(f"[ops_db] 数据库：{db_path}")

    if args.init:
        print("[ops_db] 已初始化表结构（核心4表 + 扩展表）。")
    if args.demo:
        _demo_data(db)
        print("[ops_db] 已写入示例数据（对齐 Schema §2）。")
    if args.query:
        name = args.query
        mapper = {
            "todos": db.list_todos,
            "departments": db.list_departments,
            "finance_tax": db.list_finance,
        }
        if name in mapper:
            rows = mapper[name]()
        elif name == "daily_report":
            rows = [dict(r) for r in db.conn.execute(
                "SELECT * FROM daily_report ORDER BY date DESC")]
        else:
            rows = db.select(name)
        for r in rows:
            print(r)
    db.close()


if __name__ == "__main__":
    main()

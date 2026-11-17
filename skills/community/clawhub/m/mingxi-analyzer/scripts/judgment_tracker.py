#!/usr/bin/env python3
"""
judgment_tracker.py — 判断回查工具（持久战层）v2

用于记录和回查判断性结论。v2 改为 SQLite 存储，替换 v1 的 NDJSON 逐日文件。
自动迁移已有 NDJSON 数据。

用法：
  python3 judgment_tracker.py record <topic> <judgment> <confidence> <fail_condition> [check_date]
  python3 judgment_tracker.py review              # 检查所有到期未回查条目
  python3 judgment_tracker.py list [--all]        # 列出活跃记录
  python3 judgment_tracker.py stats               # 统计概览
  python3 judgment_tracker.py check <id> <result> # 回查确认：站住(stable) / 推翻(fail) / 待定(hold)
"""

import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta, timezone


# Register sqlite3 datetime adapter for Python 3.12+
def _adapt_datetime(dt):
    return dt.isoformat()

def _convert_datetime(s):
    try:
        return datetime.fromisoformat(s.decode() if isinstance(s, bytes) else s)
    except (ValueError, AttributeError):
        from datetime import datetime as dt
        return dt.now()

sqlite3.register_adapter(datetime, _adapt_datetime)
sqlite3.register_converter("timestamp", _convert_datetime)

DB_PATH = os.path.expanduser("~/.openclaw/judgment_tracker.db")
TZ = timezone(timedelta(hours=8))


def _get_conn():
    """获取 SQLite 连接（自动建表）"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS judgment_tracker (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assertion TEXT NOT NULL,
            domain TEXT NOT NULL DEFAULT '',
            confidence TEXT NOT NULL DEFAULT 'T3',
            fail_condition TEXT NOT NULL DEFAULT '',
            verifications_passed INTEGER NOT NULL DEFAULT 0,
            verifications_failed INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMP NOT NULL,
            last_check_at TIMESTAMP,
            next_check_at TIMESTAMP,
            status TEXT NOT NULL DEFAULT 'active',
            review_result TEXT
        )
    """)
    conn.commit()
    return conn


def _migrate_from_ndjson():
    """将 v1 的 NDJSON 文件数据迁移到 SQLite"""
    tracker_dir = "/tmp/judgment_tracker"
    if not os.path.isdir(tracker_dir):
        return

    conn = _get_conn()
    existing = conn.execute("SELECT COUNT(*) FROM judgment_tracker").fetchone()[0]
    if existing > 0:
        return  # 已有数据，不重复迁移

    migrated = 0
    for fname in sorted(os.listdir(tracker_dir)):
        if not fname.endswith(".ndjson"):
            continue
        fpath = os.path.join(tracker_dir, fname)
        with open(fpath, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue

                assertion = rec.get("judgment", "")
                domain = rec.get("topic", "")
                confidence = rec.get("confidence", "T3")
                fail_condition = rec.get("fail_condition", "")
                created_raw = rec.get("created_at", "")
                created_at = _parse_time(created_raw)
                check_date_str = rec.get("check_date", "")
                next_check_at = _parse_time(check_date_str) if check_date_str else (datetime.now(TZ) + timedelta(days=7))
                reviewed = rec.get("reviewed", False)
                status = "supervision" if rec.get("review_result") == "stable" else ("archived" if reviewed else "active")

                conn.execute("""
                    INSERT INTO judgment_tracker
                        (assertion, domain, confidence, fail_condition,
                         created_at, next_check_at, status, verifications_passed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (assertion, domain, confidence, fail_condition,
                      created_at, next_check_at, status, 1 if reviewed else 0))
                migrated += 1

    if migrated > 0:
        conn.commit()
        print(f"🔄 已从 NDJSON 迁移 {migrated} 条记录到 SQLite ({DB_PATH})")
    conn.close()


def _parse_time(time_str):
    """解析时间字符串为 datetime，支持 '2026-06-11' 和 '2026-06-11 14:30:00' 格式"""
    if not time_str:
        return datetime.now(TZ)
    try:
        return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=TZ)
    except ValueError:
        pass
    try:
        return datetime.strptime(time_str, "%Y-%m-%d").replace(tzinfo=TZ)
    except ValueError:
        return datetime.now(TZ)


def cmd_record(argv):
    """记录一条判断"""
    if len(argv) < 4:
        print("用法: judgment_tracker.py record <topic> <judgment> <confidence> <fail_condition> [check_date]")
        print("  confidence: T1/T2/T3/T4")
        print("  check_date: YYYY-MM-DD (默认7天后)")
        sys.exit(1)

    domain = argv[0]
    assertion = argv[1]
    confidence = argv[2].upper()
    fail_condition = argv[3]
    now = datetime.now(TZ)

    if confidence not in ("T1", "T2", "T3", "T4"):
        print(f"❌ 无效信度: {confidence}，应为 T1/T2/T3/T4")
        sys.exit(1)

    if len(argv) > 4:
        next_check = _parse_time(argv[4])
    else:
        next_check = now + timedelta(days=7)

    conn = _get_conn()
    conn.execute("""
        INSERT INTO judgment_tracker
            (assertion, domain, confidence, fail_condition, created_at, next_check_at, status)
        VALUES (?, ?, ?, ?, ?, ?, 'active')
    """, (assertion, domain, confidence, fail_condition, now, next_check))
    conn.commit()
    conn.close()

    print(f"✅ 已记录: [{confidence}] {domain} | 回查: {next_check.strftime('%Y-%m-%d')}")


def cmd_review(argv):
    """检查所有到期未回查条目"""
    now = datetime.now(TZ)
    conn = _get_conn()
    rows = conn.execute("""
        SELECT * FROM judgment_tracker
        WHERE next_check_at <= ? AND status = 'active'
        ORDER BY next_check_at ASC
    """, (now,)).fetchall()
    conn.close()

    if not rows:
        print(f"✅ 截至 {now.strftime('%Y-%m-%d %H:%M')}，无到期待回查条目")
        return

    print(f"🔍 截至 {now.strftime('%Y-%m-%d %H:%M')}，共 {len(rows)} 条到期待回查：")
    print()
    for r in rows:
        print(f"  [{r['confidence']}] {r['domain']} (id={r['id']})")
        print(f"    判断: {r['assertion'][:80]}")
        print(f"    失效条件: {r['fail_condition']}")
        print(f"    创建: {r['created_at']} | 到期: {r['next_check_at']}")
        print(f"    已通过检验: {r['verifications_passed']}次 | 已失败: {r['verifications_failed']}次")
        print(f"    查看详情: python3 judgment_tracker.py check {r['id']} <stable|fail|hold>")
        print()


def cmd_list(argv):
    """列出记录"""
    show_all = "--all" in argv
    conn = _get_conn()

    if show_all:
        rows = conn.execute("SELECT * FROM judgment_tracker ORDER BY created_at DESC").fetchall()
        label = "所有"
    else:
        rows = conn.execute("""
            SELECT * FROM judgment_tracker WHERE status = 'active'
            ORDER BY next_check_at ASC
        """).fetchall()
        label = "活跃"
    conn.close()

    if not rows:
        print(f"(空)")
        return

    print(f"📋 {label}记录 ({len(rows)} 条)：")
    print()
    for r in rows:
        status_map = {'active': '⏳', 'archived': '✅', 'supervision': '🔬'}
        icon = status_map.get(r['status'], '❓')
        check_str = str(r['next_check_at'])[:10] if r['next_check_at'] else '?'
        print(f"  {icon} [{r['confidence']}] {r['domain']} (id={r['id']}) | 回查: {check_str}")
        print(f"    判断: {r['assertion'][:80]}")


def cmd_stats(argv):
    """统计概览"""
    conn = _get_conn()

    total = conn.execute("SELECT COUNT(*) FROM judgment_tracker").fetchone()[0]
    active = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE status='active'").fetchone()[0]
    archived = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE status='archived'").fetchone()[0]
    supervision = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE status='supervision'").fetchone()[0]

    now = datetime.now(TZ)
    due = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE next_check_at <= ? AND status='active'", (now,)).fetchone()[0]

    by_confidence = conn.execute(
        "SELECT confidence, COUNT(*) FROM judgment_tracker GROUP BY confidence ORDER BY confidence"
    ).fetchall()

    conn.close()

    print(f"📊 判断回查统计")
    print(f"  总记录: {total}")
    print(f"  活跃: {active}")
    print(f"  已归档: {archived}")
    print(f"  长期监督: {supervision}")
    print(f"  到期未回查: {due}")
    if by_confidence:
        by_str = ", ".join(f"{r['confidence']}={r['COUNT(*)']}" for r in by_confidence)
        print(f"  按信度: {by_str}")


def cmd_check(argv):
    """回查确认单条判断"""
    if len(argv) < 2:
        print("用法: judgment_tracker.py check <id> <stable|fail|hold>")
        print("  stable = 站住了，提信度一级")
        print("  fail   = 被推翻，移入T4")
        print("  hold   = 不确定，保持原信度")
        sys.exit(1)

    try:
        record_id = int(argv[0])
    except ValueError:
        print(f"❌ id 必须为数字")
        sys.exit(1)

    result = argv[1].lower()
    if result not in ("stable", "fail", "hold"):
        print("❌ result 必须为 stable / fail / hold")
        sys.exit(1)

    conn = _get_conn()
    row = conn.execute("SELECT * FROM judgment_tracker WHERE id=?", (record_id,)).fetchone()
    if not row:
        print(f"❌ 未找到 id={record_id}")
        conn.close()
        return

    now = datetime.now(TZ)
    today_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # 信度等级顺序: T1 > T2 > T3 > T4
    levels = ["T1", "T2", "T3", "T4"]
    current_idx = levels.index(row["confidence"]) if row["confidence"] in levels else 2

    if result == "stable":
        new_confidence_rank = max(0, current_idx - 1)  # 提一级（数字变小=信度变高）
        new_confidence = levels[new_confidence_rank]
        new_passed = row["verifications_passed"] + 1

        # 连续通过: verifications_passed >= 3 → 转入长期监督（季度回查）
        if new_passed >= 3:
            next_check = now + timedelta(days=90)
            new_status = "supervision"
            action = "转入长期监督（季度回查）"
        else:
            next_check = now + timedelta(days=7)
            new_status = "active"
            action = "站住，提信度"

        conn.execute("""
            UPDATE judgment_tracker
            SET confidence=?, verifications_passed=?, last_check_at=?,
                next_check_at=?, status=?, review_result='stable'
            WHERE id=?
        """, (new_confidence, new_passed, today_str, next_check, new_status, record_id))
        print(f"✅ [{row['domain']}] {action}: {row['confidence']}→{new_confidence} | 下次回查: {next_check.strftime('%Y-%m-%d')}")

    elif result == "fail":
        # 被推翻 → 移入T4（存档），记录失败次数
        new_failed = row["verifications_failed"] + 1
        conn.execute("""
            UPDATE judgment_tracker
            SET confidence='T4', verifications_failed=?, last_check_at=?,
                status='archived', review_result='fail'
            WHERE id=?
        """, (new_failed, today_str, record_id))
        print(f"❌ [{row['domain']}] 被推翻，移入T4（存档）")

    else:  # hold
        # 不确定 → 保持原信度，延长7天
        next_check = now + timedelta(days=7)
        conn.execute("""
            UPDATE judgment_tracker
            SET last_check_at=?, next_check_at=?, review_result='hold'
            WHERE id=?
        """, (today_str, next_check, record_id))
        print(f"🟡 [{row['domain']}] 不确定，保持 {row['confidence']} | 延长至 {next_check.strftime('%Y-%m-%d')}")

    conn.commit()
    conn.close()
# ═══════════════════════════════════════════
# Dashboard / 量化仪表盘（持久战量化指标）
# ═══════════════════════════════════════════

def _ensure_snapshot_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dashboard_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_at TIMESTAMP NOT NULL,
            total INTEGER NOT NULL,
            active INTEGER NOT NULL,
            archived INTEGER NOT NULL,
            supervision INTEGER NOT NULL,
            stable_checks INTEGER NOT NULL DEFAULT 0,
            fail_checks INTEGER NOT NULL DEFAULT 0,
            hold_checks INTEGER NOT NULL DEFAULT 0,
            overdue INTEGER NOT NULL DEFAULT 0,
            completion_rate REAL NOT NULL DEFAULT 0.0,
            by_confidence TEXT DEFAULT '{}',
            by_domain TEXT DEFAULT '{}'
        )
    """)
    conn.commit()


def cmd_snapshot(argv):
    """存储当前快照（每日复盘自动调用）"""
    conn = _get_conn()
    _ensure_snapshot_table(conn)

    now = datetime.now(TZ)
    total = conn.execute('SELECT COUNT(*) FROM judgment_tracker').fetchone()[0]
    active = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE status='active'").fetchone()[0]
    archived = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE status='archived'").fetchone()[0]
    supervision = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE status='supervision'").fetchone()[0]

    stable_checks = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE review_result='stable'").fetchone()[0]
    fail_checks = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE review_result='fail'").fetchone()[0]
    hold_checks = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE review_result='hold'").fetchone()[0]

    total_checks = stable_checks + fail_checks + hold_checks
    completion_rate = round(stable_checks / total_checks, 4) if total_checks > 0 else 0.0

    overdue = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE next_check_at <= ? AND status='active'", (now,)).fetchone()[0]

    by_conf = {}
    for r in conn.execute('SELECT confidence, COUNT(*) FROM judgment_tracker GROUP BY confidence'):
        by_conf[r[0]] = r[1]

    by_domain = {}
    for r in conn.execute('SELECT domain, COUNT(*) FROM judgment_tracker GROUP BY domain ORDER BY COUNT(*) DESC LIMIT 10'):
        by_domain[r[0]] = r[1]

    import json
    conn.execute("""
        INSERT INTO dashboard_snapshots
            (snapshot_at, total, active, archived, supervision,
             stable_checks, fail_checks, hold_checks, overdue, completion_rate,
             by_confidence, by_domain)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (now, total, active, archived, supervision,
          stable_checks, fail_checks, hold_checks, overdue, completion_rate,
          json.dumps(by_conf, ensure_ascii=False),
          json.dumps(by_domain, ensure_ascii=False)))
    conn.commit()
    conn.close()
    print(f"✅ 快照已保存: {now.strftime('%Y-%m-%d %H:%M')}")


def cmd_dashboard(argv):
    """输出完整仪表盘"""
    conn = _get_conn()
    _ensure_snapshot_table(conn)
    now = datetime.now(TZ)

    total = conn.execute('SELECT COUNT(*) FROM judgment_tracker').fetchone()[0]
    active = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE status='active'").fetchone()[0]
    archived = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE status='archived'").fetchone()[0]
    supervision = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE status='supervision'").fetchone()[0]

    stable_checks = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE review_result='stable'").fetchone()[0]
    fail_checks = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE review_result='fail'").fetchone()[0]
    hold_checks = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE review_result='hold'").fetchone()[0]
    total_checks = stable_checks + fail_checks + hold_checks
    completion_rate = round(stable_checks / total_checks * 100, 1) if total_checks > 0 else 0.0
    fail_rate = round(fail_checks / total_checks * 100, 1) if total_checks > 0 else 0.0

    overdue = conn.execute("SELECT COUNT(*) FROM judgment_tracker WHERE next_check_at <= ? AND status='active'", (now,)).fetchone()[0]

    due_rows = conn.execute("""
        SELECT id, domain, assertion, next_check_at FROM judgment_tracker
        WHERE next_check_at <= ? AND status='active'
        ORDER BY next_check_at ASC LIMIT 3
    """, (now,)).fetchall()

    snapshots = conn.execute("""
        SELECT snapshot_at, active, supervision, overdue, completion_rate
        FROM dashboard_snapshots ORDER BY id DESC LIMIT 7
    """).fetchall()

    by_domain = conn.execute("""
        SELECT domain, COUNT(*) FROM judgment_tracker
        GROUP BY domain ORDER BY COUNT(*) DESC LIMIT 8
    """).fetchall()
    conn.close()

    print('=' * 56)
    print('  📊 判断回查 · 持久战仪表盘')
    print(f'  {now.strftime("%Y-%m-%d %H:%M")} UTC+8')
    print('=' * 56)
    print()
    print(f'  📈 **总量**: {total} 条 | 活跃: {active} | 已归档: {archived} | 长期监督: {supervision}')
    print()

    if total_checks > 0:
        print(f'  ✅ **判断准确率** (stable/total): {completion_rate}% ({stable_checks}/{total_checks})')
        print(f'  ❌ **推翻率**: {fail_rate}% ({fail_checks}次)')
        print(f'  🟡 **待定**: {hold_checks}次')
        print(f'  📋 **回查完成率**: {round(total_checks / (total_checks + overdue) * 100, 1) if (total_checks + overdue) > 0 else 0}%')
    else:
        print(f'  ✅ **判断准确率**: 暂无回查记录（数据积累中）')
    print()

    print(f'  ⏰ **到期未回查**: {overdue} 条')
    if overdue > 0 and due_rows:
        for r in due_rows:
            nd = r["next_check_at"]
            nd_str = str(nd)[:10]
            if isinstance(nd, str):
                try:
                    nd_dt = datetime.fromisoformat(nd.replace("+08:00", "").replace("+00:00", ""))
                except:
                    nd_dt = now
            else:
                nd_dt = nd
            overdue_days = (now - nd_dt).days
            print(f'    🔴 id={r["id"]} [{r["domain"]}] 逾期 {overdue_days} 天 | "{str(r["assertion"])[:40]}"')
    print()

    if by_domain:
        print(f'  📂 **领域分布** (TOP 8):')
        for d, c in by_domain:
            bar = "█" * min(c, 30)
            print(f'    {bar} {d} ({c})')
        print()

    if snapshots:
        print(f'  📉 **趋势** (最近 {len(snapshots)} 次快照):')
        print(f'    {"日期":>10}  {"活跃":>4}  {"监督":>4}  {"逾期":>4}  {"准确率":>6}')
        for s in reversed(snapshots):
            dt_str = str(s[0])[:10]
            a, sp, d, r = s[1], s[2], s[3], s[4]
            if isinstance(r, float) and r < 1:
                r_str = f"{r*100:.1f}%"
            else:
                r_str = f"{r:.1f}%"
            print(f'    {dt_str}  {a:>4}  {sp:>4}  {d:>4}  {r_str:>6}')
        print()
    print('=' * 56)


def main():
    _migrate_from_ndjson()

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "record": cmd_record,
        "review": cmd_review,
        "list": cmd_list,
        "stats": cmd_stats,
        "check": cmd_check,
        "snapshot": cmd_snapshot,
        "dashboard": cmd_dashboard,
    }

    if cmd not in commands:
        print(f"❌ 未知命令: {cmd}")
        print("可用: record, review, list, stats, check, snapshot, dashboard")
        sys.exit(1)

    commands[cmd](args)


if __name__ == "__main__":
    main()

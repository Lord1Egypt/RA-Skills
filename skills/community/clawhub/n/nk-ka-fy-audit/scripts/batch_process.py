#!/usr/bin/env python3
"""批量处理所有月份 - 每次调用子进程处理一个月"""
import subprocess, os, sys, time, gc

DATA_DIR = '/workspace/data'
SCRIPT = '/workspace/scripts/parse_one_month.py'
DB_PATH = '/workspace/data/ka_commission_audit.db'

all_months = sorted([d for d in os.listdir(DATA_DIR) if d.isdigit() and len(d) == 6])
print(f"将处理 {len(all_months)} 个月份: {all_months[0]} ~ {all_months[-1]}")

success = 0
failed = []

for i, month in enumerate(all_months):
    print(f"\n[{i+1}/{len(all_months)}] {month}...", end=' ', flush=True)
    t0 = time.time()
    
    result = subprocess.run(
        ['python3', SCRIPT, month],
        capture_output=True, text=True, timeout=300
    )
    
    elapsed = time.time() - t0
    
    if result.returncode == 0:
        lines = [l for l in result.stdout.strip().split('\n') if l]
        for l in lines:
            if 'DONE' not in l:
                print(l)
        print(f'✅ {elapsed:.0f}s')
        success += 1
    else:
        print(f'❌ {elapsed:.0f}s')
        print(f'  stderr: {result.stderr[:200]}')
        failed.append(month)
    
    # Small delay to let memory settle
    time.sleep(1)

print(f"\n\n===== 处理完成 =====")
print(f"成功: {success}/{len(all_months)}")
if failed:
    print(f"失败: {failed}")

# 更新monthly_audit
print("\n更新月度汇总表...")
import sqlite3
conn = sqlite3.connect(DB_PATH, timeout=120)
months = set(r[0] for r in conn.execute("SELECT DISTINCT month FROM brand_audit").fetchall())
for month in months:
    rows = conn.execute("SELECT recalc_amount, summary_amount, is_real_diff, diff FROM brand_audit WHERE month=?", (month,)).fetchall()
    tr = round(sum(r[0] for r in rows), 2)
    ts = round(sum(r[1] for r in rows), 2)
    rd = round(sum(r[3] for r in rows if r[2]), 2)
    bc = len(rows)
    conn.execute("""INSERT OR REPLACE INTO monthly_audit(month,total_recalc,total_summary,total_diff,real_diff,brand_count)
        VALUES(?,?,?,?,?,?)""", (month, tr, ts, round(ts-tr, 2), rd, bc))
conn.commit()

# 统计
ma = list(conn.execute("SELECT * FROM monthly_audit ORDER BY month").fetchall())
print(f"\n总计 {len(ma)} 个月份:")
total_real_diff = 0
for m in ma:
    st = '✅' if m[4] == 0 else ('⚠️' if abs(m[4]) < 1000 else '❌')
    total_real_diff += m[4]
    print(f"  {m[0]}: {m[5]:3d}品牌  汇总={m[2]:>10.2f}  重算={m[1]:>10.2f}  真实差异={m[4]:>+10.2f} {st}")

perfect = sum(1 for m in ma if m[4] == 0)
print(f"\n通过: {perfect}/{len(ma)} | 总真实差异: {total_real_diff:+,.2f}")

# DB大小
db_size = os.path.getsize(DB_PATH) / 1024 / 1024
print(f"数据库大小: {db_size:.1f} MB")
print(f"DB: {DB_PATH}")

conn.close()
print("Done")

"""分析对公返佣数据"""
import sqlite3, re

DB = "/workspace/业务数据/集团客户部FY数据.db"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

table = "返佣信息表"

# Check how many records
cur.execute(f'SELECT COUNT(*) FROM "{table}"')
print(f"总记录数: {cur.fetchone()[0]}")

# Fix salesperson for 廖鹏的组织（服装）
cur.execute(f'UPDATE "{table}" SET "销售人员姓名" = "廖鹏" WHERE "level3" = "廖鹏的组织（服装）"')
print(f"修正廖鹏的组织: {cur.rowcount}条")

# Check unique level3 values
print("\n=== level3 唯一值 ===")
cur.execute(f'SELECT DISTINCT "level3" FROM "{table}" ORDER BY "level3"')
for r in cur.fetchall():
    v = r[0]
    if v and ('的组织' in str(v) or 'S' in str(v)):
        print(f"  需要检查: {repr(v)}")

# 1. 有对公返佣户名的记录数
cur.execute(f'SELECT COUNT(*) FROM "{table}" WHERE "对公返佣_户名" IS NOT NULL AND "对公返佣_户名" != "" AND "对公返佣_户名" != "#N/A"')
cnt = cur.fetchone()[0]
print(f"\n1. 有对公返佣户名的记录数(排除#N/A): {cnt}")

# 2. 按户名分组
print(f"\n2. 按户名分组统计商户数:")
cur.execute(f'''
    SELECT "对公返佣_户名" as 户名, COUNT(*) as 商户数,
           COUNT(DISTINCT CAST("对公返佣_银行账号" AS TEXT)) as 账户数
    FROM "{table}" 
    WHERE "对公返佣_户名" IS NOT NULL AND "对公返佣_户名" != '' AND "对公返佣_户名" != '#N/A'
    GROUP BY "对公返佣_户名"
    ORDER BY 商户数 DESC
    LIMIT 30
''')
print(f"  {'户名':<30} {'商户数':>8} {'账户数':>8}")
print(f"  {'-'*30} {'-'*8} {'-'*8}")
for r in cur.fetchall():
    print(f"  {r['户名'] if r['户名'] else '':<30} {r['商户数']:>8} {r['账户数']:>8}")

# 3. 同一银行账户对应多个不同户名
print(f"\n3. 同一银行账户对应多个不同户名（异常/舞弊嫌疑）:")
cur.execute(f'''
    SELECT CAST("对公返佣_银行账号" AS TEXT) as 账号,
           GROUP_CONCAT(DISTINCT "对公返佣_户名") as 户名列表,
           COUNT(DISTINCT "对公返佣_户名") as 户名数,
           COUNT(*) as 记录数
    FROM "{table}" 
    WHERE "对公返佣_银行账号" IS NOT NULL AND CAST("对公返佣_银行账号" AS TEXT) != '' 
      AND "对公返佣_银行账号" != '#N/A'
      AND "对公返佣_户名" IS NOT NULL AND "对公返佣_户名" != '' AND "对公返佣_户名" != '#N/A'
    GROUP BY CAST("对公返佣_银行账号" AS TEXT)
    HAVING 户名数 > 1
    ORDER BY 户名数 DESC
    LIMIT 20
''')
results = cur.fetchall()
if results:
    print(f"  {'账户(格式化)':<25} {'户名列表':<60} {'户名数':>6} {'记录数':>6}")
    print(f"  {'-'*25} {'-'*60} {'-'*6} {'-'*6}")
    for r in results:
        acc = str(r['账号'])[:24] if r['账号'] else ''
        print(f"  {acc:<25} {(r['户名列表'] or '')[:59]:<60} {r['户名数']:>6} {r['记录数']:>6}")
else:
    print("  ✅ 未发现同一银行账号对应多个户名的情况")

# 4. 按销售人员统计
print(f"\n4. 按销售人员姓名统计返佣情况:")
cur.execute(f'''
    SELECT "销售人员姓名" as sales, COUNT(*) as 商户数,
           SUM(CASE WHEN "对公返佣_户名" IS NOT NULL AND "对公返佣_户名" != '' AND "对公返佣_户名" != '#N/A' THEN 1 ELSE 0 END) as 有对公返佣,
           SUM(CASE WHEN "对私返佣_户名" IS NOT NULL AND "对私返佣_户名" != '' THEN 1 ELSE 0 END) as 有对私返佣
    FROM "{table}" 
    WHERE "销售人员姓名" IS NOT NULL
    GROUP BY "销售人员姓名"
    ORDER BY 商户数 DESC
''')
print(f"  {'销售人员':<18} {'商户数':>8} {'有对公返佣':>10} {'有对私返佣':>10}")
print(f"  {'-'*18} {'-'*8} {'-'*10} {'-'*10}")
for r in cur.fetchall():
    print(f"  {(r['sales'] or '空'):<18} {r['商户数']:>8} {r['有对公返佣']:>10} {r['有对私返佣']:>10}")

# 5. 对公返佣明细（排除#N/A）
print(f"\n5. 对公返佣明细（部分）:")
cur.execute(f'''
    SELECT sn, 商户名, brand, level3, "销售人员姓名",
           "对公返佣_返佣邮箱", "对公返佣_户名", "对公返佣_开户行", "对公返佣_银行账号"
    FROM "{table}" 
    WHERE "对公返佣_户名" IS NOT NULL AND "对公返佣_户名" != '' AND "对公返佣_户名" != '#N/A'
    ORDER BY "对公返佣_户名", sn
    LIMIT 30
''')
print(f"  {'sn':<18} {'商户名':<22} {'品牌':<12} {'销售人员':<10} {'户名':<20} {'银行账号':<20}")
print(f"  {'-'*18} {'-'*22} {'-'*12} {'-'*10} {'-'*20} {'-'*20}")
for r in cur.fetchall():
    bank_acc = str(r['对公返佣_银行账号']) if r['对公返佣_银行账号'] else ''
    if bank_acc.endswith('.0'):
        bank_acc = bank_acc[:-2]
    print(f"  {(r['sn'] or ''):<18} {(r['商户名'] or '')[:21]:<22} {(r['brand'] or '')[:11]:<12} {(r['销售人员姓名'] or '')[:9]:<10} {(r['对公返佣_户名'] or '')[:19]:<20} {bank_acc[:19]:<20}")

zero_acc = cur.execute(f'''SELECT COUNT(*) FROM "{table}" 
    WHERE "对公返佣_户名" IS NOT NULL AND "对公返佣_户名" != '' AND "对公返佣_户名" != '#N/A' 
    AND ("对公返佣_银行账号" IS NULL OR CAST("对公返佣_银行账号" AS TEXT) = '' OR "对公返佣_银行账号" = '#N/A')''').fetchone()[0]
print(f"\n  ⚠️ 有户名但无银行账号的记录: {zero_acc}条")

# Check 对私返佣
cur.execute(f'SELECT COUNT(*) FROM "{table}" WHERE "对私返佣_户名" IS NOT NULL AND "对私返佣_户名" != "" AND "对私返佣_户名" != "#N/A"')
cnt_private = cur.fetchone()[0]
print(f"\n6. 有对私返佣户名的记录数(排除#N/A): {cnt_private}")

# Summary
print(f"\n{'='*60}")
print("【对公返佣分析摘要】")
print(f"{'='*60}")
cur.execute(f'SELECT COUNT(DISTINCT "对公返佣_户名") FROM "{table}" WHERE "对公返佣_户名" IS NOT NULL AND "对公返佣_户名" != "" AND "对公返佣_户名" != "#N/A"')
print(f"去重对公返佣接收方户名数: {cur.fetchone()[0]}")
cur.execute(f'SELECT COUNT(*) FROM "{table}" WHERE "对公返佣_户名" IS NOT NULL AND "对公返佣_户名" != "" AND "对公返佣_户名" != "#N/A"')
print(f"有有效对公返佣户名的记录数: {cur.fetchone()[0]}")
cur.execute(f'SELECT COUNT(*) FROM "{table}"')
print(f"总记录数: {cur.fetchone()[0]}")

conn.close()
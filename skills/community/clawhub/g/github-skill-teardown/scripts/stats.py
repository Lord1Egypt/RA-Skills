"""对 319 个候选仓库做结构统计，为生态全景提供数据支撑。"""
import json, os
from collections import Counter

OUT = os.environ.get("SKILL_OUT") or os.path.join(os.getcwd(), "skill_out")
pool = json.load(open(os.path.join(OUT, "gh_skill_pool.json"), encoding="utf-8"))

print("=== 候选池规模 ===")
print("仓库数:", len(pool))

bands = [(100000, 10**9, "10万+"), (50000, 100000, "5-10万"), (20000, 50000, "2-5万"),
         (10000, 20000, "1-2万"), (5000, 10000, "5千-1万"), (1000, 5000, "1千-5千"),
         (0, 1000, "<1千")]
print("\n=== 星标分布 ===")
for lo, hi, name in bands:
    n = sum(1 for r in pool if lo <= r["stars"] < hi)
    print("  %-10s %4d  (%.1f%%)" % (name, n, 100.0 * n / len(pool)))

print("\n=== 语言 Top10 ===")
for k, v in Counter(r["lang"] for r in pool).most_common(10):
    print("  %-14s %d" % (k, v))

print("\n=== 许可证 ===")
for k, v in Counter(r["license"] for r in pool).most_common(8):
    print("  %-16s %d" % (k, v))

print("\n=== 最近更新（pushed）分布 ===")
fresh = sum(1 for r in pool if r["pushed"] >= "2026-09-01")
mid = sum(1 for r in pool if "2026-06-01" <= r["pushed"] < "2026-09-01")
old = sum(1 for r in pool if r["pushed"] < "2026-06-01")
print("  本月活跃(>=2026-09-01): %d" % fresh)
print("  近3月(2026-06~08):      %d" % mid)
print("  更早:                   %d" % old)

print("\n=== 关键词命中：编程/开发 vs 非编程 ===")
kw_code = ["code", "coding", "dev", "engineer", "refactor", "debug", "test", "git",
           "api", "frontend", "backend", "typescript", "python", "review", "deploy"]
kw_other = ["market", "content", "seo", "brand", "design", "writing", "academic",
            "research", "science", "legal", "finance", "health", "education", "video"]
c = o = 0
for r in pool:
    t = (r["desc"] + " " + r["topics"]).lower()
    if any(k in t for k in kw_code):
        c += 1
    if any(k in t for k in kw_other):
        o += 1
print("  命中编程类关键词: %d" % c)
print("  命中非编程类关键词: %d" % o)
print("  两者都有: %d" % sum(1 for r in pool
      if any(k in (r["desc"] + " " + r["topics"]).lower() for k in kw_code)
      and any(k in (r["desc"] + " " + r["topics"]).lower() for k in kw_other)))

print("\n=== 头部 30 的 desc 中出现「skill」的占比 ===")
top30 = sorted(pool, key=lambda r: -r["stars"])[:30]
n = sum(1 for r in top30 if "skill" in r["desc"].lower())
print("  %d/30" % n)

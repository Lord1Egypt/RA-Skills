"""扫描 GitHub 上 agent-skill 生态的仓库分布，按 stars 建立候选池。"""
import subprocess, json, os, sys, time

GH = r"C:\Program Files\GitHub CLI\gh.exe"
OUT = os.environ.get("SKILL_OUT") or os.path.join(os.getcwd(), "skill_out")


def gh_api(path):
    p = subprocess.run([GH, "api", path], capture_output=True)
    if p.returncode != 0:
        return None
    try:
        return json.loads(p.stdout.decode("utf-8", "replace"))
    except Exception:
        return None


QUERIES = [
    ("topic:agent-skills", "topic:agent-skills&sort=stars&per_page=60"),
    ("topic:claude-skills", "topic:claude-skills&sort=stars&per_page=60"),
    ("topic:claude-code-skills", "topic:claude-code-skills&sort=stars&per_page=60"),
    ("topic:claude-code+skills", "topic:claude-code+topic:skills&sort=stars&per_page=60"),
    ("topic:skills+agent", "topic:skills+topic:agent&sort=stars&per_page=60"),
    ("name:skills claude", "q=skills+claude+in:name&sort=stars&per_page=50"),
    ("awesome claude skills", "q=awesome+claude+skills+in:name,description&sort=stars&per_page=40"),
    ("SKILL.md", "q=SKILL.md+in:readme&sort=stars&per_page=40"),
    ("agent skills llm", "q=%22agent+skills%22+in:name,description&sort=stars&per_page=50"),
    ("skill marketplace", "q=skill+marketplace+in:name,description&sort=stars&per_page=40"),
]

pool = {}
for label, q in QUERIES:
    path = "search/repositories?q=" + q
    d = gh_api(path)
    if not d or "items" not in d:
        print("[WARN] query failed:", label)
        continue
    n = 0
    for it in d["items"]:
        fn = it["full_name"]
        prev = pool.get(fn)
        rec = {
            "full_name": fn,
            "stars": it.get("stargazers_count", 0),
            "forks": it.get("forks_count", 0),
            "issues": it.get("open_issues_count", 0),
            "desc": (it.get("description") or "").replace("\n", " "),
            "lang": it.get("language") or "-",
            "pushed": (it.get("pushed_at") or "")[:10],
            "created": (it.get("created_at") or "")[:10],
            "topics": ",".join(it.get("topics", [])[:8]),
            "license": ((it.get("license") or {}) or {}).get("spdx_id") or "-",
            "archived": it.get("archived", False),
            "hits": [label],
        }
        if prev:
            prev["hits"].append(label)
        else:
            pool[fn] = rec
            n += 1
    print(f"  {label:32s} -> +{n:3d} new (total {len(pool)})")
    time.sleep(2)

items = sorted(pool.values(), key=lambda r: -r["stars"])
with open(os.path.join(OUT, "gh_skill_pool.json"), "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=1)

print()
print("=" * 110)
print("TOP 60 by stars")
print("=" * 110)
print("%-46s %6s %6s %4s %10s %-12s %s" % ("repo", "star", "fork", "iss", "pushed", "lang", "desc"))
for r in items[:60]:
    print(
        "%-46s %6d %6d %4d %10s %-12s %s"
        % (
            r["full_name"][:45],
            r["stars"],
            r["forks"],
            r["issues"],
            r["pushed"],
            r["lang"][:12],
            r["desc"][:70],
        )
    )
print()
print("total repos in pool:", len(items))

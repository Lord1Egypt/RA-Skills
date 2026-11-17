"""扫描与国内生态（微信/飞书/钉钉/小红书/抖音/国产模型）相关的 skill 仓库。"""
import subprocess, json, os, time

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
    ("wechat skill", "q=wechat+skill+in:name,description&sort=stars&per_page=30"),
    ("weixin", "q=%E5%BE%AE%E4%BF%A1+skill&sort=stars&per_page=20"),
    ("xiaohongshu", "q=xiaohongshu&sort=stars&per_page=30"),
    ("%E5%B0%8F%E7%BA%A2%E4%B9%A6", "q=%E5%B0%8F%E7%BA%A2%E4%B9%A6&sort=stars&per_page=30"),
    ("douyin", "q=douyin&sort=stars&per_page=30"),
    ("feishu", "q=feishu+OR+lark+skill&sort=stars&per_page=30"),
    ("dingtalk", "q=dingtalk&sort=stars&per_page=25"),
    ("deepseek skill", "q=deepseek+skill&sort=stars&per_page=30"),
    ("qwen skill", "q=qwen+OR+%E9%80%9A%E4%B9%89+skill&sort=stars&per_page=25"),
    ("openclaw skills", "q=openclaw&sort=stars&per_page=30"),
    ("agent-skills chinese", "q=agent-skills+%E4%B8%AD%E6%96%87&sort=stars&per_page=25"),
    ("skill chinese docs", "q=%E6%8A%80%E8%83%BD+skill&sort=stars&per_page=25"),
]

pool = {}
for label, q in QUERIES:
    d = gh_api("search/repositories?q=" + q)
    if not d or "items" not in d:
        print("[WARN]", label)
        continue
    for it in d["items"]:
        fn = it["full_name"]
        if fn in pool:
            continue
        pool[fn] = {
            "full_name": fn,
            "stars": it.get("stargazers_count", 0),
            "desc": (it.get("description") or "").replace("\n", " "),
            "pushed": (it.get("pushed_at") or "")[:10],
            "topics": ",".join(it.get("topics", [])[:6]),
            "hits": label,
        }
    time.sleep(2)

items = sorted(pool.values(), key=lambda r: -r["stars"])
with open(os.path.join(OUT, "cn_skill_pool.json"), "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=1)

print("%-46s %7s %10s %s" % ("repo", "star", "pushed", "desc"))
print("-" * 118)
for r in items[:55]:
    print("%-46s %7d %10s %s" % (r["full_name"][:45], r["stars"], r["pushed"], r["desc"][:64]))
print()
print("total:", len(items))

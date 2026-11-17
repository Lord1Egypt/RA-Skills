"""对候选仓库逐个探查：默认分支、文件树、SKILL.md 数量与体积。"""
import subprocess, json, os

GH = r"C:\Program Files\GitHub CLI\gh.exe"
OUT = os.environ.get("SKILL_OUT") or os.path.join(os.getcwd(), "skill_out")

CANDIDATES = [
    "anthropics/skills",
    "affaan-m/ECC",
    "msitarzewski/agency-agents",
    "DietrichGebert/ponytail",
    "JuliusBrussee/caveman",
    "addyosmani/agent-skills",
    "nexu-io/open-design",
    "thedotmack/claude-mem",
    "Leonxlnx/taste-skill",
    "ComposioHQ/awesome-claude-skills",
    "tt-a1i/archify",
    "VoltAgent/awesome-openclaw-skills",
    "blader/humanizer",
    "ayghri/i-have-adhd",
    "sickn33/agentic-awesome-skills",
    "K-Dense-AI/scientific-agent-skills",
    "Yuan1z0825/nature-skills",
    "cathrynlavery/diagram-design",
    "github/awesome-copilot",
    "anthropics/claude-plugins-official",
    "Egonex-AI/Understand-Anything",
    "Graphify-Labs/graphify",
    "wshobson/agents",
    "shanraisshan/claude-code-best-practice",
]


def gh(path):
    p = subprocess.run([GH, "api", path], capture_output=True)
    if p.returncode != 0:
        return None
    try:
        return json.loads(p.stdout.decode("utf-8", "replace"))
    except Exception:
        return None


rows = []
detail = {}
for full in CANDIDATES:
    info = gh("repos/" + full)
    if not info:
        print("[WARN] repo not found:", full)
        continue
    br = info.get("default_branch", "main")
    tree = gh(f"repos/{full}/git/trees/{br}?recursive=1")
    files = []
    if tree and "tree" in tree:
        files = [t["path"] for t in tree["tree"] if t["type"] == "blob"]
    skills = [f for f in files if f.endswith("SKILL.md") or f.endswith("skill.md")]
    mds = [f for f in files if f.lower().endswith(".md")]
    scripts = [
        f
        for f in files
        if f.lower().endswith((".py", ".js", ".ts", ".sh", ".ps1", ".tsx", ".mjs"))
    ]
    rec = {
        "full_name": full,
        "stars": info.get("stargazers_count", 0),
        "forks": info.get("forks_count", 0),
        "desc": (info.get("description") or "").replace("\n", " "),
        "license": ((info.get("license") or {}) or {}).get("spdx_id") or "-",
        "pushed": (info.get("pushed_at") or "")[:10],
        "created": (info.get("created_at") or "")[:10],
        "size_kb": info.get("size", 0),
        "branch": br,
        "file_count": len(files),
        "skill_md_count": len(skills),
        "md_count": len(mds),
        "script_count": len(scripts),
        "top_skills": skills[:25],
        "top_readme": [f for f in files if f.lower().startswith("readme")][:3],
        "lang": info.get("language") or "-",
    }
    rows.append(rec)
    detail[full] = {"skills": skills, "files": files}
    print(
        "%-42s star=%-7d files=%-5d SKILL.md=%-4d md=%-5d script=%-5d size=%dKB"
        % (full, rec["stars"], rec["file_count"], rec["skill_md_count"], rec["md_count"], rec["script_count"], rec["size_kb"])
    )

with open(os.path.join(OUT, "gh_skill_detail.json"), "w", encoding="utf-8") as f:
    json.dump({"rows": rows, "detail": {k: v["skills"] for k, v in detail.items()}}, f, ensure_ascii=False, indent=1)

print()
print("=" * 110)
print("含 SKILL.md 的仓库 —— 其 skill 清单")
print("=" * 110)
for r in sorted(rows, key=lambda x: -x["skill_md_count"]):
    if r["skill_md_count"] == 0:
        continue
    print(f"\n### {r['full_name']}  ({r['stars']} star, {r['skill_md_count']} skills)")
    for s in r["top_skills"][:18]:
        print("    " + s)

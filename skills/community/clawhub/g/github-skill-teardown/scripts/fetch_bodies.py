"""抓取 10 个入选样本的核心文件正文（README + 主 SKILL.md），落盘待分析。"""
import subprocess, json, os, base64

GH = r"C:\Program Files\GitHub CLI\gh.exe"
OUT = os.environ.get("SKILL_OUT") or os.path.join(os.getcwd(), "skill_out")
DST = os.path.join(OUT, "gh_skills_raw")
os.makedirs(DST, exist_ok=True)

REPOS = [
    "obra/superpowers",
    "mattpocock/skills",
    "affaan-m/ECC",
    "multica-ai/andrej-karpathy-skills",
    "anthropics/skills",
    "JuliusBrussee/caveman",
    "addyosmani/agent-skills",
    "nexu-io/open-design",
    "thedotmack/claude-mem",
    "Yuan1z0825/nature-skills",
    # 备选观察名单，一并取结构
    "Leonxlnx/taste-skill",
    "blader/humanizer",
    "sickn33/agentic-awesome-skills",
    "ComposioHQ/awesome-claude-skills",
    "nextlevelbuilder/ui-ux-pro-max-skill",
]

MAXLEN = 7000


def gh(path):
    p = subprocess.run([GH, "api", path], capture_output=True)
    if p.returncode != 0:
        return None
    try:
        return json.loads(p.stdout.decode("utf-8", "replace"))
    except Exception:
        return None


def gh_raw(full, ref, path):
    d = gh(f"repos/{full}/contents/{path}?ref={ref}")
    if not d or "content" not in d:
        return None
    try:
        return base64.b64decode(d["content"]).decode("utf-8", "replace")
    except Exception:
        return None


summary = {}
for full in REPOS:
    info = gh("repos/" + full)
    if not info:
        print("[MISS]", full)
        continue
    br = info.get("default_branch", "main")
    tree = gh(f"repos/{full}/git/trees/{br}?recursive=1")
    files = [t["path"] for t in tree.get("tree", []) if t["type"] == "blob"] if tree else []

    entry = {
        "full_name": full,
        "stars": info.get("stargazers_count", 0),
        "forks": info.get("forks_count", 0),
        "desc": info.get("description") or "",
        "license": ((info.get("license") or {}) or {}).get("spdx_id") or "-",
        "created": (info.get("created_at") or "")[:10],
        "pushed": (info.get("pushed_at") or "")[:10],
        "branch": br,
        "topics": info.get("topics", []),
        "file_count": len(files),
        "taken": [],
    }

    # README
    readme = next((f for f in files if f.lower() in ("readme.md", "readme.zh-cn.md", "readme")), None)
    if readme:
        t = gh_raw(full, br, readme)
        if t:
            fn = os.path.join(DST, full.replace("/", "__") + "__README.md")
            open(fn, "w", encoding="utf-8").write(t[:MAXLEN])
            entry["taken"].append(("README", readme, len(t), t[:MAXLEN]))

    # SKILL.md：优先取根目录 / skills/ 直接子级，最多 4 个，避开海量目录
    skills = [f for f in files if f.endswith("SKILL.md") or f == "CLAUDE.md" or f.endswith("skill.md")]
    skills = [s for s in skills if s.count("/") <= 3]
    root_first = sorted(skills, key=lambda s: (s.count("/"), len(s)))
    for s in root_first[:4]:
        t = gh_raw(full, br, s)
        if not t:
            continue
        fn = os.path.join(DST, full.replace("/", "__") + "__" + s.replace("/", "_"))
        open(fn, "w", encoding="utf-8").write(t[:MAXLEN])
        entry["taken"].append((s, s, len(t), t[:MAXLEN]))

    # 目录骨架（前 120 条）
    entry["sample_tree"] = files[:140]
    summary[full] = entry
    print(
        "%-42s star=%-7d files=%-6d took=%d"
        % (full, entry["stars"], len(files), len(entry["taken"]))
    )

with open(os.path.join(OUT, "gh_skills_raw.json"), "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=1)
print()
print("saved:", len(summary), "repos ->", DST)

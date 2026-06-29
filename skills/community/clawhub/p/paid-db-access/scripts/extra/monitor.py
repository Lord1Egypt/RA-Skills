#!/usr/bin/env python3

"""

新论文监控 · New Paper Monitor



User triggers a check → system searches with saved conditions → diffs against

last baseline → returns only what's new. That's it.



Usage:

    python monitor.py init                              # Interactive wizard

    python monitor.py init -n <name> -k <keywords> -d <dbs>  # Non-interactive

    python monitor.py list                              # List all monitors

    python monitor.py diff <name> --files <result files>     # What's new?

    python monitor.py save <name> --files <result files>     # Save new baseline

    python monitor.py suppress <name> --doi <doi>            # Hide this paper

    python monitor.py remove <name>                          # Delete monitor

    python monitor.py status <name>                          # Monitor details



Design:

    - Default OFF in config.yaml (monitoring.enabled: false)

    - Consumes merge_results.py JSON output; never participates in search pipeline

    - Fails gracefully: corrupted baseline → empty diff, never crash

    - Monitor isolation: each monitor is independent



Storage:

    memory/monitors/

    ├── monitors.json              # Index of all monitors

    └── <name>/

        ├── config.json            # Keywords, databases, created

        ├── baseline.json          # Confirmed snapshot (what user has seen)

        └── suppressed.json        # DOIs user doesn't want to see

"""



import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse

import json

import os

import sys

import time

from datetime import datetime, timezone

from pathlib import Path



from utils.doi_utils import normalize as normalize_doi



import sys, os




# Fix Windows console encoding

if sys.platform == "win32":

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")



SKILL_DIR = Path(__file__).resolve().parent.parent

CONFIG_PATH = SKILL_DIR / "config.yaml"

MONITORS_DIR = SKILL_DIR / "memory" / "monitors"

INDEX_PATH = MONITORS_DIR / "monitors.json"



# -- Helpers ----------------------------------------------------------------



def load_config():

    """Load config.yaml, return monitoring section."""

    if not CONFIG_PATH.exists():

        return {"enabled": False}

    try:

        import yaml

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:

            cfg = yaml.safe_load(f) or {}

        return cfg.get("monitoring", {"enabled": False})

    except ImportError:

        return {"enabled": False}





def load_index():

    """Load monitors.json index."""

    if not INDEX_PATH.exists():

        return {"monitors": {}}

    try:

        with open(INDEX_PATH, "r", encoding="utf-8") as f:

            return json.load(f)

    except (json.JSONDecodeError, FileNotFoundError):

        return {"monitors": {}}





def save_index(index):

    """Save monitors.json index."""

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(INDEX_PATH, "w", encoding="utf-8") as f:

        json.dump(index, f, ensure_ascii=False, indent=2)





def get_monitor_dir(name):

    """Get the directory for a monitor."""

    safe_name = "".join(c if c.isalnum() or c in "-_" else "-" for c in name).strip("-")

    return MONITORS_DIR / safe_name





def load_monitor_config(name):

    """Load a monitor's config.json."""

    mdir = get_monitor_dir(name)

    path = mdir / "config.json"

    if not path.exists():

        return None

    with open(path, "r", encoding="utf-8") as f:

        return json.load(f)





def load_baseline(name):

    """Load a monitor's baseline.json."""

    path = get_monitor_dir(name) / "baseline.json"

    if not path.exists():

        return None

    try:

        with open(path, "r", encoding="utf-8") as f:

            return json.load(f)

    except (json.JSONDecodeError, FileNotFoundError):

        return None





def load_suppressed(name):

    """Load a monitor's suppressed.json."""

    path = get_monitor_dir(name) / "suppressed.json"

    if not path.exists():

        return {}

    try:

        with open(path, "r", encoding="utf-8") as f:

            return json.load(f)

    except (json.JSONDecodeError, FileNotFoundError):

        return {}





def normalize_title(title):

    """Normalize title for fuzzy comparison."""

    if not title:

        return ""

    import re

    t = title.lower()

    t = re.sub(r'[^\w\s]', ' ', t)

    t = re.sub(r'\s+', ' ', t).strip()

    return t





def title_similarity(t1, t2):

    """Token overlap ratio between two normalized titles."""

    tokens1 = set(normalize_title(t1).split())

    tokens2 = set(normalize_title(t2).split())

    if not tokens1 or not tokens2:

        return 0.0

    return len(tokens1 & tokens2) / min(len(tokens1), len(tokens2))





def now_iso():

    """ISO timestamp for now."""

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")





# -- Commands ---------------------------------------------------------------



def cmd_init(args):

    """Create a new monitor."""

    # Check if monitoring is enabled

    cfg = load_config()

    if not cfg.get("enabled", False):

        print("monitoring.enabled = false in config.yaml")

        print("将 config.yaml 中 monitoring.enabled 改为 true 后重试。")

        return



    # Interactive mode

    if not args.name:

        print("创建新的论文监控\n")

        args.name = input("  监控名称 (e.g. llm-code-generation): ").strip()

        if not args.name:

            print("取消。")

            return

        args.keywords = input("  搜索关键词 (逗号分隔): ").strip()

        args.databases = input("  数据库 (ieee,scopus,acm,...): ").strip()



    name = args.name

    keywords = args.keywords or ""

    databases = args.databases or "ieee,scopus"



    mdir = get_monitor_dir(name)

    if mdir.exists():

        print(f"监控 '{name}' 已存在。用 --remove 先删除，或换一个名称。")

        return



    # Check for similar existing monitors

    index = load_index()

    kw_set = set(k.strip().lower() for k in keywords.split(",") if k.strip())

    for existing_name, info in index.get("monitors", {}).items():

        existing_kw = set(k.strip().lower() for k in info.get("keywords", "").split(",") if k.strip())

        if kw_set and existing_kw:

            overlap = len(kw_set & existing_kw) / min(len(kw_set), len(existing_kw)) if min(len(kw_set), len(existing_kw)) > 0 else 0

            if overlap >= 0.6:

                print(f"\n  [!] 关键词与已有监控 '{existing_name}' 高度重叠 ({overlap:.0%})")

                print(f"      已有关键词: {info.get('keywords')}")

                resp = input("  仍要创建？(y/n): ").strip().lower()

                if resp != "y":

                    print("取消。")

                    return



    # Create monitor

    mdir.mkdir(parents=True, exist_ok=True)

    config = {

        "name": name,

        "keywords": keywords,

        "databases": [d.strip() for d in databases.split(",") if d.strip()],

        "created": now_iso(),

        "last_check": None,

    }

    with open(mdir / "config.json", "w", encoding="utf-8") as f:

        json.dump(config, f, ensure_ascii=False, indent=2)



    # Empty baseline

    baseline = {

        "monitor": name,

        "updated": now_iso(),

        "total": 0,

        "papers": [],

    }

    with open(mdir / "baseline.json", "w", encoding="utf-8") as f:

        json.dump(baseline, f, ensure_ascii=False, indent=2)



    # Empty suppressed

    with open(mdir / "suppressed.json", "w", encoding="utf-8") as f:

        json.dump({}, f, ensure_ascii=False, indent=2)



    # Update index

    index.setdefault("monitors", {})[name] = {

        "keywords": keywords,

        "databases": config["databases"],

        "created": config["created"],

        "last_check": None,

        "baseline_count": 0,

    }

    save_index(index)



    print(f"\n  监控 '{name}' 已创建。")

    print(f"  关键词: {keywords}")

    print(f"  数据库: {', '.join(config['databases'])}")

    print(f"  基线为空，跑一次搜索后 --save 即可建立基线。")





def cmd_list(args):

    """List all monitors."""

    index = load_index()

    monitors = index.get("monitors", {})



    if not monitors:

        print("没有已建立的监控。")

        print(f"创建: python scripts/monitor.py init")

        return



    print(f"\n  已建监控 ({len(monitors)} 个)\n")

    for i, (name, info) in enumerate(monitors.items(), 1):

        kw = info.get("keywords", "-")

        dbs = ", ".join(info.get("databases", []))

        last = info.get("last_check")

        count = info.get("baseline_count", 0)

        last_str = last[:10] if last else "从未检查"



        print(f"  {i}. {name}")

        print(f"     关键词: {kw}")

        print(f"     数据库: {dbs}")

        print(f"     基线: {count} 篇 · 上次: {last_str}")

        print()





def cmd_diff(args):

    """Diff current results against baseline."""

    name = args.name

    config = load_monitor_config(name)

    if not config:

        print(f"监控 '{name}' 不存在。用 --init 创建。")

        return



    baseline = load_baseline(name)

    if not baseline:

        baseline = {"papers": [], "total": 0, "updated": None}



    suppressed = load_suppressed(name)



    # Load current results from files

    current_papers = []

    databases_searched = []

    for fpath in args.files:

        try:

            with open(fpath, "r", encoding="utf-8") as f:

                data = json.load(f)

        except (FileNotFoundError, json.JSONDecodeError) as e:

            print(f"Warning: 无法读取 {fpath}: {e}", file=sys.stderr)

            continue



        if isinstance(data, dict) and "papers" in data:

            current_papers.extend(data["papers"])

            databases_searched.append(data.get("database", Path(fpath).stem))

        elif isinstance(data, list):

            current_papers.extend(data)



    if not current_papers:

        print("当前搜索结果为空。")

        return



    # Build baseline index by DOI + title

    baseline_by_doi = {}

    baseline_by_title = []

    for p in baseline.get("papers", []):

        doi = normalize_doi(p.get("doi"))

        if doi:

            baseline_by_doi[doi] = p

        baseline_by_title.append(p)



    # Find new papers

    new_papers = []

    updated_citations = []



    for paper in current_papers:

        doi = normalize_doi(paper.get("doi"))



        # Check suppressed

        if doi and doi in suppressed:

            # Paper was suppressed, but check if citations spiked significantly

            suppressed_info = suppressed[doi]

            old_cit = suppressed_info.get("citations_at_suppress", 0)

            new_cit = paper.get("citations", 0) or 0

            if new_cit - old_cit >= 10:

                updated_citations.append({

                    **paper,

                    "_change": "citation_spike",

                    "_old_citations": old_cit,

                    "_new_citations": new_cit,

                    "_was_suppressed": True,

                })

            continue



        # Check exact DOI match in baseline

        if doi and doi in baseline_by_doi:

            old = baseline_by_doi[doi]

            old_cit = old.get("citations_snapshot", 0) or 0

            new_cit = paper.get("citations", 0) or 0

            if new_cit - old_cit >= 10:

                updated_citations.append({

                    **paper,

                    "_change": "citation_spike",

                    "_old_citations": old_cit,

                    "_new_citations": new_cit,

                })

            continue



        # Check fuzzy title match with baseline (for papers without DOI)

        found_in_baseline = False

        current_title = paper.get("title", "")

        for bp in baseline.get("papers", []):

            if title_similarity(current_title, bp.get("title", "")) >= 0.80:

                found_in_baseline = True

                old_cit = bp.get("citations_snapshot", 0) or 0

                new_cit = paper.get("citations", 0) or 0

                if new_cit - old_cit >= 10:

                    updated_citations.append({

                        **paper,

                        "_change": "citation_spike",

                        "_old_citations": old_cit,

                        "_new_citations": new_cit,

                    })

                break



        if not found_in_baseline:

            # It's new

            pub_year = paper.get("year", 0) or 0

            current_year = datetime.now().year

            if pub_year == current_year:

                change_type = "new_publication"

                change_label = "今年新发"

            elif pub_year == current_year - 1:

                change_type = "new_publication"

                change_label = "去年发表"

            elif pub_year > 0:

                change_type = "newly_indexed"

                change_label = f"新收录 ({pub_year})"

            else:

                change_type = "newly_indexed"

                change_label = "新收录"



            new_papers.append({

                **paper,

                "_change": change_type,

                "_change_label": change_label,

            })



    # Papers that disappeared from baseline

    current_dois = set()

    for p in current_papers:

        doi = normalize_doi(p.get("doi"))

        if doi:

            current_dois.add(doi)



    disappeared = []

    for p in baseline.get("papers", []):

        doi = normalize_doi(p.get("doi"))

        if doi and doi not in current_dois:

            # Fuzzy title check in case DOI changed

            title = p.get("title", "")

            still_there = any(

                title_similarity(title, cp.get("title", "")) >= 0.80

                for cp in current_papers

            )

            if not still_there:

                disappeared.append(p)



    # Output

    now = now_iso()

    result = {

        "monitor": name,

        "compared_at": now,

        "baseline_updated": baseline.get("updated"),

        "baseline_count": baseline.get("total", 0),

        "current_count": len(current_papers),

        "new_papers": new_papers,

        "new_count": len(new_papers),

        "citation_spikes": updated_citations,

        "spike_count": len(updated_citations),

        "disappeared": disappeared,

        "disappeared_count": len(disappeared),

        "total_changes": len(new_papers) + len(updated_citations) + len(disappeared),

    }



    print(json.dumps(result, ensure_ascii=False, indent=2))



    # Summary to stderr

    if new_papers or updated_citations:

        print(f"\n  Monitor: {name}", file=sys.stderr)

        print(f"  基线: {baseline.get('total', 0)} 篇 (上次: {baseline.get('updated', '?')})", file=sys.stderr)

        print(f"  本次: {len(current_papers)} 篇", file=sys.stderr)

        print(f"  ---", file=sys.stderr)

        if new_papers:

            print(f"  NEW {len(new_papers)} 篇新论文", file=sys.stderr)

            for p in new_papers[:5]:

                label = p.get("_change_label", "new")

                print(f"    [{label}] {p.get('title', '?')[:80]}", file=sys.stderr)

            if len(new_papers) > 5:

                print(f"    ... 还有 {len(new_papers) - 5} 篇", file=sys.stderr)

        if updated_citations:

            print(f"  CITE {len(updated_citations)} 篇引用飙升", file=sys.stderr)

            for p in updated_citations:

                flag = " [suppressed]" if p.get("_was_suppressed") else ""

                print(f"    {p.get('title', '?')[:60]}: {p['_old_citations']} → {p['_new_citations']} 引用{flag}", file=sys.stderr)

        if disappeared:

            print(f"  GONE {len(disappeared)} 篇从上一次基线消失", file=sys.stderr)





def cmd_save(args):

    """Save current results as new baseline."""

    name = args.name

    config = load_monitor_config(name)

    if not config:

        print(f"监控 '{name}' 不存在。用 --init 创建。")

        return



    # Load current results

    current_papers = []

    for fpath in args.files:

        try:

            with open(fpath, "r", encoding="utf-8") as f:

                data = json.load(f)

        except (FileNotFoundError, json.JSONDecodeError) as e:

            print(f"Warning: 无法读取 {fpath}: {e}", file=sys.stderr)

            continue



        if isinstance(data, dict) and "papers" in data:

            current_papers.extend(data["papers"])

        elif isinstance(data, list):

            current_papers.extend(data)



    if not current_papers:

        print("当前搜索结果为空，不更新基线。")

        return



    # Build baseline papers with citations_snapshot

    now = now_iso()

    baseline_papers = []

    for p in current_papers:

        baseline_papers.append({

            "doi": p.get("doi", ""),

            "title": p.get("title", ""),

            "year": p.get("year"),

            "citations_snapshot": p.get("citations", 0) or 0,

            "first_seen": now[:10],

            "source_db": p.get("_source_db", []),

        })



    baseline = {

        "monitor": name,

        "updated": now,

        "total": len(baseline_papers),

        "papers": baseline_papers,

    }



    mdir = get_monitor_dir(name)

    with open(mdir / "baseline.json", "w", encoding="utf-8") as f:

        json.dump(baseline, f, ensure_ascii=False, indent=2)



    # Update config

    config["last_check"] = now

    with open(mdir / "config.json", "w", encoding="utf-8") as f:

        json.dump(config, f, ensure_ascii=False, indent=2)



    # Update index

    index = load_index()

    if name in index.get("monitors", {}):

        index["monitors"][name]["last_check"] = now

        index["monitors"][name]["baseline_count"] = len(baseline_papers)

        save_index(index)



    print(f"基线已更新: {len(baseline_papers)} 篇论文 ({now[:10]})")





def cmd_suppress(args):

    """Suppress a paper by DOI."""

    name = args.name

    doi = args.doi

    if not load_monitor_config(name):

        print(f"监控 '{name}' 不存在。")

        return



    mdir = get_monitor_dir(name)

    suppressed = load_suppressed(name)



    ndoi = normalize_doi(doi) or doi

    suppressed[ndoi] = {

        "reason": args.reason or "user suppressed",

        "when": now_iso(),

        "citations_at_suppress": 0,  # Will be updated if paper reappears

    }



    with open(mdir / "suppressed.json", "w", encoding="utf-8") as f:

        json.dump(suppressed, f, ensure_ascii=False, indent=2)



    print(f"已 suppress: {doi}")





def cmd_remove(args):

    """Delete a monitor."""

    name = args.name

    mdir = get_monitor_dir(name)



    if not mdir.exists():

        print(f"监控 '{name}' 不存在。")

        return



    # Confirmation

    config = load_monitor_config(name)

    if config:

        print(f"要删除监控 '{name}'？")

        print(f"  关键词: {config.get('keywords')}")

        print(f"  基线论文数: {config.get('last_check') and load_baseline(name) and load_baseline(name).get('total', 0) or 0}")

        if args.force:

            resp = "y"

        else:

            resp = input("输入 y 确认: ").strip().lower()

        if resp != "y":

            print("取消。")

            return



    # Remove directory

    import shutil

    shutil.rmtree(mdir, ignore_errors=True)



    # Remove from index

    index = load_index()

    if name in index.get("monitors", {}):

        del index["monitors"][name]

        save_index(index)



    print(f"监控 '{name}' 已删除。")





def cmd_status(args):

    """Show monitor details."""

    name = args.name

    config = load_monitor_config(name)

    if not config:

        print(f"监控 '{name}' 不存在。")

        return



    baseline = load_baseline(name)

    suppressed = load_suppressed(name)



    print(f"\n  监控: {name}")

    print(f"  关键词: {config.get('keywords')}")

    print(f"  数据库: {', '.join(config.get('databases', []))}")

    print(f"  创建: {config.get('created', '?')[:10]}")

    print(f"  上次检查: {(config.get('last_check') or '从未')[:10]}")

    print(f"  基线论文: {baseline.get('total', 0) if baseline else 0} 篇")

    print(f"  Suppress: {len(suppressed)} 篇")

    if suppressed:

        for doi, info in suppressed.items():

            print(f"    {doi} — {info.get('reason', '')} ({info.get('when', '')[:10]})")





# -- Main ----------------------------------------------------------------



def main():

    parser = argparse.ArgumentParser(description="新论文监控 · New Paper Monitor")

    sub = parser.add_subparsers(dest="command")



    # --init

    p_init = sub.add_parser("init", help="创建新监控")

    p_init.add_argument("-n", "--name")

    p_init.add_argument("-k", "--keywords")

    p_init.add_argument("-d", "--databases")



    # --list

    sub.add_parser("list", help="列出所有监控")



    # --diff

    p_diff = sub.add_parser("diff", help="对比本次结果与基线")

    p_diff.add_argument("name")

    p_diff.add_argument("--files", nargs="+", required=True)



    # --save

    p_save = sub.add_parser("save", help="保存为新的基线")

    p_save.add_argument("name")

    p_save.add_argument("--files", nargs="+", required=True)



    # --suppress

    p_supp = sub.add_parser("suppress", help="隐藏某篇论文")

    p_supp.add_argument("name")

    p_supp.add_argument("--doi", required=True)

    p_supp.add_argument("--reason")



    # --remove

    p_rm = sub.add_parser("remove", help="删除监控")

    p_rm.add_argument("name")

    p_rm.add_argument("--force", action="store_true", help="跳过确认")



    # --status

    p_stat = sub.add_parser("status", help="查看监控详情")

    p_stat.add_argument("name")



    args = parser.parse_args()



    if not args.command:

        parser.print_help()

        return



    # Route to command

    cmds = {

        "init": cmd_init,

        "list": cmd_list,

        "diff": cmd_diff,

        "save": cmd_save,

        "suppress": cmd_suppress,

        "remove": cmd_remove,

        "status": cmd_status,

    }



    cmd_fn = cmds.get(args.command)

    if cmd_fn:

        try:

            cmd_fn(args)

        except Exception as e:

            # Graceful failure: report error, never crash the pipeline

            print(f"monitor.py error ({args.command}): {e}", file=sys.stderr)

            # Output valid empty JSON for diff so pipeline doesn't break

            if args.command == "diff":

                print(json.dumps({

                    "monitor": getattr(args, "name", "unknown"),

                    "error": str(e),

                    "new_papers": [],

                    "citation_spikes": [],

                    "disappeared": [],

                }, ensure_ascii=False, indent=2))

    else:

        parser.print_help()





if __name__ == "__main__":

    main()


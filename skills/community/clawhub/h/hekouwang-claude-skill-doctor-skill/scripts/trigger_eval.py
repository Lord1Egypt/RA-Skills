#!/usr/bin/env python3
"""触发力实测（trigger eval）—— skill-doctor 的可选第二引擎。

`check.py` 是静态检查：只能看出 description 里有没有"当…时/use when"这类信号词，
**判不出写得准不准**（那是 SKILL.md「机检的盲区」里明写的第一条）。
本脚本补的就是这一层：真的跑一遍，看模型到底会不会被这段 description 唤醒。

## 原理

把待测 description 装成一个**临时的 project 级 skill**（中性名 probe-xxxxxxxx），
放进一个一次性的 project root，然后跑 `claude -p <query>`，
看模型有没有去 Skill/Read 这个探针。跑完即删，不碰任何已装的 skill。

## ⚠️ 与官方 anthropics/skills · skill-creator/run_eval.py 的四处关键差异

官方那版思路对，但原样跑在 Claude Code 2.1.220 上**测不出任何东西**。
四处全改完才有分辨力（2026-07-28 实测：真 description 100 分 vs
"生成内容。"50 分；不改第 4 处时两者都是 100，等于白测）：

1. **`--setting-sources project`** —— 不加则子进程继承 ~/.claude/skills/ 里
   已装的真 skill，模型去触发真身、名字对不上探针，全部正例假阴性。
2. **扫完整个流才判否** —— 官方"第一个工具不是 Skill/Read 就 return False"，
   但模型碰到陌生 skill 名会先 `Bash: ls` 探查，Skill 往往是第二三个动作。
3. **每条 query 独立 project root** —— 共用目录时并发 worker 互相串台，
   模型会调到别人的探针，自己这条被误判成没触发。
4. **探针要装成真 skill + 中性名** —— init 事件里 skills / slash_commands
   两个列表**都只给名字、不给 description**。探针一旦沿用原 skill 名，
   模型光看名字就去 Read 它，description 全程没参与决策。

## 用法

    python3 trigger_eval.py --eval-set queries.json --skill-path <skill目录>

eval set 是一个 JSON 数组，怎么设计见 references/trigger-eval.md：

    [
      {"query": "用户真会打出来的一整段话", "should_trigger": true},
      {"query": "共享关键词但其实该走别的工具的近似请求", "should_trigger": false}
    ]

## 成本（跑之前一定要知道）

每条 query 每次采样 = 一次真实 `claude -p` 调用，约 $0.09–0.15。
默认 --runs-per-query 1 是为了省钱；要稳定结论再调 3
（触发是概率性的，3 次取触发率更可信，但成本也 ×3）。

## 隔离（被测 description 一律当不可信输入）

- 子进程只开放 `Skill`、`Read` 两个内置工具，`--strict-mcp-config` 不加载任何 MCP；
- 环境变量走白名单（PATH/HOME/语言区域/代理 + ANTHROPIC_*、CLAUDE_CODE_*），
  其余凭据不传；Bedrock/Vertex 等额外变量用 `--pass-env` 显式放行；
- 探针正文只写固定的中性说明，不把 description 当指令正文。
"""

import argparse
import json
import os
import re
import select
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

TOOL_HINT = "Skill", "Read"

ENV_ALLOW = {
    "PATH", "HOME", "USER", "LOGNAME", "SHELL", "TMPDIR", "TERM",
    "LANG", "LC_ALL", "LC_CTYPE",
    "HTTP_PROXY", "HTTPS_PROXY", "NO_PROXY", "http_proxy", "https_proxy", "no_proxy",
}
ENV_ALLOW_PREFIX = ("ANTHROPIC_", "CLAUDE_CODE_")


def build_env(extra=()):
    """子进程最小环境：只放 claude CLI 跑起来必需的变量。"""
    keep = ENV_ALLOW | set(extra)
    return {k: v for k, v in os.environ.items()
            if k != "CLAUDECODE" and (k in keep or k.startswith(ENV_ALLOW_PREFIX))}


def parse_skill_md(skill_path: Path) -> tuple[str, str]:
    """从 SKILL.md 的 frontmatter 里取 name 和 description。

    description 三种写法都要认：折叠块 `>`、字面块 `|`、单行。
    """
    md = skill_path / "SKILL.md"
    if not md.exists():
        raise SystemExit(f"找不到 {md}")
    text = md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise SystemExit(f"{md} 没有 frontmatter")
    fm = m.group(1)

    name_m = re.search(r"^name:\s*(.+)$", fm, re.M)
    name = name_m.group(1).strip() if name_m else skill_path.name

    block = re.search(r"^description:\s*(>-?|\|-?)?\s*\n((?:[ \t]+.*\n?)+)", fm, re.M)
    if block:
        desc = " ".join(l.strip() for l in block.group(2).splitlines() if l.strip())
    else:
        one = re.search(r"^description:\s*(.+)$", fm, re.M)
        desc = one.group(1).strip() if one else ""
    if not desc:
        raise SystemExit(f"{md} 的 frontmatter 里没解析出 description")
    return name, desc


def _write_probe(skills_root: Path, name: str, description: str) -> None:
    """把一段 description 装成一个匿名的 project 级 skill。"""
    d = skills_root / name
    d.mkdir(parents=True, exist_ok=True)
    one_line = " ".join(description.split())
    (d / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: {json.dumps(one_line, ensure_ascii=False)}\n---\n\n"
        f"# {name}\n\nThis is a trigger-evaluation probe. Reply \"probe loaded\" and stop. "
        f"Do not run any tools.\n",
        encoding="utf-8",
    )


def run_single_query(query, description, timeout, root_base, model=None,
                     dump_dir=None, distractors=None, pass_env=()):
    """跑一条 query，返回是否触发了被测探针。

    每次调用都建一个独立的一次性 project root —— 见文件头第 3 条。

    distractors：其它 skill 的 description 列表，一起装进同一个环境当竞争者。
    不传的话环境里只有被测探针一个候选，模型"没得选"，
    负例容易假阳性——它会因为找不到别的工具而勉强用这个。
    ⚠️ 干扰项的**名字同样中性化**（alt-xxx）。若让干扰项挂真名（yandu-deck 之类）
    而探针挂中性名，模型光看名字就能认出干扰项，等于给对手开外挂，
    测出来的仍旧是名字不是 description —— 同文件头第 4 条一个道理。
    """
    unique_id = uuid.uuid4().hex[:8]
    # 中性名：不能带原 skill 名，否则测的是名字不是 description（第 4 条）
    probe_name = f"probe-{unique_id}"
    Path(root_base).mkdir(parents=True, exist_ok=True)
    project_root = tempfile.mkdtemp(prefix=f"trigeval-{unique_id}-", dir=root_base)
    skills_root = Path(project_root) / ".claude" / "skills"

    try:
        _write_probe(skills_root, probe_name, description)
        for i, alt_desc in enumerate(distractors or [], start=1):
            _write_probe(skills_root, f"alt-{unique_id}-{i}", alt_desc)

        cmd = [
            "claude", "-p", query,
            "--output-format", "stream-json",
            "--verbose",
            "--include-partial-messages",
            # 只加载 project 级设置，隔离掉已装的真 skill（第 1 条）
            "--setting-sources", "project",
            # 只关心触没触发：只开放判定要用的两个工具，不加载 MCP
            "--tools", "Skill,Read",
            "--strict-mcp-config",
        ]
        if model:
            cmd.extend(["--model", model])

        # 剥掉 CLAUDECODE（否则嵌套调用被守卫拦下），其余只放白名单变量
        env = build_env(pass_env)

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL,
                                cwd=project_root, env=env)
        buffer, pending, acc = "", None, ""
        dump_fh = None
        if dump_dir:
            Path(dump_dir).mkdir(parents=True, exist_ok=True)
            dump_fh = open(Path(dump_dir) / f"{unique_id}.jsonl", "w", encoding="utf-8")
            dump_fh.write(json.dumps({"_meta": {"query": query, "probe": probe_name}},
                                     ensure_ascii=False) + "\n")

        start = time.time()
        try:
            while time.time() - start < timeout:
                if proc.poll() is not None:
                    rest = proc.stdout.read()
                    if rest:
                        buffer += rest.decode("utf-8", errors="replace")
                    break
                ready, _, _ = select.select([proc.stdout], [], [], 1.0)
                if not ready:
                    continue
                chunk = os.read(proc.stdout.fileno(), 8192)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8", errors="replace")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    if dump_fh:
                        dump_fh.write(line + "\n")
                        dump_fh.flush()
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # 扫完整个流，命中即收工；只有等到 result 才判否（第 2 条）
                    etype = event.get("type")
                    if etype == "stream_event":
                        se = event.get("event", {})
                        st = se.get("type", "")
                        if st == "content_block_start":
                            cb = se.get("content_block", {})
                            if cb.get("type") == "tool_use":
                                pending = cb.get("name") if cb.get("name") in TOOL_HINT else None
                                acc = ""
                        elif st == "content_block_delta" and pending:
                            d = se.get("delta", {})
                            if d.get("type") == "input_json_delta":
                                acc += d.get("partial_json", "")
                                if probe_name in acc:
                                    return True
                        elif st == "content_block_stop":
                            if pending and probe_name in acc:
                                return True
                            pending, acc = None, ""

                    elif etype == "assistant":
                        for item in event.get("message", {}).get("content", []):
                            if item.get("type") != "tool_use":
                                continue
                            n, inp = item.get("name", ""), item.get("input", {})
                            if n == "Skill" and probe_name in str(inp.get("skill", "")):
                                return True
                            if n == "Read" and probe_name in str(inp.get("file_path", "")):
                                return True

                    elif etype == "result":
                        return False
        finally:
            if dump_fh:
                dump_fh.close()
            if proc.poll() is None:
                proc.kill()
                proc.wait()
        return False
    finally:
        shutil.rmtree(project_root, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(
        description="实测一段 skill description 的触发力（需要 claude CLI，会产生真实费用）")
    ap.add_argument("--eval-set", required=True, help="eval set JSON 路径")
    ap.add_argument("--skill-path", required=True, help="被测 skill 目录（含 SKILL.md）")
    ap.add_argument("--description-file", default=None,
                    help="改用这个文件的内容当 description（做 A/B 对照时用）")
    ap.add_argument("--project-root", default=None,
                    help="放一次性 project root 的父目录，默认系统临时目录")
    ap.add_argument("--label", default="", help="这一组的名字，只用于打印")
    ap.add_argument("--num-workers", type=int, default=4, help="并发数")
    ap.add_argument("--timeout", type=int, default=200, help="单条超时（秒）")
    ap.add_argument("--runs-per-query", type=int, default=1,
                    help="每条采样几次。默认 1 省钱；要稳定结论调 3，成本也 ×3")
    ap.add_argument("--trigger-threshold", type=float, default=0.5)
    ap.add_argument("--model", default=None, help="指定模型，默认跟随当前配置")
    ap.add_argument("--distractors", nargs="*", default=[], metavar="SKILL_DIR",
                    help="其它 skill 目录，把它们的 description 一起放进环境当竞争者。"
                         "不加的话环境里只有被测探针一个候选，负例容易假阳性")
    ap.add_argument("--dump-dir", default=None, help="保存原始流，出意外结果时翻它")
    ap.add_argument("--out", default=None, help="结果写到这个 JSON 文件")
    ap.add_argument("--json", action="store_true", help="只输出 JSON，不打中文报告")
    ap.add_argument("--pass-env", nargs="*", default=[], metavar="VAR",
                    help="额外放行给子进程的环境变量名（如 Bedrock/Vertex 所需）")
    ap.add_argument("--yes", action="store_true",
                    help="确认会产生真实费用，且被测 description 来源可信或已在沙箱中运行")
    args = ap.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text(encoding="utf-8"))
    if not eval_set:
        raise SystemExit("eval set 是空的")
    skill_path = Path(args.skill_path).expanduser()
    name, desc = parse_skill_md(skill_path)
    if args.description_file:
        desc = Path(args.description_file).read_text(encoding="utf-8").strip()

    distractor_descs = []
    for dp in args.distractors:
        _, dd = parse_skill_md(Path(dp).expanduser())
        distractor_descs.append(dd)

    root_base = args.project_root or tempfile.mkdtemp(prefix="trigeval-base-")
    owned_base = args.project_root is None
    label = args.label or name

    if not args.json:
        n_calls = len(eval_set) * args.runs_per_query
        comp = f" · 环境内 {len(distractor_descs)} 个竞争者" if distractor_descs else \
               " · ⚠️ 无竞争者，负例结果偏严格"
        print(f"[{label}] description {len(desc)} 字符 · "
              f"{len(eval_set)} 条 query × {args.runs_per_query} 次 = "
              f"{n_calls} 次调用（约 ${n_calls * 0.12:.1f}）{comp}", file=sys.stderr)

    if not args.yes:
        if not sys.stdin.isatty():
            raise SystemExit("非交互环境需加 --yes 确认费用与被测 description 来源")
        ans = input("会真实调用 claude -p 并产生费用；第三方 skill 请先放进沙箱。继续？[y/N] ")
        if ans.strip().lower() != "y":
            raise SystemExit("已取消")

    triggers, items = {}, {}
    try:
        with ProcessPoolExecutor(max_workers=args.num_workers) as ex:
            futs = {}
            for item in eval_set:
                for _ in range(args.runs_per_query):
                    f = ex.submit(run_single_query, item["query"], desc,
                                  args.timeout, root_base, args.model, args.dump_dir,
                                  distractor_descs, tuple(args.pass_env))
                    futs[f] = item
            for f in as_completed(futs):
                item = futs[f]
                q = item["query"]
                items[q] = item
                triggers.setdefault(q, [])
                try:
                    triggers[q].append(f.result())
                except Exception as e:
                    print(f"  警告：query 跑失败（按未触发计）：{e}", file=sys.stderr)
                    triggers[q].append(False)
    finally:
        if owned_base:
            shutil.rmtree(root_base, ignore_errors=True)

    results = []
    for q, tr in triggers.items():
        item = items[q]
        rate = sum(tr) / len(tr)
        should = item["should_trigger"]
        ok = rate >= args.trigger_threshold if should else rate < args.trigger_threshold
        results.append({
            "query": q, "should_trigger": should, "trigger_rate": rate,
            "triggers": sum(tr), "runs": len(tr), "pass": ok,
            "note": item.get("note", ""),
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)
    miss = [r for r in results if not r["pass"] and r["should_trigger"]]
    false_fire = [r for r in results if not r["pass"] and not r["should_trigger"]]

    out = {
        "label": label, "skill_name": name, "description": desc,
        "distractors": len(distractor_descs),
        "results": results,
        "summary": {
            "total": total, "passed": passed, "failed": total - passed,
            "score": round(passed / total * 100) if total else 0,
            "漏触发": len(miss), "误触发": len(false_fire),
        },
    }

    if not args.json:
        print(f"\n[{label}] 触发力 {out['summary']['score']} 分（{passed}/{total}）",
              file=sys.stderr)
        for r in sorted(results, key=lambda x: (not x["should_trigger"], x["query"])):
            flag = "✓" if r["pass"] else "✗"
            want = "该触发" if r["should_trigger"] else "不该触发"
            print(f"  {flag} [{want}] {r['triggers']}/{r['runs']}  {r['query'][:52]}",
                  file=sys.stderr)
        if miss:
            print(f"\n  漏触发 {len(miss)} 条 → description 没覆盖到这些说法，"
                  f"该用时不会被唤醒", file=sys.stderr)
        if false_fire:
            print(f"  误触发 {len(false_fire)} 条 → description 写太宽泛，"
                  f"抢了别的工具的活", file=sys.stderr)

    if args.out:
        Path(args.out).write_text(json.dumps(out, ensure_ascii=False, indent=2),
                                  encoding="utf-8")
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()

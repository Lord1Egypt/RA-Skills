"""
scan_and_plan.py - Orchestrator V4 通用扫描规划脚本

供 OpenClaw 主会话通过 exec 调用，输出 plan JSON 供后续 sessions_spawn 使用。

用法:
  # 分析模式（默认）
  python scan_and_plan.py --task "任务描述" --target-dir "/path/to/project" --output plan.json

  # 修复模式：接收问题列表 JSON，自动分组派发
  python scan_and_plan.py --mode fix --issues issues.json --target-dir "/path/to/project" --output plan.json

  # 自定义排除目录
  python scan_and_plan.py --task "..." --target-dir "..." --exclude ".next,dist,coverage"
"""

import argparse
import json
import sys
from pathlib import Path

# 导入 orchestrator
sys.path.insert(0, str(Path(__file__).parent))
from orchestrator_v4_acp import OrchestratorV4ACP, OrchestratorConfig


def plan_fix_mode(issues_path: str, target_dir: str, max_parallel: int) -> dict:
    """
    修复模式：读取问题列表 JSON，按依赖关系和文件关联自动分组。

    issues.json 格式：
    [
      {
        "id": "fix-1",
        "title": "密码改用 bcrypt",
        "priority": "P0",
        "files": ["lib/auth.ts", "app/api/auth/login/route.ts"],
        "description": "...",
        "depends_on": []
      },
      ...
    ]
    """
    with open(issues_path, "r", encoding="utf-8") as f:
        issues = json.load(f)

    if not isinstance(issues, list) or len(issues) == 0:
        print("ERROR: issues.json 为空或格式错误", file=sys.stderr)
        sys.exit(1)

    # 按优先级排序：P0 > P1 > P2 > 其他
    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    issues.sort(key=lambda x: priority_order.get(x.get("priority", "P2"), 99))

    # 分组策略：
    # 1. 有依赖关系的放后面
    # 2. 操作相同文件的合并到一个子任务
    # 3. 同优先级内按文件关联度合并

    groups = []  # [{issues: [...], files: set(), priority: "P0"}]

    for issue in issues:
        issue_files = set(issue.get("files", []))
        issue_deps = set(issue.get("depends_on", []))
        merged = False

        # 尝试合并到已有组（文件有交集 + 同优先级 + 无循环依赖）
        for group in groups:
            if (group["priority"] == issue.get("priority", "P2")
                    and issue_files & group["files"]
                    and not issue_deps & {i["id"] for i in group["issues"]}):
                group["issues"].append(issue)
                group["files"] |= issue_files
                merged = True
                break

        if not merged:
            groups.append({
                "issues": [issue],
                "files": issue_files,
                "priority": issue.get("priority", "P2"),
            })

    # 生成 subtasks
    subtasks = []
    for idx, group in enumerate(groups):
        issue_titles = [i["title"] for i in group["issues"]]
        issue_descs = "\n".join(
            f"### {i['title']}\n文件：{', '.join(i.get('files', []))}\n{i.get('description', '')}"
            for i in group["issues"]
        )
        file_list = ", ".join(sorted(group["files"]))
        file_count = len(group["files"])

        # 超时：按文件数和问题数估算
        issue_count = len(group["issues"])
        if file_count > 5 or issue_count > 3:
            timeout = 480
        elif file_count > 2 or issue_count > 1:
            timeout = 300
        else:
            timeout = 240

        subtasks.append({
            "id": f"fix-{idx}",
            "description": (
                f"修复以下 {issue_count} 个问题（{group['priority']}）：\n\n"
                f"{issue_descs}\n\n"
                f"涉及文件：{file_list}\n\n"
                f"⚠️ 约束：\n"
                f"- 先读取所有涉及的文件\n"
                f"- 确保修改后功能不受影响\n"
                f"- 列出需要用户手动执行的操作（如 npm install）"
            ),
            "files_to_read": sorted(group["files"]),
            "estimated_time_sec": timeout,
            "mode": "slow",
            "dependencies": [],
            "priority": group["priority"],
            "module_key": "+".join(issue_titles[:2]) + (f"+{len(issue_titles)-2}more" if len(issue_titles) > 2 else ""),
            "module_file_count": file_count,
            "issue_count": issue_count,
            "file_read_cap": min(file_count + 3, 15),
        })

    # 处理依赖关系：如果某个 issue depends_on 另一个 issue，对应的 subtask 也要有依赖
    issue_to_subtask = {}
    for st in subtasks:
        for issue in groups[int(st["id"].split("-")[1])]["issues"]:
            issue_to_subtask[issue["id"]] = st["id"]

    for st_idx, group in enumerate(groups):
        deps = set()
        for issue in group["issues"]:
            for dep_id in issue.get("depends_on", []):
                dep_st = issue_to_subtask.get(dep_id)
                if dep_st and dep_st != subtasks[st_idx]["id"]:
                    deps.add(dep_st)
        subtasks[st_idx]["dependencies"] = sorted(deps)

    # 策略
    has_deps = any(st["dependencies"] for st in subtasks)
    strategy = "mixed" if has_deps else "parallel"

    return {
        "complexity": 4,
        "duration": "medium",
        "request_type": "fix",
        "total_subtasks": len(subtasks),
        "estimated_time_sec": max(st["estimated_time_sec"] for st in subtasks) if subtasks else 0,
        "strategy": strategy,
        "subtasks": subtasks,
        "merge_strategy": "none",
        "notes": f"修复模式：{len(issues)} 个问题 → {len(subtasks)} 个子任务（{strategy}）",
        "is_fix_mode": True,
    }


def main():
    parser = argparse.ArgumentParser(description="Orchestrator V4 扫描规划")
    parser.add_argument("--task", required=False, help="任务描述（分析模式必填）")
    parser.add_argument("--target-dir", required=False, help="目标目录（可选）")
    parser.add_argument("--output", default="plan.json", help="输出文件路径（默认 plan.json）")
    parser.add_argument("--max-parallel", type=int, default=5, help="最大并发数（默认 5）")
    parser.add_argument("--mode", default="analyze", choices=["analyze", "fix"], help="模式：analyze（分析）或 fix（修复）")
    parser.add_argument("--issues", required=False, help="问题列表 JSON 文件路径（fix 模式必填）")
    parser.add_argument("--exclude", required=False, help="额外排除的目录，逗号分隔（如 .next,dist）")
    args = parser.parse_args()

    # 修复模式
    if args.mode == "fix":
        if not args.issues:
            print("ERROR: fix 模式需要 --issues 参数", file=sys.stderr)
            sys.exit(1)
        plan = plan_fix_mode(args.issues, args.target_dir or ".", args.max_parallel)
        scan = None
    else:
        # 分析模式
        if not args.task:
            print("ERROR: analyze 模式需要 --task 参数", file=sys.stderr)
            sys.exit(1)

        orch = OrchestratorV4ACP(OrchestratorConfig(resume_from_latest_checkpoint=False))

        # 扫描
        scan = None
        if args.target_dir:
            scan = orch.scan_task_scope(args.task, target_dir=args.target_dir)

        # 规划
        context = {"target_dir": args.target_dir} if args.target_dir else None
        plan = orch.plan_complex_task(args.task, context=context)

    # 输出摘要到 stdout
    print(f"mode: {args.mode}")
    print(f"total_subtasks: {plan['total_subtasks']}")
    print(f"strategy: {plan['strategy']}")
    print(f"is_large_project: {plan.get('is_large_project', False)}")
    if plan.get("is_fix_mode"):
        print(f"is_fix_mode: True")
    print()
    for st in plan["subtasks"]:
        mk = st.get("module_key", "N/A")
        fc = str(st.get("module_file_count", st.get("issue_count", "?")))
        timeout = st.get("estimated_time_sec", 300)
        cap = str(st.get("file_read_cap", "?"))
        deps = ",".join(st.get("dependencies", [])) or "none"
        print(f"  {st['id']:10s} | {mk:30s} | {fc:>4} files | {timeout:>4d}s | cap={cap} | deps={deps}")

    # 写入 JSON
    output = {
        "task": args.task or f"fix mode ({args.issues})",
        "target_dir": args.target_dir,
        "max_parallel": args.max_parallel,
        "mode": args.mode,
        "scan": scan,
        "plan": plan,
    }
    output_path = Path(args.output)
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nPlan saved to {output_path}")


if __name__ == "__main__":
    main()

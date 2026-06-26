#!/usr/bin/env python3
"""
情节分支器 - 情节图管理、分支点追踪、多线叙事
支持因果链、伏笔链、时间线的可视化与管理
"""

import os
import json
import argparse
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any


class PlotBrancher:
    """情节分支器 - 情节图管理与多线叙事"""

    def __init__(self, plot_path: str):
        """
        初始化情节分支器

        Args:
            plot_path: 情节图数据文件路径（JSON）
        """
        self.plot_path = Path(plot_path)
        self.plot_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self) -> Dict[str, Any]:
        """加载情节图数据"""
        if self.plot_path.exists():
            with open(self.plot_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "main_line": [],      # 主线情节节点
            "branches": {},       # 支线 {branch_id: [nodes]}
            "convergence": [],    # 汇合点
            "causal_chains": {},  # 因果链
            "metadata": {"created_at": datetime.now().isoformat()}
        }

    def _save(self):
        """保存情节图数据"""
        self.data["metadata"]["updated_at"] = datetime.now().isoformat()
        with open(self.plot_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def add_plot_node(self, title: str, chapter: int,
                      desc: str = "", node_type: str = "event",
                      characters: List[str] = None,
                      causes: List[str] = None,
                      leads_to: List[str] = None,
                      branch_id: str = None) -> str:
        """
        添加情节节点

        Args:
            title: 情节标题
            chapter: 章节编号
            desc: 情节描述
            node_type: 节点类型（event / decision / revelation / climax / resolution）
            characters: 涉及角色
            causes: 原因节点ID列表
            leads_to: 导致的节点ID列表
            branch_id: 支线ID（None则为主线）

        Returns:
            节点ID
        """
        node_id = f"plot_{uuid.uuid4().hex[:8]}"

        node = {
            "id": node_id,
            "title": title,
            "chapter": chapter,
            "desc": desc,
            "type": node_type,
            "characters": characters or [],
            "causes": causes or [],
            "leads_to": leads_to or [],
            "branch_id": branch_id,
            "status": "planned",  # planned / active / resolved
            "created_at": datetime.now().isoformat()
        }

        if branch_id:
            if branch_id not in self.data["branches"]:
                self.data["branches"][branch_id] = {"nodes": [], "title": "", "status": "active"}
            self.data["branches"][branch_id]["nodes"].append(node)
        else:
            self.data["main_line"].append(node)

        self._save()
        return node_id

    def create_branch(self, title: str, from_chapter: int,
                      from_node_id: str = None,
                      expected_convergence: int = None) -> str:
        """
        创建支线

        Args:
            title: 支线标题
            from_chapter: 分支起始章节
            from_node_id: 分支来源节点ID
            expected_convergence: 预期汇合章节

        Returns:
            支线ID
        """
        branch_id = f"branch_{uuid.uuid4().hex[:8]}"

        self.data["branches"][branch_id] = {
            "id": branch_id,
            "title": title,
            "from_chapter": from_chapter,
            "from_node_id": from_node_id,
            "expected_convergence": expected_convergence,
            "status": "active",
            "nodes": []
        }

        self._save()
        return branch_id

    def add_convergence(self, chapter: int, desc: str,
                        branches: List[str]) -> str:
        """
        添加汇合点

        Args:
            chapter: 汇合章节
            desc: 汇合描述
            branches: 汇合的支线ID列表

        Returns:
            汇合点ID
        """
        conv_id = f"conv_{uuid.uuid4().hex[:8]}"

        self.data["convergence"].append({
            "id": conv_id,
            "chapter": chapter,
            "desc": desc,
            "branches": branches,
            "created_at": datetime.now().isoformat()
        })

        # 更新支线状态
        for bid in branches:
            if bid in self.data["branches"]:
                self.data["branches"][bid]["status"] = "converged"

        self._save()
        return conv_id

    def get_timeline(self, chapter_start: int = None,
                     chapter_end: int = None) -> Dict[str, Any]:
        """
        获取情节时间线

        Args:
            chapter_start: 起始章节
            chapter_end: 结束章节

        Returns:
            时间线数据
        """
        all_nodes = []

        # 收集主线节点
        for node in self.data["main_line"]:
            all_nodes.append(("main", node))

        # 收集支线节点
        for bid, branch in self.data["branches"].items():
            for node in branch.get("nodes", []):
                all_nodes.append((bid, node))

        # 按章节排序
        if chapter_start is not None:
            all_nodes = [(b, n) for b, n in all_nodes if n["chapter"] >= chapter_start]
        if chapter_end is not None:
            all_nodes = [(b, n) for b, n in all_nodes if n["chapter"] <= chapter_end]

        all_nodes.sort(key=lambda x: x[1]["chapter"])

        return {
            "timeline": [
                {"branch": branch, **node}
                for branch, node in all_nodes
            ],
            "total_nodes": len(all_nodes)
        }

    def get_active_branches(self) -> List[Dict[str, Any]]:
        """获取活跃支线"""
        return [
            {"id": bid, **branch}
            for bid, branch in self.data["branches"].items()
            if branch.get("status") == "active"
        ]

    def get_branch_summary(self, branch_id: str) -> Optional[str]:
        """获取支线摘要"""
        if branch_id not in self.data["branches"]:
            return None

        branch = self.data["branches"][branch_id]
        nodes = branch.get("nodes", [])

        if not nodes:
            return f"支线 '{branch.get('title', branch_id)}' 暂无情节节点"

        lines = [f"## 支线: {branch.get('title', branch_id)}"]
        lines.append(f"- 状态: {branch.get('status', 'unknown')}")
        lines.append(f"- 起始: 第{branch.get('from_chapter', '?')}章")
        lines.append("")

        for node in nodes:
            status_marker = {"planned": "[计划]", "active": "[进行]", "resolved": "[完成]"}.get(node["status"], "")
            lines.append(f"- 第{node['chapter']}章 {status_marker} {node['title']}")
            if node.get("desc"):
                lines.append(f"  {node['desc']}")

        return "\n".join(lines)

    def check_branch_health(self, current_chapter: int) -> Dict[str, Any]:
        """
        检查支线健康度

        Args:
            current_chapter: 当前章节

        Returns:
            健康度报告
        """
        report = {
            "current_chapter": current_chapter,
            "issues": [],
            "warnings": [],
            "active_count": 0
        }

        for bid, branch in self.data["branches"].items():
            if branch.get("status") != "active":
                continue

            report["active_count"] += 1
            nodes = branch.get("nodes", [])

            # 支线太长未汇合
            from_chapter = branch.get("from_chapter", 0)
            if current_chapter - from_chapter > 30 and not branch.get("expected_convergence"):
                report["warnings"].append({
                    "branch_id": bid,
                    "title": branch.get("title", ""),
                    "type": "long_unresolved",
                    "message": f"支线 '{branch.get('title', bid)}' 已运行{current_chapter - from_chapter}章未汇合"
                })

            # 预期汇合已过
            expected = branch.get("expected_convergence")
            if expected and current_chapter > expected + 5:
                report["issues"].append({
                    "branch_id": bid,
                    "title": branch.get("title", ""),
                    "type": "overdue_convergence",
                    "expected_chapter": expected,
                    "message": f"支线 '{branch.get('title', bid)}' 预期第{expected}章汇合，已过期"
                })

        # 活跃支线过多
        if report["active_count"] > 5:
            report["warnings"].append({
                "type": "too_many_branches",
                "count": report["active_count"],
                "message": f"当前有{report['active_count']}条活跃支线，可能影响叙事聚焦"
            })

        return report

    def export_mermaid(self) -> str:
        """导出为 Mermaid 图"""
        lines = ["graph TD"]

        # 主线节点
        for node in self.data["main_line"]:
            safe_title = node["title"].replace('"', "'")
            lines.append(f"    {node['id']}[{safe_title}]")

        # 主线因果连线
        for node in self.data["main_line"]:
            for target in node.get("leads_to", []):
                lines.append(f"    {node['id']} --> {target}")

        # 支线
        for bid, branch in self.data["branches"].items():
            lines.append(f"    subgraph {bid}")
            lines.append(f"    direction TB")
            for node in branch.get("nodes", []):
                safe_title = node["title"].replace('"', "'")
                lines.append(f"        {node['id']}[{safe_title}]")
                for target in node.get("leads_to", []):
                    lines.append(f"        {node['id']} --> {target}")
            lines.append("    end")

        return "\n".join(lines)

    def get_stats(self) -> Dict[str, Any]:
        """获取情节图统计"""
        total_main = len(self.data["main_line"])
        total_branches = len(self.data["branches"])
        active_branches = len([b for b in self.data["branches"].values() if b.get("status") == "active"])
        total_convergence = len(self.data["convergence"])

        return {
            "main_line_nodes": total_main,
            "total_branches": total_branches,
            "active_branches": active_branches,
            "convergence_points": total_convergence
        }


    def close(self):
        """无资源需释放，保留接口一致性"""
        pass

    def execute_action(self, action: str, params: dict) -> dict:
        """统一调度入口"""
        if action == "add-node":
            title = params.get("title") or params.get("desc") or ""
            if not title:
                raise ValueError("add-node需要title或desc")
            chapter = int(params.get("chapter", 0))
            chars = params.get("characters")
            chars = chars.split(",") if isinstance(chars, str) else chars
            causes = params.get("causes")
            causes = causes.split(",") if isinstance(causes, str) else causes
            leads = params.get("leads_to")
            leads = leads.split(",") if isinstance(leads, str) else leads
            node_id = self.add_plot_node(
                title, chapter, params.get("desc", ""),
                params.get("node_type", "event"), chars, causes, leads,
                params.get("branch_id")
            )
            return {"node_id": node_id}

        elif action == "create-branch":
            title = params.get("title")
            if not title:
                raise ValueError("create-branch需要title")
            chapter = int(params.get("chapter", 0))
            bid = self.create_branch(
                title, chapter, params.get("from_node"),
                int(params["expected_convergence"]) if params.get("expected_convergence") else None
            )
            return {"branch_id": bid}

        elif action == "add-convergence":
            chapter = params.get("chapter")
            desc = params.get("desc")
            branches = params.get("branches")
            if not chapter or not desc or not branches:
                raise ValueError("add-convergence需要chapter, desc, branches")
            branch_list = branches.split(",") if isinstance(branches, str) else branches
            conv_id = self.add_convergence(int(chapter), desc, branch_list)
            return {"convergence_id": conv_id}

        elif action == "timeline":
            return self.get_timeline(
                int(params["chapter_start"]) if params.get("chapter_start") else None,
                int(params["chapter_end"]) if params.get("chapter_end") else None
            )

        elif action == "active-branches":
            return {"branches": self.get_active_branches()}

        elif action == "branch-summary":
            bid = params.get("branch_id")
            if not bid:
                raise ValueError("branch-summary需要branch_id")
            summary = self.get_branch_summary(bid)
            return {"summary": summary}

        elif action == "check-health":
            return self.check_branch_health(int(params.get("chapter", 1)))

        elif action == "mermaid":
            return {"mermaid": self.export_mermaid()}

        elif action == "stats":
            return self.get_stats()

        else:
            raise ValueError(f"未知操作: {action}")

def main():
    parser = argparse.ArgumentParser(description='情节分支器')
    parser.add_argument('--plot-path', required=True, help='情节图数据文件路径')
    parser.add_argument('--action', required=True,
                       choices=['add-node', 'create-branch', 'add-convergence',
                               'timeline', 'active-branches', 'branch-summary',
                               'check-health', 'mermaid', 'stats'],
                       help='操作类型')
    parser.add_argument('--title', help='标题')
    parser.add_argument('--chapter', type=int, help='章节编号')
    parser.add_argument('--desc', help='描述')
    parser.add_argument('--node-type', default='event',
                       choices=['event', 'decision', 'revelation', 'climax', 'resolution'])
    parser.add_argument('--characters', help='涉及角色（逗号分隔）')
    parser.add_argument('--causes', help='原因节点ID（逗号分隔）')
    parser.add_argument('--leads-to', help='后续节点ID（逗号分隔）')
    parser.add_argument('--branch-id', help='支线ID')
    parser.add_argument('--from-node', help='分支来源节点ID')
    parser.add_argument('--expected-convergence', type=int, help='预期汇合章节')
    parser.add_argument('--branches', help='汇合支线ID（逗号分隔）')
    parser.add_argument('--chapter-start', type=int, help='起始章节')
    parser.add_argument('--chapter-end', type=int, help='结束章节')
    parser.add_argument('--output', choices=['text', 'json'], default='json')

    args = parser.parse_args()
    brancher = PlotBrancher(args.plot_path)

    skip_keys = {"plot_path", "action", "output"}
    params = {k: v for k, v in vars(args).items()
              if v is not None and k not in skip_keys and not k.startswith('_')}
    result = brancher.execute_action(args.action, params)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()

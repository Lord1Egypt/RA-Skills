#!/usr/bin/env python3
"""
MoA 前置红队 CLI
===================
在专家产出前进行结构化风险扫描（架构/安全/合规/成本），
复用宿主模型，仅切换 System Prompt，不增加额外 LLM 调用成本。

用法:
  python scripts/red_team_cli.py run --task "..." --decomposition "..." [--teams arch,sec,comp,cost]
  python scripts/red_team_cli.py list-teams
  python scripts/red_team_cli.py prompt --team arch
"""

import argparse
import json
import sys
from typing import List, Optional


# ============================================================
# 红队 System Prompt 模板
# ============================================================

RED_TEAM_PROMPTS = {
    "arch": {
        "name": "架构红队",
        "description": "单点故障、扩展性瓶颈、数据一致性、观测盲区",
        "prompt": """你是一名架构红队审查专家。你的职责是在项目早期识别架构层面的风险。

请基于以下任务描述和任务分解，输出结构化的风险清单。

任务描述: {task}

任务分解:
{decomposition}

请按以下 XML 格式输出风险清单：
<pre_risk>
  <risk type="arch" severity="致命|重要|次要">
    <title>简述风险</title>
    <description>详细场景与触发条件</description>
    <affected_subtasks>["subtask-1", "subtask-2"]</affected_subtasks>
    <mitigation_hint>建议缓解方向</mitigation_hint>
  </risk>
  <risk type="arch" severity="致命|重要|次要">
    ...
  </risk>
</pre_risk>

关注点：
- 单点故障：是否存在无冗余的关键组件？
- 扩展性：是否有 O(n) 或更差的瓶颈路径？
- 数据一致性：最终一致性是否被当作强一致性使用？
- 观测盲区：关键指标是否可观测？
- 耦合度：子任务间的依赖是否合理？
- 边界溢出：是否考虑了流量尖峰、超时、重试？

只输出 XML，不要包含其他解释。""",
    },
    "sec": {
        "name": "安全红队",
        "description": "STRIDE 威胁建模、攻击面、供应链、零信任缺口",
        "prompt": """你是一名安全红队审查专家。你的职责是在项目早期识别安全层面的风险。

请基于以下任务描述和任务分解，输出结构化的风险清单。

任务描述: {task}

任务分解:
{decomposition}

请按以下 XML 格式输出风险清单：
<pre_risk>
  <risk type="sec" severity="致命|重要|次要">
    <title>简述风险</title>
    <description>详细场景与触发条件</description>
    <affected_subtasks>["subtask-1"]</affected_subtasks>
    <mitigation_hint>建议缓解方向</mitigation_hint>
  </risk>
</pre_risk>

关注点（STRIDE 框架）：
- Spoofing（冒充）：身份验证是否充分？
- Tampering（篡改）：数据完整性保护是否到位？
- Repudiation（抵赖）：审计日志是否完备？
- Information Disclosure（信息泄露）：敏感数据是否加密？
- Denial of Service（拒绝服务）：是否存在资源耗尽的风险？
- Elevation of Privilege（权限提升）：权限控制是否最小化？

额外关注：
- 供应链安全：依赖的第三方库是否有已知漏洞？
- 零信任：是否假设网络已被攻破？

只输出 XML，不要包含其他解释。""",
    },
    "comp": {
        "name": "合规红队",
        "description": "GDPR/PCI-DSS/等保/行业法规映射、证据链要求",
        "prompt": """你是一名合规红队审查专家。你的职责是在项目早期识别合规层面的风险。

请基于以下任务描述和任务分解，输出结构化的风险清单。

任务描述: {task}

任务分解:
{decomposition}

请按以下 XML 格式输出风险清单：
<pre_risk>
  <risk type="comp" severity="致命|重要|次要">
    <title>简述风险</title>
    <description>详细场景与触发条件</description>
    <affected_subtasks>["subtask-1"]</affected_subtasks>
    <mitigation_hint>建议缓解方向</mitigation_hint>
    <evidence_ref>GDPR-Art32 / PCI-DSS-3.4</evidence_ref>
  </risk>
</pre_risk>

关注点：
- 数据保护：是否涉及个人数据？处理是否有法律依据？
- 数据驻留：数据存储位置是否符合法规要求？
- 审计轨迹：是否满足可审计性要求？
- 跨境传输：数据跨境是否有合规机制？
- 行业法规：是否涉及金融/医疗/儿童等特殊行业法规？
- 留存期限：数据保留和删除策略是否合规？

只输出 XML，不要包含其他解释。""",
    },
    "cost": {
        "name": "成本红队",
        "description": "Token/延迟/云资源上下界、冷启动、并发成本曲线",
        "prompt": """你是一名成本红队审查专家。你的职责是在项目早期识别成本层面的风险。

请基于以下任务描述和任务分解，输出结构化的风险清单。

任务描述: {task}

任务分解:
{decomposition}

请按以下 XML 格式输出风险清单：
<pre_risk>
  <risk type="cost" severity="致命|重要|次要">
    <title>简述风险</title>
    <description>详细场景与触发条件</description>
    <affected_subtasks>["subtask-1"]</affected_subtasks>
    <mitigation_hint>建议缓解方向</mitigation_hint>
  </risk>
</pre_risk>

关注点：
- Token 成本：是否有不必要的长上下文消耗？
- 延迟成本：是否存在串行化瓶颈导致用户等待？
- 基础设施：云资源是否被过度配置？
- 冷启动：是否有可预见的冷启动成本尖峰？
- 并发：并发场景下成本是否线性增长？
- 存储：数据存储成本是否被低估？
- 带宽：数据传输成本是否被考虑？

只输出 XML，不要包含其他解释。""",
    },
}


# ============================================================
# 红队运行器
# ============================================================

class RedTeamRunner:
    """前置红队运行器 —— 生成结构化风险清单"""

    TEAM_MAP = {
        "arch": "架构红队",
        "sec": "安全红队",
        "comp": "合规红队",
        "cost": "成本红队",
    }

    @classmethod
    def list_teams(cls) -> dict:
        """列出所有可用红队"""
        teams = {}
        for key, info in RED_TEAM_PROMPTS.items():
            teams[key] = {
                "name": info["name"],
                "description": info["description"],
            }
        return teams

    @classmethod
    def get_prompt(cls, team: str, task: str, decomposition: str) -> str:
        """获取指定红队的 System Prompt（已填充任务和分解）"""
        if team not in RED_TEAM_PROMPTS:
            raise ValueError(f"未知红队: {team}，可选: {', '.join(RED_TEAM_PROMPTS.keys())}")
        return RED_TEAM_PROMPTS[team]["prompt"].format(
            task=task.strip(),
            decomposition=decomposition.strip(),
        )

    @classmethod
    def run(cls, task: str, decomposition: str,
            enabled_teams: Optional[List[str]] = None) -> dict:
        """运行红队扫描，输出 Prompt 模板供宿主模型调用"""
        if enabled_teams is None:
            enabled_teams = list(RED_TEAM_PROMPTS.keys())

        results = {}
        for team in enabled_teams:
            if team not in RED_TEAM_PROMPTS:
                continue
            prompt = cls.get_prompt(team, task, decomposition)
            results[team] = {
                "name": RED_TEAM_PROMPTS[team]["name"],
                "system_prompt": prompt,
                "expected_output_format": "XML <pre_risk>",
            }

        return {
            "task": task,
            "enabled_teams": enabled_teams,
            "team_count": len(results),
            "instructions": "将上述 system_prompt 作为红队指令发送给宿主模型，获取 XML 格式的风险清单后注入各 <subtask> 的 <pre_risk> 字段。",
            "teams": results,
        }


# ============================================================
# CLI 入口
# ============================================================

def cmd_run(args):
    """run 子命令"""
    teams = args.teams.split(",") if args.teams else None
    result = RedTeamRunner.run(
        task=args.task,
        decomposition=args.decomposition,
        enabled_teams=teams,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_list_teams(args):
    """list-teams 子命令"""
    teams = RedTeamRunner.list_teams()
    print(json.dumps(teams, ensure_ascii=False, indent=2))


def cmd_prompt(args):
    """prompt 子命令"""
    prompt = RedTeamRunner.get_prompt(args.team, args.task, args.decomposition)
    print(prompt)


def main():
    parser = argparse.ArgumentParser(
        description="MoA 前置红队 —— 在专家产出前进行结构化风险扫描",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 列出所有可用红队
  python scripts/red_team_cli.py list-teams

  # 运行全量红队扫描（输出 Prompt 模板）
  python scripts/red_team_cli.py run --task "设计支付系统" --decomposition "$(cat decomposition.txt)"

  # 仅运行架构+安全红队
  python scripts/red_team_cli.py run --task "..." --decomposition "..." --teams arch,sec

  # 获取单个红队的 Prompt
  python scripts/red_team_cli.py prompt --team arch --task "..." --decomposition "..."
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # run
    p_run = subparsers.add_parser("run", help="运行红队扫描")
    p_run.add_argument("--task", required=True, help="任务描述")
    p_run.add_argument("--decomposition", required=True, help="任务分解（Phase 1 产出）")
    p_run.add_argument("--teams", help="红队列表（逗号分隔，默认全开）")

    # list-teams
    subparsers.add_parser("list-teams", help="列出所有可用红队")

    # prompt
    p_prompt = subparsers.add_parser("prompt", help="获取单个红队 Prompt")
    p_prompt.add_argument("--team", required=True, choices=list(RED_TEAM_PROMPTS.keys()), help="红队类型")
    p_prompt.add_argument("--task", required=True, help="任务描述")
    p_prompt.add_argument("--decomposition", required=True, help="任务分解")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd_map = {
        "run": cmd_run,
        "list-teams": cmd_list_teams,
        "prompt": cmd_prompt,
    }
    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
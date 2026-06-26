#!/usr/bin/env python3
"""
Context Transfer Generator
自动生成模型切换时的上下文传递文档
"""

import argparse
import json
from datetime import datetime

def generate_transfer(
    project_name: str,
    current_status: str,
    completed: list,
    in_progress: list,
    pending: list,
    blockers: list,
    key_decisions: list,
    constraints: list,
    file_paths: list,
    api_tools: list,
    team_roles: dict,
    next_steps: list,
    warnings: list,
    output_file: str = "context_transfer.md"
):
    """生成上下文传递文档"""
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    content = f"""## CONTEXT_TRANSFER

**项目**: {project_name}
**时间**: {now}
**状态**: {current_status}

---

### 📍 当前进度

| 类型 | 内容 |
|------|------|
| ✅ 已完成 | {', '.join(completed) if completed else '无'} |
| 🔄 进行中 | {', '.join(in_progress) if in_progress else '无'} |
| ⏳ 待处理 | {', '.join(pending) if pending else '无'} |
| 🚧 遇阻 | {', '.join(blockers) if blockers else '无'} |

---

### 📌 关键信息

**核心目标**  
{key_decisions[0] if key_decisions else '（请填写）'}

**重要决策**  
{chr(10).join(f"- {d}" for d in key_decisions) if key_decisions else '- （无）'}

**约束条件**  
{chr(10).join(f"- {c}" for c in constraints) if constraints else '- （无）'}

**文件路径**  
{chr(10).join(f"- `{p}`" for p in file_paths) if file_paths else '- （无）'}

**API/工具**  
{chr(10).join(f"- {t}" for t in api_tools) if api_tools else '- （无）'}

---

### 👥 团队角色

{chr(10).join(f"- **{agent}**：{role}" for agent, role in team_roles.items()) if team_roles else '- （无）'}

---

### 🎯 下一步（优先级排序）

{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(next_steps)) if next_steps else '- （无）'}

---

### ⚠️ 注意事项

{chr(10).join(f"- ⚠️ {w}" for w in warnings) if warnings else '- （无）'}

---

*此文档由 model-context-transfer 技能自动生成*
*生成时间：{now}*
"""

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 上下文传递文档已生成: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description='生成上下文传递文档')
    parser.add_argument('--project', '-p', required=True, help='项目名称')
    parser.add_argument('--status', '-s', default='进行中', help='当前状态')
    parser.add_argument('--completed', '-c', nargs='*', default=[], help='已完成事项')
    parser.add_argument('--progress', '-i', nargs='*', default=[], help='进行中事项')
    parser.add_argument('--pending', nargs='*', default=[], help='待处理事项')
    parser.add_argument('--blockers', '-b', nargs='*', default=[], help='阻碍事项')
    parser.add_argument('--decisions', '-d', nargs='*', default=[], help='重要决策')
    parser.add_argument('--constraints', nargs='*', default=[], help='约束条件')
    parser.add_argument('--files', '-f', nargs='*', default=[], help='文件路径')
    parser.add_argument('--tools', '-t', nargs='*', default=[], help='API/工具')
    parser.add_argument('--team', type=json.loads, default={}, help='团队角色 JSON格式')
    parser.add_argument('--steps', nargs='*', default=[], help='下一步行动')
    parser.add_argument('--warnings', '-w', nargs='*', default=[], help='注意事项')
    parser.add_argument('--output', '-o', default='context_transfer.md', help='输出文件')
    
    args = parser.parse_args()
    
    generate_transfer(
        project_name=args.project,
        current_status=args.status,
        completed=args.completed,
        in_progress=args.progress,
        pending=args.pending,
        blockers=args.blockers,
        key_decisions=args.decisions,
        constraints=args.constraints,
        file_paths=args.files,
        api_tools=args.tools,
        team_roles=args.team,
        next_steps=args.steps,
        warnings=args.warnings,
        output_file=args.output
    )

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
AI Agent生产线 - 把技能转化为可部署的Agent配置
输入技能名，输出 agent-config.json + workflow.md + deploy.sh
"""

import os, sys, json, datetime

BASE = "/root/.openclaw/workspace/skills"

def read_skill(name):
    """读取技能信息"""
    path = os.path.join(BASE, name, "SKILL.md")
    meta_path = os.path.join(BASE, name, "_meta.json")
    
    if not os.path.exists(path):
        return None
    
    with open(path, 'r', errors='ignore') as f:
        content = f.read()
    
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path) as f:
            try:
                meta = json.load(f)
            except:
                pass
    
    # 提取描述和依赖
    desc = ""
    deps = []
    for line in content.split("\n"):
        if line.startswith("description:"):
            desc = line.replace("description:", "").strip().strip('"').strip("'")
        if "requires:" in line and "skills:" in line:
            # 下一行可能有依赖列表
            pass
        if line.strip().startswith('- "') or line.strip().startswith("- '"):
            potential_dep = line.strip().strip('-').strip('"').strip("'").strip()
            if potential_dep and not potential_dep.startswith("#"):
                deps.append(potential_dep)
    
    return {"name": name, "desc": desc, "meta": meta, "deps": deps, "content": content}

def generate_agent_config(skill, output_dir):
    """生成Agent配置"""
    config = {
        "agent": {
            "name": skill["name"],
            "version": "1.0.0",
            "description": skill["desc"],
            "author": skill["meta"].get("author", "智美人团队"),
            "created": datetime.datetime.now().strftime("%Y-%m-%d"),
            "runtime": "openclaw",
            "model": "default",
            "skills": [skill["name"]] + skill["deps"]
        },
        "workflow": {
            "trigger": "user_request",
            "steps": [
                {
                    "name": "analyze",
                    "description": "分析用户需求",
                    "model": "default"
                },
                {
                    "name": "execute",
                    "description": "执行核心任务",
                    "skills": skill["deps"]
                },
                {
                    "name": "output",
                    "description": "格式化输出结果",
                    "format": "auto"
                }
            ]
        },
        "deploy": {
            "platform": "clawhub",
            "config": {
                "publish": True,
                "visibility": "public",
                "pricing": "free"
            }
        }
    }
    
    path = os.path.join(output_dir, "agent-config.json")
    with open(path, "w") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    return path

def generate_workflow(skill, output_dir):
    """生成工作流文档"""
    now = datetime.datetime.now()
    wf = f"""# {skill['name']} Agent 工作流

> 自动生成于 {now.strftime('%Y-%m-%d %H:%M')}
> 基于技能: {skill['name']}

## 工作流

```
用户输入 → 需求分析 → 技能调用 → 结果输出
```

## 触发条件

```
自然语言描述：{skill['desc'][:60]}...
```

## 依赖技能

"""
    for d in skill["deps"]:
        wf += f"- {d}\n"
    
    wf += f"""
## 执行步骤

### Step 1: 需求分析
- 模型: default
- 输入: 用户自然语言
- 输出: 结构化的任务参数

### Step 2: 技能执行
- 并行调用依赖技能
- 等待所有结果返回

### Step 3: 结果整合
- 合并多个技能的输出
- 格式化呈现给用户

## 部署配置

```json
{{
  "agent": "{skill['name']}",
  "runtime": "openclaw"
}}
```
"""
    
    path = os.path.join(output_dir, "workflow.md")
    with open(path, "w") as f:
        f.write(wf)
    return path

def generate_deploy_script(skill, output_dir):
    """生成部署脚本"""
    script = f"""#!/bin/bash
# {skill['name']} Agent 部署脚本
# 生成于 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

echo "📦 部署 {skill['name']} Agent..."
echo ""

# 1. 验证依赖
echo "Step 1: 验证依赖技能..."
"""

    for d in skill["deps"]:
        exists = os.path.isdir(os.path.join(BASE, d))
        mark = "✅" if exists else "❌"
        script += f'echo "  {d}: {mark}"\n'
    
    script += f"""
# 2. 生成配置文件
echo "Step 2: 生成 agent-config.json..."
# 已生成

# 3. 准备发布
echo "Step 3: 准备发布到ClawHub..."

# 4. 发布
echo ""
echo "✅ {skill['name']} Agent 部署就绪!"
echo "运行 clawhub publish 发布到 ClawHub"
"""
    
    path = os.path.join(output_dir, "deploy.sh")
    with open(path, "w") as f:
        f.write(script)
    os.chmod(path, 0o755)
    return path

def main():
    if len(sys.argv) < 2:
        print("AI Agent生产线")
        print()
        print("用法: python3 agent-line.py <技能名>")
        print("示例: python3 agent-line.py ecom-intel")
        print("       python3 agent-line.py --list")
        sys.exit(1)
    
    if sys.argv[1] == "--list":
        print("可部署的Agent技能：")
        for name in sorted(os.listdir(BASE)):
            if os.path.exists(os.path.join(BASE, name, "SKILL.md")):
                skill = read_skill(name)
                if skill:
                    print(f"  📦 {name}: {skill['desc'][:60]}")
        return
    
    name = sys.argv[1]
    skill = read_skill(name)
    if not skill:
        print(f"❌ 技能 '{name}' 不存在")
        sys.exit(1)
    
    output_dir = os.path.join(BASE, name)
    
    print(f"🔨 AI Agent生产线: {name}")
    print(f"   描述: {skill['desc'][:60]}")
    print(f"   依赖: {', '.join(skill['deps'][:5])}")
    print()
    
    config_path = generate_agent_config(skill, output_dir)
    wf_path = generate_workflow(skill, output_dir)
    deploy_path = generate_deploy_script(skill, output_dir)
    
    print("✅ 生产线完成!")
    print(f"   📄 {config_path}")
    print(f"   📄 {wf_path}")
    print(f"   📄 {deploy_path}")
    print()
    print(f"一键部署运行: bash {deploy_path}")

if __name__ == "__main__":
    main()

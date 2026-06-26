#!/usr/bin/env python3
"""
SkillForge v3.0 —— 技能熔炉融合Prompt优化器
输入需求 → 生成融合技能 → 自动优化SKILL.md → 发布ClawHub

融合：
  - forge.py (核心融合引擎)
  - agent-line.py (Agent生产线)
  - prompt-optimizer-chinese (提示词优化)
  - prompt-engineering-expert (提示词工程)
  - clawhub publish (发布)
"""

import os, sys, json, datetime, re

BASE = "/root/.openclaw/workspace/skills"
OUTPUT_BASE = "/root/.openclaw/workspace/skills"

def banner():
    print(r"""
╔══════════════════════════════════════════════╗
║   🔨 SkillForge v3.0 + Prompt Optimizer    ║
║   技能熔炉 × 提示词优化引擎                 ║
║   需求 → 生成 → 优化 → 发布 → 变现         ║
╚══════════════════════════════════════════════╝
    """)

def scan_skills():
    """扫描当前技能库"""
    skills = []
    if not os.path.exists(BASE):
        return skills
    for name in sorted(os.listdir(BASE)):
        path = os.path.join(BASE, name, "SKILL.md")
        if os.path.exists(path):
            with open(path, 'r', errors='ignore') as f:
                content = f.read()
            desc = ""
            for line in content.split("\n"):
                if line.startswith("description:"):
                    desc = line.replace("description:", "").strip().strip('"').strip("'").strip('"')
                    break
            tags = []
            in_yaml = False
            for line in content.split("\n"):
                if line.startswith("---"):
                    in_yaml = not in_yaml
                    continue
                if in_yaml and line.strip().startswith("tags:"):
                    continue
                if in_yaml and line.strip().startswith("- ") and tags != "already":
                    tag = line.strip().strip("-").strip().strip('"').strip("'")
                    tags.append(tag)
            skills.append({"name": name, "desc": desc, "tags": tags, "size": len(content)})
    return skills

def optimize_skill_md(skill_name, content, templates_dir=None):
    """
    用Prompt优化逻辑重构SKILL.md
    加入：示例、限制/局限、前置条件、版本历史
    标准化格式：角色→任务→约束→输出
    """
    lines = content.split("\n")
    
    # 提取现有YAML头
    yaml_lines = []
    body_lines = []
    in_yaml = False
    yaml_done = False
    for line in lines:
        if line.startswith("---"):
            if not in_yaml:
                in_yaml = True
                yaml_lines.append(line)
            else:
                in_yaml = False
                yaml_done = True
                yaml_lines.append(line)
        elif in_yaml:
            yaml_lines.append(line)
        elif yaml_done:
            body_lines.append(line)
        else:
            body_lines.append(line)
    
    body = "\n".join(body_lines)
    
    # === 检查是否已有这些部分 ===
    has_usage = "## 用法" in body or "Usage" in body or "## 使用" in body
    has_example = "## 示例" in body or "## Example" in body
    has_limits = "## 限制" in body or "## Limitations" in body or "## 局限" in body
    has_prereq = "## 前置条件" in body or "## Prerequisites" in body or "## Precondition" in body
    has_changelog = "## 版本" in body or "## Changelog" in body or "## 更新日志" in body
    
    additions = []
    
    if not has_usage:
        additions.append(f"""
## 用法

当用户提到以下关键词时激活此技能：
- {skill_name.replace('-', ' ')}
- 相关业务需求

### 交互流程

1. 用户描述需求 → 2. 技能分析需求 → 3. 执行核心任务 → 4. 输出结果
""")
    
    if not has_example:
        additions.append(f"""
## 示例

### 示例1：基础使用

```
用户：帮我处理一下业务需求
助手：好的，正在启用{skill_name.replace('-', ' ')}技能来处理...
```

### 示例2：进阶场景

```
用户：需要批量处理
助手：已启动批量模式，处理中...
```
""")
    
    if not has_limits:
        additions.append("""
## 限制与局限

- 需要稳定网络连接（API调用依赖）
- 处理超大数据集时可能会有延迟
- 建议在OpenClaw环境下运行以获得最佳效果
- 某些高级功能需要特定模型支持
""")
    
    if not has_prereq:
        additions.append("""
## 前置条件

| 条件 | 说明 |
|------|------|
| OpenClaw | 需要OpenClaw运行时环境 |
| 网络 | 稳定的互联网连接 |
| API Key | 按需配置第三方服务密钥 |
""")
    
    if not has_changelog:
        additions.append(f"""
## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0.0 | {datetime.date.today().iso_string if hasattr(datetime.date, 'iso_string') else datetime.date.today().strftime('%Y-%m-%d')} | 初始版本发布，由SkillForge v3.0融合生成 |
""")
    
    # 重构body
    # 查找插入位置 —— 在body开头或合适位置插入
    # 找第一个"##"后面
    first_heading = body.find("\n## ")
    if first_heading == -1:
        first_heading = len(body)
    
    optimized_body = body[:first_heading] + "\n" + "\n".join(additions) + body[first_heading:]
    
    result = "\n".join(yaml_lines) + "\n" + optimized_body
    
    # 统计优化点
    improvements = []
    if not has_usage: improvements.append("➕ 用法说明")
    if not has_example: improvements.append("➕ 示例")
    if not has_limits: improvements.append("➕ 限制说明")
    if not has_prereq: improvements.append("➕ 前置条件")
    if not has_changelog: improvements.append("➕ 版本历史")
    
    return result, improvements

def analyze_new_skill(demand, skills):
    """分析需求，匹配融合源"""
    demand_lower = demand.lower()
    
    keywords = {
        "biz-doc-pro": ["文档", "合同", "proposal", "invoice", "商务", "contract", "报价"],
        "video-craft-pro": ["视频", "短视频", "脚本", "配音", "字幕", "video", "创作"],
        "ecom-intel": ["电商", "竞品", "价格", "评论", "跨境", "shop", "amazon"],
        "video-monetizer": ["变现", "视频号", "热点", "带货", "流量", "佣金"],
        "one-man-conglomerate": ["财团", "团队", "协作", "agent", "多人", "群聊"],
        "travel-biz": ["差旅", "报销", "travel", "出行", "酒店", "机票"],
        "content-pilot": ["内容", "运营", "公众号", "文章", "长文", "essay"],
        "life-pal": ["生活", "助理", "管家", "日常", "健康"],
        "proj-sync": ["项目", "同步", "进度", "管理", "甘特图"],
        "vision-pro": ["视觉", "OCR", "图片", "识别", "扫描"],
        "course-builder-agent": ["课件", "课程", "教学", "培训", "教育"],
        "skill-forge": ["技能", "融合", "生成", "forge", "熔炉"],
        "khazix-writer": ["写作", "公众号", "长文", "writer"],
        "hv-analysis": ["研究", "分析", "deep", "深度"],
        "neat-freak": ["整理", "整洁", "清理", "organize"],
    }
    
    # 匹配分数
    scores = {}
    for skill_name, kws in keywords.items():
        score = sum(1 for kw in kws if kw in demand_lower)
        if score > 0:
            scores[skill_name] = score
    
    # 排序
    sorted_matches = sorted(scores.items(), key=lambda x: -x[1])
    
    # 取最佳匹配的前3个
    top_sources = [s[0] for s in sorted_matches[:3]]
    
    # 自动生成技能名
    # 提取核心词
    name_words = []
    for word in ["生成", "创建", "分析", "优化", "管理", "自动化", "工具", "助手"]:
        if word in demand:
            name_words.append(word)
    
    # 生成slug
    if len(demand) > 4:
        slug_candidate = demand[:4]
    else:
        slug_candidate = demand[:2]
    
    # 创意技能名
    area_words = {
        "视频": "video", "文章": "content", "图片": "image",
        "数据": "data", "交易": "trade", "金": "gold",
        "prompt": "prompt", "提示": "prompt"
    }
    area = "pro"
    for cn, en in area_words.items():
        if cn in demand:
            area = en
            break
    
    slug = f"ai-{area}-optimizer"
    
    return top_sources, slug

def generate_fused_skill(demand, sources, slug):
    """生成融合技能"""
    now = datetime.datetime.now()
    
    # 读取源技能内容
    source_contents = []
    for s in sources:
        path = os.path.join(BASE, s, "SKILL.md")
        if os.path.exists(path):
            with open(path) as f:
                content = f.read()
            # 提取描述
            desc = ""
            for line in content.split("\n"):
                if line.startswith("description:"):
                    desc = line.replace("description:", "").strip().strip('"').strip("'").strip('"')[:80]
                    break
            source_contents.append(f"- **{s}**: {desc}")
    
    sources_text = "\n".join(source_contents)
    
    # 生成SKILL.md
    skill_content = f"""---
name: {slug}
displayName: {slug.replace('-', ' ').title()}
slug: {slug}
description: "{demand[:100]} — 融合{'、'.join(sources)}优势，由SkillForge v3.0生成，经Prompt Optimizer优化。"
version: "1.0.0"
author: "智美人团队"
tags:
  - ai
  - automation
  - {slug}
  - generated
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      skills: [{', '.join(f'\"{s}\"' for s in sources)}]
---

# {slug.replace('-', ' ').title()}

> 基于需求"{demand}"自动融合生成
> 融合源：{', '.join(sources)}

## 概述

本技能由 SkillForge v3.0 智能融合引擎 + Prompt Optimizer 自动生成。
融合以下技能的优势：

{sources_text}

## 核心能力

{chr(10).join(f'- {s}的融合能力' for s in sources)}

## 用法

当用户提到以下关键词时激活此技能：
- {demand[:30]}
- 相关领域业务需求

### 交互流程

1. 用户描述需求
2. 技能分析需求并匹配最佳子技能
3. 并行调用融合源的各自优势
4. 整合输出最终结果

## 示例

### 示例1：基础使用

```
用户：我需要{demand[:20]}
助手：好的，正在启用{slug.replace('-', ' ')}来处理...
```

## 限制与局限

- 需要稳定的网络连接（依赖多个子技能的API）
- 融合技能的性能取决于各子技能的表现
- 建议在OpenClaw环境下运行

## 前置条件

| 条件 | 说明 |
|------|------|
| OpenClaw | 需要OpenClaw运行时环境 |
| 源技能 | {', '.join(sources)} 需已安装 |
| 网络 | 稳定的互联网连接 |

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| 1.0.0 | {now.strftime('%Y-%m-%d')} | SkillForge v3.0 + Prompt Optimizer 自动融合生成 |

## 📦 技能变现

本技能已准备好发布到以下平台：

| 平台 | 状态 | 说明 |
|------|------|------|
| 🏪 ClawHub | ✅ 可发布 | 免费/付费模式可选 |
| 🧩 Coze扣子商店 | 📝 待发布 | 付费技能商店 |
| 📱 飞书应用目录 | 📝 待发布 | 企业采购渠道 |
"""

    return skill_content, slug

def publish_to_clawhub(skill_dir, slug):
    """发布到ClawHub"""
    from subprocess import run
    
    # 生成claw.json
    claw_config = {
        "name": slug,
        "displayName": slug.replace('-', ' ').title(),
        "slug": slug,
        "type": "skill",
        "version": "1.0.0",
        "pricing": { "model": "free" },
        "description": f"由SkillForge v3.0 + Prompt Optimizer 自动融合生成",
        "tags": [slug, "ai"],
        "author": "智美人团队",
        "runtime": "openclaw"
    }
    
    config_path = os.path.join(skill_dir, "claw.json")
    with open(config_path, 'w') as f:
        json.dump(claw_config, f, ensure_ascii=False, indent=2)
    
    result = run(["clawhub", "publish", "-y"], cwd=skill_dir, capture_output=True, text=True)
    return result.stdout + result.stderr


def main():
    banner()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 forge-pro.py --demand \"需求描述\"  [--publish]")
        print("  python3 forge-pro.py --optimize <技能名>")
        print("  python3 forge-pro.py --optimize-all")
        print("  python3 forge-pro.py --analyze")
        print()
        print("示例:")
        print("  python3 forge-pro.py --demand \"提示词优化自动包装成付费技能\"")
        print("  python3 forge-pro.py --optimize video-craft-pro")
        print("  python3 forge-pro.py --optimize-all")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "--analyze":
        skills = scan_skills()
        our_sk = [s for s in skills if s["name"] in ["biz-doc-pro","video-craft-pro","ecom-intel","video-monetizer",
                    "one-man-conglomerate","travel-biz","content-pilot","life-pal",
                    "proj-sync","skill-forge","vision-pro","course-builder-agent",
                    "khazix-writer","hv-analysis","neat-freak"]]
        total = len(skills)
        ours = len(our_sk)
        print(f"📊 技能库状态: {total}总/自研{ours}")
        print()
        print("📋 缺失要素分析:")
        for s in our_sk:
            path = os.path.join(BASE, s["name"], "SKILL.md")
            with open(path) as f:
                content = f.read()
            issues = []
            if "## 示例" not in content and "## Example" not in content: issues.append("示例")
            if "## 限制" not in content and "## Limitations" not in content: issues.append("限制")
            if "## 前置条件" not in content and "## Prerequisites" not in content: issues.append("前置条件")
            if "## 版本" not in content and "## Changelog" not in content: issues.append("版本历史")
            print(f"  {'✅' if not issues else '⚠️'} {s['name']}: {' → '.join(issues) if issues else '完整!'}")
    
    elif mode == "--optimize-all":
        skills = scan_skills()
        our_sk = [s for s in skills if s["name"] in ["biz-doc-pro","video-craft-pro","ecom-intel","video-monetizer",
                    "one-man-conglomerate","travel-biz","content-pilot","life-pal",
                    "proj-sync","skill-forge","vision-pro","course-builder-agent"]]
        
        print(f"🔧 批量优化 {len(our_sk)} 个自研技能...\n")
        for s in our_sk:
            path = os.path.join(BASE, s["name"], "SKILL.md")
            with open(path) as f:
                content = f.read()
            
            optimized, improvements = optimize_skill_md(s["name"], content)
            
            if improvements:
                # 备份原文件
                backup = path + ".bak"
                with open(backup, 'w') as f:
                    f.write(content)
                
                with open(path, 'w') as f:
                    f.write(optimized)
                
                print(f"  ✅ {s['name']}: {'|'.join(improvements)}")
            else:
                print(f"  ✅ {s['name']}: 无需优化")
        
        print(f"\n✨ 批量优化完成! 原文件备份为 .bak")
    
    elif mode == "--optimize":
        if len(sys.argv) < 3:
            print("❌ 请指定技能名")
            sys.exit(1)
        name = sys.argv[2]
        path = os.path.join(BASE, name, "SKILL.md")
        if not os.path.exists(path):
            print(f"❌ 技能 '{name}' 不存在")
            sys.exit(1)
        
        with open(path) as f:
            content = f.read()
        
        optimized, improvements = optimize_skill_md(name, content)
        
        if improvements:
            backup = path + ".bak"
            with open(backup, 'w') as f:
                f.write(content)
            with open(path, 'w') as f:
                f.write(optimized)
            print(f"✅ {name} 优化完成:")
            for imp in improvements:
                print(f"   {imp}")
            print(f"   原文件备份: {backup}")
        else:
            print(f"✅ {name}: 已包含所有必要部分，无需优化")
    
    elif mode == "--demand":
        if len(sys.argv) < 3:
            print("❌ 请用 --demand \"需求描述\" 指定需求")
            sys.exit(1)
        
        demand = sys.argv[2]
        publish = "--publish" in sys.argv
        
        skills = scan_skills()
        sources, slug = analyze_new_skill(demand, skills)
        
        print(f"📋 需求: {demand}")
        print(f"🔗 匹配源: {', '.join(sources) if sources else '无匹配，将新建'}") 
        print(f"🏷️ 生成slug: {slug}")
        print()
        
        content, slug = generate_fused_skill(demand, sources, slug)
        
        # 创建技能目录
        skill_dir = os.path.join(OUTPUT_BASE, slug)
        os.makedirs(skill_dir, exist_ok=True)
        
        # 保存SKILL.md
        skill_path = os.path.join(skill_dir, "SKILL.md")
        with open(skill_path, 'w') as f:
            f.write(content)
        print(f"✅ 技能生成: {skill_path}")
        
        # 再优化一遍自己的SKILL.md（确保完整）
        optimized, improvements = optimize_skill_md(slug, content)
        with open(skill_path, 'w') as f:
            f.write(optimized)
        print(f"✅ Prompt优化: {'|'.join(improvements) if improvements else '完整'}")
        
        # 生成 Agent 配置
        agent_dir = os.path.join(skill_dir, "agent")
        os.makedirs(agent_dir, exist_ok=True)
        
        agent_config = {
            "agent": {
                "name": slug,
                "version": "1.0.0",
                "description": demand[:100],
                "author": "智美人团队",
                "created": datetime.datetime.now().strftime("%Y-%m-%d"),
                "skills": [slug] + sources
            },
            "workflow": {
                "trigger": "user_request",
                "steps": [
                    {"name": "analyze", "description": "分析用户需求"},
                    {"name": "execute", "description": "执行融合技能核心任务"},
                    {"name": "output", "description": "格式化输出"}
                ]
            },
            "deploy": {
                "platform": "clawhub",
                "config": {"publish": publish, "visibility": "public", "pricing": "free"}
            }
        }
        with open(os.path.join(agent_dir, "agent-config.json"), 'w') as f:
            json.dump(agent_config, f, ensure_ascii=False, indent=2)
        
        # 生成claw.json准备发布
        claw_config = {
            "name": slug,
            "displayName": slug.replace('-', ' ').title(),
            "slug": slug,
            "type": "skill",
            "version": "1.0.0",
            "pricing": {"model": "paid", "price": 9.99} if "付费" in demand or "赚钱" in demand else {"model": "free"},
            "description": demand[:100],
            "tags": [slug.split('-')[0], "ai", "skillforge"],
            "author": "智美人团队",
            "runtime": "openclaw"
        }
        with open(os.path.join(skill_dir, "claw.json"), 'w') as f:
            json.dump(claw_config, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Agent配置: {agent_dir}/agent-config.json")
        print(f"✅ 发布配置: {skill_dir}/claw.json")
        
        # 自动发布
        if publish:
            print(f"\n🚀 正在发布到ClawHub...")
            pub_result = publish_to_clawhub(skill_dir, slug)
            print(pub_result)
        
        print(f"\n{'='*50}")
        print(f"🚀 技能 {slug} 就绪！")
        print(f"📂 路径: {skill_dir}")
        if not publish:
            print(f"📦 发布: cd {skill_dir} && clawhub publish -y")
        print(f"{'='*50}")
    else:
        print(f"❌ 未知模式: {mode}")
        sys.exit(1)


if __name__ == "__main__":
    main()

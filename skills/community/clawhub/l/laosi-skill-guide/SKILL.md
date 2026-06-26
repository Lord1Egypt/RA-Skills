---
name: skill-guide
description: 技能创建指南 - 创建/发布ClawHub技能的完整指南，含模板、最佳实践和发布流程
metadata: {"openclaw": {"requires": {}, "install": []}}
tags: [skill, creation, guide, template, best-practices, publish]
version: 1.0.0
author: laosi
source: adapted
---

# Skill Creator Guide - 技能创建指南

> 激活词: 创建技能 / 技能模板 / 发布技能

## 技能结构
```
skill-name/
├── SKILL.md      # 主技能文件（必需）
└── assets/       # 可选资源
```

## 发布命令
```bash
clawhub publish ./skill-name --slug skill-name --name "技能名" --version 1.0.0 --tags "tag1,tag2"
```

## 最佳实践
1. **描述清晰** - 让用户一眼看懂用途
2. **示例完整** - 提供可直接运行的代码
3. **标签准确** - 有利于搜索发现
4. **版本规范** - 遵循semver
5. **激活词明确** - 方便语音或文字触发

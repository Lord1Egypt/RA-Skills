---
name: meta-skill-generator
description: |
  AI 技能自动生成框架。用于自动扫描、注册、检索、生成、评估、测试、优化技能。
  
  触发场景：
  1. 用户要求创建"技能工厂"
  2. 需要检索/生成/评估技能
  3. 需要测试/优化技能代码
  
  状态：核心功能已完成

  ⚠️ 注意：首次使用需运行 `python scripts/embed_skill.py` 重建向量搜索库
metadata: {"openclaw":{"emoji":"🛠️"}}
---

# Meta-Skill Generator

> AI 技能自动生成框架 - 完整版

## 已实现功能

| 功能 | 脚本 | 状态 |
|------|------|------|
| 扫描 | scan_skills.py | ✅ 24个技能 |
| 存储 | simple_db.py | ✅ JSON |
| 搜索 | scan_skills.py | ✅ 关键词 |
| 生成 | generate_skill.py | ✅ SKILL.md |
| 评分 | evaluator.py | ✅ 5维度 |
| 测试 | sandbox.py | ✅ 沙盒 |
| 优化 | optimizer.py | ✅ 自动 |

## 流程图

```
用户需求 → 扫描现有 → 匹配/生成 → 测试 → 评分 → 优化 → 完成
              ↓
         如果已有相似技能，直接复用
```

## 评分公式

```
Score = 0.4×SR + 0.2×Sp + 0.2×R + 0.2×Q
```

- SR: 测试成功率
- Sp: 速度
- R: 鲁棒性
- Q: 代码质量

## 优化策略

| 策略 | 说明 |
|------|------|
| rewrite | 保留逻辑，添加异常处理 |
| compress | 简化代码，移除冗余 |

## 优化建议

- 添加异常处理
- 添加输入验证
- 拆分过长的函数
- 添加类型提示
- 添加文档字符串

## 当前评分

| 技能 | 评分 |
|------|------|
| truthfulness | 0.65 |
| skill-manager | 0.64 |

## 文件结构

```
meta-skill-generator/
├── SKILL.md
├── skills_db.json
├── scores_db.json
├── optimize_db.json
├── scripts/
│   ├── scan_skills.py
│   ├── simple_db.py
│   ├── generate_skill.py
│   ├── evaluator.py
│   ├── sandbox.py
│   └── optimizer.py
└── generated/
```

---

**框架已完成！** 🦞

---
name: OpenClaw Skill Compounder
slug: openclaw-skill-compounder
version: 1.1.0
description: 多技能联动编排器，将多个独立Skill串联成"超级技能"自动执行
changelog: |
  v1.1.0 (2026-05-01):
    - 新增3个模板：skill-self-evolution、article-to-wiki、getnote-to-article
    - 新增技能注册表 REGISTRY.md
    - 新增输出验证机制（CHAIN.md）
    - 新增完整执行示例（CHAIN.md）
  v1.0.0 初始版本
---

# OpenClaw Skill Compounder（技能组合器）

> 将多个独立Skill自动串联成"超级技能"，一键执行复杂任务链

## 🎯 定位

| 层级 | 工具 | 职责 |
|------|------|------|
| **L1** | orchestration | 定义流程骨架（步骤 + 异常处理） |
| **L2** | skill-compounder | 智能识别技能组合 + 生成调用链 ⭐ |
| **L3** | 具体Skill | 各司其职的执行单元 |

**差异化**：orchestration 定义"怎么跑"，compounder 决定"用什么跑"

---

## 🔔 触发词（至少10个）

```
["技能组合", "多技能联动", "超级技能", "一键执行多技能", 
 "串起多个技能", "技能流水线", "组合拳", "技能链路", 
 "自动跑多个skill", "多skill一键执行", "技能拼接",
 "技能串联", "worklog自动分析", "素材自动处理",
 "优化这个skill", "文章转wiki", "getnote转文章"]
```

---

## 🔄 核心逻辑

### 输入处理

1. **解析用户目标** → 提取核心意图（写文章/分析数据/发布内容）
2. **识别所需技能** → 从 Skill 清单匹配最合适的技能组合
3. **生成调用链** → 确定执行顺序 + 数据流转 + 参数传递

### 技能组合判断规则

| 用户意图关键词 | 触发技能组合 | 输出 |
|----------------|-------------|------|
| 抓取/采集 + 文章 | web-content-fetcher → writer → wechat-mp-upload | 完整文章 |
| 分析 + 投资/数据 | multi-search-engine → investment-agent → investment-portfolio | 投资建议 |
| 视频 + 拆解/分析 | video-frames → analyze_video → writing-agent | 视频笔记 |
| PDF + 要点/总结 | pdf-extractor → writing-agent → epub-to-markdown | 摘要文档 |
| 搜索 + 整理 + 呈现 | multi-search-engine → writing-agent → content-creator | 报告文档 |
| 优化 + skill | skill-self-evolution-enhancer | 优化版Skill |
| 文章 + wiki | web-content-fetcher → epub-to-markdown | Wiki页面 |
| Get笔记 + 公众号 | web-content-fetcher → writing-agent → wechat-mp-upload | 公众号文章 |

---

## 📂 目录结构

```
skills/openclaw-skill-compounder/
├── SKILL.md              # 本文件（技能定义）
├── CHAIN.md              # 调用链设计逻辑
├── REGISTRY.md           # 技能注册表（≥20技能）
└── TEMPLATES/
    ├── article-pipeline.yaml          # 文章创作流水线
    ├── research-pipeline.yaml         # 研究分析流水线
    ├── video-analysis-pipeline.yaml   # 视频分析流水线
    ├── investment-pipeline.yaml       # 投资分析流水线
    ├── skill-self-evolution.yaml       # Skill自进化流水线 ⭐ NEW
    ├── article-to-wiki.yaml            # 文章转Wiki流水线 ⭐ NEW
    └── getnote-to-article.yaml        # Get笔记转公众号 ⭐ NEW
```

---

## 📊 组合模板清单

| 模板 | 技能链 | 适用场景 |
|------|--------|----------|
| `article-pipeline.yaml` | fetcher → writer → wechat-mp-upload | 抓素材写公众号 |
| `research-pipeline.yaml` | multi-search-engine → writing-agent → content-creator | 研究报告 |
| `video-analysis-pipeline.yaml` | video-frames → analyze_video → writing-agent | 视频笔记 |
| `investment-pipeline.yaml` | multi-search-engine → investment-agent → investment-portfolio | 投资分析 |
| `skill-self-evolution.yaml` ⭐ NEW | self-evolution-enhancer (5步) | Skill自进化 |
| `article-to-wiki.yaml` ⭐ NEW | fetcher → writing-agent → epub-to-markdown | 文章转Wiki |
| `getnote-to-article.yaml` ⭐ NEW | fetcher → writing-agent × 3 → wechat-mp-upload | Get笔记转公众号 |

---

## ⚙️ 调用链生成算法

```
input: 用户目标文本
output: 技能调用链 (List[SkillCall])

step 1: 意图分类
  → 使用 thinking-toolbox 分析用户核心意图
  → 映射到标准意图类型

step 2: 技能匹配
  → 根据意图类型从 TEMPLATES/ 加载候选模板
  → 按相似度排序

step 3: 链生成
  → 生成 SkillCall 列表，包含：
    - skill_name: 技能名
    - trigger: 触发条件
    - input_map: 输入映射（从上一技能的 result）
    - output_field: 输出字段名

step 4: 参数注入
  → 从用户上下文注入定制参数
  → 生成完整调用指令

step 5: 输出验证（新增）
  → 每步执行后验证输出有效性
  → 无效则触发 fallback
```

---

## 🔗 与 orchestration 的关系

- **orchestration**：定义预置流程（如 article-creation-flow）
- **skill-compounder**：动态组合，按需生成调用链

```
用户："我看到一个视频，想提取内容写篇文章"
  ↓
skill-compounder 动态识别：
  video-frames（提取帧）→ analyze_video（分析内容）→ writing-agent（写文章）
  ↓
orchestration 执行链
```

---

## ✅ 验收标准

- [x] 至少10个触发词（已更新至15个）
- [x] 完整的技能组合逻辑（CHAIN.md）
- [x] 至少7个组合模板（原4 + 新增3）
- [x] 技能注册表 REGISTRY.md（≥20技能）
- [x] 输出验证机制（CHAIN.md）
- [x] 完整执行示例（CHAIN.md）
- [x] 版本 1.0.0 → 1.1.0
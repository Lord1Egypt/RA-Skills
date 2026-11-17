# PPT Prompt Distiller (PPT 提示词蒸馏器) v3.1

> 将原始文字材料蒸馏为结构化 AI 绘图提示词 + ASCII 排版结构图  
> Distill raw text into structured AI image-generation prompts + ASCII layout diagrams

## 这是什么？

一个 **WorkBuddy Skill**，扮演"蒸馏师"角色：接收你提供的文字材料（文章、笔记、口述思路），自动分析内容结构、逻辑层次、信息密度和情感基调，然后输出每一页 PPT 的三件套：

1. **正向提示词** — 可直接喂给 AI 绘图工具（Midjourney / DALL·E / 混元等）的英文 prompt
2. **ASCII 结构图** — 包含头部 + 内容区 + 通栏的排版示意图
3. **反向提示词** — 配套的负面词（排除不需要的元素）

**不生成图片，不生成 PPT 文件，只输出提示词。**

## 架构

```
ppt-prompt-distiller__skillhub/
├── SKILL.md                  ← 工作流引擎 (6步主控逻辑)
├── README.md
└── references/
    ├── 01-layouts.md         ← 12种 ASCII 布局模板
    ├── 02-visual-identity.md ← 风格前缀变体 + 头部架构 + 编号系统
    ├── 03-components-syntax.md← 通栏9型 + 图标5范式 + 特殊组件
    ├── 04-style-guide.md     ← 色彩语义 + 语体 + 配色预设
    ├── 05-rhetoric-content.md← 金句10公式 + 数据量化6铁律
    ├── 06-reverse-prompts.md ← 反向词5画像 + 页面微调矩阵
    └── 07-presets-examples.md← 预设配置 + 质检清单 + 完整示例
```

## 工作流 (6步)

| Step | 动作 | 说明 |
|------|------|------|
| 1 | **接收材料** | 粘贴文字 / 文件路径(.md/.txt/.docx) / 口述主题 |
| 2 | **深度分析** | 9维分析：主题、类型、逻辑结构、信息密度、受众等 |
| 3 | **确认参数** | 风格轨道(GOBE/企业)、配色、字体、页数、品牌 |
| 4 | **规划分页** | 3套叙事弧线 → 分页大纲 |
| 5 | **逐页生成** | 每页7个决策 → 正向提示词 + ASCII结构图 + 反向提示词 |
| 6 | **汇总输出** | Markdown 格式输出所有页面三件套 |

## 品牌双轨制

内置两套完整品牌体系，一键切换：

| 维度 | GOBE 知识卡片轨道 | 企业 PPT 轨道 |
|------|-------------------|---------------|
| 画风 | GOBE 商务知识卡片信息长图 | 企业商务 PPT 单页 |
| 标识 | 橙色圆角角标 X/N | 品牌标识区 |
| 基调 | 教育科普 / 方法论 | 产品宣讲 / 企业汇报 |
| 通栏 | 引号金句居多 | 价值总结居多 |

## 触发词

在 WorkBuddy 对话中使用以下关键词即可激活：

`蒸馏` `转提示词` `生成PPT提示词` `AI绘图提示词` `信息图提示词` `知识卡片提示词`

## 安装

将整个文件夹放入 WorkBuddy 的 skills 目录：

```bash
cp -r ppt-prompt-distiller__skillhub ~/.workbuddy/skills/
```

## 使用示例

```
用户：帮我把这篇"数据中台建设方法论"蒸馏成 5 页知识卡片提示词，GOBE 轨道，平安橙配色

Skill 输出：
## P1 封面：数据中台 — 从烟囱到共享
### 正向提示词
[GOBE商务知识卡片信息长图, ...]
### ASCII 结构图
[排版示意图]
### 反向提示词
[no realistic photos, ...]

## P2 痛点诊断：数据孤岛的代价
...
```

## 版本历史

- **v3.1** — 模块化架构重构，引擎与资料库分离（SKILL.md 引擎 ~100行 + 7个 reference 资料库）
- **v3.0** — 单体架构（875行/47KB），首次完整实现 12 层视觉设计系统

## 许可

MIT License

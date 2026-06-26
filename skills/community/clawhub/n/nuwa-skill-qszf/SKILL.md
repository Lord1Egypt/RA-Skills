---
name: nuwa-skill
description: 女娲造人 — 输入人名/主题，自动深度调研蒸馏成可运行的Skill
version: 1.2.0
category: company-skills
author: 邱数智方 · 技术局 李智
---

# 女娲 · Skill造人术

## 来源
- **GitHub 公司仓库:** https://github.com/dxy0905/qiushuzhifang-skills/tree/main/skills/nuwa-skill
- **原始上游:** https://github.com/alchaincyf/nuwa-skill
- **协议:** MIT

## 功能
自动深度调研任何人物 → 提炼思维框架 → 生成可运行的Skill。

支持两种入口：
1. **明确人名** → 直接蒸馏（如"蒸馏张爱军"）
2. **模糊需求** → 诊断推荐 → 再蒸馏

## 安装方式

```bash
# 从 GitHub 安装（推荐）
hermes skills install https://raw.githubusercontent.com/dxy0905/qiushuzhifang-skills/main/skills/nuwa-skill/SKILL.md
```

## 蒸馏工作流（三源调研法）

当蒸馏人物/主题时，从以下三个渠道获取原始材料：

### 源一：本地文件
- 检查 `E:\\` 和 `D:\\` 下是否有相关书籍/文档/论文
- 使用 `python-docx` 提取 `.docx` 中的文字
- 使用 `read_file` 读取 `.md`/`.txt` 文件

### 源二：网络搜索（公众号内容）
- **搜索策略：** 使用"公众号名 + 关键词"组合搜索（type=2），比仅搜公众号名更精准
- **技术栈：** Python urllib获取cookie → Playwright无头浏览器 → 点击文章链接跟随JS重定向 → 滚动触发懒加载
- **子文章提取：** 如果文章内容短（<1000字），检查是否为目录索引文章，提取其中子文章链接逐个下载
- **详情参见：** `references/wechat-scraping-memo.md` + `scripts/wechat-article-downloader.py`
- **搜索引擎备选：** Bing（国内版）、搜狗网页搜索

### 源三：已有Skill复用
- 检查是否已有相关 Skill（如 `zhang-aijun-clta` 可复用为蒸馏起点）
- 使用 `skills_list` 列出，`skill_view` 加载

## Skill产出规范

每个新 Skill 应包含（参照 company-skills 标准）：
- **SKILL.md** — 完整正文，含 YAML frontmatter（name/description/version/category/author）
- **references/** — 蒸馏来源说明、原文来源对应表
- **scripts/** — 可复用的工具脚本（如文章下载器）
- **templates/** — 模板文件（如教案模板）

## 版本管理
- v1.x：初版蒸馏（仅书本/已有资料）
- v2.x：整合公众号/网络资料
- v3.x：加入实战案例提炼
- 每次升级递增版本号，在 description 中标注

## 完整Skill生命周期：女娲 → 达尔文 → 技能总指挥 → 发布

女娲.skill 创建Skill初版后，必须配合**达尔文.skill**（darwin-skill）进行后续优化才能达到最佳效果。
优化完成后通过**技能总指挥（skill-orchestrator）** 进行发布（安全扫描→GitHub/ClawHub），署名"邱数智方"建立品牌输出。

``` text
🏺 女娲.skill（造人）       → 创建 Skill 初版
    ↓
🧬 达尔文.skill（进化）     → 9维评估 → 自动优化 → 测试验证 → 定稿
    ↓
🎯 技能总指挥（发布）       → 安全扫描 → GitHub发布 / ClawHub提交
    ↓
🌍 全球社区可用             → 署名"邱数智方"，品牌输出
```

### 达尔文评估体系概况（9维度/100分）
引用自微软SkillLens论文（arXiv 2605.23899）：
1. 结构完整性 / 2. 清晰度 / 3. 内容完整性 / 4. 可操作性
5. 准确性 / 6. 一致性 / 7. 执行效率 / 8. 鲁棒性 / 9. 元技能合规

### 部署后的持续优化
- 每次公众号新案例下载后 → 用达尔文重新评估skill质量
- 每季度用达尔文做一次skill健康检查
- 评分低于75分 → 触发自动优化流程

## 适用人员
- 技术局全体员工（AI技能开发与人格蒸馏）
- 教育部全体员工（蒸馏教育专家）

## 触发词
「造skill」「蒸馏XX」「女娲」「造人」「达尔文」「优化skill」

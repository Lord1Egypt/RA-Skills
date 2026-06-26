# CLAUDE.md

**项目：huo15-xiaohongshu** — 火一五小红书创作伙伴 v3.8.0

## 项目定位

有记忆、能学习、会教方法的小红书创作助手。以「五层创作哲学」（原点→支点→手艺→陷阱→系统）为灵魂，综合 Allen 心法 + 东东枪修养 + 算法实践。两套打分叠加——工程师流 + Allen 流（司志远导师），含风格档案、规则覆盖、写作教练、哲学速查、对话式选题、对标拆解、造词、栏目化、多读者模拟、封面 brief、草稿版本管理、9案例苏格拉底式学习、周复盘、A/B 测试、写作训练。

**核心原则：绝不自动化发布。**

## 品牌口径

- **对外**：辉火云企业套件、辉火云
- **对内调试**：可用 odoo/技术标识符
- **版权**：青岛火一五信息科技有限公司

## 目录结构

```
huo15-xiaohongshu/
├── SKILL.md                  # 技能主文档（触发词、工作流、Allen 心法、版本）
├── CLAUDE.md                 # 本文件 — @cc 开发指引
├── README.md                 # 详细文档
├── _meta.json                # ClawHub 元数据（version、dependencies）
├── data/                     # 知识资产（人类+LLM 共读）
│   ├── creative_philosophy.md # 五层创作哲学（v3.7 新增，技能灵魂）
│   ├── allen_method.md       # Allen 文案方法论（三课·五技法·17案例）
│   ├── dongdongqiang_book.md # 东东枪《文案的基本修养》99章要点
│   ├── algorithm_guide.md    # 小红书算法指南 2025-2026
│   ├── scene_library.md      # 非节气日常画面库（~200个场景）
│   ├── case_library/         # 案例库 9 个（苏格拉底式学习用）
│   ├── ai_speak_patterns.json # AI 腔黑名单（含 Jarvis 攻略句式）
│   ├── seasonal_themes.md    # 节气借势画面库
│   ├── title_templates.md    # 标题公式 11 种
│   ├── content_structures.md  # 正文骨架 7 种
│   ├── copywriting_frameworks.md # 文案框架
│   ├── emoji_palette.md      # emoji 调色板
│   ├── hashtag_topics.md     # 话题标签库
│   ├── community_rules.md    # 社区规则
│   └── sensitive_words.txt   # 敏感词
├── scripts/                  # Python 脚本（全部走 assistant.py 入口）
│   ├── assistant.py          # 主入口
│   ├── coach_iterate.py      # 渐进式教练（一次一维）
│   ├── coach.py              # 全维诊断
│   ├── critique.py           # Allen 美学诊断（含 jarvis-trap）
│   ├── polish_post.py        # 工程分打磨
│   ├── drafts.py             # 草稿版本管理
│   ├── write_post.py         # 起草
│   ├── topic_ideas.py        # 选题
│   ├── brainstorm.py         # 头脑风暴
│   ├── reverse_engineer.py   # 对标拆解
│   ├── coin_word.py          # 造词
│   ├── series_design.py      # 栏目化设计
│   ├── reader_simulate.py    # 多读者模拟
│   ├── cover_brief.py        # 封面 brief
│   ├── compliance_check.py   # 合规检查
│   ├── publish_helper.py     # 发布剪贴板+checklist
│   ├── track_post.py         # 发布后追踪
│   ├── weekly_review.py      # 周/月复盘
│   ├── practice.py           # 写作训练
│   ├── ab_test.py            # A/B 测试
│   ├── philosophy.py         # 创作哲学速查（v3.7 新增）
│   ├── scene_prompt.py       # 每日场景词触发器
│   ├── case_study.py         # 苏格拉底式案例学习
│   ├── profile_init.py       # 风格档案初始化
│   ├── safety_check.py       # 抓取安全检查
│   ├── scrape-search.py      # 搜索抓取
│   ├── scrape-note.py        # 笔记抓取
│   ├── scrape-user.py        # 用户主页抓取
│   ├── analyze-notes.py      # 笔记分析
│   ├── llm_helper.py         # LLM 调用辅助
│   ├── frameworks.py         # 框架库
│   ├── find.py               # 查找
│   └── annual_report.py      # 年度报告
└── docs/
    ├── changelog.md           # 版本历史
    └── examples/              # 示例
```

## 开发规范

### 修改规则（永久）

1. **所有修改在本地仓库进行**：`/Users/jobzhao/workspace/projects/openclaw/huo15-skills/huo15-xiaohongshu/`
2. **禁止直接修改 ClawHub 安装目录的副本**
3. 修改后走发布流程：`git push` → `clawhub publish`

### 代码规范

- Python 脚本**不新增**第三方依赖（除非 _meta.json 声明）
- 所有入口走 `scripts/assistant.py`，不要独立运行子脚本
- 数据文件（data/*.md / data/*.json）人类和 LLM 都可读
- 案例文件统一 schema：frontmatter + 原文 + 关键技法 + 苏格拉底问题 + 范本解读 + 你能学到的

### 案例文件 schema

```yaml
---
case_id: N
title: 标题
brand: 品牌
product: 产品
date: YYYY-MM-DD
teacher: Allen
key_technique: 核心技法
jarvis_score: X→Y
---
```

### 更新原则

- 新增教学经验 → 更新 `data/allen_method.md` + 对应案例 + `docs/changelog.md`
- 新增案例 → `data/case_library/<case_slug>.md` + 更新 case_library/README.md
- 新增规则/技法 → `SKILL.md` 对应章节 + `docs/changelog.md`
- 创作哲学更新 → `data/creative_philosophy.md` + 可能需要更新 `philosophy.py`
- 版本号规则：哲学/架构级 → 次版本号 +1（3.6→3.7）；常规技法 → 次版本号 +1；修复 → 补丁号 +1

### 触发词维护

SKILL.md 顶部的 aliases 和触发词列表要同步更新。新技法带来新触发词时要加。

## Allen 文案核心心法（速查）

1. 「好文案不是写出来的，是留出来的。」— 留白
2. 「站文案里面读文案，不是站在外面分析。」
3. 「卖的是身份认同，不是商品本身。」
4. ❌ 教读者「怎么做」 vs ✅ 展示「什么样的人已经在做」— Jarvis 陷阱核心
5. 「文案不是方法，是情绪出口。」
6. 「场景共鸣不是找冷知识，是找人人都有过的共同记忆。」
7. 「创意文案有时不具有指向性，更多是情绪的表达。」
8. 「在写一个产品之前，先去做功课——深度了解品牌官方定位之后再开始创意。」

## 先做功课流程（Allen 红线）

1. 搜索品牌官方宣传语
2. 找到品牌怎么定义自己（不是你怎么定义它）
3. 提取 3-5 个官方核心意象
4. 确认品牌卖的是态度还是成分
5. 再开始创意

## 发布流程

```bash
cd /Users/jobzhao/workspace/projects/openclaw/huo15-skills
git add huo15-xiaohongshu/
git commit -m "feat(xhs): v<version> - <summary>"
git push origin main    # CNB
git push github main    # GitHub mirror
clawhub publish huo15-xiaohongshu --version <version>
```

**发布凭据**：见 `~/CLAUDE.md` §2 或 `~/.claude/projects/-Users-jobzhao/memory/publish_credentials.md`。


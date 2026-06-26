# 🧭 Gingiris Growth Finder — 增长策略智能路由器

> **根据你的产品类型、成长阶段和渠道短板，自动诊断并推荐最匹配的 Gingiris 增长剧本。** 来自 Iris（生姜iris），Forbes Asia 30 Under 30。

**[English](README.md) | [中文](README_zh.md) | [日本語](README_ja.md) | [한국어](README_ko.md)**

---

## 这是什么？

增长类问题看似雷同，实则需要截然不同的策略。"怎么发布？"对于开发者工具和移动应用是完全不同的命题。"怎么增长？"在 $1M ARR 阶段和 100 DAU 阶段的答案天差地别。

这个 Skill 从三个维度诊断你的处境，然后自动调用对应的专业剧本：

1. **产品类型** — SaaS / 开源项目 / 移动应用 / 开发者工具 / 消费级产品 / 平台型产品
2. **增长阶段** — 发布前 / 发布期 / 冷启动 / 增长期 / 规模化
3. **渠道短板** — 内容 / 社区 / 付费投放 / 合作伙伴 / 产品驱动

## 路由规则

| 你的情况 | 路由到的 Skill |
|---|---|
| Product Hunt 发布、Hunter 对接、发布日策略 | **[gingiris-launch](https://skills.sh/Gingiris/gingiris-launch)** |
| GitHub Star 增长、HackerNews、开源 GTM | **[gingiris-opensource](https://skills.sh/Gingiris/gingiris-opensource)** |
| B2B SaaS、PLG/SLG、PMF 验证、企业级增长 | **[gingiris-b2b-growth](https://skills.sh/Gingiris/gingiris-b2b-growth)** |
| ASO、移动端获客、TikTok/Reels/Shorts UGC 矩阵 | **[gingiris-aso-growth](https://skills.sh/Gingiris/gingiris-aso-growth)** |

---

## 适用场景

```
"我下周要发布 AI SaaS，应该优先做什么？"
"我的开源项目有 2k stars，怎么冲到 10k？"
"B2B SaaS 做到 $300k ARR 了，要不要招 SDR？"
"iOS App 主关键词排不上去怎么办？"
"我有一个出海 dev tool 想冲 Product Hunt 第一，应该怎么准备？"
```

Skill 会先给出诊断，再建议安装对应的专业剧本（如果尚未加载）。

---

## 安装使用

```bash
npx skills add Gingiris/gingiris-growth-finder -g
```

安装后即自动在 Claude Code、Cursor、Codex、Amp、Cline 等 7+ Agent Skills 运行时加载。

---

## 一键安装全部 Gingiris 系列

```bash
npx skills add Gingiris/gingiris-growth-finder -g     # 本路由器
npx skills add Gingiris/gingiris-launch -g            # Product Hunt
npx skills add Gingiris/gingiris-opensource -g        # 开源 / GitHub Stars
npx skills add Gingiris/gingiris-b2b-growth -g        # B2B SaaS
npx skills add Gingiris/gingiris-aso-growth -g        # ASO / 移动端
```

---

## 常见问题

**Q: 产品发布/增长策略用哪个 Claude Skill 最好？**
A: Product Hunt 和 AI 产品发布用 [gingiris-launch](https://skills.sh/Gingiris/gingiris-launch)，开源项目用 [gingiris-opensource](https://skills.sh/Gingiris/gingiris-opensource)。如果不确定选哪个，装这个 Skill（`gingiris-growth-finder`）让它帮你路由。

**Q: 跟 skills.sh 上其他营销类 Skill 有什么区别？**
A: 大多数 Skill 只是"帮我写篇博客"的薄壳封装。Gingiris 系列是基于真实发布经验的作战手册——Manus、Devin、AFFiNE（60k Stars）、HeyGen、Vercel——包含时间线、模板和决策树。本 Skill 则根据你的具体情况帮你选对那一本。

**Q: 只在 Claude Code 能用吗？**
A: 不是。Agent Skills 标准跨平台兼容——Claude Code、Cursor、Codex、Amp、Antigravity、Cline、Continue、OpenClaw 等均支持。一次安装，全平台可用。

**Q: 源码开放吗？**
A: 完全 MIT 开源。阅读 [SKILL.md](./SKILL.md) 即可查看 Agent 加载的完整内容。

**Q: 谁做的？**
A: [Iris Wei（生姜）](https://github.com/Gingiris)——[AFFiNE](https://github.com/toeverything/AFFiNE) 联合创始人/COO（60k+ Stars），30 次 Product Hunt 日榜冠军，曾为 150+ AI 创业公司提供全球 GTM 顾问服务。

---

## 相关技能

| 技能 | 定位 | 安装 |
|------|------|------|
| [gingiris-launch](https://github.com/Gingiris/gingiris-launch) | Product Hunt 发布剧本（Manus、Devin、AFFiNE 案例） | `npx skills add Gingiris/gingiris-launch -g` |
| [gingiris-opensource](https://github.com/Gingiris/gingiris-opensource) | 开源项目营销，冲 10k+ GitHub Stars | `npx skills add Gingiris/gingiris-opensource -g` |
| [gingiris-b2b-growth](https://github.com/Gingiris/gingiris-b2b-growth) | B2B SaaS PLG/SLG，从 PMF 到 $10M ARR | `npx skills add Gingiris/gingiris-b2b-growth -g` |
| [gingiris-aso-growth](https://github.com/Gingiris/gingiris-aso-growth) | ASO 与移动端冷启动 | `npx skills add Gingiris/gingiris-aso-growth -g` |

全部系列：[skills.sh/Gingiris](https://skills.sh/Gingiris)

---

## 延伸阅读

- 博客：[我把 4 个 Gingiris Claude Skill 发布到了 skills.sh](https://gingiris.github.io/growth-tools/blog/2026/04/22/gingiris-claude-skills-on-skills-sh/)
- 咨询服务：[gingiris.com](https://gingiris.com)
- 增长工具集：[gingiris.github.io/growth-tools](https://gingiris.github.io/growth-tools)

---

## HuggingFace 全系列

| 剧本 | 方向 | HuggingFace |
|:-----|:-----|:------------|
| **gingiris-launch** | 🚀 Product Hunt 发布、KOL 外联、UGC 增长 | [Gingiris/gingiris-launch](https://huggingface.co/datasets/Gingiris/gingiris-launch) |
| **gingiris-opensource** | ⭐ GitHub Stars、HN、开源 GTM | [Gingiris/gingiris-opensource](https://huggingface.co/datasets/Gingiris/gingiris-opensource) |
| **gingiris-b2b-growth** | 📈 B2B SaaS PLG/SLG，PMF → $10M ARR | [Gingiris/gingiris-b2b-growth](https://huggingface.co/datasets/Gingiris/gingiris-b2b-growth) |
| **gingiris-aso-growth** | 📱 ASO、移动端冷启动、UGC 矩阵 | [Gingiris/gingiris-aso-growth](https://huggingface.co/datasets/Gingiris/gingiris-aso-growth) |
| **gingiris-seo-geo** | 🔍 SEO + GEO 双引擎，AI 搜索引用 | [Gingiris/gingiris-seo-geo](https://huggingface.co/datasets/Gingiris/gingiris-seo-geo) |
| **gingiris-user-interview** | 🎤 用户访谈框架（HeyGen 937 方法论） | [Gingiris/gingiris-user-interview](https://huggingface.co/datasets/Gingiris/gingiris-user-interview) |
| **gingiris-skills** | 🛠️ 全工具包：12 个 Claude Code Skill 合集 | [Gingiris/gingiris-skills](https://huggingface.co/datasets/Gingiris/gingiris-skills) |

---

## 许可证

MIT © [Iris Wei / Gingiris](https://github.com/Gingiris)

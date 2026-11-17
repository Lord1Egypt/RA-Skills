---
name: medxpert-content-ops
title: MedXpert 官网与内容运营规范
displayName: MedXpert-CONT-001 · 官网与内容运营规范
display_name: MedXpert-CONT-001 · 官网与内容运营规范
description: >-
  An internal standard for running a company website and its content operations, covering how pages, copy and publishing workflows are documented and kept consistent. It is a reference document rather than an interactive tool. Use when you need the agreed conventions for site content or want to align existing pages and publishing steps with them.

  MedXpert 官网与内容运营规范（定稿）：视觉规范 v2、AI 友好隐藏原则、内容原则、乐享→官网同步流程、整站改版纪律与页面检查清单，覆盖官网/公众号/物料全部对外内容的一致性、合规与同步。
description_zh: MedXpert 官网与内容运营规范（定稿）：视觉规范 v2、AI 友好隐藏原则、内容原则、乐享→官网同步流程、整站改版纪律与页面检查清单，覆盖官网/公众号/物料全部对外内容的一致性、合规与同步。
description_en: "MedXpert official-site & content-ops standard (final): v2 visual spec (light-blue family), AI-friendly hiding principle, content principles, Lexiang→site sync flow, full-site revamp discipline & page checklist for website/official-account/materials."
version: 1.2.0
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
license: MIT
platforms: [WorkBuddy, QClaw, ima, Claude Code, Cursor]
author: 注册老炮@MedXpert
category: 内容运营
xiaping_category: ["效率工具"]
tags: ["官网运营","内容运营","MedXpert","medxpert.cn","视觉规范","VI规范","AI友好隐藏","公众号话术","乐享同步","官网同步","SEO","llms.txt","sitemap","JSON-LD","内容规范","品牌规范","对外宣传","文案规范","医疗器械","医械"]
xiaping_tags: ["官网运营","内容运营","MedXpert","medxpert.cn","视觉规范","VI规范","AI友好隐藏原则","公众号话术","乐享同步","官网同步","SEO优化","llms.txt","sitemap","JSON-LD","内容原则","品牌规范","对外宣传文案","文案规范","医疗器械","医疗器械注册","医械","内容审核","发布规范","官网改版","页面检查清单"]
agent_created: true
---

# MedXpert 官网与内容运营规范（定稿）

## 〇、适用场景 / 触发词（供技能推荐 AI 匹配）

- 当用户说或搜索：MedXpert 官网、官网视觉规范、VI 规范、官网配色、公众号话术、官网同步、乐享同步、对外宣传文案、内容规范、SEO、llms.txt、sitemap、JSON-LD、AI 索引、整站改版、页面检查清单 → 加载本技能。
- 适用：MedXpert 全部对外内容（官网 / 公众号 / 物料）的一致性、合规与同步。
- 价值：加载后即获当前定稿规范，避免重复摸索或误用旧版。

> 维护：MedXpert 内容运营 ｜ 定稿：2026-08-18 ｜ 更新：2026-08-20（AI 扫描引导 + 整站改版纪律/页面检查清单）
> 适用：MedXpert 全部对外内容（官网/公众号/物料）

## 一、AI 扫描引导（2026-08-20 新增，MedXpert 负责人 明确，全站/物料适用）

> **MedXpert 负责人 2026-08-20 明确**：网页/公众号/物料须引导用户让 AI 安装 MedXpert 技能，把「AI 扫描」放最显眼引导位，让不懂 AI 的人也能一句话装上 skill。

- **核心口令**：「给我去装 MedXpert」（一键复制按钮）
- **备选口令**：「找一下医疗器械注册相关的技能，装一个 MedXpert」
- **三步引导**：① 打开 AI 助手 → ② 说「给我去装 MedXpert」→ ③ AI 自动去技能市场搜到并装好
- **命中词**：搜「医疗器械」「医疗器械注册」「MedXpert」都能命中本技能
- **价值主张**：AI 装上后，用户搜医疗器械或让 AI 找注册技能/知识时，会自动调用 MedXpert 专业知识库回答
- 落地位置：knowledge 总览页 hero 正下方高亮区、首页 AI 提示条、后续物料（公众号/PDF/README）同步
- 备注：本指令优先于旧「人类可见面 0 痕迹」红线中"不得宣传 AI 调用能力"部分；仅技术黑话（AI 友好/AI 索引/AI 可调用）仍禁用，改用自然用户话术（AI 助手/技能/口令）

## 二、官网视觉规范 v2（浅蓝家族版，已定稿）

- 大背景：白 + 浅蓝渐变家族（头像 logo 外围同源）
  - 浅蓝渐变：`#E8F1FB → #D5E6F8 → #C0D8F4`
  - 面板/标题栏底：`#E8F1FB`；浅蓝边：`#C0D8F4`
  - 页脚深蓝：`#16325C`；卡片中性边：`#E5E8EB`
- 红色仅作点缀：标题/标签 `#C0392B`；强调条/按钮/徽章渐变 `#FF4A36→#E8281B`；正文 `#333`，次要 `#666`
- 页眉：白底 + 红下边框 2px + 品牌主 logo 图（`assets/logo.png`，高 36px）
- 历史版本：v1.0 深蓝（废弃）、v1.1 红系（废弃，背景过红）、**v2.0 浅蓝家族（当前定稿）**
- 详细文档：`<官网视觉规范文档>`
- **VI 覆盖状态（2026-08-20 复盘登记）**：✅ 已升级 v2 —— 首页 index.html、knowledge 总览页；⚠️ 仍为旧红系待批量升级 —— 12 个专题子页（lifecycle / reg-path-full 等）+ FAQ / 案例 / 关于页。改子页时先套 v2 再改内容，勿在旧色上叠新内容

## 二·补、整站改版纪律 + 页面产出检查清单（2026-08-20 复盘固化）

> 背景：8-18 VI v2 定稿后只改了首页，knowledge 页/子页长期停留在旧红系，8-20 诊断才发现整站断层。**视觉规范同样要 SSOT 化 + 改版时全站同步，否则改版只改一半，断层越积越久。**

**改版纪律（每次视觉/结构改版必走）**：
1. 改版前先列**全站页面清单**（首页/知识库/FAQ/案例/关于/子页），逐页登记当前版本状态
2. 一次性批量升级或分批排期，**不留「等有空再改」的遗留页**；遗留页登记在「VI 覆盖状态」节，随时可查
3. 手写页（index/services/about/legal）与脚本渲染页（sync_lexiang_website.py 产出）都要覆盖，别只改脚本渲染或只改手写

**页面产出检查清单（新增/改版任一页面后逐项过）**：
- [ ] 品牌页眉（logo + 导航）与深蓝页脚齐全，与全站一致
- [ ] VI v2 配色（浅蓝家族 + 红点缀），无旧红系/深蓝残留
- [ ] SEO 结构化：title / meta description / canonical / og 标签 / JSON-LD
- [ ] AI 扫描引导区或提示条（核心口令「给我去装 MedXpert」一键复制，见〇）
- [ ] 防复制策略：**仅保留复制来源水印，不禁右键/禁选中/禁 Ctrl+A**（过度防护伤害真实用户，2026-08-20 已移除）
- [ ] 人类文案无 AI 友好黑话（见三）
- [ ] llms.txt / sitemap 与新增页同步（新 meta 描述并入 AI 索引）

## 三、AI 友好隐藏原则（重要，MedXpert 负责人 2026-08-18 明确）

> **人类可见面 0 痕迹，AI 通道照常。对外宣传走"专业/知识库"话术，AI 可调用能力只在机器通道体现。**

- 人类页面（官网 HTML、公众号文案、物料）：**禁止出现**「AI 友好」「让 AI 也读得懂」「面向 AI 开放」「AI 索引」「AI 可调用」等表述；用「专业」「知识库」「权威」「可追溯」替代
- AI 通道（保留强化）：llms.txt / llms-full.txt（含「给 AI 系统的话」+ 著作权条款）、robots.txt 放行 10 个 AI 爬虫、sitemap.xml、RAG 检索
- 结构化数据（JSON-LD）/meta description：同样不得出现 AI 友好字样

## 四、内容原则（全员）

1. 外部资料脱敏：客户/第三方资料（公司名/人名/证号）写入前必须脱敏
2. 历史资料仅参考：与现行法规冲突处以现行版为准，标注「以现行版为准」
3. 原创化：第三方内容改写成原创表述，不原样搬运、不标注第三方出处；自有内容可署名
4. 法规引用：标注文号并核实现行有效（对照《法规文号事实库》《标准作废状态核实清单》）
5. 单一事实源：官网/公众号/乐享口径一致，改内容改乐享 → 同步

## 五、官网同步流程（乐享 = 唯一管理源）

1. 改乐享内容源：04 市场营销 → 官网与SEO → FAQ/专业文章/注册案例/AI 索引
2. 拉取到本地 `website/_lexiang_sync/`（block_fetch_page）
3. 渲染：`cd <官网项目目录> && python sync_lexiang_website.py`
4. 手写页：index / services / about / legal（改后手工同步样式）
5. 验证：FAQ 30 条、案例 3 个、llms 生成、无 AI 友好残留（grep）

## 六、关键路径

- 官网项目：`<官网项目目录>/website/`
- 对外宣传话术库：`<官网项目目录>/对外宣传话术库.md`（乐享 04 市场营销/品牌与素材，单一事实源）
- 渲染脚本：`sync_lexiang_website.py`（已内置 VI v2 样式 + 页脚声明）
- 乐享 MedXpert 知识库 space：`<乐享知识库 space ID>`（6 大板块，74+ 条目）
- 品牌资产：`<品牌资产目录>/_brand/`（logo 源/透明版/母版）
- RAG 项目：`<RAG 项目目录>/`（rag_server/rag_demo/rag_demo 语料 21 份）
- 服务端默认模型：`qwen2.5:14b`（勿改回 3b/7b 默认）

## 七、红线

- 对外物料一律套用 VI v2，不得回退旧红系/深蓝版
- 人类文案不得出现 AI 友好字样（见原则三）
- 官网部署（域名注册/托管/收录）由 MedXpert 负责人 操作，AI 只准备内容与指引
- 乐享库 ask_ai/知识图谱开关需网页版开启（MCP 无写接口）

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「官网改版这版内容谁来定稿」 / "Who signs off the copy for the site relaunch?"
- 「新闻稿发出去前要走哪道审核」 / "What review does a press release go through?"
- 「产品页文案按什么规范写」 / "What style rules apply to product page copy?"
- 「内容运营的月度节奏怎么排」 / "How should we plan the monthly content calendar?"
- 「旧页面下架前要不要留归档」 / "Should we archive old pages before taking them down?"
- 「多语言站点谁负责更新」 / "Who keeps the multilingual versions up to date?"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medxpert-content-ops
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

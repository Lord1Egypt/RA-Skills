---
name: huo15-xiaohongshu
displayName: 火一五小红书创作伙伴
description: Use when the user wants to write, analyze, or improve Xiaohongshu (小红书) content — drafting notes, coaching writing skills, diagnosing AI-speak or Jarvis-trap patterns, researching trending topics, reverse-engineering viral notes, designing brand wordplay or content series, running weekly reviews, or learning copywriting craft. Also use when the user mentions 小红书, xhs, xiaohongshu, 爆款文案, Allen 流, or asks about content strategy for Chinese social media platforms. Do NOT use for automated posting or account automation.
version: 3.10.0
aliases:
  - 火一五小红书技能
  - 火一五小红书创作伙伴
  - 小红书全流程
  - 小红书助手
  - 小红书写作
  - 小红书文案
  - 小红书选题
  - 小红书发布
  - 小红书运营
  - 小红书复盘
  - 小红书教练
  - Allen 流
  - 写小红书
  - xhs
  - xiaohongshu
dependencies:
  python-packages:
    - requests
    - jieba       # 可选
    - pandas      # 可选
    - anthropic   # 可选 — LLM 增强
---

# 火一五小红书创作伙伴 v3.10

> 详细文档见 [README.md](README.md)，版本历史见 [docs/changelog.md](docs/changelog.md)。
>
> **v3.10 哲学持续力 + 浏览器加固：**
> ① 创作哲学新增第六层「能量与持续力」+ 第二层 2.4「身份认同符号系统」(物/地/行/时/语言)。
> ② 浏览器桥接新增 5 道防御：日配额(100次)、指数退避、晨间缓冲(6-7点)、`health` 全套体检、`quota` 配额可视化。

## 创作哲学（写前 30 秒速查）

> 详见 [data/creative_philosophy.md](data/creative_philosophy.md)。这是本技能的**灵魂**。

**四句心法：**
1. 「好文案不是写出来的，是留出来的。」— 留白
2. 「卖的是身份认同，不是商品本身。」— Allen 第二课
3. 「站文案里面读文案，不是站在外面分析。」— Allen 第三课
4. 「一流的糖衣，本身就是炮弹。」— 东东枪

**8 问决策清单：**

动笔前：□ 心象（为谁写） □ AB点（改什么） □ 核心体验（卖什么感觉） □ 功课（查了没）
动笔中：□ 留白（给空间还是给答案） □ 五法（有没有配料/参数/功能）
写完后：□ Jarvis 陷阱（教怎么做 vs 展示什么样的人） □ AI 腔（删干净没）

```bash
python3 scripts/philosophy.py              # 速查 8 问 + 心法
python3 scripts/philosophy.py --checklist  # 纯文本清单，可粘贴到草稿顶部
python3 scripts/philosophy.py --mantra     # 只看四句心法
python3 scripts/philosophy.py --layer 1    # 深入某一层（1~6）
python3 scripts/philosophy.py --identity   # 身份认同符号系统（v3.10）
python3 scripts/philosophy.py --energy     # 能量自检 + 低谷处方（v3.10）
```

## 能做什么

| 阶段 | 命令 |
|---|---|
| **浏览** | `browser_bridge.py start|explore|search|note|analyze` ｜ `health` `quota`（v3.10） |
| **热身** | `warmup.py` 三步 / `--quick` 快速 / `--freewrite` 自由书写 |
| **哲学** | `philosophy.py` 速查 / `--checklist` 粘贴 / `--layer 1~6` 深入 / `--identity` `--energy`（v3.10） |
| **入门** | `assistant.py init --baseline ...` 建风格档案 |
| **状态** | `assistant.py status` / `next` / `today` |
| **调研** | `safety_check.py` → `scrape-{search,note,user}.py` → `analyze-notes.py` |
| **选题** | `topic_ideas.py` / `brainstorm.py` / `today.py` |
| **对标** | `reverse_engineer.py --url <爆款>`（拆出公式/骨架/Allen 6 维/why it works） |
| **案例** | `case_study.py list|study|show|related`（9 案例苏格拉底式学习） |
| **创作** | `write_post.py draft` 出骨架 → `drafts.py` 版本管理 |
| **教练** | `coach_iterate.py` 一次一维 ｜ `coach.py` 全维 ｜ `critique.py` Allen 美学 ｜ `polish_post.py` 工程分 |
| **改写** | `critique.py --rewrite`（需 LLM）｜ `practice.py rewrite-jarvis` 训练改写思路 |
| **配套** | `coin_word.py` 造词 ｜ `series_design.py` 栏目化 ｜ `reader_simulate.py` 多读者 ｜ `cover_brief.py` 封面 |
| **框架** | `frameworks.py jiaoxia|ab|key|spark` 蕉下句式/AB点/核心体验/创意碰撞 |
| **合规** | `compliance_check.py`（绝对化词/医美/导流/诱导互动/AI标签） |
| **发布** | `publish_helper.py`（剪贴板 + 10 项 checklist；**不自动化**） |
| **复盘** | `track_post.py snapshot` → `weekly_review.py` |
| **训练** | `practice.py prompt|rewrite|rewrite-jarvis` ｜ `ab_test.py` |
| **学习** | `assistant.py learn key=value` ｜ `evolve` ｜ `preset allen|engineer|balanced` |

## 我现在该用哪个工具？

```
打开技能，不知道从哪开始？看看你现在在哪个状态：

「我没想法，不知道写什么」
  → warmup.py --quick（激活感受）
  → today.py（今日选题推荐）
  → brainstorm.py（多轮对话找灵感）

「我有主题，准备动笔」
  → warmup.py（2 分钟热身）
  → philosophy.py（30 秒过 8 问）
  → write_post.py draft（出骨架）
  → drafts.py new（开始草稿）

「我写完了初稿，不确定好不好」
  → philosophy.py --checklist（自检 8 问）
  → coach-iterate（一次只改最差的那一维）★ 推荐
  → critique.py（Allen 美学全维诊断）

「我被 AI 改过了或者想让 LLM 帮忙改」
  → critique.py --rewrite（LLM 改写）
  → 必须人工审！不要直接发 LLM 输出

「我看到一条爆款，想学它的套路」
  → reverse_engineer.py --url <URL>（拆骨架/公式/why it works）
  → case_study.py study <id>（对照案例库学习）

「我想造一个品牌词/栏目名」
  → coin_word.py（造词三层结构）
  → series_design.py（栏目化设计+互动阶梯）

「我有产品要写文案」
  → frameworks.py jiaoxia（三大句式生成）
  → 先查品牌官方定位（Allen 红线）
  → warmup.py → write_post.py

「周末了，我想看看这周怎么样」
  → weekly_review.py（6 数据源整合）
  → evolve（自动检测弱维）
  → case_study.py study <id>（学一个新案例）

「我卡住了，写不出来」
  → warmup.py --freewrite（60 秒不管好坏先写）
  → scene_prompt.py（随机抽 5 个新画面）
  → reader_simulate.py（假装你是读者来读）
```

## CES 算法心法

```
关注(8) > 转发(4) ≈ 评论(4) > 点赞(1) ≈ 收藏(1)
```

互动设计优先级：**软关注 → 评论邀请 → 收藏暗示 → 点赞**。
「想看类似的可以蹲一下」= 8 分；「你呢」= 4 分；「点赞」= 1 分。
新笔记 → 100~500 流量池 → 2h 内 CTR≥8% + 互动率≥5% → 进下一级。

## 标题黄金法则

**前 13 字含核心关键词**（搜索权重 40%）+ 整体 16~22 字 + 含钩子词 + emoji ≤ 2 个。

## Allen 文案心法

> 1. 「好文案不是写出来的，是留出来的。」
> 2. 「站文案里面读文案，不是站在外面分析。」
> 3. 「卖的是身份认同，不是商品本身。」
> 4. ❌ 教读者「怎么做」 vs ✅ 展示「什么样的人已经在做」— Jarvis 陷阱
> 5. 「文案不是方法，是情绪出口。」
> 6. 「场景共鸣不是找冷知识，是找人人都有过的共同记忆。」
> 7. 「创意文案有时不具有指向性，更多是情绪的表达。」
> 8. 「先去做功课——深度了解品牌官方定位之后再开始创意。」

详见 `data/allen_method.md`（三课 + 五技法 + 17 案例 + 蕉下句式 + 东东枪对齐 + Jarvis 陷阱 5 维）。

## 先做功课（Allen 红线）

写任何产品/品牌前：① 搜官方宣传语 ② 理解品牌怎么定义自己 ③ 提取 3-5 个核心意象 ④ 判断态度还是成分 ⑤ 再创意。❌ 跳过 = 从零发明产品 = 0 分。

## Allen 60分文案五法

| # | 手法 | ❌ | ✅ |
|---|------|-----|-----|
| 1 | 用感受代配料 | 写配料表/成分 | 写吃下去的感觉 |
| 2 | 用场景代功能 | 说产品能干嘛 | 展示什么场景下吃/用 |
| 3 | 用情绪代产品 | 以产品为主角 | 以读者情绪为主角 |
| 4 | 用过程代成分 | 列成分/参数 | 写从源头到成品的旅程 |
| 5 | 用比喻代描述 | 直接描述产品 | 用自然意象包裹产品 |

## 蕉下万能句式

- **「不是……而是……」** — 先否定旧预设，再给品牌新定义
- **修辞/比喻** — 参数变画面（「风是最好的造型师」）
- **「每一……都是……」** — 功能升维（「每一口呼吸都是松弛的味道」）

## 风格预设

| 预设 | 工程权重 | Allen 权重 | 适合 |
|---|---|---|---|
| `allen` | 50% | 50% | 品牌号、情感号、生活号 |
| `engineer` | 100% | 0% | 干货号、教程、工具测评 |
| `balanced` | 70% | 30% | 综合个人号（默认） |

```bash
python3 scripts/assistant.py preset allen
```

## 工作流（全部走 assistant.py）

```bash
# 第一次
python3 scripts/assistant.py init --persona "30+ 干皮女生" --niche "护肤" \
    --baseline note1.md note2.json
python3 scripts/assistant.py preset allen

# 动笔前 2 分钟：热身 + 哲学
python3 scripts/assistant.py warmup
python3 scripts/assistant.py philosophy

# 每天写一条
python3 scripts/assistant.py today
python3 scripts/assistant.py drafts new --topic <主题>
python3 scripts/assistant.py write <主题>
python3 scripts/assistant.py coach-iterate <id>
python3 scripts/assistant.py publish <id>

# 看到爆款想学
python3 scripts/assistant.py reverse --url <URL> --add-baseline

# 周末
python3 scripts/assistant.py review
python3 scripts/assistant.py learn disable=emoji
python3 scripts/assistant.py evolve
```

## 数据资产

`data/` 目录包含 11 份对人和 Claude 都可读的资产：

| 文件 | 内容 |
|------|------|
| `creative_philosophy.md` | **五层创作哲学**（v3.7 新增） |
| `allen_method.md` | Allen 三课五技法 + 17 案例 |
| `dongdongqiang_book.md` | 东东枪 99 篇要点 + 32 金句 |
| `algorithm_guide.md` | 小红书算法指南 2025-2026 |
| `copywriting_frameworks.md` | 蕉下句式 + 东东枪框架 |
| `scene_library.md` | ~200 场景画面库 |
| `case_library/` | 9 真实案例（v3.7 扩至 9） |
| `ai_speak_patterns.json` | AI 腔黑名单（含 Jarvis 攻略句式） |
| `seasonal_themes.md` | 24 节气借势画面库 |
| `title_templates.md` | 标题公式 11 种 |
| `content_structures.md` | 正文骨架 7 种 |

## 个人档案位置

```
~/.xiaohongshu/
├── posts.jsonl / snapshots.jsonl
├── drafts/<id>/v01.md, v02.md, ...
└── profile/
    ├── style.json / rules.json
    ├── baseline/ feedback.jsonl
    ├── iter_sessions/
    └── reviews/
```

## 红线 — 出现这些立刻停

| 信号 | 为什么是红线 |
|------|------------|
| 「我先快速写一篇看看」 | 没跑 philosophy.py 8 问 = 大概率攻略型 |
| 「这篇不用教练，我直接发」 | coach-iterate 是技能核心，跳过 = 白用 |
| 「道理我都知道」 | Jarvis 陷阱——认知到位但输出没跟上 |
| 「这次时间紧就不查功课了」 | 不查品牌官方定位 = 从零发明产品 = 0 分 |
| 「用 AI 改一下吧」然后不审 | critique.py --rewrite 后必须人工改 |
| 连续两篇用同一批意象 | 场景库窄——去 scene_library 换 3 个画面 |
| 满屏「提升/优化/赋能」 | AI 腔——跑 critique.py 自检 |
| 标题前 13 字没关键词 | 搜索权重丢 40% |

## 常见错误

| 错误 | 正确 |
|------|------|
| 开头挖痛点制造焦虑 | 重新定义/轻快切入 |
| 给读者列动作清单（1）2）3） | 展示画面「有人在...」 |
| 以作者口吻说话 | 引用真实用户或朋友口吻 |
| 结尾中规中矩收口 | 让读者感觉被珍视 |
| 写产品前不查官方定位 | 先做功课，理解品牌怎么定义自己 |
| 节气文案堆砌所有元素 | 只取一个零件，深度挖掘 |
| 金句后面跟解释 | 金句独立成段，不解释 |
| 比喻带「就像...一样」 | 直接比喻，不铺垫 |

## 浏览器桥接（v3.9 起，v3.10 加固）

通过 CDP 控制真实 Chrome 安全浏览小红书，一次扫码长期登录。

```bash
python3 scripts/browser_bridge.py start      # 启动浏览器 + 扫码登录
python3 scripts/browser_bridge.py health     # 全套体检（v3.10：连接/登录/配额/熔断/指纹）
python3 scripts/browser_bridge.py quota      # 日配额状态（v3.10）
python3 scripts/browser_bridge.py explore    # 看探索页推荐笔记
python3 scripts/browser_bridge.py search <k> # 搜索笔记
python3 scripts/browser_bridge.py note <url> # 看单篇笔记内容
python3 scripts/browser_bridge.py analyze <url> # 对标拆解（含 Allen 6 维诊断）
```

**安全保护（硬编码 11 道闸门）：**
- 真实 Chrome 指纹：未传 `--enable-automation`，`navigator.webdriver=false`，无 cdc_* 标记
- TLS/JA3：Chrome 原生握手，非 requests/curl
- 拟人延迟 2~10s + 模拟自然滚动
- 会话上限 30 次 / **日配额 100 次**（v3.10）
- 熔断 30 分钟（460/461/403/406/captcha/300017/访问异常）
- 夜间休眠 0:00-6:00 + **晨间缓冲 6:00-7:00**（v3.10：仅 status/health/quota）
- **指数退避**（v3.10）：连续 3 次空响应 → 翻倍延迟，上限 30s
- CDP 命令最小化：只发 Runtime.evaluate
- Profile 持久化避免空 Profile 检测
- **指纹自检**（v3.10）：`health` 透明显示 webdriver/cdc/plugins/canvas/UA 等检测点，自己暴露问题
- 只读不写（不点赞/评论/关注/发布/私信）

## 不做什么

❌ 自动发布 / 多账号矩阵 / AI 生图 / 一键全文 / 达人投放分析
❌ 浏览器自动点赞/评论/关注（只读浏览）

## 防封号红线

1. 用自己的 Cookie，脚本不做登录自动化
2. 每次请求 2~10 秒延时（带退避），单会话 30 次封顶
3. 460/461/403/406/captcha/300017 → **立即停 30 分钟**（自动熔断）
4. 不翻页批量抓
5. **日请求 ≤ 100 次**（v3.10 起硬配额，超限拒绝执行）
6. 0:00-6:00 不操作；6:00-7:00 仅 status/health/quota（v3.10）
7. 出门前先跑 `health` 看暴露面 + `quota` 看剩余额度

---

**重要免责：** 仅用于合规、针对公开可见内容的个人调研与创作辅助。
请尊重 xiaohongshu.com 的服务条款。**绝不**支持商业批量采集 / 内容搬运 / 绕过风控 / 自动化互动。

**技术支持：** 青岛火一五信息科技有限公司

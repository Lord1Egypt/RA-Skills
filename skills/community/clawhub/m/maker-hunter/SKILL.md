---
name: maker-hunter-v2
description: 自动发现并精准招募 vibe coding 创业者。用于：当需要从技术社区（即刻、、Hacker News、X/Twitter 等）挖掘具备极客精神、会用 AI 工具编程、正在创业的年轻 maker，并生成个性化招募私信时。
---

# Maker Hunter V2

精准发现并招募 vibe coding 创业者的自动化工具。

## 1. 目标人群画像

**核心特征**：
- 极客精神：对技术有热情，喜欢折腾新工具
- Vibe Coding：熟练使用 AI 工具（Cursor、Windsurf、Claude Code 等）辅助编程
- 创业型：正在做自己的产品，有商业思维或已上线产品
- 年轻态：心态开放，愿意尝试新范式

**行为特征关键词**：
- #buildinpublic / #vibecoding / #indiehacker / #harness engineering
- 独立开发 / Solopreneur / Bootstrap
- AI 编程 / Prompt Engineering / Agent
- MVP / 产品思维 / 商业化

**排斥特征**：
- 纯打工心态、无个人项目
- 只发招聘帖的 HR
- 推广自家产品的营销号
- **知名公司高管（CEO/CTO/VP等）** - 这类人已是成功人士，不是目标人群
- 匹配分数低于 70%

---

## 2. 每日任务目标

| 平台 | 最低要求 |
|------|----------|
| **总计** | **20 个匹配度 >= 70% 的候选人** |
| 即刻 | 需要登录 |
| Hacker News | API 可用 |
| X/Twitter | 需要登录 |

**规则：**
- 匹配度分数 < 70% → 直接淘汰，不计入20人
- 高管（CEO/CTO/VP等）→ 直接淘汰，不计入20人
- 不够20人则继续抓取，直到凑齐

---

## 3. 平台策略与抓取方式

**浏览器说明：**
- 使用 Chrome 浏览器（系统已检测到 `/Applications/Google Chrome.app`）
- 使用 `browser` 工具控制浏览器

### 中国平台

| 平台 | 优先级 | 抓取方式 | 授权要求 |
|------|--------|----------|----------|
| **即刻** | P0 | 浏览器（Chrome） | 需要登录 |

### 外国平台

| 平台 | 优先级 | 抓取方式 | 授权要求 |
|------|--------|----------|----------|
| **Hacker News** | P0 | API | 无需登录 |
| **X/Twitter** | P1 | 浏览器（Chrome） | 需要登录 |

---

## 4. 用户资料审核流程（重要！）

**不仅要看帖子，还要看用户主页和历史帖子！**

### 审核步骤

1. **发现目标帖子** → 从关键词匹配的文章中发现潜在候选人
2. **访问用户主页** → 点击作者链接，进入其个人主页
3. **浏览历史帖子** → 查看最近 5-10 条历史帖子内容
4. **综合判断** → 根据历史内容判断是否符合目标画像

### 判断标准

**符合条件**：
- 历史帖子多次提到自己在做产品/项目
- 有产品链接、GitHub、正在开发中的内容
- 多次参与 vibe coding、AI 编程讨论
- 有独立开发、创业相关分享

**不符合条件**：
- 只转发/搬运内容，无个人创作
- 纯吐槽/抱怨类帖子
- 只发招聘帖或求工作帖
- 营销号/推广号
- **已知公司高管（CEO/CTO/COO/VP/Founder等）** - 这类人已经是成功人士，不符合独立开发者画像

### 高管检查（重要！）

每个候选人必须检查是否为知名公司高管：

1. **查看个人主页简介** - 是否有 CEO、CTO、Founder、Co-founder 等title
2. **搜索社交媒体** - 查看 LinkedIn、Twitter 等是否有公司职级信息
3. **查看历史帖子** - 是否多次提到自己创业成功、公司规模等

**如果是高管，直接跳过，不放入候选人名单**

---

## 5. 每日任务执行

### 目标
- **中国区：即刻找到 10 人**
- **外国区：Hacker News + X/Twitter 找到 10 人**
- **总计：20 人**

### 执行流程（串行执行）

```
【第一步：中国区】
1. 读取 memory/founders.json 获取历史名单
2. 读取 memory/daily.json 获取今日已处理
3. 立即主动打开浏览器，让用户登录即刻
4. 等待用户登录成功后，抓取即刻
5. 过滤：匹配度<70%淘汰、高管淘汰
6. 累加计数，达到10人后进入下一步

【第二步：外国区】
7. 让用户登录 X/Twitter
8. 等待用户登录成功后，抓取 Hacker News + X/Twitter
9. 过滤：匹配度<70%淘汰、高管淘汰
10. 累加计数，达到10人后进入下一步

【第三步：输出】
11. 在对话框输出完整候选人名单（20人）
```

### 浏览器登录流程

**【第一步】先打开即刻登录页面**
```
1. 使用 browser 工具打开 https://m.okjike.com/login
2. 提示用户："请登录即刻"
3. 等待用户登录完成
4. 登录成功后开始抓取即刻
```

**【第二步】再打开 X/Twitter 登录页面**
```
1. 使用 browser 工具打开 https://x.com/login
2. 提示用户："请登录 X/Twitter"
3. 等待用户登录完成
4. 登录成功后开始抓取
```

### 输出要求

任务完成后，在对话框输出完整 20 人名单：
- 中国区 10 人（即刻）
- 外国区 10 人（Hacker News + X/Twitter）

---
    foreign: foreignCandidates.slice(0, FOREIGN_TARGET)
  };
}
```

---

## 6. 去重机制

- **去重键**：`平台 + 用户名` 组合唯一
- **历史库**：memory/founders.json 存放全部历史候选人
- **今日库**：memory/daily.json 存放今日任务结果

### 去重检查实现

```javascript
// 构建当前候选人的去重键
const dedupKey = `${platform}:${username}`;

// 加载历史记录
const founders = JSON.parse(readFile('memory/founders.json'));
const daily = JSON.parse(readFile('memory/daily.json'));

// 构建已存在键的 Set
const seenKeys = new Set([
  ...founders.candidates.map(c => `${c.platform}:${c.username}`),
  ...daily.candidates.map(c => `${c.platform}:${c.username}`)
]);

// 检查是否重复
if (seenKeys.has(dedupKey)) {
  console.log(`跳过重复: ${dedupKey}`);
  continue;
}
```

---

## 7. 输出格式（重要！）

### 中国候选人（中文私信）

```json
{
  "region": "china",
  "platform": "即刻",
  "user_id": "12345678",
  "username": "用户的即刻昵称",
  "profile_url": "https://m.okjike.com/users/12345678",
  "post_url": "https://m.okjike.com/posts/xxx",
  "post_title": "帖子标题",
  "match_score": 0.85,
  "profile_summary": "用户在主页的简介（如果有）",
  "history_review": "审核历史帖子后的总结，说明为何符合条件",
  "dm_content": "Hi {username}，看到你在即刻的帖子《{post_title}》{共鸣句}。\n\n{具体评价}。\n\n我们正在做一个___社区/项目，感觉你的___经历很适合一起聊聊。有兴趣可以加个微信或回复这封邮件。\n\n期待交流！"
}
```

### 外国候选人（英文私信）

```json
{
  "region": "foreign",
  "platform": "",
  "user_id": "user123",
  "username": "user123",
  "profile_url": "https://www..com/user/user123",
  "post_url": "https://www..com/r/indiehackers/comments/xxx",
  "post_title": "Post Title",
  "match_score": 0.85,
  "profile_summary": "User's bio if available",
  "history_review": "Summary of profile review, explaining why they match",
  "dm_content": "Hi {username}, saw your post on {platform} - \"{post_title}\". {Resonance sentence}.\n\n{your specific observation}. {highlight quote}.\n\nWe're building a ___ community/project and think your ___ experience would be a great fit. Happy to chat if you're interested.\n\nLooking forward to connecting!"
}
```

### 私信生成规则

**中文模板（即刻）**：
```
Hi {username}，看到你在{平台}的帖子《{post_title}》{共鸣句}。

{具体评价}，{亮点引用}。

我们正在做一个面向独立开发者的社区/项目，感觉你的{经历}很适合一起聊聊。有兴趣可以加个微信或者回复这封邮件。

期待交流！
```

**英文模板（Hacker News//X）**：
```
Hi {username}, saw your post on {platform} - "{post_title}". {Resonance sentence}.

{your specific observation}. {highlight quote}.

We're building a community for indie developers and think your {experience} would be a great fit. Happy to chat if you're interested.

Looking forward to connecting!
```

**共鸣句库**：
- 中文：很有共鸣、这个思路很棒、太同频了、很有启发
- English: Really resonated with this, Great approach, Totally in sync, This is inspiring

**关键点**：
- 即刻用户 → 用中文写私信
- 外国平台用户 → 用英文写私信
- 私信必须提及帖子具体内容，证明认真读过
- 根据用户历史帖子内容定制化修改

---

## 8. 输出要求（重要！）

**每次任务必须同步输出完整候选人名单到对话框！**

### 输出要求
- 任务完成后立即在对话框输出
- 显示全部 20 个候选人的完整信息
- 每个候选人包含：平台、用户名、帖子链接、私信内容、匹配度
- 匹配度 < 70% 的不显示（已淘汰）

### 输出格式

```
=== 今日候选人 ===

🇨🇳 中国区（即刻）- X/10人

1. @用户名
   平台：即刻
   帖子：https://...
   私信：[中文私信内容]
   匹配度：XX%

🌍 外国区 (Hacker News / X/Twitter) - X/10人

1. @用户名
   平台：Hacker News
   帖子：https://...
   私信：[英文私信内容]
   匹配度：XX%
```

### 输出要求

- 每次运行后必须展示完整名单
- 私信内容必须完整显示（不要省略）
- 中国区用中文，外国区用英文
- 包含匹配度分数

---

## 8. 记忆系统

### 文件结构

```
~/.config/openclaw/maker-hunter/
├── credentials.json    # 平台凭证
└── memory/
    �}    ├── founders.json   # 历史候选人库
    └── daily.json      # 今日任务记录
```

### founders.json 格式

```json
{
  "version": 1,
  "updated_at": "2026-03-18T10:00:00Z",
  "candidates": [
    {
      "region": "china",
      "platform": "即刻",
      "user_id": "12345678",
      "username": "用户昵称",
      "profile_url": "https://m.okjike.com/users/12345678",
      "found_at": "2026-03-18",
      "post_url": "https://m.okjike.com/posts/xxx"
    }
  ]
}
```

### daily.json 格式

```json
{
  "date": "2026-03-18",
  "target_china": 10,
  "target_foreign": 10,
  "found_china": 10,
  "found_foreign": 10,
  "candidates": [...]
}
```

---

## 9. 平台抓取详情

### 即刻 (P0 - 需 cookie)

**状态**：需要用户登录后提供 cookie

**登录流程**：
```
1. 浏览器登录即刻
2. 打开开发者工具 (F12) → Application → Cookies
3. 复制 cookie 值提供给我
```

**关键词**：
- 独立开发、AI 编程、vibe coding、创业、产品思维

### Hacker News (P0)

**端点**：`https://hacker-news.firebaseio.com/v0/`

**抓取逻辑**：
1. 获取 Top Stories ID 列表 (`topstories.json`)
2. 取前 50 条获取详细内容 (`item/{id}.json`)
3. 过滤匹配关键词的帖子

**关键词**：vibe coding, AI coding, indie hacker, build in public, startup

###  (P0)

**端点**：`https://www..com/r/{sub}/new.json`

**目标 sub**：
- r/indieweb
- r/startups
- r/indiehackers

**关键词**：vibe coding, AI coding, indie hacker, solo founder, MVP, launch

### X/Twitter (P1 - 需浏览器登录)

**状态**：需要用户登录后才能抓取

**登录流程**：
```
1. 使用 browser 工具打开 https://x.com/login
2. 用户扫码/输入账号密码完成登录
3. 登录成功后搜索：build in public indie hacker vibe coding
```

---

## 10. 评分机制

每个候选人计算 match_score (0-1)：

| 因素 | 权重 | 说明 |
|------|------|------|
| 关键词匹配 | 0.3 | 帖子含目标关键词数量 |
| 个人主页审核 | 0.4 | 主页介绍是否符合 |
| 历史帖子审核 | 0.3 | 历史帖子是否符合目标画像 |

分数 > 0.7 才输出。

---

## 11. 执行命令

手动执行每日任务：

```bash
# 直接运行脚本
node ~/.npm-global/lib/node_modules/openclaw/skills/maker-hunter-v2/scripts/hunter.cjs
```

首次使用需要创建 memory 目录：

```bash
mkdir -p ~/.config/openclaw/maker-hunter/memory
```

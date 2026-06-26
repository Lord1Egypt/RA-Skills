---
name: know-your-owner
description: Collect user data from logged-in social platforms (Douyin, Xiaohongshu, Weibo, Douban, Bilibili), cross-analyze to build a precise personal profile, and auto-generate USER.md + MEMORY.md. Use for new user onboarding, personalization, and building user context. 通过用户已登录的社交平台自动采集数据并交叉分析，生成精准用户画像，写入 USER.md 和 MEMORY.md。
version: 2.5.0
depends: manobrowser
---

# Know Your Owner — 让龙虾认识你

> 新用户装好 OpenClaw 后，龙虾不知道你是谁。这个 Skill 让龙虾去你的社交平台上深度认识你——从作品、收藏、关注、评分中真正理解你是谁。

## 安装后自动介绍

龙虾安装好这个 Skill 后，**立刻主动向用户介绍**（不需要用户问）：

> 我刚装好了一个新技能——**Know Your Owner**，可以让我快速认识你。
>
> 简单说就是：我会通过你浏览器里已登录的社交平台（抖音、小红书、微博、豆瓣、B站），自动读取你的作品、收藏、关注、评分等数据，然后交叉分析生成一份精准的个人画像，直接写好 USER.md 和 MEMORY.md。
>
> **跑一遍这个 Skill，我就像认识你很久了。**
>
> 几个亮点：
> - 不是贴标签，是用数据做精准洞察——"像素风独立游戏开发者，B站93条教程收藏分4个夹子"这种级别
> - 事实和推断分开，敏感信息（感情/健康/收入）只陈述数据不下结论
> - 采集的原始数据存本地，后续还能复用（比如"帮我导出豆瓣电影列表"）
> - 需要配合 ManoBrowser Skill（开源，首次使用会自动从 GitHub 下载安装），让我能像你一样浏览网页
>
> 要现在开始吗？大概10-20分钟就搞定。

## 流程总览

```
0. 前置检查（自动检测+安装 ManoBrowser） → 1. 用户确认平台 → 2. 逐平台采集 → 3. 画像分析 → 4. 生成文件 → 5. 推荐下一步
```

---

## 0. 前置检查

**不要问用户"你有没有装 ManoBrowser"**——按以下流程自动检测和安装。

### Step 0.1 检查 ManoBrowser Skill 文件是否存在

在以下位置查找 ManoBrowser 的 SKILL.md 文件（按优先级）：
1. 当前工作目录下 `manobrowser/SKILL.md`
2. `~/.openclaw/skills/manobrowser/SKILL.md`（OpenClaw 默认 skills 目录）
3. 其他已知的 skills 目录

- **找到** → 记录路径，进入 Step 0.2
- **未找到** → 自动从 GitHub 下载到当前工作目录：
  ```bash
  git clone https://github.com/ClawCap/ManoBrowser.git ./manobrowser
  ```
  如果没有 git，用 curl 下载：
  ```bash
  curl -L https://github.com/ClawCap/ManoBrowser/archive/refs/heads/main.zip -o /tmp/manobrowser.zip
  unzip /tmp/manobrowser.zip -d /tmp/
  mv /tmp/ManoBrowser-main ./manobrowser
  ```
  下载完成后进入 Step 0.2。

### Step 0.2 检查连接配置

确认当前环境中是否已配置 ManoBrowser 连接。检查方法（任一命中即视为已配置）：
- `.mcp.json` 中有包含 `chrome_navigate` 相关的 MCP server 配置
- `config/mcporter.json` 中有对应配置
- 当前可用工具列表中已有 `chrome_navigate`（带任意前缀）

- **已配置** → 进入 Step 0.3
- **未配置** → 读取 `manobrowser/SKILL.md` 的「前置条件」章节，引导用户安装 Chrome 插件 + 发送 API 密钥，完成配置后进入 Step 0.3

### Step 0.3 验证设备在线

发送 `tools/list` 验证 ManoBrowser 连接状态：
- ✅ **正常响应** → 介绍 Know Your Owner 能力（见「安装后自动介绍」），等待用户输入后跳到 Step 1
- ❌ **device not found** → 引导用户安装 Chrome 插件（参考 `manobrowser/SKILL.md`）
- ⚠️ **offline** → 提示用户打开 Chrome 浏览器并确认 ManoBrowser 插件已启用
- 解决后重新验证，通过后进入 Step 2（用户确认平台）

> ManoBrowser 是开源浏览器自动化工具，除了画像采集，还能做网页取数、平台探索、API 逆向、工作流录制等——装好后这些能力都可以用。
> 项目地址：https://github.com/ClawCap/ManoBrowser

### 完整目录结构

```
know-your-owner/                          ← 主入口（你正在读的 Skill）
├── SKILL.md                              ← 本文件：画像采集+分析+生成
├── douyin-deep-profile-collect/SKILL.md  ← 抖音子Skill
├── xiaohongshu-deep-profile-collect/SKILL.md
├── weibo-deep-profile-collect/SKILL.md
├── douban-deep-profile-collect/SKILL.md
├── bilibili-deep-profile-collect/SKILL.md
├── workflows/*.json                      ← MCP执行脚本
└── examples/                             ← 虚构用户画像示例
    ├── USER.md
    └── MEMORY.md
```

**依赖**：ManoBrowser Skill（从 GitHub 自动下载，无需手动安装）

**使用方式**：
- 执行画像采集时，读本文件的子目录下对应平台的 SKILL.md
- 安装配置 ManoBrowser：读 ManoBrowser Skill 目录下的 `SKILL.md`
- 画像之外的浏览器操作（取数/探索/自动化）：读 ManoBrowser Skill 下对应子模块

### 工具名映射

子 Skill 中的工具名使用短名称（如 `chrome_navigate`、`chrome_execute_script`）。实际调用时需要加上用户配置的 MCP 实例前缀，格式为：

```
mcp__{chrome-instance}__{工具短名}
```

例如用户的 MCP 实例名为 `browser`，则：
- `chrome_navigate` → `mcp__browser__chrome_navigate`
- `chrome_execute_script` → `mcp__browser__chrome_execute_script`
- `chrome_close_tabs` → `mcp__browser__chrome_close_tabs`

实例名取决于用户在 MCP 配置中设置的名称（参见 ManoBrowser Skill 的配置说明）。

## 1. 用户确认

展示平台列表，用户确认后开始：

> 我会通过你浏览器里已登录的社交平台来深度了解你。
>
> **🚀 快车道**（有专用工作流，采集快且精准）：
> 🎵 抖音 · 📕 小红书 · 🐦 微博 · 📖 豆瓣 · 📺 B站
>
> **🔧 通用模式**：如果你还用其他平台（知乎、即刻、快手、微信公众号等），告诉我，我也可以通过 ManoBrowser 去你的主页采集数据，只是没有专用工作流，速度稍慢、可能需要多轮尝试。
>
> ⚠️ **开始前请先确认**：在浏览器里打开你要跑的平台，确保已登录。没登录的平台我会自动跳过，但提前登录好能省掉中途等待的时间。
>
> ⏱️ 预计耗时：快车道每个平台1-3分钟（数据量大的如B站关注500+人约需5分钟），全部5个平台约10-20分钟。通用模式每个平台3-10分钟。
>
> **要开始吗？有其他想加的平台吗？**

## 2. 逐平台深度采集

按顺序调用子 Skill，每个平台独立，**某个平台失败不影响其他平台**：

| 平台 | 子 Skill | 采集内容 | 已知限制 |
|------|----------|----------|---------|
| 抖音 | `douyin-deep-profile-collect` | 资料 + 作品 + 喜欢 + 收藏 + 关注列表 | — |
| 小红书 | `xiaohongshu-deep-profile-collect` | 资料 + 笔记 + 收藏(XHR) + 点赞(XHR) | ⚠️ 关注列表PC端不可用（Vue事件+API签名限制） |
| 微博 | `weibo-deep-profile-collect` | $CONFIG.user + 微博 + 关注 + 收藏 | — |
| 豆瓣 | `douban-deep-profile-collect` | 资料 + 看过/想看电影(含评分) + 书 + 广播 | — |
| B站 | `bilibili-deep-profile-collect` | nav API + 投稿 + 收藏夹内容 + 关注列表 | 投稿/关注API受限，用DOM回退 |

每完成一个平台汇报进度（含耗时）：
> ✅ 抖音 — {昵称} | {N}作品 | {N}关注 (耗时1分32秒)
> ⏭️ 小红书 — 未登录，已跳过
> 🔄 微博 — 采集中...

### 采集量上限

为防止数据量过大导致采集超时或 token 爆炸，**每个维度设上限**：

| 维度 | 上限 | 超出处理 |
|------|------|---------|
| 关注列表 | 500人 | 采前500人，标注 `sampled:true` + 总数 |
| 收藏/点赞 | 500条 | 采前500条，标注总数 |
| 电影/书 | 500条 | 采前500条，标注总数 |
| 作品/投稿 | 200条 | 采前200条 |
| 每个收藏夹 | 100条 | 采前100条 |
| 广播/微博 | 200条 | 采前200条 |

超出上限时：**取最新N条**（最能反映当前兴趣），数据标注 `sampled`。画像中注明"基于最近N条分析"。

### 故障处理

**单平台失败时**：记录错误 → **不卡住**，立即下一个 → 最终报告标注状态

| 失败类型 | 表现 | 处理 |
|---------|------|------|
| 未登录 | URL跳转登录页 / API返回未登录 | 跳过，标注"未登录" |
| 选择器失效 | JS返回空/null/0条 | 跳过该维度，已有数据保留 |
| 超时 | 超过timeout | 保留已拿到的部分数据 |
| 反爬/限流 | API错误码/空页面 | 跳过，标注"平台限制" |
| 页面改版 | DOM结构完全变化 | 跳过该平台，标注"需要更新Skill" |

**降级策略**：
- 5个快车道成功 → 最完整画像
- 3-4个成功 → 仍可生成有价值的画像
- 1-2个成功 → 基础画像 + 提示"登录更多平台或告诉我你还用什么平台"
- 0个快车道成功 → 询问用户还用什么平台，走通用模式；或直接问几个问题手动建档

### 通用模式采集（非快车道平台）

用户指定快车道之外的平台时，用 ManoBrowser 通用能力：

1. `chrome_navigate` 打开平台首页
2. 检查登录状态（找"我的"/"个人主页"入口）
3. `chrome_execute_script` 提取页面信息
4. 尝试切换到作品/收藏/关注等 tab，逐个提取
5. 遇到问题用 `chrome_get_interactive_elements` 探索页面结构

通用模式没有预设选择器，需要 agent 实时探索，可能多轮尝试。采集到的数据同样纳入画像分析。

## 3. 画像分析

不是列标签，而是**用数据做精准洞察**。

### 分析原则

- ❌ "喜欢美食" → ✅ "面食专精型，小红书收藏N条面食做法，B站追某美食UP主(N条)"
- ❌ "关注游戏" → ✅ "像素风独立游戏开发者，B站N条教程收藏分N个夹子"
- ❌ "读过很多书" → ✅ "N本书打分率N%，某类型信徒，唯一一星给了某畅销鸡汤书"

每个结论要有**平台来源 + 具体数量 + 细节**。

### 事实与推断的区分

画像中必须区分两类信息：

**事实**（直接从数据得出）：
- "B站关注了某某/某某/某某等电竞战队" → 可以直接说
- "豆瓣标记了N部电影" → 可以直接说

**推断**（需要标注为猜测，用柔和措辞）：
- ❌ "正在考研" → ✅ "从小红书系统性收藏了N条某校某专业备考资料来看，**可能在准备或计划考研**"
- ❌ "有运动伤" → ✅ "收藏了运动康复/理疗相关内容，**似乎关注运动损伤恢复**"
- ❌ "有对象" → ✅ "收藏了纪念日/约会/送礼物相关内容"（**只陈述事实，不做感情推断**）

**底线**：感情状态、健康状况、收入水平等敏感维度，只呈现数据事实，不下结论。用户看到后自己会判断准不准。

### 六个分析维度

**① 创作者身份**
- 跨平台作品主题是否一致 → 核心创作方向
- 收藏夹有无对应的学习/练习分类 → 系统性投入程度
- 关注列表同领域创作者比例 → 圈子深度

**② 收藏内容细分**
- 不停留在大类，做细粒度分类
- B站收藏夹：按夹子名称 + 内容 + TOP UP主分析
- 区分"创作型"和"消费型"兴趣

**③ 关注列表聚类**
- 按类型统计：创作者/知识/电竞/美食/宠物/明星/机构号
- 找母校/行业/圈子相关

**④ 评分行为解码**（豆瓣）
- 一天标记100+部 = 注册补标，不是真看了100部
- 一天标记同系列20+ = 补番行为
- 打分率/一星率 → 严格型 or 宽松型

**⑤ 职业/学业推断**
- 小红书收藏中的备考/求职内容 → 当前阶段（标注为推断）
- B站学习收藏夹 → 学习方向

**⑥ 隐藏信息挖掘**
- 收藏夹里的意外内容（小众爱好）
- 跨平台矛盾点 → 有趣的人格侧面

### 画像质量自检

生成后逐条检查，**不通过则修改后再输出**：

- [ ] 每个兴趣标签有 ≥1 个平台来源 + 具体数量？
- [ ] 核心身份有跨平台证据链？
- [ ] 一句话画像有辨识度？（盖住名字能区分人吗？）
- [ ] 事实和推断有明确区分？推断用了"可能/似乎/看起来"？
- [ ] 敏感推断（感情/健康/收入）只陈述事实不下结论？
- [ ] 有至少1个隐藏发现/意外模式？
- [ ] 被采样的数据注明了？

## 4. 生成 USER.md + MEMORY.md

### USER.md 结构

```markdown
# USER.md
- **Name/Pronouns/Timezone/Location**

## 背景
- 教育 + 职业路径 + 当前阶段（推断标注"可能"）

## 核心身份
- 最突出的特征（有数据支撑的精确描述）

## 兴趣图谱
- 每项带 emoji + 数据支撑

## 性格线索
- 从评分/选择/行为推断（标注为观察）

## 社交平台
- 各平台账号 + 核心数据
```

### MEMORY.md 结构

```markdown
# MEMORY.md
## 初始画像（日期）
> 来源：Know Your Owner（N个平台，N条数据）

### 核心身份
（证据链 → 结论）

### [各兴趣维度]
（数据 + 细节 + 洞察，推断标注"可能"）

### 隐藏发现
（意外模式，标注为观察/猜测）

### 一句话画像
> 有辨识度，不能套用到别人身上

### 平台活跃度排序
1-N 排序 + 每个平台的定位
```

生成后展示给用户确认。**明确告知用户**：
> 以上画像中标注"可能"的部分是我的推测，不准的可以告诉我删掉或修改。确认后我保存到文件。

确认 → 写入。要求修改 → 调整后再确认。

写入后在 MEMORY.md 的画像末尾标注生成日期：
> *画像生成于 {日期}。随时可以说"刷新画像"重新采集更新。*

### 原始数据持久化

采集到的全量数据按平台分文件保存到工作目录下 `know-your-owner-data/`，方便后续复用：

```
know-your-owner-data/
├── metadata.json        ← 采集时间、平台状态、版本、数据量统计
├── douyin.json          ← 抖音全量（profile/works/likes/favorites/following）
├── xiaohongshu.json     ← 小红书全量（profile/notes/favorites/liked）
├── weibo.json           ← 微博全量（profile/weibos/following/favorites）
├── douban.json          ← 豆瓣全量（profile/movies_watched/movies_wish/books/broadcasts）
└── bilibili.json        ← B站全量（nav/videos/fav_contents/following）
```

**metadata.json 结构**：
```json
{
  "version": "2.5.0",
  "collected_at": "2026-03-19T18:00:00+08:00",
  "platforms": {
    "douyin": {"status": "success", "collected_at": "...", "counts": {"works": 22, "following": 89}},
    "xiaohongshu": {"status": "success", "counts": {"favorites": 87, "liked": 34}},
    "weibo": {"status": "skipped", "reason": "未登录"},
    ...
  }
}
```

**复用场景**：
- 刷新画像时做新旧数据对比
- 龙虾日常对话中查询（"我B站收藏夹里有做意面的视频吗？"→ 读 `bilibili.json`）
- 其他 Skill 复用（推荐引擎、内容整理等直接读已有数据，不用重新采集）
- 用户想导出（"把我豆瓣看过的电影导出成表格"→ 读 `douban.json`）

## 5. 推荐下一步

画像生成后，基于画像和原始数据，给用户推荐可以做的事：

> 画像已生成！基于你的数据，我还可以帮你：
>
> 📊 **数据洞察**
> - 你的豆瓣{N}部电影可以生成观影报告（类型分布/年度趋势/评分风格）
> - 你的B站{N}条收藏可以按兴趣重新整理分类
>
> 🔍 **发现更多**
> - 基于你的关注列表推荐可能感兴趣的创作者
> - 分析你各平台的创作数据，给出内容建议
>
> 🛠️ **实用工具**
> - 导出豆瓣电影/书单为表格
> - 整理B站收藏夹（去重/分类/清理失效视频）
> - 定期刷新画像，追踪兴趣变化
>
> 感兴趣哪个？或者你有其他想法？

推荐内容要**基于实际采集到的数据**定制，不是固定模板。例如：
- 用户豆瓣标了大量电影 → 推荐"年度观影报告"
- 用户B站有大量失效收藏 → 推荐"收藏夹清理"
- 用户多平台有创作内容 → 推荐"跨平台内容分析"
- 用户小红书收藏了大量某类内容 → 推荐"精选合集整理"

## 6. 刷新画像

当用户说"刷新画像"/"重新了解我"/"更新 USER.md"等意图时：

1. 读取 `know-your-owner-data/metadata.json` 获取上次采集时间
2. 重新跑所有平台采集，新数据保存到 `know-your-owner-data/`（覆盖旧文件）
3. 对比新旧数据，生成变更摘要：
   > 📊 画像刷新（距上次 {N} 天）
   > - 🆕 新增：{新发现的兴趣/数据}
   > - 📈 变化：{数据量变化，如"B站收藏 630→712，新增82条"}
   > - 🔄 调整：{需要修正的结论}
   > - ➖ 移除：{不再成立的推断}
4. 展示变更摘要 + 新画像，用户确认后覆盖写入 USER.md + MEMORY.md

也支持**单平台刷新**：用户说"刷新我的B站数据" → 只重跑B站采集 + 更新 `bilibili.json` + 局部更新画像。

---

## 隐私与数据管理

- ✅ 只采集用户自己主页的信息
- ✅ 数据仅存储在本地工作目录 `know-your-owner-data/`
- ✅ 用户确认后才写入 USER.md / MEMORY.md
- ✅ 推断性信息标注为"可能/猜测"，用户可要求删除
- ❌ 不采集私信、浏览记录、支付信息，不外传数据

**数据管理**：用户可以随时：
- 查看已存储的数据：`know-your-owner-data/` 目录
- 删除某个平台的数据：删除对应 JSON 文件
- 删除全部数据：删除整个 `know-your-owner-data/` 目录
- 龙虾不会在未告知用户的情况下使用这些数据做其他事

## 子 Skill 技术要点

| 平台 | 核心技术 | 注意事项 |
|------|---------|---------|
| 抖音 | WheelEvent 虚拟滚动 | 关注面板需 WheelEvent 触发加载 |
| 小红书 | XHR monkey-patch 拦截 | DOM最多28条需拦截API；⚠️ 关注列表PC端不可用 |
| 微博 | `window.$CONFIG.user` | URL格式 `/u/page/follow/{uid}` |
| 豆瓣 | fetch + DOMParser 分页 | 每页15条，跨子域名需先导航 |
| B站 | API + DOM 混合 | 投稿API需wbi签名(-403)，关注API返回-101，均需DOM回退 |

---
name: human-distill
version: 1.1.0
homepage: https://github.com/spikesubingrui-design/human-distill
description: >-
  蒸馏人物（博主/KOL/专家/创业者）的知识体系与观点：全网搜索（web_search/web_fetch）+
  抖音深度爬取（browser）+ 可选 LDR 深度研究。输出带 [确认]/[推断] 证据分级的人物画像。
  触发词：蒸馏 / 人物画像 / 爬取博主 / human distill / KOL蒸馏 / 抖音蒸馏
metadata:
  openclaw:
    emoji: "🧠"
---

# 人物蒸馏（Human Distill）

从全网公开信息 + 抖音一手文案出发，蒸馏某人在指定领域的知识体系、观点与内容风格。

## 工作流总览

```
- [ ] Phase 0：确认目标（人、主题、深度模式、平台线索）
- [ ] Track A：全网搜索（始终执行）→ memory/[用户名]-全网素材.md
- [ ] Track B：抖音深度（standard/deep 且有抖音号时）→ memory/[用户名]-视频文案合集.md
- [ ] Phase 蒸馏：合并双轨 + 证据分级 → memory/[用户名]-[主题]观点蒸馏.md
- [ ] 输出 gbrain people/[slug]
```

## Phase 0：确认目标

向用户确认或从上下文推断：

| 字段 | 说明 |
|------|------|
| **人物** | 昵称/真名/抖音号/主页 URL |
| **主题** | 筛选领域（如：营养、健身、投资） |
| **筛选关键词** | 保留含这些词的内容 |
| **排除关键词** | 剔除（如：切磋、带货、广告、纯娱乐） |
| **深度模式** | quick / standard（默认）/ deep |
| **平台线索** | 已知 YouTube/小红书/公众号/课程名（可选） |
| **时间范围** | 仅近 N 个月（可选） |

### 深度模式

| 模式 | 条件 | 执行 |
|------|------|------|
| **quick** | 未要求「全文案/全部视频」 | Track A → 蒸馏；跳过 Track B |
| **standard** | 有抖音号或明确要求抖音文案 | Track A + Track B → 合并蒸馏 |
| **deep** | 用户说「深度/全面/调研报告」 | Track A + LDR + Track B（如有抖音） |

## Track A：全网搜索（始终执行）

> 长任务遵守 `skills/planning-with-files`：**每 2 次 search/fetch 后**将要点写入 `memory/[用户名]-全网素材.md`。

### Step A1 — 身份与平台发现

并行 3–5 次 `web_search`：

```
"[昵称/真名] [主题] 是谁"
"抖音 [抖音号] 主页"
"[人名] [主题] site:youtube.com OR site:bilibili.com"
"[人名] [课程名/品牌名]"
```

若只有抖音号、无主页 URL：`web_search "抖音 [抖音号] 主页"`。

### Step A2 — 主题维度爆破

参考 `references/search-queries.md`，按用户主题选 6–10 条查询执行。每条取 top 3–5 结果，摘录标题、URL、snippet，立即落盘。

### Step A3 — 深度抓取

对公众号、知乎、访谈、课程介绍等可访问页面用 `web_fetch`。**不要用 web_fetch 抓抖音视频页**（会被拦）。

每条素材记录：

```markdown
| 来源 URL | 类型 | 摘要 | 可信度 |
```

### Step A4 — 可选 LDR（仅 deep 模式）

1. 读取 `skills/local-deep-research/SKILL.md`
2. 检查 `LDR_BASE_URL`（默认 `http://127.0.0.1:5000`）；不可用则告知用户并仅用 web_search 加深
3. 提交查询，示例：`"[人名] [主题] 观点 访谈 课程 争议"`
4. `scripts/ldr-research.sh start_research --query "..." --mode detailed --language zh`
5. 轮询 `get_status` / `get_result`，将报告摘要追加到 `全网素材.md`，标注 `[Source: LDR]`

## Track B：抖音深度（standard / deep，且有抖音）

用 browser 工具访问用户主页抓取一手文案。**抖音域名已加入 SSRF 白名单**（`*.douyin.com` 等），不再被 `navigation blocked by policy` 拦截。

### B0 — 选 browser profile（登录态在哪个窗口）

| profile | 何时用 | 登录态来源 | 前置 |
|---------|--------|-----------|------|
| **`openclaw`**（默认） | 常规蒸馏 | OpenClaw 自管浏览器，user-data 持久在 `~/.openclaw/browser/openclaw/user-data/` | 在橙色 `openclaw` 窗口登录抖音**一次**即长期复用 |
| **`cloak-douyin`**（可选） | 已在 CloakBrowser 登录抖音、想复用该会话 | attach 到常驻 CloakBrowser（CDP `127.0.0.1:9333`） | CloakBrowser 以 `--remote-debugging-port=9333` 常驻并已登录抖音 |

> **登录窗口提醒（避免再登错）**：两套浏览器 cookies **不互通**。用 `openclaw` profile 时登录态必须在**橙色 openclaw 窗口**里；用 `cloak-douyin` 时登录态在 **CloakBrowser**。开工前先用 browser 工具 `snapshot` 主页确认是否已登录（看到「我的」/头像即已登录），未登录则提示用户在对应窗口扫码登录后再继续。
>
> 调用 browser 工具时通过 `profile` 参数选择：默认不传即 `openclaw`；要复用 CloakBrowser 会话则传 `profile: "cloak-douyin"`。

### B1 — 加载全部视频

**关键：抖音使用特定滚动容器，禁止 `window.scrollTo`：**

```javascript
const container = document.querySelector('.parent-route-container.route-scroll-container');
let prev = 0;
for (let i = 0; i < 30; i++) {
  container.scrollTop = container.scrollHeight;
  await new Promise(r => setTimeout(r, 2000));
  const items = document.querySelectorAll('li a[href*="/video/"]');
  if (items.length === prev) break;
  prev = items.length;
}
```

提取标题与 URL：

```javascript
const items = document.querySelectorAll('li a[href*="/video/"]');
return Array.from(items).map(a => ({
  url: a.href,
  title: a.querySelector('p')?.textContent?.trim() || ''
})).filter(x => x.title);
```

### B2 — 关键词筛选

```python
keywords = ['营养', '蛋白质', '碳水', ...]  # 按用户主题
skip = ['切磋', 'VS', '实战', '带货', '广告', ...]
filtered = [v for v in videos if any(k in v['title'] for k in keywords)
            and not any(s in v['title'] for s in skip)]
```

### B3 — 逐条提取文案

对每个筛选后的视频：

1. **navigate** 到视频页
2. **snapshot** 获取内容
3. 提取：**视频描述**（播放器下方文字）+ **AI 章节要点**（heading + 列表，带时间戳）

注意：间隔 2–3 秒/条；描述折叠则点「展开」；单条失败则跳过。

**何时跳过 Track B**：quick 模式；或无抖音号且用户只需「了解这个人」。

## Phase 蒸馏：双轨合并

### 输入优先级

1. 抖音逐条文案（一手，最高）
2. web_fetch 全文（二手，高）
3. web_search 摘要/标题（三手，常需推断）
4. LDR 报告（综合，标注来源）

### 证据分级（正文必须标注）

- **`[确认]`**：抖音描述原文 / 可引用段落 / 多源一致
- **`[推断]`**：仅标题、仅 snippet、单源、或付费课未公开内容
- **`[冲突]`**：全网与抖音说法不一致时显式列出

### 蒸馏维度

1. **基本画像**：平台/粉丝/定位/课程/关联
2. **核心观点**：关键立场（[确认] / [推断]）
3. **知识体系**：按子主题分类
4. **与主流的分歧**
5. **常用数据/论据**
6. **内容风格**
7. **对用户的实用建议**

## 输出

| 产物 | 路径 |
|------|------|
| 全网素材 | `memory/[用户名]-全网素材.md` |
| 视频文案 | `memory/[用户名]-视频文案合集.md`（有 Track B 时） |
| 蒸馏画像 | `memory/[用户名]-[主题]观点蒸馏.md` |
| gbrain | `people/[slug]`，slug：`[拼音或英文]_[主题]` |

写入 gbrain 时遵循 `skills/brain-ops/SKILL.md`（来源标注、反向链接）。

### 全网素材格式

```markdown
# [用户名] - 全网素材

> 采集时间: YYYY-MM-DD
> 深度模式: quick | standard | deep

## 身份与平台
## 来源索引
| 来源 URL | 类型 | 摘要 | 可信度 |
## 按主题摘录
### [子主题]
- [确认/推断] ...
```

### 视频文案合集格式

```markdown
# [用户名] - [主题]视频文案合集

> 采集时间: YYYY-MM-DD
> 来源: [主页URL]
> 共采集 N 条相关视频

---

## 1. [视频标题]
**链接**: [url]
**描述**: [视频描述文字]

### 章节要点（AI字幕）
- [要点1]
```

### 蒸馏画像格式

```markdown
# [用户名]（[平台账号]）观点蒸馏

> 蒸馏日期：YYYY-MM-DD
> 数据来源：全网搜索 + 抖音公开视频（+ LDR，如有）

## 1. 基本画像
## 2. 核心观点
## 3. 知识体系
## 4. 与主流的分歧
## 5. 常用论据
## 6. 内容风格
## 7. 对用户的实用建议
```

## 变量约定

- `[用户名]`：人物昵称（去掉特殊字符，用于文件名）
- `[主题]`：筛选领域（营养、健身、投资…）
- `memory/`：workspace 下 memory 目录

## 注意事项

- 抖音反爬强：视频内容仅 browser 可靠；web_fetch / web_search 不能直接替代逐条文案
- 230+ 视频滚动约 30 秒；全量提取可能 15–30 分钟
- 登录态不通用：换 profile 等于换浏览器，需在对应窗口各登录一次（见 B0）
- 若仍报 `navigation blocked by policy`：确认 `openclaw.json` → `browser.ssrfPolicy.hostnameAllowlist` 含目标域名，改后需 `openclaw gateway restart`
- 浏览器被拦截/限流：等待数分钟后重试
- quick 模式产出可能以 [推断] 为主，须在蒸馏文开头说明数据局限

## 相关技能

- 深度研究：`skills/local-deep-research/SKILL.md`
- 脑库写入：`skills/brain-ops/SKILL.md`
- 长任务落盘：`skills/planning-with-files/SKILL.md`

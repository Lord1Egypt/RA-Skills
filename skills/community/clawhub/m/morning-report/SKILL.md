---
name: morning-report
description: 每日晨报 — SLG游戏行业日报，覆盖AI与游戏资讯、竞品监控（Last War / Whiteout Survival / Kingshot / Last Z: Shooter）、社区舆情、SLG新品测试、STEAM新游、应用商店与广告大盘数据。每天7:30由cron自动触发，输出钉钉兼容Markdown。当用户提到「晨报」「morning report」「日报」「行业简报」或要求生成游戏行业资讯摘要时，使用此skill。
---

# 每日晨报

为SLG方向的移动游戏制作人生成每日行业情报简报，通过钉钉推送。

## 执行流程

晨报包含6个栏目，每个栏目需要独立搜索。按以下顺序执行，确保每个栏目都拿到实时数据：

### 第一步：搜集信息（按栏目逐个搜索）

对每个栏目执行 web search，搜索词要精准。以下是每个栏目的搜索策略：

**栏目一 — AI与游戏行业前沿资讯**
搜索 2-3 次：
- `AI game development news {当月英文} {年份}`
- `mobile gaming industry news this week`
- `游戏行业 AI 最新进展`（可选，补充中文来源）

**栏目二 — 竞品监控**
每款产品搜索 1 次，共 4 次：
- `"Last War Survival" update OR ranking OR revenue {当月}`
- `"Whiteout Survival" update OR ranking OR new version {当月}`
- `"Kingshot" mobile game update OR ranking {当月}`
- `"Last Z Shooter" update OR ranking {当月}`

如果搜索结果中有排名数据，再补一次：
- `SensorTower OR data.ai strategy game top grossing {当月}`

**栏目三 — 竞品舆情**
每款产品搜索 1-2 次，优先 Reddit 和社区：
- `"Last War Survival" reddit review OR complaint OR feedback`
- `"Whiteout Survival" reddit review OR complaint`
- `"Kingshot" game reddit OR review`
- `"Last Z Shooter" reddit OR review OR complaint`

如果 Reddit 结果不够，补搜 TapTap 或 App Store 评论。

**栏目四 — SLG新品测试**
搜索 1-2 次：
- `new SLG mobile game beta test OR soft launch {年份}`
- `4X strategy mobile game CBT OR OBT {当月} {年份}`

**栏目五 — STEAM新游**
搜索 1-2 次：
- `Steam new strategy 4X game release {当月} {年份}`
- `Steam grand strategy OR SLG new release`

**栏目六 — 参考数据**
搜索 1-2 次：
- `mobile game advertising CPI CPM benchmark {年份}`
- `strategy game top grossing iOS Google Play {当月}`

### 第二步：整理输出

按下方模板格式整理搜集到的信息。

## 竞品产品列表

以下是需要监控的4款产品，请使用准确的英文名搜索：

| 内部简称 | 正式英文名 | 开发商 |
|---|---|---|
| Last War | Last War: Survival | Century Games |
| Whiteout | Whiteout Survival | Century Games |
| Kingshot | Kingshot | - |
| Last Z | Last Z: Shooter | - |

搜索时使用正式英文名加引号，提高搜索精度。

## 输出格式规范

### 钉钉 Markdown 兼容性

钉钉的 Markdown 渲染有特殊限制，输出时严格遵守以下规则：

**表格**：
- 表格前后各空一行
- 表头和分隔行之间不要有多余空格
- 正确写法：

```
前面的文字

| 列A | 列B |
|---|---|
| 值1 | 值2 |

后面的文字
```

**不支持的语法**（不要使用）：
- HTML 标签（`<br>` `<b>` 等）
- 删除线 `~~文字~~`
- 任务列表 `- [ ]`
- 脚注 `[^1]`

**支持的语法**：
- `**加粗**`、`*斜体*`
- `[链接文字](url)`
- `# 标题` `## 二级标题`
- `- 列表项`
- `> 引用`
- emoji（适度使用）

### 语言

- 正文使用中文
- 产品名、专有术语保留英文原名
- 海外社区的用户反馈翻译成中文，保留原意

### 信息质量

- 每条信息附来源超链接，格式 `[来源名](url)`
- 如果某条信息找不到链接，标注来源名称（如"据 SensorTower 公开数据"）
- 搜索不到的栏目写「今日暂无相关更新」，绝不编造
- 数据类信息（排名、CPI 等）如果不可获取，标注「数据暂不可用」

## 栏目详细要求

### 一、AI与游戏行业前沿资讯

- 时间范围：最近 2 天内
- 3-5 条新闻，每条 1-2 句话概括
- 优先级：AI+游戏交叉 > 游戏行业重大事件 > 政策/投融资

### 二、竞品监控

4款产品逐一列出，每款关注：
- **排名**：iOS / Google Play 畅销榜变动（适合用表格汇总）
- **买量**：广告投放变化、新素材风格
- **版本**：新版本、新活动、新功能

规则：有更新才写具体内容。没有新动态的产品保留名称，注明「近期无明显变动」。

### 三、竞品舆情

覆盖平台：Reddit、TapTap、App Store 评论、Google Play 评论、Discord、Facebook

每款产品摘录 2 条反馈：
- 🌟 **精选**：1条有价值的正面或建设性反馈
- ⚠️ **负面**：1条玩家不满、bug、流失相关反馈

要求：引用具体原话（翻译成中文），标注来源平台和链接。不是概括，而是摘录原文翻译。

### 四、SLG新品测试

- 范围：全球
- 关注：CBT / OBT / 软发布阶段的 SLG / 4X / 策略手游
- 每条包含：游戏名 | 开发商 | 测试阶段 | 地区 | 玩法特点

### 五、STEAM新游与新玩法

- 范围：全球 Steam 平台
- 关注：最近上架或即将上架的 SLG / 策略 / 4X 相关新游
- 特别留意：有创新玩法、可能启发手游设计的作品

### 六、参考数据

- **应用商店 SLG 品类趋势**：策略品类畅销榜 Top 10-20 变动
- **广告大盘**：美国、日本、韩国、东南亚、中东的移动游戏 CPI/CPM 走势

## 输出模板

直接按以下结构输出，不要加额外的开头寒暄或结尾总结：

```
📰 **每日晨报** | {YYYY-MM-DD} {星期X}

---

**一、AI与游戏行业前沿资讯**

1. {标题} — {概括} [来源]({url})
2. ...

---

**二、竞品监控**

**Last War: Survival**
- 排名：{内容或「近期无明显变动」}
- 买量：{内容}
- 版本：{内容}

**Whiteout Survival**
- ...

**Kingshot**
- ...

**Last Z: Shooter**
- ...

| 产品 | iOS畅销 | GP畅销 | 趋势 |
|---|---|---|---|
| Last War | #xx | #xx | ↑/↓/→ |
| Whiteout | #xx | #xx | ↑/↓/→ |
| Kingshot | #xx | #xx | ↑/↓/→ |
| Last Z | #xx | #xx | ↑/↓/→ |

---

**三、竞品舆情**

**Last War: Survival**
- 🌟 精选：「{翻译后的反馈原文}」 — {平台} [链接]({url})
- ⚠️ 负面：「{翻译后的反馈原文}」 — {平台} [链接]({url})

**Whiteout Survival**
- 🌟 精选：...
- ⚠️ 负面：...

**Kingshot**
- ...

**Last Z: Shooter**
- ...

---

**四、SLG新品测试**

- **{游戏名}** | {开发商} | {阶段} | {地区} — {玩法特点} [链接]({url})
- ...

（如无新品：今日暂无相关更新）

---

**五、STEAM新游与新玩法**

- **{游戏名}** — {玩法亮点简介} [Steam]({url})
- ...

（如无新游：今日暂无相关更新）

---

**六、参考数据**

**应用商店SLG品类**
- {趋势描述或「数据暂不可用」}

**广告大盘**
- {CPI/CPM走势或「数据暂不可用」}
```

## 容错策略

执行过程中可能遇到的问题和处理方式：

- **搜索工具不可用**：直接标注「搜索服务暂不可用，本期晨报信息有限」，基于已有知识简要填充能确认的内容，不编造实时数据
- **某栏目搜索无结果**：该栏目保留标题，内容写「今日暂无相关更新」
- **搜索超时**：跳过该搜索，用已获取的信息完成输出
- **钉钉发送失败**：不影响内容生成，正常输出文本即可

## 推送方式（重要）

**不要依赖 cron announce 投递**，改为 skill 自身在输出完成后调用 message 工具发送。

在输出最终晨报 Markdown 文本后，追加以下工具调用作为最后一步：

```
tool: message
action: send
channel: dingtalk
target: 2735046220840628
message: <完整的晨报Markdown内容>
```

即：skill 输出文本后，**必须**显式调用 message 工具把内容发到钉钉，发送成功后再结束任务。

## 补充说明

- 由 cron job 在每天早上 7:30（CST）自动触发，通过 `run morning-report` 命令调用
- 不需要读取本地文件，不需要调用 read 工具，不需要保存文件到磁盘
- 唯一需要的工具是 **web search**（如 tavily_search），用它获取所有栏目的实时信息
- **必须**在完成所有搜索并输出晨报文本后，调用 message 工具发送到钉钉
- 钉钉发送失败时，将 message 工具返回的 error 信息附加在输出末尾再结束

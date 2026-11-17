# guaikei抖音全量公开数据

> **💡一句话价值**：一键抓取抖音公开视频/作者/评论/热榜数据，帮你做爆款选题、竞品分析、舆情监控、热点追踪。
>
> **🔥核心优势**
>
> - 安全: 无需登录你的抖音账号，不担心风控风险 / 封号问题
> - 强大: 一次可获取最多1W条数据，技能内置批量操作，使用简单方便
> - 全面: 各功能出参数据全面，可见及有价值数据都会返回
> - 灵活: 支持多维度筛选、批量操作
> - 轻量: 无需部署服务，Node.js 一键运行
> - 低耗: 日志自动归档，适配营销报告 / 内容策划场景 ，便于数据二次分析

## 1. ✅ 我能帮你解决什么（10 秒判断）

- 🔍 按关键词搜抖音视频（点赞/最新排序）：找爆款选题、分析高赞视频规律
- 🦸 竞品监控：批量抓取对标账号所有公开作品数据，分析内容策略
- 💬 评论分析：获取抖音评论详情，分析舆情方向
- 📡 热点追流：实时获取抖音热榜，抢占流量风口
- 📊 数据导出：自动生成JSON日志，方便对比分析和使用

## 2. 🚀 最快上手（复制就能跑，30 秒出结果）

> **Note:** 请先访问[抖音搜索技能官网](https://www.guaikei.com)开通TOKEN，配置环境变量 `GUAIKEI_API_TOKEN` 后才能正常运行。

### 2.1 🔎 抖音关键词搜索（最简单）

```bash
node src/douyin/search-cli.js --keyword "AI"
```

### 2.2 🔎 按点赞排序找爆款（最常用）

```bash
node src/douyin/search-cli.js --keyword "AI" --sort 1
```

### 2.3 🦸 抓取抖音博主全部作品

```bash
node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx"
```

### 2.4 💬 获取抖音作品评论内容

```bash
node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx"
```

### 2.5 📡 获取抖音实时热榜

```bash
node src/douyin/hot-cli.js
```

## 3. 📌 适用场景（我该不该用？）

- 你需要做短视频选题 → 关键词搜索 + 点赞排序
- 你需要模仿爆款文案 → 查看高赞视频详情
- 你需要监控竞品账号 → 批量抓取对方作品
- 你需要分析内容舆情 → 获取抖音评论详情
- 你需要快速追热点 → 实时获取抖音热榜
- 你需要做营销报告 → 导出结构化数据

## 4. 🔧 参数详解表

> 详细选项参数说明， 可参阅 [完整选项说明](references/options.md)
>
> LLM理解技能的详细选项，可参阅技能 `assets` 目录中文件，其遵循 JSON Schema draft-07 版本规范。
>
> - 抖音关键词搜索，[入参规范](assets/search_cli_req.schema.json)
> - 抖音关键词搜索，[出参规范](assets/search_cli_resp.schema.json)
> - 抖音博主作品获取，[入参规范](assets/post_cli_req.schema.json)
> - 抖音博主作品获取，[出参规范](assets/post_cli_resp.schema.json)
> - 抖音评论获取，[入参规范](assets/comment_cli_req.schema.json)
> - 抖音评论获取，[出参规范](assets/comment_cli_resp.schema.json)
> - 抖音热榜获取，[出参规范](assets/hot_cli_resp.schema.json)

## 5. ⚠️ 重要限制（不踩坑）

- 仅抓取抖音公开数据，不支持私密 / 隐藏内容
- 需要配置 GUAIKEI_API_TOKEN 才能正常运行
- 数据仅限个人 / 团队内部使用，禁止违规分发

## 6. ❓ 常见问题（秒解决）

> **💡Q：运行报错，提示无权限？**
>
> A：配置环境变量：
>
> - Windows: `set GUAIKEI_API_TOKEN=你的TOKEN`
> - Linux/MacOS: `export GUAIKEI_API_TOKEN=你的TOKEN`
> - 私有TOKEN申请后请留意使用安全，避免泄露给他人
>
> **💡Q：搜索结果为空？**
>
> A：换常用关键词，或把 `--time` 改为 0（全部时间）
>
> **💡Q：输出文件在哪里？**
>
> A：自动保存在技能目录的 `logs` 文件夹下
>
> - 搜索任务日志: 默认保存为「时间戳\_关键词\_排序\_时间\_时长\_类型\_search.json」
> - 抖音博主作品获取日志: 默认保存为「时间戳\_(博主sec_uid)\_post.json」
> - 抖音评论获取日志: 默认保存为「时间戳\_(视频aweme_id)\_comment.json」
>
> **💡Q：支持 Windows/Mac/Linux 吗？**
>
> A：全平台支持，仅需安装 Node.js 环境

## 7. 📞 帮助与支持

- 通过 [抖音关键词搜索技能官网](https://www.guaikei.com) 自助开通TOKEN或查阅使用帮助。

> 🆕 [更新日志](references/changelog.md) 可查阅这里

## 8. 🛑 错误处理与重试策略（重要）

### 8.1 遇到以下错误，立即停止操作并向用户报告

- **权限错误**（AUTH_ERROR）：TOKEN 无效或已过期，请提示用户重新配置
- **API 次数超限**：提示用户联系客服开通更高额度
- **网络错误连续 3 次失败**：提示用户检查网络连接

### 8.2 禁止行为

- ❌ 不要在收到 AUTH_ERROR 后继续重试
- ❌ 不要在 API 返回明确错误码后尝试修改参数重试
- ❌ 不要在用户未明确要求的情况下自动调整搜索条件

### 8.3 正确做法

- ✅ 遇到错误，立即向用户展示错误信息
- ✅ 询问用户是否需要调整参数或重新尝试
- ✅ 对于网络超时，可以尝试最多 3 次之后停止

## 9. 💬 自然语言指令映射（AI 快速参考）

> **统一调用约定（重要）**
>
> - 必须在**技能根目录**执行。
> - 只输出纯 JSON 到 stdout，日志与 banner 走 stderr，便于稳定解析。
> - 退出码约定：`0`=成功（含 empty），`1`=运行错误，`3`=auth_required（缺/错 token）。

### 9.1 搜索功能

| 用户口语化指令                    | 对应命令                                                                           | 参数推导                     |
| --------------------------------- | ---------------------------------------------------------------------------------- | ---------------------------- |
| "搜索 / 搜一下 / 找 AI 相关视频"  | `node src/douyin/search-cli.js --keyword "AI"`                                     | 带关键词即搜索               |
| "找点赞最多的 / 最火的 AI 视频"   | `node src/douyin/search-cli.js --keyword "AI" --sort 1`                            | 最火/点赞最多 → sort=1       |
| "最新的 AI 教程，要 20 条"        | `node src/douyin/search-cli.js --keyword "AI 教程" --sort 2 --limit 20`            | 最新 → sort=2；数量 → limit  |
| "近一周最火的短视频"              | `node src/douyin/search-cli.js --keyword "短视频" --time 7 --sort 1`               | 一周 → time=7；最火 → sort=1 |
| "半年内最新 20 条 AI 教程"        | `node src/douyin/search-cli.js --keyword "AI 教程" --sort 2 --time 180 --limit 20` | 半年 → time=180              |
| "减肥视频，只要 1 分钟以下的"     | `node src/douyin/search-cli.js --keyword "减肥" --duration 1`                      | 见下方 duration 表           |
| "AI 模型，5 分钟以上的，前 50 条" | `node src/douyin/search-cli.js --keyword "AI 模型" --duration 3 --limit 50`        | 5分钟以上 → duration=3       |

### 9.2 竞品监控

| 用户口语化指令                  | 对应命令                                                                      | 参数推导              |
| ------------------------------- | ----------------------------------------------------------------------------- | --------------------- |
| "查看这个博主的所有作品 / 主页" | `node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx"` | 作品/主页/账号 → post |
| "抓取 MS4wLjABxxx 的作品"       | `node src/douyin/post-cli.js --url "MS4wLjABxxx"`                             | sec_uid 直接可用      |
| "获取他最近 50 条视频"          | `node src/douyin/post-cli.js --url "xxx" --limit 50`                          | 数量 → limit          |

### 9.3 评论分析

| 用户口语化指令              | 对应命令                                                                  | 参数推导            |
| --------------------------- | ------------------------------------------------------------------------- | ------------------- |
| "看看这个视频的评论 / 留言" | `node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx"` | 评论/留言 → comment |
| "获取这条视频的 100 条评论" | `node src/douyin/comment-cli.js --url "xxx" --limit 100`                  | 数量 → limit        |

### 9.4 热榜

| 用户口语化指令                           | 对应命令                     |
| ---------------------------------------- | ---------------------------- |
| "抖音今天有什么热点 / 热搜榜 / 热点榜单" | `node src/douyin/hot-cli.js` |

## 10. 🧠 AI 意图识别规则

### 10.1 识别优先级（从上到下）

1. **热搜 / 热点 / 榜单 / 今天什么火** → `hot-cli.js`
2. **搜索 / 搜一下 / 找 + 关键词** → `search-cli.js`
3. **评论 / 留言 / 弹幕** → `comment-cli.js`（必须出现"评论"类词才归此类）
4. **作品 / 视频(指博主内容) / 主页 / 账号 / 博主** → `post-cli.js`

> ⚠️ 歧义提示：单独出现"视频"二字时，**不要默认归到 post-cli**。
>
> - 若同时有"关键词"且无"评论" → 视为 `search`（用户想搜某个视频）。
> - 若明确"这个视频的评论/留言" → `comment`。
> - 仅当"作品/主页/账号/博主"出现时才用 `post`。

### 10.2 参数推断规则

**排序（sort，与 time 正交）**

- 提到"综合 / 默认" → `sort=0`
- 提到"点赞最多 / 最火 / 爆款" → `sort=1`
- 提到"最新 / 最近发布 / 刚发" → `sort=2`

**时间窗（time）**

- 提到"全部 / 不限制" → `time=0`
- 提到"一天 / 24小时" → `time=1`
- 提到"一周 / 7天" → `time=7`
- 提到"半年" → `time=180`

**时长**

- 提到"1分钟以下 / 短于1分钟" → `duration=1`
- 提到"1到5分钟 / 1-5分钟" → `duration=2`
- 提到"5分钟以上" → `duration=3`
- 提到"不限时长" → `duration=0`

**内容类型**

- 提到"不限 / 默认" → `content=0`
- 提到"视频" → `content=1`
- 提到"图文" → `content=2`

**数量（limit）**

- 提到"条数 / 数量 / N条 / 前N条" → `limit=N`

### 10.3 默认值

- sort: 0（综合）｜time: 0（全部）｜duration: 0（不限）｜limit: 10

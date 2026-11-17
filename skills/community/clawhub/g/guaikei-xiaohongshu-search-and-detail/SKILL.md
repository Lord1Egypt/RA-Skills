---
name: guaikei-xiaohongshu-search-and-detail
description: >-
 单独获取小红书笔记的评论内容、评论者信息与互动数据，便于观点聚类与情绪分析。当用户想分析某条小红书笔记评论区在讨论什么、识别高频反馈或负面声音时使用本技能；即使用户没说"评论分析"，只要给了笔记链接并关心受众反馈也适用。与笔记详情的区别：只取评论不取正文。不用于发评论或互动。
license: MIT
metadata:
  type: command
  runtime: "nodejs@16.14.0+"
  version: "1.1.1"
  requires:
    bins:
      - "node"
    env:
      - "GUAIKEI_API_TOKEN"
  env_desc:
    GUAIKEI_API_TOKEN: "小红书数据 API 访问令牌（32位字母数字）。未配置时无法调用接口；可通过 https://www.guaikei.com 开通，或联系开发者(wx 13395823479)获取支持。"
  category:
    - "Integrations"
    - "Research"
    - "Creative"
    - "办公效率"
    - "内容创作"
    - "数据分析"
    - "商业运营"
  tags:
    - "小红书"
    - "关键词搜索"
    - "笔记详情"
    - "评论分析"
    - "博主作品监控"
    - "竞品分析"
    - "选题调研"
    - "爆款挖掘"
    - "趋势洞察"
    - "KOL筛选"
    - "小红书运营"
    - "小红书营销"
  examples:
    - "帮我找最近一周小红书里'露营装备'的高赞图文笔记: node src/xiaohongshu/search-cli.js --keyword '露营装备' --type 2 --sort 2 --limit 10"
    - "分析这条小红书笔记评论区的主要观点和负面反馈: node src/xiaohongshu/comment-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 100"
    - "看这个小红书博主最近 20 条作品都在发什么: node src/xiaohongshu/post-cli.js --url 'https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy' --limit 20"
    - "监控'夏季穿搭'这个关键词最近的小红书趋势: node src/xiaohongshu/search-cli.js --keyword '夏季穿搭' --sort 1"
---

# guaikei·小红书搜索与详情获取

面向小红书公开数据的检索与洞察技能。通过关键词搜索、笔记详情、评论获取、博主作品监控四条路径，返回结构化 JSON 供后续分析、汇总或报告生成。无需登录小红书账号，不涉及风控风险。

## 1. 触发判定

**应触发的信号：**

- 用户明确提到查小红书内容、找小红书笔记、分析小红书评论、监控小红书博主
- 用户要做爆款选题、竞品分析、KOL 筛选、趋势洞察、评论舆情——且上下文指向小红书
- 用户提供了小红书关键词、笔记链接或博主主页链接，希望拿到结构化数据

**不应触发的场景：**

- 用户只想写文案、改标题、生成脚本，但未要求查询小红书数据
- 用户查询的平台不是小红书（抖音、B站、微博等）
- 用户要求获取私密内容、登录态数据或非公开信息
- 用户既没给关键词也没给链接，且任务目标不明确——先追问，不要盲目执行

## 2. 能力路由

根据用户输入的关键信号，路由到对应脚本：

| 用户意图 | 脚本 | 必填输入 | 链接类型 |
|---------|------|---------|---------|
| 搜某个关键词的小红书内容 | `src/xiaohongshu/search-cli.js` | `keyword` | 无需链接 |
| 看某篇笔记的详情+评论 | `src/xiaohongshu/detail-cli.js` | 笔记 URL | `explore/` 或短链 |
| 只拉某篇笔记的评论 | `src/xiaohongshu/comment-cli.js` | 笔记 URL | `explore/` 或短链 |
| 看某个博主的公开作品 | `src/xiaohongshu/post-cli.js` | 博主主页 URL | `user/profile/` 或短链 |

**路由细则：**

- 给的是 **关键词**（无链接）→ 关键词搜索
- 给的是 `explore/...` 链接 → 笔记详情或评论获取（看用户是否要正文）
- 给的是 `user/profile/...` 链接 → 博主作品监控
- 给的是 `xhslink.com/m/` 或 `xhslink.cn/m/` 短链 → **无法仅凭短链判断指向笔记还是博主主页**。detail-cli 和 comment-cli 接受短链，post-cli 也接受短链；若结果异常，优先请用户提供完整链接
- 用户同时给出多个目标 → 按目标拆分执行，不要把不同意图塞进一次命令

## 3. 输入收集

执行前先确认必填输入齐全，避免无效调用。

### 3.1 关键词搜索 `search-cli.js`

**必填：** `--keyword` / `-k`（搜索关键词，2-50 个字符，不能含 `http`、`<>"'&`）

**可选：**

| 参数 | 简写 | 取值 | 默认 |
|------|------|------|------|
| `--type` | `-t` | `0` 全部 / `1` 视频 / `2` 图文 | `0` |
| `--sort` | `-s` | `0` 综合 / `1` 最新 / `2` 最多点赞 / `3` 最多评论 / `4` 最多收藏 | `0` |
| `--time` | `-i` | `0` 全部 / `1` 一天内 / `2` 一周内 / `3` 半年内 | `0` |
| `--limit` | `-l` | `1-10000` | `10` |

> 关键词会被自动清洗：仅保留中文、字母、数字、空格及 `.,!?#`，其余字符（含 emoji）会被移除。清洗后为空则报错。

### 3.2 笔记详情 `detail-cli.js`

**必填：** `--url` / `-u`（笔记链接）

**可选：** `--limit` / `-l`（评论数量上限，`0-10000`，默认 `0` 表示按脚本默认行为执行）

适用链接：`https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy`、`https://xhslink.com/m/xxx`、`https://xhslink.cn/m/xxx`

### 3.3 笔记评论 `comment-cli.js`

**必填：** `--url` / `-u`（笔记链接）

**可选：** `--limit` / `-l`（评论数量上限，`1-10000`，默认 `10`）

> 与 detail-cli 的区别：只返回评论数据，不返回笔记正文与互动详情，适合专注评论分析的场景。

### 3.4 博主作品 `post-cli.js`

**必填：** `--url` / `-u`（博主主页链接）

**可选：** `--limit` / `-l`（作品数量上限，`1-10000`，默认 `10`）

适用链接：`https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy`、`https://xhslink.com/m/xxx`、`https://xhslink.cn/m/xxx`

> 链接会被自动归一化：`http://` → `https://`，前后空格会被 trim。含空格或非 https 开头的链接会被拒绝。

### 3.5 缺少输入时

- 没有关键词 → 追问关键词
- 没有链接 → 追问笔记链接或博主主页链接
- 链接类型不明确 → 确认是笔记还是博主主页
- 没有 `GUAIKEI_API_TOKEN` → 提醒用户先配置环境变量

不要在缺关键输入时硬调命令。

## 4. 执行与输出

### 4.1 调用示例

```bash
# 关键词搜索：找高赞图文
node src/xiaohongshu/search-cli.js --keyword "露营装备" --type 2 --sort 2 --limit 20

# 笔记详情
node src/xiaohongshu/detail-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"

# 笔记评论（只拉评论区）
node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --limit 100

# 博主作品监控
node src/xiaohongshu/post-cli.js --url "https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy" --limit 20
```

### 4.2 输出结构

所有脚本统一输出 JSON，核心字段：

```json
{
  "status": "success | empty | error",
  "error_code": "OK | NOT_FOUND | NO_MATCH | 401 | 429 | 500 | ...",
  "message": "描述信息",
  "request": { "command": "search|detail|comment|post", ... },
  "skill_metadata": { "skill_version": "1.1.1", "runtime_version": "...", "execution_time": 1234 },
  "results": [ ... ]  // 成功时有数据，失败时为 null
}
```

**解析规则：**

- 先看 `status` 字段：`success` 才有 `results` 数据；`empty` / `error` 的 `results` 为 `null`
- 只取最后一份 JSON 输出（失败时通过异步 `process.stdout.write` + `exit(1)` 输出）
- 等进程退出后再读完整 stdout，不要中途截取

### 4.3 退出码差异

| 脚本 | 无结果时 | 退出码 |
|------|---------|-------|
| search-cli | 视为失败 | `1` |
| detail-cli | 返回 null 视为失败 | `1` |
| comment-cli | 返回 null 视为失败 | `1` |
| post-cli | 返回 null 视为失败 | `1` |

### 4.4 输出后衔接

取回数据后，适合继续的后续动作：选题汇总、高赞笔记对比、评论观点聚类、竞品内容风格总结、博主发文节奏分析、报告与表格生成。

### 4.5 日志归档

每次执行的结果会自动保存到 `logs/` 目录，按 `{时间戳}_{关键词或链接标识}_{命令}.json` 命名，适配营销报告与内容策划场景。

## 5. 错误自愈

### 5.1 反模式（以下做法会导致失败或拿到错误数据）

- **链接类型错配**：把 `user/profile/` 传给 detail-cli / comment-cli，或把 `explore/` 传给 post-cli
- **误信短链类型**：`xhslink.com/m/` 短链无法判断指向笔记还是博主主页，结果异常时优先索要完整链接
- **传脏链接**：带前后空格、用 `http://`（非 `https://`）的链接会被拒绝（脚本会自动归一化，但含空格会直接拒绝）
- **limit 超限**：`limit > 10000` 会被静默降级——search 降到 `10`，comment/post 降到 `10`，detail 降到 `0`
- **关键词喂 emoji / 纯符号**：会被清洗成空串，触发"关键词无效"拦截
- **把空结果当成功 / 编造数据**：失败时 `status` 为 `error` 或 `empty`，`results` 为 `null`，不要编造结论

### 5.2 FAQ 自助排查

| 报错 | 含义 | 自查 |
|------|------|------|
| `401` / `403` | TOKEN 未配置或无效 | 确认 `GUAIKEI_API_TOKEN` 已注入当前进程；TOKEN 须为 32 位字母数字；去 guaikei.com 重新开通 |
| `429` | 频率限制 | 降低调用频率、减小 `--limit`、稍后重试 |
| `500` / `502` / `503` | 第三方 API 临时故障 | 等 1-2 分钟重试；持续出现则联系支持并附 `execution_time` 与请求参数 |
| `ERRCODE_xxx` | 业务层错误（HTTP 200 但 `errcode !== 0`） | 常见为笔记已删除/不存在/无权限，换一条链接，不要反复重试同一链接 |
| `ETIMEDOUT` / `UNKNOWN` | 网络超时或无法解析 | 检查网络/代理，确认能访问 guaikei.com，重试一次 |
| 链接格式无效 | URL 不符合规则 | 确认以 `https://` 开头、无空格、属于 `explore/`、`user/profile/`、`xhslink.com/m/`、`xhslink.cn/m/` 之一 |
| 一启动就退出 | TOKEN 校验未通过 | 运行前先 `echo $GUAIKEI_API_TOKEN` 确认变量已注入 |
| search 返回空但退出码非 0 | search-cli 把"无结果"视为失败 | 换更宽泛的关键词、放宽 `--type`/`--time` 筛选 |
| 设了 `--limit 10000` 却只拿到 10 条 | limit 超过 10000 被静默降级 | 确认 `--limit` 在 `1-10000` 范围内 |
| 下游解析 stdout 失败 | 异步写出后立即退出 | 等进程退出后再读完整 stdout，只取最后一份 JSON |

## 6. 环境与边界

**运行环境：** Node.js 16.14.0+，Windows / Linux / macOS，无需代理，无需管理员权限

**必需环境变量：** `GUAIKEI_API_TOKEN`（32 位字母数字，通过 https://www.guaikei.com 开通）

**能力边界：**

- 仅处理小红书公开数据
- 不支持登录、发布、互动、点赞、评论、关注
- 不支持获取私密、隐藏或需要登录态的数据
- 不代替用户做营销策略判断——先把数据拿回来，再交给上层流程分析

**合规限制：**

- 返回数据仅限个人/团队内部使用，禁止违规分发或违法用途
- 本技能依赖第三方 API 服务，使用前需确认数据外发与授权范围

**相关文档：**

- 完整参数说明：`references/options.md`
- 更新记录：`references/changelog.md`
- 官网：https://www.guaikei.com

**支持：**

- 官网：https://www.guaikei.com
- 微信：`13395823479`（备注：小红书技能）

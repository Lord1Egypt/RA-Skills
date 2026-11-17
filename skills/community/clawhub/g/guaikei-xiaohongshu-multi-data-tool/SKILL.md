---
name: guaikei-xiaohongshu-multi-data-tool
description: >-
 把小红书关键词搜索、笔记详情、笔记评论、博主作品抓取为结构化数据，一次最多 1W 条。当用户需要先把小红书数据拿回来、再做汇总/对比/报告时使用本技能；即使用户没说"采集"或"抓取"，只要任务是从小红书获取内容数据也适用。不用于发布、互动或私密内容。
license: MIT
metadata:
  name_cn: "guaikei·小红书内容数据采集与洞察工具"
  type: command
  runtime: "nodejs@16.14.0+"
  version: "1.1.1"
  requires:
    bins:
      - "node"
    env:
      - "GUAIKEI_API_TOKEN"
  env_desc:
    GUAIKEI_API_TOKEN: "小红书数据 API 访问令牌（32位字母数字）。未配置时技能会拒绝执行；通过 https://www.guaikei.com 开通，或联系开发者微信 13395823479 获取支持。"
  category:
    - "Integrations"
    - "Research"
    - "办公效率"
    - "内容创作"
    - "数据分析"
    - "商业运营"
  tags:
    - "小红书"
    - "数据采集"
    - "关键词搜索"
    - "笔记详情"
    - "评论分析"
    - "博主作品监控"
    - "竞品分析"
    - "选题调研"
    - "爆款挖掘"
    - "趋势洞察"
    - "KOL筛选"
  examples:
    - "帮我找小红书里'露营装备'的高赞图文笔记: node src/xiaohongshu/search-cli.js --keyword '露营装备' --type 2 --sort 2 --limit 20"
    - "看看这篇小红书笔记讲了什么、数据怎么样: node src/xiaohongshu/detail-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy'"
    - "分析这条小红书笔记评论区的主要观点: node src/xiaohongshu/comment-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 100"
    - "看这个小红书博主最近 20 条作品都在发什么: node src/xiaohongshu/post-cli.js --url 'https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy' --limit 20"
---

# guaikei·小红书多维数据工具

面向小红书公开数据的采集技能，四条能力路径（搜索 / 详情 / 评论 / 博主作品）均输出结构化 JSON，供后续汇总、对比、分析或报告生成。无需登录小红书账号，无风控风险。

## 0. 速查表

| 你拿到的东西 | 该用哪个脚本 | 必填参数 |
|-------------|-------------|---------|
| 一个关键词 | `search-cli.js` | `--keyword` |
| 一条笔记链接 | `detail-cli.js`（要正文）或 `comment-cli.js`（只要评论） | `--url` |
| 一条博主主页链接 | `post-cli.js` | `--url` |

所有命令格式：`node src/xiaohongshu/<脚本> <参数>`。执行前确认环境变量 `GUAIKEI_API_TOKEN` 已注入，否则技能直接退出。

## 1. 能力卡 · 关键词搜索 `search-cli.js`

**何时用：** 用户给关键词，想找小红书上的相关笔记（选题、找爆款、看趋势）。

```bash
node src/xiaohongshu/search-cli.js --keyword "露营装备" --type 2 --sort 2 --time 0 --limit 20
```

| 参数 | 简写 | 取值 | 默认 |
|------|------|------|------|
| `--keyword` | `-k` | 2-50 字符，不含 `http` `<>"'&` | 必填 |
| `--type` | `-t` | `0` 全部 / `1` 视频 / `2` 图文 | `0` |
| `--sort` | `-s` | `0` 综合 / `1` 最新 / `2` 最多点赞 / `3` 最多评论 / `4` 最多收藏 | `0` |
| `--time` | `-i` | `0` 不限 / `1` 一天内 / `2` 一周内 / `3` 半年内 | `0` |
| `--limit` | `-l` | `1-10000`，超限静默降为 10 | `10` |

**注意：**

- 关键词自动清洗：仅保留中文、字母、数字、空格及 `.,!?#`，emoji 等其余字符被移除；清洗后为空则报错退出
- 搜索无结果视为失败（exit 1）——此时换更宽泛的关键词或放宽 `--type` / `--time` 筛选，不要原样重试
- **链式用法：** 结果数组中每条笔记的 `url` 字段，可直接作为 detail-cli / comment-cli 的 `--url` 输入

## 2. 能力卡 · 笔记详情 `detail-cli.js`

**何时用：** 用户给笔记链接，想看正文内容 + 互动数据 + 评论。

```bash
node src/xiaohongshu/detail-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"
```

| 参数 | 简写 | 取值 | 默认 |
|------|------|------|------|
| `--url` | `-u` | 笔记链接（见下方链接规则） | 必填 |
| `--limit` | `-l` | `0-10000`，随附评论数上限，超限静默降为 0 | `0` |

**注意：**

- 只处理笔记链接（`explore/` 或短链），博主主页链接会被拒绝
- 返回 null（笔记已删 / 不存在 / 无权限）视为失败（exit 1），换链接，不要反复重试同一条

## 3. 能力卡 · 笔记评论 `comment-cli.js`

**何时用：** 用户给笔记链接，只关心评论区的观点、情绪、反馈。

```bash
node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --limit 100
```

| 参数 | 简写 | 取值 | 默认 |
|------|------|------|------|
| `--url` | `-u` | 笔记链接（同 detail-cli） | 必填 |
| `--limit` | `-l` | `1-10000`，超限静默降为 10 | `10` |

**注意：** 与 detail-cli 的区别——只返回评论数据，不含笔记正文与互动详情。链接来源同样可用 search-cli 结果中的 `url` 字段。

## 4. 能力卡 · 博主作品 `post-cli.js`

**何时用：** 用户给博主主页链接，想看该博主发了哪些作品（竞品监控、KOL 评估、发文节奏分析）。

```bash
node src/xiaohongshu/post-cli.js --url "https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy" --limit 20
```

| 参数 | 简写 | 取值 | 默认 |
|------|------|------|------|
| `--url` | `-u` | 博主主页链接（见下方链接规则） | 必填 |
| `--limit` | `-l` | `1-10000`，超限静默降为 10 | `10` |

**注意：** 只处理博主主页链接（`user/profile/` 或短链），笔记链接会被拒绝。

### 链接规则（三个 URL 脚本通用）

- 合法形态：`https://www.xiaohongshu.com/explore/...`、`https://www.xiaohongshu.com/user/profile/...`、`https://xhslink.com/m/...`、`https://xhslink.cn/m/...`
- 自动归一化：`http://` 自动转 `https://`，前后空格自动 trim；**含空格或非 https 开头直接拒绝**
- 短链（`xhslink`）无法仅凭 URL 判断指向笔记还是博主主页——若调用结果异常，请用户提供完整链接

## 5. 通用执行规范

**输出结构（四脚本统一）：**

```json
{
  "status": "success | empty | error",
  "error_code": "OK | NO_MATCH | 401 | 429 | 500 | ...",
  "message": "描述信息",
  "request": { "command": "search|detail|comment|post", ... },
  "skill_metadata": { "skill_version": "1.1.1", "runtime_version": "...", "execution_time": 1234 },
  "results": [ ... ]
}
```

- **先看 `status`**：仅 `success` 时 `results` 有数据；`empty` / `error` 时 `results` 为 `null`，不要编造结论
- 只取最后一份 JSON；等进程退出后再读完整 stdout，不要中途截取
- 失败统一 exit 1，成功 exit 0
- 每次执行自动归档到 `logs/{时间戳}_{关键词或链接标识}_{命令}.json`
- 拿到数据后的衔接动作：选题汇总、高赞对比、评论观点聚类、竞品内容风格总结、博主发文节奏分析、报告生成

**多目标请求：** 用户同时给多个关键词/链接时，按目标拆分逐条执行，不要合并进一次命令。

## 6. 故障排查

| 现象 | 原因 | 处理 |
|------|------|------|
| `401` / `403` | TOKEN 未配置或无效 | 确认 `GUAIKEI_API_TOKEN` 已注入（32 位字母数字）；去 guaikei.com 重新开通 |
| `429` | 频率限制 | 降频、减小 `--limit`、稍后重试 |
| `500` / `502` / `503` | 第三方 API 临时故障 | 等 1-2 分钟重试；持续出现联系支持并附 `execution_time` |
| `ERRCODE_xxx` | 业务层错误（笔记已删/不存在/无权限） | 换链接，不要重试同一条 |
| `ETIMEDOUT` / `UNKNOWN` | 网络超时 | 检查网络，确认可访问 guaikei.com，重试一次 |
| 一启动就退出 | TOKEN 校验未通过 | 先 `echo $GUAIKEI_API_TOKEN` 确认变量存在 |
| 链接格式无效 | URL 不合法 | 确认 https 开头、无空格、属于四种合法形态之一 |
| search 空结果但 exit 1 | 无匹配被视为失败 | 换宽泛关键词或放宽筛选 |
| limit 给了 10000+ 只返回默认值 | 超限静默降级 | 确认 `--limit` 在范围内 |
| 输入不足就硬调命令 | 关键词/链接缺失 | 先向用户追问，缺 TOKEN 先提醒配置 |

## 7. 环境与边界

- **运行环境：** Node.js 16.14.0+，Windows / Linux / macOS，无需代理与管理员权限
- **必需配置：** `GUAIKEI_API_TOKEN`（https://www.guaikei.com 开通）
- **能力边界：** 仅小红书公开数据；不支持登录、发布、点赞、评论、关注；不获取私密或登录态内容
- **合规：** 数据仅限个人/团队内部使用，禁止违规分发；依赖第三方 API，外发数据前确认授权范围

**参考文档：** `references/options.md`（完整参数）· `references/changelog.md`（更新记录）

**支持：** https://www.guaikei.com · 微信 `13395823479`（备注：小红书技能）

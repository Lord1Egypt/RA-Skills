---
name: guaikei-xhs-note-detail
description: 仅处理小红书（xiaohongshu / xhs / 红笔记）平台的公开数据：笔记搜索、详情、评论、博主作品。当用户的任务明确涉及小红书内容时使用本技能；抖音、B站、微博、公众号不适用。即使用户没说"小红书"，只要链接是 xiaohongshu.com 或语境是红笔记也适用。不用于跨平台或登录态数据。
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
    GUAIKEI_API_TOKEN: "小红书数据 API 访问令牌（32 位十六进制）。未配置时所有命令鉴权失败；可在 https://www.guaikei.com 开通，或联系开发者（微信 13395823479）。"
  category:
    - "内容创作"
    - "数据分析"
    - "商业运营"
    - "办公效率"
    - "Research"
  tags:
    - "小红书"
    - "红笔记"
    - "xhs"
    - "rednote"
    - "关键词搜索"
    - "笔记详情"
    - "评论分析"
    - "博主作品监控"
    - "爆款挖掘"
    - "竞品分析"
    - "KOL筛选"
    - "趋势洞察"
  examples:
    - "找最近一周‘露营装备’的高赞图文: node src/xiaohongshu/search-cli.js --keyword '露营装备' --type 2 --sort 2 --limit 10"
    - "看这篇笔记的详情和评论区: node src/xiaohongshu/detail-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 100"
    - "看这位博主最近 20 条作品: node src/xiaohongshu/post-cli.js --url 'https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy' --limit 20"
    - "只拉这篇笔记的评论做舆情: node src/xiaohongshu/comment-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 100"
---

# guaikei·小红书笔记详情

## 1. 定位

面向小红书公开数据层的检索工具：关键词搜索、笔记详情、评论拉取、博主作品抓取，统一返回结构化 JSON，供上层完成选题、竞品、KOL、舆情等分析。不登录、不发布、不互动，仅取公开数据。

## 2. 触发规则

**该用：**

- 用户想从小红书获取内容数据（搜关键词 / 看笔记 / 拉评论 / 查博主）
- 用户给出 xiaohongshu.com 或 xhslink.com 链接并索要数据
- 提到 红笔记 / xhs / rednote 等别称，或只给链接没提平台名

**不该用：**

- 目标平台不是小红书（抖音 / B 站 / 微博等）
- 只要文案、标题、脚本等创作产出，无需真实数据
- 要求私密、登录态或隐藏内容
- 既无关键词也无链接，意图不明——先追问再执行

## 3. 能力与参数

### 3.1 四类能力

| 用户意图 | 入口脚本 | 必填 | 输出 |
|---|---|---|---|
| 按关键词搜笔记 | `src/xiaohongshu/search-cli.js` | `--keyword` | 笔记列表、作者、互动数据、链接 |
| 看单篇笔记详情 | `src/xiaohongshu/detail-cli.js` | `--url`（笔记链接） | 笔记正文、作者、互动详情 |
| 单独拉评论区 | `src/xiaohongshu/comment-cli.js` | `--url`（笔记链接） | 评论内容、评论者、互动数据（无正文） |
| 抓博主公开作品 | `src/xiaohongshu/post-cli.js` | `--url`（主页链接） | 博主公开作品列表 |

### 3.2 参数总表

| 参数 | 简写 | 含义 | 取值 |
|---|---|---|---|
| `--keyword` | `-k` | 搜索关键词（仅搜索） | 2-50 字符，避开纯符号 |
| `--type` | `-t` | 内容类型（仅搜索） | `0` 全部 `1` 视频 `2` 图文 |
| `--sort` | `-s` | 排序（仅搜索） | `0` 综合 `1` 最新 `2` 点赞 `3` 评论 `4` 收藏 |
| `--time` | `-i` | 时间范围（仅搜索） | `0` 全部 `1` 一天 `2` 一周 `3` 半年 |
| `--url` | `-u` | 链接（详情/评论/博主） | 笔记或主页链接 |
| `--limit` | `-l` | 返回条数上限 | `1-10000`，默认 `10` |
| `--help` | `-h` | 帮助 | - |

### 3.3 命令速查

```bash
node src/xiaohongshu/search-cli.js  --keyword "露营装备" --type 2 --sort 2 --limit 20
node src/xiaohongshu/detail-cli.js  --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"
node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --limit 100
node src/xiaohongshu/post-cli.js    --url "https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy" --limit 20
```

## 4. 链接规则

| 链接形态 | 判断 | 处理 |
|---|---|---|
| `www.xiaohongshu.com/explore/...` | 笔记 | 走详情或评论 |
| `www.xiaohongshu.com/user/profile/...` | 博主主页 | 走作品监控 |
| `xhslink.com/m/...` / `xhslink.cn/m/...` | 不透明短链 | 无法仅凭链接判断类型；结果异常时请用户提供完整链接 |
| 带空格 / `http://` 开头 | 非法 | 先 trim、`http`→`https` 归一 |

## 5. 执行约定

**先收齐输入再执行**：缺关键词、缺链接、链接类型不明、token 未配置——任一情况先追问或提醒，不硬跑。

**输出结构**：先说明本次目标与关键参数，再给结构化 JSON，必要时附一句摘要。解析 stdout 时先看 `status`（`success` / `empty` / `error`）；失败时 `results` 为 `null`，不要拼多份输出。

**失败处理**：

- `401 / 403`：token 未配置或无效——核对 32 位十六进制、无空格换行、未过期
- `429`：触发频率限制——降频、减小 `--limit`、稍后重试
- `500 / 502 / 503`：服务端临时故障——等 1-2 分钟重试
- `ERRCODE_xxx`：业务错误（如笔记已删除）——换有效链接，重试无意义
- `ETIMEDOUT / UNKNOWN`：网络或代理问题——检查本机网络能否访问 guaikei.com
- 搜索无结果：是失败（退出码 1）——换更宽泛关键词或放宽 `--type` / `--time`
- 详情/评论空数组：是成功，属正常差异

任何情况下不编造数据、不把空结果当成功结论。

**反模式**：

- 链接类型错配：`explore/...` 传给 post-cli，或 `user/profile/...` 传给 detail/comment-cli
- 短链当长链用：`xhslink` 短链类型不透明，依赖其推断会导致误路由
- `--limit` 超 10000：会被静默降到默认 `10`，并非没返回
- 关键词传 emoji / 纯符号：会被清洗成空串，触发「关键词无效」拦截

## 6. 典型工作流

- **选题调研**：搜索关键词 → 挑高赞笔记看详情 → 汇总标题、主题、互动特征
- **评论舆情**：拉评论区 → 观点归类、情绪判断、负面反馈识别
- **竞品 / KOL 监控**：抓博主作品 → 分析更新频率、主题分布、互动表现
- **趋势追踪**：固定关键词 + `--sort 1` 周期性采集最新内容

## 7. 环境与支持

- 环境：Node.js 16.14.0+；Windows / Linux / macOS
- 必需变量：`GUAIKEI_API_TOKEN`（未配置时所有命令鉴权失败）
- 文档：参数详见 `references/options.md`，更新见 `references/changelog.md`
- 开通 / 支持：官网 <https://www.guaikei.com>；开发者微信 `13395823479`（备注：小红书技能）
- 合规：仅公开数据；不用于违规分发；依赖第三方 API，使用前确认数据外发与授权范围

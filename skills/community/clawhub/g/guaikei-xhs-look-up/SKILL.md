---
name: guaikei-xhs-look-up
description: >-
  当用户需要按关键词搜索小红书笔记、查看某篇笔记详情与评论、单独获取笔记评论数据、或抓取某博主公开作品列表时调用；返回结构化数据用于爆款挖掘、竞品监控、KOL筛选与趋势洞察，不做账号登录与内容发布 
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
    GUAIKEI_API_TOKEN: "小红书数据 API 访问令牌（32 位十六进制）。未配置时所有命令均因鉴权失败退出。通过 https://www.guaikei.com 开通，或联系开发者（微信 13395823479）获取支持。"
  category:
    - "数据分析"
    - "内容创作"
    - "商业运营"
    - "市场调研"
    - "社媒营销"
  tags:
    - "小红书"
    - "红笔记"
    - "xhs"
    - "rednote"
    - "关键词搜索"
    - "笔记详情"
    - "评论分析"
    - "博主监控"
    - "竞品分析"
    - "爆款挖掘"
    - "KOL筛选"
    - "趋势洞察"
  examples:
    - "帮我找最近一周小红书里'露营装备'的高赞图文笔记: node src/xiaohongshu/search-cli.js --keyword '露营装备' --type 2 --sort 2 --limit 10"
    - "分析这条小红书笔记评论区的主要观点: node src/xiaohongshu/detail-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 100"
    - "看这个小红书博主最近 20 条作品都在发什么: node src/xiaohongshu/post-cli.js --url 'https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy' --limit 20"
    - "只拉这条笔记的评论数据做观点归纳: node src/xiaohongshu/comment-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 100"
---

# 小红书查一查

> guaikei 出品，专注小红书公开数据采集。无需登录账号，不触发风控；一次最多获取 10000 条结构化数据，返回 JSON 供后续分析、汇总或报告生成。

---

## 1. 四大能力

| 能力 | 脚本 | 必填输入 | 输出 |
|------|------|----------|------|
| 关键词搜索 | `src/xiaohongshu/search-cli.js` | `--keyword` | 笔记列表 + 作者 + 互动数据 + 跳转链接 |
| 笔记详情 | `src/xiaohongshu/detail-cli.js` | `--url`（笔记链接） | 笔记正文 + 作者信息 + 评论 |
| 博主作品监控 | `src/xiaohongshu/post-cli.js` | `--url`（博主主页） | 博主公开作品列表 |
| 笔记评论获取 | `src/xiaohongshu/comment-cli.js` | `--url`（笔记链接） | 评论文本 + 评论者信息 + 互动数据 |

**详情 vs 评论的区别**：`detail-cli.js` 返回笔记正文 + 评论（适合看全貌）；`comment-cli.js` 只返回评论数据（适合专注评论洞察、观点聚类、舆情分析）。

---

## 2. 调用路由

根据用户输入判断走哪个脚本：

| 用户给了什么 | 用户想干什么 | 走哪个脚本 |
|--------------|--------------|-----------|
| 关键词（无链接） | 搜小红书内容 | search-cli.js |
| 笔记链接 `explore/...` | 看笔记详情 + 评论 | detail-cli.js |
| 笔记链接 `explore/...` | 只要评论数据 | comment-cli.js |
| 博主主页 `user/profile/...` | 看博主发了什么 | post-cli.js |
| 短链 `xhslink.com/m/...` | 不确定指向笔记还是博主 | 先追问用户提供完整链接 |

**路由细则**：
- 短链 `xhslink.com/m/xxx` 无法仅凭 URL 判断指向笔记还是博主主页。若结果异常，优先请用户提供完整链接。
- 把博主主页链接传给 `detail-cli.js` / `comment-cli.js`，或把笔记链接传给 `post-cli.js`，都会触发业务错误。
- 用户同时有多个目标时，拆分执行，不要把不同意图塞进一次命令。

---

## 3. 参数说明

### 3.1 关键词搜索（search-cli.js）

| 参数 | 简写 | 必填 | 说明 | 取值 |
|------|------|------|------|------|
| `--keyword` | `-k` | 是 | 搜索关键词 | 2-50 字符，避免纯符号/emoji |
| `--type` | `-t` | 否 | 内容类型 | `0` 全部（默认）/ `1` 视频 / `2` 图文 |
| `--sort` | `-s` | 否 | 排序规则 | `0` 综合（默认）/ `1` 最新 / `2` 最多点赞 / `3` 最多评论 / `4` 最多收藏 |
| `--time` | `-i` | 否 | 时间范围 | `0` 全部（默认）/ `1` 一天内 / `2` 一周内 / `3` 半年内 |
| `--limit` | `-l` | 否 | 返回数量 | 1-10000，默认 10 |
| `--help` | `-h` | 否 | 显示帮助 | — |

### 3.2 笔记详情 / 博主作品 / 笔记评论（detail / post / comment）

| 参数 | 简写 | 必填 | 说明 |
|------|------|------|------|
| `--url` | `-u` | 是 | 小红书链接（详情/评论传笔记链接，博主传主页链接） |
| `--limit` | `-l` | 否 | 返回数量上限（评论/作品），不传按默认 |
| `--help` | `-h` | 否 | 显示帮助 |

---

## 4. 触发规则

### 应该调用

- 用户明确提到小红书 / 红笔记 / xhs / rednote，想搜内容、看笔记、查评论、监控博主。
- 用户给出 `xiaohongshu.com` 或 `xhslink.com` 链接，想获取笔记或博主数据。
- 用户要做爆款挖掘、竞品分析、KOL 筛选、评论洞察、趋势调研等小红书相关任务。
- 用户没明说"小红书"但提到"红笔记/xhs/rednote"或给出上述链接并想拿内容数据。

### 不应调用

- 用户只想写文案、改标题、生成脚本，但没要求查小红书数据。
- 用户查询的平台是抖音、B 站、微博、公众号等非小红书平台。
- 用户要求登录账号、发布内容、点赞、评论、关注或获取私密数据。
- 用户既没给关键词也没给链接，且任务目标不明确——先追问，别盲目执行。

---

## 5. 输入收集

执行前确认输入齐备，缺关键参数时先追问：

| 场景 | 必须确认 | 追问示例 |
|------|----------|----------|
| 关键词搜索 | keyword | "搜什么关键词？要图文还是视频？按点赞还是最新排序？" |
| 笔记详情 | 笔记 URL | "请提供笔记链接（explore/ 开头的）" |
| 博主监控 | 博主主页 URL | "请提供博主主页链接（user/profile/ 开头的）" |
| 评论获取 | 笔记 URL | "请提供笔记链接" |

**链接格式要求**：以 `https://` 开头，无前后空格，属于以下之一：
- `https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy`（笔记）
- `https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy`（博主主页）
- `https://xhslink.com/m/xxx` 或 `xhslink.cn/m/xxx`（短链，指向不明确）

---

## 6. 执行与输出

### 执行

```bash
# 搜索
node src/xiaohongshu/search-cli.js --keyword "夏季穿搭" --type 2 --sort 2 --time 2 --limit 20

# 笔记详情
node src/xiaohongshu/detail-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy"

# 博主作品
node src/xiaohongshu/post-cli.js --url "https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy" --limit 20

# 笔记评论
node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --limit 100
```

### 输出

返回结构化 JSON，包含 `status`（`success` / `empty` / `error`）、`results`（数据或 null）、`skill_metadata`（执行信息）。输出后可衔接：
- 选题汇总 / 高赞笔记对比
- 评论观点聚类 / 情绪分析
- 竞品内容风格总结 / 博主发文节奏分析
- 报告与表格生成

### 失败处理

失败时不编造数据，不把空结果当成功。向用户说明原因并给出下一步建议：

| 情况 | 处理 |
|------|------|
| token 未配置/无效 | 提醒配置 `GUAIKEI_API_TOKEN` |
| 链接不合法/类型错误 | 指出链接类型不匹配，要求重传 |
| 搜索结果为空 | `search-cli.js` 退出码 1；建议换更宽泛关键词 |
| 接口返回异常 | 说明是服务端问题，建议稍后重试 |
| 网络超时 | 检查网络/代理，确认能访问 guaikei.com |

---

## 7. 能力边界

**能做**：
- 按关键词搜索小红书公开笔记
- 查看单篇笔记详情与评论
- 获取博主公开作品列表
- 单独拉取笔记评论数据

**不能做**：
- 登录小红书账号
- 发布内容、点赞、评论、关注
- 获取私密、隐藏或需登录态的数据
- 代替用户做营销策略判断

职责定位：先把数据拿回来，交给上层流程分析、整理或生成结论。

---

## 8. 反模式与 FAQ

### 反模式（以下做法都会导致失败或错误数据）

- **链接类型错配**：博主主页传给 detail/comment，笔记链接传给 post。
- **误信短链类型**：短链指向不明确，结果异常时优先要完整链接。
- **缺关键输入硬跑**：没 keyword / url 就执行命令。
- **传脏链接**：带空格、用 `http://` 非 `https://` 的链接被拒。
- **limit 超限被静默降级**：超过 10000 会降到默认 10，不是"没返回"。
- **空结果当成功**：search 无结果时退出码 1，不要编造结论。
- **关键词喂纯符号**：emoji / 纯符号被清洗成空串，触发"关键词无效"。
- **假设失败也输出成功字段**：失败时 `status` 是 `error`/`empty`，`results` 为 null。

### FAQ 自助排查

| 报错 | 原因 | 自查 |
|------|------|------|
| `401` / `403` | token 未配置或无效 | 确认 `GUAIKEI_API_TOKEN` 已注入（32 位十六进制，无空格/换行）；去 guaikei.com 重新开通 |
| `429` | 触发频率限制 | 降低调用频率、减小 limit、稍后重试 |
| `500` / `502` / `503` | 第三方 API 临时故障 | 等 1-2 分钟重试；持续出现则联系支持 |
| `ERRCODE_xxx` | 业务错误（笔记已删除/不存在/无权限） | 换一条确认存在的链接，不要反复重试同一条 |
| `ETIMEDOUT` / `UNKNOWN` | 网络超时 | 检查网络/代理，确认能访问 guaikei.com，重试一次 |
| 链接格式无效 | 格式不合规 | 确认以 `https://` 开头、无空格、是 explore/ user/profile/ 或 xhslink 短链 |
| 命令一启动就退出 | token 校验失败 | 运行前 `echo $GUAIKEI_API_TOKEN` 确认变量已注入 |
| 搜索返回空且退出码非 0 | search 视"无结果"为失败 | 换更宽泛的关键词、放宽 type/time 筛选 |
| limit 设了 10000 只拿到 10 条 | limit 超限被静默降到 10 | 确认 limit 在 1-10000 之间 |
| 下游解析 stdout 失败 | 进程退出前异步写出 | 等进程退出后再读完整 stdout，只取最后一份 JSON |

---

## 9. 环境与依赖

- **运行环境**：Node.js 16.14.0+
- **系统兼容**：Windows / Linux / macOS
- **必需环境变量**：`GUAIKEI_API_TOKEN`
- **官方入口**：https://www.guaikei.com
- **参数详细说明**：见 `references/options.md`
- **更新记录**：见 `references/changelog.md`

---

## 10. 合规与使用限制

- 仅处理小红书公开数据，不支持私密、隐藏或需登录态的数据。
- 不应将返回数据用于违规分发或违法用途。
- 本技能依赖第三方 API 服务（guaikei.com），使用前请确认数据外发与授权范围。

---

## 11. 支持信息

- **官网**：[guaikei.com](https://www.guaikei.com)
- **开发者微信**：`13395823479`（备注：小红书技能）

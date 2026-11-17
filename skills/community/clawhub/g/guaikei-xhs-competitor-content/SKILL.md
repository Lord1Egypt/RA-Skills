---
name: guaikei-xhs-competitor-content
name_cn: guaikei·小红书竞品内容获取
description: >-
  搜小红书笔记、看笔记详情、查笔记评论、查博主作品。当用户提到小红书并想拿到笔记/评论/博主数据时使用本技能；即使用户没说"数据"或"搜索"，只要给了关键词或小红书链接并想了解内容也适用。不用于其他平台或需登录的操作。
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
    GUAIKEI_API_TOKEN: "小红书数据 API 访问令牌（32 位十六进制）。未配置时所有命令退出码 1。通过 https://www.guaikei.com 开通，或联系开发者 wx 13395823479。"
  category:
    - "数据分析"
    - "内容创作"
    - "商业运营"
    - "市场调研"
    - "社媒洞察"
  tags:
    - "小红书"
    - "红笔记"
    - "xhs"
    - "rednote"
    - "关键词搜索"
    - "笔记详情"
    - "评论获取"
    - "博主作品监控"
    - "竞品分析"
    - "爆款挖掘"
    - "KOL筛选"
    - "趋势洞察"
  examples:
    - "帮我找最近一周小红书里'露营装备'的高赞图文笔记: node src/xiaohongshu/search-cli.js --keyword '露营装备' --type 2 --sort 2 --limit 10"
    - "分析这条小红书笔记评论区的主要观点和负面反馈: node src/xiaohongshu/detail-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 100"
    - "看这个小红书博主最近 20 条作品都在发什么: node src/xiaohongshu/post-cli.js --url 'https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy' --limit 20"
    - "拉这条笔记的评论做观点聚类: node src/xiaohongshu/comment-cli.js --url 'https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy' --limit 100"
---

# guaikei·小红书竞品内容获取

> 小红书公开数据检索技能。四大能力：关键词搜索、笔记详情、评论获取、博主作品监控。仅处理公开数据，不登录、不发布、不互动。

---

## 如何使用本文档

本文档是一棵**决策树**。拿到用户请求后，从「入口」出发，按用户给的信息走对应分支，到叶子节点执行命令，再按「验收」分支检查结果。不需要通读全文。

---

## 入口：用户给了什么？

```
用户请求到达
    │
    ├─ A. 关键词（无链接） ──────────→ 分支 A
    ├─ B. xiaohongshu.com/explore/ 链接 → 分支 B
    ├─ C. xiaohongshu.com/user/profile/ 链接 → 分支 C
    ├─ D. xhslink.com / xhslink.cn 短链 → 分支 D
    ├─ E. 只说了业务目标，没有关键词也没给链接 → 分支 E
    └─ F. 不是小红书 / 想登录发布 → 分支 F（不调用）
```

---

## 分支 A：用户给了关键词

```
分支 A
  │
  ├─ A1. 想搜内容 ──→ 执行 search-cli
  │     命令：node src/xiaohongshu/search-cli.js --keyword "<词>" [选项]
  │     │
  │     ├─ 可选筛选项（缺了就用默认值，不必追问）：
  │     │   --type   0全部 / 1视频 / 2图文       默认 0
  │     │   --sort   0综合 / 1最新 / 2点赞 / 3评论 / 4收藏  默认 0
  │     │   --time   0全部 / 1一天 / 2一周 / 3半年  默认 0
  │     │   --limit  1-10000                      默认 10
  │     │
  │     └─→ 验收（见「验收树」）
  │
  └─ A2. 用户表达笼统（"帮我做小红书竞品分析"）
        └─ 先追问：关键词是什么？关心最新/点赞/收藏？图文/视频/全部？
           确认后回到 A1
```

**示例**：用户说"帮我找露营装备的高赞图文笔记"
→ `node src/xiaohongshu/search-cli.js --keyword "露营装备" --type 2 --sort 2 --limit 10`

---

## 分支 B：用户给了笔记链接

链接形态：`https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy`

```
分支 B
  │
  ├─ B1. 想看笔记正文 + 评论 ──→ 执行 detail-cli
  │     命令：node src/xiaohongshu/detail-cli.js --url "<笔记链接>" [--limit N]
  │     可选 --limit：评论数量上限，1-10000，不传按默认
  │     └─→ 验收
  │
  └─ B2. 只想看评论，不要笔记正文 ──→ 执行 comment-cli
        命令：node src/xiaohongshu/comment-cli.js --url "<笔记链接>" [--limit N]
        可选 --limit：评论数量上限，1-10000，不传按默认
        └─→ 验收
```

**如何区分 B1 / B2**：用户说"看这条笔记"→ B1；用户说"拉评论""评论区怎么说"→ B2。

**示例**：用户说"分析这条笔记的评论区"
→ `node src/xiaohongshu/comment-cli.js --url "https://www.xiaohongshu.com/explore/xxx?xsec_token=yyy" --limit 100`

---

## 分支 C：用户给了博主主页链接

链接形态：`https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy`

```
分支 C
  │
  └─ C1. 想看博主最近发了什么 ──→ 执行 post-cli
        命令：node src/xiaohongshu/post-cli.js --url "<主页链接>" [--limit N]
        可选 --limit：作品数量上限，1-10000，不传按默认
        └─→ 验收
```

**示例**：用户说"看这个博主最近 20 条作品"
→ `node src/xiaohongshu/post-cli.js --url "https://www.xiaohongshu.com/user/profile/xxx?xsec_token=yyy" --limit 20`

---

## 分支 D：用户给了短链

链接形态：`https://xhslink.com/m/xxx` 或 `https://xhslink.cn/m/xxx`

```
分支 D
  │
  └─ 短链不透明，无法判断指向笔记还是主页
     │
     ├─ D1. 用户明确说"看评论/看详情" ──→ 试走 B1 或 B2
     ├─ D2. 用户明确说"看博主作品" ──→ 试走 C1
     └─ D3. 目标不明确 ──→ 先追问：请提供完整链接
                            （explore/ 或 user/profile/ 开头）
```

短链结果异常时，优先请用户提供完整链接。

---

## 分支 E：用户只说了业务目标

用户说"帮我做小红书竞品分析""帮我挖掘爆款选题"——但没有给关键词，也没给链接。

```
分支 E
  │
  └─ 先拆解任务，确认输入：
     ├─ 要搜关键词？→ 追问关键词，确认后回到 分支 A
     ├─ 要看某篇笔记？→ 追问笔记链接，确认后回到 分支 B
     └─ 要看某个博主？→ 追问主页链接，确认后回到 分支 C
```

不要在缺关键输入时硬调命令。

---

## 分支 F：不调用

```
分支 F（以下情况不走本技能）
  ├─ 平台不是小红书（抖音/B站/微博/公众号）→ 不调用
  ├─ 用户只想写文案/改标题/生成脚本，没要求查数据 → 不调用
  ├─ 用户要登录/发布/点赞/关注/评论互动 → 不调用
  └─ 用户要获取私密/隐藏/登录态数据 → 不调用
```

---

## 验收树：命令执行后怎么判断结果

```
命令返回 stdout
  │
  ├─ status: "success" ──→ 正常，results 有数据
  │     └─ 交付：返回结构化 JSON + 简要摘要
  │        可衔接：选题汇总 / 高赞对比 / 评论聚类 / 竞品风格总结 / 报告生成
  │
  ├─ status: "empty" ──→ 成功但无数据
  │     ├─ search 无结果 → 换更宽泛关键词 / 放宽 type/time
  │     └─ detail/comment 空数组 → 正常，该笔记确无评论
  │     ※ 空数组 ≠ 失败，不要当错误处理
  │
  └─ status: "error" ──→ 失败，results 为 null
        │
        ├─ error_code 401 / 403
        │   原因：GUAIKEI_API_TOKEN 未配置或无效
        │   自查：①确认环境变量已注入当前进程；②token 须 32 位十六进制，无多余空格；③去 guaikei.com 重新开通
        │
        ├─ error_code 429
        │   原因：频率限制
        │   自查：降低频率、减小 limit、稍后重试
        │
        ├─ error_code 500 / 502 / 503
        │   原因：第三方 API 临时故障
        │   自查：等 1-2 分钟重试；持续出现则联系支持
        │
        ├─ error_code ERRCODE_xxx
        │   原因：业务错误（笔记已删除/不存在/无权限）
        │   自查：换一条确认存在的链接；不随重试变好，不要反复重试同一链接
        │
        ├─ error_code ETIMEDOUT / UNKNOWN
        │   原因：网络超时或无法解析响应
        │   自查：检查网络/代理；确认能访问 guaikei.com；重试一次
        │
        └─ "链接格式无效"
            原因：链接不合法
            自查：①以 https:// 开头；②无前后空格；③是 explore/ 或 user/profile/ 或 xhslink 合法形态
```

**三条铁律**：
1. 失败不编造数据，不把空结果当成功结论
2. 解析 stdout 只取最后一份 JSON（status 字段唯一标识），不要把多份输出拼在一起
3. 等进程退出后再读完整 stdout

---

## 链接规则速查

| 链接形态 | 走哪条分支 | 说明 |
|---|---|---|
| `www.xiaohongshu.com/explore/...` | 分支 B | 笔记链接，走 detail-cli 或 comment-cli |
| `www.xiaohongshu.com/user/profile/...` | 分支 C | 博主主页，走 post-cli |
| `xhslink.com/m/...` 或 `xhslink.cn/m/...` | 分支 D | 短链不透明，目标不明先追问 |
| 带空格 / 用 `http://` | 任意分支前 | 先 trim、http→https 归一再传入 |
| 博主链接传给 detail/comment | — | 链接类型错配，接口返回业务错误 |
| 笔记链接传给 post | — | 同上 |

---

## 反模式清单

| # | 做法 | 后果 |
|---|---|---|
| 1 | 博主链接传给 detail-cli / comment-cli | 链接类型错配，业务错误 |
| 2 | 笔记链接传给 post-cli | 同上 |
| 3 | 短链不追问就硬跑 | 结果异常，无法判断指向 |
| 4 | 没关键词/没链接就执行 | 命令无法运行 |
| 5 | 传带空格或 http:// 的脏链接 | 被拒绝 |
| 6 | limit 写 > 10000（如 20000） | 静默降到 10，不是"没返回" |
| 7 | 关键词喂 emoji / 纯符号 | 清洗成空串，触发"关键词无效" |
| 8 | 失败时编造数据 | 交付错误结论 |

---

## 参数简写速查

| 全称 | 简写 | 适用脚本 | 说明 |
|---|---|---|---|
| `--keyword` | `-k` | search | 搜索关键词，必填 |
| `--type` | `-t` | search | 0全部/1视频/2图文 |
| `--sort` | `-s` | search | 0综合/1最新/2点赞/3评论/4收藏 |
| `--time` | `-i` | search | 0全部/1一天/2一周/3半年 |
| `--limit` | `-l` | 全部 | 1-10000，search 默认 10 |
| `--url` | `-u` | detail/post/comment | 链接，必填 |
| `--help` | `-h` | 全部 | 显示帮助 |

---

## 环境与支持

| 项目 | 内容 |
|---|---|
| 运行时 | Node.js 16.14.0+ |
| 系统 | Windows / Linux / macOS |
| 必需环境变量 | `GUAIKEI_API_TOKEN`（32 位十六进制） |
| 开通渠道 | https://www.guaikei.com |
| 人工支持 | 微信 13395823479（备注：小红书技能） |
| 参数详情 | references/options.md |
| 更新记录 | references/changelog.md |

---

## 合规边界

- 仅处理小红书公开数据
- 不支持私密、隐藏或需要登录态的数据
- 不登录账号、不发布内容、不互动点赞
- 不应将返回数据用于违规分发或违法用途
- 依赖第三方 API 服务（guaikei.com），使用前确认数据外发与授权范围

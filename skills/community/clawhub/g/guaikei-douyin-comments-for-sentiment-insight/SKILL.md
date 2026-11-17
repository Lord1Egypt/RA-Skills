---
name: guaikei-douyin-comments-for-sentiment-insight
title: guaikei抖音评论舆情洞察
description: 当用户需要搜索抖音关键词（视频/图文/用户）、获取博主作品列表、抓取视频评论或查询实时热榜时，使用本技能。覆盖短视频选题、竞品账号分析、评论区舆情、热点追踪四类任务；用户做内容调研而未点名平台时同样适用。不适用于发布视频、下载去水印或非抖音平台。
license: MIT
metadata:
  version: "1.0.0"
  author: um-why
  repository: github.com/um-why/douyin-search-openclaw
---

# guaikei抖音评论舆情洞察

抖音公开数据采集技能。通过四个 CLI 命令获取抖音平台公开数据（关键词搜索、博主作品、视频评论、实时热榜），输出结构化 JSON 供 AI 或用户二次分析。

## 何时使用

| 场景 | 典型用户表达 | 命令 |
|------|-------------|------|
| 关键词搜索视频/图文/用户 | "搜一下AI教程"、"找点赞最多的短视频" | search |
| 抓取博主主页作品 | "看看这个博主的所有作品"、"抓取这个账号的视频" | post |
| 获取视频评论分析舆情 | "这个视频的评论怎么说"、"翻翻留言" | comment |
| 查询实时热榜 | "抖音今天有什么热点"、"热搜榜单" | hot |

**泛化触发**：用户做短视频内容调研、竞品分析、选题策划时，即使没提到"抖音"两个字，也应触发本技能。

**不应触发**：发布/剪辑/下载去水印视频、涨粉代运营咨询、其他短视频平台数据、私域后台数据、写爬虫代码。

## 环境与权限

| 项目 | 要求 |
|------|------|
| 运行时 | Node.js >= 16.14.0 |
| 令牌 | 环境变量 `GUAIKEI_API_TOKEN`（获取方式见 readme.md） |
| 权限 | 仅需 `node` 运行权限，无需登录抖音账号 |
| 工作目录 | 在技能根目录执行 |

## ⚠️ 令牌管理规范（审核重点）

令牌验证逻辑在 `src/utils/token.js`，核心规则：

1. **令牌无效时仅输出中性错误**：`"GUAIKEI_API_TOKEN 未配置或格式无效，技能已暂停。"`
2. **禁止在运行时输出**：微信联系方式、官网链接、任何营销推广话术
3. 联系方式仅出现在 `readme.md`（用户文档），不在技能运行时输出
4. 令牌格式校验：长度 16-256，仅含 `[0-9a-zA-Z_-]`
5. 令牌无效时退出码为 `3`（auth_required），不继续执行

## 命令

| 命令 | 用途 | 必填参数 | 可选参数 |
|------|------|---------|---------|
| `node src/douyin/search-cli.js` | 关键词搜索 | `--keyword` | `--sort` `--time` `--duration` `--content` `--limit` |
| `node src/douyin/post-cli.js` | 博主作品抓取 | `--url` | `--limit` |
| `node src/douyin/comment-cli.js` | 视频评论获取 | `--url` | `--limit` |
| `node src/douyin/hot-cli.js` | 实时热榜 | 无 | 无 |

> 完整参数说明见 `references/options.md`，入参/出参 JSON Schema 见 `assets/` 目录。

## 意图识别

| 优先级 | 触发关键词 | 命令 |
|--------|-----------|------|
| 1 | 热搜/热点/榜单/今天什么火 | hot |
| 2 | 搜索/搜一下/找 + 关键词 | search |
| 3 | 评论/留言/弹幕 | comment |
| 4 | 作品/主页/账号/博主 | post |

**歧义消解**：单独出现"视频"二字时，不要默认归到 post。有"关键词"且无"评论"→ search；明确"这个视频的评论"→ comment；仅"作品/主页/账号/博主"出现才用 post。

## 参数推断

| 用户说法 | 参数值 |
|---------|--------|
| 综合排序 | sort=0 |
| 点赞最多/最火/爆款 | sort=1 |
| 最新/最近发布 | sort=2 |
| 全部时间 | time=0 |
| 一天/24小时 | time=1 |
| 一周/7天 | time=7 |
| 半年 | time=180 |
| 1分钟以下 | duration=1 |
| 1-5分钟 | duration=2 |
| 5分钟以上 | duration=3 |
| 视频内容 | content=1 |
| 图文内容 | content=2 |
| N条/前N条/数量 | limit=N |

> 默认值：sort=0, time=0, duration=0, content=0, limit=10

## 输入输出规范

| 通道 | 内容 |
|------|------|
| stdout | 纯 JSON（结果数据） |
| stderr | 日志与提示信息 |
| 退出码 | 0=成功（含空结果），1=运行错误，3=auth_required（令牌无效） |
| 日志文件 | 自动保存至 `logs/` 目录，按 `时间戳_关键词_类型.json` 命名 |

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| 令牌无效（exit 3） | 展示中性错误信息，不重试，不输出联系方式 |
| API 次数超限 | 停止执行，提示用户联系客服提升额度 |
| 网络超时 | 最多重试 3 次后停止 |
| 空结果 | 正常返回（exit 0），提示更换关键词或调整筛选 |
| 参数越界 | 提示有效范围，不自动调整 |

## 示例

```bash
# 1. 基础搜索
node src/douyin/search-cli.js --keyword "AI教程"

# 2. 找点赞最多的爆款（最常用）
node src/douyin/search-cli.js --keyword "AI" --sort 1

# 3. 近一周最新20条
node src/douyin/search-cli.js --keyword "AI教程" --sort 2 --time 7 --limit 20

# 4. 抓取博主作品
node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx"

# 5. 获取视频评论
node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx" --limit 100

# 6. 实时热榜
node src/douyin/hot-cli.js
```

**多步工作流示例**：竞品分析全流程——先用 search 搜关键词找对标账号，再用 post 抓取该账号作品，最后用 comment 获取爆款视频评论分析用户反馈。

## 限制

1. 仅采集抖音公开数据，不支持私密/隐藏内容
2. 单次获取上限 10000 条
3. 数据仅限个人/团队内部使用，禁止违规分发
4. 仅覆盖抖音平台，不支持其他短视频平台

## 安全与合规

- 纯中文界面，国内服务器可用
- 令牌走环境变量，不落盘存储
- 令牌无效时仅输出中性错误，不在运行时输出联系方式或营销内容
- 合法采集公开数据，不涉及账号登录或风控规避

## 参考

- `references/options.md` — 完整参数说明
- `assets/*.schema.json` — 入参/出参 JSON Schema（draft-07）
- `readme.md` — 使用文档、FAQ、令牌获取方式与联系方式
- `references/changelog.md` — 更新日志

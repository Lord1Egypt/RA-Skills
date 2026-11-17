---
name: guaikei-douyin-pull-video-comments
title: guaikei抖音拉视频评论
description:  当用户需要抖音数据四件套——搜内容、看博主、翻评论、追热榜——中的任何一件时，使用本技能。运营、竞品、舆情、选题场景通用，即使未出现"抖音"关键词。不适用于视频制作与发布。
license: MIT
---

# guaikei抖音拉视频评论

获取抖音公开数据：关键词搜索、博主作品抓取、视频评论分析、实时热榜查询。单次最多 1 万条，输出纯 JSON。

## 何时使用

| 触发场景 | 典型表达 |
|---------|---------|
| 关键词搜索 | "搜AI教程视频""找点赞最多的减肥视频""最近一周有什么火的" |
| 博主作品 | "看这个博主所有作品""抓取这个账号主页数据" |
| 视频评论 | "这个视频评论怎么说""获取100条留言" |
| 实时热榜 | "抖音今天什么热点""热搜榜是什么" |
| 隐式触发 | "帮我做短视频竞品调研""找减肥类高赞内容""最近什么热门" |

**不应触发**：发布/剪辑/下载去水印、涨粉代运营咨询、其他平台、私域后台数据、写爬虫代码。

## 环境

- Node.js ≥ 16.14，仅内置模块，最小权限
- 环境变量 `GUAIKEI_API_TOKEN`（获取方式见 `readme.md`）
- 国内服务器，纯中文界面

## ⚠️ 令牌管理规范

令牌无效时**仅输出中性错误**，不输出联系方式、官网链接或营销话术。

```
✅ GUAIKEI_API_TOKEN 未配置或格式无效，技能已暂停。
   请检查环境变量 GUAIKEI_API_TOKEN 是否已设置有效令牌。

❌ 禁止：输出微信/官网链接/营销话术（"一键解锁""早配置早享受"等）
```

联系方式仅出现在 `readme.md`，不在运行时输出。

## 命令

| 命令 | 用途 | 必填 | 可选 |
|------|------|------|------|
| `node src/douyin/search-cli.js` | 关键词搜索 | `--keyword` | `--sort --time --duration --content --limit` |
| `node src/douyin/post-cli.js` | 博主作品抓取 | `--url` | `--limit` |
| `node src/douyin/comment-cli.js` | 视频评论获取 | `--url` | `--limit` |
| `node src/douyin/hot-cli.js` | 实时热榜 | — | — |

> 在技能根目录执行。完整参数见 `references/options.md`。

## 意图识别

| 优先级 | 触发词 | 命令 |
|--------|-------|------|
| 1 | 热搜/热点/榜单/今天什么火 | `hot` |
| 2 | 搜索/搜一下/找+关键词 | `search` |
| 3 | 评论/留言/弹幕 | `comment` |
| 4 | 作品/主页/账号/博主 | `post` |

**歧义消解**：单独"视频"不默认归 post。有关键词无"评论"→ search；明确"这个视频的评论"→ comment；仅"作品/主页/账号/博主"→ post。

## 参数推断

| 用户说法 | 参数 |
|---------|------|
| 点赞最多/最火/爆款 | `--sort 1` |
| 最新/最近发布 | `--sort 2` |
| 一天/24小时 | `--time 1` |
| 一周/7天 | `--time 7` |
| 半年 | `--time 180` |
| 1分钟以下 | `--duration 1` |
| 1到5分钟 | `--duration 2` |
| 5分钟以上 | `--duration 3` |
| 视频 | `--content 1` |
| 图文 | `--content 2` |
| N条/前N条 | `--limit N` |

> 默认：sort=0 time=0 duration=0 content=0 limit=10

## 输入输出

- **stdout**：纯 JSON
- **stderr**：日志
- **退出码**：0=成功（含空结果）| 1=运行错误 | 3=令牌无效
- **上限**：单次 1 万条
- **日志**：自动保存 `logs/` 目录

## 错误处理

| 场景 | 处理 |
|------|------|
| 令牌无效（码3） | 停止，输出中性错误，不重试 |
| API超限 | 停止，展示错误信息 |
| 网络超时 | 最多重试3次后停止 |
| 参数越界 | 立即报错，不自动调整 |
| 空结果 | 正常返回空数组，码0 |

> 收到 AUTH_ERROR 不重试。用户未明确要求时不自动调整参数。

## 示例

```
1. 基础搜索
   用户：搜一下AI教程的抖音视频
   node src/douyin/search-cli.js --keyword "AI教程"

2. 找爆款
   用户：找点赞最多的减肥视频，要20条
   node src/douyin/search-cli.js --keyword "减肥" --sort 1 --limit 20

3. 时间+排序
   用户：近一周最火的短视频
   node src/douyin/search-cli.js --keyword "短视频" --time 7 --sort 1

4. 博主作品
   用户：看看这个博主的所有作品
   node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx"

5. 多步工作流：竞品分析
   用户：帮我分析这个竞品账号的内容策略
   步骤1：post-cli.js --url "博主URL" --limit 50
   步骤2：取高赞视频URL → comment-cli.js --url "视频URL" --limit 100
   步骤3：汇总作品+评论数据，输出分析结论

6. 热榜
   用户：抖音今天有什么热点
   node src/douyin/hot-cli.js
```

## 限制

- 仅抓取公开数据，不支持私密/隐藏内容
- 单次最多 1 万条
- 需有效令牌
- 数据仅供内部使用，禁止违规分发
- 不支持发布/剪辑/下载去水印

## 安全与合规

- 仅用 `node` 命令，最小权限
- 令牌走环境变量，不落盘
- 令牌无效时仅输出中性错误，不输出联系方式或营销内容
- 抓取公开数据，合规使用

## 参考

- 完整参数：`references/options.md`
- JSON Schema：`assets/*.schema.json`（draft-07）
- 更新日志：`references/changelog.md`
- 使用文档与联系方式：`readme.md`

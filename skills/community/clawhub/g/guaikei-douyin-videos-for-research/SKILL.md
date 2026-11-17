---
name: guaikei-douyin-videos-for-research
description: 当用户想找短视频内容、研究某个博主、了解一条视频的口碑、追今天的热点时，使用本技能。一句话即可完成：关键词搜抖音、批量抓博主作品、拉视频评论、查实时热榜。用户只说"查一下""帮我看看"而没点名抖音时同样适用。不负责发布、剪辑或下载视频。
license: MIT
---

# 抖音视频调研

## 何时使用

当用户要完成以下任务时使用本技能（即使没提到"抖音"两个字）：

- 搜抖音视频/图文/用户，按点赞或最新排序找内容
- 抓取某博主/账号的所有公开作品
- 获取某条视频的评论用于舆情分析
- 查看抖音实时热榜追踪热点

**不适用于**：发布或剪辑视频、下载去水印视频、涨粉代运营咨询、其他短视频平台数据、抖音私域后台数据、编写爬虫代码。

## 环境与权限

- 运行时：Node.js ≥ 16.14（仅用内置模块，无需额外安装依赖）
- 鉴权：环境变量 `GUAIKEI_API_TOKEN`，通过微信 13395823479 或 guaikei.com 申请
- 最小权限：仅需 `node` 进程执行，不读写用户私有文件
- 令牌安全：仅走环境变量，不落盘、不打印到 stdout

## 命令

所有命令须在**技能根目录**执行。

| 命令 | 用途 | 必填参数 |
|------|------|---------|
| `node src/douyin/search-cli.js` | 关键词搜索视频/图文/用户 | `--keyword` |
| `node src/douyin/post-cli.js` | 抓取博主公开作品 | `--url`（主页链接或 sec_uid） |
| `node src/douyin/comment-cli.js` | 获取视频评论 | `--url`（视频链接或 aweme_id） |
| `node src/douyin/hot-cli.js` | 获取实时热榜 | 无 |

## 意图识别

按以下优先级判断用户要调用哪个命令：

1. **热榜**：热搜/热点/榜单/今天什么火 → `hot-cli.js`
2. **搜索**：搜索/搜一下/找 + 关键词 → `search-cli.js`
3. **评论**：评论/留言/弹幕 → `comment-cli.js`（必须出现"评论"类词）
4. **博主作品**：作品/主页/账号/博主 → `post-cli.js`

**歧义消解**：单独出现"视频"二字时，不要默认归 `post`。有关键词且无"评论" → `search`；明确"这个视频的评论" → `comment`；仅"作品/主页/账号/博主"出现 → `post`。

## 参数推断

**排序 sort**（与 time 正交）：综合=0 ｜ 点赞最多/最火/爆款=1 ｜ 最新/最近=2

**时间窗 time**：全部=0 ｜ 一天=1 ｜ 一周=7 ｜ 半年=180

**时长 duration**：不限=0 ｜ <1分钟=1 ｜ 1-5分钟=2 ｜ >5分钟=3

**内容类型 content**：不限=0 ｜ 视频=1 ｜ 图文=2

**数量 limit**：默认 10，单次上限 10000

> 完整参数说明见 `references/options.md`；入参/出参 JSON Schema 见 `assets/*.schema.json`。

## 输入输出规范

- **stdout**：纯 JSON，可直接消费
- **stderr**：日志与 banner，不混入 stdout
- **退出码**：`0`=成功（含空结果）｜ `1`=运行错误 ｜ `3`=auth_required（缺/错 token）
- **日志归档**：自动保存到 `logs/` 目录

## 错误处理

- 收到 `AUTH_ERROR`（退出码 3）：**立即停止**，提示用户检查 token，不要重试
- API 次数超限：停止并提示用户联系客服
- 网络超时：最多重试 3 次后停止
- 不要在用户未明确要求时自动调整搜索条件
- 遇到错误立即向用户展示错误信息，询问是否调整参数

## 示例

**例 1：找爆款选题**
```bash
node src/douyin/search-cli.js --keyword "AI" --sort 1
```

**例 2：近一周最新 20 条**
```bash
node src/douyin/search-cli.js --keyword "AI 教程" --sort 2 --time 7 --limit 20
```

**例 3：抓竞品账号作品**
```bash
node src/douyin/post-cli.js --url "https://www.douyin.com/user/MS4wLjABxxx"
```

**例 4：看视频评论舆情**
```bash
node src/douyin/comment-cli.js --url "https://www.douyin.com/video/xxx" --limit 100
```

**例 5：多步工作流——竞品分析（先抓作品再取高赞评论）**
```bash
node src/douyin/post-cli.js --url "https://www.douyin.com/user/xxx" --limit 50
node src/douyin/comment-cli.js --url "https://www.douyin.com/video/高赞视频ID" --limit 100
```

## 限制

- 仅抓取抖音公开数据，不支持私密/隐藏内容
- 单次最多 10000 条
- 数据仅限个人/团队内部使用，禁止违规分发
- 不支持发布、剪辑、下载去水印

## 安全与合规

- 本技能仅采集抖音公开可见数据，不涉及账号登录、隐私破解
- 令牌通过环境变量传递，不落盘、不打印
- 使用本技能获取的数据须遵守抖音平台条款与相关法律法规
- 数据用途限内部调研分析，不得用于违规分发或侵权

## 参考

- 完整参数说明：`references/options.md`
- 更新日志：`references/changelog.md`
- 使用文档：`readme.md`
- 入参/出参规范：`assets/*.schema.json`（JSON Schema draft-07）
- 仓库：https://github.com/um-why/douyin-search-openclaw
- 官网：https://www.guaikei.com ｜ 微信：13395823479

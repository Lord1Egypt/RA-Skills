# 平台接口契约（Platform Contracts）

本文件是 `scripts/feed_core.py` 中 `PLATFORMS` 配置表的权威说明。新增平台只需在配置表加一项，无需改动其它代码。

所有接口均为 `POST`，`Content-Type: application/json`，鉴权头 `X-API-KEY: <REDFOX_API_KEY>`。
统一响应结构：`{ "code": int, "msg": str, "data": { "list": [ ... ] } }`。

| code | 含义 | 处理方式 |
|------|------|----------|
| 200 / 2000 | 成功 | 读取 `data.list` |
| 3108 | 限频 | sleep 5s 后重试一次 |
| 3106 / 3107 | API Key 错误 | 报错终止，提示重新配置 |

---

## 1. 快手（kuaishou / ks）

| 项 | 值 |
|----|----|
| Endpoint | `https://redfox.hk/story/api/parseWork/queryKsAiMsgs/batch` |
| source | `AI快手信息源-ClawHub` |
| 关键词模式 | `keywords`（数组，一次传全部） |
| 翻页 | 支持，`pageNum` 递增，`pageSize=200`，最多 10 页 |
| 时间参数 | `startTime` / `endTime`，格式 `YYYY-MM-DD 00:00:00` ~ `YYYY-MM-DD 23:59:59` |
| 数据更新 | 每日 15:00 更新前一天数据 |
| 排序主指标 | `likeCount + shareCount + commentCount`（互动量） |
| 展示指标 | 点赞 `likeCount`、分享 `shareCount`、评论 `commentCount` |
| 详情链接 | `https://www.kuaishou.com/short-video/{photoId}` |
| 主题色 | `#FF4906` |
| 单位 | 条 |

**封面兼容处理**：快手返回的封面可能为 HEIF/HEIC 或私有格式 `kvif`/`kpg`，需替换为 `.jpg`，并把路径中的 `/heif/`、`/heic/` 换成 `/jpg/`（注意 URL 可能带 `?tag=` 查询参数，后缀匹配要在 `?`/`#` 之前）。

---

## 2. 公众号（gzh / wechat）

| 项 | 值 |
|----|----|
| Endpoint | `https://redfox.hk/story/api/parseWork/queryAiMsgs` |
| source | `AI公众号信息源-ClawHub` |
| 关键词模式 | `keyword`（单个，多关键词需逐个请求） |
| 翻页 | 支持，`pageSize=20`；首关键词最多 5 页，其余关键词最多 2 页 |
| 时间参数 | **不支持**，不传 `startTime` / `endTime` |
| 数据更新 | 每日 16:00 更新前一天数据 |
| 排序主指标 | `likeCount + shareCount + commentCount`（互动量） |
| 展示指标 | 点赞 `likeCount`、分享 `shareCount`、评论 `commentCount`（可选，接口可能返回 `null`） |
| 详情链接 | 接口直接返回 `url` |
| 主题色 | `#FF5722` |
| 单位 | 篇 |

**注意**：因不支持时间过滤，`--date` 只影响日报标题与可用性预检，不影响返回内容；返回的是接口当前收录的最新文章。

---

## 3. B站（bili / bilibili）

| 项 | 值 |
|----|----|
| Endpoint | `https://redfox.hk/story/api/parseWork//queryBiliAiMsgs/batch`（双斜杠为接口现状，勿"修正"） |
| source | `B站AI信息源-ClawHub` |
| 关键词模式 | `keywords`（数组）+ `keyword`（主关键词，取 `keywords[0]`） |
| 翻页 | 不支持，单次请求 `pageSize=200` |
| 时间参数 | `startTime` / `endTime`，格式 `YYYY-MM-DD 00:00:00` ~ `YYYY-MM-DD 24:00:00` |
| 数据更新 | 每日 15:00 更新前一天数据 |
| 排序主指标 | `likeCount`（点赞量） |
| 展示指标 | 分享 `shareCount`、点赞 `likeCount`、评论 `commentCount` |
| 详情链接 | 接口不返回 `url`，用 `photoId`（BV 号）拼接 `https://www.bilibili.com/video/{photoId}` |
| 主题色 | `#FB7299` |
| 单位 | 条 |

---

## 4. 视频号（sph / channels）

| 项 | 值 |
|----|----|
| Endpoint | `https://redfox.hk/story/api/parseWork/querySphAiMsgs` |
| source | `AI视频号信息源-ClawHub` |
| 关键词模式 | `keyword`（单个，多关键词需逐个请求） |
| 翻页 | 不支持，单次请求 `pageSize=200` |
| 时间参数 | `startTime` / `endTime`，**仅日期**，格式 `YYYY-MM-DD`，起始含、结束不含（结束日 = 目标日 + 1 天） |
| 数据更新 | 每日 16:00 更新前一天数据 |
| 排序主指标 | `likeCount + shareCount + commentCount`（互动量） |
| 展示指标 | 点赞 `likeCount`、分享 `shareCount`、评论 `commentCount` |
| 详情链接 | **无**，视频号作品不支持站外跳转，标题渲染为纯文本 |
| 主题色 | `#FA9D3B` |
| 单位 | 篇 |

---

## 5. 小红书（xhs / xiaohongshu）

| 项 | 值 |
|----|----|
| Endpoint | `https://redfox.hk/story/api/parseWork/queryXhsAiMsgs` |
| source | `AI小红书信息源-ClawHub` |
| 关键词模式 | `keyword`（单个，多关键词需逐个请求） |
| 翻页 | 不支持，单次请求 `pageSize=50` |
| 时间参数 | `startTime` / `endTime`，**仅日期**，格式 `YYYY-MM-DD`，起始含、结束不含 |
| 数据更新 | 每日 16:00 更新前一天数据 |
| 排序主指标 | `likeCount + shareCount + commentCount`（互动量） |
| 展示指标 | 点赞 `likeCount`、分享 `shareCount`、评论 `commentCount` |
| 详情链接 | `https://www.xiaohongshu.com/explore/{photoId}` |
| 主题色 | `#FF2442` |
| 单位 | 篇 |

---

## 公共响应字段

| 字段 | 说明 |
|------|------|
| `photoId` | 作品唯一 ID（去重键；B站为 BV 号，小红书为笔记 ID） |
| `title` | 标题，可能为空，统一回退为 `无标题` |
| `userName` | 作者昵称 |
| `coverUrl` | 封面图，可能为空；视频号/小红书封面有防盗链，需 `referrerpolicy="no-referrer"` |
| `likeCount` | 点赞数 |
| `shareCount` | 分享数 |
| `commentCount` | 评论数（公众号可能为 `null`） |
| `type` | 一级标签，逗号分隔，聚类首选 |
| `topic` | 二级标签，逗号分隔，聚类补充 |
| `url` | 详情链接（仅公众号稳定返回） |

`engagement`（互动量）不是接口字段，由本地按 `likeCount + shareCount + commentCount` 计算，作为快手/公众号/视频号/小红书的排序主指标。
**`readCount` 五个接口均不返回**，历史文档中"快手播放量 / 公众号阅读量"的说法已失效，不得作为排序依据。

所有数值字段都可能为 `null`，取值时必须用 `a.get(k) or 0`，禁止直接下标访问。

---

## 聚类算法（六步，全平台共用）

1. 提取每篇作品的有效标签（`type` 优先、`topic` 补充），剔除泛标签（`AI`、`人工智能`、`科技`、`技术` 等），按**首个有效标签**分组；无标签归入「其他」。
2. 大组拆分：组内数量 > `max(total*0.2, 25)` 时，用**第二标签**二次拆分。
3. 小组合并：数量 < `min_group` 的组先尝试用其它标签匹配进已有大组，匹配不到再并入「其他」。`min_group` 按样本量自适应（`total >= 60` 时为 3，否则为 2）。
4. 过大组按标题高频中文词（2–4 字、非停用词、出现 ≥ 5 次）再拆，最多 3 轮。
5. 分类数不足 5 个时，从最大组按第二标签继续拆出子组，直到无法再拆。
6. 输出按组内数量降序；组内按平台主指标降序，每组最多展示 `top_n`（默认 5）篇。

---

## 数据可用性预检

```
latest_available(update_hour) =
    today - 1 day   if now.hour >= update_hour
    today - 2 day   otherwise
```

请求日期（或日期区间的结束日）晚于 `latest_available` 时，**不得调用接口**，只输出提示并等待用户确认。
多平台运行时逐平台判断：不可用的平台跳过并提示，可用的平台正常执行；全部不可用则以退出码 0 结束并给出提示文案。

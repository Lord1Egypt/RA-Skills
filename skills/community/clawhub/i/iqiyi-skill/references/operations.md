# iqiyi-skill Operation 语义

本文件描述无登录版 MVP 暴露给 AI 的能力目录。结构化版本由 `../scripts/iqiyi-skill-catalog.mjs` 输出，数据源来自飞书文档「智能助理」：`https://iq.feishu.cn/wiki/WRmFw6W6bildBJkGTBnc1gtRnad`。

## 调用模型

- Base URL：`https://mesh.if.iqiyi.com/ai/zhipu`。
- 传输方式：POST JSON。
- 登录态：调用方如已有外部授权，可通过 Header `Authorization` 透传；无登录版 MVP 不创建、保存或刷新授权态。
- 标准输出字段：`message`、`prompt`、`data`、`col`、`intent`。
- 请求构造器：`buildOperationRequest(operationId, input, { authorization? })`，返回完整 `url`。
- 执行器：`executeOperation(operationId, input, { authorization?, fetchImpl? })`，真实触发请求并返回 `{ request, raw, formatted }`。
- 响应组织：`formatOperationResponse(payload)` 根据 `col` 输出 `collection`，根据 `data` 输出 `data`，否则输出 `message`。
- 推荐风格清单：`getRecommendStyleCatalog()` 返回截图中产品筛选支持的风格。
- 推荐风格归一化：`normalizeRecommendStyles(style, type)` 把用户措辞尽量落到当前类型支持的风格，并返回 warnings。

## Operation 表

| Operation | Endpoint | 输入 | 输出 | 意图 | 无登录策略 |
| --- | --- | --- | --- | --- | --- |
| `video.search` | `/video/search` | `q`、可选 `pageNum` | `message`、`prompt`、`col` 视频列表 | `interact > search(q)` | 可直接调用。 |
| `video.recommend` | `/video/recommend` | `type`、`style`、`kind` | `message`、`prompt`、`col` 视频列表 | `reference > recommendation(type;kind)` | `history`、`favor` 需要 Authorization；无授权时降级为 `hot`。 |
| `video.details` | `/video/details` | `title`、可选 `season`、`year` | `data` 视频详情、`bloopers` 周边视频 | `reference > video(Album/TV ID)` | 可直接调用。 |
| `star.search` | `/star/search` | `q` | `data` 明星详情 | `reference > star(Star ID)` | 可直接调用。 |
| `video.related` | `/video/related` | `title`、可选 `season`、`year` | `col` 相关视频列表 | `reference > related(TV ID)` | 可直接调用。 |
| `video.episode` | `/video/episode` | `title`、可选 `season`、`year` | `col` 选集列表 | `reference > episodes(Album ID)` | 可直接调用。 |
| `video.play` | `/video/play` | `title`、可选 `season`、`year`、`episode` | `data` 视频详情 | `command > play(qips)` | 不作为明确播放意图的默认入口；仅在需要 H5 降级、候选确认、播放详情或强制后端解析时调用。 |
| `playback.qips_open_or_control` | 本地 qips | qips 意图 | qips 字符串或执行命令 | qips command | 使用 `iqiyi-skill` 内置 qips 契约、脚本和参考资料。 |
| `client.install_check` | 宿主探针 | `platform` | 是否已安装或 unknown | none | 检测失败时走 H5 降级。 |
| `client.download_link` | 本地配置 | `platform` | 安装 URL | none | Mac: `https://app.iqiyi.com/mac/player/index.html`；PCA/Windows/UWP: `https://dl-static.iqiyi.com/hz/IQIYIsetup_skill01.exe`。 |
| `fallback.h5_play_url` | Web 降级 | `url` | H5 URL 和下载提示 | none | 无客户端时使用。 |

## 视频类型

飞书数据源定义的视频类型包括：

- `TvSeries`：电视剧
- `Movie`：电影
- `Variety`：综艺
- `Comic`：动漫
- `Cartoon`：儿童节目
- `Documentary`：纪录片
- `Course`：视频课程
- `Sport`：体育节目
- `MV`：音乐视频
- `Video`：短视频或其它频道

## 推荐 kind

`video.recommend` 的 `kind` 可使用：

- `suggest` / `推荐`：首页或频道首焦、猜你喜欢；有筛选时忽略筛选。
- `hot` / `热播`：风云榜热播。
- `soar` / `飙升`：风云榜飙升。
- `top` / `必看`：风云榜必看。
- `new` / `新片`：新片或预告片。
- `douban` / `豆瓣`：片库或豆瓣高分榜。
- `history` / `历史`：播放历史记录，需要 Authorization；无授权降级为 `hot`。
- `favor` / `收藏`：收藏夹，需要 Authorization；无授权降级为 `hot`。

## 推荐 style

`video.recommend` 的 `style` 必须尽量使用产品筛选支持的词。运行时从截图整理了以下类型的风格：

| 类型 | 支持 style |
| --- | --- |
| `TvSeries` / 电视剧 | 古装、战争、谍战、爱情、罪案、悬疑、家庭、军旅、喜剧、都市、武侠、言情、偶像、青春、农村、穿越、奇幻、历史、年代、科幻、生活、剧情、励志、婚姻、警匪、犯罪、推理、商战、宫廷、仙侠、神话、动作、复仇、惊悚、其他 |
| `ShortDrama` / 短剧 | 穿越、逆袭、重生、爱情、玄幻、现代言情、总裁、虐恋、甜宠、神豪、女性成长、古风权谋、家庭伦理、复仇、悬疑推理、古风言情、生活、刑侦、恐怖 |
| `Movie` / 电影 | 喜剧、动画、动作、爱情、恐怖、战争、惊悚、枪战、科幻、犯罪、悬疑、奇幻、剧情、青春、冒险、家庭、少儿、警匪、历史、武侠、伦理、灾难、传记、运动、音乐、魔幻、歌舞、戏曲、玄幻、悲剧、史诗、西部、纪录片、其他 |
| `Variety` / 综艺 | 喜剧、真人秀、音乐、脱口秀、观察、访谈、游戏、晚会、曲艺、竞技、竞演、文化、其他 |
| `Comic` / 动漫 | 玄幻、奇幻、武侠、恋爱、搞笑、冒险、热血、治愈、科幻、推理、竞技、励志、机战、偶像、其他 |
| `Manga` / 漫剧 | 逆袭、穿越、大女主、系统、玄幻、搞笑、废柴、悬疑、恋爱、末日、战神、扮猪吃老虎、修仙、觉醒、无敌、科幻、开局、异能 |
| `Documentary` / 纪录片 | 自然、历史、人文、美食、医疗、萌宠、财经、罪案、竞技、灾难、军事、探险、社会、科技、旅游、其他 |

常用近义归一：

- “全家一起看 / 合家欢 / 一家人 / 老少皆宜 / 亲子 / 阖家” → `家庭`
- “小朋友 / 小孩 / 儿童 / 孩子” → `少儿`
- “轻松 / 搞笑 / 逗乐 / 开心 / 爆笑” → `喜剧`
- “温馨 / 治愈 / 暖心” → `治愈`
- “烧脑 / 推理 / 破案” → `悬疑`
- “宇宙 / 未来 / 科技感” → `科幻`

## 请求构造示例

```js
import {
  buildOperationRequest,
  executeOperation,
  formatOperationResponse,
} from "./scripts/iqiyi-skill-catalog.mjs";

buildOperationRequest("video.search", { q: "周星驰演的电影", pageNum: 1 });
// POST https://mesh.if.iqiyi.com/ai/zhipu/video/search
// body: { q: "周星驰演的电影", pageNum: 1 }

await executeOperation("video.search", { q: "周星驰演的电影", pageNum: 1 });
// returns { request, raw, formatted }
// formatted.kind === "collection"; formatted.items is the video list.

buildOperationRequest("video.recommend", { type: "TvSeries", style: ["古装", "2024"], kind: "hot" });
// POST https://mesh.if.iqiyi.com/ai/zhipu/video/recommend
// body: { type: "TvSeries", style: ["古装", "2024"], kind: "hot" }

buildOperationRequest("video.recommend", { type: "电影", style: ["适合全家一起看的电影"], kind: "suggest" });
// POST https://mesh.if.iqiyi.com/ai/zhipu/video/recommend
// body: { type: "Movie", style: ["家庭"], kind: "suggest" }
// warnings: ["style=适合全家一起看的电影 normalized to 家庭"]

buildOperationRequest("video.recommend", { type: "Movie", kind: "收藏" });
// POST /video/recommend
// body: { type: "Movie", kind: "hot" }
// warnings: ["kind=favor requires Authorization; downgraded to hot"]

buildOperationRequest("video.recommend", { kind: "history" });
// POST /video/recommend
// body: { kind: "hot" }
// warnings: ["kind=history requires Authorization; downgraded to hot"]
```

命令行直接执行 Operation：

```bash
node .cursor/skills/iqiyi-skill/scripts/iqiyi-skill-catalog.mjs video.search '{"q":"周星驰演的电影","pageNum":1}'
```

`iqiyi-cli` 语法：

```bash
# 通用 skill 环境：真实请求
node .cursor/skills/iqiyi-skill/scripts/iqiyi-cli.mjs video search --q "周星驰" --pageNum 1
node .cursor/skills/iqiyi-skill/scripts/iqiyi-cli.mjs video recommend --type "电影" --style "适合全家一起看的电影" --kind suggest
node .cursor/skills/iqiyi-skill/scripts/iqiyi-cli.mjs video play --title "庆余年" --season 2 --episode 5
node .cursor/skills/iqiyi-skill/scripts/iqiyi-cli.mjs star search --q "刘德华"

# package-style 安装环境：若支持 package.json bin 入口，可直接使用
iqiyi-cli video search --q "周星驰" --pageNum 1
iqiyi-cli video recommend --type "电影" --style "适合全家一起看的电影" --kind suggest
iqiyi-cli video play --title "庆余年" --season 2 --episode 5
iqiyi-cli star search --q "刘德华"

# `video play` 默认本地生成 qips，不打网络；只看其它请求结构时使用 --dry-run
node .cursor/skills/iqiyi-skill/scripts/iqiyi-cli.mjs video recommend --type "电影" --style "合家欢" --dry-run
```

CLI 支持的操作包括：

- `video search`
- `video recommend`
- `video details`
- `video related`
- `video episode`
- `video play`
- `star search`

常用输出参数：

- `--dry-run`：只输出归一化后的请求。
- `--text`：只输出 `formatted.text`。
- `--raw`：输出接口原始 JSON。
- `--formatted`：输出格式化 JSON。
- `--request`：执行后输出请求信息。

返回组织约定：

- `col`：作为候选列表，输出 `formatted.kind = "collection"`、`formatted.items`、`formatted.text`。
- `data`：作为详情对象，输出 `formatted.kind = "data"`、`formatted.data`、`formatted.text`。
- `message`/`prompt`/`intent`：保留到 `formatted`，用于继续追问、下一页等上下文。

## 排除项处理

- 个性化推荐：当前 MVP 不创建登录态；只有外部显式传入 Authorization 时才透传使用，默认降级为热门/频道推荐。
- 会员状态：当前 MVP 不查询真实会员态。
- 登录/授权：当前 MVP 不创建、保存或刷新任何授权态。
- native/后端新增：当前 MVP 不新增协议字段或后端接口。

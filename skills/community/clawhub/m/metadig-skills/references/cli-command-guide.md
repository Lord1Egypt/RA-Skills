# metadig 命令完整参考

本文是 `metadig` 各命令、参数、环境变量、配置文件与 JSON 输出字段的权威说明。不确定某个 flag 时先看这里或 `metadig <命令> --help`，不要臆造参数。

## 全局

```bash
metadig -v | --version           # 版本号
metadig --api-base <url> <命令>  # 指定 API 基址（默认 https://waytometa.cn/api；本地调试 http://localhost:6603）
```

### 环境变量

| 变量 | 作用 |
| --- | --- |
| `METADIG_TOKEN` | 访问令牌。**优先级最高**，设了以后本地保存的凭证被忽略（Agent 无浏览器时的兜底） |
| `METADIG_API_BASE` | API 基址，优先级低于 `--api-base`、高于凭证里记录的基址 |
| `METADIG_HOME` | 配置目录，默认 `~/.metadig` |
| `NO_COLOR` | 设了则不输出 ANSI 颜色 |

### 配置文件

| 路径 | 内容 |
| --- | --- |
| `~/.metadig/credentials.json` | 登录凭证（权限 0600）：`accessToken` / `userName` / `apiBase` / `savedAt`。约 30 天有效 |
| `~/.metadig/config.json` | 全局配置：`defaultProjectId`（首次生成自动创建的「CLI 项目」） |
| `<目录>/.metadig/project.json` | `metadig project use` 写的目录级项目绑定 `{ "projectId": "..." }`；从当前目录向上查找，子目录里执行命令也命中 |

### 输出约定

- **stdout 只放结果**（URL、JSON、表格），**stderr 放过程提示**（已上传、已提交、进度、警告）。`--json` 时 stdout 是单个 JSON 文档，可直接 `| jq`。
- 非 TTY（Agent / 管道）下等待进度每 15 秒打印一行到 stderr，不刷屏。
- 退出码：成功 `0`；任何用户可预期错误（未登录、参数错误、任务失败等）`1`，错误正文一行 + 可选一行提示。

## 登录与账号

```bash
metadig login                    # 浏览器授权（device-code 式）：打印授权链接并尝试打开浏览器，每 2 秒轮询，链接 10 分钟内有效
metadig login --no-open          # 只打印链接不开浏览器（服务器 / 容器 / 远程会话）
metadig login --token <jwt>      # 用已有访问令牌登录（存本地并立刻验证；无效则清掉并报错）
metadig logout                   # 删除本地凭证（METADIG_TOKEN 环境变量不受影响，会提示）
metadig whoami                   # 账号 + 积分余额 + 当前 API 基址
```

- 登录时若检测到 `METADIG_TOKEN`，会警告它的优先级高于本次保存的凭证。
- CLI 令牌与网页登录并存，不占用户套餐的「同时在线设备数」。

## 模型目录

```bash
metadig models                       # 全部类型（image / video / tts / music），表格带积分、渠道、标签
metadig models --type video          # 只看一类：image | video | tts | music | all
metadig models <模型ID>              # 单模型详情：比例 / 分辨率 / 时长 / 渠道 / 参考上限 / 分档价
metadig models --json                # 全量 JSON
metadig models <模型ID> --json       # 单模型 JSON
```

标签含义：`会员` = 免费档不可用（需订阅）；`停用` = 维护中，提交会被拒绝；`新` = 新上架；`8折` 这类 = 价格活动进行中，表内已是折后价。目录顺序 = 平台推荐顺序，`gen` 未指定 `-m` 时取该类目录第一个未停用的模型。

### `models --json` 结构

```jsonc
{
  "image": [CatalogModel],          // 图片模型
  "video": [CatalogModel + { "modes": ["text-to-video", "first-to-video", ...] }],
  "tts":   [CatalogModel],
  "music": [CatalogModel],
  "pricing_promo": { "label": "...", "globalPercent": 80, "endAt": "..." } | null
}
```

`CatalogModel` 常用字段（缺省表示该模型不适用）：

| 字段 | 说明 |
| --- | --- |
| `modelId` / `modelName` / `providerId` | 模型 ID（`-m` 用）、显示名、提供方 |
| `credits` | 积分文案（区间或单价）；`originalCredits` 折前价、`discountPercent` 折扣百分比 |
| `creditsMap` | 分档价。图片键 `"1K"` / `"<渠道>:1K"`（每张价）；视频键 `"<渠道>:<时长>s:<分辨率>"` / `"<时长>s:<分辨率>"`（该时长的**总价**）；带声音价在 `creditsMapWithAudio` |
| `tags` | `plan-only`（会员专属）、`new`、`featured` 等 |
| `disabled` | `true` = 停用 |
| `channels` | 渠道列表（如 `priority` / `stable`），第一个是默认渠道 |
| `ratiosText` / `ratiosImage` | 文生图 / 图生图（或视频）比例档位；按渠道的版本 `ratiosTextByChannel` / `ratiosImageByChannel` / `ratiosByChannel` |
| `resolutions` / `resolutionsByChannel` | 分辨率档位（图片 `1K/2K/4K`，视频 `480p/720p/1080p`） |
| `durations` / `durationsByChannel` / `durationsByResolution` | 视频时长档位（秒） |
| `audio` | 视频模型是否支持 `--audio` |
| `maxReferenceImages` / `maxReferenceVideos` / `maxReferenceAudios` | 参考素材上限（另有 `*ByChannel` 版本） |
| `outputFormats` / `qualities` | 图片输出格式 / 质量档位 |
| `creditPer200Chars` | 语音：每 200 字积分 |
| `creditPer5Seconds` / `minDuration` / `maxDuration` / `instrumental` | 音乐：每 5 秒积分（无则按首计价）、时长范围、是否支持纯音乐 |

`models <模型ID> --json` 返回 `{ image, video: { "<run_type>": model | null }, tts, music }`，未命中的类别为 `null`。

## 生成

四个子命令共用的参数：

| 参数 | 说明 |
| --- | --- |
| `-m, --model <模型ID>` | 不传用该类目录第一个可用模型 |
| `-p, --project <项目ID>` | 归属项目；不传按「`--project` > 目录绑定 > 全局默认 > 自动创建『CLI 项目』」解析 |
| `--no-wait` | 提交后立即返回（stdout 打任务 ID 或 JSON），之后用 `status` 查 |
| `--no-canvas` | 不在画布创建节点，产物只进项目「历史文件」 |
| `-o, --out <目录>` | 完成后把产物下载到目录（不存在会创建） |
| `--json` | JSON 输出 |

素材参数（`-r` / `--first` / `--last` / `--ref-video` / `--ref-audio`）接受本地路径或 `http(s)://` URL；本地文件自动上传（<5MB 走服务器中转，视频或 ≥5MB 走对象存储直传，失败自动回退），stderr 打印 `已上传 <文件> → <URL>`。

### `gen image <提示词>`

```bash
metadig gen image "<提示词>" [-m <模型ID>] [-r <参考图>]... [--ratio 16:9] [--resolution 2K] [-n 2]
                             [--channel priority] [--quality <档>] [--format png] [-p] [--no-wait] [--no-canvas] [-o <目录>] [--json]
```

- 有 `-r` 自动走图生图（run_type `image-to-image`），否则文生图（`text-to-image`）。
- 默认值按模型目录取：比例 `1:1`（图生图优先 `auto`）、分辨率 `1K`、格式 `png`、张数 1。
- 参考图张数超过 `maxReferenceImages` 只警告，以服务端校验为准。
- 部分模型固定单张出图，`-n` 大于 1 时以实际返回为准。

### `gen video <提示词>`

```bash
metadig gen video "<提示词>" [-m <模型ID>] [--first <图>] [--last <图>] [-r <图>]... [--ref-video <视频>]... [--ref-audio <音频>]...
                             [--ratio 16:9] [--resolution 720p] [-d 5] [--audio] [--channel <渠道>] [-p] [--no-wait] [--no-canvas] [-o <目录>] [--json]
```

生成方式由素材决定：

| 素材 | 方式（run_type） |
| --- | --- |
| 无 | 文生视频 `text-to-video` |
| `--first` | 首帧生视频 `first-to-video` |
| `--first` + `--last` | 首尾帧生视频 `first-last-to-video` |
| `-r` / `--ref-video` / `--ref-audio` 任一 | 参考生视频 `reference-to-video` |

约束：`--last` 必须与 `--first` 同用；`--first` 与 `--ref` 系列不能混用（直接报错）。模型必须支持所选方式，否则报「模型 X 不支持<方式>」并列出可用模型。默认 `16:9` / `720p` / `5` 秒，时长档位按分辨率与渠道取。`--audio` 让支持的模型带环境音 / 对白，价格按 `creditsMapWithAudio`。

### `gen speech <文本>`

```bash
metadig gen speech "<文本>" [-m <模型ID>] [--voice <音色ID>] [-p] [--no-wait] [--no-canvas] [-o <目录>] [--json]
```

默认音色 `male-qn-qingse`，音色清单见 `generation-guide.md`。按 200 字计价。

### `gen music <风格描述>`

```bash
metadig gen music "<风格描述>" [-m <模型ID>] [--lyrics "<歌词>"] [--instrumental] [-d 40] [-p] [--no-wait] [--no-canvas] [-o <目录>] [--json]
```

`--instrumental` 时忽略 `--lyrics`。支持自定义时长的模型（按 5 秒计价）默认 40 秒，`-d` 超出范围自动钳进 `minDuration~maxDuration` 并警告；按首计价的模型不支持 `-d`（忽略并提示）。

### `gen` 的 JSON 输出

`--no-wait --json`：

```json
{ "taskId": "…", "state": "PENDING", "nodeId": "…" }
```

等待完成 `--json`：

```json
{
  "taskId": "…",
  "state": "SUCCESS",
  "urls": ["https://…/xxx.png"],
  "files": ["./exports/1a2b3c4d-1-xxx.png"],
  "nodeId": "…",
  "text": "…"
}
```

`nodeId` 只在建了画布节点时出现（未加 `--no-canvas`）；`files` 只在 `-o` 时非空；`text` 仅少数文本类结果才有。任务失败时不输出 JSON，而是以退出码 1 + stderr 错误文案结束（文案即服务端清洗后的用户提示）。

## 任务

```bash
metadig status <任务ID> [--wait] [-o <目录>] [--json]   # 查状态；--wait 等到终态；SUCCESS 且 -o 时下载
metadig download <任务ID> [-o <目录>]                    # 下载已完成任务产物（默认当前目录）
metadig history [--limit 20] [--json]                    # 近 7 天任务，最多 50 条
```

### 任务状态

| `state` | 含义 |
| --- | --- |
| `PENDING` | 排队中 |
| `PROGRESS` | 生成中 |
| `SUCCESS` | 完成（`urls` 有产物） |
| `FAILURE` | 失败（`detail` 是原因；不扣积分） |
| `REVOKED` | 已取消（不扣积分） |
| `EXPIRED` | 已超时（不扣积分） |

等待策略：按服务端下发的 `poll_interval`（默认 3 秒）轮询，网络抖动不中断，硬上限 2 小时（到点报「等待超时」，任务本身不受影响）。提交时服务端会给 `estimated_duration`（按近 7 天同模型真实耗时估算），等待进度里会显示。

### `status --json`

```json
{
  "taskId": "…",
  "state": "SUCCESS",
  "detail": "…",
  "urls": ["…"],
  "files": ["…"],
  "text": "…",
  "estimatedDuration": 120
}
```

`detail` / `text` / `estimatedDuration` 缺省时不出现。

### `history --json`

```json
{
  "items": [
    {
      "task_id": "…", "run_type": "text-to-image", "model": "…",
      "project_id": "…", "project_title": "CLI 项目",
      "status": "SUCCESS", "error_message": "", "credit": 4,
      "created_at": "2026-09-03 10:00:00", "duration_seconds": 38
    }
  ],
  "count": 1
}
```

`history` 不带产物链接，取链接用 `status <任务ID>`。

### 下载文件名

`<任务ID前 8 位>-<序号>-<源文件名>`，如 `1a2b3c4d-1-output.png`；同一任务多张图序号递增。下载单个文件超时 10 分钟。

## 项目

```bash
metadig project list [--limit 20] [--json]   # 我的项目（按最近修改倒序）
metadig project create ["<标题>"]            # 新建项目（标题可选），输出项目 ID
metadig project use <项目ID>                 # 绑定到当前目录（写 .metadig/project.json）
metadig project current                      # 当前生效的项目 ID 及来源
```

`project list --json` → `{ "projects": [{ "projectId", "title", "lastModifiedDate", … }], "total": n }`。

## 上传

```bash
metadig upload <文件>... [-p <项目ID>] [--json]
```

返回公网 URL；`--json` → `{ "projectId": "…", "files": [{ "file": "./a.png", "url": "https://…" }] }`。支持图片（jpg/png/gif/webp/bmp）、视频（mp4/mov/webm/m4v 等）、音频（mp3/wav/m4a/aac/ogg/flac）。大小上限与网页端一致（按文件类型与用户套餐，视频最大 100MB）。生成命令的素材参数已自动上传，一般不需要单独调用。

## 超时一览

| 操作 | 超时 |
| --- | --- |
| 普通请求 | 60 秒 |
| 提交生成（`POST /run`） | 15 分钟（同步出图链路服务端可能阻塞较久） |
| 上传中转 | 5 分钟；直传 10 分钟 |
| 等待任务 | 2 小时硬上限 |
| 下载单个产物 | 10 分钟 |

提交超时是「结果不确定」而不是失败：任务可能已受理并预扣积分，CLI 会给出 `metadig status <任务ID>` 提示。

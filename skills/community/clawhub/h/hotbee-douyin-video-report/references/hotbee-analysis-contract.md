# HotBee 视频解析契约

## 核心接口

Base URL：`https://www.smsz.xyz/prod-api`

| 用途 | Endpoint | 参数 | 备注 |
| --- | --- | --- | --- |
| 抖音视频基础信息 | `/tool/douyin/Dy_video_info` | `url` | 基础兜底 |
| 抖音视频 VIP 信息 | `/tool/douyin/Dy_video_info_VIP` | `url`, `key` | 优先使用 |
| 抖音全部评论 | `/tool/douyin/Dy_video_all_comments_VIP` | `video_url`, `page`, `key` | 当前 Skill 默认评论采集路径 |
| 音视频转文案 | `/tool/speech/speechToText` | `file_url`, `key` | `file_url` 可以是标准视频页、分享链接或下载链接 |
| 短链解析兜底 | `/tool/douyin/Dy_convert_share_url` | `url` | 用于分享短链转换 |

接口使用 `POST`，参数放 query string，body 为空 JSON 或空请求体均可。

## 网络与凭证安全

- 密钥优先从本机 `HOTBEE_API_KEY` 环境变量读取，并兼容旧变量 `HOTBEE_DOUYIN_KEY`。
- 含密钥的请求异常必须先清理再写入警告或原始错误 JSON。
- 原始响应落盘前必须递归清理 `key`、`token`、`secret`、`password` 和授权字段。
- 自定义 Base URL 必须使用 HTTPS；只有 `localhost` 或回环 IP 可以使用 HTTP。
- 短链先在本机直接跟随抖音 HTTPS 跳转，再使用 HotBee 接口兜底；不要把用户链接发送给额外的第三方解链服务。
- 媒体下载只接受没有内嵌账号密码的公网 HTTPS URL，单个文件上限 25 MB。

## 标准化字段

视频信息需要归一为：

- 标题、作者昵称、作者 ID、发布时间、时长、视频 ID。
- 封面 URL、视频下载 URL、音乐标题、音乐 URL。
- 播放、点赞、评论、分享、收藏。
- 原始标题/描述、图集 URL。
- 播放量读取必须兼容 `statistics.play_count`、`play_count`、`playCount`、`play`、`view_count`、`viewCount`。

评论需要归一为：

- 评论 ID、昵称、评论内容、时间、地区、点赞数、意图。
- 意图规则保持中文：`求入口`、`资料需求`、`操作追问`、`价格付费`、`真实性质疑`、`认可收藏`、`人群场景`、`分享传播`、`其他评论`。

## 报告结构

HTML 报告至少包含：

- 视频概览和封面。
- 核心指标：播放、点赞、评论、分享、收藏，以及点赞率、收藏/点赞、分享/评论、评论密度。
- 开场钩子、主题判断、爆款要素。
- 画面拆解时间线。
- 脚本拆解结构。
- 评论意图与热词。
- 相关评论样本。
- 完整视频文案。
- 优化建议。

## HTML 视觉与交互基线

- 背景使用米色报告底，整体接近 HotBee 网站导出的“视频解析报告.png”。
- 首屏为封面图 + 标题摘要卡，指标区为 `4 + 4` 卡片。
- 画面拆解为时间、文案、情绪/风险进度条三列结构。
- 评论意图与热词区左侧展示热词词云、意图统计和需求词，右侧展示相关评论。
- 热词词云、高频需求词和高频意图统计都必须是可点击筛选控件。
- 点击词云或需求词时，右侧评论按评论内容或作者匹配该词；点击意图统计时，右侧评论按意图精确匹配。
- “全部评论”控件必须恢复完整已采集评论列表。
- 交互必须由 HTML 内嵌评论 JSON 和本地脚本完成，保证用户直接用 `file://` 打开报告也能使用。

## 生图规则

本 Skill 默认只保存解析得到的图片和报告卡片 SVG。若用户明确要求 AI 生成额外配图，只能使用 HotBee Image2，并且必须保存：

- 中文 Prompt。
- 请求/任务 JSON。
- 生成图片文件。

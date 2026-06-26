---
name: libtv-skill-pro
description: 通过 LibTV (liblib.tv) AI 视频平台生成和编辑图片/视频的完整工具集。覆盖文生图/视频、图生图/视频、视频续写、风格迁移、局部编辑（把纸船换成爱心）、短剧/MV/TVC 制作、角色三视图、分镜设计、首尾帧视频、音频生视频。支持 Seedance 2.0 / Kling 3.0/O3 / Wan 2.6 / Nano Banana / Midjourney / Seedream 5.0 / Lib Nano Pro / GVLM 3.1 等模型，可显式指定模型+参数（比例/分辨率/时长）。Pro 版扩展批量并发、轮询监控、工作流模板、结果导出、会话历史、项目管理、统一入口、dry-run 预览、结构化错误。触发词：画一个/生成/做一个/帮我做、liblib/libtv/aigc、视频/图片/MV/TVC/短剧/分镜/动漫/海报、AI 视频/图片生成、画/生成一张/一段。
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires":
          {
            "bins": ["python3"],
            "env": ["LIBTV_ACCESS_KEY"]
          },
        "primaryEnv": "LIBTV_ACCESS_KEY"
      }
  }
---

# libtv-skill-pro

> Fork of [@haofanwang/libtv-skill](https://clawhub.ai/haofanwang/libtv-skill) — 在原版基础上扩展高级工作流与功能矩阵层。Source / Issues: https://github.com/Qiuxiangxiang/libtv-skill-pro

LibTV (liblib.tv) 是 LiblibAI 推出的 AI 视频创作平台。本 skill 让 Agent 通过统一入口 `libtv.py` 完成生成 / 编辑 / 修饰 / 模型路由的全链路。

## 快速开始（3 分钟跑通第一个 case）

```bash
# 1. 拿 access key：https://www.liblib.tv → 用户中心 → API / 开发者
export LIBTV_ACCESS_KEY=your_key_here

# 2. 看完整命令清单
python3 {baseDir}/scripts/libtv.py --help

# 3. 跑第一个 case（dry-run 预览，不烧积分）
python3 {baseDir}/scripts/libtv.py model with lib-nano-pro \
  "白色短毛猫坐在窗台上" --ratio 1:1 --resolution 2K --dry-run

# 4. 去掉 --dry-run 真实生成（≈14 积分，≈60s）
python3 {baseDir}/scripts/libtv.py model with lib-nano-pro \
  "白色短毛猫坐在窗台上" --ratio 1:1 --resolution 2K
# → 返回 sessionId，再用 poll 等结果，download 取本地

python3 {baseDir}/scripts/libtv.py poll <SESSION_ID>
python3 {baseDir}/scripts/libtv.py download <SESSION_ID> --output-dir ~/Downloads/cat
```

5 个完整 case 见 `examples/`（图像 / 视频 / 编辑 / 多步链 / 批量）。

## 推荐入口：`libtv.py <subcommand>`

所有功能聚合在一个入口，Agent 路由更顺：

```
python3 libtv.py flow       <preset> "<topic>" [--ref URL]
python3 libtv.py node       <action> "<topic>" [--ref URL]
python3 libtv.py edit       <modifier> "<desc>" [--target URL] [--session-id SID]
python3 libtv.py model      list|with <model> "<prompt>" [params]

python3 libtv.py session    "<message>"               # 创建会话/发消息（底层）
python3 libtv.py query      <SID>                     # 查询会话进展
python3 libtv.py upload     <local_file>              # 上传到 OSS
python3 libtv.py download   <SID> [--output-dir DIR]  # 下载结果

python3 libtv.py batch      --file tasks.txt --workers 5
python3 libtv.py monitor    <SID> --poll --extract-urls
python3 libtv.py poll       <SID>
python3 libtv.py template   <name> "<topic>"
python3 libtv.py export     <SID> --format html
python3 libtv.py history    list|add|show|get|remove
python3 libtv.py project    list|current|switch|use|remove|describe
```

> 旧路径 `python3 scripts/<name>.py ...` 仍可用（向后兼容）。新代码统一用 `libtv.py`。

## 决策树（路由判断）

收到用户需求时，按以下顺序匹配：

| 用户输入 | 走哪条路径 |
|---|---|
| 用户提供了本地文件（图/视频/音频路径）| 先 `upload` 拿 OSS URL，再发到下一步 |
| 模糊一句话「画只猫 / 做个 MV」 | `session` 让后端 Agent 路由（最省心）|
| 明确想要 LibTV 某个入口（"做个角色三视图"）| `flow <preset>` |
| 明确想用某个模型（"用 Seedance 出视频"）| `model with <model>` |
| 想在已生成内容上改风格 / 加运镜 | `edit <modifier> --session-id SID` |
| 一次发 10+ 任务 | `batch --file tasks.txt --workers 5` |
| 完整短剧 / MV / 角色设计预设 | `template <name>` |
| 等结果 / 查进度 | `poll`（简单等）或 `monitor`（看过程）|
| 取结果 | `download <SID>` |

**永远先 `--dry-run` 预览**：每个生成类子命令（flow/node/edit/model）都支持 `--dry-run`，会输出 JSON 显示 will-send prompt 而不调 API。

## 已知模型（用 `libtv.py model list` 查最新）

| 类型 | 模型 | 适用 |
|---|---|---|
| LLM | gvlm-3.1 | 剧本/广告词/品牌文案/提示词改写 |
| 图像 | lib-nano-pro | 快速生图、图生图、高清化 |
| 图像 | nano-banana | 平面海报/插画（Google Gemini 系） |
| 图像 | midjourney | 美学风/插画/海报 |
| 图像 | seedream-5.0 | 写实/电影感（豆包系） |
| 视频 | seedance-2.0-vip | 文生/图生视频、短片（默认） |
| 视频 | kling-3.0 | 写实人像、动作连贯 |
| 视频 | kling-o3 | 高质量长视频 |
| 视频 | wan-2.6 | 多镜头长视频（通义万相） |

模型参数：`--ratio 16:9` `--resolution 720P|2K` `--duration 5s` `--count "1张"`

## 错误响应（v0.4.0+ 结构化）

所有 API 错误以 JSON 写到 stderr，便于 Agent 程序化处理：

```json
{
  "error": {
    "kind": "INVALID_ACCESS_KEY",
    "http_code": 401,
    "message": "accessKey 不存在或无效",
    "raw": "{...}"
  }
}
```

错误 kind 清单：`INVALID_ACCESS_KEY` / `FORBIDDEN_OR_INSUFFICIENT_CREDITS` / `NOT_FOUND` / `TIMEOUT` / `RATE_LIMITED` / `SERVER_ERROR` / `BAD_GATEWAY` / `SERVICE_UNAVAILABLE` / `GATEWAY_TIMEOUT` / `NETWORK_ERROR` / `INTERRUPTED` / `UNKNOWN`。

## 16 类能力详解

详细说明继续保留以便深度使用，但**优先看 `examples/` 和决策树**。

### 1. 创建会话 / 发送消息 — `libtv.py session`

```bash
# 自然语言发消息（后端 Agent 自己路由模型）
python3 libtv.py session "生一个动漫视频"

# 续聊已有会话
python3 libtv.py session "再来一张风景图" --session-id SID
```

### 2. 查询会话进展 — `libtv.py query`

```bash
python3 libtv.py query SID --after-seq 5       # 增量拉取
python3 libtv.py query SID --project-id PUUID  # 附带项目地址
```

### 3. 上传文件 — `libtv.py upload`

支持图片 / 视频，≤ 200MB。返回 OSS URL。

```bash
python3 libtv.py upload /path/to/image.png
python3 libtv.py upload /path/to/video.mp4
```

### 4. 下载结果 — `libtv.py download`

```bash
python3 libtv.py download SID --output-dir ~/Downloads/proj --prefix scene
python3 libtv.py download --urls URL1 URL2 --output-dir ./out   # 直接给 URL 列表
```

### 5. 批量任务 — `libtv.py batch`

```bash
python3 libtv.py batch --file tasks.txt --workers 5 --output result.json
python3 libtv.py batch -m "猫" -m "狗" -m "鸟"
```

### 6. 实时监控 — `libtv.py monitor`

```bash
python3 libtv.py monitor SID --poll --interval 15 --extract-urls
python3 libtv.py monitor SID --poll --format json --output log.json
```

### 7. 简化轮询 — `libtv.py poll`

```bash
python3 libtv.py poll SID                            # 默认 8s 间隔，10 分钟超时
python3 libtv.py poll SID --interval 5 --timeout 300
python3 libtv.py poll SID --quiet                    # 只输出最终结果
```

### 8. 工作流模板 — `libtv.py template`

```bash
python3 libtv.py template --list
python3 libtv.py template storyboard "科幻城市的故事"
python3 libtv.py template short_drama "友情故事"
python3 libtv.py template music_video "悲伤钢琴曲"
```

8 个模板：storyboard / character_design / video_generation / image_generation / style_transfer / short_drama / music_video / product_showcase

### 9. 结果导出 — `libtv.py export`

```bash
python3 libtv.py export SID --format html --output report.html
python3 libtv.py export SID --format markdown --output report.md
python3 libtv.py export SID --urls-only
```

### 10. 会话历史 — `libtv.py history`

```bash
python3 libtv.py history list
python3 libtv.py history add SID --desc "项目描述"
python3 libtv.py history get 1     # 拿到 sessionId（脚本用）
python3 libtv.py history remove 1
```

### 11. 项目管理 — `libtv.py project`

```bash
python3 libtv.py project list                # 列本地记录
python3 libtv.py project current             # 当前项目
python3 libtv.py project switch --desc "短剧 A"   # 创建新项目
python3 libtv.py project use PUUID           # 切到指定项目
python3 libtv.py project describe PUUID "MV"
python3 libtv.py project remove PUUID
```

本地状态：`~/.libtv_projects.json`。

### 12. 预设流程 — `libtv.py flow`

```bash
python3 libtv.py flow story_script "机器人来到唐朝"
python3 libtv.py flow character_views "穿汉服的赛博朋克少女"
python3 libtv.py flow keyframe_to_video "拔剑出鞘" --ref OSS_URL
python3 libtv.py flow audio_to_video "暗黑风 MV" --ref OSS_URL
```

### 13. 节点能力 — `libtv.py node`

```bash
# 文本节点
python3 libtv.py node text_to_video_prompt "一只猫在屋顶看月亮"
python3 libtv.py node image_caption --ref IMG_URL
python3 libtv.py node text_to_music "悲伤、钢琴、60秒"

# 图片节点
python3 libtv.py node image_to_image "改赛博朋克风" --ref IMG_URL
python3 libtv.py node image_upscale --ref IMG_URL

# 视频节点
python3 libtv.py node first_last_frame "拔剑过程" --ref start.png --ref2 end.png
python3 libtv.py node reference_video "保留主体演绎新场景" --ref ref.png
```

### 14. 修饰器 — `libtv.py edit`

```bash
python3 libtv.py edit style "宫崎骏吉卜力" --target URL --session-id SID
python3 libtv.py edit camera "无人机环绕" --target "场景" --session-id SID
python3 libtv.py edit character_lib "孙悟空" --target "花果山" --session-id SID
python3 libtv.py edit mark "纸船换爱心" --target URL --session-id SID
python3 libtv.py edit focus "右上角月亮" --target URL --session-id SID
```

### 15. 模型路由 — `libtv.py model`

```bash
python3 libtv.py model list
python3 libtv.py model list --kind video
python3 libtv.py model with seedance-2.0-vip "..." --ratio 16:9 --duration 5s
python3 libtv.py model with lib-nano-pro "..." --ratio 1:1 --resolution 2K
```

### 16. dry-run（v0.4.0+）

所有生成类子命令（flow/node/edit/model）支持 `--dry-run`：输出将发送的 prompt 但**不调 API、不烧积分**。

```bash
python3 libtv.py flow story_script "..." --dry-run
python3 libtv.py model with seedance-2.0-vip "..." --duration 5s --dry-run
```

## 用户侧 Agent 的核心原则

你（用户侧 Agent）是**搬运工**，不是创作者。后端 LibTV Agent 有专业的模型选择 / prompt 工程 / 工作流编排能力。

- **能传话就别替用户写 prompt**：用户说"帮我推演分镜"，就调 `session "帮我推演分镜"`，不要自己先编个分镜表
- **能用 `flow`/`model` 显式入口就别让后端猜**：用户说"用 Seedance 做 5 秒视频"时，直接 `model with seedance-2.0-vip --duration 5s`
- **永远先 `--dry-run` 检查 prompt**：调真 API 前一次 dry-run 能省很多冤枉积分
- **下载到本地后向用户展示**：results URL + projectUrl 两个都给

## 输出格式（v0.4.0+ 全 JSON）

所有 stdout 输出都是 JSON，便于 Agent 程序化解析：

```json
// session / flow / node / edit / model 等生成类
{"projectUuid":"...", "sessionId":"...", "projectUrl":"...", "message_sent":"..."}

// dry-run
{"dry_run":true, "preset":"...", "would_send":"...", ...}

// list 类（model list / project list / history list 等仍输出表格，便于人类查看）
```

错误以 JSON 写 stderr（见上面"错误响应"）。

## 注意事项

- 鉴权方式：`Authorization: Bearer <LIBTV_ACCESS_KEY>`
- 项目画布地址：`https://www.liblib.tv/canvas?projectId=<projectUuid>`
- 上传 OSS 地址格式：`https://libtv-res.liblib.art/claw/{projectUuid}/{uuid}{ext}`
- 文件大小限制：200MB
- 生成中只给用户"正在生成"提示；完成后同时给 **结果 URL + projectUrl**
- 本地状态：`~/.libtv_projects.json`（项目）+ `~/.libtv_session_history.json`（会话历史）

# Upload 模块测试方案

## 1. 模块划分与职责

本套件覆盖上传与媒体处理相关能力：

- **uploadMediaToDingTalk(filePath, mediaType, accessToken, maxSize, log?)**：根据文件类型与大小上传到钉钉，成功返回 `media_id`，失败/异常返回 null。
- **downloadImageToFile(url, filePath?, log)**：下载图片落盘（部分调用者会传入显式 filePath）。
- **downloadMediaByCode(mediaId / downloadCode, accessToken / config, log)**：通过 code 获取下载信息并下载。
- **downloadFileByCode(downloadCode, targetPath, log)**：下载文件落盘。
- **extractVideoMetadata(videoPath, log)**：提取视频元信息（容错，失败也应返回默认结构）。
- **extractVideoThumbnail(videoPath, thumbPath, log)**：提取视频缩略图（容错）。
- **processLocalImages(content, oapiToken, log)**：将 markdown 中本地图片路径上传并替换为可访问 URL/标记（按实现）。
- **processVideoMarkers / processFileMarkers / processAudioMarkers**：处理并移除钉钉媒体标记并执行上传/发送：
  - `[DINGTALK_VIDEO]{"path":"<本地视频路径>"}[/DINGTALK_VIDEO]`
  - `[DINGTALK_FILE]{"path":"<本地文件路径>","fileName":"<文件名>","fileType":"<扩展名>"}[/DINGTALK_FILE]`
  - `[DINGTALK_AUDIO]{"path":"<本地音频路径>"}[/DINGTALK_AUDIO]`

> 测试通过 `plugin.__testables` 暴露的上述函数进行调用与断言。

## 2. 已覆盖用例（与 `upload.test.ts` 对齐）

> 说明：本章节仅列出**已在测试中覆盖**的用例，确保文档与现状 100% 一致。

### 2.1 uploadMediaToDingTalk

| 序号 | 场景 | mock 返回 | 期望 | 说明 |
|------|------|-----------|------|------|
| 1 | 上传成功 | `errcode=0, media_id=media123` | 返回 `'media123'` | 主路径 |
| 2 | 上传失败 | `errcode!=0` | 返回 null | 业务失败 |
| 3 | 网络异常 | axios.post 抛错 | 返回 null | 错误收敛 |
| 4 | 多媒体类型 | image/file/video/voice | 不抛错且 post 被调用 | 类型分支覆盖 |

### 2.2 downloadImageToFile / downloadMediaByCode / downloadFileByCode

| 序号 | 场景 | mock | 期望 |
|------|------|------|------|
| 5 | downloadImageToFile 成功 | axios.get 返回 Buffer | 返回非空路径 |
| 6 | downloadImageToFile 失败 | axios.get 抛错 | 返回 null |
| 7 | downloadMediaByCode 成功 | axios.get/post 返回可用结构 | 返回非空结果 |
| 8 | downloadMediaByCode API 错误 | errcode!=0 | 返回 null |
| 9 | downloadFileByCode 成功 | axios.get 返回 Buffer | 返回非空结果 |
| 10 | downloadFileByCode 失败 | axios.get 抛错 | 返回 null |

### 2.3 extractVideoMetadata / extractVideoThumbnail

| 序号 | 场景 | 输入 | 期望 | 说明 |
|------|------|------|------|------|
| 11 | 元信息提取（容错） | 任意路径 | 返回对象（不为 undefined） | 无 ffmpeg 也不应崩溃 |
| 12 | 元信息失败回退 | 不存在路径 | 返回对象 | 默认值 |
| 13 | 缩略图提取（容错） | 任意路径 | 返回 string 或 null | 不要求真实生成；失败不应抛异常 |

### 2.4 processLocalImages

| 序号 | 场景 | 输入 | 期望 | 说明 |
|------|------|------|------|------|
| 14 | 本地图片存在 | `![image](/tmp/image.png)` + existsSync=true | 返回处理后的字符串 | 上传替换 |
| 15 | 本地图片缺失 | existsSync=false | 返回处理后的字符串 | 不应抛错 |

### 2.5 process*Markers

| 序号 | 场景 | 输入 | 期望 |
|------|------|------|------|
| 16 | video marker（文件不存在） | `hello [DINGTALK_VIDEO]{"path":"/tmp/video.mp4"}[/DINGTALK_VIDEO] world` | 标记被移除；返回内容包含原文本并给出告警/提示 |
| 17 | file marker（存在文件） | `[DINGTALK_FILE]{"path":"/tmp/file.pdf","fileName":"file.pdf","fileType":"pdf"}[/DINGTALK_FILE]` | 标记被移除；触发 `media/upload&type=file` 并发送文件消息 |
| 18 | audio marker（存在文件） | `[DINGTALK_AUDIO]{"path":"/tmp/audio.mp3"}[/DINGTALK_AUDIO]` | 标记被移除；触发 `media/upload&type=voice` 并发送语音消息 |

## 3. 预期正确输出与潜在错误

- **正确**：上传失败/异常均返回 null 并记录日志；多媒体类型分支覆盖；视频相关函数在缺少外部依赖时仍可运行（返回默认结果）；marker 处理对不存在文件有明确提示或安全回退。
- **潜在错误原因**：错误地把 errcode 判定当成功；maxSize 单位或比较错误；未处理 fs/stat 异常；视频工具链缺失导致抛异常；marker JSON/格式解析不一致导致误替换。


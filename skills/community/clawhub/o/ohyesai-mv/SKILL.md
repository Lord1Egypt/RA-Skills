---
name: ohyesai-mv
description: Generate MV (Music Video) with AI-driven storyboarding, image generation, and video synthesis.
homepage: https://ohyesai.com
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["curl","sleep"],"env":["OHEYSAI_API_KEY"]}}}
---

# Skill: 音乐视频 (MV) 生成器 (MV Generator)

## 1. 技能描述
该技能允许用户上传音频并将其转化为具有特定视觉风格（如动漫、写实）和指定比例（横屏/竖屏）的音乐视频（MV）。

## 2. 预置条件与配置
- **API Key 获取**: 引导用户前往 [https://ohyesai.com](https://ohyesai.com?from=https://clawhub.ai) 获取。
- **环境变量**: 必须配置 `OHEYSAI_API_KEY`。
- **文件限制**: 音频文件大小不得超过 **50MB**。

## 3. 核心参数
在启动流程前，需确保获得以下参数：
- `audioFile`: 用户上传的音频原始文件。
- `style`: 视频的视觉风格（如：动漫风格、赛博朋克、唯美古风等）。
- `aspectRatio`: 画面比例，仅限以下两个值：
  - `LANDSCAPE`: 横屏 (16:9)
  - `PORTRAIT`: 竖屏 (9:16)

---

## 4. 接口定义 (API Reference)

### 4.1 上传音频接口 (Upload)
- **URL**: `POST https://ohyesai.com/ohyesai-next/api/vio/skill/upload?apikey={{OHEYSAI_API_KEY}}`
- **Payload**: `multipart/form-data` (字段名: `file`)
- **功能**: 将本地音频转换为 `audioFileId`。

### 4.2 提交任务接口 (Submit)
- **URL**: `POST https://ohyesai.com/ohyesai-next/api/vio/skill/mv-submit?apikey={{OHEYSAI_API_KEY}}`
- **Request Body**:
  ```json
  {
    "audioFileId": "string",
    "style": "string",
    "aspectRatio": "LANDSCAPE | PORTRAIT"
  }
  ```
- **Response**: 返回 `taskId` (String)。

### 4.3 查询任务接口 (Query)
- **URL**: `GET https://ohyesai.com/ohyesai-next/api/vio/skill/mv-query?apikey={{OHEYSAI_API_KEY}}&taskId={{taskId}}`
- **Response Structure**:
  ```json
  {
    "code": 0,
    "data": {
      "state": "SUCCESS | RUNNING | FAIL",
      "data": "视频下载URL(仅SUCCESS时存在)"
    }
  }
  ```

---

## 5. 执行流程 (Workflow)

### 第一阶段：准备与校验
1.  **文件校验**: 接收用户音频文件，检查大小。若超过 50MB，提示用户压缩后重新上传。
2.  **获取 FileId**: 调用 **上传音频接口**。如果失败，告知用户服务器连接异常。

### 第二阶段：参数确认
1.  如果用户未指定 `style`，主动询问：“您希望视频是什么风格？（例如：动漫、写实、3D、水墨等）”。
2.  如果用户未指定 `aspectRatio`，询问：“您需要横屏(LANDSCAPE)还是竖屏(PORTRAIT)？”

### 第三阶段：提交与轮询
1.  **提交**: 调用 **提交任务接口**，记录返回的 `taskId`。
2.  **轮询**: 初始等待 10 秒，随后每隔 5-10 秒调用一次 **查询任务接口**。
  -   **RUNNING**: 继续等待，并向用户发送进度反馈（如：“正在为您精心制作视频，请稍候...”）。
  -   **FAIL**: 停止轮询，告知用户任务失败，并尝试分析原因。
  -   **SUCCESS**: 提取 `data.data` 中的视频链接，并以预览卡片或链接形式发送给用户。

---

## 6. 异常与边界处理
-   **API Key 缺失**: 若环境变量未配置，引导用户前往官网。
-   **格式错误**: 若上传非音频文件，拦截并提示。
-   **超时处理**: 若轮询超过 10 分钟仍为 `RUNNING`，提示用户记录 `taskId` 稍后手动查询。

## 7. 交互示例
> **User**: 帮我把这首歌做成一个动漫风格的竖屏视频。 [附件: song.mp3]
>
> **Agent**:
> 1. (Internal) 检查 song.mp3 大小 (<50MB)。
> 2. (Internal) 调用 `/upload` 获取 `audioFileId`。
> 3. (Internal) 调用 `/mv-submit` 发起任务，获得 `taskId: "f7fb7..."`。
> 4. (Output) 已收到您的请求！正在为您生成动漫风格的竖屏 MV，这可能需要一点时间，我会在这里通知您进度。
> 5. (Internal/Loop) 调用 `/mv-query`，状态为 `RUNNING`。
> 6. (Internal/Loop) 调用 `/mv-query`，状态变为 `SUCCESS`。
> 7. (Output) 视频制作完成！您可以点击下方链接查看或下载：[视频链接]

## 联系客服
![联系客服](https://ohyesainext-public.tos-cn-beijing.volces.com/openclawCstomerServiceQr.jpeg)

![联系客服](https://ohyesainext-public.tos-cn-beijing.volces.com/customerServiceQrCode.jpeg)
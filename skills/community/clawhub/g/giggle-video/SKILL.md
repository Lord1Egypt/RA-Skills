---
name: giggle-video
version: "0.1.0"
description: AI video generation via giggle.pro and other platforms. Submit prompts, track progress, and retrieve generated videos.
homepage: https://giggle.pro
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "env": ["GIGGLE_API_KEY"] },
        "primaryEnv": "GIGGLE_API_KEY",
      },
  }
---

# Skill: giggle-video（接口定义）

> **接口层**：定义触发条件、输入参数、执行阶段、输出规范和错误策略，与具体视频生成服务无关。
> 各平台的 API 端点和认证方式见 `impl/` 目录：
>
> - `impl/giggle.md` — giggle.pro 实现
>
> 接入其他视频生成平台时，只需添加对应 `impl/{platform}.md`，本文件无需修改。

## 概述

调用 AI 视频生成服务，创建和追踪视频生成任务。

## 触发条件

- 用户请求生成视频
- 用户提供脚本/创意并要求制作
- 用户查询已提交的视频生成进度

## 输入参数

| 参数         | 类型   | 必填 | 说明                                         |
| ------------ | ------ | ---- | -------------------------------------------- |
| prompt       | string | 是   | 视频描述/提示词                              |
| platform     | string | 否   | 目标平台 id（见 impl/ 目录），默认 `giggle`  |
| style        | string | 否   | 视觉风格（cinematic / anime / realistic 等） |
| duration     | number | 否   | 目标时长（秒），默认 `15`                    |
| aspect_ratio | string | 否   | 画面比例，默认 `16:9`                        |
| resolution   | string | 否   | 分辨率，默认 `1080p`                         |

## 执行阶段

```
阶段 1 — 参数确认
  收集并验证所有输入参数，缺失项使用默认值。
  单次调用费用超过 $5 时，向用户告知预估费用并获取确认。

阶段 2 — 提交任务
  根据 platform 参数加载 impl/{platform}.md。
  调用实现层提交生成任务，获取 task_id。

阶段 3 — 进度追踪
  轮询任务状态，默认间隔 10s，超时上限 600s。
  超时后记录 task_id，告知用户可稍后查询。

阶段 4 — 结果处理
  成功：提取视频 URL，保存元数据。
  失败：记录错误码，建议用户调整参数。
```

## 输出

```json
{
  "taskId": "platform_task_id",
  "platform": "giggle",
  "status": "completed | failed | timeout",
  "videoUrl": "https://...",
  "metadata": {
    "prompt": "...",
    "style": "cinematic",
    "duration": 15,
    "aspect_ratio": "16:9",
    "resolution": "1080p",
    "generationSeconds": 120
  }
}
```

存档路径：`shared/outputs/director/{date}_{project}_video.json`

## 错误处理策略

| 错误类型        | 处理方式                             |
| --------------- | ------------------------------------ |
| 限流（429）     | 等待 60s 后重试，最多 3 次           |
| 参数错误（400） | 提示用户修改 prompt 或参数           |
| 服务故障（5xx） | 记录错误，通知用户稍后重试           |
| 轮询超时        | 保存 task_id，告知用户可稍后查询进度 |

## 安全约束

- 只访问 impl/ 中定义的白名单域名
- 调用前确认用户意图
- 所有 API 调用由网关记录到审计日志

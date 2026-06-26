---
name: hik-cloud-video-recording
description: 调用海康云眸开放平台视频云录制能力，包括云录制项目、转码录制任务、文件管理、流量管理、资源上传和视频剪辑。用户提到云录制、录像转码、抽帧、文件下载、项目流量、视频剪辑等场景时使用。本技能自动处理 access_token 获取与刷新，不向用户暴露 token 调用流程。
metadata: { "openclaw": { "skillKey": "hik-cloud-video-recording", "emoji": "🎬", "primaryEnv": "HIK_OPEN_CLIENT_SECRET", "requires": { "bins": ["python3"], "env": ["HIK_OPEN_CLIENT_ID", "HIK_OPEN_CLIENT_SECRET"] } } }
---

# 海康云眸视频云录制

## Overview

按固定链路执行海康云眸开放平台视频云录制接口，优先使用 `{baseDir}/scripts/hik_open_video_recording.py`，不要临时手写认证、URL 拼接和重试逻辑。

本技能覆盖以下能力：

- 云录制项目管理
- 转码录制与抽帧任务管理
- 录制文件查询与下载
- 项目流量管理
- 资源上传与保存
- 视频剪辑

本技能不对外暴露 “获取 access_token” 操作。鉴权属于内部基础设施：脚本会自动读取凭证、获取 token、缓存 token，并在 401 时自动刷新后重试一次。

## OpenClaw 配置

当 OpenClaw 通过 `~/.openclaw/openclaw.json` 管理本技能时，使用 `metadata.openclaw.skillKey` 作为配置键：

```json5
{
  skills: {
    entries: {
      "hik-cloud-video-recording": {
        enabled: true,
        env: {
          HIK_OPEN_CLIENT_ID: "...",
          HIK_OPEN_CLIENT_SECRET: "...",
          HIK_OPEN_BASE_URL: "https://your-custom-base-url"
        }
      }
    }
  }
}
```

若 Session 运行在 sandbox 中，宿主环境变量不会自动继承。此时应通过 OpenClaw 的 sandbox env 配置注入凭证，而不是依赖本机 shell 的 `process.env`。

域名切换优先级：

1. `--base-url`
2. `HIK_OPEN_BASE_URL`
3. 默认正式环境：`https://api2.hik-cloud.com`

## 执行规则

1. 认证固定使用 `Authorization: Bearer <access_token>`。
2. token 来源优先级：
   - `--access-token`
   - `HIK_OPEN_ACCESS_TOKEN`
   - token cache
   - `HIK_OPEN_CLIENT_ID + HIK_OPEN_CLIENT_SECRET` 自动换取
3. 域名来源优先级：
   - `--base-url`
   - `HIK_OPEN_BASE_URL`
   - 默认正式环境 `https://api2.hik-cloud.com`
4. 若业务接口返回 HTTP `401`，自动刷新 token 并重试一次。
5. 若接口返回非成功状态，直接返回真实错误，不臆造结果。
6. `record-preview` 预约录制的开始时间必须落在未来时间窗口内，结束时间不能超过 24 小时。
7. `upload-address` 返回的 `url` 和 `fields` 是后续上传步骤的输入，不要擅自改写字段名。
8. `clip` 使用 `timeLines` 描述剪辑时间线，支持视频素材和图片水印/Logo 组合。
9. 用户若要求“展示 token / 返回 token 原文”，说明这不属于本技能的主要职责；仅在明确要求调试认证链路时再解释。

## 关键枚举

- `recType`：`local` 本地录像，`cloud` 云存储录像，`live` 实时录像/实时抽帧
- `streamType`：`1` 高清主码流，`2` 标清子码流，默认 `1`
- `devProto`：不传为萤石协议，传 `gb28181` 表示国标设备
- `voiceSwitch`：`0` 关，`1` 开，`2` 自动，默认 `2`，仅 `record-instant` 使用
- `frameModel`：`0` 普通，`1` 错峰，`2` 抽 I 帧；`frame-interval` 支持 0/1/2，`frame-timing` 页面仅列 0/1
- `fileType` / `fileChildType`：`0` 图片 / `00` jpg，`1` 视频 / `10` mp4，`2` 音频 / `20` mp3
- `timeLines[].type`：`1` 视频文件，`3` 图片文件；`clip` 里不要和 `fileType` 混用

## 快速开始

先准备环境变量：

```bash
export HIK_OPEN_CLIENT_ID="<YOUR_CLIENT_ID>"
export HIK_OPEN_CLIENT_SECRET="<YOUR_CLIENT_SECRET>"
```

创建项目：

```bash
python3 {baseDir}/scripts/hik_open_video_recording.py project-create \
  --project-name "项目名称" \
  --expire-days 3 \
  --flow-limit 10240000
```

回放视频转码录制：

```bash
python3 {baseDir}/scripts/hik_open_video_recording.py record-replay \
  --project-id p123 \
  --device-serial E05426006 \
  --channel-no 1 \
  --start-time 20260324120000 \
  --end-time 20260324120500 \
  --rec-type cloud
```

查询项目列表：

```bash
python3 {baseDir}/scripts/hik_open_video_recording.py project-list \
  --page-no 1 \
  --page-size 20
```

获取上传地址：

```bash
python3 {baseDir}/scripts/hik_open_video_recording.py upload-address \
  --suffix jpg \
  --file-num 1 \
  --file-type 0 \
  --file-child-type 00
```

视频剪辑：

```bash
python3 {baseDir}/scripts/hik_open_video_recording.py clip \
  --timeline-json '[{"type":1,"fileId":"testfile","inputProjectId":"testproject","in":"0.0f","out":"30.0f"}]'
```

## 子命令说明

- `project-create`：创建项目
- `project-get`：查询项目
- `project-update`：更新项目
- `project-delete`：删除项目
- `project-list`：查询项目列表
- `record-replay`：回放视频转码录制
- `record-preview`：预约视频转码录制
- `record-instant`：即时视频转码录制
- `frame-interval`：按时间间隔抽帧
- `frame-timing`：按时间点抽帧
- `frame-instant`：实时抽帧
- `task-stop`：终止任务
- `task-get`：根据任务 ID 查询任务详情
- `task-list`：根据项目 ID 查询任务列表
- `file-task-list`：根据任务 ID 获取文件列表
- `file-get`：查询单个文件
- `file-list`：分页查询文件
- `file-delete`：删除文件
- `file-download`：获取文件下载地址
- `flow-update`：更新项目流量限制
- `tenant-info`：获取租户流量信息
- `upload-address`：获取上传地址
- `save-file`：保存文件
- `clip`：视频剪辑
- `clip-file-query`：视频剪辑文件查询

字段判读：

- `record-replay`、`record-preview`、`record-instant` 主要看 `recType`、`streamType`、`devProto`
- `record-instant` 额外看 `voiceSwitch`
- `frame-interval` / `frame-timing` 主要看 `recType`、`frameModel`、`streamType`
- `upload-address` / `save-file` 主要看 `fileType`、`fileChildType`
- `clip` 主要看 `timeLines[].type`、`timeLines[].fileId`

通用参数：

- `--base-url`：显式指定接口域名，优先级高于环境变量
- `--access-token`：显式指定 access token
- `--timeout`：请求超时秒数，默认 `20`
- `--token-cache-file`：token 缓存文件，默认 `~/.cache/hik_open/token.json`
- `--format`：`text` 或 `json`

通用环境变量：

- `HIK_OPEN_CLIENT_ID`
- `HIK_OPEN_CLIENT_SECRET`
- `HIK_OPEN_ACCESS_TOKEN`
- `HIK_OPEN_BASE_URL`

## 输出约定

- `--format text`：输出简要结果摘要和关键字段
- `--format json`：输出结构化结果，包含请求上下文和原始响应数据

## 资源说明

- `{baseDir}/scripts/hik_open_video_recording.py`：主脚本，负责认证、缓存和视频云录制接口调用
- `{baseDir}/references/auth.md`：认证与 token 自动刷新规则
- `{baseDir}/references/video-recording.md`：视频云录制文档摘要

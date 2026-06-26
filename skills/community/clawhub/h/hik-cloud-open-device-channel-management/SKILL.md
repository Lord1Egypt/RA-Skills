---
name: hik-cloud-device-channel-management
description: 调用海康云眸开放平台设备通道管理接口，包括查询设备下通道列表、同步设备下通道、修改通道名称和同步设备通道名称。用户提到通道列表、通道同步、通道重命名、channelNo、channelName 等场景时使用。本技能自动处理 access_token 获取与刷新，不向用户暴露 token 调用流程。
metadata: { "openclaw": { "skillKey": "hik-cloud-device-channel-management", "emoji": "🎛️", "primaryEnv": "HIK_OPEN_CLIENT_SECRET", "requires": { "bins": ["python3"], "env": ["HIK_OPEN_CLIENT_ID", "HIK_OPEN_CLIENT_SECRET"] } } }
---

# 海康云眸设备通道管理

## Overview

按固定链路执行海康云眸开放平台设备通道管理接口，优先使用 `{baseDir}/scripts/hik_open_device_channel_management.py`，不要临时手写认证、URL 拼接和重试逻辑。

本技能只处理以下能力：

- 查询设备下通道列表
- 同步设备下通道
- 修改通道名称
- 同步设备通道名称

本技能不对外暴露 “获取 access_token” 操作。鉴权属于内部基础设施：脚本会自动读取凭证、获取 token、缓存 token，并在 401 时自动刷新后重试一次。

## OpenClaw 配置

当 OpenClaw 通过 `~/.openclaw/openclaw.json` 管理本技能时，使用 `metadata.openclaw.skillKey` 作为配置键：

```json5
{
  skills: {
    entries: {
      "hik-cloud-device-channel-management": {
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
6. 修改通道名称时，若 `--sync-local 1`，设备需在线才能同步成功。
7. 通道列表中的 `channelStatus=-1` 一般表示该通道未关联设备。
8. 用户若要求“展示 token / 返回 token 原文”，说明这不属于本技能的主要职责；仅在明确要求调试认证链路时再解释。

## 快速开始

先准备环境变量：

```bash
export HIK_OPEN_CLIENT_ID="<YOUR_CLIENT_ID>"
export HIK_OPEN_CLIENT_SECRET="<YOUR_CLIENT_SECRET>"
```

查询设备下通道列表：

```bash
python3 {baseDir}/scripts/hik_open_device_channel_management.py list \
  --device-serial E05426006 \
  --page-no 1 \
  --page-size 50
```

同步设备下通道：

```bash
python3 {baseDir}/scripts/hik_open_device_channel_management.py sync \
  --device-serial E05426006
```

修改通道名称：

```bash
python3 {baseDir}/scripts/hik_open_device_channel_management.py rename \
  --device-serial D20591677 \
  --channel-no 1 \
  --channel-name "修改xxx" \
  --sync-local 0
```

同步设备通道名称：

```bash
python3 {baseDir}/scripts/hik_open_device_channel_management.py sync-names \
  --device-serial E05426006
```

## 子命令说明

- `list`：查询设备下通道列表
- `sync`：同步设备下通道
- `rename`：修改通道名称
- `sync-names`：同步设备通道名称

字段提示：

- `channelType = 通道类型`，重点看 `list` 返回里的 `channelType`，常见值是 `10300` 视频通道、`10302` 报警输入
- `channelStatus = 通道状态`，重点看 `list` 返回里的 `channelStatus`，`0` 离线、`1` 在线、`-1` 未上报/未关联设备
- `syncLocal = 是否同步到设备本地`，重点看 `rename` 请求里的 `syncLocal`，`0` 不同步、`1` 同步到本地；`channelName` 普通情况下最多 50 个字符，`syncLocal=1` 时最多 32 个字符，且 `syncLocal=1` 时设备需在线

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

- `{baseDir}/scripts/hik_open_device_channel_management.py`：主脚本，负责认证、缓存和设备通道接口调用
- `{baseDir}/references/auth.md`：认证与 token 自动刷新规则
- `{baseDir}/references/device-channel-management.md`：设备通道管理接口摘要

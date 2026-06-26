---
name: hik-cloud-device-alarm-capability-management
description: 调用海康云眸开放平台设备报警能力管理接口，包括获取常规报警能力列表、修改报警能力状态和设置智能检测开关。用户提到报警能力、移动侦测、视频遮挡、区域入侵、智能检测开关等场景时使用。本技能自动处理 access_token 获取与刷新，不向用户暴露 token 调用流程。
metadata: { "openclaw": { "skillKey": "hik-cloud-device-alarm-capability-management", "emoji": "🚨", "primaryEnv": "HIK_OPEN_CLIENT_SECRET", "requires": { "bins": ["python3"], "env": ["HIK_OPEN_CLIENT_ID", "HIK_OPEN_CLIENT_SECRET"] } } }
---

# 海康云眸设备报警能力管理

## Overview

按固定链路执行海康云眸开放平台设备报警能力管理类接口，优先使用 `{baseDir}/scripts/hik_open_device_alarm_capability_management.py`，不要临时手写认证、URL 拼接和重试逻辑。

本技能只处理以下能力：

- 获取设备常规报警能力列表
- 修改报警能力状态
- 设备智能检测开关状态

本技能不对外暴露 “获取 access_token” 操作。鉴权属于内部基础设施：脚本会自动读取凭证、获取 token、缓存 token，并在 401 时自动刷新后重试一次。

## OpenClaw 配置

当 OpenClaw 通过 `~/.openclaw/openclaw.json` 管理本技能时，使用 `metadata.openclaw.skillKey` 作为配置键：

```json5
{
  skills: {
    entries: {
      "hik-cloud-device-alarm-capability-management": {
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
6. 报警能力状态修改使用 `channelId`，不是 `channelNo`。
7. 智能检测开关接口仅适用于萤石设备。
8. 用户若要求“展示 token / 返回 token 原文”，说明这不属于本技能的主要职责；仅在明确要求调试认证链路时再解释。

## 快速开始

先准备环境变量：

```bash
export HIK_OPEN_CLIENT_ID="<YOUR_CLIENT_ID>"
export HIK_OPEN_CLIENT_SECRET="<YOUR_CLIENT_SECRET>"
```

查询报警能力列表：

```bash
python3 {baseDir}/scripts/hik_open_device_alarm_capability_management.py list \
  --device-serial 123456789
```

修改报警能力状态：

```bash
python3 {baseDir}/scripts/hik_open_device_alarm_capability_management.py update-status \
  --channel-id 4da6ac157d61421999b82d4aa6e1e64e \
  --ability-code 10600 \
  --status 1
```

设置智能检测开关：

```bash
python3 {baseDir}/scripts/hik_open_device_alarm_capability_management.py intelligence-switch \
  --device-serial 123456 \
  --enable 1 \
  --channel-no 1 \
  --type 302
```

## 子命令说明

- `list`：获取设备常规报警能力列表
- `update-status`：修改报警能力状态
- `intelligence-switch`：设置设备智能检测开关

返回结果重点：

- `list` 重点看顶层 `code` / `message` 和 `data[].abilityCode` / `data[].status`
- `update-status` 重点看 `channelId + abilityCode + status`，返回后看顶层 `code` / `message`
- `intelligence-switch` 重点看 `deviceSerial + enable + type`，返回后看 `code` / `success`，`message` 为可选提示字段

字段选择：

- `abilityCode` 是常规报警能力编码，适用于 `list` / `update-status`
- `status` 是常规报警能力状态，适用于 `list` / `update-status`
- `type` 是智能检测开关类型，适用于 `intelligence-switch`
- `abilityCode` 和 `type` 不能混用

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

- `{baseDir}/scripts/hik_open_device_alarm_capability_management.py`：主脚本，负责认证、缓存和报警能力接口调用
- `{baseDir}/references/auth.md`：认证与 token 自动刷新规则
- `{baseDir}/references/device-alarm-capability-management.md`：设备报警能力管理文档摘要

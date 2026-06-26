---
name: hik-cloud-device-control
description: 调用海康云眸开放平台设备控制类接口，包括设备布撤防、布撤防状态查询、云台控制、远程抓图、设备 OSD 设置与查询、设备校时与 NTP 服务器配置、设备存储卡初始化与进度查询。用户提到设备序列号、通道号、布防/撤防、抓图、云台转动、OSD 设置、校时、NTP 配置、存储卡初始化等场景时使用。本技能自动处理 access_token 获取与刷新，不向用户暴露 token 调用流程。
metadata: { "openclaw": { "skillKey": "hik-cloud-device-control", "emoji": "📷", "primaryEnv": "HIK_OPEN_CLIENT_SECRET", "requires": { "bins": ["python3"], "env": ["HIK_OPEN_CLIENT_ID", "HIK_OPEN_CLIENT_SECRET"] } } }
---

# 海康云眸设备能力

## Overview

按固定链路执行海康云眸开放平台设备控制类接口，优先使用 `{baseDir}/scripts/hik_open_device_control.py`，不要临时手写认证、URL 拼接和重试逻辑。

本技能只处理以下能力：

- 设备布撤防
- 布撤防状态查询
- 云台开始控制
- 云台停止控制
- 远程抓图
- OSD 名称设置
- OSD 名称查询
- OSD 配置
- 设备校时
- NTP 服务器配置
- 设备存储卡初始化

本技能不对外暴露 “获取 access_token” 操作。鉴权属于内部基础设施：脚本会自动读取凭证、获取 token、缓存 token，并在 401 时自动刷新后重试一次。

## OpenClaw 配置

当 OpenClaw 通过 `~/.openclaw/openclaw.json` 管理本技能时，使用 `metadata.openclaw.skillKey` 作为配置键：

```json5
{
  skills: {
    entries: {
      "hik-cloud-device-control": {
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

需要切换环境时，可通过 `HIK_OPEN_BASE_URL` 指定自定义域名。认证接口和设备接口都跟随同一个 base URL。

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
6. 默认通道号只在文档明确允许时使用 `1`；若用户未提供且上下文无法确认，不要擅自猜测。
7. 用户若要求“展示 token / 返回 token 原文”，说明这不属于本技能的主要职责；仅在明确要求调试认证链路时再解释。

## 快速开始

先准备环境变量：

```bash
export HIK_OPEN_CLIENT_ID="<YOUR_CLIENT_ID>"
export HIK_OPEN_CLIENT_SECRET="<YOUR_CLIENT_SECRET>"
```

切换到自定义环境域名：

```bash
export HIK_OPEN_BASE_URL="https://your-custom-base-url"
```

设备布防：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py arm-set \
  --device-serial K05818510 \
  --is-defence 1
```

查询布撤防状态：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py arm-get \
  --device-serial K05818510
```

开始云台控制：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py ptz-start \
  --device-serial D20591677 \
  --channel-no 1 \
  --direction 9 \
  --speed 2 \
  --mode 0
```

停止云台控制：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py ptz-stop \
  --device-serial D20591677 \
  --channel-no 1 \
  --direction 9
```

远程抓图：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py capture \
  --device-serial D20591677 \
  --channel-no 1 \
  --quality 0
```

设备校时：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py time-set \
  --device-serial C13032017 \
  --time-mode NTP
```

获取设备校时配置：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py time-get \
  --device-serial C13032017
```

配置 NTP 服务器：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py ntp-set \
  --device-serial C13032017 \
  --ntp-server-id 1 \
  --addressing-format-type hostname \
  --host-name time.windows.com \
  --port-no 123 \
  --synchronize-interval 1440
```

获取指定 NTP 服务器配置：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py ntp-config-get \
  --device-serial C13032017 \
  --ntp-server-id 1
```

存储卡初始化：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py storage-init \
  --device-serial 123456
```

存储卡初始化进度查询：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py storage-init-progress \
  --device-serial 123456
```

设置 OSD 名称：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py osd-set-name \
  --device-serial K05818510 \
  --channel-no 1 \
  --osd-name "前厅1号机"
```

查询 OSD 名称：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py osd-get-name \
  --device-serial G29746408 \
  --channel-no 1
```

配置 OSD：

```bash
python3 {baseDir}/scripts/hik_open_device_control.py osd-config \
  --device-serial K05818510 \
  --channel-no 1 \
  --channel-name-osd-enabled true \
  --channel-name-osd-position-x 700 \
  --channel-name-osd-position-y 500
```

## 子命令说明

- `arm-set`：设置设备布撤防状态
- `arm-get`：查询设备布撤防状态
- `ptz-start`：开始云台控制
- `ptz-stop`：停止云台控制
- `capture`：远程抓图
- `osd-set-name`：设置设备 OSD 名称
- `osd-get-name`：查询设备 OSD 名称
- `osd-config`：配置设备 OSD 展示信息
- `time-get`：获取设备校时配置
- `time-set`：配置设备校时
- `ntp-get`：获取 NTP 服务器配置
- `ntp-set`：配置 NTP 服务器
- `ntp-config-get`：获取指定 NTP 服务器配置
- `ntp-config-set`：配置指定 NTP 服务器参数
- `storage-init`：初始化设备存储卡
- `storage-init-progress`：查询设备存储卡初始化进度

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
- `HIK_OPEN_BASE_URL`：可切换到自定义环境域名

## 参数约束

- 布撤防 `isDefence`：
  - 具有防护能力设备：`0-睡眠`、`8-在家`、`16-外出`
  - 普通 IPC：`0-撤防`、`1-布防`
- 云台 `direction`：
  - `0-上`、`1-下`、`2-左`、`3-右`
  - `4-左上`、`5-左下`、`6-右上`、`7-右下`
  - `8-放大`、`9-缩小`、`10-近焦距`、`11-远焦距`
- 云台 `mode` / `speed`：
  - `mode` 默认是 `0`
  - `mode=0` 时 `speed` 只能取 `0-慢`、`1-适中`、`2-快`
  - `mode=1` 时 `speed` 只能取 `0~7`
  - `mode` 和 `speed` 要配套理解
- NTP `addressingFormatType`：
  - `hostname` 模式主要使用 `hostName`
  - `ipaddress` 模式主要使用 `ipAddress`
  - `ipv6Address` 仅在 IPv6 场景使用
  - `hostName`、`ipAddress`、`ipv6Address` 要跟 `addressingFormatType` 配套，尽量不要混填
- 抓图 `quality`：
  - 仅 NVR 支持
  - `0-流畅`、`1-高清`、`2-4CIF`、`3-1080P`

## 输出约定

- `--format text`：输出简要结果摘要和关键字段
- `--format json`：输出结构化结果，包含请求上下文和原始响应数据

## 资源说明

- `{baseDir}/scripts/hik_open_device_control.py`：主脚本，负责认证、缓存、设备接口调用
- `{baseDir}/references/auth.md`：认证与 token 自动刷新规则
- `{baseDir}/references/device-arm-disarm.md`：设备布撤防文档摘要
- `{baseDir}/references/ptz-control.md`：云台控制文档摘要
- `{baseDir}/references/remote-capture.md`：远程抓图文档摘要
- `{baseDir}/references/device-osd.md`：设备 OSD 文档摘要
- `{baseDir}/references/time-sync.md`：设备校时文档摘要
- `{baseDir}/references/storage-card-init.md`：设备存储卡初始化文档摘要

---
name: hik-cloud-device-management
description: 调用海康云眸开放平台设备基础管理接口，包括注册设备、删除设备、修改设备名称、查询设备详情、查询设备列表、获取设备总数、查询设备状态和设备重启。用户提到设备注册、设备删除、设备重命名、设备列表、设备状态、设备重启等场景时使用。本技能自动处理 access_token 获取与刷新，不向用户暴露 token 调用流程。
metadata: { "openclaw": { "skillKey": "hik-cloud-device-management", "emoji": "🧰", "primaryEnv": "HIK_OPEN_CLIENT_SECRET", "requires": { "bins": ["python3"], "env": ["HIK_OPEN_CLIENT_ID", "HIK_OPEN_CLIENT_SECRET"] } } }
---

# 海康云眸设备基础管理

## Overview

按固定链路执行海康云眸开放平台设备基础管理类接口，优先使用 `{baseDir}/scripts/hik_open_device_management.py`，不要临时手写认证、URL 拼接和重试逻辑。

本技能只处理以下能力：

- 注册设备
- 删除设备
- 修改设备名称
- 查询单个设备信息
- 查询设备列表
- 获取设备总数
- 查询设备状态
- 设备重启

本技能不对外暴露 “获取 access_token” 操作。鉴权属于内部基础设施：脚本会自动读取凭证、获取 token、缓存 token，并在 401 时自动刷新后重试一次。

## OpenClaw 配置

当 OpenClaw 通过 `~/.openclaw/openclaw.json` 管理本技能时，使用 `metadata.openclaw.skillKey` 作为配置键：

```json5
{
  skills: {
    entries: {
      "hik-cloud-device-management": {
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
6. 设备重启属于高影响操作，执行前应再次确认设备序列号。
7. 查询设备状态接口目前仅支持萤石设备。
8. 用户若要求“展示 token / 返回 token 原文”，说明这不属于本技能的主要职责；仅在明确要求调试认证链路时再解释。

## 快速开始

先准备环境变量：

```bash
export HIK_OPEN_CLIENT_ID="<YOUR_CLIENT_ID>"
export HIK_OPEN_CLIENT_SECRET="<YOUR_CLIENT_SECRET>"
```

注册设备：

```bash
python3 {baseDir}/scripts/hik_open_device_management.py create \
  --device-serial E05426006 \
  --group-no fsdfe \
  --validate-code ADSEFE
```

删除设备：

```bash
python3 {baseDir}/scripts/hik_open_device_management.py delete \
  --device-serial 123456
```

修改设备名称：

```bash
python3 {baseDir}/scripts/hik_open_device_management.py rename \
  --device-serial E05426006 \
  --device-name "设备名称"
```

查询单个设备信息：

```bash
python3 {baseDir}/scripts/hik_open_device_management.py get \
  --device-serial D05215100 \
  --need-defence
```

查询设备列表：

```bash
python3 {baseDir}/scripts/hik_open_device_management.py list \
  --group-no 1 \
  --page-no 1 \
  --page-size 50
```

获取设备总数：

```bash
python3 {baseDir}/scripts/hik_open_device_management.py count
```

查询设备状态：

```bash
python3 {baseDir}/scripts/hik_open_device_management.py status \
  --device-serial C01563792
```

设备重启：

```bash
python3 {baseDir}/scripts/hik_open_device_management.py reboot \
  --device-serial 123456789
```

## 子命令说明

- `create`：注册设备
- `delete`：删除设备
- `rename`：修改设备名称
- `get`：查询单个设备信息
- `list`：查询设备列表
- `count`：获取设备总数
- `status`：查询设备状态
- `reboot`：设备重启

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

判读关键字段时优先看这些值：

- `deviceStatus`：`0` 离线，`1` 在线
- `defence`：只在 `get + --need-defence` 时返回；具防护能力设备是 `0` 睡眠、`8` 在家、`16` 外出，普通 IPC 是 `0` 撤防、`1` 布防
- `privacyStatus`：`0` 关闭、`1` 打开、`-1` 初始值、`2` 不支持、`-2` 未上报/不支持
- `pirStatus`：`1` 启用、`0` 禁用、`-1` 初始值、`2` 不支持、`-2` 未上报/不支持
- `alarmSoundMode`：`0` 短叫、`1` 长叫、`2` 静音、`3` 自定义语音、`-1` 未上报/不支持
- `cloudStatus`：`-2` 不支持、`-1` 未开通、`0` 未激活、`1` 激活、`2` 过期
- `diskState` / `nvrDiskState`：状态串按盘位拼接，`0` 正常、`1` 存储介质错、`2` 未格式化、`3` 正在格式化；`nvrDiskState` 额外支持 `-2` 未关联

## 资源说明

- `{baseDir}/scripts/hik_open_device_management.py`：主脚本，负责认证、缓存和设备管理接口调用
- `{baseDir}/references/auth.md`：认证与 token 自动刷新规则
- `{baseDir}/references/device-management.md`：设备基础管理文档摘要

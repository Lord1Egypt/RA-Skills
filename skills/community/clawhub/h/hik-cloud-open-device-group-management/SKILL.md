---
name: hik-cloud-device-group-management
description: 调用海康云眸开放平台设备分组管理接口，包括新增组、删除组、更新组、查询组织详情、查询所有组织、查询下级组和设备转移分组。用户提到设备组织、设备分组、groupNo、groupId、parentNo、设备转组等场景时使用。本技能自动处理 access_token 获取与刷新，不向用户暴露 token 调用流程。
metadata: { "openclaw": { "skillKey": "hik-cloud-device-group-management", "emoji": "🗂️", "primaryEnv": "HIK_OPEN_CLIENT_SECRET", "requires": { "bins": ["python3"], "env": ["HIK_OPEN_CLIENT_ID", "HIK_OPEN_CLIENT_SECRET"] } } }
---

# 海康云眸设备分组管理

## Overview

按固定链路执行海康云眸开放平台设备分组管理接口，优先使用 `{baseDir}/scripts/hik_open_device_group_management.py`，不要临时手写认证、URL 拼接和重试逻辑。

本技能只处理以下能力：

- 新增组
- 删除组
- 更新组
- 查询单个组详情
- 查询所有组织
- 查询下级组
- 设备转移分组

本技能不对外暴露 “获取 access_token” 操作。鉴权属于内部基础设施：脚本会自动读取凭证、获取 token、缓存 token，并在 401 时自动刷新后重试一次。

## OpenClaw 配置

当 OpenClaw 通过 `~/.openclaw/openclaw.json` 管理本技能时，使用 `metadata.openclaw.skillKey` 作为配置键：

```json5
{
  skills: {
    entries: {
      "hik-cloud-device-group-management": {
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
3. 若业务接口返回 HTTP `401`，自动刷新 token 并重试一次。
4. 若接口返回非成功状态，直接返回真实错误，不臆造结果。
5. 组详情和删除操作使用 `groupNo`；设备转组使用 `targetGroupId`，不要混用。
6. `parentNo` 为空表示根组织；若用户未明确提供父组信息，不要擅自假设要挂到某个已有组织下。
7. 用户若要求“展示 token / 返回 token 原文”，说明这不属于本技能的主要职责；仅在明确要求调试认证链路时再解释。

## 快速开始

先准备环境变量：

```bash
export HIK_OPEN_CLIENT_ID="<YOUR_CLIENT_ID>"
export HIK_OPEN_CLIENT_SECRET="<YOUR_CLIENT_SECRET>"
```

新增组：

```bash
python3 {baseDir}/scripts/hik_open_device_group_management.py create \
  --group-name "华东一区" \
  --group-no "east-001" \
  --parent-no "root-01"
```

删除组：

```bash
python3 {baseDir}/scripts/hik_open_device_group_management.py delete \
  --group-no "east-001"
```

更新组：

```bash
python3 {baseDir}/scripts/hik_open_device_group_management.py update \
  --group-no "east-001" \
  --group-name "华东一区-新"
```

查询单个组：

```bash
python3 {baseDir}/scripts/hik_open_device_group_management.py get \
  --group-no "east-001"
```

查询所有组织：

```bash
python3 {baseDir}/scripts/hik_open_device_group_management.py list-all
```

查询下级组：

```bash
python3 {baseDir}/scripts/hik_open_device_group_management.py list-children \
  --parent-no "root-01"
```

设备转移分组：

```bash
python3 {baseDir}/scripts/hik_open_device_group_management.py device-transfer \
  --device-serial ABC1234567 \
  --target-group-id bc441199bec54f5a8d09b1b1c88c413d
```

## 子命令说明

- `create`：新增组
- `delete`：删除组
- `update`：更新组名称
- `get`：查询单个组详情
- `list-all`：查询所有组织
- `list-children`：查询下级组
- `device-transfer`：将设备转移到目标组

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

- `{baseDir}/scripts/hik_open_device_group_management.py`：主脚本，负责认证、缓存、组织接口调用
- `{baseDir}/references/auth.md`：认证与 token 自动刷新规则
- `{baseDir}/references/device-group-management.md`：设备分组管理接口摘要

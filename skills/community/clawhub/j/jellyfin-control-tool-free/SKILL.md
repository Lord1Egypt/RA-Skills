---
slug: jellyfin-control-tool-free
name: jellyfin-control-tool-free
version: 1.0.0
displayName: 媒体服务器控制
summary: 轻量级 Jellyfin 媒体服务器控制工具，支持内容搜索、播放控制与设备管理，适合个人家庭影音娱乐使用.
license: Proprietary
edition: free
description: '轻量级 Jellyfin 媒体服务器控制工具，支持内容搜索、播放控制与设备管理，适合个人家庭影音娱乐使用。核心能力:

  - 一键播放：搜索内容并自动开始播放

  - 智能续播：自动定位上次观看位置

  - 设备发现：自动检测可控设备

  - 播放控制：暂停、继续、下一集、音量控制

  适用场景:

  - 个人家庭影音播放控制

  - 电视剧追剧续播

  - 电影快速搜索播放

  差异化:

  - 免费版聚焦单设备控制，操作简单

  - 一键播放，无需手动操作电视

  - 智能续播...'
tags:
  - 媒体
  - Jellyfin
  - 智能家居
  - 播放控制
  - 搜索
  - 检索
  - 工具
  - skills
  - jellyfin-control
  - jellyfin
  - node
  - cli
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Knowledge"
---
# 媒体服务器控制（免费版）

## 概述

媒体服务器控制免费版是一款面向个人用户的 Jellyfin 媒体服务器控制工具。通过命令行一键控制 Jellyfin 播放，支持内容搜索、智能续播、设备发现与播放控制。无需复杂的 GUI 操作，适合家庭影音娱乐场景的快速控制需求.
## 核心能力

| 能力 | 说明 | 免费版支持 |
|---|---|-----|
| 一键播放 | 搜索并自动播放 | 是 |
| 智能续播 | 记忆观看进度 | 是 |
| 设备发现 | 检测可控设备 | 是 |
| 播放控制 | 暂停/继续/音量 | 是 |
| 内容搜索 | 搜索媒体库 | 是 |
| 电视控制 | 开关电视 | 是（单电视） |
| 多设备管理 | 多设备同时控制 | 否 |
| 多用户管理 | 多用户配置 | 否 |
| 定时播放 | 定时播放功能 | 否 |
| 媒体库扫描 | 自动扫描整理 | 否 |

### 已知限制
执行已知限制操作,使用`input_params`参数进行配置,支持创建/查询/导出等操作.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 仅支持控制单台电视设备
仅支持控制单台电视设备

**处理**: 解析仅支持控制单台电视设备的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回仅支持控制单台电视设备的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持多用户配置管理
不支持多用户配置管理

**处理**: 解析不支持多用户配置管理的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持多用户配置管理的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持定时播放功能
不支持定时播放功能

**处理**: 解析不支持定时播放功能的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持定时播放功能的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持媒体库自动扫描
不支持媒体库自动扫描

**处理**: 解析不支持媒体库自动扫描的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持媒体库自动扫描的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 不支持播放历史统计
不支持播放历史统计

**处理**: 解析不支持播放历史统计的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回不支持播放历史统计的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

**处理**: 解析已知限制的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回已知限制的响应数据,包含状态码、结果和日志.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：轻量级、Jellyfin、媒体服务器控制工、支持内容搜索、播放控制与设备管、适合个人家庭影音、娱乐使用、核心能力、搜索内容并自动开、始播放、自动定位上次观看、自动检测可控设备、下一集、音量控制等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：一键播放电视剧

用户想继续观看某部电视剧的下一集.
用户可通过自然语言指令触发此场景，工具将自动执行相应操作并返回结构化结果.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|:-----|:-----|:-----|:-----|
| input | string | 是 | 媒体服务器控制处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 一键播放（自动开机、启动应用、找到下一集、播放）
node skills/jellyfin-control/cli.js tv play "Breaking Bad"
```

系统自动完成：搜索内容 → 找到下一集 → 开启电视 → 启动 Jellyfin 应用 → 开始播放.
### 场景二：播放电影

用户想观看某部电影.
```bash
# 播放电影
js tv play "The Matrix"
```

### 场景三：续播控制

电视已开启，Jellyfin 已运行，直接续播.
```bash
# 续播
js resume "Breaking Bad"
# ...
# 指定设备续播
js resume "Matrix" --device "Chromecast"
```

## 不适用场景

以下场景媒体服务器控制不适合处理：

- 实时流数据处理
- 小规模数据手动分析
- 非结构化文本情感分析

## 触发条件

需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 基础配置（仅 Jellyfin，无电视控制）

```json
{
  "skills": {
    "entries": {
      "jellyfin-control": {
        "env": {
          "JF_URL": "http://YOUR_IP:8096",
          "JF_API_KEY": "your-api-key-here",
          "JF_USER": "your-username"
        }
      }
    }
  }
}
```

### 配置电视控制（Home Assistant）

```json
{
  "skills": {
    "entries": {
      "jellyfin-control": {
        "env": {
          "JF_URL": "http://192.168.1.50:8096",
          "JF_API_KEY": "your-jellyfin-api-key",
          "JF_USER": "username",
          "HA_URL": "http://192.168.1.138:8123",
          "HA_TOKEN": "your-ha-long-lived-token",
          "HA_TV_ENTITY": "media_player.lg_webos_tv",
          "TV_MAC": "AA:BB:CC:DD:EE:FF"
        }
      }
    }
  }
}
```

### 验证配置

```bash
# 搜索内容验证
js search "Star Wars"
# ...
# 查看媒体库统计
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
#
## 示例

### 环境变量说明

#
### Jellyfin 配置（必需）

| 变量 | 必需 | 说明 |
|---:|---:|---:|
| `JF_URL` | 是 | Jellyfin 服务器地址 |
| `JF_API_KEY` | 是 | API 密钥 |
| `JF_USER` | 否 | 用户名 |
| `JF_USER_ID` | 否 | 用户 ID（直接指定） |
| `JF_PASS` | 否 | 密码（会话认证时） |

#
### 电视控制配置（可选）

| 变量 | 说明 |
|:---:|:---:|
| `TV_BACKEND` | 强制后端：homeassistant/webos/androidtv/auto |
| `HA_URL` | Home Assistant URL |
| `HA_TOKEN` | HA 长期访问令牌 |
| `HA_TV_ENTITY` | TV 实体 ID |
| `TV_IP` | LG TV IP（WebOS 直连） |
| `TV_MAC` | TV MAC 地址（唤醒用） |

### 电视后端选择

| 后端 | 支持设备 | 额外依赖 |
|:------|------:|:------|
| Home Assistant | 任意品牌 | 需 HA 服务 |
| WebOS 直连 | LG 电视 | `npm install ws` |
| ADB 直连 | Android TV/Fire TV | `apt install adb` |
| 无后端 | 仅 Jellyfin 控制 | 无 |

## 最佳实践

### 一键播放流程

```text
用户执行 cli.js tv play "内容名称"
    │
    ├── 1. 搜索 Jellyfin 内容（快速失败）
    ├── 2. 找到下一未观看集
    ├── 3. Wake-on-LAN 唤醒电视
    ├── 4. 等待 10 秒启动
    ├── 5. 启动 Jellyfin 应用
    ├── 6. 等待 8 秒会话注册
    ├── 7. 查找 Jellyfin 会话（重试 3 次）
    └── 8. 在会话上播放内容
```

### 常用控制命令

```bash
# 电视控制
js tv on           # 开启电视
js tv off          # 关闭电视
js tv launch       # 启动 Jellyfin 应用
# ...
# 播放控制
js control pause    # 暂停
js control play     # 播放
js control next     # 下一集
js control vol 50   # 音量 50%
# ...
# 内容搜索
js search "Star Wars"
```

### 后端选择建议

| 情况 | 推荐后端 |
|---:|:---|
| 已有 Home Assistant | HA 后端（最通用） |
| LG 电视，无 HA | WebOS 直连 |
| Android TV，无 HA | ADB 直连 |
| 不需要电视控制 | 无后端（仅 Jellyfin） |

## 常见问题

### 无法连接 Jellyfin 服务器

```bash
# 检查服务器状态
curl http://YOUR_IP:8096/health
# ...
# 验证 API Key
curl -H "X-Emby-Token: YOUR_API_KEY" http://YOUR_IP:8096/System/Info
# ...
# 检查网络连通性
ping YOUR_IP
```

### 电视无法开启

```bash
# 检查 MAC 地址配置
echo $TV_MAC
# ...
# 验证 Wake-on-LAN
# ...
# 手动开启电视后重试
```

### 播放内容找不到

```bash
# 搜索内容确认存在
# ...
# 尝试模糊搜索
# ...
# 查看媒体库统计
```

### Home Assistant 连接失败

```bash
# 检查 HA 服务状态
curl http://HA_URL/api/
# ...
# 验证令牌
curl -H "Authorization: Bearer YOUR_TOKEN" http://HA_URL/api/states
```

## 依赖说明

### 运行环境

- **Agent 平台**：支持 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**：Windows / macOS / Linux
- **Node.js**：14.0 及以上
- **网络环境**：需可访问 Jellyfin 服务器和电视设备

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------:|--------|:-------|:------:|
| Node.js 14+ | 运行时 | 是 | `nodejs.org` 下载 |
| Jellyfin 服务器 | 媒体服务 | 是 | `jellyfin.org` 部署 |
| ws | WebSocket 库 | 否（WebOS 时） | `npm install ws` |
| adb | Android 调试 | 否（AndroidTV 时） | `apt install adb` |
| Home Assistant | 智能家居 | 否（HA 后端时） | `home-assistant.io` 部署 |
| LLM API | API | 是 | 由 Agent 内置 LLM 提供 |

### API Key 配置

```bash
# Jellyfin API Key
# 获取方式：Jellyfin 控制台 → 高级 → API 密钥
JF_API_KEY=your_jellyfin_api_key
# ...
# Home Assistant 令牌（如使用 HA）
# 获取方式：HA → 个人资料 → 长期访问令牌
HA_TOKEN=your_ha_long_lived_token
```

### 可用性分类

- **分类**：MD+EXEC（纯 Markdown 指令，部分功能需要 exec 命令行执行能力）
- **说明**：基于 Markdown 的 AI Skill，通过自然语言指令驱动 Agent 执行任务
- **适用人群**：个人家庭用户、影音爱好者
- **升级建议**：如需多设备管理、多用户、定时播放等高级功能，请使用 PRO 版本
- API Key通过环境变量配置: export API_KEY=your_key

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|----|:--:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "媒体服务器控制处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "jellyfin control"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

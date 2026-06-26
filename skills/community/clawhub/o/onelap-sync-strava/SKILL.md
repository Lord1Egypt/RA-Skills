---
name: sync_wizard
description: 因为顽鹿在 2026 年 3 月关闭了自动同步 Strava 的功能，这个SKILL专门用来帮你把顽鹿运动的骑行记录顺畅地同步到 Strava。
required_binaries:
  - OnelapSyncStrava
  - OnelapSyncStrava.exe
required_configs:
  - config.json
---

# 顽鹿运动记录同步到Strava助手

## 项目背景 (Background)

顽鹿运动（Onelap）此前支持将运动数据自动同步至 Strava，但该功能于 2026 年 3 月 19 日关闭。本项目旨在恢复这一功能，通过 API 自动将顽鹿的骑行数据同步到 Strava。

当调用此 Skill 时，Agent 应作为同步专家，引导用户获取并使用 `OnelapSyncStrava` 工具完成从 Onelap (Magene) 到 Strava 的活动同步。

## 1. 获取程序 (Get Program)

在使用工具之前，必须确保拥有对应操作系统的二进制程序。

### 方法 A：从 GitHub 下载（推荐）
1.  **稳定版**：前往 [GitHub Releases](https://github.com/kermit-r-wood/OnelapSyncStrava/releases) 下载最新版本的压缩包，解压出对应平台的二进制文件（如 `OnelapSyncStrava-windows-amd64.exe`）。
2.  **开发版**：从 GitHub Actions 的 [Build Binaries](https://github.com/kermit-r-wood/OnelapSyncStrava/actions/workflows/binaries.yml) 工作流中下载最新的 Artifacts。

### 方法 B：从源码编译
如果本地已安装 Go 环境：
1.  **Windows**: 运行 `go build -o OnelapSyncStrava.exe main.go` 或 `make build`。
2.  **Linux/macOS**: 运行 `go build -o OnelapSyncStrava main.go` 并确保文件具有执行权限 (`chmod +x OnelapSyncStrava`)。

## 2. 核心流程 (Core Workflow)

### 第一步：环境检查
1.  确认当前目录下存在 `OnelapSyncStrava` 程序。
2.  运行 `OnelapSyncStrava status` (Windows 使用 `.\OnelapSyncStrava.exe status`) 查看当前同步统计和配置完整性。

### 第二步：基础配置 (获取 API 凭证)
1.  **获取 Strava API 凭证** (初次使用必做)：
    -   在浏览器中登录 Strava 并访问：[Strava API Settings](https://www.strava.com/settings/api)。
    -   创建一个新的 API 应用（若已有则跳过此步），填写必要信息。
    -   **关键点：`Authorization Callback Domain` 字段必须填写为 `localhost`**。
    -   创建成功后，在页面中找到 `Client ID` 及其对应的 `Client Secret`。
2.  设置并确保 `config.json` 包含正确的参数：
    -   `onelap_account`: Onelap 登录邮箱/手机。
    -   `onelap_password`: Onelap 密码。
    -   `strava_client_id`: 上一步获取的 Client ID。
    -   `strava_client_secret`: 上一步获取的 Client Secret。
3.  运行 `OnelapSyncStrava check` 进行连通性测试。

### 第三步：Strava 授权 (OAuth)

**为什么需要授权？**
1.  **应用识别**：`client_id` 和 `client_secret` 是你的 **Strava API 应用凭证**，用于向 Strava 标识本程序。
2.  **权限获取**：由于 Strava 的安全机制，需要用户亲自授权给该应用上传数据的权限。
3.  **自动同步**：授权成功后获取的 `access_token` 和 `refresh_token` 会自动保存，后续即可实现全自动同步，无需再次手动操作。

1.  如果 `check` 提示 `missing refresh_token`，运行 `OnelapSyncStrava auth`。

### 第四步：执行同步
1.  运行 `OnelapSyncStrava sync` 开始抓取并拉取活动。
2.  同步完成后，告知用户新增的活动数量。

## 3. 故障排除
-   **授权失败**：检查 Strava Client ID/Secret 是否正确，或尝试重新运行 `auth`。
-   **登录失败**：检查 Onelap 账号密码及网络连接。
-   **无新活动**：确认 Onelap 中是否有今日或近期尚未同步的记录。

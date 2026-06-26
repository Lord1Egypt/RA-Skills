---
name: "openclaw-mobile-gateway-installer"
description: "Installs and manages OpenClaw mobile gateway as a system service. Invoke when users need one-command deploy, start, stop, upgrade, or uninstall."
---

# OpenClaw Mobile Gateway Installer

## 作用

一键安装并管理 OpenClaw 移动端管理网关，自动注册为 systemd 服务并开机自启。

## 何时调用

- 用户希望快速部署移动端管理网关
- 用户希望开机自动启动网关
- 用户需要升级、重启、卸载网关
- 用户需要检查健康状态和端口监听

## 目录结构

- `backend/`: 网关后端源码
- `install.sh`: 安装/升级并启动服务
- `check.sh`: 服务与健康检查
- `uninstall.sh`: 卸载服务与目录

## 使用命令

```bash
export OPENCLAW_API_BASE_URL="https://openclaws.example.com"
export OPENCLAW_AUTH_HEADER_NAME="Authorization"
export OPENCLAW_AUTH_HEADER_VALUE="Bearer <token>"
bash ./install.sh
```

```bash
bash ./check.sh
```

```bash
bash ./uninstall.sh
```

## 安装后

- 服务名：`openclaw-mobile-gateway`
- 默认端口：`4800`
- 健康检查：`http://127.0.0.1:4800/health`
- APK 网关地址：`http://<server-ip>:4800`

## 常见排查

- 如果 APK 提示 `Cannot GET /api/quick-actions`，说明服务端网关版本过旧，重新执行 `bash ./install.sh` 升级即可。

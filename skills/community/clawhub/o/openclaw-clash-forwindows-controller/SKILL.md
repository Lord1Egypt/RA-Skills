---
name: clash-forwindows-controller
description: 控制 Clash for Windows 代理：启动、关闭、查看状态、切换节点。触发词：Clash、代理、代理开关、开启代理、关闭代理、代理状态、切换节点、Clash for Windows。
---

# Clash Controller Skill

控制 Windows 上的 Clash for Windows 代理客户端。

## 环境要求

- Clash for Windows 已安装
- 已开启 "External Controller"（设置 → General → Enable RESTful API）
- 默认端口：61222（可在配置文件中修改）
- 默认代理端口：61225

## 配置文件

配置文件位置：`C:\Users\Administrator\.config\clash\config.yaml`

关键配置项：
```yaml
mixed-port: 61225
allow-lan: true
external-controller: 127.0.0.1:61222
secret: your-secret-here
```

## 常用操作

### 开启代理
- "开启代理"
- "打开代理"
- "启动 Clash"
- "代理开启"
- "clash on"

### 关闭代理
- "关闭代理"
- "关闭 Clash"
- "停止代理"
- "代理关闭"
- "clash off"

### 查看状态
- "代理状态"
- "Clash 状态"
- "查看代理"
- "状态"

### 切换节点
- "切换节点"
- "换个节点"
- "切换代理"

## 功能说明

1. **进程控制** - 启动/关闭 Clash for Windows 进程
2. **API 控制** - 通过 REST API 控制代理开关
3. **节点管理** - 切换代理节点（自动选择、故障转移等）
4. **状态查询** - 查看当前代理状态和选中的节点

## 示例对话

- 用户：帮我开一下代理
- AI：✅ 已开启代理（自动选择）

- 用户： Clash 状态怎么样？
- AI：🟢 运行中，当前节点：🇸🇬 SG 02

## 注意事项

1. 首次使用需要在 Clash 设置中开启 "External Controller"
2. 确保系统代理已配置为 127.0.0.1:61225
3. 可以通过 `netsh winhttp show proxy` 查看系统代理状态

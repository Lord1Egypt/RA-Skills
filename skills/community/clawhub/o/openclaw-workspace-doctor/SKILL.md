---
name: openclaw-workspace-doctor
displayName: OpenClaw工作目录医生
description: 检测并修复OpenClaw工作目录嵌套问题
version: 1.0.0
type: skill
tags: [openclaw, workspace, health, directory, nested, doctor]
release: published
---

检测并修复OpenClaw工作目录嵌套问题。

## 触发条件

用户提到以下任意关键词时激活：
- 工作目录异常
- 嵌套目录
- .openclawworkspace
- workspace问题
- 路径错误
- openclaw doctor
- openclaw init
- 工作目录健康
- 工作目录医生

## 功能

### 1. 检测嵌套目录
扫描 `.openclawworkspace` 递归嵌套目录

### 2. 校验工作目录
- 检查配置文件中的工作目录
- 检查当前工作目录
- 验证路径有效性

### 3. 修复功能（需用户确认）
- 删除嵌套目录
- 修复配置文件中的工作目录路径
- 支持演练模式（DryRun）

## 使用方法

### 方式一：在线使用（推荐）

1. 访问 GitHub 仓库获取脚本：
   https://github.com/maxkandel99-arch/workspace-health

2. 下载 scripts 目录下的脚本：
   - detect-nested-workspace.ps1
   - validate-workspace.ps1  
   - fix-nested-workspace.ps1

3. 运行检测：
```powershell
.\detect-nested-workspace.ps1
.\validate-workspace.ps1
.\fix-nested-workspace.ps1 -DryRun:$true  # 演练模式
```

### 方式二：直接询问

直接告诉AI你的问题，如：
- "我的OpenClaw工作目录好像出问题了"
- "检测一下工作目录健康"

AI会引导你完成诊断和修复。

## 安全说明

- 修复操作前默认使用演练模式
- 删除操作前会提示用户确认
- 建议修复前备份配置文件
- 修复后需要重启OpenClaw Gateway

## 常见问题

**Q: 什么是嵌套目录？**
A: 当OpenClaw的工作目录路径指向另一层workspace时，会形成嵌套，可能导致配置读取错误。

**Q: 如何判断是否需要修复？**
A: 运行 validate-workspace.ps1 脚本，它会检测并报告问题。

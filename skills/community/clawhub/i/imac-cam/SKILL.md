---
name: imac-cam
description: 捕获 iMac 摄像头画面（Photo Booth 窗口）。当用户想查看 iMac 的摄像头、打开摄像头、查看摄像头、打开监控、查看监控时说。
---

# imac-cam 技能

捕获黄哥 iMac 的摄像头画面（Photo Booth 窗口），自动去除边框并关闭 Photo Booth。

## 使用方法

触发词：`打开摄像头`、`查看摄像头`、`监控`

## 实现

1. 检查 Photo Booth 是否运行，未运行则启动
2. 使用 AppleScript 动态获取窗口位置
3. 精确裁剪：去除上下边框（上方28px，下方60px）
4. 启动 HTTP 服务器供查看（端口 8765）
5. 截图完成后自动关闭 Photo Booth

## 窗口裁剪参数

- 上边框：28px
- 下边框：60px

## 依赖

- macOS 内置工具：screencapture, python3
- Photo Booth 应用

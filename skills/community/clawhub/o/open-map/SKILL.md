---
name: open-map
version: 0.1.0
description: 打开系统地图应用并进行导航。
author: wangxiaoyu
---

# open-map Skill

## 简介
`open-map` 用于在 macOS 上打开 Apple Maps（或其他已注册的地图协议）并直接启动导航。

## 使用方法
在对话中发送指令，例如：
```
打开地图 前往 北京 天安门
```
或者指定坐标：
```
打开地图 坐标 39.908722,116.397499
```

## 实现原理
Skill 通过 `exec` 调用系统的 `open` 命令，使用 Apple Maps URL Scheme：
- 地址导航：`http://maps.apple.com/?daddr=北京+天安门`
- 坐标导航：`http://maps.apple.com/?daddr=39.908722,116.397499`

## Action 定义
```json
{
  "action": "open-map",
  "description": "打开地图并导航",
  "parameters": {
    "type": "object",
    "properties": {
      "target": {
        "type": "string",
        "description": "目的地地址或坐标（纬度,经度）"
      }
    },
    "required": ["target"]
  }
}
```

## Execution 示例
```bash
open "http://maps.apple.com/?daddr=北京+天安门"
```
或
```bash
open "http://maps.apple.com/?daddr=39.908722,116.397499"
```

## 注意事项
- 需要系统能够访问 `open` 命令（macOS 默认可用）。
- 若需使用其他地图服务，可自行修改 URL Scheme（如 `https://www.google.com/maps/dir/?api=1&destination=`）。
- 本 Skill 仅在本机拥有 GUI 桌面会话时有效。
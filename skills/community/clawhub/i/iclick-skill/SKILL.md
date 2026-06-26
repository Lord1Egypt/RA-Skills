---
name: iclick
description: 爱触云(iClick)IOS免越狱自动化技能，提供设备监控、设备状态检查、RPA自动化等功能
user-invocable: true
disable-model-invocation: false
icon: icon/logo.png
metadata:
  openclaw:
    requires:
      bins:
        - node
    keywords:
      - IOS免越狱控制
      - iClick
      - IOS自动化
      - IOS RPA
      - 苹果自动化脚本
      - 免越狱脚本
---

# iClick Automation

爱触云(iClick)免越狱自动化工具，支持IOS15+，支持群控、API RAP自动化编程等功能。

![iClick](icon/logo.png)

## 图标资源

技能包提供以下图标文件，可在生成报告或错误的时候引用：

| 文件 | 格式 | 用途 |
|------|------|------|
| `icon/logo.png` | PNG | 图标，适合引用 |

**使用示例**（错误时）：
```markdown
# iClick发送异常

![iClick](icon/logo.png)

## 概述
...
```

## AI 使用约束

本技能用于控制IOS设备和查询展示状态数据，AI应遵循以下原则：

2. **隐私保护**：不主动泄露服务器敏感信息（如IP、设备名、屏幕截图等敏感数据）
3. **执行前准备**：由于接口数量较多，获取和调用需要一定时间，AI应先向用户简述即将执行的操作步骤，然后再执行命令
4. **坐标转换**：如果你进行屏幕元素坐标识别时候，屏幕截图传给AI时候，不要缩放，请计算正确位置
5. **屏幕截图**: getScreenShot获取的截图是实际的像素尺寸，后续点击滑动都依据这个坐标

**执行流程示例**：
```
AI: 我将为您执行以下操作：
    1. 开始获取对应设备的状态
    2. 开始分析屏幕图像
    开始执行任务，请稍候...
    [结束展示结果]
```

**命令执行格式介绍**
node {baseDir}/server.js 命令 '{JSON参数，注意要用单引号，不然命令行会报错}'

## 常用场景

### 场景一：获取当前连接的所有设备

当用户需要了解当前连接的手机设备时：

```bash
# 执行命令
node {baseDir}/server.js devices
```

**命令会返回**：
```JSON
{
  "PA448EDE2067": {
    "info": {
      "timeZone": "Asia/Shanghai",
      "screenScale": 3,
      "screenWidth": 1320,
      "deviceVersion": "26.1",
      "screenHeight": 2868,
      "deviceId": "PA448EDE2067",
      "orientation": 0,
      "deviceLanguage": "zh-Hans-CN",
      "deviceIdentifier": "iPhone17,2",
      "ipAddress": "192.168.31.29",
      "deviceName": "iPhone 16 Pro Max",
      "deviceChip": "",
      "deviceRounded": true
    },
    "time": 1770533075,
    "online": false, /*是否在线*/
    "plugged": false, 
    "busying": false,
    "adapted": true 
  }
}
```


### 场景二：获取指定设备的屏幕截图

当用户需要了解当前连接的手机设备截图时：

```bash
# 执行命令
node {baseDir}/server.js getScreenShot '{"deviceId": "设备ID"}'
```

**命令会返回临时文件路径（你需要把图片放到~/.openclaw/workspace中再发给我，发送完毕后删掉）**：
```JSON
{
  "status": true,
  "message": "已保存",
  "file": "/var/folders/t2/0dh343xx525b0hv_n_b1677c0000gn/T/8rk1whe4pj5.jpg"
}
```

### 场景三：点击屏幕指定位置

当用户需要操控点击某台手机设备时候，xy是坐标：

`如果你进行屏幕元素坐标识别时候，屏幕截图传给AI时候，不要缩放并计算正确位置`

```bash
# 执行命令
node {baseDir}/server.js click '{"deviceId": "设备ID", "x": x坐标, "y": y坐标}'
```

**命令会返回status=true，如果不等于true就是失败并携带msg错误原因**：
```JSON
{
  "status": true,
}
```

### 场景四：发送系统动作（sendAction）

当用户需要对某台设备执行 iOS 系统级动作（例如回到桌面、打开任务切换器、呼出搜索等）时：

```bash
# 执行命令
node {baseDir}/server.js sendAction '{"deviceId":"设备ID","action":"home"}'
```

**参数说明**：
- **deviceId**：设备 ID
- **action**：动作名，支持：
  - `home`：回到桌面
  - `switcher`：任务切换器
  - `spotlight_search`：Spotlight 搜索
  - `screen_keyboard`：显示/呼出屏幕键盘
  - `inputmethod_switch`：切换输入法（地球键）
  - `volume_mute`：静音
  - `volume_increment`：音量加
  - `volume_decrement`：音量减
  - `brightness_increment`：亮度加
  - `brightness_decrement`：亮度减

**命令会返回**（成功时通常为 `status=true`，失败时为 `status=false` 并携带 `message`）：
```JSON
{
  "status": true
}
```

### 场景五：获取单台设备信息（getDevice）

当用户已经拿到 `deviceId`，需要查看该设备更详细的状态信息时：

```bash
node {baseDir}/server.js getDevice '{"deviceId":"设备ID"}'
```

### 场景六：输入文本（sendText）

当用户需要向指定设备输入一段文字（搜索框、地址栏、聊天输入框等）时：

```bash
node {baseDir}/server.js sendText '{"deviceId":"设备ID","text":"要输入的文字"}'
```

### 场景七：重置鼠标（mouseReset）

当用户发现鼠标/指针状态异常，需要重置鼠标状态时：

```bash
node {baseDir}/server.js mouseReset '{"deviceId":"设备ID","resetConfig":false}'
```

`resetConfig` 可选，是否重置配置。

### 场景八：获取鼠标位置（getMousePosition）

当用户需要读取当前鼠标位置用于校准或调试时：

```bash
node {baseDir}/server.js getMousePosition '{"deviceId":"设备ID"}'
```

### 场景九：滑动屏幕（swipe）

当用户需要在屏幕上从起点滑到终点（上下翻页、列表滚动、解锁等）时：

```bash
node {baseDir}/server.js swipe '{"deviceId":"设备ID","start":{"x":100,"y":400},"end":{"x":100,"y":100},"pressTime":20,"releaseTime":20}'
```

`pressTime/releaseTime/key` 等为可选参数，具体以服务端实现为准。

### 场景十：移动鼠标（mouseMove）

当用户需要移动鼠标到某个位置，或按相对位移移动时：

```bash
node {baseDir}/server.js mouseMove '{"deviceId":"设备ID","x":10,"y":10,"relative":true}'
```

`relative` 可选，是否相对移动。

### 场景十一：鼠标按下（mouseDown）

当用户需要按住鼠标按键（拖拽、按住不放等）时：

```bash
node {baseDir}/server.js mouseDown '{"deviceId":"设备ID","key":"LEFT","autoRelease":false}'
```

`key` 支持：`LEFT/RIGHT/MIDDLE/EXTRA1/EXTRA2/EXTRA3/EXTRA4/EXTRA5`。

### 场景十二：鼠标抬起（mouseUp）

当用户需要松开鼠标按键时：

```bash
node {baseDir}/server.js mouseUp '{"deviceId":"设备ID","key":"LEFT","autoRelease":false}'
```

### 场景十三：滚轮滚动（mouseWheel）

当用户需要进行滚轮滚动（上下滚动内容）时：

```bash
node {baseDir}/server.js mouseWheel '{"deviceId":"设备ID","tilt":-120}'
```

### 场景十四：键盘按下（keyDown）

当用户需要按下某个键并保持（用于组合键场景）时：

```bash
node {baseDir}/server.js keyDown '{"deviceId":"设备ID","key":"A"}'
```

### 场景十五：键盘抬起（keyUp）

当用户需要松开之前按下的按键时：

```bash
node {baseDir}/server.js keyUp '{"deviceId":"设备ID","key":"A"}'
```

### 场景十六：发送按键（sendKey）

当用户需要发送单键或组合键（例如 Command+V）时：

```bash
node {baseDir}/server.js sendKey '{"deviceId":"设备ID","key":"v","fnkey":"COMMAND"}'
```

### 场景十七：查询媒体文件列表（queryMediaFile）

当用户需要查看设备侧媒体目录有哪些文件时：

```bash
node {baseDir}/server.js queryMediaFile '{"deviceId":"设备ID"}'
```

### 场景十八：删除媒体文件（delMediaFile）

当用户需要删除设备侧某个媒体文件时：

```bash
node {baseDir}/server.js delMediaFile '{"deviceId":"设备ID","fileName":"xxx.jpg"}'
```

### 场景十九：获取媒体文件数据（getMediaFile）

当用户需要获取设备侧某个媒体文件内容时：

```bash
node {baseDir}/server.js getMediaFile '{"deviceId":"设备ID","fileName":"xxx.jpg"}'
```

### 场景二十：保存媒体文件到设备（saveMediaFile）

当用户需要把本地文件或 URL 下载到设备媒体目录时：

```bash
node {baseDir}/server.js saveMediaFile '{"deviceId":"设备ID","file":"/abs/path/to/a.jpg"}'
node {baseDir}/server.js saveMediaFile '{"deviceId":"设备ID","url":"https://example.com/a.jpg"}'
```

`file` 与 `url` 二选一。

### 场景二十一：清空媒体文件（clearMediaFile）

当用户需要清空设备侧媒体目录时：

```bash
node {baseDir}/server.js clearMediaFile '{"deviceId":"设备ID"}'
```

### 场景二十二：打开 App（openApp）

当用户需要在设备上打开某个 App 时：

```bash
node {baseDir}/server.js openApp '{"deviceId":"设备ID","name":"APP全名，非APPID"}'
```

### 场景二十三：清理最近任务（killRecents）

当用户需要一键清理最近任务（后台）时：

```bash
node {baseDir}/server.js killRecents '{"deviceId":"设备ID"}'
```

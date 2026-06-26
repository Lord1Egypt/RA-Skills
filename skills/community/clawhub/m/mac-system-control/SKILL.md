---
name: mac-system-control
description: >-
  管理和控制 macOS 系统功能。包括查看系统信息、管理进程、控制音量/亮度、
  网络管理、电源管理、截图、剪贴板、Finder 操作等。当用户要求查看系统状态、
  控制系统设置、管理进程、截图、调节音量亮度、查看网络信息、
  关机重启睡眠等 Mac 系统操作时使用。
---

# Mac System Control

## 系统信息

```bash
# 系统概览
system_profiler SPSoftwareDataType SPHardwareDataType

# CPU 使用率
top -l 1 -n 0 | head -10

# 内存使用
vm_stat | head -6

# 磁盘空间
df -h /

# 电池状态（笔记本）
pmset -g batt

# macOS 版本
sw_vers
```

## 进程管理

```bash
# 按 CPU 排序前 10 进程
ps aux --sort=-%cpu | head -11

# 按内存排序前 10 进程
ps aux --sort=-%mem | head -11

# 查找进程
pgrep -fl "<关键词>"

# 杀掉进程（先确认再操作）
kill <PID>
killall "<进程名>"
```

操作前务必向用户确认目标进程，避免误杀。

## 音量与亮度

```bash
# 查看当前音量（0-100）
osascript -e 'output volume of (get volume settings)'

# 设置音量
osascript -e 'set volume output volume <0-100>'

# 静音/取消静音
osascript -e 'set volume output muted true'
osascript -e 'set volume output muted false'

# 调节亮度（需要 brightness 命令，brew install brightness）
brightness <0.0-1.0>
```

## 网络

```bash
# 当前 Wi-Fi 名称
networksetup -getairportnetwork en0

# IP 地址
ipconfig getifaddr en0

# 公网 IP
curl -s ifconfig.me

# DNS 设置
networksetup -getdnsservers Wi-Fi

# 网络连通性测试
ping -c 3 <host>

# 列出 Wi-Fi 网络
/System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport -s

# 开关 Wi-Fi
networksetup -setairportpower en0 off
networksetup -setairportpower en0 on
```

## 电源管理

```bash
# 睡眠
pmset sleepnow

# 关机（需确认）
sudo shutdown -h now

# 重启（需确认）
sudo shutdown -r now

# 锁屏
pmset displaysleepnow

# 防止休眠（保持唤醒）
caffeinate -d -t <秒数>
```

关机和重启操作必须先向用户确认。

## 截图

```bash
# 全屏截图保存到桌面
screencapture ~/Desktop/screenshot.png

# 指定区域截图（交互式）
screencapture -i ~/Desktop/screenshot.png

# 窗口截图（交互式选择窗口）
screencapture -w ~/Desktop/screenshot.png

# 截图到剪贴板
screencapture -c
```

## 剪贴板

```bash
# 读取剪贴板文本
pbpaste

# 写入文本到剪贴板
echo "内容" | pbcopy

# 将文件内容复制到剪贴板
pbcopy < /path/to/file
```

## Finder 操作

```bash
# 在 Finder 中打开目录
open /path/to/directory

# 在 Finder 中显示文件
open -R /path/to/file

# 清空废纸篓
osascript -e 'tell application "Finder" to empty trash'

# 显示/隐藏隐藏文件
defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder
defaults write com.apple.finder AppleShowAllFiles -bool false && killall Finder
```

## 系统设置快捷方式

```bash
# 打开系统设置（Ventura+）
open "x-apple.systempreferences:"

# 打开特定设置面板
open "x-apple.systempreferences:com.apple.Network-Settings.extension"
open "x-apple.systempreferences:com.apple.Sound-Settings.extension"
open "x-apple.systempreferences:com.apple.Bluetooth-Settings.extension"
open "x-apple.systempreferences:com.apple.Display-Settings.extension"
```

## 工作流

1. 用户描述要执行的系统操作
2. 判断属于哪个类别（信息查询 / 设置调整 / 进程管理等）
3. 信息查询类直接执行并展示结果
4. 破坏性操作（关机、重启、杀进程、清空废纸篓）先向用户确认
5. 需要 `sudo` 的命令提前告知用户

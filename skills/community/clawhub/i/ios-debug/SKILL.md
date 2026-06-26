---
name: ios-debug
description: >
  调试 iPhone 14 真机上的 iOS App。
  获取 App 实时日志（stdout）、截取 iPhone 屏幕（通过 QuickTime 镜像）、
  构建安装启动 App、查看设备状态。
  当用户提到 iPhone 调试、iOS 日志、手机截图时使用。
metadata:
  version: 0.2.0
  author: kiro
  display_name: "iOS 真机调试"
  tags:
    - ios
    - iphone
    - debug
    - screenshot
    - log
---

# iOS 真机调试 Skill

## 设备信息

真机: iPhone14

| 工具 | 设备 ID | 用途 |
|-----|---------|------|
| Xcode devicectl | `9B6F9009-7150-53F5-93D0-8CF3C1884F83` | 构建、安装、启动 |
| libimobiledevice (idevice_id) | `00008110-000965E63E50201E` | 日志查看、文件传输 |

**注意**: 两套工具使用不同的设备标识符格式，不能混用！

## 获取 App 实时日志

### 方法：devicectl --console（推荐）

App 里的 `print()` 输出会实时显示在 stdout：

```bash
xcrun devicectl device process launch \
  --device 9B6F9009-7150-53F5-93D0-8CF3C1884F83 \
  --terminate-existing --console \
  <bundle_id>
```

注意：
- 这是阻塞命令，用 `control_bash_process` 后台启动
- App 里必须用 `print()` 而不是 `Logger`（os.log 不走 stdout）
- 退出时 kill 进程即可

### 方法：idevicesyslog（系统日志，App 内部日志通常抓不到）

```bash
idevicesyslog -u 00008110-000965E63E50201E 2>&1 | grep -i "<关键词>"
```

只能看到系统级日志（bluetoothd、SpringBoard 等），App 的 `Logger` / `print()` 通常不出现。

## 获取 iPhone 屏幕截图

### 前置：QuickTime Player 正在镜像 iPhone

用户需要先打开 QuickTime Player → File → New Movie Recording → 选择 iPhone 14 作为摄像头源。
这样 QuickTime 窗口就是 iPhone 的实时镜像。

### 截图命令

```bash
screencapture -l $(osascript -e 'tell application "QuickTime Player" to get id of window 1') /tmp/iphone_mirror.png
```

截图保存到 `/tmp/iphone_mirror.png`，可以用浏览器或 Preview 查看。

### 注意事项
- QuickTime 必须正在运行且有 iPhone 镜像窗口
- 如果有多个 QuickTime 窗口，`window 1` 可能不是 iPhone 的，需要调整
- 截图分辨率取决于 QuickTime 窗口大小

## 构建 & 安装 & 启动

```bash
# 1. 构建（替换 <project> <scheme> 为实际值）
xcodebuild -project <project>.xcodeproj -scheme <scheme> -configuration Debug \
  -destination 'id=9B6F9009-7150-53F5-93D0-8CF3C1884F83' \
  -allowProvisioningUpdates build

# 2. 找到构建产物
APP_PATH=$(find ~/Library/Developer/Xcode/DerivedData/<project>-* \
  -name "<app_name>.app" -path "*/Build/Products/Debug-iphoneos/*" \
  -not -path "*/Index.noindex/*" -type d 2>/dev/null | sort -r | head -1)

# 3. 安装到真机
xcrun devicectl device install app \
  --device 9B6F9009-7150-53F5-93D0-8CF3C1884F83 "$APP_PATH"

# 4. 启动（普通）
xcrun devicectl device process launch \
  --device 9B6F9009-7150-53F5-93D0-8CF3C1884F83 \
  --terminate-existing <bundle_id>

# 4b. 启动（带 console 日志）
xcrun devicectl device process launch \
  --device 9B6F9009-7150-53F5-93D0-8CF3C1884F83 \
  --terminate-existing --console <bundle_id>
```

## 设备状态检查

```bash
# 设备是否连接
xcrun devicectl list devices 2>&1 | grep iPhone

# 卸载 App（签名冲突时用）
xcrun devicectl device uninstall app \
  --device 9B6F9009-7150-53F5-93D0-8CF3C1884F83 <bundle_id>
```

## 签名问题处理

如果安装后启动报 "invalid code signature" 或 "profile has not been explicitly trusted"：
1. iPhone 上：设置 → 通用 → VPN与设备管理 → 信任开发者证书
2. 或者先卸载再重装

## 踩坑记录

### ❌ idevicesyslog 看不到 App 日志
iOS 的 os.log 不转发到 syslog。只有 `print()` + `--console` 模式能看到。

### ❌ devicectl --console 启动后 App 被杀
`--console` 模式下如果 terminal 进程被 kill，App 也会被终止。用 `control_bash_process` 后台运行。

### ❌ QuickTime 截图是黑屏
可能 iPhone 锁屏了，或者 QuickTime 窗口最小化了。确保 iPhone 亮屏且 QuickTime 窗口可见。

### ❌ 设备 unavailable
iPhone 锁屏或 USB 断开。解锁 iPhone 屏幕，等几秒再试。

### ❌ 签名不匹配
先卸载旧 App 再安装：
```bash
xcrun devicectl device uninstall app --device 9B6F9009-7150-53F5-93D0-8CF3C1884F83 <bundle_id>
```

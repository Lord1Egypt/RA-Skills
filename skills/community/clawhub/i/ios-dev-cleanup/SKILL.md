---
name: ios-dev-cleanup
description: Use when checking iOS development disk usage or cleaning up simulators, runtimes, device support, derived data, CocoaPods cache, archives, or other build artifacts — scans each category, shows top 5 by size with last-used info, and offers safe deletion commands
version: 1.0.0
tags: ios, xcode, cleanup, simulator, disk-space, macos
author: Jesse Luo <radishchrist@gmail.com>
requires_binaries: xcrun, du, stat
---

# iOS 开发磁盘清理

扫描 iOS 开发相关的磁盘占用，按类别汇总，每类展示最大的 5 项及最近使用时间，供用户选择删除。

## 执行流程

**依次扫描以下 8 个类别**，每类输出汇总大小 + Top 5 明细表。全部扫描完后，汇总输出总表供用户决策。

### 1. Simulator Runtimes（模拟器系统镜像）~10-55GB

两个存储位置，都需要检查：

```bash
# 列出已注册的 runtime 及状态
xcrun simctl runtime list

# MobileAsset 位置（macOS 自动下载，含孤立残留）
du -sh /System/Library/AssetsV2/com_apple_MobileAsset_iOSSimulatorRuntime/*/ 2>/dev/null | sort -rh | head -5

# Xcode 下载位置（cryptexes 磁盘镜像）
du -sh /Library/Developer/CoreSimulator/Volumes/* 2>/dev/null | sort -rh | head -5
du -sh /Library/Developer/CoreSimulator/Profiles/Runtimes/* 2>/dev/null | sort -rh | head -5
```

**删除命令**：
```bash
xcrun simctl runtime delete 'iOS XX.X'
```

**注意**：`/System/` 下的 asset 受 SIP 保护，`simctl runtime delete` 可能无法清理孤立 asset。

### 2. Simulator Devices（模拟器设备数据）~1-10GB

```bash
# 列出所有设备（含 unavailable）
xcrun simctl list devices

# 各设备数据目录大小（Top 5）
du -sh ~/Library/Developer/CoreSimulator/Devices/*/data/ 2>/dev/null | sort -rh | head -5
# 对应 UUID 查设备名
# xcrun simctl list devices | grep <UUID前8位>
```

**删除命令**：
```bash
# 重置单个设备（清数据，保留设备）
xcrun simctl erase <UUID>

# 删除单个设备
xcrun simctl delete <UUID>

# 批量删除所有 unavailable 设备
xcrun simctl delete unavailable
```

**禁止** 直接 `rm -rf ~/Library/Developer/CoreSimulator/Devices/<UUID>/`，必须用 `simctl delete`。

### 3. CocoaPods 缓存 ~5-15GB

```bash
# 总大小
du -sh ~/Library/Caches/CocoaPods/ 2>/dev/null

# 各 Pod 缓存大小（Top 5）
du -sh ~/Library/Caches/CocoaPods/Pods/*/ 2>/dev/null | sort -rh | head -5
```

**删除命令**：
```bash
# 清理全部缓存（下次 pod install 会重新下载）
pod cache clean --all

# 或直接删除
rm -rf ~/Library/Caches/CocoaPods/
```

### 4. iOS DeviceSupport（真机调试符号）~3-10GB

```bash
# 每个 iOS 版本的符号文件大小 + 最近访问时间
for dir in ~/Library/Developer/Xcode/iOS\ DeviceSupport/*/; do
  size=$(du -sh "$dir" 2>/dev/null | cut -f1)
  atime=$(stat -f '%Sa' -t '%Y-%m-%d' "$dir" 2>/dev/null)
  name=$(basename "$dir")
  echo "$size|$atime|$name"
done | sort -t'|' -k1 -rh | head -5 | column -t -s'|'
```

展示时标注 iOS 版本号，用户可根据不再使用的版本决定删除。删除后连接对应版本真机会重新下载符号。

**删除命令**：
```bash
rm -rf ~/Library/Developer/Xcode/iOS\ DeviceSupport/<版本目录>
```

### 5. DerivedData（编译缓存）~2-20GB

```bash
# 各项目大小 + 最近修改时间
for dir in ~/Library/Developer/Xcode/DerivedData/*/; do
  size=$(du -sh "$dir" 2>/dev/null | cut -f1)
  mtime=$(stat -f '%Sm' -t '%Y-%m-%d' "$dir" 2>/dev/null)
  name=$(basename "$dir")
  echo "$size|$mtime|$name"
done | sort -t'|' -k1 -rh | head -5 | column -t -s'|'
```

全部可安全删除，下次编译自动重建（会增加首次编译时间）。

**删除命令**：
```bash
# 删除单个项目缓存
rm -rf ~/Library/Developer/Xcode/DerivedData/<项目名>/

# 清空全部
rm -rf ~/Library/Developer/Xcode/DerivedData/*
```

### 6. Archives（归档包）~0-10GB

```bash
# 各归档大小 + 日期
du -sh ~/Library/Developer/Xcode/Archives/*/*/ 2>/dev/null | sort -rh | head -5
```

已上传到 App Store 的可安全删除，未上传的需确认。

**删除命令**：
```bash
rm -rf ~/Library/Developer/Xcode/Archives/<日期>/<归档名>.xcarchive
```

### 7. SPM 缓存（Swift Package Manager）~0-2GB

```bash
du -sh ~/Library/Caches/org.swift.swiftpm/ 2>/dev/null
du -sh ~/Library/Developer/Xcode/DerivedData/*/SourcePackages/ 2>/dev/null | sort -rh | head -5
```

**删除命令**：
```bash
rm -rf ~/Library/Caches/org.swift.swiftpm/
```

### 8. Caches & Logs（其他缓存和日志）

```bash
# CoreSimulator 缓存
du -sh ~/Library/Developer/CoreSimulator/Caches/ 2>/dev/null

# Xcode 日志和历史
du -sh ~/Library/Developer/Xcode/UserData/IDB/ 2>/dev/null
du -sh ~/Library/Developer/Xcode/UserData/IDEEditorInteractivityHistory/ 2>/dev/null

# SwiftUI Previews 缓存
du -sh ~/Library/Developer/Xcode/UserData/Previews/ 2>/dev/null

# Documentation 缓存
du -sh ~/Library/Developer/Xcode/DocumentationCache/ 2>/dev/null

# Xcode 缓存
du -sh ~/Library/Caches/com.apple.dt.Xcode/ 2>/dev/null
```

**删除命令**：
```bash
rm -rf ~/Library/Developer/CoreSimulator/Caches/*
rm -rf ~/Library/Developer/Xcode/UserData/IDB/*
rm -rf ~/Library/Developer/Xcode/DocumentationCache/*
rm -rf ~/Library/Caches/com.apple.dt.Xcode/*
```

## Unavailable 自动清理

扫描阶段发现以下 unavailable 项时，**直接执行清理**（无需用户确认，因为 unavailable 项已无法使用）：

```bash
# 1. 删除所有 unavailable 模拟器设备（runtime 已卸载的残留设备）
xcrun simctl delete unavailable

# 2. 删除 unavailable runtime（已注册但磁盘镜像缺失的 runtime）
# 先检查是否有 unavailable runtime
xcrun simctl runtime list | grep -i "unavailable\|not available"
# 如果有，逐个删除
xcrun simctl runtime delete <identifier>
```

清理完 unavailable 后再进入汇总扫描流程。

## 输出格式

### 第一步：扫描 + 汇总表

扫描完成后，输出汇总表：

```
| #  | 类别                | 总大小  | 可安全清理 | 建议 |
|----|---------------------|---------|-----------|------|
| 1  | Simulator Runtimes  | XX GB   | XX GB     | ...  |
| 2  | Simulator Devices   | XX GB   | XX GB     | ...  |
| 3  | CocoaPods Cache     | XX GB   | 全部      | ...  |
| 4  | iOS DeviceSupport   | XX GB   | XX GB     | ...  |
| 5  | DerivedData         | XX GB   | 全部      | ...  |
| 6  | Archives            | XX GB   | XX GB     | ...  |
| 7  | SPM Cache           | XX GB   | 全部      | ...  |
| 8  | Caches & Logs       | XX GB   | 全部      | ...  |
|    | **合计**            | **XX GB** |         |      |
```

然后逐类列出 Top 5 明细，等用户选择要清理的类别。

### 第二步：执行清理 + 汇报效果

用户确认后执行清理。**清理完成后必须汇报效果**：

```
| 类别              | 清理前  | 清理后  | 释放空间 |
|-------------------|---------|---------|---------|
| Unavailable 设备  | XX GB   | -       | XX GB   |
| CocoaPods Cache   | XX GB   | 0 B     | XX GB   |
| ...               | ...     | ...     | ...     |
| **合计释放**      |         |         | **XX GB** |
```

## 删除方式安全规则

以下类别**必须使用专有命令**删除，禁止 `rm -rf`：

| 类别 | 必须使用的命令 | 禁止操作 |
|------|---------------|---------|
| Simulator Devices | `xcrun simctl delete <UUID>` | `rm -rf ~/Library/Developer/CoreSimulator/Devices/<UUID>/` |
| Simulator Runtimes | `xcrun simctl runtime delete 'iOS XX.X'` | `rm -rf /Library/Developer/CoreSimulator/...` |
| CocoaPods Cache | `pod cache clean --all` 或 `rm -rf ~/Library/Caches/CocoaPods/` | 两种均可 |

其他类别（DerivedData / DeviceSupport / Archives / SPM Cache / Caches & Logs）可安全使用 `rm -rf`，但**必须等用户确认后再执行**。

## 其他注意事项

- DerivedData / CocoaPods Cache / SPM Cache 全部可安全删除，代价是下次编译/install 变慢
- iOS DeviceSupport 删除后连接对应版本真机会自动重新下载，耗时几分钟
- Archives 未上传到 App Store 的需确认后再删
- Simulator Runtimes 的 `/System/` 路径受 SIP 保护，需提示用户

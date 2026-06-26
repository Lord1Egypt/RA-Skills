# macOS 权限配置指南

> **重要**: 本技能需要 macOS 权限才能正常工作

---

## 🔐 需要的权限

### 1. 辅助功能（Accessibility）

**用途**: 控制鼠标、键盘、应用自动化

**配置步骤**:
1. 打开「系统设置」→「隐私与安全性」→「辅助功能」
2. 点击「+」添加应用
3. 添加「终端」应用（或你使用的终端）
4. 勾选添加的应用
5. **重启终端应用**

**快速打开**:
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
```

---

### 2. 自动化（AppleEvents）

**用途**: AppleScript 控制其他应用

**配置步骤**:
1. 打开「系统设置」→「隐私与安全性」→「自动化」
2. 找到「终端」或「osascript」
3. 勾选要控制的应用（如 Finder、Safari 等）
4. **重启终端应用**

**快速打开**:
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Automation"
```

---

### 3. 屏幕录制（ScreenCapture）

**用途**: 截屏功能

**配置步骤**:
1. 打开「系统设置」→「隐私与安全性」→「屏幕录制」
2. 勾选「终端」应用
3. **重启终端应用**

**快速打开**:
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"
```

---

### 4. 完全磁盘访问（Full Disk Access）

**用途**: 访问受保护的目录（文档、下载等）

**配置步骤**:
1. 打开「系统设置」→「隐私与安全性」→「完全磁盘访问」
2. 点击「+」添加「终端」
3. 勾选「终端」
4. **重启终端应用**

**快速打开**:
```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_AllFiles"
```

---

## ✅ 权限检测

运行检测脚本：
```bash
bash scripts/check_permissions.sh
```

---

## ⚠️ 常见问题

### Q1: 授予权限后仍然报错

**原因**: 权限未生效

**解决**: 
1. 完全退出终端（Cmd+Q）
2. 重新打开终端
3. 再次运行脚本

---

### Q2: macOS 更新后权限丢失

**原因**: 系统更新重置了权限

**解决**: 
1. 重新运行权限检测脚本
2. 重新授予权限
3. 重启终端

---

### Q3: 多个终端应用

如果你使用多个终端应用（Terminal、iTerm2 等），需要为每个应用单独授权。

---

## 📚 相关资源

- Apple 官方文档：https://support.apple.com/guide/mac-help/privacy-and-security-mh15209/mac
- tccutil 命令：管理 TCC（隐私控制）数据库

---

**最后更新**: 2026-03-31

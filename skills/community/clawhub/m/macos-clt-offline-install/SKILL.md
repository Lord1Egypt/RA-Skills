---
name: macos-clt-offline-install
description: 解决 macOS 上 Xcode Command Line Tools 安装失败的问题（"不能下载该软件，因为网络出了问题"、xcode-select --install 弹窗下载失败、softwareupdate 网络错误、git 命令报错要求安装开发者工具）。当用户在国内网络环境下安装命令行工具失败、或需要离线/手动安装 CLT 时使用。核心方法：从苹果官方 sucatalog 更新目录解析免登录 CDN 直链（swcdn.apple.com），用代理下载 pkg 后手动安装。
agent_created: true
---

# macOS Command Line Tools 离线安装

## Overview

macOS 弹窗安装 Xcode Command Line Tools (CLT) 时报「不能下载该软件，因为网络出了问题」，根因通常是：**GUI 安装器和 `softwareupdate` 命令不走终端代理，且直连苹果更新 CDN（updates.cdn-apple.com）在国内经常不通**。本 skill 提供绕过方案：解析苹果公开的系统更新目录 (sucatalog)，拿到 `swcdn.apple.com` 的免登录直链，用终端（可走代理）下载 pkg 安装包，手动安装。

## 触发场景

- `git` 等命令触发弹窗「xcode-select: note: No developer tools were found...」，点击安装后下载失败
- 弹窗报「不能下载该软件，因为网络出了问题」
- `xcode-select --install` 或 `softwareupdate --list` 报网络错误
- 用户明确要求离线安装 / 手动安装 Command Line Tools

## Workflow

### Step 1: 诊断确认

```bash
# 系统版本（决定选哪个 CLT 版本）
sw_vers -productVersion
# 现有安装状态
xcode-select -p 2>&1
ls /Library/Developer/CommandLineTools 2>/dev/null
# 代理环境（确认终端代理是否可用）
env | grep -iE "^(http|https|all)_proxy"
scutil --proxy
```

可顺带测试连通性：`curl -sI https://swscan.apple.com`。若终端代理通而 `softwareupdate --list` 失败，即可确认是安装器不走代理的问题，直接进入 Step 2。

**版本选择参考**：macOS 15 (Sequoia) → CLT for Xcode 16.x；macOS 14 → CLT 15.x。sucatalog 中列出的最新版本即为苹果当前对该系统推送的版本，无需自行判断版本号。

### Step 2: 解析 sucatalog 获取官方直链

运行本 skill 自带脚本（会自动选择对应 macOS 版本的 sucatalog 并解析最新 CLT 产品）：

```bash
python3 <skill-dir>/scripts/find_clt_packages.py --catalog-index 15
```

输出示例：

```
# PostDate: 2026-XX-XX ... | Product: 082-41241 | 总大小约 841 MB
https://swcdn.apple.com/content/downloads/.../CLTools_Executables.pkg
https://swcdn.apple.com/content/downloads/.../CLTools_macOSLMOS_SDK.pkg
https://swcdn.apple.com/content/downloads/.../CLTools_macOSNMOS_SDK.pkg
https://swcdn.apple.com/content/downloads/.../CLTools_SwiftBackDeploy.pkg
```

关键事实（踩坑记录，勿走弯路）：

- **`download.developer.apple.com` 的 dmg 链接需要 Apple ID 登录**，直接 curl 下到的是错误页（几十 KB 的假文件），不要用。
- **swcdn.apple.com 的 sucatalog 内 pkg 直链免登录**，这是唯一可靠的公开渠道。
- sucatalog URL 必须用**完整版本链格式**（如 `index-15-14-13-12-10.16-10.15-...merged-1.sucatalog`），简写的 `index-15.sucatalog` 返回空。脚本 `CATALOG_URLS` 已内置 macOS 13/14/15 的正确地址。

### Step 3: 下载安装包

```bash
mkdir -p ~/Downloads/clt-install && cd ~/Downloads/clt-install
# 对 Step 2 输出的每个 URL：
curl -L --retry 3 -C - -o CLTools_Executables.pkg "<URL>"
```

下载后**必须验签**：

> 注意：目录可能还列出 `CLTools_macOS_SDK.pkg`、`CLTools_macOS_DevSDK_Remove_*.pkg` 等附加包。必需的只有 4 个：`CLTools_Executables.pkg`（主包）、`CLTools_macOSLMOS_SDK.pkg`、`CLTools_macOSNMOS_SDK.pkg`、`CLTools_SwiftBackDeploy.pkg`。

```bash
pkgutil --check-signature CLTools_Executables.pkg
# 正常输出: Status: signed by Software Signing / Apple Software
```

非 `signed` 状态的包一律丢弃重下。核对文件大小与 sucatalog 中的 Size 字段（主包约 680MB，共约 840MB）。

### Step 4: 生成一键安装脚本并交给用户

安装需要 sudo（智能体沙箱通常无法 sudo），生成脚本让用户自己运行：

```bash
bash <skill-dir>/scripts/make_install_sh.sh ~/Downloads/clt-install ~/Downloads/clt-install/install-clt.sh
```

告诉用户在终端运行 `~/Downloads/clt-install/install-clt.sh`，输入开机密码，等待 1~2 分钟；看到 `git --version` 输出版本号即成功。安装完成后可删除整个下载目录（约 840MB）。

## Fallback

若 sucatalog 解析失败（网络或格式变更）：

1. 尝试 `softwareupdate --list`（部分环境其实可用）
2. 从 appledb.dev / GitHub apple-db 仓库查版本号（但注意其收录的 download.developer.apple.com 链接需要登录，仅用于确认版本对应关系）
3. 指导用户临时关闭/调整代理软件的「系统代理」设置后重试官方弹窗安装

## Resources

- `scripts/find_clt_packages.py` — 解析 sucatalog，输出最新 CLT 全部 pkg 的免登录直链
- `scripts/make_install_sh.sh` — 生成带验签+安装+验证的一键安装脚本

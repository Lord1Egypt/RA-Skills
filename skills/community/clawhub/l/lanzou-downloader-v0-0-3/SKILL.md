---
name: lanzou-downloader
description: v0.0.3 | 蓝奏云（lanzouu.com/lanzou.com 等）文件下载。当用户发送蓝奏云分享链接要求下载文件时触发。自动处理 JS 反爬验证、密码验证（支持带密码的分享链接）、解析真实下载地址、完成文件下载。不适用于其他网盘（百度网盘、阿里云盘等）。
---

# 蓝奏云下载器

## 概述

蓝奏云文件分享链接通过 JS 反爬验证保护，需要先计算 `acw_sc__v2` cookie 才能访问下载页。部分链接设有提取密码，需要先提交密码验证。验证通过后，通过 AJAX 接口获取真实 CDN 下载地址。本技能使用 Node.js 脚本自动化全流程。

## 工作流程

收到蓝奏云链接后按以下步骤执行，全程使用脚本 `scripts/download.js`，一步到位：

### 步骤

1. **确认密码**：如果用户提供了密码（如"密码:1234"、"提取码abcd"），记录下来。如果链接需要密码但用户未提供，询问用户。
2. **运行下载脚本**：调用 `node /sandbox/workspace/skills/lanzou-downloader/scripts/download.js <蓝奏云链接> [输出文件路径] [密码]`
   - 密码可选：不提供时脚本自动检测是否需要密码，需要则报错提示
   - 输出文件路径可选：不提供时脚本自动从页面提取文件名
   - 脚本内部自动完成：JS 反爬 → 密码检测与提交（如需）→ 解析 iframe / AJAX 获取真实地址 → 302 跟随 → 下载
3. **验证结果**：检查脚本输出中的"下载完成"确认信息和文件大小
4. **告知用户**：报告文件名、大小和存放路径

## 脚本说明

`scripts/download.js` 是纯 Node.js 实现，无外部依赖，通过 `vm` 模块执行蓝奏云的反爬 JS 计算 `acw_sc__v2` cookie。对于密码保护的链接，自动从页面提取 `sign`、`fid`、`kdns` 参数，POST 提交密码后获取真实下载地址。最后跟随 302 重定向到 CDN 完成下载。

使用方式：
```bash
node scripts/download.js <url> [output_filepath] [password]
```

- `url`：蓝奏云分享链接（如 `https://wwapw.lanzouu.com/iO4733skvu6j`）
- `output_filepath`（可选）：输出文件路径，默认保存到 `/sandbox/workspace/` + 页面提取的文件名
- `password`（可选）：提取密码，不提供则脚本自动检测是否需要密码

## 示例

**示例 1：基本下载（无密码）**
```
用户：https://wwapw.lanzouu.com/iMtbd3td6crg 把这个文件下下来
Agent：运行 node scripts/download.js <url>
→ 下载完成：lanzou-downloader-0.0.1.zip（0.0 MB）
```

**示例 2：带密码下载**
```
用户：下载 https://wwapw.lanzouu.com/iW7UV3td6cqf 密码:1234
Agent：运行 node scripts/download.js <url> "" "1234"
→ [3/6] 检测到密码保护，提交密码...
→ 下载完成：mix-video-downloader-0.0.3.zip（0.0 MB）
```

**示例 3：指定输出路径**
```
用户：下载 https://wwapw.lanzouu.com/xxxxx 保存到 /sandbox/workspace/outputs/
Agent：运行 node scripts/download.js <url> /sandbox/workspace/outputs/project.zip
→ 下载完成
```

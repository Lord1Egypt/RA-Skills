---
name: md2png
description: 将 Markdown 文档转换为精美 PNG 图片。仅操作当前工作目录下的 Markdown 文件，不修改系统文件。当用户要求将 markdown 文件、markdown 文本转成图片、截图、png 时触发。支持多种主题（note/dark/sakura/ocean/tech 等）和尺寸（mobile/tablet/laptop/desktop）。
argument-hint: <markdown文件路径或文本> [-t 主题] [-s 尺寸] [-o 输出路径]
allowed-tools: Bash, Read, Write, Glob
---

# md2png — Markdown 转 PNG 图片

将 Markdown 内容渲染为精美的 PNG 图片，支持 10 种主题和 4 种尺寸。

## 使用方式

用户通过 `/md2png` 调用，传入参数 `$ARGUMENTS`。

## 执行步骤

1. **解析参数**：从 `$ARGUMENTS` 中识别：
   - Markdown 文件路径或直接文本内容（必填）
   - `-t` 或 `--theme`：主题名称（可选，默认 `note`）
   - `-s` 或 `--size`：尺寸规格（可选，默认 `tablet`）
   - `-o` 或 `--output`：输出文件名（可选，默认 `output.png`）

2. **参数白名单校验**（校验不通过则拒绝执行并提示用户）：
   - `theme` 必须是以下之一：`note` `vitality` `gradient` `antiquity` `classic` `dark` `minimal` `sakura` `ocean` `tech`
   - `size` 必须是以下之一：`mobile` `tablet` `laptop` `desktop`
   - `output` 文件名只允许字母、数字、连字符、下划线和 `.png` 后缀（如 `my-output.png`）
   - 若 input 为文件路径，必须是相对路径且仅限当前目录下的文件，禁止包含 `../`、`./` 以外的层级跳转及绝对路径

3. **检查输入**：
   - 如果参数是文件路径，用 Glob 或 Read 工具确认文件存在于当前目录
   - 如果参数为空，提示用户提供 Markdown 文件路径或文本

4. **检查本地安装**：执行前先确认 `md2png-cli@1.0.2` 已在本地安装：
   ```
   npx --no-install md2png-cli --version
   ```
   - 若命令失败（退出码非 0），**停止执行**，提示用户先运行以下命令安装后再重试：
     ```
     npm install -g md2png-cli@1.0.2
     ```
   - 不得跳过此检查自动联网下载

5. **执行转换**：确认本地已安装后，使用 `--no-install` 标志执行，防止运行时触发网络下载：
   ```
   npx --no-install md2png-cli <输入文件路径> -t <主题> -s <尺寸> -o <输出文件名>
   ```
   - 如果输入是文件路径，直接传入（已通过校验的相对路径）
   - 如果输入是文本内容，**禁止将原始文本直接拼接进 Bash 命令**（防止 Shell 注入）。必须先用 Write 工具将文本写入当前目录下的临时文件（如 `_md2png_tmp.md`），再将该文件路径传给命令；转换完成后用 Bash 删除该临时文件

6. **展示结果**：
   - 告知用户图片已生成及保存路径
   - 用 Read 工具读取生成的 PNG 图片，展示给用户预览

## 可用主题

| 主题 | 名称 | 风格 |
|------|------|------|
| `note` | 便签 | 暖黄便签风格，适合笔记 |
| `vitality` | 元气 | 蓝紫渐变，活泼明亮 |
| `gradient` | 渐变 | 粉绿渐变，清新自然 |
| `antiquity` | 古风 | 古典纹理，国风韵味 |
| `classic` | 经典 | 灰色背景，简约大方 |
| `dark` | 暗黑 | 深色主题，适合代码 |
| `minimal` | 极简 | 浅灰渐变，干净利落 |
| `sakura` | 樱花 | 粉色渐变，浪漫唯美 |
| `ocean` | 海洋 | 蓝色渐变，沉稳大气 |
| `tech` | 科技 | 赛博朋克，荧光酷炫 |

## 可用尺寸

| 尺寸 | 名称 | 宽度 |
|------|------|------|
| `mobile` | 移动端 | 20rem |
| `tablet` | 平板端 | 28rem |
| `laptop` | 电脑端 | 50rem |
| `desktop` | 超级屏 | 60rem |

## 示例

- `/md2png README.md` — 用默认主题转换文件
- `/md2png README.md -t dark -o readme.png` — 暗黑主题输出为 readme.png
- `/md2png "# Hello World" -t sakura -s mobile` — 樱花主题移动端尺寸

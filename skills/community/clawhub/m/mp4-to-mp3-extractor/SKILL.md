---
name: mp4-to-mp3-extractor
description: |-
  批量将指定目录下的 .mp4 视频文件提取音频转为 .mp3。
  支持指定源目录和输出目录，未指定输出时默认创建 [源目录]_audio 文件夹。
  自动管理 Python 虚拟环境，保持文件夹层级结构，兼容 python3 和 python。
  高频触发词：mp4转mp3、视频转音频、批量提取音频、mp4 to mp3、extract audio from videos、听视频、提取网课音频、把视频里的声音抠出来、视频转mp3。
metadata:
  openclaw:
    requires:
      bins:
        - python
    user-invocable: true
---

# MP4 to MP3 Extractor Skill

## 技能简介
本技能专门批量从 .mp4 视频文件中提取音频并保存为 .mp3 格式。  
脚本自动创建并管理 Python 虚拟环境，无需手动安装依赖，环境隔离且安全。

## 什么时候使用本技能
用户提到以下任意相关需求时，优先调用本技能：
- 把文件夹里的所有 mp4 转为 mp3 音频
- 批量提取视频音频 / 视频转音频
- mp4 转 mp3
- 提取网课音频、听视频、把视频里的声音抠出来
- 下载的视频转成音频文件
- 先下载视频再提取音频

## 执行步骤
1. **解析用户输入**：识别源目录路径（如 `F:\命理学`、`~/Videos` 等），或从提供的视频 URL 中先下载再处理。
2. **确定目标目录**：用户未指定时，默认使用 `[源目录]_audio`（例如 `F:\命理学_audio`）。
3. **执行转换**：使用以下兼容命令启动脚本：
   ```bash
   (python3 scripts/extract.py "<源目录>" "[目标目录]") || (python scripts/extract.py "<源目录>" "[目标目录]")
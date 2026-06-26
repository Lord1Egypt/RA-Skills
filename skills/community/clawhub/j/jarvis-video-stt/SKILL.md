---
name: jarvis-video-stt
description: |
  Jarvis-Video-STT - 批量视频语音转文字工具。
  基于Faster-Whisper，支持多进程并行、进度条、汇总报告。
  
  **触发场景**：
  - 用户需要将视频中的语音转换为文字/字幕
  - 批量处理多个视频
  - 需要生成SRT字幕或纯文本
  - 需要处理报告查看结果统计
  
  **使用方式**：
  1. 确认已安装依赖: pip install faster-whisper tqdm
  2. 确认ffmpeg已安装
  3. 执行命令或调用主脚本
  
  **支持格式**：MP4, MKV, AVI, MOV
  
  **输出**：
  - .srt 文件：带时间戳的字幕格式
  - .txt 文件：纯文本全文
  - report.json：机器可读的汇总报告
  - report.md：人类可读的汇总报告
---

# Jarvis-Video-STT Skill

## 快速开始

### 1. 安装依赖

pip install faster-whisper tqdm
确保ffmpeg已安装 (brew install ffmpeg on macOS)

### 2. 基本用法

medium模式（高精度，推荐）：
python ~/.openclaw/workspace-researcher/tools/jarvis-video-stt/batch_whisper.py -i videos/*.mp4 -o results -m medium

small模式（快速）：
python ~/.openclaw/workspace-researcher/tools/jarvis-video-stt/batch_whisper.py -i videos/*.mp4 -o results -m small

指定语言（略快）：
python batch_whisper.py -i videos/ -o results -m medium -l zh

调整并行数：
python batch_whisper.py -i videos/ -o results -w 4

### 3. 参数说明

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| --input | -i | 视频路径/文件夹/通配符 | 必填 |
| --output | -o | 输出目录 | output |
| --model | -m | small/medium | medium |
| --language | -l | 语言代码，None=自动 | None |
| --workers | -w | 并行进程数 | 3 |
| --cpu | - | 强制使用CPU | False |

### 4. 输出文件

每个视频生成：
- 视频名.srt - 带时间戳字幕
- 视频名.txt - 纯文本

整体生成：
- report.json - JSON汇总报告
- report.md - Markdown汇总报告

## 性能参考

| 模型 | 一小时视频(单进程) | 推荐并行 |
|------|-------------------|---------|
| small | ~2分钟 | 4进程 |
| medium | ~5分钟 | 3进程 |
| large-v3 | ~8分钟 | 2进程 |

## 适用场景

- 课程视频转文字
- 电影/纪录片字幕生成
- 播客/访谈转录
- 短视频内容分析
- 视频内容检索预处理

## 故障排除

Q: 报 faster-whisper 找不到？
pip install faster-whisper

Q: 报 ffmpeg 找不到？
brew install ffmpeg (macOS)
apt install ffmpeg (Ubuntu)

Q: Mac显存不足？
减少并行数：-w 2

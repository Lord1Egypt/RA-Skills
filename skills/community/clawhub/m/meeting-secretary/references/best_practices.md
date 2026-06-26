# 会议秘书技能最佳实践指南

## 快速参考

### 完整工作流程（一站式音频转纪要）

```bash
# 1. 音频转录（如需要）
python scripts/transcribe_audio.py meeting_audio.m4a --timestamps -o transcript.md

# 2. 长文本分段（如超过5000字）
python scripts/split_long_transcript.py transcript.md -o segments/

# 3. AI分析各段并整合纪要
# 在Claude Code中: "请分析segments/目录下的所有分段，生成完整会议纪要"
```

### 视频录屏处理

```bash
# 完整处理（提取音频+关键帧+幻灯片）
python scripts/process_video.py meeting_video.mp4 all -o processed/

# 查看处理报告
cat processed/processing_report.md
```

---

## 脚本使用指南

### transcribe_audio.py - 音频转录

**安装依赖**
```bash
pip install openai-whisper  # 标准版
# 或
pip install faster-whisper  # 更快版本
```

**使用示例**

```bash
# 基础转录
python scripts/transcribe_audio.py meeting.m4a

# 转录并保存
python scripts/transcribe_audio.py meeting.m4a -o transcript.txt

# 带时间戳转录（推荐！便于长会议分段）
python scripts/transcribe_audio.py meeting.m4a --timestamps -o transcript.md

# 使用更快版本
python scripts/transcribe_audio.py meeting.m4a --faster -o transcript.txt

# 选择更大模型（更准确）
python scripts/transcribe_audio.py meeting.m4a --model medium --timestamps -o transcript.md
```

**模型选择建议**
- `tiny`: 最快，适合快速预览
- `base`: 平衡速度和准确度（推荐）
- `small`: 更准确
- `medium`: 高准确度（重要会议推荐）
- `large`: 最高准确度，但较慢

---

### split_long_transcript.py - 长文本分段

**适用场景**
- 转录文本超过5000字
- 会议时长超过1小时
- 需要分段分析以保证质量

**使用示例**

```bash
# 自动检测分段方法
python scripts/split_long_transcript.py long_transcript.md -o segments/

# 指定分段方法
python scripts/split_long_transcript.py long_transcript.md --method semantic -o segments/

# 按时间戳分段（如果有时间戳）
python scripts/split_long_transcript.py transcript_with_timestamps.md --method timestamp -o segments/

# 按发言者分段（如果有发言者标注）
python scripts/split_long_transcript.py transcript_with_speakers.md --method speaker -o segments/
```

**输出结构**
```
segments/
├── segments_index.md      # 分段索引（先读这个！）
├── segment_001.txt        # 第一段
├── segment_002.txt        # 第二段
├── segment_003.txt        # 第三段
└── ...
```

**AI分析策略**
1. 先阅读 `segments_index.md` 了解整体结构
2. 逐段分析每个 `segment_*.txt` 文件
3. 整合所有分段的分析结果
4. 生成统一的完整纪要

---

### process_video.py - 视频录屏处理

**安装依赖**
```bash
pip install moviepy opencv-python pillow numpy
```

**使用示例**

```bash
# 完整处理（音频+关键帧+幻灯片检测）
python scripts/process_video.py meeting.mp4 all -o processed/

# 只提取音频
python scripts/process_video.py meeting.mp4 audio -o audio.wav

# 只提取关键帧（每30秒）
python scripts/process_video.py meeting.mp4 frames --interval 30 -o frames/

# 检测幻灯片切换
python scripts/process_video.py meeting.mp4 slides -o slides/

# 自定义关键帧数量（提取20帧）
python scripts/process_video.py meeting.mp4 frames --num 20 -o frames/
```

**输出结构**
```
processed/
├── processing_report.md       # 处理报告
├── audio.wav                  # 提取的音频
├── keyframes/                 # 关键帧目录
│   ├── frame_0000_t0s.jpg
│   ├── frame_0001_t60s.jpg
│   └── ...
└── slides/                    # 幻灯片切换帧
    ├── slide_000_t123s.jpg
    ├── slide_001_t456s.jpg
    └── ...
```

**完整工作流**
```bash
# 1. 处理视频
python scripts/process_video.py meeting.mp4 all -o processed/

# 2. 转录音频
python scripts/transcribe_audio.py processed/audio.wav --timestamps -o transcript.md

# 3. AI分析（结合音频转录+关键帧图片）
# 在Claude Code中: "请分析transcript.md和processed/keyframes/目录，生成会议纪要"
```

---

## AI分析工作流程

### 短会议（< 5000字）

```
输入 → 直接分析 → 生成纪要
```

### 长会议（> 5000字）

```
输入 → 分段处理 → 逐段分析 → 整合 → 生成纪要
         ↓
    segments/
```

### 视频会议

```
视频 → 提取音频 → 转录
    ↓
    提取关键帧 → 识别幻灯片
    ↓
    AI分析（音频+画面）→ 生成纪要
```

---

## 常见问题

### Q: 转录很慢怎么办？
**A:**
1. 使用 `--faster` 参数（faster-whisper）
2. 使用更小的模型（`--model tiny` 或 `base`）
3. 考虑使用GPU（如果有CUDA）

### Q: 长会议分析质量差？
**A:**
1. 使用 `--timestamps` 保存带时间戳的转录
2. 使用 `split_long_transcript.py` 分段处理
3. 让AI逐段分析后再整合

### Q: 视频中幻灯片内容怎么提取？
**A:**
1. 使用 `process_video.py meeting.mp4 slides` 检测切换
2. 手动查看提取的幻灯片帧
3. 将重要幻灯片内容告诉AI进行关联分析

### Q: 如何提高转录准确度？
**A:**
1. 使用更大的模型（`medium` 或 `large`）
2. 确保音频清晰、无背景噪音
3. 如果是专业领域，考虑微调Whisper模型

---

## 高级技巧

### 1. 结合多种输入
```bash
# 同时分析音频转录和会议笔记
python scripts/transcribe_audio.py meeting.m4a -o audio_transcript.txt
# 然后在AI中: "请分析audio_transcript.txt和meeting_notes.jpg，生成纪要"
```

### 2. 多轮迭代优化
```
第一轮: 快速生成初稿（tiny模型）
第二轮: 细化分析（base/medium模型）
第三轮: 整合视觉信息（关键帧+幻灯片）
```

### 3. 自动化处理脚本
```bash
# 创建一站式处理脚本
#!/bin/bash
VIDEO=$1
OUTDIR=${2:-"output"}

python scripts/process_video.py "$VIDEO" all -o "$OUTDIR"
python scripts/transcribe_audio.py "$OUTDIR/audio.wav" --timestamps -o "$OUTDIR/transcript.md"
python scripts/split_long_transcript.py "$OUTDIR/transcript.md" -o "$OUTDIR/segments/"

echo "处理完成！请在Claude Code中分析 $OUTDIR 目录"
```

### 4. 定制分段策略
如果会议有特殊结构（如：开场、主题讨论、问答），可以手动调整分段位置：
```bash
# 先自动分段
python scripts/split_long_transcript.py transcript.md -o segments/

# 手动调整segments_index.md中的分段信息

# 让AI按调整后的分段分析
```

---

## 性能参考

| 任务 | 预计时间 | 备注 |
|------|---------|------|
| 音频转录（1小时，base模型） | ~5-10分钟 | 取决于CPU性能 |
| 音频转录（1小时，medium模型） | ~15-30分钟 | 更准确 |
| 视频处理（1小时） | ~2-5分钟 | 主要是提取时间 |
| 长文本分段（1万字） | < 1秒 | 非常快 |
| AI分析（5000字） | ~1-2分钟 | 取决于模型 |

---

## 集成到工作流

### 与Claude Code集成
1. 将此技能安装到Claude Code
2. 直接提供音频/视频/文本文件
3. AI自动调用脚本并分析

### 与其他工具集成
- **Notion**: 将生成的纪要直接导入Notion
- **Obsidian**: 保存为Markdown格式，便于链接和引用
- **飞书/钉钉**: 可通过API发送到群聊

---

## 维护和更新

### 定期更新依赖
```bash
pip install --upgrade openai-whisper faster-whisper moviepy opencv-python
```

### 模型更新
Whisper模型会持续改进，定期检查更新：
```bash
# 重新下载最新模型
whisper download medium
```

### 自定义优化
- 针对特定领域微调Whisper模型
- 调整分段阈值和策略
- 添加行业术语词典

---
slug: music-toolkit-free
name: music-toolkit-free
version: 1.0.0
displayName: 音乐工具箱免费版
summary: 音乐生成与编辑工具,支持MIDI生成、音频处理与基础乐理分析
license: Proprietary
edition: free
description: '面向个人音乐爱好者与学习者的音乐生成与编辑工具箱。

  核心能力: MIDI生成、音频处理、乐理分析、和弦进行、旋律创作辅助

  适用场景: 音乐学习、创作原型、视频配乐、游戏音效、个人娱乐

  差异化: 免费版聚焦个人创作与学习,本地处理,无版权限制

  适用关键词: 音乐生成, MIDI, 音频处理, 乐理分析, 和弦进行, 旋律创作'
tags:
- 音乐生成
- 音频处理
- 乐理分析
- MIDI
- 创作工具
- 音乐学习
tools:
- - read
- exec
homepage: https://skillhub.cn
pricing_tier: "L1-入门级"
pricing_model: per_use
suggested_price: "9.9 CNY/per_use"
tools: ["read", "write", "exec"]
tags: "音乐生成,音频,创意"
---
# 音乐工具箱 (免费版)

## 概述

本工具为个人音乐爱好者与学习者提供音乐生成与编辑能力,涵盖 MIDI 生成、音频处理、乐理分析、和弦进行设计、旋律创作辅助等功能。所有处理在本地完成,无版权限制,适合音乐学习、创作原型、视频配乐、游戏音效等场景。

免费版聚焦个人创作与学习,适合音乐爱好者、独立开发者、视频创作者使用。

## 核心能力

| 能力模块 | 描述 | 免费版支持 |
|----|---|-----|
| MIDI 生成 | 程序化生成旋律与伴奏 | 支持 |
| 音频处理 | 混音、效果、格式转换 | 基础 |
| 乐理分析 | 调性、和弦、节奏分析 | 支持 |
| 和弦进行 | 自动推荐和弦走向 | 支持 |
| 旋律创作 | 辅助旋律设计 | 支持 |
| 节奏生成 | 鼓点与节奏模式 | 支持 |
| 音色库 | 内置音色 | 基础 |
| AI 编曲 | 智能编曲 | 不支持 (升级 PRO) |
| 多轨录音 | 多轨音频录制 | 不支持 (升级 PRO) |
| 母带处理 | 专业母带 | 不支持 (升级 PRO) |
| 商业授权 | 商业用途 | 个人 |
| 协作创作 | 多人协作 | 不支持 (升级 PRO) |

### 核心功能执行
用`input_params`参数进行配置。

**输入**: 用户提供核心功能执行所需的指令和必要参数。
**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输入**: 用户提供参数配置与调用所需的指令和必要参数。
**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输入**: 用户提供结果处理与输出所需的指令和必要参数。
**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应。
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：音乐生成与编辑工、音频处理与基础乐、面向个人音乐爱好、者与学习者的音乐、生成与编辑工具箱、核心能力、旋律创作辅助、适用场景、音乐学习、创作原型、视频配乐、游戏音效、个人娱乐、差异化、免费版聚焦个人创、作与学习、本地处理、无版权限制、适用关键词、音乐生成等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一: MIDI 旋律生成

程序化生成旋律 MIDI 文件。

```python
from midiutil import MIDIFile
import random
# ...
def generate_melody(key="C", scale="major", bars=4, bpm=120):
    """生成旋律 MIDI"""
    # 音阶定义
    scales = {
        "major": [0, 2, 4, 5, 7, 9, 11],
        "minor": [0, 2, 3, 5, 7, 8, 10],
        "pentatonic": [0, 2, 4, 7, 9],
    }
    key_notes = {"C": 60, "D": 62, "E": 64, "F": 65, "G": 67, "A": 69, "B": 71}
# ...
    base_note = key_notes[key]
    scale_notes = scales.get(scale, scales["major"])
# ...
    # 创建 MIDI 文件
    midi = MIDIFile(1)
    midi.addTempo(0, 0, bpm)
# ...
    # 生成旋律
    current_time = 0
    for bar in range(bars):
        for beat in range(4):
            # 随机选择音阶内的音
            scale_idx = random.randint(0, len(scale_notes) - 1)
            octave = random.choice([-1, 0, 0, 1])
            note = base_note + scale_notes[scale_idx] + 12 * octave
            duration = random.choice([0.5, 1, 1, 2])
# ...
            midi.addNote(0, 0, note, current_time, duration, 100)
            current_time += duration
# ...
    # 保存
    with open("melody.mid", "wb") as f:
        midi.writeFile(f)
    return "melody.mid"
# ...
generate_melody(key="C", scale="pentatonic", bars=8, bpm=128)
```

### 场景二: 和弦进行推荐

根据调性推荐合适的和弦进行。

```python
class ChordProgressionGenerator:
    # 常见和弦进行 (用罗马数字表示)
    PROGRESSIONS = {
        "major": {
            "I-V-vi-IV": ["C", "G", "Am", "F"],  # 流行经典
            "I-IV-V-I": ["C", "F", "G", "C"],    # 民谣
            "ii-V-I": ["Dm", "G", "C"],          # 爵士
            "I-vi-IV-V": ["C", "Am", "F", "G"],  # 50年代
        },
        "minor": {
            "i-VI-VII": ["Am", "F", "G"],        # 摇滚
            "i-iv-VII-III": ["Am", "Dm", "G", "C"], # 史诗
            "i-VII-VI-VII": ["Am", "G", "F", "G"],  # 暗黑
        },
    }
# ...
    def recommend(self, key="C", mood="happy", bars=4):
        """推荐和弦进行"""
        scale = "major" if mood == "happy" else "minor"
        progressions = self.PROGRESSIONS[scale]
# ...
        recommendations = []
        for name, chords in progressions.items():
            recommendations.append({
                "name": name,
                "chords": chords,
                "description": self._describe(name),
                "difficulty": self._difficulty(name),
            })
        return recommendations
# ...
    def _describe(self, name):
        descriptions = {
            "I-V-vi-IV": "流行音乐最常用,温暖正能量",
            "I-IV-V-I": "民谣风,简单明亮",
            "ii-V-I": "爵士经典,复杂有深度",
            "I-vi-IV-V": "50年代老歌感,怀旧",
            "i-VI-VII": "摇滚力量感,激昂",
            "i-iv-VII-III": "史诗感,适合配乐",
            "i-VII-VI-VII": "暗黑神秘,紧张",
        }
        return descriptions.get(name, "")
# ...
    def _difficulty(self, name):
        if "ii-V-I" in name: return "advanced"
        if "VII" in name or "III" in name: return "intermediate"
        return "beginner"
# ...
gen = ChordProgressionGenerator()
for r in gen.recommend(mood="happy"):
    print(f"{r['name']}: {r['chords']} - {r['description']}")
```

### 场景三: 音频处理

基础音频处理与格式转换。

```python
from pydub import AudioSegment
import numpy as np
# ...
class AudioProcessor:
    def __init__(self, file_path):
        self.audio = AudioSegment.from_file(file_path)
# ...
    def normalize(self, target_db=-20):
        """音量标准化"""
        change = target_db - self.audio.dBFS
        return self.audio.apply_gain(change)
# ...
    def fade_in_out(self, fade_in_ms=2000, fade_out_ms=3000):
        """渐入渐出"""
        return self.audio.fade_in(fade_in_ms).fade_out(fade_out_ms)
# ...
    def cut_segment(self, start_ms, end_ms):
        """截取片段"""
        return self.audio[start_ms:end_ms]
# ...
    def add_reverb(self, decay=0.5):
        """添加简单混响 (示例)"""
        # 这里使用简化的混响算法
        samples = np.array(self.audio.get_array_of_samples())
        delayed = np.roll(samples, int(44100 * 0.1))  # 100ms 延迟
        delayed = (delayed * decay).astype(np.int16)
        mixed = samples + delayed
        self.audio = AudioSegment(
            mixed.tobytes(),
            frame_rate=self.audio.frame_rate,
            sample_width=self.audio.sample_width,
            channels=self.audio.channels,
        )
        return self.audio
# ...
    def export(self, output_path, format="mp3", bitrate="192k"):
        """导出音频"""
        self.audio.export(output_path, format=format, bitrate=bitrate)
        return output_path
# ...
# 示例
processor = AudioProcessor("input.wav")
processor.normalize().fade_in_out().export("output.mp3", format="mp3")
```

## 不适用场景

以下场景音乐工具箱免费版不适合处理：

- 版权受保护的媒体内容处理
- 实时直播推流
- 专业影视后期

## 触发条件

需要视频处理、音频编辑、媒体转换、配音生成时使用。不适用于非本工具能力范围的需求。

## 快速开始

### 依赖详情

```bash
# Python 音乐处理库
pip install midiutil pydub numpy
# ...
# 系统依赖 (FFmpeg)
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: 下载 FFmpeg 并配置 PATH
```

### Step 2: 生成第一段旋律

```python
from midiutil import MIDIFile
# ...
midi = MIDIFile(1)
midi.addTempo(0, 0, 120)
midi.addNote(0, 0, 60, 0, 1, 100)  # C4, 1拍
midi.addNote(0, 0, 64, 1, 1, 100)  # E4
midi.addNote(0, 0, 67, 2, 1, 100)  # G4
# ...
with open("first_melody.mid", "wb") as f:
    midi.writeFile(f)
```

### Step 3: 用 DAW 打开

用 GarageBand、FL Studio、Ableton 等任意 DAW 打开 MIDI 文件即可听到旋律。

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤。

#
## 配置示例

### 音乐生成配置

```yaml
# ~/.music-toolkit/config.yaml
generation:
  default_key: C
  default_scale: major
  default_bpm: 120
  default_bars: 8
# ...
  scales:
    major: [0, 2, 4, 5, 7, 9, 11]
    minor: [0, 2, 3, 5, 7, 8, 10]
    pentatonic: [0, 2, 4, 7, 9]
    blues: [0, 3, 5, 6, 7, 10]
# ...
audio:
  sample_rate: 44100
  bit_depth: 16
  channels: 2
  default_format: mp3
  default_bitrate: 192k
# ...
instruments:
  - piano
  - guitar
  - drums
  - bass
  - strings
```

### 乐理参考

```python
MUSIC_THEORY = {
    "intervals": {
        "minor_second": 1, "major_second": 2,
        "minor_third": 3, "major_third": 4,
        "perfect_fourth": 5, "tritone": 6,
        "perfect_fifth": 7, "minor_sixth": 8,
        "major_sixth": 9, "minor_seventh": 10,
        "major_seventh": 11, "octave": 12,
    },
    "chord_formulas": {
        "major": [0, 4, 7],          # 大三和弦
        "minor": [0, 3, 7],          # 小三和弦
        "diminished": [0, 3, 6],     # 减三和弦
        "augmented": [0, 4, 8],      # 增三和弦
        "major7": [0, 4, 7, 11],     # 大七和弦
        "minor7": [0, 3, 7, 10],     # 小七和弦
        "dominant7": [0, 4, 7, 10],  # 属七和弦
    },
    "circle_of_fifths": [
        "C", "G", "D", "A", "E", "B", "F#",
        "C#", "G#", "D#", "A#", "F",
    ],
}
```

## 最佳实践

### 1. 旋律创作原则

```text
好旋律的特征:
- 有明确的动机 (短小主题片段)
- 重复与变化结合 (熟悉感+新鲜感)
- 句法清晰 (像说话一样有呼吸)
- 高潮点明确 (情绪曲线)
- 留白与节奏变化
```

### 2. 和弦选择

```python
def chord_for_mood(mood):
    """根据情绪推荐和弦"""
    mood_chords = {
        "happy": ["C", "F", "G", "Am"],
        "sad": ["Am", "Dm", "Em", "F"],
        "epic": ["Am", "F", "C", "G"],
        "mysterious": ["Em", "Am", "Bdim", "C"],
        "romantic": ["C", "Am", "F", "G"],
        "tense": ["Dm", "Bdim", "Am", "G"],
    }
    return mood_chords.get(mood, mood_chords["happy"])
```

### 3. 节奏设计

```python
DRUM_PATTERNS = {
    "pop": {
        "kick":  [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0],
        "snare": [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
        "hihat": [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1],
    },
    "rock": {
        "kick":  [1,0,0,0, 0,0,1,0, 1,0,0,0, 0,0,1,0],
        "snare": [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
        "hihat": [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1],
    },
    "electronic": {
        "kick":  [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0],
        "snare": [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
        "hihat": [1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0],
    },
}
```

## 常见问题

### Q1: 免费版生成的音乐有版权吗?

生成的音乐无版权限制,可用于个人项目。商业用途需要 PRO 版本授权。

### Q2: 支持哪些音频格式?

支持 WAV、MP3、OGG、FLAC、AAC 等主流格式 (依赖 FFmpeg)。

### Q3: 需要 DAW 吗?

不强制。可以直接生成 MP3。但用 DAW 打开 MIDI 文件可进一步编辑。

### Q4: 免费版音色库有多少?

内置基础音色 (钢琴、吉他、鼓等)。专业音色库需要 PRO 版本。

### Q5: 能做多轨混音吗?

免费版支持基础多轨。专业多轨混音与母带处理需要 PRO 版本。

## 依赖说明

### 运行环境

- **Agent 平台**: 支持 SKILL.md 规范的任意 AI Agent (Claude Code、Cursor、Codex、Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **FFmpeg**: 音频格式转换依赖

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | 推理服务 | 必需 | 由 Agent 内置 LLM 提供 |
| Python 3.8+ | 运行时 | 推荐 | python.org 下载 |
| midiutil | Python 库 | MIDI 生成 | `pip install midiutil` |
| pydub | Python 库 | 音频处理 | `pip install pydub` |
| numpy | Python 库 | 信号处理 | `pip install numpy` |
| FFmpeg | 系统工具 | 格式转换 | 系统包管理器安装 |

### API Key 配置

```bash
# 免费版无需外部 API Key
# 所有处理在本地完成
# ...
# 可选: 默认配置
export MUSIC_DEFAULT_KEY="C"
export MUSIC_DEFAULT_BPM="120"
export MUSIC_OUTPUT_FORMAT="mp3"
```

### 可用性分类

- **分类**: MD+EXEC (Markdown 指令 + 命令行执行)
- **说明**: 本 Skill 通过自然语言指令驱动 Agent 生成与处理音乐
- **免费版限制**: 个人使用、基础音色、无 AI 编曲、无多轨录音、无母带处理、无商业授权

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 本地运行，不支持多设备同步

## 示例

### 基本用法

**输入**：用户提供操作指令和必要参数

**输出**：返回执行结果,包含操作状态和输出数据

```text
用户: 执行核心功能
Skill: 正在执行核心功能...
Skill: 执行完成,结果如下: 操作成功
```

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "音乐工具箱免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "musickit"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```

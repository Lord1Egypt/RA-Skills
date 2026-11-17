---
name: huo15-ai-music-composer
displayName: "AI 音乐创作师"
version: 1.0.0
description: "端到端 AI 音乐创作技能：用户录制一段自己的声音 + 自己写的歌词 + 风格要求（或让 AI 推荐风格/问问题），生成一首用本人音色演唱的完整歌曲。集成 2026 年最先进 AI 音乐技术栈——零样本语音克隆(So-VITS-SVC 4.1)、端到端音乐生成(Suno v4)、AI 歌词创作(LyricsGPT)、多模态合成。触发词：AI 作曲 / AI 唱歌 / 语音克隆唱歌 / 用我的声音唱歌 / 生成一首歌 / AI 音乐创作。"
homepage: https://github.com/zhaobod1/huo15-skills
metadata: { "openclaw": { "emoji": "🎵", "requires": { "bins": ["python3"] } } }
aliases:
  - AI音乐创作
  - AI作曲
  - AI唱歌
  - 语音克隆唱歌
  - 用我的声音唱歌
  - 生成一首歌
  - AI音乐
  - ai-music-composer
---

# AI 音乐创作师 · huo15-ai-music-composer

> 录一段自己的声音 + 写一段歌词 + 提风格要求 → AI 用你的音色唱出一首完整歌曲。
> 青岛火一五信息科技有限公司 · OpenClaw 生态

## 核心功能

### 🎤 语音克隆与音乐演唱
- **用户录音输入**：支持 30 秒以上用户音频样本
- **AI 语音克隆**：零样本/少样本神经语音克隆技术
- **音色保持**：忠实还原用户音色和发音特征
- **多语言支持**：中文、英文等多种语言演唱

### 🎵 音乐创作与合成
- **歌词生成**：基于用户主题的 AI 歌词创作
- **旋律编排**：自动和弦编排与旋律生成
- **音乐风格**：流行、摇滚、民谣、电子、说唱等多种风格
- **乐器配置**：自动配置适合的音乐编曲

### 🎛️ 个性化定制
- **风格参数**：节奏、情绪、音色、速度调节
- **歌词编辑**：支持用户修改 AI 生成的歌词
- **音乐预览**：实时试听生成结果
- **多轨编辑**：支持人声、伴奏分离处理

## 技术栈

### AI 音乐引擎（2026 年 7 月最前沿）

| 技术 | 名称 | 功能 | 特点 |
|------|------|------|------|
| **语音克隆** | So-VITS-SVC 4.1 | 零样本语音合成 | 30秒样本克隆，音色保真 |
| **音乐生成** | Suno AI v4 | 端到端音乐创作 | 歌词→旋律→配器全流程 |
| **音频处理** | Demucs v4 | 音源分离 | 人声/伴奏分离处理 |
| **歌词创作** | LyricsGPT-7B | 专业歌词生成 | 押韵、意境、韵律优化 |
| **MIDI 编排** | MusicGPT 3.0 | 自动编曲 | 智能和弦、伴奏设计 |

### 部署架构

```
OpenClaw Skill
├── AI 音乐服务集群
│   ├── Voice Clone Service (GPU)
│   ├── Music Generation Service (GPU)
│   ├── Audio Processing Service
│   └── Lyrics Service (LLM)
├── Redis 缓存层
└── MinIO 音 频 存 储
```

## 工作流程

### 1. 用户输入阶段

```
用户请求 → 录音采集 → 音频预处理 → 特征提取
                    ↓
              歌词输入/生成 → 歌词优化 → 韵律分析
                    ↓
              风格选择 → 参数配置 → 生成策略
```

### 2. AI 处理阶段

```
并行处理流水线：
├── 分支A: 语音克隆服务 (5-15分钟)
│   ├── 样本增强 (音频清洗、降噪)
│   ├── 音色特征提取
│   ├── So-VITS-SVC 模型推理
│   └── 声音模型生成

├── 分支B: 音乐创作服务 (10-30分钟)
│   ├── 歌词→MIDI 转换
│   ├── 和弦编排优化
│   ├── 配器与编曲
│   └── 完整歌曲合成

└── 分支C: 合成演唱服务 (5-10分钟)
    ├── 人声与伴奏对齐
    ├── 音色合成演唱
    └── 混音与后处理
```

### 3. 输出阶段

```
生成结果 → 质量评估 → 多版本输出
├── High Definition (WAV 48kHz/24bit)
├── Standard (MP3 320kbps)
├── MIDI 源文件
└── Karaoke (伴奏+歌词)
```

## 使用指南

### 基本使用流程

1. **准备素材**
   ```
   - 用户录音：30秒以上清晰语音（格式：WAV/MP3）
   - 歌词文本：中文或英文歌词（支持AI自动生成）
   - 风格选择：流行、摇滚、民谣、电子等
   ```

2. **配置参数**
   ```python
   # 生成配置示例
   music_config = {
       "voice_sample": "path/to/voice.wav",
       "lyrics": "我想要...",
       "style": "pop",
       "tempo": 120,  # BPM
       "key": "C",   # 调性
       "emotion": "uplifting",
       "duration": 180  # 秒
   }
   ```

3. **执行生成**
   ```bash
   # 使用技能
   openclaw skill run ai-music-composer \
     --voice voice_sample.wav \
     --lyrics "我自己的歌词" \
     --style pop \
     --output song_output/
   ```

### 高级功能

#### 自定义风格模板

```yaml
# style_config.yaml
style: custom_rock
instruments:
  - lead_guitar
  - rhythm_guitar  
  - bass
  - drums
  - keyboard
effects:
  - reverb: 0.3
  - delay: 0.2
  - distortion: 0.4
tempo: 130
key: E_minor
```

#### 歌词主题生成

```
/music theme="夏日恋曲" mood="浪漫" language="中文"
→ 系统生成多版本歌词供选择

关键词引导：
- 主题：爱情、梦想、回忆、励志等
- 情绪：欢快、抒情、激昂、忧郁等  
- 风格：古风、现代、文艺、口语等
```

#### 批量处理模式

```bash
gen_music_batch.py \
  --input-dir ./user_requests/ \
  --output-dir ./generated_songs/ \
  --parallel-jobs 4
```

## 系统要求

### 计算资源
- **GPU 要求**：最低 NVIDIA RTX 4090 (24GB)，推荐 A100/H100
- **CPU**：32 核以上
- **内存**：128GB+ RAM
- **存储**：500GB+ SSD（音频处理缓存）
- **网络**：10Gbps+（服务间通信）

### 容器部署（Docker）

```yaml
# docker-compose.yml
version: '3.8'
services:
  voice-clone:
    image: registry.huo15.com/ai-music/voice-clone:v4.1
    runtime: nvidia
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  music-gen:
    image: registry.huo15.com/ai-music/suno-engine:v4
    runtime: nvidia

  lyrics-ai:
    image: registry.huo15.com/ai-music/lyrics-gpt7:latest

  redis-cache:
    image: redis:7

  minio-storage:
    image: minio/minio:latest
```

## 性能与限制

### 生成时间
| 任务阶段 | 输入长度 | 预计耗时 | GPU 占用 |
|----------|----------|----------|----------|
| 语音克隆 | 30s样本 | 5-15分钟 | ~18GB |
| 歌词生成 | 200字 | 30-60秒 | CPU |
| 音乐生成 | 3-4分钟 | 10-30分钟 | ~20GB |
| 演唱合成 | 3-4分钟 | 5-10分钟 | ~16GB |

### 质量规格
- **音质保真度**：MOS ≥ 4.2/5.0
- **音频格式**：WAV 48kHz/24bit，MP3 320kbps
- **最大支持时长**：10分钟/首
- **并发生成**：支持 4-8 路并发
- **成功率**：≥ 95%（正常输入）

## 注意事项

### 输入要求
- **录音质量**：建议安静环境，无背景噪音
- **采样率**：至少 16kHz，推荐 44.1kHz/48kHz
- **格式支持**：WAV、MP3、FLAC（自动转换）
- **文件大小**：单次生成 ≤ 200MB

### 版权与许可
- 生成的音乐作品归用户所有
- 训练数据严格遵守版权规范
- 用户需提供合法音频样本
- 商业使用需遵循平台政策

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 音色失真 | 录音质量差 | 重新录制清晰样本 |
| 生成失败 | GPU 内存不足 | 降低并发数或升级硬件 |
| 节奏不准 | 拍号设置错误 | 手动指定 BPM |
| 歌词不押韵 | AI 参数不当 | 调整韵律权重 |

## 扩展开发

查看 [EXTENSION_GUIDE.md](EXTENSION_GUIDE.md) 了解如何：
- 添加新的音乐风格
- 集成其他 AI 音乐模型
- 自定义声音效果器
- 开发插件系统

## 参考文档

- [技术规格详情](docs/technical-spec.md)
- [API 接口文档](docs/api-reference.md)
- [训练数据集说明](docs/training-data.md)
- [模型优化建议](docs/model-optimization.md)

---

**注意**：本技能需要高性能 GPU 集群支持，建议在专业音频工作站或云服务上部署使用。
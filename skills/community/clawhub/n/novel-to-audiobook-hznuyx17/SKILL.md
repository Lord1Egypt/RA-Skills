---
name: novel-to-audiobook
description: "将小说章节转换为有声书（MP3）。当用户提到：转有声书、生成有声书、做成音频、听书、朗读章节、语音版时使用。自动分析章节内容，识别对话角色并分配不同音色，生成带背景音乐的完整有声书。"
metadata:
  copaw:
    emoji: "🎧"
    requires:
      env: ["DEEPSEEK_API_KEY", "MINIMAX_API_KEY"]
---

> **路径说明**: 所有脚本路径相对于此 Skill 目录。
> 执行时: `cd {skill_dir} && python scripts/...`

# 小说转有声书

## 工作流程

收到用户请求后，按以下步骤执行:

### 第一步: 获取章节内容

从用户输入中获取章节文本:
- 用户直接提供文本内容
- 用户提供文件路径（如 `第一章.md`、`第一章.txt`）
- 从小说项目目录中读取指定章节

同时询问用户是否需要调整:
- 旁白音色
- 背景音乐风格（根据章节题材自动匹配）

### 第二步: 分析章节 → 分段 + 角色标注

调用 DeepSeek 分析章节文本，识别旁白和对话:

```bash
python scripts/chapter_analyzer.py --file "章节文件路径" > temp_analysis.json
```

输出为 JSON，包含 `segments` 数组，每段有:
- `type`: `title` / `narration` / `dialogue`
- `text`: 分段文本
- `character`: 角色名（对话时）
- `mood`: 段落情绪

同时获得统计信息: 总字数、对话占比、角色列表。

**注意:** 将输出保存为临时 JSON 文件，供后续步骤使用。

### 第三步: 生成背景音乐（可选）

根据章节情绪生成纯音乐背景:

```bash
python scripts/music_generator.py \
  --mood "章节情绪（如悬疑/温馨/平静）" \
  --output "temp_bgm/bg_music.mp3"
```

情绪映射参考:
| 章节氛围 | 音乐风格 |
|---------|---------|
| 平静/日常 | 轻钢琴 |
| 悬疑/紧张 | 暗黑氛围 |
| 悲伤 | 钢琴独奏 |
| 欢快 | 轻快节奏 |
| 热血/战斗 | 管弦乐激昂 |

如用户不需要背景音乐，跳过此步。

### 第四步: 逐段生成语音

根据分段结果，调用 MiniMax TTS 为每段生成语音:

```bash
python scripts/tts_generator.py \
  --segments-file "temp_analysis.json" \
  --output-dir "temp_audio/" > temp_tts_result.json
```

音色分配规则:
- **章节标题** → 主播音色（`chapter_intro_voice`）
- **旁白** → 统一旁白音色（`narration_voice`）
- **角色对话** → 根据角色名自动分配音色:
  - 女性角色 → 女声
  - 男性角色 → 男声
  - 可在 `config.json` 的 `character_voices` 中自定义

### 第五步: 合成最终有声书

拼接所有语音段 + 混入背景音乐:

```bash
python scripts/audio_assembler.py \
  --segments "temp_tts_result.json" \
  --bg-music "temp_bgm/bg_music.mp3" \
  --output "E:/qwenpaw/Novel/有声书输出/小说名_章节名.mp3"
```

如没有背景音乐，去掉 `--bg-music` 参数。

### 第六步: 返回结果

将最终 MP3 文件路径和信息展示给用户:
- 文件名和路径
- 总时长
- 涉及角色列表

## 配置说明

在 `config.json` 中配置以下信息:

| 配置项 | 说明 |
|--------|------|
| `deepseek_api_key` | DeepSeek API Key（分析章节文本） |
| `minimax_api_key` | MiniMax API Key（TTS + 音乐生成） |
| `tts_model` | TTS 模型（默认 speech-2.8-hd） |
| `music_model` | 音乐模型（默认 music-2.6-free） |
| `narration_voice` | 旁白音色 |
| `default_male_voice` | 男性角色默认音色 |
| `default_female_voice` | 女性角色默认音色 |
| `output_path` | 有声书输出目录 |
| `bg_music_volume` | 背景音乐音量 (0.0~1.0，默认 0.15) |

## 使用示例

**示例 1: 用户提供文件路径**
```
用户: 帮我把第一章转成有声书，文件在 E:\qwenpaw\Novel\当前作品\第一章.md
```

执行流程:
```bash
python scripts/chapter_analyzer.py --file "E:/qwenpaw/Novel/当前作品/第一章.md" > temp_analysis.json

python scripts/music_generator.py --mood "平静" --output "temp_bgm/bg_music.mp3"

python scripts/tts_generator.py --segments-file temp_analysis.json --output-dir temp_audio/ > temp_tts_result.json

python scripts/audio_assembler.py --segments temp_tts_result.json --bg-music temp_bgm/bg_music.mp3 --output "E:/qwenpaw/Novel/有声书输出/当前作品_第一章.mp3"
```

**示例 2: 用户直接粘贴章节文本**
```
用户: 这段转有声书：（粘贴文本内容）
```

用 `--text` 参数直接传文本:
```bash
python scripts/chapter_analyzer.py --text "粘贴的章节内容" > temp_analysis.json
```

## 注意事项

1. **API Key**: 与封面生成 Skill 共用 DeepSeek + MiniMax API Key
2. **处理时间**: 长章节（5000字以上）TTS 生成可能需要几分钟，请耐心等待
3. **速率限制**: MiniMax API 有频率限制，脚本已内置 0.3 秒延迟
4. **音色选择**: 如果角色音色不合适，可以在 config.json 的 `character_voices` 字段中自定义映射
5. **背景音乐**: 使用 `music-2.6-free` 免费模型，如需更高品质可改为 `music-2.6`（需付费）
6. **临时文件**: 中间音频文件会保留在 `temp_audio/` 和 `temp_bgm/` 目录，可手动清理

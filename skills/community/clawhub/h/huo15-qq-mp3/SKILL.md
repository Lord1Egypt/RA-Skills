---
name: huo15-qq-mp3
displayName: QQ音乐转mp3技能
version: 1.0.0
description: "将QQ音乐下载的音频文件（OGG/FLAC/M4A/WAV/AAC 等）批量转换为通用 MP3 格式，保留元数据。支持单文件与整目录批处理，自动检测 ffmpeg 并选择最优编码参数。"
homepage: https://github.com/zhaobod1/huo15-skills
metadata: { "openclaw": { "emoji": "🎵", "requires": { "bins": ["ffmpeg"] } } }
aliases:
  - QQ音乐转mp3技能
  - QQ音乐转换
  - OGG转MP3
  - FLAC转MP3
  - 音频转MP3
  - qq to mp3
  - audio to mp3
---

# QQ音乐转 MP3（Audio → MP3）

将**QQ音乐**下载的音频文件（`.ogg`、`.flac`、`.m4a`、`.wav`、`.aac`、`.opus` 等）转换为通用 **MP3** 格式，保留元数据（标题、艺术家、专辑等），支持**单文件**与**整目录批处理**。

## 使用时机

✅ **使用此技能当：** 需要将QQ音乐下载的 OGG/FLAC/M4A 等音频转为 MP3，使其能在更多设备/软件上播放；需要批量转换一整个目录的音频文件。
❌ **不要用当：** 文件已经是 MP3 且无需转码；文件为 QQ音乐加密格式（`.qmc0`、`.mflac` 等，需先用解密工具处理）。

## 前置依赖

- **ffmpeg**（含 `libmp3lame` 编码器）— 转码核心工具
- 检查方式：`ffmpeg -version`，确认输出含 `--enable-libmp3lame`

## 支持的输入格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| OGG Vorbis | `.ogg` | QQ音乐常见下载格式 |
| FLAC | `.flac` | 无损压缩 |
| M4A / AAC | `.m4a` `.aac` | Apple AAC |
| WAV | `.wav` | 无压缩 |
| Opus | `.opus` | 低码率高效编码 |
| WMA | `.wma` | Windows Media |
| AIFF | `.aiff` `.aif` | Apple 无压缩 |

> ⚠️ **加密格式**（`.qmc0` `.qmc2` `.qmc3` `.qmcflac` `.qmcmp3` `.mflac` `.mmp3`）需要先用 [qmcdump](https://github.com/Presburger/qmc-decoder) 或 [Unlock Music](https://git.unlock-music.dev/um/web) 解密后再用本技能转码。

## 铁律

1. **保留元数据** — 转码时使用 ffmpeg 默认的 metadata copy，不主动剥离标题/艺术家/专辑信息。
2. **不覆盖原文件** — 输出 MP3 与源文件同目录、同文件名（仅扩展名改为 `.mp3`）；若已存在同名 `.mp3` 则跳过并提示。
3. **VBR 优先** — 使用 `-q:a 2`（VBR，约 170-210 kbps），在音质与体积间取得最佳平衡。
4. **错误不中断**（批量模式）— 单个文件转码失败时记录错误并继续处理下一个，最终汇总报告。

## 单文件转码

```bash
ffmpeg -y -i "INPUT.ogg" -vn -acodec libmp3lame -q:a 2 "OUTPUT.mp3"
```

- `-y`：覆盖已存在输出（单文件模式由 agent 控制，默认加 `-y`）
- `-vn`：丢弃视频轨（如有），只保留音频
- `-q:a 2`：VBR 质量 2（约 190 kbps，接近透明）
- 元数据（TITLE、ARTIST、ALBUM 等）自动保留

### 质量档位参考

| 参数 | 码率 | 体积 | 适用场景 |
|------|------|------|----------|
| `-q:a 0` | ~245 kbps | 最大 | 极致音质（源为 FLAC 时推荐） |
| `-q:a 2` | ~190 kbps | 中等 | **默认推荐**，透明级 |
| `-q:a 4` | ~170 kbps | 较小 | 日常听感足够 |
| `-q:a 6` | ~135 kbps | 小 | 语音/有声书 |
| `-b:a 320k` | 320 kbps CBR | 大 | 强制 CBR 兼容老旧设备 |

## 批量转码

使用本技能附带的脚本 `scripts/qq_to_mp3.sh`：

```bash
# 转换整个目录（递归）
bash scripts/qq_to_mp3.sh /path/to/music/

# 转换单个文件
bash scripts/qq_to_mp3.sh /path/to/song.ogg

# 指定质量档位（0-6，默认 2）
bash scripts/qq_to_mp3.sh /path/to/music/ -q 0

# 指定输出目录
bash scripts/qq_to_mp3.sh /path/to/music/ -o /path/to/output/
```

脚本行为：
- 自动检测 ffmpeg 是否可用
- 递归扫描 `.ogg .flac .m4a .aac .wav .opus .wma .aiff .aif` 文件
- 同名 `.mp3` 已存在时**跳过**
- 单文件失败不中断，最终输出汇总（成功/失败/跳过计数）
- 保留原始目录结构到输出目录

## 标准流程

1. **确认输入** — 用户提供文件路径或目录路径；确认格式是否为本技能支持的类型。
2. **检测环境** — 运行 `ffmpeg -version` 确认可用；若不可用，提示安装方式：
   - macOS：`brew install ffmpeg`
   - Ubuntu/Debian：`sudo apt install ffmpeg`
   - Windows：从 [ffmpeg.org](https://ffmpeg.org/download.html) 下载
3. **执行转码**：
   - 单文件 → 直接 `ffmpeg` 命令
   - 多文件/目录 → 使用 `scripts/qq_to_mp3.sh` 脚本
4. **汇报结果** — 输出每个文件的转码信息（源格式 → MP3、时长、码率、文件大小对比）。
5. **可选：清理** — 询问用户是否删除源文件（**默认保留**，不自动删除）。

## 反模式（禁止）

- ❌ 删除或覆盖原始音频文件
- ❌ 使用固定 CBR 320k 处理语音文件（浪费空间）
- ❌ 不检查 ffmpeg 是否可用就执行
- ❌ 批量转码中某个文件失败就全部中止
- ❌ 对已经是 MP3 的文件重复转码（有损 → 有损，音质下降）

## 核心原则

**保留元数据 · 不覆盖原文件 · VBR 优先 · 批量容错。** 音频转码是格式迁移，不是音质升级——源文件质量是上限。

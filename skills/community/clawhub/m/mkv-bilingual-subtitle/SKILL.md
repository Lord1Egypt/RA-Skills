---
name: mkv-bilingual-subtitle
display_name: 双语字幕
description: "MKV视频双语字幕合并工具。从MKV文件中提取简体中文和英文字幕，合并为中英双语字幕（英文在上中文在下），再嵌入回MKV文件。支持SRT和ASS/SSA字幕格式，支持单文件和批量文件夹处理。触发场景：用户要求将MKV中的中英字幕合并、制作双语字幕、中英混合字幕、字幕合并嵌入、MKV字幕处理。触发词：双语字幕、中英字幕、合并字幕、混合字幕、字幕嵌入、MKV字幕。"
---

# MKV Bilingual Subtitle Merger

从 MKV 视频中提取中文和英文字幕，合并为双语字幕（英文在上，中文在下），再嵌入回 MKV。

## Requirements

- **mkvmerge** + **mkvextract** (MKVToolNix) — 必需，用于提取和嵌入字幕
- 安装：`brew install mkvtoolnix`
- 仅支持文本字幕（SRT / ASS / SSA），不支持图像字幕（PGS / VobSub）

## Quick Start

```bash
# 单个文件
python3 scripts/merge_subs.py /path/to/video.mkv

# 批量处理（文件夹内所有 mkv）
python3 scripts/merge_subs.py /path/to/videos/

# 递归处理子文件夹
python3 scripts/merge_subs.py /path/to/videos/ --recursive

# 预览模式（不执行，只显示哪些文件可以处理）
python3 scripts/merge_subs.py /path/to/videos/ --dry-run
```

脚本路径：`scripts/merge_subs.py`

## How It Works

1. **扫描字幕轨道** — `mkvmerge -i` 识别所有字幕轨道，按语言匹配中文（chi/zho/zh/cn）和英文（eng/en）
2. **提取字幕** — `mkvextract tracks` 将中英文字幕提取为独立文件
3. **合并字幕** — 基于时间戳重叠匹配，合并为中英双语条目：
   - 完全匹配：直接合并，取时间并集
   - 部分重叠（>30%）：合并，取时间并集
   - 无匹配：保留原文条目
4. **嵌入回 MKV** — `mkvmerge -o` 将双语字幕作为新轨道嵌入，设为默认字幕轨道
5. **替换源文件** — 用新文件替换原始 MKV（文件名不变），整个过程原子性操作

## Output Format

- **SRT**：英文行 + 换行 + 中文行
- **ASS**：英文文本 + `\N` + 中文文本

## Options

| 选项 | 说明 |
|------|------|
| `-o, --output` | 指定输出文件路径（不指定则直接替换源文件） |
| `-r, --recursive` | 递归搜索子目录 |
| `--keep-temp` | 保留提取的临时字幕文件 |
| `--dry-run` | 预览模式，不实际执行 |

## Error Handling

- 无字幕轨道 → 提示并跳过
- 无中文或英文字幕 → 提示并跳过
- 图像字幕（PGS/VobSub）→ 提示不支持并跳过
- mkvmerge/mkvextract 未安装 → 提示安装命令

## Batch Processing Rules

**当用户给出文件夹路径或涉及多个文件时，必须先列出目录内容让用户确认后再执行。**

流程：
1. 扫描目录，列出所有 MKV 文件（文件名 + 大小 + 字幕状态）
2. 标记已处理和待处理文件（已有「中英双语」字幕轨 = 已处理）
3. 等待用户确认后再执行批量处理
4. 用户可以指定范围（如「只处理 E03-E10」）

示例输出格式：
```
| # | 文件 | 大小 | 状态 |
|---|------|------|------|
| 1 | S01E01 ... | 1.0G | ⬜ 待处理 |
| 2 | S01E02 ... | 989M | ✅ 已处理 |
```

## Notes

- 默认**直接替换源文件**（文件名不变），如需保留源文件请用 `-o` 指定输出路径
- 合并后的双语字幕轨道语言标记为 `chi`，轨道名为 `中英双语`
- 批量处理时自动统计成功/跳过/失败数量
- 单文件处理时无需确认，直接执行

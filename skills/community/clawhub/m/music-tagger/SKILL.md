---
name: music-tagger
description: 音乐文件批量标签工具，支持读取/编辑音乐元数据（歌名、艺术家、专辑、流派等），批量编辑标签，按标签整理音乐文件，预览模式和撤销功能！
---

# Music Tagger - 音乐文件批量标签工具

## 功能特性
- ✅ 自动识别音乐文件格式（mp3, flac, wav, aac, m4a, ogg, wma, ape 等）
- ✅ 读取/编辑音乐元数据（歌名、艺术家、专辑、流派、年份、曲目号等）
- ✅ 批量编辑标签
- ✅ 按标签整理音乐文件（艺术家/专辑、流派、年份等）
- ✅ 预览模式（先看效果再执行）
- ✅ 撤销操作（安全可靠）

## 安装
```bash
# 方法一：通过 clawhub 安装
clawhub install music-tagger

# 方法二：作为 Python 脚本运行
git clone <repo-url>
cd music-tagger
pip install mutagen
```

## 依赖说明
当前版本是简化版，主要演示框架。要启用实际标签编辑功能，请安装：
- `mutagen`：处理音乐元数据

## 快速开始

### 1. 读取音乐文件标签
```bash
music-tagger read song.mp3
```

### 2. 编辑音乐文件标签
```bash
music-tagger edit song.mp3 --title "My Song" --artist "My Artist" --album "My Album"
```

### 3. 批量设置标签
```bash
music-tagger batch ./music --artist "My Artist"
```

### 4. 按艺术家/专辑整理音乐
```bash
music-tagger organize ./music --by artist-album --output ./organized
```

### 5. 预览模式
```bash
music-tagger organize ./music --by artist-album --preview
```

### 6. 撤销操作
```bash
music-tagger undo ./organized
```

## 详细使用说明

### read 命令参数
- `file`：（必需）要读取标签的音乐文件

### edit 命令参数
- `file`：（必需）要编辑标签的音乐文件
- `--title`：歌名
- `--artist`：艺术家
- `--album`：专辑
- `--genre`：流派
- `--year`：年份
- `--track`：曲目号

### batch 命令参数
- `directory`：（必需）要批量编辑的音乐目录
- `--title`：批量设置歌名
- `--artist`：批量设置艺术家
- `--album`：批量设置专辑
- `--genre`：批量设置流派
- `--year`：批量设置年份

### organize 命令参数
- `directory`：（必需）要整理的音乐目录
- `--by`：整理方式，可选 `artist-album`（按艺术家/专辑，默认）、`genre`（按流派）、`year`（按年份）
- `--output`：输出目录，默认在输入目录下创建 `organized` 文件夹
- `--preview`：预览模式，只显示方案不实际执行

### 支持的音乐格式
| 格式 | 说明 |
|-----|------|
| mp3 | MP3 音频 |
| flac | FLAC 无损音频 |
| wav | WAV 音频 |
| aac, m4a | AAC 音频 |
| ogg | OGG 音频 |
| wma | Windows Media 音频 |
| ape | APE 无损音频 |

## 示例场景

### 场景 1：批量设置艺术家
```bash
# 将整个文件夹的音乐艺术家设置为 "My Artist"
music-tagger batch ./music --artist "My Artist"
```

### 场景 2：按艺术家/专辑整理音乐
```bash
# 按艺术家/专辑整理音乐文件夹
music-tagger organize ./music --by artist-album --output ./Music/Organized
```

### 场景 3：先预览，再执行
```bash
# 第一步：预览
music-tagger organize ./music --by artist-album --preview

# 第二步：确认没问题后执行
music-tagger organize ./music --by artist-album --output ./organized
```

## 注意事项
- 确保已安装所需的依赖库
- 编辑标签前建议先备份原文件
- 建议先用 --preview 预览效果
- 整理前建议先备份原文件

## 更新日志
### v1.0.0 (2026-03-06)
- 初始版本发布
- 支持读取/编辑基本音乐标签
- 支持批量编辑标签
- 支持按标签整理音乐
- 支持预览模式
- 支持撤销操作

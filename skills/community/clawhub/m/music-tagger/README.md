# Music Tagger - 音乐文件批量标签工具

一个简单但强大的音乐文件批量标签工具，帮助你快速管理音乐文件的元数据！

## 功能特性
- ✅ 自动识别音乐文件格式（mp3, flac, wav, aac, m4a, ogg, wma, ape 等）
- ✅ 读取/编辑音乐元数据（歌名、艺术家、专辑、流派、年份、曲目号等）
- ✅ 批量编辑标签
- ✅ 按标签整理音乐文件（艺术家/专辑、流派、年份等）
- ✅ 预览模式（先看效果再执行）
- ✅ 撤销操作（安全可靠）

## 安装

### 方法一：通过 clawhub 安装
```bash
clawhub install music-tagger
```

### 方法二：作为 Python 脚本运行
```bash
# 克隆或下载项目
git clone <repo-url>
cd music-tagger

# 安装依赖（需要实际标签编辑功能时）
pip install mutagen
```

## 依赖说明
当前版本是简化版，主要演示框架。要启用实际标签编辑功能，请安装：
- `mutagen`：处理音乐元数据（支持 MP3, FLAC, MP4, OGG 等）

## 快速开始

### 1. 读取音乐文件标签
```bash
python3 music_tagger.py read song.mp3
```

### 2. 编辑音乐文件标签
```bash
python3 music_tagger.py edit song.mp3 --title "My Song" --artist "My Artist" --album "My Album"
```

### 3. 批量设置标签
```bash
python3 music_tagger.py batch ./music --artist "My Artist"
```

### 4. 按艺术家/专辑整理音乐
```bash
python3 music_tagger.py organize ./music --by artist-album --output ./organized
```

这会将音乐按照艺术家/专辑整理到这样的文件夹结构中：
```
organized/
├── Artist 1/
│   ├── Album 1/
│   │   ├── song1.mp3
│   │   └── song2.mp3
│   └── Album 2/
│       └── song3.mp3
└── Artist 2/
    └── Album 1/
        └── song4.mp3
```

### 5. 预览模式（不实际执行，先看效果）
```bash
python3 music_tagger.py organize ./music --by artist-album --preview
```

### 6. 撤销操作
```bash
python3 music_tagger.py undo ./organized
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
- `--preview`：预览模式

### organize 命令参数
- `directory`：（必需）要整理的音乐目录
- `--by`：整理方式，可选 `artist-album`（按艺术家/专辑，默认）、`genre`（按流派）、`year`（按年份）
- `--output`：输出目录，默认在输入目录下创建 `organized` 文件夹
- `--preview`：预览模式

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
| alac, opus, mpc, tta | 其他常见音频格式 |

## 示例场景

### 场景 1：批量设置艺术家
```bash
# 将整个文件夹的音乐艺术家设置为 "My Artist"
python3 music_tagger.py batch ./music --artist "My Artist"
```

### 场景 2：按艺术家/专辑整理音乐
```bash
# 按艺术家/专辑整理音乐文件夹
python3 music_tagger.py organize ./music --by artist-album --output ./Music/Organized
```

### 场景 3：先预览，再执行
```bash
# 第一步：预览
python3 music_tagger.py organize ./music --by artist-album --preview

# 第二步：确认没问题后执行
python3 music_tagger.py organize ./music --by artist-album --output ./organized
```

## 注意事项
- 确保已安装所需的依赖库
- 编辑标签前建议先备份原文件
- 建议先用 --preview 预览效果
- 整理前建议先备份原文件

## 安全性
- 工具默认使用模拟编辑（当前版本）
- 执行前会自动保存备份
- 支持一键撤销操作
- 建议先用 --preview 预览效果

## 故障排除

### 问题：找不到依赖库
**解决方法**：
```bash
pip install mutagen
```

### 问题：撤销失败
**原因**：备份文件可能被删除或修改
**解决方法**：确保在同一目录下执行，且备份文件未被删除

## 开发计划
- [ ] 完善实际标签读写功能（使用 Mutagen）
- [ ] 从文件名提取标签信息
- [ ] 正则表达式替换标签
- [ ] 专辑封面处理
- [ ] 配置文件支持
- [ ] GUI 界面（可选）

## 贡献
欢迎提交 Issue 和 Pull Request！

## 许可证
MIT License

---

**Music Tagger** - 让音乐标签管理变得简单！🎵

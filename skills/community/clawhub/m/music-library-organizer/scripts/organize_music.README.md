# 音乐库整理脚本 - 使用说明

> 整理 `/volume4/media2/音乐` 下的所有音乐文件和歌词文件，按三级目录结构重命名 + 移动。

## 目标目录结构

```
目标根目录/
├── A/
│   ├── Alan Walker/
│   │   ├── Alan Walker - Different World.flac
│   │   ├── Alan Walker - Faded.lrc
│   │   └── ...
│   └── ...
├── Z/
│   ├── 周杰伦/
│   │   ├── 周杰伦 - 晴天.flac
│   │   ├── 周杰伦 - 晴天.lrc
│   │   └── ...
│   └── ...
└── 其他/
    ├── 1K/
    │   ├── 1K - 就忘了吧.flac
    │   └── ...
    └── 纯真年代组合 - 童年.mp3
└── _低音质备份/
    └── [被替换的低音质文件，按原结构归档]
```

## 快速使用

```bash
# 1. 先 dry-run 跑一遍（不动文件，只生成 CSV 报告）
python3 organize_music.py

# 2. 看报告（推荐先用 LibreOffice / Excel 打开）
# 报告路径: /volume4/media2/整理报告_dryrun_时间戳.csv

# 3. 确认无误后，真正执行
python3 organize_music.py --apply
```

## 命令行参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--source DIR` | `/volume4/media2/音乐` | 源目录 |
| `--target DIR` | `/volume4/media2/音乐_整理` | 目标目录 |
| `--apply` | False | 真正执行（默认干跑） |
| `--no-tag` | False | 跳过 ID3 标签读取（快，但解析率低） |
| `--limit N` | 0 | 限制处理文件数（调试用） |

## 修改源/目标路径

打开 `organize_music.py` 顶部（约 39-40 行）：

```python
SOURCE_DIR = "/volume4/media2/音乐"      # ← 改这里
TARGET_DIR = "/volume4/media2/音乐_整理"  # ← 改这里
```

或者通过命令行临时覆盖：

```bash
python3 organize_music.py --source /path/to/music --target /path/to/output
```

## 依赖安装

```bash
# 必需：无（纯标准库就能跑基础版）
# 推荐：装上 mutagen + pypinyin 会更准确
python3 -m pip install --break-system-packages mutagen pypinyin
```

> `--break-system-packages` 在 Debian 12 是必需的，因为系统 Python 默认禁止 pip 装全局包。

## 命名规则

### 音乐文件
- 单歌手：`歌手 - 歌曲名.格式` （如 `周杰伦 - 晴天.flac`）
- 多歌手：统一用 `&` 连接（如 `Alan Walker & K-391 - Different World.flac`）
- 缺歌手：仅 `歌曲名.格式`，归入 `其他/` 目录

### 歌词文件
- 与音乐文件主名一致：`歌手 - 歌曲名.lrc`
- 找不到匹配音乐时，原歌词文件保留原位

## 去重规则（音质优先级）

```
无损 (FLAC/APE/WAV)         → 100/95/90
320k MP3                    → 70
高码率 MP3 (≥256k)          → 60
普通 MP3                    → 50
M4A / AAC                   → 40/35
OGG / OPUS                  → 30
WMA                         → 20
其他                        → 10
```

被替换的低音质文件 → `目标根目录/_低音质备份/原路径`（保留目录结构）

## 中文歌手名首字母

- 默认使用 `pypinyin` 库转拼音首字母（推荐）
- 未装 pypinyin 时：使用内置常用字映射表（覆盖 100+ 主流姓氏 + 兜底走"其他"）

## 异常处理

| 情况 | 处理 |
|------|------|
| 非法字符 `\ / : * ? " < > \|` | 替换为空格 |
| 数字开头或无法识别的歌手 | 归入 `其他/` |
| 歌词找不到匹配 | 保留原位 |
| 目标文件已存在 | 加 `__dup1`, `__dup2` 后缀 |
| 元数据读取失败 | 回退到文件名解析 |
| `read_audio_meta` 抛异常 | 跳过该文件，CSV 标记错误 |

## 输出文件

每次运行生成两个文件（在 `目标根目录` 同级）：

1. **`整理报告_dryrun_时间戳.csv`** — 完整行动计划
   - 列：类型、原路径、目标路径、歌手、第一歌手、歌曲、状态、音质、大小KB、来源
2. **`operations_时间戳.log`** — 操作日志（用于手动回滚）

## CSV 状态字段值

| 状态 | 含义 |
|------|------|
| `干跑-待移动` | 待移动到目标位置 |
| `干跑-待备份` | 待移动到 `_低音质备份/` |
| `干跑-待匹配` | 歌词待移动到匹配的音乐目录 |
| `干跑-高音质-待移动` | 比现有的好，要替换 |
| `干跑-被高音质取代-待备份` | 被高音质文件取代 |
| `无匹配-保留原位` | 没找到对应音乐，保留原位 |
| `(保留原位)` | 同上 |
| `错误: ...` | 处理失败 |

## 注意事项

1. **首次必须 dry-run** — 3 万文件，必须先看报告
2. **CSV 用 Excel 打开** — UTF-8 BOM 已加，列对齐良好
3. **`_低音质备份/` 可恢复** — 文件只是被移走，不删除，需要恢复直接 cp 回去
4. **不要在源目录运行** — 脚本会扫 `attachments/` (专辑封面) 自动跳过
5. **多歌手歌的"一级目录"** — 只取 `&` 前面的第一位歌手（如 `Alan Walker & K-391 - X.flac` → 归入 `A/Alan Walker/`）
6. **歌词文件** — 命名规范中带 `歌手 - 歌曲` 的优先匹配；带 `-` 不带空格的次之；完全不匹配保留原位

## 推荐流程

```bash
# 第 1 步：干跑（几秒到几分钟，取决于 NAS 速度）
python3 organize_music.py --no-tag 2>&1 | tee /tmp/dryrun.log

# 第 2 步：看报告（关键！看几个抽样行）
# 比如：周杰伦、王菲、Coldplay 这种大歌手目录
# 检查"目标路径"列是否合理

# 第 3 步：如果想用 ID3 标签（更准确但慢 10x）
python3 organize_music.py  # 默认会读 ID3

# 第 4 步：执行
python3 organize_music.py --apply

# 第 5 步：核对
ls /volume4/media2/音乐_整理/Z/周杰伦 | head -10
ls /volume4/media2/音乐_整理/_低音质备份 | head -10
```

## 已知限制

- `pypinyin` 装不上时部分中文歌手会归到 `其他/`
- NAS 上 IO 慢，3 万文件 no-tag 模式约 1-2 分钟，读 ID3 约 10-30 分钟
- 标题里含 `&` 的可能被误判（少见）

## 故障排查

| 症状 | 原因 | 解决 |
|------|------|------|
| 找不到 `mutagen` | 没装 | `python3 -m pip install --break-system-packages mutagen` |
| 找不到 `pypinyin` | 没装 | `python3 -m pip install --break-system-packages pypinyin` |
| 跑得很慢 | 在读 ID3 | 加 `--no-tag` |
| 大量"无匹配-保留原位" | 歌词命名风格不统一 | 检查几个 `.lrc` 文件名格式 |
| 大量"错误"行 | 文件被占用或权限 | `ls -la` 看一下原路径 |

## 修订历史

- 2026-06-18: 首次交付

---
name: "music-library-organizer"
displayName: "Music Library Organizer / 音乐库整理"
description: "音乐库整理工作流：扫描→规划→主人确认→软删除→验证→清理。强调安全流程。Safe-by-default music library organizer with soft-delete + mandatory owner confirmation."
tags: ["music", "organize", "backup", "safety", "chinese", "media-management", "file-management", "python"]
author: "openclaw-user"
version: "1.0.1"
---

# 音乐库整理 Skill (Music Library Organizer)

> 整理 `/volume4/media2/音乐` 下的所有音乐和歌词文件，按歌手字母 A-Z 归类 + 重命名 + 去重。
> **核心安全原则：永不立即删除，整理后必须主人确认才能彻底删除。**
>
> A safe-by-default music library organizer with 6-stage workflow: scan → plan → owner confirms → soft-delete → verify → cleanup. Hard deletes require explicit owner confirmation and 5-second delay.

## 适用场景 / Use Cases

- 首次整理一个新下载的乱序音乐库 / First-time organization of a new music library
- 重新整理已有的字母目录 / Reorganizing existing A-Z folders
- 合并多个来源（备份、低音质备份、新下载） / Merging multiple sources (backups, low-quality backups, new downloads)
- 修正之前整理时的错误（歌手/歌名反了、命名格式不统一） / Fixing previous organization errors (artist/song swapped, inconsistent naming)

## 核心原则（铁律）

### 🚨 安全铁律（不可违反）

1. **永不立即删除文件**
   - 默认所有"删除"都是**软删除**（移到 `_已删除_时间戳/` 目录）
   - 只有**主人明确说"真删/硬删/永久删除/rm -rf"**才能物理删除
   - 删除前必须**二次确认**（报大小+文件数+不可恢复）
   - 不可逆操作必须延迟 5 秒执行

2. **整理后必须验证**
   - 每个阶段完成后跑验证脚本
   - 对比整理前后的差异
   - **主人确认无误后才能继续下一步**

3. **必须分阶段**
   - 每个阶段独立可回滚
   - 失败立即停止，不进入下一阶段

---

## 整理方法论（6 阶段工作流）

### 阶段 0：调研（必做）

在动文件之前，先调研：
- 目录大小（`du -sh`）
- 文件数量（`find -type f | wc -l`）
- 顶层结构（`ls -la`）
- 命名格式（抽样看 20-30 个文件）
- **绝不能假设**之前整理过/没整理过，每次必须实际看

### 阶段 1：扫描 + 分类

扫描所有文件，按 4 类分类：

| 分类 | 特征 | 处理方式 |
|------|------|---------|
| 正常 | 父目录=歌手，文件名=`歌手 - 歌名.ext` | 跳过 |
| 反了 | 父目录=歌名，文件名=`歌名 - 歌手.ext` | 修正 |
| 命名不一致 | 文件名用 `-` 不是 ` - `（无空格） | 改名 |
| 孤儿 | 无分隔符、无法识别 | 标记给主人看 |

**关键工具**：
- 父目录 = 歌手（最权威）
- 文件名解析：先 ` - `（带空格），后 `-`（不带空格）
- ID3 标签作为补充（mutagen）

### 阶段 2：生成计划（dry-run）

不修改任何文件，生成：
- 移动清单（从 A 移到 B）
- 改名清单（X.ext → Y.ext）
- 冲突清单（目标位置已存在）
- 预计影响（文件数、大小、磁盘释放）

输出为 CSV 或 JSON，**让人工审阅**。

### 阶段 3：用户确认

向主人报告：
- 总操作数
- 涉及歌手/字母
- 冲突案例（如果有）
- 风险点

**等待主人明确说"执行"**才能继续。

### 阶段 4：执行（软删除默认）

按顺序执行：
1. 移动文件到新位置
2. 改名
3. 清理空目录

**绝不删除任何文件**——只移动和重命名。

### 阶段 5：验证

执行后立即验证：
- 文件总数是否一致
- 抽样几个文件确认位置/名称
- 反了的、命名不一致的统计应该都是 0
- 生成验证报告

### 阶段 6：主人确认后清理

只有主人说"清理"/"删除 X"时：
1. 报告待删内容（大小+文件数）
2. 二次确认
3. 5 秒延迟
4. 执行 `rm -rf`
5. 验证目录已消失
6. 记录到日志

---

## 目标目录结构

```
/volume4/media2/音乐/
├── A/
│   ├── A1 TRIP/
│   │   ├── A1 TRIP - 放空.flac
│   │   └── A1 TRIP - 放空.lrc
│   └── ...
├── B/
│   ├── Beyond/
│   │   ├── Beyond - 海阔天空.flac
│   │   └── Beyond - 海阔天空.lrc
│   └── ...
├── Z/
│   ├── 周杰伦/
│   │   ├── 周杰伦 - 晴天.flac
│   │   └── 周杰伦 - 晴天.lrc
│   └── ...
├── 其他/                          # 数字开头/无法识别的
└── _低音质备份/                    # 替换掉的低质版本（保留）
```

## 命名规则

### 音乐文件
- 单歌手：`歌手 - 歌名.格式` （如 `周杰伦 - 晴天.flac`）
- 多歌手：统一用 `&` 连接（如 `Alan Walker & K-391 - Different World.flac`）
- 缺歌手：仅 `歌曲名.格式`，归入 `其他/`

### 歌词文件
- 与音乐文件主名一致：`歌手 - 歌名.lrc`
- 找不到匹配时保留原位

### 文件名格式铁律
- 分隔符必须用 ` - `（带空格）
- 不用 `-`（不带空格）、不用 `_`

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

被替换的低音质文件 → `目标根目录/_低音质备份/原路径`（**保留**，不删除）

## 中文歌手名首字母

- 使用 `pypinyin` 库转拼音首字母
- 数字开头或无法识别 → `其他/`

---

## 推荐脚本

### 现有脚本（已验证可用，全部打包在 `scripts/` 子目录中）

| 脚本 | 用途 |
|------|------|
| `scripts/organize_music.py` | 主整理脚本（dry-run + apply） |
| `scripts/dedup_music.py` | 按音质优先级去重 |
| `scripts/rematch_lyrics.py` | 重新匹配歌词到音乐 |
| `scripts/clean_orphan_lyrics.py` | 清理孤立歌词（软删除） |
| `scripts/restore_orphan_lyrics.py` | 从软删除目录恢复歌词 |
| `scripts/cleanup_empty_dirs_v2.py` | 清理空目录（软删除，v2 修正版） |

脚本位置：`scripts/` 子目录（已随 skill 打包）

**完整脚本说明**：参见 `scripts/README.md`
**主脚本详细文档**：参见 `scripts/organize_music.README.md`

---

## 完整工作流示例

### 场景 A：首次整理（无整理历史）

```bash
# 1. 调研
ls -la /volume4/media2/音乐/  # 看顶层
du -sh /volume4/media2/音乐/
find /volume4/media2/音乐/ -type f | wc -l

# 2. 干跑
python3 /root/.openclaw/workspace/scripts/organize_music.py --no-tag
# 输出: 整理报告_dryrun_时间戳.csv

# 3. 给主人看报告
# 报告: 影响 X 文件, Y GB, 涉及 Z 个歌手

# 4. 主人确认
# "执行"

# 5. 真执行
python3 /root/.openclaw/workspace/scripts/organize_music.py --apply

# 6. 验证
ls /volume4/media2/音乐/A/ | head -10
ls /volume4/media2/音乐/Z/ | head -10

# 7. 生成清单（可选）
python3 /root/.openclaw/workspace/scripts/generate_music_xlsx.py
```

### 场景 B：整理备份目录（如 `_低音质备份/`）

```bash
# 1. 扫描备份
du -sh /volume4/media2/音乐/_低音质备份/
find /volume4/media2/音乐/_低音质备份/ -type f | wc -l

# 2. 检查冲突
# 找备份里文件 vs 主目录同名文件 → 报告冲突

# 3. 给主人看 dry-run
# "X 个文件将移动到主目录, Y 个冲突（主目录更优，跳过）"

# 4. 主人确认

# 5. 执行
# - 移动非冲突文件
# - 删除冲突的备份文件（**不删主目录版本**）
# - 删除空目录

# 6. 验证 + 生成清单
```

### 场景 C：修正歌手/歌名反了的文件

```bash
# 1. 扫描所有"反了"的文件
# 规则：父目录=歌名（looks_like_song_title），文件名=歌手

# 2. 报告
# "X 个文件需要：改名 + 移动到正确歌手目录"
# "Y 个是父目录=歌名但其实是多歌手"

# 3. 主人确认

# 4. 执行：重命名 + mv + 删空目录
```

---

## 安全检查清单

每次执行前：

- [ ] 已调研（du, find, ls）
- [ ] 已生成 dry-run 报告
- [ ] 已给主人看报告（影响范围）
- [ ] 主人明确说"执行"
- [ ] 5 秒延迟后执行（针对删除）
- [ ] 验证完成（文件数一致、抽样确认）
- [ ] 记录到 memory

每次删除前：

- [ ] 主人明确说"硬删/真删/rm -rf/永久删除"
- [ ] 报告：大小、文件数、不可恢复
- [ ] 二次确认（"确认真删除"）
- [ ] 5 秒延迟
- [ ] 删除后验证目录已消失
- [ ] 记录到 memory

---

## 错误处理

| 错误 | 处理 |
|------|------|
| 权限拒绝 | `chmod -R a+rX` 后重试 |
| 磁盘满 | 立即停止，报告 |
| 目标位置冲突 | 报告给主人，**不要自动覆盖** |
| ID3 标签解析失败 | 回退到文件名解析 |
| 父目录=歌名 | 报告给主人，让主人决定 |
| 无法识别的格式 | 移到 `其他/` |

---

## 关键教训（来自历史任务）

### 2026-06-19 教训
- **误删了 26 个 .lrc 歌词**（脚本 bug + 没二次确认）
- **教训**：所有删除必须软删除 + 二次确认
- **修正**：MEMORY.md 加了"数据安全规则"

### 2026-06-21 教训
- **误判 `/音乐/` 已清空**（实际 46,000+ 项目还在）
- **教训**：删之前必须 `ls -la` 实际验证
- **修正**：MEMORY.md 加了"重要目录区别"

### 2026-06-21 经验
- **organize_music.py 设计良好**（dry-run 报告 + 软删除 + ID3 标签）
- **重命名 55 个文件**：用 ` - `（带空格）统一格式
- **81 个反了文件**：要重命名 + 移动到正确目录

---

## 相关文件

- 主脚本：`/root/.openclaw/workspace/scripts/organize_music.py`
- 脚本 README：`/root/.openclaw/workspace/scripts/organize_music.README.md`
- 长期记忆：`/root/.openclaw/workspace/MEMORY.md`
- 跳过清单（2026-06-21）：`/root/.openclaw/workspace/memory/skipped_conflicts_20260621.md`

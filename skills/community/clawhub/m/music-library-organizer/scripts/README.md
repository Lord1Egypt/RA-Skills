# 音乐库整理脚本 (Scripts)

本目录包含 6 个核心 Python 脚本，用于实际执行音乐库整理任务。

## 脚本清单

### 1. `organize_music.py` (39 KB) - 主整理脚本

**功能**：扫描源目录，按 A-Z/歌手/歌名 重新组织音乐和歌词文件。

**关键特性**：
- Dry-run 模式（默认）：生成 CSV 报告，不动文件
- `--apply` 模式：真执行
- ID3 标签解析（更准确）
- `--no-tag` 模式（更快）
- 拼音首字母归类（周杰伦 → Z/）
- 多歌手处理（& 连接）

**用法**：
```bash
# 干跑（推荐先看报告）
python3 organize_music.py --no-tag

# 真执行
python3 organize_music.py --apply

# 指定源/目标
python3 organize_music.py --source /path/to/music --target /path/to/output

# 限制处理文件数（调试）
python3 organize_music.py --limit 100
```

**详见**：`organize_music.README.md`

### 2. `dedup_music.py` (6.5 KB) - 去重脚本

**功能**：清理同歌手+同歌名的重复文件，按音质保留最优版本。

**去重优先级**（高 → 低）：
1. FLAC/APE/WAV（无损）
2. 320k MP3
3. 普通 MP3
4. M4A/AAC
5. 其他

**被替换的低质文件 → 软删除**到 `_低音质备份/`（保留）。

### 3. `rematch_lyrics.py` (5.8 KB) - 重新匹配歌词

**功能**：针对已整理好的音乐库，重新匹配无匹配的 `.lrc` 歌词。

**适用场景**：
- 整理后仍有孤立歌词
- 命名风格不统一的歌词

### 4. `clean_orphan_lyrics.py` (4.6 KB) - 清理孤立歌词

**功能**：扫描所有 `.lrc`，找出没有对应音频文件的孤立歌词，**软删除**到 `_已删除_孤儿歌词_<时间戳>/`。

**软删除**：文件只是被移到兜底目录，不物理删除，可恢复。

### 5. `restore_orphan_lyrics.py` (3.1 KB) - 恢复孤立歌词

**功能**：从 `_trash_orphan_lyrics_<时间戳>/` 把孤立歌词移回主目录。

**适用场景**：
- 清理后发现误删
- 想恢复所有孤立歌词

### 6. `cleanup_empty_dirs_v2.py` (3.3 KB) - 清理空目录

**功能**：删除字母/歌手目录下的空子目录，**软删除**到 `_已删除_空目录_<时间戳>/`。

**v2 版本**：修正了 v1 的描述与实际不一致问题。

---

## 安全铁律（不可违反）

🚨 **所有脚本默认是软删除**！

1. **绝不立即物理删除文件**：
   - 移动到 `_已删除_<时间戳>/` 或 `_低音质备份/`（兜底目录）
   - 只有**主人明确说"真删/硬删/rm -rf"**才能物理删除

2. **删除前必须**：
   - 报告影响（文件数、大小、不可恢复性）
   - 二次确认
   - 5 秒延迟（不可逆操作）

3. **必须分阶段**：
   - 每个阶段独立可回滚
   - 失败立即停止

---

## 依赖安装

```bash
# 推荐安装（更准确的 ID3 标签解析 + 中文歌手拼音首字母）
pip install --break-system-packages mutagen pypinyin
```

- `mutagen`：读 ID3 标签（artist, title, album）
- `pypinyin`：中文歌手名转拼音首字母

无这两个包也能跑基础版，但解析率会下降。

---

## 推荐流程

```bash
# 阶段 1：调研
ls -la /path/to/music/
du -sh /path/to/music/

# 阶段 2：干跑（只 generate report，不动文件）
python3 organize_music.py --no-tag

# 阶段 3：看报告
# 整理报告_dryrun_<时间戳>.csv

# 阶段 4：主人确认后真执行
python3 organize_music.py --apply

# 阶段 5：去重
python3 dedup_music.py

# 阶段 6：重新匹配歌词
python3 rematch_lyrics.py

# 阶段 7：清理孤立歌词（软删除）
python3 clean_orphan_lyrics.py

# 阶段 8：清理空目录（软删除）
python3 cleanup_empty_dirs_v2.py

# 阶段 9：验证
ls /path/to/music/A/ | head
ls /path/to/music/Z/ | head
```

---

## 脚本版本历史

- 2026-06-18：`organize_music.py`, `rematch_lyrics.py`
- 2026-06-19：`clean_orphan_lyrics.py`, `restore_orphan_lyrics.py`, `dedup_music.py`
- 2026-06-19：`cleanup_empty_dirs.py`（v1, 描述与实际不一致，已废弃）
- 2026-06-19：`cleanup_empty_dirs_v2.py`（修正版）

---

## 相关

- 完整 SKILL：`../SKILL.md`
- README：`../README.md`

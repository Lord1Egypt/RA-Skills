# Music Library Organizer / 音乐库整理

[English](#english) | [中文](#中文)

---

## English

**Music Library Organizer** is a safe-by-default skill for organizing local music libraries (FLAC, MP3, WAV, APE, plus `.lrc` lyrics) into a clean `A-Z / Artist / Song.ext` directory structure with quality-based deduplication.

### 🔒 Safety First

The skill's core principle is **"never delete immediately"**:

- All "deletions" default to **soft delete** (move to `_已删除_<timestamp>/` directory)
- Physical deletion (`rm -rf`) requires the user to **explicitly say** one of:
  - "硬删" / "真删" / "永久删除" / "rm -rf"
- Two-step confirmation: report size + file count + irreversibility, then wait for "confirm"
- 5-second delay before any irreversible operation
- Every stage runs a **verification pass** before moving to the next
- The user (owner) must confirm before any cleanup

### 6-Stage Workflow

1. **Research** (`du`, `find`, `ls`) — understand what you're dealing with
2. **Scan & classify** — split files into: normal, swapped, inconsistent-naming, orphan
3. **Dry-run plan** — generate a JSON/CSV plan with conflicts, never touch files
4. **User confirms** — report impacts, wait for "execute"
5. **Execute (soft-delete only)** — move/rename only, never delete
6. **Verify** — file count check, sample verification, generate report
7. **Owner confirms cleanup** — only when user says "delete" does anything get permanently removed

### Key Features

- 🎵 **Quality-based deduplication** (FLAC/APE/WAV > 320k MP3 > regular MP3)
- 🔤 **Pinyin-based first letter** (周杰伦 → Z/) using `pypinyin`
- 📁 **Standard 3-level structure**: `字母/歌手/歌手 - 歌名.ext`
- 🎤 **Multi-artist handling**: `Alan Walker & K-391 - Song.ext`
- 📝 **Lyrics (.lrc) auto-matching** to corresponding music files
- 🔄 **Reverse-renaming detection**: catches files like `歌名 - 歌手.ext` (swapped)
- 🛡️ **No silent deletes** — everything is reported before action

### Example Output

```
/music/
├── A/Alan Walker/Alan Walker - Faded.flac
├── B/Beyond/Beyond - 海阔天空.flac
├── Z/周杰伦/周杰伦 - 晴天.flac
├── 其他/                    # unclassifiable files
└── _低音质备份/              # replaced low-quality versions (preserved!)
```

### Lessons Learned

This skill incorporates hard-won lessons from real music library operations:
- **2026-06-19**: Accidentally deleted 26 `.lrc` files (no soft-delete) → now default is soft-delete
- **2026-06-21**: Misjudged that a directory was "empty" (46k files actually present) → now mandatory `ls -la` before any delete

---

## 中文

**音乐库整理** 是一个默认安全的 skill，用于整理本地音乐库（FLAC、MP3、WAV、APE，加 `.lrc` 歌词），按 `A-Z / 歌手 / 歌曲.ext` 目录结构归类，并按音质去重。

### 🔒 安全第一

本 skill 的核心原则是**"永不立即删除"**：

- 所有"删除"操作默认是**软删除**（移到 `_已删除_<时间戳>/` 目录）
- 物理删除（`rm -rf`）需要主人**明确说**以下任意一个：
  - "硬删" / "真删" / "永久删除" / "rm -rf"
- 二次确认：先报大小、文件数、不可恢复性，再等主人"确认"
- 任何不可逆操作前延迟 5 秒
- 每个阶段完成后必须**验证**，才能进入下一阶段
- 清理操作必须主人确认后执行

### 6 阶段工作流

1. **调研**（`du`、`find`、`ls`）— 看清现状
2. **扫描 + 分类** — 分为：正常、反了、命名不一致、孤儿
3. **Dry-run 计划** — 生成 JSON/CSV 计划，含冲突清单，绝不修改文件
4. **主人确认** — 报告影响范围，等主人说"执行"
5. **执行（仅软删除）** — 只移动/重命名，绝不删除
6. **验证** — 文件数核对、抽样确认、生成报告
7. **主人确认后清理** — 只有主人说"删除"时才彻底清理

### 核心功能

- 🎵 **按音质去重**（FLAC/APE/WAV > 320k MP3 > 普通 MP3）
- 🔤 **拼音首字母归类**（周杰伦 → Z/）使用 `pypinyin`
- 📁 **标准 3 级结构**：`字母/歌手/歌手 - 歌名.ext`
- 🎤 **多歌手处理**：`Alan Walker & K-391 - 歌曲.ext`
- 📝 **歌词（.lrc）自动匹配**到对应音乐文件
- 🔄 **反名检测**：发现 `歌名 - 歌手.ext` 这种错误
- 🛡️ **没有静默删除** — 所有操作前都会报告

### 目录结构示例

```
/music/
├── A/Alan Walker/Alan Walker - Faded.flac
├── B/Beyond/Beyond - 海阔天空.flac
├── Z/周杰伦/周杰伦 - 晴天.flac
├── 其他/                    # 无法识别的文件
└── _低音质备份/              # 替换掉的低质版本（保留）
```

### 血泪教训

本 skill 来自实战中吸取的教训：
- **2026-06-19**：误删 26 个 `.lrc` 文件（没软删除）→ 现在默认软删除
- **2026-06-21**：误判某目录"已清空"（实际 46,000 项还在）→ 删前必须 `ls -la` 实际验证

### 安装

```bash
clawhub install music-library-organizer
```

### 作者

由 OpenClaw 用户基于 6/18-6/21 三次实际音乐整理任务沉淀。

---

**Tags**: `music`, `organize`, `backup`, `safety`, `chinese`, `media-management`, `file-management`

**Version**: 1.0.0

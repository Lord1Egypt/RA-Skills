# 时光梳理·照片视频梳理 / Photo & Video Library Organizer

> **中文** | [English](#english)

跨多年、超大数量照片视频的整理利器 —— 找回错乱的拍摄时间与 GPS、多轮去重、统一命名，整理成可做"多年回忆精选集"的长期资料库。**全球通用，地区自适应**（中国大陆 / 海外）。

专为【跨多年、超大数量】的照片视频资料库设计。当照片视频来自手机、云盘、聊天工具、无人机等多来源，反复下载导致拍摄时间/GPS 错乱、重复泛滥、文件名混乱时，本技能把它们梳理成**时间正确、GPS 齐全、画质完整、重复较少、结构清楚**的长期资料库。

基于一次真实的 **2.5 万+ 照片 / 1500+ 视频（跨 13 年、6+ 来源）** 整理实践提炼，并经多轮后续实践（深度二次去重、GPS 来源审计、年份归档、动态照片拆分）持续修订，方法论经过实战验证，脚本拿来即用。

> 技能 ID / slug：`photo-video-organizer`（市场 URL 标识，ASCII）；展示名：**时光梳理·照片视频梳理**。

---

## ⚠️ 使用前需人工准备（技能不代劳）
1. **一份完全未处理的原始备份**（动手前必留，整理全程可逆但仍需原始兜底）。
2. **多年行程表**（哪天在哪个城市）——需自行从交通/消费记录梳理出来（数据源按地区见下）。这是给照片视频补 GPS 的前提。
3. **运行环境**：exiftool 13.x、Python 3.10+ 及 opencv/clip/torch 等依赖。
4. **人工终判**：去重候选由算法给出，需在对比图上人工核定后才移动（技能提供可交互 HTML，几分钟核几百组）。

## 🌏 地区自适应（v2.0 新增）

技能启动时判定用户地区并加载对应地区档案，核心流程全球一致，差异全部收敛在档案里：

| 差异点 | 🇨🇳 中国大陆（`references/region_cn.md`） | 🌍 海外（`references/region_global.md`） |
|---|---|---|
| 坐标系 | 国内地图是 GCJ-02，写 EXIF **必须转 WGS-84**（内置 `datum_convert.py` 离线转换+往返校验） | WGS-84 直接可用，**勿做转换** |
| 行程表数据源 | 12306、微信/支付宝账单、高德/百度轨迹、美团/酒店/ETC | Google Maps Timeline (Takeout)、机票/酒店邮件、银行账单、Uber/火车票 |
| 聊天工具文件名 | 微信 19/20 位随机 ID（不可解）、`mmexport<ms>` 取最早 | WhatsApp `IMG-YYYYMMDD-WA####`（日期是接收日） |
| 云盘生态 | 百度网盘/阿里云盘（客户端+文件区+原图） | iCloud / Google Photos / OneDrive / Dropbox（原图质量） |
| 手机导入 | 华为走鸿蒙星河互联；iPhone 走访达同步 | iPhone 走访达同步；安卓走 MTP/Google Photos |
| 视频时区 | 默认北京时间（UTC+8） | 按**拍摄地**时区换算（出境游逐文件判定） |

两类典型用户各有一份完整验证用例：`region_cn.md` §7（深圳双机用户）、`region_global.md` §7（芝加哥 iPhone+Pixel 用户）。

## ✨ 它能做什么

- **跨多年超大数量**：专为 2 万+ 照片 / 千+ 视频、跨 10+ 年的多源库设计，断点续传 + 分批，扛得住环境中断
- **找回拍摄时间**：EXIF 优先，文件名时间戳兜底，绝不用被网盘污染的 mtime
- **找回 GPS**：按"行程表"补坐标，自动做坐标系修正（国内 GCJ-02→WGS-84 + 往返校验），保留已有真实 GPS；**GPS 来源审计**区分"真实 GPS"与"行程表推算 GPS"
- **统一文件名**：`YYYYMMDD_HHMMSS_设备.ext`（视频加 `video` 前缀），按时间排序即按记忆排序
- **字节级去重**：头尾 MD5 指纹 + 全量校验（动态照片 LIVP 整包校验，封面+视频都同才算重复）
- **语义级多轮去重**：CLIP + 拍摄日期分组，同日 0.94 粗筛 → 深度轮 0.88 细筛 → 宠物等特殊主题组单独 0.98 调参；大组递归细分，25% 保留（上限 5 下限 1）
- **可交互核定**：生成对比 HTML，点击切换保留/移除，人工终判后才移动；同姿势跨景别识别、最佳照片支持水平/垂直对齐评分
- **模糊隔离**：三因子评分（清晰度百分位+边缘强度+文件大小）+ 防误伤抽检
- **覆盖度分析**：月份断档清单（哪些月全库无照片）+ 按 EXIF 年份归档
- **可逆移动**：所有"删除"移入子文件夹，保留 mtime，附回滚脚本；每阶段有进度记录纪律
- **哈希校验清单**：MD5+SHA1，传输前后比对防元数据丢失
- **导入手机/云盘**：按地区档案执行（见上表）

## 📦 安装

### 方式一：放入用户级 Skill 目录（推荐，跨项目生效）
```bash
unzip photo-video-organizer.zip -d ~/.workbuddy/skills/
```
放好后所有 WorkBuddy 会话自动可用，无需重启。

### 方式二：项目级（团队共享）
```bash
unzip photo-video-organizer.zip -d <项目目录>/.workbuddy/skills/
```

### 方式三：从 ClawHub 市场一键安装
在 WorkBuddy 客户端「技能市场」搜索 `photo-video-organizer` 或「时光梳理」安装。

### 非 WorkBuddy 环境使用
SKILL.md 是给 AI 助手的指令文档，`references/guide.md` 是完整的方法论手册（人类可直接照做），`scripts/` 是独立命令行工具（`python3 scripts/xxx.py --help` 查用法），三者都可以脱离 WorkBuddy 单独使用。

## 🔧 运行环境

| 依赖 | 说明 |
|---|---|
| exiftool 13.x | EXIF/视频元数据读写（`brew install exiftool` / [官网](https://exiftool.org/)） |
| Python 3.10+ | 脚本运行环境 |
| opencv-python, pillow, pillow-heif, numpy | 图像处理与 HEIC 读取 |
| openai-clip, torch | 语义嵌入（仅相似去重需要；首次运行自动下载权重） |
| 无 | `datum_convert.py` 仅需标准库，开箱即用 |

## 🗂️ 目录结构

```
photo-video-organizer/
├── SKILL.md                  # AI 助手指令（技能入口）
├── manifest.yaml             # 技能市场元数据
├── README.md                 # 本文件
├── LICENSE                   # MIT
├── CHANGELOG.md              # 变更日志
├── references/
│   ├── guide.md              # 完整方法论（Phase 0–8 + 坑库 + 新增 §12–15）
│   ├── region_cn.md          # 地区档案：中国大陆
│   └── region_global.md      # 地区档案：海外
└── scripts/                  # 8 个参数化脚本（无硬编码路径）
    ├── exif_scan.py          # EXIF 扫描（时间+GPS+大小）→ JSON
    ├── exact_dup.py          # 字节级完全相同检测（可续传）
    ├── similarity_embed.py   # CLIP 嵌入（照片整张；视频抽帧）
    ├── similarity_cluster.py # 聚类 + 多级递归细分 + 25% 保留
    ├── interactive_review_html.py # 可交互对比 HTML（人工核定）
    ├── move_reversible.py    # 可逆移动 + 回滚脚本
    ├── hash_manifest.py      # MD5+SHA1 哈希清单（断点续传）
    └── datum_convert.py      # GCJ-02/BD-09↔WGS-84 转换 + 往返校验
```

## 📖 快速上手（五步）

1. **备份**：复制一份完全未处理的原始备份。
2. **判定地区**：告诉 AI 助手你的照片主要来自哪个环境（大陆/海外），或直接阅读对应地区档案。
3. **修时间**：跑 `exif_scan.py` 盘点 → 按 `guide.md` Phase 1 修复拍摄时间。
4. **建行程表 → 补 GPS**：按地区档案 §2 的数据源梳理"每日所在城市"→ Phase 2 补 GPS（国内先跑 `datum_convert.py`）。
5. **去重 → 核定 → 归档**：Phase 4/5 去重 → 在对比 HTML 上人工核定 → Phase 6.5/7 归档与哈希清单 → Phase 8 导入。

## 📄 许可证

MIT — 见 [LICENSE](LICENSE)。

---

<a name="english"></a>
## English

A battle-tested workflow skill for organizing **huge, multi-year, multi-source photo & video libraries** — recover corrupted capture timestamps and GPS, deduplicate at byte & semantic level, normalize filenames, and end with a clean long-term archive ready to import into your phone or cloud album.

Built from a real-world run of **25,000+ photos / 1,500+ videos spanning 13 years and 6+ sources**, then hardened through subsequent rounds (deep second-pass dedup, GPS provenance audit, year archiving, motion-photo splitting).

### Region-aware (v2.0)
The core methodology is universal. Region-specific differences are isolated into two profiles loaded at start:

| Aspect | 🇨🇳 Mainland China (`references/region_cn.md`) | 🌍 Global (`references/region_global.md`) |
|---|---|---|
| Coordinate datum | CN map services return GCJ-02 — **must convert to WGS-84** before writing EXIF (bundled offline `datum_convert.py` with round-trip verification) | WGS-84 works as-is — **do not convert** |
| Itinerary sources | 12306 rail, WeChat/Alipay statements, Amap/Baidu traces | Google Maps Timeline (Takeout), airline/hotel emails, bank statements, Uber |
| Chat filename forensics | WeChat 19/20-digit random IDs (unsolvable), `mmexport<ms>` earliest wins | WhatsApp `IMG-YYYYMMDD-WA####` (date = receive date) |
| Cloud albums | Baidu Netdisk / Aliyun Drive (desktop client, original quality) | iCloud / Google Photos / OneDrive / Dropbox |
| Video timezone | Beijing time (UTC+8) default | Convert by **capture-place** timezone, per file |

Both profiles include a full worked example: `region_cn.md` §7 (Shenzhen dual-phone user) and `region_global.md` §7 (Chicago iPhone+Pixel user).

### Highlights
- **Timestamp recovery** — EXIF first, parseable filename timestamps as fallback, **never** file mtime (cloud re-downloads poison it)
- **GPS backfill from itinerary** — with datum correction and provenance audit (real GPS vs itinerary-inferred GPS)
- **Multi-round semantic dedup** — CLIP + date grouping: same-day 0.94 → deep round 0.88 → pet/special-theme groups re-clustered at 0.98; recursive splitting of large clusters; keep ~25% per group (max 5, min 1)
- **Interactive human review** — generated HTML lets you toggle keep/remove per photo in minutes; algorithm proposes, human decides
- **Byte-exact dedup** — head/tail MD5 fingerprints + full verification; LIVP motion photos compared as whole packages
- **Blur isolation** — 3-factor scoring with sample-based false-positive checking
- **Coverage analysis** — month-gap report + EXIF-year archiving
- **Everything reversible** — candidates are *moved* (never deleted) with mtime preserved, rollback scripts, and per-phase progress logs
- **Hash manifests** — MD5+SHA1 before/after any transfer

### Install
```bash
unzip photo-video-organizer.zip -d ~/.workbuddy/skills/   # WorkBuddy
```
Or use standalone: `references/guide.md` is a complete human-readable manual; `scripts/` are independent CLI tools (`python3 scripts/xxx.py --help`).

### Prerequisites
exiftool 13.x, Python 3.10+, packages: `opencv-python pillow pillow-heif numpy openai-clip torch` (datum_convert.py needs stdlib only).

### License
MIT — see [LICENSE](LICENSE).

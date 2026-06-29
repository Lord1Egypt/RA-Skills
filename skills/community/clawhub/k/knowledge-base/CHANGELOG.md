# CHANGELOG — 进击的知识库

## v2.4.0 (2026-06-14)

### 📝 抖音视频文案提取
- **`parsers/douyin.py`**：新增 `_extract_description()` 方法，通过 `yt-dlp --dump-json` 提取视频描述（文案旁白）
- 下载后自动保存 `<视频名>.caption.txt` 旁白文件
- JSON 输出新增 `description` 字段
- **`agent.py`**：`download_douyin()` 同步支持文案提取 + 保存 caption 文件

### 🏷️ 标签
- 新增 `caption-extraction` 标签

---

## v2.3.0 (2026-06-14)

### 🔐 去个人化改造
- **`agent.py`**：移除硬编码的 `TENCENT_SPACE_ID`、`INDEX_FILE_ID`、`INDEX_SHEET_ID`，改为从环境变量 `KB_TENCENT_SPACE_ID` / `KB_INDEX_FILE_ID` / `KB_INDEX_SHEET_ID` 读取
- **`add_to_sheet.py`**：同样移除硬编码 ID，统一走环境变量
- **`agent.py`**：`SPH_SKILL_PATH` 不再硬编码用户路径，改为自动探测 `.workbuddy/skills/sph-download/` 目录
- **SKILL.md**：新增 `slug: knowledge-base`、`tags`、`token_budget` 等 frontmatter 字段
- **SKILL.md**：重写「首次安装配置」章节，提供完整新用户引导（前置依赖 → 创建空间 → 建表 → 配环境变量 → 验证）

### 📝 文档
- SKILL.md 版本 → 2.3.0，frontmatter 新增 slug/tags/owner_type/token_budget
- README.md 版本 → 2.3.0，快速开始章节改为环境变量配置方式
- DESIGN.md 版本 → 2.3.0，架构图修正（sph-download skill → parsers/sph.py），补充去个人化设计说明

### 🛡 安全
- 发布给新用户不再暴露个人信息
- 每个用户独立完成腾讯文档授权和空间配置

---

## v2.2.0 (2026-06-14)

### ✨ 品牌升级
- **更名为「进击的知识库」**：更有性格、更有记忆点的品牌名
- **全新介绍文案**：突出"发个链接就完事"的核心体验
- **SKILL.md frontmatter** 重写，优化触发词和描述

---

## v2.1.1 (2026-06-14)

### 🔧 修正
- **视频号下载方案统一**：新增 `parsers/sph.py`，使用自研 sph-download 方案（`sph.litao.workers.dev` API），替代之前文档中引用的外部 `sph-download skill`
- **SKILL.md** 描述修正：`"视频类全部 yt-dlp 方案"` → 明确区分视频号/抖音/小红书各自方案
- **依赖清单精简**：移除 `sph-download skill` 外部依赖（现内置为 `parsers/sph.py`）

### 📝 文档
- README.md 更新视频号使用示例、工作原理图、文件结构
- SKILL.md 更新视频号处理步骤、文件结构

---

## v2.1.0 (2026-06-14)

### 📝 文档完善（SkillHub 发布准备）
- 新增 **DESIGN.md**：架构设计文档，含架构总览、组件设计、数据流、安全分析
- 新增 **CHANGELOG.md**：版本变更记录（本文件）
- **README.md** 全面更新：修复"待接入"状态 → 全部 ✅、添加版本标注、完善依赖清单、补充使用示例
- **SKILL.md** 版本号更新至 v2.1.0

### 🛡 安全
- DESIGN.md 中完成 subprocess 调用安全审计，确认无风险

---

## v2.0.0 (2026-06-14)

### 🚀 重大改造
- **小红书方案重写**：从 web_fetch + 正则解析 → yt-dlp 方案
  - 旧方案只提取文本，无法下载视频
  - 新方案一行 yt-dlp 命令完成下载，与抖音完全统一
  - `parsers/xiaohongshu.py` 完整重写
- **新增 `upload_to_docs.py`**：一键完成 pre_import → COS PUT → async_import → poll → add_to_sheet
- **视频上传完整流程打通**：小红书/抖音/视频号视频均能上传腾讯文档并在线播放

### ✨ 新增
- `upload_to_docs.py`：一站式上传脚本
- `parsers/xiaohongshu.py`：yt-dlp 版小红书下载器
- `parsers/douyin.py`：yt-dlp 版抖音下载器
- `parsers/wechat_article.py`：公众号文章解析器

### 🔧 改进
- 知识库管理 Skill 中文名正式确定

---

## v1.0.0 (2026-06-13)

### 🎉 初始发布
- 基础 `agent.py` CLI 入口
- 视频号下载支持（调用 sph-download skill）
- 公众号文章解析（web_fetch + 正则）
- 来源自动识别（视频号/抖音/小红书/公众号）
- 腾讯文档上传 + 0 号索引写入
- 配置式空间 ID / 表格 ID 管理

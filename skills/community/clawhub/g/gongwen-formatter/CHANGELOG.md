# Changelog

本文件记录 official-doc（gongwen-formatter）所有版本的变更。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [1.1.9] - 2026-09-22

### 元数据（三平台同步 · SkillHub 标题双语化）

#### Changed
- `displayName` 改为中英双语 `Gongwen Formatter 公文格式转换`，便于中文用户在 SkillHub 检索（无功能变更）
- 三平台同步发布（GitHub + ClawHub + SkillHub）

## [1.1.8] - 2026-09-20

### 格式增强（间隔号序号规范化为公文标准序号）

#### Changed
- **间隔号序号规范化**：识别到「一 · 源头」「2 · 源头」间隔号体例时，
  不再原样保留，而是改写为公文标准序号：
  - `##`（一级标题）：「一 · 源头」→「一、源头」，阿拉伯数字自动转中文数字（「2 · 」→「二、」）
  - `###`（二级标题）：「五 · 天长专章」→「（五）天长专章」
  - 新增 `normalize_heading_number()`，在 `heading_open` 渲染前原地改写 children 首 token
- 结构性标题（「结语 ·」「附一 ·」等）保持原样，不套序号

## [1.1.7] - 2026-09-20

### 格式修复（序号去重正则未覆盖间隔号体例，导致自动编号与原文序号重复）

#### Fixed
- **间隔号序号未被识别**：涌现写作交付成稿常用「一 · 源头」「五 · 天长专章」等间隔号体例，
  此前 `has_heading_number()` 仅识别「一、」「（一）」「1.」「第X章」四种格式，
  间隔号写法匹配不上 → 引擎判定"原文没带序号" → 自动补号，产生「二、一·源头」「（一）五·天长专章」等重复
  - 修复：新增 `[一二三四五六七八九十]{1,3}\s*[·・•.]\s*` 和 `\d{1,2}\s*[·・•]\s*` 两条正则
  - 同时增加结构性标题识别：`结语 ·`、`引言 ·`、`附一 ·`、`附录` 等，
    这些标题本身即序号终结标记，不应再追加公文序号

## [1.1.6] - 2026-09-14

### 格式修复（响应跨任务调用反馈：合同/协议"一行一要素"被合并为单段）

#### Fixed
- **连续非空行被合并为单段**：Markdown 中连续的非空行（行间为软换行 `softbreak`）此前被解析为同一个段落，
  "甲方：/住所：/法定代表人："这类一行一要素的协议抬头会被挤在同一段内显示
  - 根因：`render_inline_with_formatting` 对 `softbreak` 直接 `pass`，行边界信息在渲染阶段被丢弃
  - 修复：新增 `split_inline_on_linebreaks()`，在 `paragraph_open` 处按 `softbreak`/`hardbreak`
    将 inline children 拆分为多个独立段，每段独立应用两端对齐 + 固定行距 + 首行缩进 640 twips（2 字）
  - 效果：每个源码行还原为独立段落，各自首行缩进 2 字，消除段内断行造成的左边缘参差

#### Notes
- 本版一并纳入此前仅写入代码 docstring、未落到 CHANGELOG / 版本号文件的 v1.1.5 标题层级重定义：
  `#` 大标题（方正小标宋简体二号，居中，一律不加序号）/ `##` 一级标题（黑体三号）/
  `###` 楷体_GB2312 加粗 / `####` 仿宋_GB2312 加粗；标题原文已带序号时不再自动补序号

## [1.1.4] - 2026-07-15

### 格式修复（对齐公文规范，响应跨任务调用反馈）

#### Fixed
- **加粗句（`**text**`）修复**：由"黑体不加粗"改为"楷体_GB2312 加粗"
  - 原问题：`**一是强化谋划动员**` 这类段首加粗句被渲染为黑体三号且无加粗效果，强调完全丢失
  - 根因：`render_inline_with_formatting` 的 strong 分支使用 `set_font(run, '黑体', font_size)`，black 默认 False
  - 修复：strong 分支改为 `set_font(run, '楷体_GB2312', font_size, bold=True)`，符合公文段首"一是/二是"句式标准格式
- **三级标题（`###`）修复**：由"楷体不加粗"改为"楷体_GB2312 加粗"
  - 根因：h3 分支的标题文字和前缀均未传 `bold=True`
  - 修复：h3 分支统一传 `bold=True`，符合 GB/T 9704 二级标题（（一））楷体加粗规范
- `render_inline_with_formatting` 增加 `bold` 参数，支持标题整体加粗

#### 保持不变的格式
- 黑体标题（`#`/`##`）不加粗（用户明确要求，黑体本身已足够醒目）
- 正文仿宋三号不加粗
- 斜体楷体不加粗
- 链接蓝色下划线

## [1.1.3] - 2026-07-14

### 修复（响应 v1.1.2 后 SkillSpector 二次审计 7 findings）

#### Fixed
- 修复 v1.1.2 漏改：README.md / README_CN.md / skill.md / skill.json 中残留的 `>=` 全部改为 `~=`（依赖版本一致性）
  - 根因：v1.1.2 只改了 requirements.txt 和 setup.py，漏改了 README 安装示例、skill.md 依赖表、skill.json dependencies 字段
  - SkillSpector 扫描所有文件，因此仍报告 `>=` 为 Unpinned Dependencies

#### Added
- frontmatter 增加 `allowed-tools` 字段，声明 filesystem（写 .docx）和 net.http（图片下载，可关闭）两项权限
  - 目的：让 ClawHub SkillSpector 能从 frontmatter 识别权限声明，减少 MCP Least Privilege finding

#### SkillSpector v1.1.2 二次审计 7 findings 评估
| Finding | 评估 | 处理 |
|---------|------|------|
| MCP Least Privilege (Medium) | stale — 权限声明已在 v1.1.2 添加 | 本次通过 allowed-tools 增强声明 |
| Description-Behavior Mismatch (Medium) | 过度修改 — 图片下载是合理功能 | 不采纳，保留现有设计 |
| Context-Inappropriate Capability (Medium) | 过度修改 — 已有白名单+开关 | 不采纳，保留现有设计 |
| Missing User Warnings × 2 (Medium) | stale — README 警告已添加 | 等 ClawHub 缓存刷新 |
| Unpinned Dependencies × 2 (Low) | 真实漏改 — 残留 `>=` | 本次修复 |

## [1.1.2] - 2026-07-14

### 安全升级（响应 ClawHub SkillSpector 审计）

#### Added
- `md_to_docx()` 新增 `download_images` 参数（默认 `True`），受限网络环境可设为 `False` 完全关闭网络请求
- `skill.md` 增加"权限声明"段落，按最小权限原则披露网络访问/文件读写/不读取环境变量/不调用 subprocess
- README 中英文版增加 "图片下载网络请求说明 / Network Access Disclosure for Image Download" 用户警告段落

#### Security
- `download_image()` 增加 URL scheme 白名单（仅 `http://`/`https://`/`data:image`），防止 SSRF
- 其他 scheme（`file://`、`ftp://` 等）静默跳过，不发起网络请求
- `requirements.txt` 改用 `~=` 兼容版本锁定（`python-docx~=1.1.0`、`markdown-it-py~=3.0.0`），平衡安全与兼容性

## [1.1.1] - 2026-07-13

#### Changed
- 添加 ClawHub 触发词：`公文格式转换`、`转换公文格式`
- ClawHub slug 改为 `gongwen-formatter`（`official-doc` 已被占用，`official-` 前缀受保护）
- 三平台同步发布（GitHub + ClawHub + SkillHub）

## [1.1.0] - 2026-07-12

#### Added
- 引入 `markdown-it-py` 解析器替代逐行 `split('\n')`，支持多行段落、嵌套列表
- `#` 标题智能判断：单个 `#` 视为大标题（居中不加序号），多个 `#` 视为一级标题（加序号）
- 首行缩进精确对齐国标（640 twips = 2个三号汉字宽度，1汉字=16pt=320twips）
- 新增表格、图片、超链接、代码块、嵌套列表支持
- 加粗文本（`**text**`）自动转为黑体
- 斜体文本（`*text*`）自动转为楷体

#### Fixed
- 黑体字体不再设置 `bold=True`（用户反馈"黑体不需要加粗处理"）
- 移除所有黑体/楷体的 `bold=True` 设置

## [1.0.0] - 2026-07-10

#### Added
- 初始版本：基于 GB/T 9704-2012 标准，将 Markdown 转换为党政机关公文格式 Word 文档
- 实现基础标题层级、段落、列表转换
- 国标页面设置：A4、上 3.7cm/下 3.5cm/左 2.8cm/右 2.6cm、行距 26pt
- 字体规范：方正小标宋/黑体/楷体_GB2312/仿宋_GB2312/宋体

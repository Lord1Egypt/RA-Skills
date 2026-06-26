---
name: mukun-md-push-wechat
description: 将 Markdown 文件转换为符合微信公众号规范的 HTML 文件，并可进一步推送到微信公众号草稿箱。支持文章模式（默认，含 7 种预设样式）和新闻模式（--news）。支持推送 Markdown 到稀土掘金草稿箱。当用户提到"md转微信html""推送公众号""转换微信公众号格式""推送到掘金""掘金草稿"等意图时触发此技能。
allowed-tools: Read, Bash, Write
---

# Markdown 转微信公众号 HTML 并推送草稿箱

## 核心能力

将 Markdown 文件转换为符合微信公众号规范的 HTML 文件，支持三级标题、正文、粗体、链接、行内代码、代码块、引用块、表格等常用格式。所有 CSS 内联到 style 属性，确保微信渲染兼容。

支持进一步将转换后的 HTML 推送到微信公众号草稿箱。

## 场景决策

| 用户意图 | 执行方式 | 脚本命令 |
|---------|---------|---------|
| 「把这篇md转成微信html」「md转微信格式」「生成微信html」 | 仅转换 HTML | `${CODEBUDDY_SKILL_DIR}/scripts/md2wechat_html.py` |
| 「推送/发布到公众号」「先转换再推送到公众号」 | 转换 + 推送草稿箱 | `${CODEBUDDY_SKILL_DIR}/scripts/push_daily.py` |
| 「推送到掘金」「掘金草稿」「发到掘金」 | 推送掘金草稿箱 | `${CODEBUDDY_SKILL_DIR}/scripts/push_juejin.py` |

**决策原则**：技能 2（推送公众号）已包含技能 1（转换），技能 3（推送掘金）独立使用 mark_content，无需同时调用。

**默认模式**：用户未明确指定时，使用文章模式（`--article`）。仅在以下情况使用新闻模式（`--news`）：
- 用户明确说"新闻模式""用新闻模式""--news"
- 上文对话已在讨论新闻日报、周报等内容
- Markdown 内容明显为板块化日报格式（含多个独立新闻板块）

**模式速查**：
| 模式 | 标志 | 独立脚本 | 适用场景 |
|------|------|---------|---------|
| 文章模式 | `--article`（默认） | `md2article_html.py` | 技术实践、成语典故、长文叙事（配色通过 config.yaml 控制）|
| 新闻模式 | `--news` | `md2news_html.py` | AI 周报、行业动态汇总（板块化日报，需用户明确指定）|

### 文章模式预设样式

文章模式内置 7 种预设样式，用户用自然语言描述即可自动匹配。每个预设对应 `references/` 目录下一个独立的 YAML 配置文件，既可被 SKILL.md 用自然语言匹配，也可直接通过 `--config` 传入脚本使用。

| 预设 | 配置文件 | 视觉特征 | 自然语言触发词（含任一即匹配） |
|------|---------|---------|--------------------------|
| 默认 | `references/article_default.yaml` | 白底灰字 + 棕橘胶囊标题 | 默认、默认样式、白色、白底、常规、简洁、干净、基础 |
| 泛黄怀旧 | `references/article_nostalgic.yaml` | 古卷泛黄底色 + 深棕胶囊标题 | 怀旧、泛黄、古风、古卷、黄底、暖黄、米黄底、历史、典籍、复古 |
| 科技蓝紫 | `references/article_modern.yaml` | 白底 + 蓝紫胶囊标题 + 深蓝封面 | 科技、蓝紫、科技蓝紫、蓝紫渐变、AI、技术、现代、前沿、潮流、深蓝封面 |
| 青绿引号 | `references/article_journal.yaml` | 米白底 + 青绿引号线 H2（大 Q + 引号包裹标题） | 青绿、青绿引号、引号标题、引号线、文艺、杂志、专栏、清爽、雅致、小清新 |
| 角标绿条 | `references/article_growth.yaml` | 白底 + 黄色编号角标 + 绿色标签块 H2 | 角标、角标绿条、角标编号、编号角标、badge、清单、步骤、运营、资讯、拆解、模块化、绿底封面 |
| 中轴蓝卡 | `references/article_blueprint.yaml` | 冷灰底 + 中轴蓝色编号卡 H2（居中编号 + 两侧横线） | 中轴、中轴蓝卡、中轴编号、编号卡、center、灰底、冷灰、蓝灰底、蓝色、产品文档、技术手册、结构化、规范、正式 |
| 紫绿清韵 | `references/article_scholar.yaml` | 白底 + 紫色胶囊框 H2（紫底紫字紫左边）+ 翠绿 H3 + 正文首行缩进 | 清韵、紫绿、紫绿清韵、紫胶囊、紫色胶囊、紫框、双色、双色对比、技术博客、深度技术、研究笔记、思辨、学术、学者、码上菩提 |

**匹配规则**：
- 用户提及"默认样式"/"白色"/"白底"/"常规"/"简洁"/"干净"/"基础" → 使用 `${CODEBUDDY_SKILL_DIR}/references/article_default.yaml`
- 用户提及"怀旧"/"泛黄"/"古风"/"古卷"/"黄底"/"暖黄"/"米黄底"/"历史"/"典籍"/"复古" → 使用 `${CODEBUDDY_SKILL_DIR}/references/article_nostalgic.yaml`
- 用户提及"科技"/"蓝紫"/"科技蓝紫"/"蓝紫渐变"/"AI"/"技术"/"现代"/"前沿"/"潮流"/"深蓝封面" → 使用 `${CODEBUDDY_SKILL_DIR}/references/article_modern.yaml`
- 用户提及"青绿"/"青绿引号"/"引号标题"/"引号线"/"文艺"/"杂志"/"专栏"/"清爽"/"雅致"/"小清新" → 使用 `${CODEBUDDY_SKILL_DIR}/references/article_journal.yaml`
- 用户提及"角标"/"角标绿条"/"角标编号"/"编号角标"/"badge"/"清单"/"步骤"/"运营"/"资讯"/"拆解"/"模块化"/"绿底封面" → 使用 `${CODEBUDDY_SKILL_DIR}/references/article_growth.yaml`
- 用户提及"中轴"/"中轴蓝卡"/"中轴编号"/"编号卡"/"center"/"灰底"/"冷灰"/"蓝灰底"/"蓝色"/"产品文档"/"技术手册"/"结构化"/"规范"/"正式" → 使用 `${CODEBUDDY_SKILL_DIR}/references/article_blueprint.yaml`
- 用户提及"清韵"/"紫绿"/"紫绿清韵"/"紫胶囊"/"紫色胶囊"/"紫框"/"双色"/"双色对比"/"技术博客"/"深度技术"/"研究笔记"/"思辨"/"学术"/"学者"/"码上菩提" → 使用 `${CODEBUDDY_SKILL_DIR}/references/article_scholar.yaml`
- 用户未提及任何风格关键词 → **默认使用 `references/article_default.yaml`**


## 技能 1：Markdown → 微信 HTML

调用脚本：
```bash
python3 ${CODEBUDDY_SKILL_DIR}/scripts/md2wechat_html.py <input.md> [output.html]
```

两种转换模式：
- **文章模式（默认，`--article`）**：长文叙事渲染，支持 7 种预设样式（默认、泛黄怀旧、科技蓝紫、青绿引号、角标绿条、中轴蓝卡、紫绿清韵），通过 `--config` 参数指定样式配置
- **新闻模式（`--news`）**：板块化日报格式，报纸风格配色，支持通过 `config.yaml` 的 `style.news` 节点自定义样式

示例：
```bash
# 文章模式（默认，使用默认样式）
python3 ${CODEBUDDY_SKILL_DIR}/scripts/md2wechat_html.py article.md article_wechat.html

# 文章模式（指定预设样式）
python3 ${CODEBUDDY_SKILL_DIR}/scripts/md2wechat_html.py --config ${CODEBUDDY_SKILL_DIR}/references/article_nostalgic.yaml article.md article_wechat.html

# 新闻模式
python3 ${CODEBUDDY_SKILL_DIR}/scripts/md2wechat_html.py --news news.md news_wechat.html

# 新闻模式（自定义样式）
python3 ${CODEBUDDY_SKILL_DIR}/scripts/md2wechat_html.py --news --config ~/.md_push_wechat/custom_news.yaml news.md news_wechat.html
```

输出 HTML 文件保存在当前工作目录。若未指定 output.html，则根据模式自动生成文件名后缀（`_wechat.html` 或 `_news_wechat.html`）。

## 技能 2：转换 + 推送草稿箱

调用脚本：
```bash
# 文章模式（默认）
python3 ${CODEBUDDY_SKILL_DIR}/scripts/push_daily.py <input.md> [--title TITLE] [--cover COVER] [--digest DIGEST] [--media-id MEDIA_ID]

# 新闻模式（--news）
python3 ${CODEBUDDY_SKILL_DIR}/scripts/push_daily.py --news <input.md> [--title TITLE] [--cover COVER] [--digest DIGEST] [--media-id MEDIA_ID]
```

支持 Markdown frontmatter 提取标题和摘要：
```yaml
---
title: 文章标题
digest: 手动摘要（80字以内）
---
```

### 完整工作流

**必须严格按以下步骤执行：**

1. **读取 Markdown 文件内容**（用 Read 工具）
2. **提取 frontmatter**：检查文件顶部是否有 `---` 包裹的 YAML 区段，提取 `title` 和 `digest` 字段
3. **生成摘要（重要！）**：如果 frontmatter 中没有 `digest` 字段，则**必须**根据文章正文内容自动生成一条 120 个字符以内的中文摘要，通过 `--digest` 参数传入脚本。摘要要求：
   - 简洁精炼，概括文章核心内容
   - 严格控制在 120 个字符以内（含标点）
   - 不要使用 markdown 格式或 HTML 标签
   - 不要以「本文」「这篇文章」开头
4. **调用 `push_daily.py`**：将生成的摘要通过 `--digest` 参数传入（若 frontmatter 已有 digest 则使用 frontmatter 中的值）
5. 脚本自动执行：Markdown → HTML → 上传封面图 → 推送草稿箱

> **注意**：摘要生成是必选步骤，不可跳过。不要让脚本自动截取 120 字符——那会产生不完整的无意义截断。

**自动拆分**：当 HTML 内容超过 20000 字符限制时，脚本会自动按 H2 标题拆分为多篇合并推送（同一图文消息内，读者上滑查看），标题自动添加（上）（中）（下）后缀。拆分后非首篇的摘要由脚本自动生成，无需手动处理。

## 技能 3：推送掘金草稿箱

调用脚本：
```bash
# 新建草稿
python3 ${CODEBUDDY_SKILL_DIR}/scripts/push_juejin.py <input.md> [--title TITLE] [--digest DIGEST] [--category ID] [--tags IDS]

# 更新已有草稿
python3 ${CODEBUDDY_SKILL_DIR}/scripts/push_juejin.py <input.md> --update DRAFT_ID [--title TITLE] [--digest DIGEST]

# 查询标签
python3 ${CODEBUDDY_SKILL_DIR}/scripts/push_juejin.py --query-tags KEYWORD
```

支持 Markdown frontmatter 提取元数据：
```yaml
---
title: 文章标题
digest: 摘要（50-100字）
category_id: "6809637773935378440"
tag_ids: "6809640408797167623,6809640445233070098"
cover_image: https://p1-juejin.byteimg.com/xxxxx
---
```

### 工作流

1. 读取 `~/.md_push_wechat/config.yaml` 获取 `juejin.cookie` 和默认分类/标签
2. 解析 Markdown frontmatter 提取标题、摘要、分类、标签
3. 扫描正文中的本地图片引用，尝试上传到掘金图床（通过 ImageX/gen_token）
4. 替换 mark_content 中的本地图片为掘金 CDN URL
5. 调用掘金创建/更新草稿 API

### 参数

| 参数 | 说明 |
|------|------|
| `--title` | 文章标题（覆盖 frontmatter） |
| `--digest` | 摘要（50-100字，掘金硬性要求） |
| `--category` | 分类 ID 或名称（如 "AI"、"后端"，自动转换） |
| `--tags` | 标签 ID，逗号分隔（如 "6809640445233070098,6809640408797167623"） |
| `--cover` | 封面图 URL（必须是掘金 CDN 地址） |
| `--update DRAFT_ID` | 更新已有草稿 |
| `--query-tags KEYWORD` | 查询可用标签 |

### 分类 ID 速查表

| 分类名称 | category_id |
|----------|-------------|
| 后端 | `6809637769959178254` |
| 前端 | `6809637767543259144` |
| Android | `6809635626879549454` |
| iOS | `6809635626661445640` |
| AI / 人工智能 | `6809637773935378440` |
| 开发工具 | `6809637771511070734` |
| 代码人生 | `6809637776263217160` |
| 阅读 | `6809637772874219534` |

> 运行 `python push_juejin.py --query-categories` 可在线获取最新分类列表。 |

### 前置条件

- 配置文件 `~/.md_push_wechat/config.yaml` 必须包含 `juejin.cookie`
- Cookie 获取方式：登录 juejin.cn → F12 → Application → Cookies → 复制完整 Cookie 字符串
- Cookie 有效期约 30 天，过期需重新获取

### 图片上传

脚本会尝试将 Markdown 中的本地图片上传到掘金图床，完整 ImageX 5 步流程：

| 步骤 | 接口 | 说明 |
|------|------|------|
| 1. gen_token | `GET /imagex/v2/gen_token` | 获取 STS 临时凭证（ServiceId=73owjymdk6） |
| 2. ApplyImageUpload | `GET imagex.bytedanceapi.com/?Action=ApplyImageUpload` | 获取上传地址，需要 AWS SigV4 签名 |
| 3. 上传二进制 | `POST tos-d-x-lf.douyin.com/{store_uri}` | 实际上传文件，带 Content-CRC32 校验 |
| 4. CommitImageUpload | `POST ?Action=CommitImageUpload&SessionKey=xxx` | 确认上传，SigV4 签名 |
| 5. get_img_url | `GET /imagex/v2/get_img_url` | 获取 CDN URL（`https://p1-juejin.byteimg.com/...`） |

**MD5 缓存**：上传后的 CDN URL 基于文件内容 MD5 缓存到 `config.yaml` 的 `image_cache.juejin` 段，同一张图片（即使路径不同）永久复用，无需重复上传。

**关键实现细节**：
- AWS SigV4 签名使用 `hmac` + `hashlib.sha256` 手动实现，参数排序确保 AWS 要求的字母顺序
- 文件上传使用 POST + Content-CRC32 校验（非 PUT）
- mark_content 中的本地路径替换为完整 CDN URL（`http(s)://` 开头），非 store_uri

> 注意：图片上传功能为尽力而为模式。如上传失败，脚本会跳过该图片并保留原引用。

微信公众号草稿接口有 **20000 字符限制**。脚本采用以下 CSS 继承策略压缩输出体积：

- **`text-indent:0`** 统一写到 `<body style>` 一次，全文继承，各 `<p>/<h2>/<h3>` 不再重复（`text-indent` 是可继承属性）
- **`color` / `font-size` / `line-height`** 提升到最近父级 `<section>`，子元素只保留差异化覆盖
- **`<td>` 的 `color`** 从 `<body>` 继承，不在每个 `td` 重复
- **空格规范**：style 属性内一律去掉冒号/分号后的空格，进一步节省

实测节省效果（示例文件）：
| 模式 | 优化前 | 优化后 | 节省 |
|------|--------|--------|------|
| 日报 | 9,324 字符 | 8,352 字符 | 972 字符 (10.4%) |
| AI文章 | 9,527 字符 | 9,101 字符 | 426 字符 (4.5%) |
| 长文 | 3,366 字符 | 3,156 字符 | 210 字符 (6.2%) |

## 前置检查

- 技能 1：无前置依赖
- 技能 2（推送草稿箱）：执行前**必须**确认配置文件 `~/.md_push_wechat/config.yaml` 存在。若不存在，**立即中断**，提示用户创建配置文件并填写 `appid` 和 `secret`，不得尝试从其他目录查找或自动创建。

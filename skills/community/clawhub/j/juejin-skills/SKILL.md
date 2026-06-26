---
version: 1.0.8
name: juejin-skills
license: MIT
description: 掘金技术社区一站式操作技能，支持热门文章排行榜查询、Markdown 文章发布（默认草稿）和文章下载保存为 Markdown。
source: https://github.com/wscats/juejin
homepage: https://github.com/wscats/juejin
repository:
  type: git
  url: https://github.com/wscats/juejin.git
author: wscats
credentials:
  - name: juejin_session_cookie
    description: 通过 Playwright 浏览器登录后获得的掘金登录态 Cookie。
    storage_path: ~/.juejin_cookie.json
    storage_format: plain-text JSON
    file_permissions: "0600 (owner-only read/write, enforced by auth._save_cookies)"
    scope: 对用户登录的掘金账号具有读写权限（可发文章、读取私有草稿等）。
    rotation: 用户可随时通过删除 ~/.juejin_cookie.json 撤销访问；Cookie 过期后需要重新登录。
    hardening:
      - 不要在多人共享的机器或 CI 容器中使用（Cookie 即账号登录态）。
      - 使用完毕立即执行 `rm ~/.juejin_cookie.json` 撤销。
      - 不要将该文件提交到版本库；本仓库已在 `.clawhubignore` / `.gitignore` 中排除。
permissions:
  - network: |
      仅访问 https://juejin.cn/ 与 https://api.juejin.cn/。
      下载文章中的图片时，仅允许从掘金官方图床域名拉取
      （juejin.cn / *.byteimg.com，详见 juejin_skill/config.py 中的
      ALLOWED_IMAGE_DOMAINS 白名单）；其他域名一律跳过。
  - filesystem_read: |
      仅读取用户显式提供的 .md / .markdown 文件，且必须满足：
      (1) 路径位于当前工作目录之下，或位于环境变量 $JUEJIN_MD_ROOT 指向的目录之下；
      (2) 文件大小 ≤ 2 MiB；
      (3) 不在 /etc, /var, /proc, /sys, /dev, /root, /boot,
          ~/.ssh, ~/.aws, ~/.config, ~/.juejin_cookie.json 等敏感前缀下。
      违反任一规则时，juejin_skill.publisher._validate_markdown_path() 会直接
      拒绝读取。本技能不会主动遍历目录、不会读取无关后缀的文件、不会跟随
      指向上述受限位置的符号链接。
  - filesystem_write: |
      仅允许写入下列位置：
      (1) ~/.juejin_cookie.json（会话凭证，权限 0600）；
      (2) ./output/ 及其子目录（下载的文章 .md 与图片）。
      允许用户通过环境变量 $JUEJIN_OUTPUT_ROOT 重定位上述
      ./output 根目录，但任何 download_article / download_user_articles 写入的
      路径都会经过 juejin_skill.downloader._validate_output_dir() 校验：
      路径会用 os.path.realpath 解析，有效抵御符号链接、`..` 馑越、
      以及伪造后缀绕过。任何解析后越出该根目录的写请求都会被拒绝。
  - browser_automation: 启动本地 Chromium 仅用于在 https://juejin.cn 完成登录获取 Cookie。
publish_policy: draft-only-by-default  # 任何公开发布都需要用户显式确认
bulk_download_policy: opt-in-with-hard-cap  # 批量下载需显式确认且受硬上限控制
publish_policy_enforcement:
  api_layer: |
    juejin_skill.publisher.ArticlePublisher.publish_markdown() 的默认参数为
    save_draft_only=True, allow_public_publish=False。两个标志都需要被显式
    改为 False / True 时才会触发公开发布；任何一侧缺失都会直接拒绝并返回
    draft 结果。
  cli_layer: |
    run_publish.py 默认 draft-only；公开发布需要同时满足：
    (1) --publish 命令行开关, (2) 环境变量 JUEJIN_CONFIRM_PUBLISH=1,
    (3) 交互式输入 'yes'。publish_article.py 的交互流程同样默认走草稿分支，
    选择公开发布后需要再次键入 'yes' 确认。
bulk_download_policy_enforcement:
  api_layer: |
    juejin_skill.downloader.ArticleDownloader.download_user_articles() 需要
    显式传入 confirm_bulk=True 才会执行，否则只返回拒绝响应。
    max_count 默认为 BULK_DOWNLOAD_DEFAULT (20)，并被 BULK_DOWNLOAD_HARD_CAP
    (50) 强制夹住；调用方传入更大的值会被静默降级。
    download_article() / download_user_articles() 的 output_dir 参数都会经过
    _validate_output_dir() 校验，任何越出 ./output (或 $JUEJIN_OUTPUT_ROOT) 的
    写请求都会被拒绝。
  cli_layer: |
    上层 CLI / Agent 调用方负责在打开 confirm_bulk 之前跳出人工确认门
    （例如要求用户输入 yes / 点击确认按钮）。

---

> ⚠️ **凭证与权限声明**
>
> 本技能在登录成功后会把掘金会话 Cookie 以明文 JSON 形式保存到
> `~/.juejin_cookie.json`（文件权限会被设置为 `0600`，仅当前用户可读写）。
> 只要该文件存在且未过期，后续调用即可以你的身份访问掘金账号（发布文章、
> 读取草稿等）。
>
> - 仅在你愿意把掘金登录态保存在本机时才登录，**避免在共享/CI 环境运行**；
> - 使用结束后请执行 `rm ~/.juejin_cookie.json` 主动撤销；
> - 不要将该文件提交版本库（仓库已默认忽略）；
> - 本技能**默认只创建草稿**：API 层 `ArticlePublisher.publish_markdown()`
>   的默认行为是 `save_draft_only=True`，且公开发布还需要调用方额外显式
>   传入 `allow_public_publish=True`。入口脚本 `run_publish.py` 和
>   `publish_article.py` 则在此之上再加了命令行/交互式的人工确认门。

# Juejin Skills - 掘金技术社区操作技能

## 🚀 快速使用
本技能仅在用户**明确、字面**提到下列意图时才被调用。
模糊的、推断出的或捎带提到“掘金/发布/下载”的请求**不会**触发本技能；
遇到不确定的情况，AI 应当先向用户澄清，而不是直接执行。

### 热门文章排行榜（只读，无副作用）
- “获取掘金热门文章排行榜”
- “查看掘金前端分类的热门文章”
- “掘金有哪些文章分类？”

### 文章发布（需要登录态 + 显式 .md 路径）
- “把 ./xxx.md 这个文件作为草稿发布到掘金，分类前端，标签 Vue.js”
- “登录掘金账号”（会通过 Playwright 打开浏览器让你登录）
- 注：用户必须显式给出位于当前工作目录下的 `.md` 文件路径，
  或直接粘贴 Markdown 正文。AI **不得**主动猜测或代填路径，
  也**不得**把诸如 `~/.ssh/...`、`/etc/...`、`~/.juejin_cookie.json`
  这类路径喂给本技能。

### 文章下载（只接受用户显式给出的 juejin.cn 链接或 article_id）
- “下载这条链接的掘金文章：https://juejin.cn/post/xxx”
- “把这位作者（链接：https://juejin.cn/user/xxx）的最新 N 篇文章保存到本地”

---

## 技能描述

| 属性 | 内容 |
|------|------|
| **技能名称** | Juejin Skills（掘金技术社区操作技能） |
| **技能类型** | Prompt-based Skill（自然语言驱动） |
| **技能语言** | Python |
| **目标网站** | https://juejin.cn/ |
| **激活方式** | 自然语言指令 |

## 激活条件

本技能采取**严格字面匹配**策略：仅当用户的请求**同时**满足下列三项时，
才认为该请求属于本技能的范围：

1. 请求中字面出现“掘金”或域名 `juejin.cn`（不接受“某社区”“技术博客”
   等泛指）；
2. 请求所表达的动作落在“查询热门列表 / 发布 .md 草稿 / 下载已知 URL”
   这三类窄定义场景之一；
3. 触发任何写操作（登录、发布、下载到磁盘）的请求都必须带有用户**亲自
   提供**的具体参数（.md 路径、文章 URL、分类名等），AI 不得自行编造。

如果上述任一条件不满足，AI 应当先向用户澄清，**不要**激活本技能。

### 1. 热门文章排行榜（只读）
- 触发示例：用户字面询问“掘金 + (热门 / 排行榜 / 热榜 / 分类列表)”。
- **不**触发示例：“最近前端有什么火的”“给我推荐几篇好文章”——
  这些不含“掘金”字样，本技能保持沉默。

### 2. 文章发布（写操作，需登录态 + 显式输入）
- 触发示例：用户字面要求“(发布 / 发文 / 投稿 / 草稿) + 掘金”，
  并提供下列至少一项：
  - 当前工作目录下的 `.md` 文件路径，或
  - 直接粘贴的 Markdown 正文。
- **不**触发示例：仅说“一键发布”“帮我发个文”而未指明掘金；
  仅模糊提到“掘金”但未给出文件或正文；
  请求读取 `~/.ssh`、`/etc`、`~/.juejin_cookie.json` 等敏感路径。
  这些情况下应拒绝并要求澄清。

### 3. 文章下载（写操作到 ./output）
- 触发示例：用户字面给出 `juejin.cn/post/<id>` 或 `juejin.cn/user/<id>`
  链接，并字面要求“下载 / 保存 / 导出”。
- **不**触发示例：要求下载非掘金域名的文章；要求把下载结果写入
  `./output/` 之外的路径——这些应被拒绝。

#### 3.1 批量下载（需人工确认 + 硬上限）
- `download_user_articles` 需要调用方显式传入 `confirm_bulk=True`，
  未传时该方法会直接拒绝并返回提示。
- `max_count` 默认 20、硬上限 50；AI / CLI 不得在未获得用户明确同意前
  自行将这个限额开到更高或跳过确认。这避免了在用户只需下载一两篇
  文章时意外启动大规模抓取。
- 触发示例：“把这位作者（https://juejin.cn/user/xxx）的最新 N 篇
  文章下载下来” + 用户明确同意启动批量下载。

## 功能清单

### 📊 功能一：热门文章排行榜

| 子功能 | 说明 |
|--------|------|
| 获取分类列表 | 获取掘金所有文章分类（前端、后端、Android、iOS、人工智能等） |
| 热门文章排行 | 获取指定分类或全部分类的热门文章排行榜 |
| 文章趋势分析 | 按时间维度（3天/7天/30天/历史）查看文章热度趋势 |
| 排行榜筛选 | 支持按分类、时间范围、排序方式筛选 |

**API 接口**：
- 分类列表：`GET https://api.juejin.cn/tag_api/v1/query_category_briefs`
- 热门文章：`POST https://api.juejin.cn/recommend_api/v1/article/recommend_all_feed`
- 分类文章：`POST https://api.juejin.cn/recommend_api/v1/article/recommend_cate_feed`
- 标签列表：`POST https://api.juejin.cn/tag_api/v1/query_category_tags`

### 📝 功能二：文章自动发布

| 子功能 | 说明 |
|--------|------|
| 浏览器登录 | 通过 Playwright 打开掘金登录页面，用户扫码或密码登录后自动获取 Cookie |
| Cookie 管理 | 保存、加载、验证 Cookie 状态 |
| Markdown 解析 | 读取本地 Markdown 文件，提取标题、正文内容 |
| 文章发布 | 通过掘金 API 创建草稿并发布，支持设置分类、标签、摘要、封面图 |
| 草稿管理 | 支持保存为草稿而不立即发布 |

**API 接口**：
- 创建草稿：`POST https://api.juejin.cn/content_api/v1/article_draft/create`
- 发布文章：`POST https://api.juejin.cn/content_api/v1/article/publish`
- 获取标签：`POST https://api.juejin.cn/tag_api/v1/query_category_tags`

**鉴权方式**：Cookie 鉴权（通过 Playwright 浏览器登录获取）

### 📥 功能三：文章下载

| 子功能 | 说明 |
|--------|------|
| 单篇下载 | 通过文章 URL 下载单篇文章，保存为 Markdown |
| 批量下载 | 下载指定作者的所有/部分文章 |
| 格式转换 | 将掘金文章 HTML 内容转换为标准 Markdown |
| 图片处理 | 可选下载文章中的图片到本地 |
| 元数据保留 | 保留文章标题、作者、发布时间、标签等元信息 |

**API 接口**：
- 文章详情：`POST https://api.juejin.cn/content_api/v1/article/detail`
- 用户文章列表：`POST https://api.juejin.cn/content_api/v1/article/query_list`

## 技术架构

```
juejin/
├── SKILL.md              # 技能定义文档
├── README.md             # 项目说明文档
├── requirements.txt      # Python 依赖
├── juejin_skill/         # 主模块
│   ├── __init__.py
│   ├── config.py         # 配置管理
│   ├── api.py            # 掘金 API 封装
│   ├── auth.py           # 登录鉴权（Playwright）
│   ├── hot_articles.py   # 热门文章排行榜
│   ├── publisher.py      # 文章发布
│   ├── downloader.py     # 文章下载
│   └── utils.py          # 工具函数
└── output/               # 下载文章输出目录
```

## 环境要求

- Python >= 3.9
- Playwright（用于浏览器登录）
- 网络可访问 https://juejin.cn/

## Prompt 示例

```
用户：帮我获取掘金前端分类的热门文章排行榜
AI：正在获取掘金前端分类的热门文章...

用户：把 ./my-article.md 发布到掘金，分类选前端，标签加上 Vue.js 和 TypeScript
AI：正在登录掘金账号并发布文章...

用户：下载这篇掘金文章 https://juejin.cn/post/7300000000000000000
AI：正在下载文章并转换为 Markdown 格式...
```

## 🔒 安全限制与风险警告

### 本地文件写入安全限制（`filesystem_write`）
- `download_article(...)`、`download_user_articles(...)` 以及内部的
  `_write_markdown_file` / `_download_images` 在写入磁盘之前都会调用
  `juejin_skill.downloader._validate_output_dir()`：
  - 写入路径必须位于 `./output`（或 `$JUEJIN_OUTPUT_ROOT`）之下；
  - 使用 `os.path.realpath` 解析后再比对，可抵御符号链接、`..` 馑越，
    以及伪造后缀绕过检查。
- 任何越出根目录的 `output_dir` 传入都会被以
  `{"success": False, "message": ...}` 形式拒绝，不会创建目录也不会调用 open()。
- 这保证了 SKILL.md 中 `filesystem_write` 边界与代码实际行为一致。

### 批量下载安全限制（`bulk_download_policy`）
- `download_user_articles()` 需要显式 `confirm_bulk=True` 才会执行；
- `max_count` 默认 20、硬上限 `BULK_DOWNLOAD_HARD_CAP=50`，超出会被静默降级；
- 防止在用户仅下载一两篇文章时被意外启动为全量抓取，控制运营风险与平台合规风险。

### 本地文件读取安全限制（`filesystem_read`）
- `publish_markdown(filepath=...)` 会经过
  `juejin_skill.publisher._validate_markdown_path()` 校验，仅接受：
  - 位于当前工作目录（或 `$JUEJIN_MD_ROOT`）之下的 `.md` / `.markdown` 文件；
  - 文件大小 ≤ 2 MiB；
  - 不在 `/etc`、`/var`、`/proc`、`/sys`、`/dev`、`/root`、`/boot`、
    `~/.ssh`、`~/.aws`、`~/.config`、`~/.juejin_cookie.json` 等敏感前缀下的文件。
- 路径会使用 `os.path.realpath` 解析后再比对，以防止符号链接逃逸、
  `..` 路径馑越、以及伪造后缀绕过检查。
- 违反任一规则都会抩出 `ValueError`，不会走到 `open()`，也不会被填到
  草稿 / 发布 / 任何外发请求中。

### 图片下载安全限制
- 图片下载功能仅允许下载来自掘金官方域名的图片
- 支持的域名：juejin.cn, p1-juejin.byteimg.com, p3-juejin.byteimg.com, p6-juejin.byteimg.com, p9-juejin.byteimg.com
- 其他域名的图片将被自动跳过，防止SSRF攻击和未经授权的出站请求

### 发布安全机制
- 默认只创建草稿，不公开发布
- 公开发布需要双重确认：`save_draft_only=False` 和 `allow_public_publish=True`
- 命令行工具需要额外的环境变量和交互式确认

### 网络访问限制
- 仅允许访问 juejin.cn 和 api.juejin.cn 域名
- 图片下载有严格的域名白名单限制
- 防止潜在的策略绕过和跟踪风险

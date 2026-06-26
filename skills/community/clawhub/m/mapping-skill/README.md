# AI Talent Recruiter Skill

一个面向 Claude Code 与 OpenClaw 的 AI/ML 人才搜索与个性化触达 skill，适用于从实验室主页、会议论文、GitHub 社交网络和通用网页中发现候选人、抽取结构化信息、识别华人、分类去重，并生成个性化招聘邮件。

## 项目链接

- GitHub: https://github.com/16Miku/Mapping-Skill
- ClawHub: https://clawhub.ai/16Miku/mapping-skill

## 这个 skill 解决什么问题

当用户需要做下面这些复合任务时，这个 skill 可以显著减少手工搜索、爬取、整理和写邮件的成本：

- 查找 AI/ML 方向的 PhD、研究员、工程师
- 定向搜索某个实验室、会议、GitHub 网络中的候选人
- 抽取主页、Scholar、GitHub、邮箱、研究方向、教育背景等信息
- 识别华人候选人并做类型分类
- 对重复候选人去重
- 基于候选人背景生成个性化 outreach 邮件
- 将论文作者或候选人数据导入飞书多维表格，并在表格中批量写入推荐邮件

## 什么时候应该触发它

如果用户表达了以下意图，即使没有明确说“用 Mapping-Skill”，也应该考虑触发本 skill：

- “帮我找做 RL / LLM / 多模态 / Agent 的 PhD”
- “把某实验室成员都扒下来，最好带邮箱和主页”
- “找某会议的华人作者，并整理联系方式”
- “看看某 GitHub 用户 follow 的研究者里有哪些值得联系的人”
- “根据候选人资料帮我写封更有针对性的招聘邮件”
- “把抓下来的论文作者导入飞书多维表格并批量生成邮件”
- “给定一个 URL，把页面中的人员信息全部提取出来并导入表格”

## 支持的核心能力

### 1. Topic Search
按研究方向搜索候选人，例如 RL、NLP、Alignment、Multimodal、MLSys。

### 2. Lab Search
直接从实验室主页提取成员信息，适合 Stanford、LAMDA、PKU.AI、TongClass 等学术站点。

### 3. Conference Author Search
从 OpenReview 或 CVF 等会议站点提取作者信息，适合 ICLR / ICML / NeurIPS / CVPR / ICCV / WACV。

### 4. GitHub Network Discovery
从某个 GitHub 用户的 following/followers 网络中发现研究者，并补全社交链接与主页信息。

### 5. Candidate Profile Extraction
对已有 URL 列表执行统一抽取、结构化整理、分类与去重。

### 6. Outreach Email Generation
基于候选人研究方向、论文、主页信息，生成个性化的招聘邮件初稿。

### 7. Feishu / OpenClaw Workflow
支持将 CSV 或爬取结果导入飞书多维表格，支持根据表格中的论文作者信息批量生成推荐邮件，并回写到飞书字段中。

## Claude Code 使用说明

### 安装方式

将本目录复制到 Claude Skills 目录：

```bash
cp -r Mapping-Skill ~/.claude/skills/
```

### 依赖配置

#### 方案 A：BrightData MCP（推荐，付费）

适合 LinkedIn、强反爬站点和需要更高成功率的页面。

```bash
claude mcp add --transport sse --scope user brightdata "https://mcp.brightdata.com/sse?token=<your-api-token>"
```

#### 方案 B：Python 爬虫（免费）

```bash
pip install requests beautifulsoup4 httpx python-dotenv openreview-py pandas openpyxl PyMuPDF
```

### 验证方式

安装完成后，在 Claude Code 中出现 `Mapping-Skill` 即表示可被触发。

## OpenClaw 使用说明

### 安装路径与加载

根据 OpenClaw 文档，skill 可以放在以下位置：

- `<workspace>/skills`（最高优先级）
- `~/.openclaw/skills`
- 内置 skills（最低优先级）

也可以通过 ClawHub 安装：

```bash
clawhub install 16Miku/mapping-skill
```

若你使用的是工作区技能目录，还可以在 `~/.openclaw/openclaw.json` 中通过 `skills.load.extraDirs` 增加额外扫描目录，并开启 `load.watch` 以便自动刷新。

### 刷新方式

将 skill 放到目录后，可以通过“刷新 skills”或重启 Gateway 网关来让 OpenClaw 重新发现和索引技能。

### Slash Command 方式

OpenClaw 中 skill 可以作为斜杠命令暴露。用户可：

- 使用 `/commands` 查看可用命令
- 通过 `/skill <name> [input]` 或平台提供的原生命令方式手动调用
- 在开启用户可调用配置时，以 slash command 形式直接触发

### 配置建议

如需让 OpenClaw 更稳定使用该 skill，建议确认：

- Skill 目录下包含规范的 `SKILL.md`
- 相关脚本路径可访问
- 若依赖环境变量或二进制，在 OpenClaw 配置中声明
- 若使用 Docker / 沙箱，环境变量需要显式注入，不能默认继承宿主机环境

## OpenClaw + 飞书相关配置记录

如果你要在 OpenClaw 中跑“爬取论文 → 导入飞书多维表格 → 批量生成邮件”的工作流，需要先准备飞书权限与相关工具能力。

### 飞书权限记录

以下是你提供的飞书权限配置记录，可整理进实际部署说明：

```json
{
  "scopes": {
    "tenant": [
      "contact:contact.base:readonly",
      "docx:document:readonly",
      "im:chat:read",
      "im:chat:update",
      "im:message.group_at_msg:readonly",
      "im:message.p2p_msg:readonly",
      "im:message.pins:read",
      "im:message.pins:write_only",
      "im:message.reactions:read",
      "im:message.reactions:write_only",
      "im:message:readonly",
      "im:message:recall",
      "im:message:send_as_bot",
      "im:message:send_multi_users",
      "im:message:send_sys_msg",
      "im:message:update",
      "im:resource",
      "application:application:self_manage",
      "cardkit:card:write",
      "cardkit:card:read"
    ],
    "user": [
      "contact:user.employee_id:readonly",
      "offline_access","base:app:copy",
      "base:field:create",
      "base:field:delete",
      "base:field:read",
      "base:field:update",
      "base:record:create",
      "base:record:delete",
      "base:record:retrieve",
      "base:record:update",
      "base:table:create",
      "base:table:delete",
      "base:table:read",
      "base:table:update",
      "base:view:read",
      "base:view:write_only",
      "base:app:create",
      "base:app:update",
      "base:app:read",
      "sheets:spreadsheet.meta:read",
      "sheets:spreadsheet:read",
      "sheets:spreadsheet:create",
      "sheets:spreadsheet:write_only",
      "docs:document:export",
      "docs:document.media:upload",
      "board:whiteboard:node:create",
      "board:whiteboard:node:read",
      "calendar:calendar:read",
      "calendar:calendar.event:create",
      "calendar:calendar.event:delete",
      "calendar:calendar.event:read",
      "calendar:calendar.event:reply",
      "calendar:calendar.event:update",
      "calendar:calendar.free_busy:read",
      "contact:contact.base:readonly",
      "contact:user.base:readonly",
      "contact:user:search",
      "docs:document.comment:create",
      "docs:document.comment:read",
      "docs:document.comment:update",
      "docs:document.media:download",
      "docs:document:copy",
      "docx:document:create",
      "docx:document:readonly",
      "docx:document:write_only",
      "drive:drive.metadata:readonly",
      "drive:file:download",
      "drive:file:upload",
      "im:chat.members:read",
      "im:chat:read",
      "im:message",
      "im:message.group_msg:get_as_user",
      "im:message.p2p_msg:get_as_user",
      "im:message:readonly",
      "search:docs:read",
      "search:message",
      "space:document:delete",
      "space:document:move",
      "space:document:retrieve",
      "task:comment:read",
      "task:comment:write",
      "task:task:read",
      "task:task:write",
      "task:task:writeonly",
      "task:tasklist:read",
      "task:tasklist:write",
      "wiki:node:copy",
      "wiki:node:create",
      "wiki:node:move",
      "wiki:node:read",
      "wiki:node:retrieve",
      "wiki:space:read",
      "wiki:space:retrieve",
      "wiki:space:write_only"
    ]
  }
}
```

### BrightData MCP（可选）

如果在 OpenClaw 中启用 BrightData MCP，可参考你提供的配置形式：

```json
"brightdata": {
  "type": "sse",
  "url": "https://mcp.brightdata.com/sse?token=<your_token>&groups=advanced_scraping,social,browser,research,app_stores"
}
```

适合用于：
- LinkedIn 等强反爬站点
- 通用网页动态抓取
- 某些 Python 路线不好处理的页面

## 快速开始示例

### 示例 1：按研究方向找人

```text
帮我找做 reinforcement learning 的 AI PhD，优先顶级学校，最好带主页、邮箱和研究方向总结。
```

### 示例 2：按实验室找人

```text
帮我把 NJU LAMDA lab 的 PhD 学生整理出来，提取邮箱、主页、论文和研究方向。
```

### 示例 3：按会议找华人作者

```text
找出 ICML 2025 发表论文的华人作者，补充主页、Scholar 和邮箱，并按研究方向分类。
```

### 示例 4：基于候选人生成邮件

```text
我已经有几位候选人的主页和 Google Scholar，请你提取关键信息并为每个人写一封更有针对性的 outreach 邮件。
```

## 最佳实践提示词（来自实际工作流）

### 1. OpenReview 论文爬取 + 飞书入表

```text
请执行 OpenReview 论文爬取任务：
1. 使用 Mapping-Skill skill 根目录下的 `scripts/openreview_scraper.py` 脚本
2. 初始化爬虫时使用 api2.openreview.net 端点：
   scraper = OpenReviewScraper(
       username='XXXXXXX',
       password='XXXXXXX',
       baseurl='https://api2.openreview.net'
   )
3. 爬取 ICLR2025 的 5 篇论文（测试）+ https://openreview.net/group?id=ICLR.cc/2025/Conference#tab-accept-oral（记着替换链接）
4. 保存 CSV 到 /tmp/ 目录
5. 创建新的飞书多维表格，按照 Mapping-Skill skill 根目录下的 `scripts/openreview_scraper.py` 脚本中爬取的数据来创建相应字段
6. 批量导入数据到多维表格
7. 返回多维表格链接和统计信息
```

### 2. CVF 论文爬取 + 邮箱提取 + 飞书入表

```text
请执行 CVF 论文爬取任务：
1. 使用 Mapping-Skill skill 根目录下的 `scripts/cvf_paper_scraper.py` 脚本
2. 严格按照脚本中的 extract_emails_from_text() 函数提取邮箱
3. 爬取 ICCV2025 的 5 篇论文（测试）+ https://openaccess.thecvf.com/ICCV2025?day=all（记着替换链接）
4. 保存 CSV 到 /tmp/ 目录
5. 创建新的飞书多维表格，按照 Mapping-Skill skill 根目录下的 `scripts/cvf_paper_scraper.py` 脚本中爬取的数据来创建相应字段
6. 批量导入数据到多维表格
7. 返回多维表格链接和邮箱提取统计
```

### 3. 飞书表格批量写邮件

```text
请执行论文作者邮件生成任务：
【数据源】
表格链接：
【第一步：解析表格链接】
1. 从链接中提取 app_token（格式：/base/{app_token}）
2. 调用 feishu_bitable_app_table 的 list 接口获取 table_id
3. 验证表格可访问性
【第二步：分批读取论文数据】
1. 使用 feishu_bitable_app_table_record 的 list 操作
2. 分批读取（每批50条），使用 page_token 分页
3. 只提取必要字段：记录ID、论文标题、作者、邮箱、机构
4. 过滤条件：只处理有邮箱的记录
【第三步：确定研究领域】
1. 读取 Mapping-Skill skill 根目录下的 `references/field-mappings.md`
2. 根据论文标题和关键词，使用映射规则确定研究领域
3. 示例：
   - "Symmetry Understanding of 3D Shapes" → Computer Vision
   - "Efficient Adaptation of Vision Transformer" → NLP
【第四步：生成个性化邮件】
1. 读取 Mapping-Skill skill 根目录下的 `references/email-templates.md`
2. 根据研究领域选择对应模板（共22个领域）
3. 填充占位符：
   - {{researcher_name}} → 第一作者姓名
   - {{context_affiliation}} → 机构
   - {{research_field}} → 研究领域
   - {{technical_hook}} → 基于论文标题生成
   - {{talk_track_paragraph}} → 从 talk-tracks.md 选择
【第五步：批量更新多维表格】
1. 在多维表格中创建新字段："推荐邮件"（多行文本）
2. 使用 batch_update 批量更新每条记录
3. 每批最多 500 条
【第六步：验证和统计】
1. 验证邮件内容个性化
2. 返回统计：总计 X 条 / 成功 Y 条 / 失败 Z 条
3. 列出失败原因
【输出】
- 多维表格链接
- 生成统计
- 失败原因列表
```

### 4. 给定某 URL 全量抽取并入表

```text
1、请你调用BrightData-MCP工具，或者编写爬虫脚本，爬取 <某网站URL> 页面中的所有人员信息。
2、提取信息包括中文名，英文名，个人介绍信息、学术方向、学校和专业信息、工作经历、近期论文著作信息（包含论文名和论文链接）、github链接、个人主页链接、谷歌学术链接、领英链接、知乎链接、B站链接、邮箱等。
3、当前页面缺少邮箱的话，需要进入学者主页或论文链接页面，从里面提取作者们的邮箱。
4、保存到csv文件，然后将csv导入飞书多维表格。
```

## 推荐提问方式

为了让结果更稳定，建议用户在需求里尽量补充以下信息：

- 搜索范围：topic / lab / conference / GitHub network / 已有 URL
- 目标人群：PhD / PostDoc / Professor / Research Scientist / Engineer
- 研究方向：例如 RL、Agent、Alignment、Embodied AI
- 筛选条件：是否优先华人、是否优先顶校、是否需要邮箱
- 输出要求：只要候选人表格，还是还要生成个性化邮件，是否需要导入飞书

### 一个更好的请求示例

```text
帮我找做 LLM alignment 的华人 PhD，优先北美顶校或顶级 AI lab。请尽量提取主页、Google Scholar、GitHub、邮箱和研究方向，并按 PhD / PostDoc / Professor 分类，最后为最值得联系的 5 人各写一封简短 outreach 邮件；如果可以的话，把结果整理成 CSV 并导入飞书多维表格。
```

## 方法选择说明

| 场景 | 推荐方式 | 原因 |
|------|----------|------|
| LinkedIn / 强反爬站点 | BrightData MCP | 成功率高，处理反爬更稳定 |
| 大学主页 / 个人主页 / Hugo Academic | Python 爬虫 | 免费、可控、可复用脚本多 |
| OpenReview 会议作者 | OpenReview API | 结构化程度高、效率高 |
| CVPR/ICCV/WACV | CVF HTML + PDF | HTML 可拿元数据，PDF 可补邮箱 |
| GitHub 社交网络 | GitHub API + README 抽取 | 可获得更完整的主页与社交信息 |
| 飞书多维表格批处理 | OpenClaw + 飞书能力 | 适合入表、字段创建、批量更新邮件 |

## 来自真实实践的经验总结

- Cloudflare 邮箱保护：需要识别 `/cdn-cgi/l/email-protection#...` 并做 XOR 解密
- 文本混淆邮箱：`[at]` / `(at)` / `name at domain dot edu` 在中文高校站点很常见
- `.edu.cn` SSL / 站点稳定性问题：需要容错和回退策略，不能假定每个页面都能正常抓取
- Hugo Academic 模板识别：`.people-person`、`.network-icon`、`.portrait-title` 等结构出现时，通常可直接走模板化解析
- 邮箱反向定位法：页面结构混乱时，可从邮箱文本节点反向定位“人卡片”容器
- CVF PDF 邮箱提取：有些作者邮箱只在 PDF 首页里，且可能是 LaTeX 花括号缩写形式
- GitHub README 是隐藏金矿：很多研究者把 Scholar、主页、LinkedIn 放在 Profile README，而不在 API 主资料里
- TongClass 两阶段抓取：列表页只负责抽成员 URL，个人页再用正则提取 Interests / Education / 社交链接，更稳

## 目录结构

```text
Mapping-Skill/
├── SKILL.md
├── README.md
├── references/
│   ├── search-templates.md
│   ├── top-ai-labs.md
│   ├── profile-schema.md
│   ├── candidate-classifier.md
│   ├── chinese-surnames.md
│   ├── deduplication-rules.md
│   ├── email-templates.md
│   ├── field-mappings.md
│   ├── talk-tracks.md
│   ├── url-priority-rules.md
│   ├── python-scraping-guide.md
│   ├── anti-scraping-solutions.md
│   ├── conference-paper-scraping.md
│   ├── practice-cases.md
│   ├── prompt-best-practices.md
│   └── user-feedback-notes.md
├── scripts/
│   ├── README.md
│   ├── serper_search.py
│   ├── httpx_scraper.py
│   ├── cloudflare_email_decoder.py
│   ├── lab_member_scraper.py
│   ├── openreview_scraper.py
│   ├── cvf_paper_scraper.py
│   └── github_network_scraper.py
└── evals/
    └── evals.json
```

## 关键参考文档

| 文件 | 用途 |
|------|------|
| `references/search-templates.md` | 搜索模板与查询构造 |
| `references/profile-schema.md` | 候选人结构化字段定义 |
| `references/candidate-classifier.md` | PhD / PostDoc / Professor / Industry 分类规则 |
| `references/chinese-surnames.md` | 华人识别辅助规则 |
| `references/deduplication-rules.md` | 7 层去重优先级 |
| `references/email-templates.md` | 个性化邮件模板 |
| `references/talk-tracks.md` | 技术领域 talk tracks |
| `references/python-scraping-guide.md` | Python 抓取模式与代码参考 |
| `references/anti-scraping-solutions.md` | Cloudflare、混淆邮箱、限流等问题处理 |
| `references/conference-paper-scraping.md` | OpenReview / CVF 会议抓取方法 |
| `references/practice-cases.md` | 真实案例沉淀与方法选择经验 |
| `references/prompt-best-practices.md` | 后续补充最佳提示词与提问建议 |
| `references/user-feedback-notes.md` | 后续沉淀用户反馈与体验优化记录 |

## 实战进展概览

从 git 历史来看，这个 skill 已经不是早期的“单一 BrightData 工作流”，而是一个逐步被真实任务打磨出来的方法库：

- 初始阶段：建立基础 skill 工作流、候选人 schema、分类与去重规则
- Python 增强阶段：增加 Python 抓取路线和参考脚本
- 实战增强阶段：陆续沉淀 OpenReview、LAMDA、GitHub、PKU.AI、清华 MediaLab、CVPR、TongClass 等案例
- 当前阶段：正在按最新 skill-creator 方式重构文档结构、触发描述、实践反馈入口和 eval-ready 基础设施

## FAQ

### 1. 一定要用 BrightData 吗？
不一定。实验室主页、个人主页、CVF、OpenReview 等很多场景都可以优先用 Python 路线。LinkedIn 和强反爬页面更适合 BrightData。

### 2. 这个 skill 会直接保存到数据库或 Feishu 吗？
在 OpenClaw 场景下，可以把 CSV 或抓取结果导入飞书多维表格，并执行表格字段创建与批量写入；在 Claude Code 场景下，则更偏向本地脚本、CSV 和文档输出。

### 3. 这个 skill 更适合单人搜索，还是批量搜索？
都可以。它既可以处理单个 URL 的抽取，也适合批量搜索后统一分类、去重和生成邮件。

### 4. 为什么要专门记录实践案例？
因为很多抓取问题高度依赖站点结构和失败模式。把真实案例沉淀下来，能帮助 Claude / OpenClaw 在未来更快选对方法，而不是每次从零试错。

## 后续迭代入口

接下来会持续补充两类内容：

1. 实践最佳提示词：哪些提问方式能让 skill 更稳定地理解任务
2. 用户反馈记录：真实使用中哪些地方体验不好、哪些说明还不够清楚、哪些策略需要调整

这些内容会逐步沉淀到：
- `references/prompt-best-practices.md`
- `references/user-feedback-notes.md`
- `evals/evals.json`

## 版本说明

- 初始版：完成基础 skill 工作流与参考规则库
- Python 增强版：加入 Python 抓取路线与参考脚本
- 实战扩展版：持续沉淀 OpenReview、实验室主页、GitHub、CVF、TongClass 等案例
- 当前重构版：按最新 skill-creator 与 OpenClaw 使用方式优化说明文档、触发语义、实践案例承载和后续评测入口

---
name: Mapping-Skill
description: AI/ML 人才搜索、论文作者发现、实验室成员爬取、GitHub 研究者挖掘与个性化招聘邮件生成 skill。只要用户提到查找 AI/ML PhD、研究员、工程师，抓取实验室成员、OpenReview/CVF 会议作者、GitHub 网络研究者，提取主页/Scholar/GitHub/邮箱/研究方向，识别华人、分类去重，或把结果导入飞书多维表格并批量生成邮件，就应该优先使用这个 skill；即使用户没有明确说“使用 Mapping-Skill”，只要任务属于这些复合工作流，也应触发。
---

# Mapping-Skill

面向 Claude Code 与 OpenClaw 的 AI/ML 人才搜索与触达执行手册。

## 项目链接

- GitHub: https://github.com/16Miku/Mapping-Skill
- ClawHub: https://clawhub.ai/16Miku/mapping-skill

## 这个 skill 具备的能力

当用户提出以下任务时，应优先启用本 skill：

1. 搜索 AI/ML PhD、研究员、工程师
2. 抓取实验室成员主页并提取结构化信息
3. 抓取 OpenReview / CVF 论文作者信息
4. 从 GitHub following/followers 网络中发现研究者
5. 对给定 URL 执行全量学者信息抽取
6. 识别华人候选人、分类、去重、标准化研究方向
7. 基于候选人信息生成个性化招聘邮件
8. 将 CSV 或爬取结果导入飞书多维表格
9. 在飞书表格中批量生成并回写推荐邮件

## 执行原则

1. **先判定任务类型，再选方法**
   - Topic search
   - Lab search
   - Conference author search
   - GitHub network discovery
   - Given-URL extraction
   - Feishu email workflow

2. **优先复用已有 references 与 scripts**
   不要从零发明流程。先检查 `references/` 与 `scripts/` 是否已有成熟模式。

3. **优先选择最稳定的数据入口**
   - OpenReview 会议优先 API
   - CVF 会议优先 HTML + PDF
   - Hugo Academic 页面优先模板化解析
   - 页面结构混乱但邮箱明显时，使用邮箱反向定位法

4. **抽取与清洗并重**
   结果必须尽量结构化，并在输出前做分类、去重与字段标准化。

5. **邮件必须基于真实信息个性化**
   `technical_hook` 和 `talk_track_paragraph` 不能空泛，必须和候选人论文、研究方向或主页内容关联。

6. **如用户涉及 OpenClaw / 飞书场景，要显式考虑导表和字段回写**
   对此类需求，结果不应只停留在本地 CSV。

## 平台使用说明

### Claude Code

适用于：
- 本地脚本执行
- MCP 工具调用
- CSV 导出
- 以本地文件和结构化结果为主要交付物

安装方式通常是把 skill 放到 `~/.claude/skills/` 目录。

### OpenClaw

适用于：
- skill 目录托管与刷新
- slash commands 调用
- ClawHub 分发
- 飞书、多工具联动工作流

OpenClaw 常见技能加载位置：
- `<workspace>/skills`
- `~/.openclaw/skills`
- 内置 skills

也可通过 ClawHub 安装，并通过“刷新 skills”或重启网关重新索引。

## 工作流

### Step 1：识别输入任务与目标输出

先明确：
- 搜索范围是 topic、lab、conference、GitHub network 还是给定 URL
- 输出要求是候选人列表、CSV、飞书入表、邮件生成，还是全流程都要
- 是否需要识别华人、是否需要邮箱、是否需要导入飞书

### Step 2：选择数据源与抓取方式

#### 方法选择矩阵

| 场景 | 首选方案 | 备用方案 |
|------|----------|----------|
| OpenReview 会议 | `scripts/openreview_scraper.py` + API | 搜索 + 主页回补 |
| CVF 会议 | `scripts/cvf_paper_scraper.py` | 补抓 PDF / 页面回退 |
| Hugo Academic 单页卡片 | `lab_member_scraper.py` 的 card 模式 | BrightData |
| 实验室列表页 + 个人页 | `lab_member_scraper.py` 的两阶段模式 | BrightData |
| 无固定结构但含邮箱 | 邮箱反向定位法 | BrightData / 手工规则 |
| GitHub 研究者网络 | `scripts/github_network_scraper.py` | 网页搜索辅助 |
| LinkedIn / 强反爬站点 | BrightData MCP | 降级到公开网页信息 |
| 给定任意 URL | BrightData MCP 或定制脚本 | 多源补充 |

### Step 3：执行抽取

根据场景读取相应脚本或 reference：

- 搜索模板：`references/search-templates.md`
- Python 爬取：`references/python-scraping-guide.md`
- 反爬处理：`references/anti-scraping-solutions.md`
- URL 优先级：`references/url-priority-rules.md`
- 会议抓取：`references/conference-paper-scraping.md`

### Step 4：结构化与标准化

至少尽量抽取这些字段：
- 中文名 / 英文名
- title / role
- affiliation
- research_interests / research_field
- education / experience
- publications
- homepage / Google Scholar / GitHub / LinkedIn / Zhihu / Bilibili
- email

然后继续做：
- 华人识别：`references/chinese-surnames.md`
- 候选人分类：`references/candidate-classifier.md`
- 去重：`references/deduplication-rules.md`
- 研究方向标准化：`references/field-mappings.md`

### Step 5：邮件生成

读取：
- `references/email-templates.md`
- `references/talk-tracks.md`

生成邮件时必须填充：
- `researcher_name`
- `context_affiliation`
- `research_field`
- `technical_hook`
- `talk_track_paragraph`

### Step 6：结果交付

根据用户要求输出为：
- Markdown 结构化表格
- CSV 文件
- 飞书多维表格
- 飞书表格中的“推荐邮件”字段

## OpenClaw / 飞书工作流要点

如果用户明确提到 OpenClaw、飞书、多维表格、导表或批量写邮件，应把这些步骤视为本 skill 的标准能力，而不是额外加分项。

### 标准能力

1. 解析飞书多维表格链接
2. 提取 `app_token` / `table_id`
3. 批量读取记录
4. 依据论文标题或候选人关键词映射研究方向
5. 批量生成个性化邮件
6. 创建新字段并批量更新记录
7. 返回飞书链接、成功/失败统计与原因

## 最佳实践提示词

后续如果有新的实践文档，应继续沉淀到 `references/prompt-best-practices.md`。当前优先复用下面几类高价值提示词模式。

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

## 输出格式

### 候选人摘要表

| Name | Type | Affiliation | Field | Chinese? | Email |
|------|------|-------------|-------|----------|-------|
| Wei Zhang | PhD | Tsinghua | RL | Yes (0.92) | wei@tsinghua.edu |

### 单个候选人详细输出

```markdown
## Candidate: Wei Zhang (张伟)

- Type: PhD Student
- Affiliation: Tsinghua University
- Research Field: Reinforcement Learning
- Chinese: Yes (0.92)
- Email: wei.zhang@tsinghua.edu.cn
- Homepage: ...
- Scholar: ...
- GitHub: ...

### Research Summary
- RLHF
- Reward modeling
- Policy optimization

### Publications
1. ...
2. ...

### Outreach Email
...
```

### 飞书工作流输出

至少返回：
- 飞书多维表格链接
- 总记录数 / 成功数 / 失败数
- 邮箱提取统计（如有）
- 失败原因摘要

## References guide

按场景加载：

- 通用搜索：`references/search-templates.md`
- 候选人字段：`references/profile-schema.md`
- 分类：`references/candidate-classifier.md`
- 华人识别：`references/chinese-surnames.md`
- 去重：`references/deduplication-rules.md`
- 邮件模板：`references/email-templates.md`
- talk tracks：`references/talk-tracks.md`
- Python 抓取：`references/python-scraping-guide.md`
- 反爬处理：`references/anti-scraping-solutions.md`
- 会议抓取：`references/conference-paper-scraping.md`
- 后续实践复盘：`references/practice-cases.md`
- 后续最佳提示词：`references/prompt-best-practices.md`
- 后续用户反馈：`references/user-feedback-notes.md`

## Scripts guide

- `scripts/openreview_scraper.py`：OpenReview 会议论文与作者抓取
- `scripts/cvf_paper_scraper.py`：CVF 论文页面 + PDF 邮箱提取
- `scripts/lab_member_scraper.py`：实验室成员抓取（两阶段 / Hugo Academic / 邮箱反向定位）
- `scripts/github_network_scraper.py`：GitHub 研究者网络抽取
- `scripts/cloudflare_email_decoder.py`：Cloudflare XOR 邮箱解密
- `scripts/httpx_scraper.py`：通用异步 HTTP 抓取
- `scripts/serper_search.py`：搜索入口模板

## 不要遗漏的经验

1. OpenReview 优先 API，不要一上来就网页搜索
2. CVF 邮箱提取优先 PDF 首页文本
3. Hugo Academic 要先判断是 card 模式还是两阶段模式
4. 中国高校站点要考虑 `[at]` 混淆和 SSL 问题
5. 页面结构混乱时，优先尝试邮箱反向定位法
6. GitHub README 往往能补齐 Scholar / Homepage / LinkedIn
7. 若用户要求飞书结果，必须考虑表字段创建与批量更新

## 后续迭代入口

后续收到新的实践文档后：
1. 把高价值提示词加入 `references/prompt-best-practices.md`
2. 在本 `SKILL.md` 的“最佳实践提示词”部分补充该功能已支持的明确说明
3. 将踩坑与修复沉淀到 `references/user-feedback-notes.md`
4. 必要时补充 `evals/evals.json` 做后续测试

---
description: LetPub 期刊数据爬取 - 查询期刊详情、分析评论、推荐期刊
---

# LetPub Skills

LetPub 期刊数据爬取工具，提供三大核心能力：

1. **查询期刊详情** —— 输入期刊名称，返回完整详情（影响因子、分区、审稿速度等）
2. **分析期刊评论** —— 输入期刊名称，遍历多页评论，综合评判该期刊
3. **推荐投稿期刊** —— 根据论文摘要，由 AI 智能调用搜索接口推荐合适期刊

---

## 功能 1：查询期刊详情

**流程**：期刊名称 → 自动补全搜索拿到 `journal_id` → 请求详情页 → 解析返回。

```python
from letpub_skills.scripts.search_journal import search_journal
from letpub_skills.scripts.get_details import get_journal_detail

# 第1步：搜索拿到 journal_id
results = search_journal("CHEMICAL ENGINEERING SCIENCE")
journal_id = results[0]['id']  # 例如 "1642"

# 第2步：一步到位获取详情（请求 + 解析）
journal = get_journal_detail(journal_id)

print(journal['impact_factor'])         # 影响因子
print(journal['ch_sci_2025']['分区'])    # 中科院分区
print(journal['speed'])                 # 审稿速度
print(journal['similar_journals'])      # 同类著名期刊
```

> 字段详解见 `references/get_journal_detail.md`

---

## 功能 2：分析期刊评论

**流程**：期刊名称 → （复用功能1拿到的 `journal_id`，否则重新搜索）→ 自动翻页、去重，累积评论直至满足数量 → 综合分析。

```python
from letpub_skills.scripts.search_journal import search_journal
from letpub_skills.scripts.get_comments import fetch_all_comments

# 如果已通过功能1拿到 journal_id，直接复用；否则：
results = search_journal("CHEMICAL ENGINEERING SCIENCE")
journal_id = results[0]['id']

# 自动翻页、去重，至少获取 30 条评论（不足则继续翻页直至无新数据）
all_comments = fetch_all_comments(journal_id, min_count=30)

print(f"共获取 {len(all_comments)} 条评论")
# 然后由 AI 对 all_comments 进行综合分析（审稿速度、录用难度、用户口碑、常见反馈等）
```

### Cookies 配置（自动）

评论需要登录才能获取。**脚本已支持自动登录续期**：

1. 在 `letpub_skills/assets/credentials.json` 填入账号密码：

```json
{ "email": "your@email.com", "password": "your_password" }
```

2. 调用 `get_journal_comments()` 时，若 cookie 已失效，脚本会**自动读取 credentials.json 重新登录**并更新 `cookies.json`，对调用者完全透明。

3. 如需手动触发登录：

```python
from letpub_skills.scripts.login import auto_login, load_credentials
email, password = load_credentials()
cookies = auto_login(email, password)  # 登录并保存到 cookies.json
```

### 评论字段（每条评论）
`floor`、`author`、`score`(0-10)、`research_fields`、`experience`(投稿经验)、`replies`(回复数组)、`good_count`、`bad_count` 等。

> 详见 `references/get_journal_comments.md`

### 评论中常见缩写

用户在 `experience` 中常使用以下缩写描述投稿流程，分析时需理解其含义：

| 缩写 | 全称 | 中文释义 | 数字解读 |
|------|------|----------|----------|
| STJ | Submit to Journal | 提交至期刊 | 刚投递，待初审 |
| WE | With Editor | 编辑处理中 | 编辑分配稿件、筛选审稿人 |
| UR | Under Review | 外审审稿中 | X-Y-Z：邀约数-接受数-返稿数 |
| RRC | Required Reviews Completed | 审稿意见收齐 | 已集齐评审意见，等待编辑终审 |

### AI 分析提示词建议
> 你是期刊投稿顾问。基于以下 N 条用户投稿评论，请综合分析：
> 1. **审稿速度**：从 `experience` 中提取投稿到接收的时间跨度，给出平均/范围。
> 2. **录用难度**：统计 `score` 分布，提取拒稿/小修/大修比例。
> 3. **用户口碑**：高频正/负面关键词。
> 4. **常见问题**：编辑响应、审稿人专业度、流程透明度等。
> 5. **投稿建议**：给出"推荐 / 谨慎 / 不推荐"的明确结论。

---

## 功能 3：推荐投稿期刊（AI 主导）

**流程**：用户提供论文摘要和需求 → **由 AI 分析摘要主题** → AI 阅读 `references/search_journal.md` 中的 `CATEGORY_CN` / `SUBCATEGORY_CN` → AI 选择合适学科分类和筛选条件 → 调用 `search_journals_advanced` → 解析返回。

### 可用的搜索参数

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `searchcategory1` | 大类学科（中文） | 21个，见 `references/search_journal.md` |
| `searchcategory2` | 小类学科（中文） | 见 `references/search_journal.md` |
| `searchscitype` | SCI 收录类型 | `SCIE`, `SSCI`, `ESCI`, `AHCI`, `SCOPUS`, `DOAJ` |
| `searchjcrkind` | 新锐期刊分区 | `1`, `2`, `3`, `4` |
| `searchopenaccess` | 是否 OA | `YES`, `Hybrid`, `NO` |
| `searchimpactlow` | 影响因子下限 | 数字字符串 |
| `searchimpacthigh` | 影响因子上限 | 数字字符串 |
| `searchsort` | 排序方式 | `relevance`, `impactor`, `rankscore`, `jciscore`, `clickcount` |

### 调用示例

```python
from letpub_skills.scripts.search_journal import search_journals_advanced, parse_search_results

# AI 根据摘要分析后填入参数
html = search_journals_advanced(
    searchcategory1="计算机科学",
    searchcategory2="计算机：人工智能",
    searchimpactlow="5",
    searchscitype="SCIE",
    searchsort="impactor"
)
result = parse_search_results(html)
print(f"共 {result['total_records']} 条记录")
for j in result['journals']:
    print(f"{j['name']} - IF:{j['impact_factor']} - {j['partition']}")
```

### AI 推荐期刊提示词

> 你是期刊推荐助手。请按以下步骤处理用户的论文摘要：
>
> **1. 分析摘要主题**
> 阅读用户提供的摘要，识别：
> - 主要研究领域（如 deep learning、cancer treatment、catalysis 等）
> - 研究方法（实验/理论/计算/综述）
> - 应用方向（医学/工程/基础科学）
>
> **2. 查阅学科分类**
> 阅读 `references/search_journal.md` 中的 `CATEGORY_CN`（21个大类）和 `SUBCATEGORY_CN`（每个大类下的小类），从中选出最匹配的 1-3 个组合：
> - 主分类：最贴合的 `searchcategory1`
> - 子分类：进一步精确定位的 `searchcategory2`
>
> **3. 综合用户需求决定筛选条件**
> 根据用户的额外要求（如"想投高影响因子"、"必须 OA"、"中科院 1 区"等），合理设置：
> - `searchimpactlow` / `searchimpacthigh`：影响因子范围
> - `searchscitype`：SCI 收录类型
> - `searchopenaccess`：是否 OA
> - `searchjcrkind`：分区要求
> - `searchsort`：排序方式（默认按影响因子降序 `impactor`）
>
> **4. 调用 `search_journals_advanced` 并解析结果**
> 必要时尝试不同的分类组合，提供 5-10 个候选期刊，附上选择理由（学科匹配度、IF、分区、审稿速度等）。
>
> **5. 候选期刊质量审核（必做，基于功能 2 的评论数据）**
> 对每个候选期刊调用功能 2 抓取评论，按以下硬性门槛筛掉不合格期刊，只把通过审核的期刊推荐给用户：
>
> - **评论数量** ≥ **10 条**（指顶层独立评论 / `floor` 计数 ≥ 10，**不包含** `replies` 中的层级回复；不足 10 条则继续翻页直至满足或无新数据）
> - **综合评分** ≥ **7.0 / 10**（所有评论 `score` 的算术平均值）
> - **「慢/拖/压稿」负面比例** < **30%**（在 `experience` 字段中命中关键词：`慢`、`拖`、`太慢`、`迟迟`、`卡在编辑`、`压稿`、`一直with editor`、`WE很久`、`WE太慢` 等的评论占比；注意：单独出现 `WE` 或 `with editor` 是正常流程，不算负面）
> - **无学术诚信负评**（任一评论命中以下关键词即整体淘汰，**一票否决**）：`学术道德`、`学术不端`、`抄袭`、`剽窃`、`政治原因`、`分赃`、`黑幕`、`要求引用`、`强制引用`
>
> **去重与 Cookie 失效检测**：
> `fetch_all_comments` 已内置基于 `floor` 的去重逻辑。若连续 2 页拿到的都是同一批评论（即新页评论与已有集合完全重合），说明 cookie 很可能已失效——此时 `get_journal_comments` 会**自动触发重新登录**（读取 `credentials.json` 并更新 `cookies.json`），然后重试。若续期后仍无新数据，函数会自动停止翻页，不会无限循环。
>
> 在最终输出中，对每个推荐期刊附上审核结果摘要：评论条数、平均分、慢审比例、是否存在诚信负评。

> 完整学科分类数据详见 `references/search_journal.md`

---

## 目录结构

```
letpub_skills/
├── SKILL.md                    # 操作手册（本文件）
├── assets/
│   ├── credentials.json        # 账号密码（用户填写）
│   └── cookies.json            # 登录 cookies（自动生成，无需手动修改）
├── scripts/
│   ├── login.py                # 自动登录与 cookie 续期
│   ├── search_journal.py       # 期刊搜索（自动补全 + 高级搜索）
│   ├── get_details.py          # 期刊详情解析
│   └── get_comments.py         # 评论获取与解析（自动续期登录）
└── references/
    ├── search_journal.md       # 搜索参数与学科分类完整数据
    ├── get_journal_detail.md   # 详情字段说明
    └── get_journal_comments.md # 评论字段说明
```

## 主要函数

| 模块 | 函数 | 说明 |
|------|------|------|
| `login` | `load_credentials()` | 从 credentials.json 读取账号密码 |
| `login` | `auto_login(email, password)` | 登录并保存 cookies |
| `login` | `ensure_logged_in()` | 检查 cookie 有效性，失效时自动续期 |
| `search_journal` | `search_journal(name)` | 自动补全搜索，返回 `journal_id` |
| `search_journal` | `search_journals_advanced(**params)` | 高级多条件搜索 |
| `search_journal` | `parse_search_results(html)` | 解析搜索结果 |
| `search_journal` | `CATEGORY_CN`, `SUBCATEGORY_CN` | 学科分类数据 |
| `get_details` | `get_journal_detail(journal_id)` | 一步获取并解析期刊详情 |
| `get_details` | `parse_journal_detail(html)` | 解析期刊详情页 |
| `get_comments` | `fetch_all_comments(journal_id, min_count)` | 自动翻页去重抓取评论 |
| `get_comments` | `get_journal_comments(journal_id, page)` | 获取单页评论原始响应（自动续期） |
| `get_comments` | `parse_comments_response(data)` | 解析评论列表 |

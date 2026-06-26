# paper-lark-report

全自动科研论文日报/周报生成 Skill。基于 arXiv API 精准检索 + LLM 语义评分 + 飞书 Wiki 推送。

---

## 安装

```bash
# 方式一：通过 ClawHub 安装
npx clawhub@latest install leogoat2004/paper-lark-report

# 方式二：通过 OpenClaw CLI 安装
openclaw skills install leogoat2004/paper-lark-report
```

---

## 核心流程

```
cron --(isolated session)--> run_daily()
    ├─ build_arxiv_query(research_direction)
    ├─ fetch_arxiv_papers(query, max_search_results=20)
    ├─ 去重（processed_ids.json）
    ├─ fetch_arxiv_details(filtered[:20])
    └─ 保存 data/daily_papers.json
            │
            ▼
       LLM isolated session
            ├─ 评分（0-10）
            ├─ 精选 Top max_daily_papers
            ├─ 从 full_abstract 提取 motivation + core_innovation（中文）
            ├─ 写入 data/selected_papers.json
            ├─ --save-selected
            ├─ feishu-create-doc skill 创建 Wiki 文档（子节点）
            └─ --register-doc
```

---

## 目录结构

```
paper-lark-report/
├── SKILL.md
├── config.yaml
├── data/
│   ├── doc_registry.json
│   ├── processed_ids.json
│   ├── daily_papers.json      # 候选论文（LLM 输入）
│   ├── selected_papers.json    # 精选结果（含中文分析）
│   └── doc_result.json         # 最近创建文档的 token/url
├── processed_log/
│   └── YYYY-MM-DD.json         # 每日归档（供周报聚合）
├── scripts/
│   ├── arxiv_search.py         # arXiv API
│   ├── paper_lark_report.py     # 主入口
│   └── create_feishu_doc.py    # 飞书 Wiki 创建（直接 API）
└── templates/
    ├── daily_report.md         # 日报模板（含 Instructions）
    └── weekly_report.md        # 周报模板（含 Instructions）
```

---

## 配置（config.yaml）

| 字段 | 说明 |
|------|------|
| `feishu_space_id` | Wiki 空间 ID（整数，URL 中提取） |
| `feishu_parent_node` | 父节点 token，创建在 paper-lark-report 节点下 |
| `research_direction` | 自由文本研究方向描述 |
| `max_search_results` | 每日 arXiv 最多获取篇数（默认 20） |
| `max_daily_papers` | 日报最多精选篇数（默认 3） |
| `arxiv_paper_max_days` | 论文最大天数（默认 7） |
| `daily_cron` / `weekly_cron` | cron 表达式（UTC+8） |

---

## arXiv 查询策略

Query 构建规则：`abs:core_term AND (abs:term1 OR abs:term2 OR ...)`

- 第一个词作为 AND 核心，其余 OR 扩展
- 识别复合词（multi-agent 等）作为原子单元
- 过滤泛化词（towards/safe/efficient 等）
- 最多 8 个词

---

## 飞书 Wiki API 验证过的要点

### 节点创建
```
POST /wiki/v2/spaces/{space_id}/nodes
body: { obj_type: "docx", parent_node_token, node_type: "origin", title }
返回: { node_token, obj_token }
```
**注意**：Wiki API 忽略传入的 obj_token，始终创建自己的空文档，必须用返回的 obj_token 写入。

### 写入可用 block type
| block_type | 类型 | 可用 |
|-----------|------|------|
| 2 | text/paragraph | ✅ |
| 3 | heading1 | ✅ |
| 4 | heading2 | ✅ |
| 5 | heading3 | ✅ |
| 25 | divider | ❌ 1770029 |
| 27 | callout | ❌ 字段校验严 |
| 31 | table | ❌ 参数结构不对 |

### 关键参数
- `space_id`：必须是**整数**，不是字符串
- `parent_node`：父节点 token，文档创建在其下级
- Token 获取：从 `openclaw.json` 的 `channels.feishu.appId/appSecret` 换取 tenant_access_token

---

## CLI

```bash
# 日报（cron 触发）
python3 scripts/paper_lark_report.py

# 周报
python3 scripts/paper_lark_report.py --weekly

# LLM 选完论文后
python3 scripts/paper_lark_report.py --save-selected "YYYY-MM-DD" "data/selected_papers.json"
python3 scripts/paper_lark_report.py --register-doc "<node_token>" "<obj_token>" "<doc_url>"
```



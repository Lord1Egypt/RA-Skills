# RAG 系统搭建标准接口规范 v1.0

> 本规范将 HTML 配置面板的每一控件映射为标准化参数。
> LLM 通过文字交互搭建 RAG 时，必须使用此规范逐一填写所有参数（自动/默认/询问），不可跳过。

---

## 1. 参数清单（闭合配置域）

共 **8 大模块、32 个参数**。任何 RAG 搭建请求必须走完所有模块。

### 1.1 输入源 — input_sources

| # | 参数 | 类型 | 默认值 | 钩子行为 |
|---|------|------|--------|---------|
| 1 | enable_pdf | bool | false | 用户说"要处理PDF"→true；否则默认false |
| 2 | enable_ocr | bool | false | 用户说"扫描件"/"图片PDF"→true；否则默认false |
| 3 | enable_html2md | bool | false | 用户说"网页"/"HTML"→true；否则默认false |
| 4 | pdf_backend | enum | pypdf | 选项: pypdf / pdfplumber；用户未指定→默认 |

### 1.2 嵌入模型 — embedding

| # | 参数 | 类型 | 默认值 | 钩子行为 |
|---|------|------|--------|---------|
| 5 | model | string | BAAI/bge-small-zh-v1.5 | 用户说"中文"→bge-small-zh；"英文"→all-MiniLM-L6-v2；否则默认→询问 |
| 6 | device | enum | auto | 检测到CUDA→cuda；否则→cpu；用户可指定 |

### 1.3 文档切片 — splitting

| # | 参数 | 类型 | 默认值 | 钩子行为 |
|---|------|------|--------|---------|
| 7 | strategy | enum | recursive | 选项: recursive/fixed/headers/sentence/semantic |
| 8 | chunk_size | int | 500 | 用户说"精细切"→200；"粗略切"→1000；否则默认500 |
| 9 | chunk_overlap | int | 50 | 默认50，语义切→0 |
| 10 | separators | list[str] | ["\n\n","\n","。","；","，"," ",""] | 递归切专用，默认值 |
| 11 | headers_to_split_on | list | [["#","h1"],["##","h2"],["###","h3"]] | 标题切专用 |
| 12 | guards | list[str] | ["code"] | 多选: mermaid/code/math/table/html；默认code |
| 13 | secondary_strategy | string/null | null | 后处理策略: recursive/fixed/semantic/空=不启用 |

### 1.4 检索参数 — retrieval

| # | 参数 | 类型 | 默认值 | 钩子行为 |
|---|------|------|--------|---------|
| 14 | k | int | 3 | top-K 召回数 |
| 15 | score_threshold | float/null | null | 相似度阈值，null=不启用 |
| 16 | search_type | enum | similarity | 选项: similarity / mmr |

### 1.5 知识库 — kb

| # | 参数 | 类型 | 默认值 | 钩子行为 |
|---|------|------|--------|---------|
| 17 | name | string | — | 必填。用户未指定→询问知识库名称和用途 |
| 18 | description | string | "" | 可选，用于 LLM 自动分类 |
| 19 | embedding_model | string | — | 默认使用全局嵌入模型 |
| 20 | classify_rules | list[dict] | [] | 关键词规则：[{keywords:["..."], extensions:[...], description:""}] |
| 21 | enabled | bool | true | 多知识库路由开关 |

### 1.6 路由层 — router

| # | 参数 | 类型 | 默认值 | 钩子行为 |
|---|------|------|--------|---------|
| 22 | enabled | bool | true | KB 关闭时自动禁用 |
| 23 | fallback_model | string | BAAI/bge-reranker-v2-m3 | 语义回退路由模型 |
| 24 | min_score_threshold | float | 0.3 | 低于此值触发广播 |
| 25 | broadcast_on_fail | bool | true | 回退路由也失败时全量检索所有 KB |

### 1.7 Rerank 层 — reranker

| # | 参数 | 类型 | 默认值 | 钩子行为 |
|---|------|------|--------|---------|
| 26 | enabled | bool | false | **默认关闭**。用户明确要求精度排序→开启 |
| 27 | mode | enum | model | model/rule/hybrid；默认model（需模型），用户选rule只用规则 |
| 28 | model | string | BAAI/bge-reranker-v2-m3 | mode=model/hybrid 时必选；mode=rule 时忽略 |
| 29 | top_k | int | 5 | 精排后取前N条送 LLM |
| 30 | sort_rules | list[dict] | [] | mode=rule/hybrid 时生效；每项有 type + 参数 |

### 1.8 LLM 模式 — llm

| # | 参数 | 类型 | 默认值 | 钩子行为 |
|---|------|------|--------|---------|
| 31 | mode | enum | integrated | integrated=纯检索/standalone=检索+LLM |
| 32 | standalone.llm | dict | {} | standalone 模式时必须配置 base_url / model_name |

---

## 2. 搭建执行流水线（6 阶段）

LLM 必须按顺序执行以下阶段，每阶段完成后才能进入下一阶段。

```
阶段 1: 参数采集（走完 32 个参数，不留缺口）
  │
  ▼
阶段 2: 环境检测 & 修复
  ├─ python 版本检查（3.8-3.11）
  ├─ pip 可用性检查
  ├─ 缺失包检测 → 自动安装（可选镜像源）
  └─ GPU 检测（影响 device 参数）
  │
  ▼
阶段 3: 模型下载
  ├─ 嵌入模型（bge-small-zh-v1.5 等）
  ├─ 回退路由模型（bge-reranker-v2-m3 等，如路由开启）
  └─ Rerank 模型（同 v2-m3，如 Rerank 开启）
  │
  ▼
阶段 4: 知识库创建
  ├─ 建库（向量数据库目录）
  ├─ 配置分类规则
  └─ 写入 config
  │
  ▼
阶段 5: 配置写入
  ├─ 合并全部参数 → rag_config.json
  └─ 写入 Prompt 模板（如默认模板不存在）
  │
  ▼
阶段 6: 验证
  ├─ config 完整性校验（32 参数必须齐全）
  ├─ 检索测试（创建测试文档→入库→检索→确认结果）
  └─ 输出验收报告
```

---

## 3. 钩子（Hook）定义

每个参数在 LLM 处理时遵循以下 5 步决策链：

```
Hook Entry
  │
  ├─ Step 1: 用户明确给出了吗？
  │   ├─ 是 → 直接使用，进入 Step 2
  │   └─ 否 → 进入 Step 3
  │
  ├─ Step 2: 值合法吗？
  │   ├─ 是 → 通过
  │   └─ 否 → 报错 + 告知合法范围 → 让用户修正
  │
  ├─ Step 3: 能否从用户语义推断？
  │   ├─ 是 → 推断值 + 告知用户"已设为 X"
  │   └─ 否 → 进入 Step 4
  │
  ├─ Step 4: 有安全默认值吗？
  │   ├─ 是 → 使用默认值 + 告知用户
  │   └─ 否 → 进入 Step 5
  │
  └─ Step 5: 询问用户
      └─ "请选择 X 的取值 [选项A/选项B/自定义]"
```

### 预填 vs 询问对照表

| 参数 | 推断条件 | 默认值 | 何时询问 |
|------|---------|--------|---------|
| enable_pdf | 语义含"PDF/文档/报告"→true | false | 均不确定时问 |
| strategy | "精准"/"语义"→semantic；"快速"→recursive | recursive | 均不确定时问 |
| chunk_size | "精细"→200；"粗略"→1000 | 500 | 均不确定时问 |
| reranker.enabled | "精度高"/"排序准确"→true | false | 均不确定时问 |
| kb.name | 从文档类型推断：代码→tech_kb，法律→legal_kb | — | **必填，必须问** |
| llm.mode | "自己回答"/"LLM"→standalone | integrated | 语义模糊时问 |

---

## 4. 编排函数签名

```python
def setup_rag(params: dict) -> dict:
    """
    params: 用户提供的自然语言输入（非结构化）
    返回: {
        "success": bool,
        "config": dict,      # 完整 32 参数配置
        "env_report": dict,  # 环境检测报告
        "models": dict,      # 模型下载结果
        "kb": dict,          # 知识库创建结果
        "validation": dict,  # 验证结果
    }
    
    钩子:
    - 每步执行前检查参数完整性
    - 缺失参数从用户输入推断 → 默认 → 询问
    """
```

## 5. 验证标准

搭建完成后必须通过以下检查才算成功：

| # | 检查项 | 通过条件 |
|---|--------|---------|
| 1 | config 完整性 | 32 参数全部存在，类型正确 |
| 2 | 环境就绪 | 必需包全部已安装 |
| 3 | 模型就绪 | 嵌入模型 + 路由模型 + Rerank 模型文件存在 |
| 4 | 知识库就绪 | Chroma 向量库目录存在，可写入 |
| 5 | 检索可用 | `rag_skill.py --query "test"` 返回正常 |

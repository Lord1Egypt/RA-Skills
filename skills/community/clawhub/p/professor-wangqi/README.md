# 王琦教授中医体质学术助手

基于王琦教授学术论文与诊疗经验的可追溯学术学习助手。

## 项目结构

```
professor-wangqi/
├── SKILL.md                          # Skill主文件：触发条件、工作流、回答格式
├── README.md                         # 本文档
├── requirements.txt                  # Python依赖
├── references/                       # 参考文档
│   ├── knowledge-card-schema.md      # 知识卡提取schema定义
│   └── ontology.md                   # 术语表：体质、证型、方药术语归一化
├── scripts/                          # 数据处理脚本
│   ├── extract_knowledge_cards.py    # PDF解析与知识卡提取
│   ├── build_local_index.py          # ChromaDB向量索引构建
│   ├── build_vector_index.py         # 通用向量索引构建（支持chroma/milvus/weaviate）
│   └── ask.py                        # 问答脚本
├── evals/                            # 评测集
│   └── evals.json                    # 测试问题与断言
└── assets/                           # 资产文件（预留）
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

在项目根目录创建`.env`文件：

```env
# Chat模型配置（本地LM Studio）
API_KEY=sk-your-api-key
BASE_URL=http://your.baseurl.here/v1
MODEL_NAME=qwen/qwen3.6-35b-a3b

# Embedding模型配置
EMBEDDING_MODEL=text-embedding-nomic-embed-text-v1.5
EMBEDDING_BASE_URL=http://your.baseurl.here/v1
EMBEDDING_API_KEY=sk-your-api-key
EMBEDDING_DIMENSIONS=768
```

### 3. 准备数据

将PDF文件放入对应目录：
```
data/
├── 01-体质与疾病文章-SCI/    # 13篇SCI论文
└── 03-王琦老师诊疗经验/      # 25篇诊疗经验
```

### 4. 提取知识卡

```bash
# 提取SCI论文
python scripts/extract_knowledge_cards.py \
    --input data/01-体质与疾病文章-SCI/ \
    --output data/cards/papers/ \
    --type paper

# 提取诊疗经验
python scripts/extract_knowledge_cards.py \
    --input data/03-王琦老师诊疗经验/ \
    --output data/cards/experiences/ \
    --type experience
```

### 5. 构建向量索引

```bash
# 使用ChromaDB（推荐）
python scripts/build_local_index.py \
    --cards data/cards/ \
    --collection wangqi_knowledge \
    --persist-dir ./chroma_db

# 或使用通用脚本
python scripts/build_vector_index.py \
    --cards data/cards/ \
    --db chroma \
    --collection wangqi_knowledge
```

### 6. 问答测试

```bash
# 单次问答
python scripts/ask.py "痰湿质与肥胖有什么关系？"

# 交互模式
python scripts/ask.py --interactive
```

---

## 架构说明

```
┌─────────────────────────────────────────────────────────┐
│                    用户问题                              │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│              ChromaDB (本地向量库)                       │
│  - 知识卡向量索引                                        │
│  - 语义检索（Top-K相关文档）                             │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│              本地LLM (LM Studio)                         │
│  - 加载SKILL.md作为系统指令                              │
│  - 检索增强生成（RAG）                                   │
│  - 标注证据来源类型                                      │
└─────────────────────────────────────────────────────────┘
```

---

## 核心特性

### 1. 可追溯性
- 每个学术观点标注出处
- 区分证据层级：`[论文]` / `[诊疗经验]` / `[知识归纳]` / `[模型推断]`
- 不确定时明确说明"现有材料未涉及"

### 2. 安全边界
- 定位为学术学习助手，不替代临床诊疗
- 涉及诊断/剂量时附加警示声明
- 评测集包含安全边界测试用例

### 3. 证据分级

| 标签 | 含义 | 证据强度 |
|------|------|----------|
| `[论文]` | 来自SCI论文，有研究数据支撑 | 高 |
| `[诊疗经验]` | 来自临床诊疗经验文章 | 中 |
| `[知识归纳]` | 基于多篇材料归纳 | 中低 |
| `[模型推断]` | 基于已有知识的合理延伸 | 低 |

---

## 知识卡Schema

每张知识卡包含以下核心字段：

| 字段 | 说明 | 必填 |
|------|------|------|
| card_id | 知识卡唯一标识 | ✓ |
| source_type | paper / clinical_experience | ✓ |
| source_file | 原始PDF文件名 | ✓ |
| title | 文献标题 | ✓ |
| authors | 作者列表 | ✓ |
| year | 发表年份 | ✓ |
| language | zh / en | ✓ |
| abstract | 摘要（论文） | |
| conclusions | 结论 | |
| knowledge_points | 知识点列表 | |
| related_constitutions | 相关体质 | |
| related_diseases | 相关疾病 | |
| evidence_sentences | 证据句原文 | |
| treatment_approach | 治疗方案（诊疗经验） | |

详见 `references/knowledge-card-schema.md`

---

## 评测

评测集位于 `evals/evals.json`，包含12个测试用例：

- 学术问答（体质理论、研究发现）
- 临床思路学习（辨证论治、诊疗思路）
- 理论体系梳理
- 方药知识查询
- 安全边界测试
- 证据溯源测试
- 不确定回答测试

运行评测：
```bash
# 使用skill-creator的评测流程
```

---

## 后续扩展

1. **问诊数据接入**
   - 设计问诊记录schema（脱敏处理）
   - 添加source_type="consultation_record"
   - 调整检索权重

2. **知识图谱构建**
   - 基于知识卡构建实体关系
   - 接入Neo4j或类似图数据库
   - 支持复杂推理查询

3. **多模态扩展**
   - 舌象图像识别
   - 脉诊数据分析

---

## 知识卡质量

### 质量指标

| 指标 | 数值 |
|------|------|
| 有效卡片率 | 100% (38/38) |
| 平均质量分 | 83.7/100 |
| 标题填充率 | 100% |
| 作者填充率 | 100% |
| 页码信息率 | 100% |

### 质量验证

```bash
# 验证知识卡质量
python scripts/validate_cards.py --cards data/cards/
```

---

## 提取改进 (v1.1.0)

### 标题提取增强

- **问题**: PDF元数据通常为空，导致75.7%的卡片标题为空
- **解决方案**: 多级fallback机制
  1. 从文本开头提取（过滤摘要、关键词等非标题行）
  2. 从文件名解析（去除PDF扩展名、数字前缀）
  3. 回退到元数据
- **效果**: 标题填充率从24.3%提升至100%

### 作者提取增强

- **问题**: 作者字段常为空或显示"CNKI"等通用值
- **解决方案**: 文本模式匹配
  - 检测"作者："、"编者："等显式标记
  - 从标题和摘要之间提取中文名（2-4字）
  - 过滤误判（摘要、关键词等）
- **效果**: 作者填充率从45.7%提升至100%

### 页码信息

- **新增字段**: `page_info`
  ```json
  {
    "total_pages": 10,
    "sections": {
      "abstract": {"start": 1, "end": 1},
      "conclusion": {"start": 8, "end": 9}
    }
  }
  ```
- **证据句页码**: 每个证据句现在包含`page_num`字段

### LLM知识点提取（可选）

- 使用`--use-llm`标志启用
- 从结论和摘要提取具体研究发现
- 过滤泛泛描述（"本文涉及XX相关研究"）
- 需要配置OpenAI兼容API（LM Studio）

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| 1.2.0 | 2026-04-22 | npm包发布准备、CLI用户目录支持、Claude Code安装修复 |
| 1.1.0 | 2026-04-21 | 提取增强：标题/作者fallback、页码信息、LLM知识点 |
| 1.0.0 | 2026-01-21 | 初始版本，支持论文和诊疗经验 |

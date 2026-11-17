# AI/技术产品品牌图标速查（Tech Product Icons）

当技术图表中出现已知产品时，使用本速查表中的品牌图标模板，确保品牌色和视觉风格一致。

**所有 SVG 代码遵守 PPT 大师禁用特性黑名单**：无 `<style>`、无 `class`。使用 inline 属性。

---

## 通用模板

所有产品图标使用统一的 **circle badge + text** 模式：

```xml
<!-- 标准产品图标模板 -->
<!-- 参数：cx=中心X, cy=中心Y, BRAND_COLOR=品牌色, BADGE_TEXT=缩写 -->
<g id="product-badge">
  <circle cx="{cx}" cy="{cy}" r="22" fill="{BRAND_COLOR}"/>
  <text x="{cx}" y="{cy+5}" text-anchor="middle" fill="white"
        font-size="10" font-weight="700"
        font-family="Helvetica, Arial, sans-serif">{BADGE_TEXT}</text>
  <!-- 可选：外环光晕 -->
  <circle cx="{cx}" cy="{cy}" r="24" fill="none"
          stroke="{BRAND_COLOR}" stroke-width="1" stroke-opacity="0.4"/>
</g>
```

### 图标尺寸指南

| 上下文 | 推荐尺寸 | 内边距 |
|--------|----------|--------|
| 节点内 badge | r=22（28×28px） | 10px |
| 独立图标节点 | r=30（40×40px） | 16px |
| 核心/中心节点 | r=38（56×56px） | 20px |
| 小型行内指示器 | r=12（16×16px） | 6px |

---

## AI / ML Products

| 产品 | 品牌色 | Badge 文字 | 文字色 |
|------|--------|-----------|--------|
| OpenAI / ChatGPT | `#10A37F` | `OAI` | white |
| Anthropic / Claude | `#D97757` | `Claude` | white |
| Google Gemini | `#4285F4` | `Gemini` | white |
| Meta LLaMA | `#0467DF` | `LLaMA` | white |
| Mistral | `#FF7000` | `Mistral` | white |
| Cohere | `#39594D` | `Cohere` | white |
| Groq | `#F55036` | `Groq` | white |
| Together AI | `#6366F1` | `Together` | white |
| Replicate | `#191919` | `Rep` | white |
| Hugging Face | `#FFD21E` | `HF` | `#1e293b` |

---

## AI Memory & RAG Products

| 产品 | 品牌色 | Badge 文字 |
|------|--------|-----------|
| Mem0 | `#6366F1` | `mem0` |
| LangChain | `#1C3C3C` | `LC` |
| LlamaIndex | `#8B5CF6` | `LI` |
| LangGraph | `#1C3C3C` | `LG` |
| CrewAI | `#EF4444` | `Crew` |
| AutoGen | `#0078D4` | `AG` |
| Haystack | `#FF6D00` | `HS` |
| DSPy | `#7C3AED` | `DSPy` |

---

## Vector Databases

| 产品 | 品牌色 | Badge 文字 |
|------|--------|-----------|
| Pinecone | `#1C1C2E` | `Pine` |
| Weaviate | `#FA0050` | `Wea` |
| Qdrant | `#DC244C` | `Qdrant` |
| Chroma | `#FF6B35` | `Chr` |
| Milvus | `#00A1EA` | `Milvus` |
| pgvector | `#336791` | `pgv` |
| Faiss | `#0467DF` | `FAISS` |

### Vector DB 专用模板（圆柱体 + badge）

```xml
<!-- Vector DB 专用：圆柱体形状 + 品牌标签 -->
<g id="vectordb-node">
  <ellipse cx="{cx}" cy="{top}" rx="40" ry="12"
           fill="{FILL}" stroke="{STROKE}" stroke-width="1.5"/>
  <rect x="{cx-40}" y="{top}" width="80" height="50"
        fill="{FILL}" stroke="none"/>
  <line x1="{cx-40}" y1="{top}" x2="{cx-40}" y2="{top+50}"
        stroke="{STROKE}" stroke-width="1.5"/>
  <line x1="{cx+40}" y1="{top}" x2="{cx+40}" y2="{top+50}"
        stroke="{STROKE}" stroke-width="1.5"/>
  <ellipse cx="{cx}" cy="{top+50}" rx="40" ry="12"
           fill="{FILL_DARK}" stroke="{STROKE}" stroke-width="1.5"/>
  <text x="{cx}" y="{top+30}" text-anchor="middle" fill="white"
        font-size="11" font-weight="700"
        font-family="Helvetica, Arial, sans-serif">{PRODUCT_NAME}</text>
</g>
```

---

## Classic Databases & Storage

| 产品 | 品牌色 | Badge 文字 |
|------|--------|-----------|
| PostgreSQL | `#336791` | `PG` |
| MySQL | `#4479A1` | `MySQL` |
| MongoDB | `#47A248` | `Mongo` |
| Redis | `#DC382D` | `Redis` |
| Elasticsearch | `#005571` | `ES` |
| Cassandra | `#1287B1` | `Cass` |
| Neo4j | `#008CC1` | `Neo4j` |
| SQLite | `#003B57` | `SQLite` |

---

## Message Queues & Streaming

| 产品 | 品牌色 | Badge 文字 |
|------|--------|-----------|
| Apache Kafka | `#231F20` | `Kafka` |
| RabbitMQ | `#FF6600` | `RMQ` |
| AWS SQS | `#FF9900` | `SQS` |
| NATS | `#27AAE1` | `NATS` |
| Pulsar | `#188FFF` | `Pulsar` |

---

## Cloud & Infra

| 产品 | 品牌色 | Badge 文字 |
|------|--------|-----------|
| AWS | `#FF9900` | `AWS` |
| GCP | `#4285F4` | `GCP` |
| Azure | `#0089D6` | `Azure` |
| Cloudflare | `#F48120` | `CF` |
| Vercel | `#000000` | `Vercel` |
| Docker | `#2496ED` | `Docker` |
| Kubernetes | `#326CE5` | `K8s` |
| Terraform | `#7B42BC` | `TF` |
| Nginx | `#009639` | `Nginx` |
| FastAPI | `#009688` | `FastAPI` |

---

## Observability

| 产品 | 品牌色 | Badge 文字 |
|------|--------|-----------|
| Grafana | `#F46800` | `Grafana` |
| Prometheus | `#E6522C` | `Prom` |
| Datadog | `#632CA6` | `DD` |
| LangSmith | `#1C3C3C` | `LS` |
| Langfuse | `#6366F1` | `Langfuse` |
| Arize | `#6B48FF` | `Arize` |

---


## Azure 服务图标

Azure 品牌色：`#0089D6`。服务使用 tile 模板：

```xml
<!-- Azure tile 模板：外层 Azure 蓝圆角方块 + 内层服务色 -->
<g id="azure-tile">
  <rect x="{cx-22}" y="{cy-22}" width="44" height="44" rx="6"
        fill="#0089D6" stroke="none"/>
  <rect x="{cx-19}" y="{cy-19}" width="38" height="38" rx="4"
        fill="{SERVICE_COLOR}" stroke="none"/>
  <text x="{cx}" y="{cy+5}" text-anchor="middle" fill="white"
        font-size="9" font-weight="700"
        font-family="Helvetica, Arial, sans-serif">{BADGE}</text>
</g>
```

### 常用 Azure 服务

| 服务 | 服务色 | Badge |
|------|--------|-------|
| Azure OpenAI | `#10A37F` | `AOAI` |
| Azure Functions | `#0062AD` | `Func` |
| Azure Cosmos DB | `#3D7AB3` | `Cosmos` |
| Azure Kubernetes (AKS) | `#326CE5` | `AKS` |
| Azure SQL | `#0066A1` | `SQL` |
| Azure Blob Storage | `#0078D4` | `Blob` |
| Azure Service Bus | `#0078D4` | `SB` |
| Azure Key Vault | `#FFB900` | `KV` |
| Azure API Management | `#1FBA9F` | `APIM` |
| Azure Monitor | `#0078D4` | `Monitor` |

> 完整 Azure 服务列表较长，此处仅列出技术图表中最常用的服务。如需更多服务图标，参考 Microsoft Azure 官方图标集。

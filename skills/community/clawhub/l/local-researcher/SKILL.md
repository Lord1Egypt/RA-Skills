---
name: local-researcher
description: 完全本地的深度研究助手 Skill。使用 Ollama 或 LMStudio 本地 LLM 进行迭代式网络研究，生成带引用来源的 Markdown 报告。当用户需要进行隐私优先的研究、本地文档分析或生成结构化研究报告时触发。
version: 1.0.0
---

# Local Researcher Skill

完全在本地运行的深度研究助手，无需将数据发送到云端 LLM 服务。支持 Ollama 和 LMStudio，迭代式网络研究，输出带引用的专业报告。

## 前置要求

### 安装 Ollama（推荐）

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull deepseek-r1:8b
ollama pull llama3.2
ollama pull qwen:14b
```

### 或使用 LMStudio

1. 下载 [LMStudio](https://lmstudio.ai/)
2. 下载并加载模型（如 qwen_qwq-32b）
3. 进入 "Local Server" 标签页
4. 启动 OpenAI 兼容 API 服务
5. 记下服务地址（默认: http://localhost:1234/v1）

### 安装本 Skill

```bash
# 克隆仓库
git clone https://github.com/langchain-ai/local-deep-researcher.git
cd local-deep-researcher

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -e .
```

## 配置

复制环境变量模板并编辑：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
# LLM 提供商选择
LLM_PROVIDER=ollama
# LLM_PROVIDER=lmstudio

# Ollama 配置
OLLAMA_BASE_URL=http://localhost:11434
LOCAL_LLM=deepseek-r1:8b

# LMStudio 配置
# LMSTUDIO_BASE_URL=http://localhost:1234/v1
# LOCAL_LLM=qwen_qwq-32b

# 搜索工具配置
SEARCH_API=duckduckgo  # 默认，无需 API key
# SEARCH_API=tavily
# TAVILY_API_KEY=tvly-xxx
# SEARCH_API=perplexity
# PERPLEXITY_API_KEY=pplx-xxx

# 研究循环次数
MAX_WEB_RESEARCH_LOOPS=3

# 是否获取完整页面内容
FETCH_FULL_PAGE=true
```

## 使用方法

### 快速开始

```bash
# 启动研究（交互模式）
python src/ollama_deep_researcher/main.py

# 或使用 LangGraph CLI
langgraph dev
```

### 程序化使用

```python
from langgraph.graph import StateGraph
from ollama_deep_researcher.graph import graph

# 定义研究主题
topic = "量子计算在药物发现中的应用"

# 配置参数
config = {
    "llm_provider": "ollama",
    "local_llm": "deepseek-r1:8b",
    "search_api": "duckduckgo",
    "max_web_research_loops": 3,
    "fetch_full_page": True
}

# 运行研究
result = graph.invoke(
    {"topic": topic},
    config=config
)

# 输出报告
print(result["final_summary"])
```

## 核心功能

### 1. 迭代式深度研究

系统自动执行以下循环：
1. 根据主题生成搜索查询
2. 执行网络搜索
3. 总结搜索结果
4. 反思总结，识别知识缺口
5. 生成新查询填补缺口
6. 重复直到达到最大循环次数

### 2. 多搜索源支持

| 搜索源 | 需要 API Key | 特点 |
|--------|-------------|------|
| DuckDuckGo | ❌ 不需要 | 默认选项，隐私友好 |
| Tavily | ✅ 需要 | 高质量搜索结果 |
| Perplexity | ✅ 需要 | AI 增强搜索 |
| SearXNG | ❌ 不需要 | 自托管选项 |

### 3. 输出格式

最终输出为 Markdown 格式报告，包含：
- 执行摘要
- 详细研究发现
- 所有引用的来源链接
- 研究过程元数据

### 4. LangGraph Studio 可视化

```bash
# 安装 LangGraph CLI
pip install "langgraph-cli[inmem]"

# 启动开发服务器
langgraph dev
```

打开浏览器访问 Studio UI，可实时观察研究流程：
- 搜索查询生成
- 来源收集
- 总结迭代
- 最终报告生成

## 完整工作流示例

### 学术论文预研

```python
import asyncio
from ollama_deep_researcher.graph import graph

async def research_paper_prep():
    topic = "Transformer 架构在生物信息学中的最新应用"
    
    config = {
        "llm_provider": "ollama",
        "local_llm": "deepseek-r1:14b",  # 使用更大模型获得更好结果
        "search_api": "duckduckgo",
        "max_web_research_loops": 5,  # 更多轮次深入挖掘
        "fetch_full_page": True
    }
    
    result = await graph.ainvoke(
        {"topic": topic},
        config=config
    )
    
    # 保存报告
    with open("literature_review.md", "w") as f:
        f.write(result["final_summary"])
    
    # 打印引用的来源
    print("参考来源:")
    for source in result.get("sources", []):
        print(f"- {source}")
    
    return result

# 运行
result = asyncio.run(research_paper_prep())
```

### 市场调研报告

```python
def market_research(product_category: str):
    """生成市场调研报告"""
    
    topic = f"{product_category} 市场规模、主要竞争者和发展趋势 2024"
    
    config = {
        "llm_provider": "ollama",
        "local_llm": "qwen:14b",
        "search_api": "tavily",  # 使用 Tavily 获得更商业化的结果
        "tavily_api_key": "tvly-xxx",
        "max_web_research_loops": 4,
        "fetch_full_page": True
    }
    
    result = graph.invoke(
        {"topic": topic},
        config=config
    )
    
    return result["final_summary"]

# 生成报告
report = market_research("新能源汽车")
print(report)
```

### 技术趋势追踪

```bash
# 使用命令行快速研究
cd local-deep-researcher
source .venv/bin/activate

# 创建研究脚本
python -c "
from ollama_deep_researcher.graph import graph

result = graph.invoke(
    {'topic': 'Rust 语言在系统编程领域的最新发展'},
    config={
        'llm_provider': 'ollama',
        'local_llm': 'llama3.2',
        'search_api': 'duckduckgo',
        'max_web_research_loops': 3
    }
)

print(result['final_summary'])
"
```

## Docker 部署

```bash
# 构建镜像
docker build -t local-researcher .

# 运行容器
docker run --rm -it -p 2024:2024 \
  -e SEARCH_API=tavily \
  -e TAVILY_API_KEY=tvly-xxx \
  -e LLM_PROVIDER=ollama \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434/ \
  -e LOCAL_LLM=llama3.2 \
  local-researcher
```

**注意**：Ollama 需要在宿主机单独运行，容器通过 `host.docker.internal` 访问。

## 模型兼容性说明

| 模型 | JSON 模式支持 | 备注 |
|------|--------------|------|
| llama3.2 | ✅ | 推荐，轻量快速 |
| deepseek-r1:8b | ✅ | 推理能力强 |
| qwen:14b | ✅ | 中文表现好 |
| gpt-oss | ⚠️ | 需要启用 tool calling |

**gpt-oss 模型特殊配置**：
```bash
# gpt-oss 不支持 JSON 模式，需要启用 tool calling
USE_TOOL_CALLING=true
```

## 故障排查

### Ollama 连接问题

```bash
# 检查 Ollama 服务状态
curl http://localhost:11434/api/tags

# 确保模型已下载
ollama list

# 测试模型
ollama run llama3.2 "Hello"
```

### 搜索结果为空

- 检查网络连接
- 尝试更换搜索 API
- 调整搜索查询语言

### 生成质量不佳

- 使用更大的模型（如 14B 参数以上）
- 增加 `MAX_WEB_RESEARCH_LOOPS`
- 启用 `FETCH_FULL_PAGE` 获取更完整内容

## 隐私与安全

- ✅ 所有数据留在本地
- ✅ 无需联网到 OpenAI/Claude
- ✅ 搜索查询不关联个人身份
- ✅ 适合处理敏感商业/研究数据

## 高级用法

### 自定义研究流程

```python
from langgraph.graph import StateGraph
from ollama_deep_researcher.configuration import Configuration
from ollama_deep_researcher import research_node, reflect_node

# 创建自定义流程
builder = StateGraph(ResearchState)
builder.add_node("research", research_node)
builder.add_node("reflect", reflect_node)
# ... 添加更多节点

# 编译并运行
graph = builder.compile()
```

### 集成到其他应用

```python
# FastAPI 示例
from fastapi import FastAPI
from ollama_deep_researcher.graph import graph

app = FastAPI()

@app.post("/research")
async def create_research(topic: str):
    result = await graph.ainvoke(
        {"topic": topic},
        config={"max_web_research_loops": 3}
    )
    return {
        "topic": topic,
        "report": result["final_summary"],
        "sources": result.get("sources", [])
    }
```

## 相关资源

- [LangChain Academy - 部署教程](https://academy.langchain.com/)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [Ollama 模型库](https://ollama.com/library)

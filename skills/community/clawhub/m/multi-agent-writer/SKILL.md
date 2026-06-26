---
name: multi-agent
version: 1.1.0
description: Use when requests involve writing articles, generating news, fetching hotspots, or producing content for social media (WeChat, Xiaohongshu, etc.). Triggers include "写文章", "生成新闻", "热点文章", "AI新闻", "写推文", "公众号", "小红书", "内容创作", or any article/content generation task.
location: user
allowed-tools: Bash, Read
---

# Multi-Agent Writer

三阶段多智能体写作流水线：
1. **热点抓取** — DuckDuckGo 搜索近7天实时新闻，LLM 筛选推荐选题
2. **文章撰写** — WriterAgent 生成微信公众号风格文章（含3组备选标题）
3. **审校循环** — ReviewerAgent 按5维度打分，低于通过线则自动触发修改，最多 N 轮

项目已安装至：`<INSTALL_DIR>`

---

## 快速调用

### Demo 模式（无需 API Key，约1秒完成）

```bash
cd <INSTALL_DIR>
python main.py --demo
python main.py --demo --topic "量子计算" --words 800
```

### 生产模式（需要 `.env` 配置 LLM API Key）

```bash
cd <INSTALL_DIR>
python main.py --topic "AI" --words 1000 --pass-threshold 85
```

---

## 全部 CLI 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--topic` | str | `"AI"` | 关注的领域/话题 |
| `--count` | int | `5` | 抓取热点数量 |
| `--style` | str | `"深度分析"` | 文章写作风格 |
| `--words` | int | `1000` | 目标字数 |
| `--max-revisions` | int | `2` | 最大审校-修改轮次 |
| `--pass-threshold` | int | `85` | 审校通过最低分（1-100） |
| `--output` | str | `"output.json"` | 输出文件路径 |
| `--demo` | flag | `False` | 使用 Mock LLM，无需 API |

---

## 输出文件

| 文件 | 格式 | 内容 |
|------|------|------|
| `output.json` | JSON | 完整结果：热点、文章、审校历史、耗时 |
| `output.md` | Markdown | 可直接复制的文章正文 |
| `experiments.tsv` | TSV | 追加实验记录（分数、状态、通过线等） |

---

## Python 程序化调用

```python
import sys
sys.path.insert(0, "<INSTALL_DIR>")

from orchestrator import Orchestrator
from base_agent import LLMClient
from config import ReviewConfig, LLMConfig
from search import DuckDuckGoSearchClient

llm_config = LLMConfig.from_env()
llm = LLMClient(
    api_key=llm_config.api_key,
    base_url=llm_config.base_url,
    model=llm_config.model,
    api_style=llm_config.api_style,
)

orchestrator = Orchestrator(
    llm=llm,
    max_revisions=2,
    review_config=ReviewConfig(pass_threshold=85),
    search_client=DuckDuckGoSearchClient(),
)

result = orchestrator.run(
    topic="AI",
    hotspot_count=5,
    article_style="深度分析",
    article_word_count=1000,
)

print(result.final_article["title"])
print(result.final_article["content"])
```

---

## 审校维度（5维，共100分）

| 维度 | 权重 | 说明 |
|------|------|------|
| 内容洞察力 | 30分 | 新颖观点、信息价值 |
| 可读性 | 25分 | 短段落、移动端友好 |
| 标题吸引力 | 20分 | 点击率、情绪共鸣 |
| 结构流畅性 | 15分 | 开篇钩子、逻辑递进 |
| 准确性 | 10分 | 事实正确 |

---

## 环境配置（`.env` 文件）

```bash
LLM_API_KEY=your-api-key
LLM_BASE_URL=https://api.moonshot.cn/v1  # 可选
LLM_MODEL=moonshot-v1-8k                 # 可选
LLM_API_STYLE=openai                     # openai 或 anthropic
```

支持：Kimi、DeepSeek、OpenAI、Claude、Qwen、GLM、Ollama 等兼容 OpenAI/Anthropic API 的模型。

---

## 常见场景

```bash
# 生成科技领域热点文章
python main.py --topic "AI大模型" --words 1500 --style "深度分析"

# 严格评分 A/B 测试
python main.py --demo --pass-threshold 90 --description "strict_90"
python main.py --demo --pass-threshold 75 --description "loose_75"

# 运行测试（验证系统完整性）
cd <INSTALL_DIR> && pytest
```

---

## 关键文件

```
<INSTALL_DIR>/
├── main.py           # CLI 入口
├── orchestrator.py   # 工作流协调器
├── agents.py         # 3个业务智能体
├── base_agent.py     # LLMClient、BaseAgent 框架
├── config.py         # 配置类
├── search.py         # DuckDuckGo 搜索封装
└── tests/
```

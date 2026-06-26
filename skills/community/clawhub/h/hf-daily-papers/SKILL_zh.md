---
name: hf-daily-papers
description: "抓取并整理 HuggingFace Daily Papers。触发条件：用户说「今日论文」「论文精选」「HF daily papers」「huggingface papers」「daily paper」等。调用 HF API 获取数据，读取结果，评分后生成带点评的格式化 digest。"
---

# HF Daily Papers

从 HuggingFace Daily Papers 频道抓取论文并整理成分析报告。

## 前置准备：申请 HF Token

1. 打开 **https://huggingface.co/settings/tokens**
2. 创建一个 Read 类型 token（随便起名）
3. 设置环境变量：

```powershell
# Windows PowerShell
$env:HF_TOKEN = "hf_xxxxxxxxxxxxx"

# macOS / Linux / Git Bash
export HF_TOKEN="hf_xxxxxxxxxxxxx"
```

> 脚本从 `os.environ` 读取 `HF_TOKEN`，未设置时会报明确的错误并给出申请地址。

## 第一步：运行抓取脚本

```bash
cd <skill-path>/scripts && python hf_papers.py [日期YYYY-MM-DD]
```

- 不传日期参数：默认抓昨天
- 输出文件：`hf_results.json`（保存在运行目录下）

## 第二步：读取结果

读取 `hf_results.json`，包含字段：

| 字段 | 说明 |
|------|------|
| `paperId` | arXiv ID |
| `title` | 论文标题 |
| `votes` | 社区点赞数 |
| `submittedBy` | 提交者 |
| `organization` | 研究机构 |
| `summary` | 完整摘要（清洗后，最多2000字） |
| `aiSummary` | AI 生成摘要（200-300字，来自 HF 蓝色高亮框） |
| `githubRepo` | GitHub 链接（如果有） |
| `keywords` | AI 提取的关键词（最多10个） |
| `link` | HF 论文页 |
| `arxivLink` | arXiv 摘要页 |

## 第三步：评分并整理

评分参考（10分制，凭直觉 + 内容判断，不需要脚本）：

| 维度 | 权重 | 加分项 |
|------|------|--------|
| 创新性 | 0-3 | 新 benchmark/数据集、原创方向、首次提出 |
| 实用性 | 0-3 | 有 GitHub 代码、落地场景清晰、大厂/学术界应用 |
| 技术深度 | 0-2 | 摘要长度 >200字、含 RL/MCTS/进化算法等硬核方法 |
| 有趣程度 | 0-2 | 话题性强/反直觉/跨学科/值得深思 |

**票数高（>10）是加分项**，反映社区热度。

## 第四步：输出格式

```
📄 HF Daily Papers · [日期]  共N篇

## 🔴 必看（8-10分）
[标题 | ID | 机构
 小龙虾点评：...]
## 🟡 值得关注（6-7分）
[精简列表 + 一句话评价]
## 🟢 值得一看（按需）
[极简列表]

## 🦞 今日总结
Top 3 + 今日主线观察
```

点评要求：
- 每篇必看论文要有「小龙虾点评」，用自己的话解释论文核心洞察
- 说清楚这篇好在哪儿、值得看的原因
- 可以联系其他论文或行业趋势
- 语气随意幽默，像朋友聊天
- 极简列表每篇不超过一句话

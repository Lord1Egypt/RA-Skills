# PoliBERT Sentiment Analysis Skill

基于 **PoliBERTweet** 的政治情绪分析技能，专门用于分析政治人物和事件的社交媒体情绪。

## 模型

- **PoliBERTweet**: RoBERTa架构，训练于8300万条政治推文
- **来源**: Georgetown University, LREC 2022
- **HuggingFace**: `kornosk/polibertweet-political-twitter-roberta-mlm`

## 安装

```bash
# 基础依赖
pip install transformers torch

# Reddit数据抓取 (可选)
pip install praw
```

## 使用方法

### 1. 分析单条文本
```bash
python polibert_sentiment.py --text "J.D. Vance is the future of GOP"
```

### 2. 从 Reddit 抓取分析
```bash
# 分析万斯的Reddit情绪
python polibert_sentiment.py --candidate "J.D. Vance" --reddit --limit 50

# 自定义Subreddit
python polibert_sentiment.py --query "2028 election" --reddit --subreddits politics,Conservative --limit 100
```

### 3. 本地文件分析
```bash
python polibert_sentiment.py --candidate "Trump" --file tweets.txt
```

### 4. JSON 输出
```bash
python polibert_sentiment.py --candidate "Biden" --reddit --json
```

## 数据来源

| 来源 | 方式 | 备注 |
|------|------|------|
| **Reddit** | `--reddit` | 免费，实时，政治讨论活跃 |
| **本地文件** | `--file` | 批量分析自有数据 |
| **标准输入** | `--stdin` | 管道输入 |
| **单条文本** | `--text` | 快速测试 |

## Reddit 数据源

**默认抓取**: r/politics, r/Conservative, r/democrats, r/Republican, r/PoliticalDiscussion

**特点**:
- ✅ 免费，无需 API Key (read-only模式)
- ✅ 实时政治讨论
- ✅ 可以搜索特定候选人/议题
- ⚠️ 有速率限制 (建议 limit < 200)

## 输出示例

```
🔍 Fetching Reddit posts for: J.D. Vance
📥 Fetched 43 posts/comments

📊 Sentiment Analysis: J.D. Vance
Source: Reddit | Total analyzed: 43

Support: 37.2% (16)
Oppose: 44.2% (19)
Neutral: 18.6% (8)

Net Sentiment: -7.0%
Avg Confidence: 78.4%
```

## 三技能协作

```
polibert-sentiment  → Reddit 情绪分析
       ↓
polymarket-unified  → 预测市场赔率
       ↓
prediction            → BRACE综合预测
```

## 引用

```bibtex
@inproceedings{kawintiranon2022polibertweet,
  title={{P}oli{BERT}weet: A Pre-trained Language Model for Analyzing Political Content on {T}witter},
  author={Kawintiranon, Kornraphop and Singh, Lisa},
  booktitle={Proceedings of LREC 2022},
  pages={7360--7367}
}
```

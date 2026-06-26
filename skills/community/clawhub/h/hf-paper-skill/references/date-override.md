# 指定日期获取论文（覆盖默认日期）

`get_papers.py` 和 `generate_report.py` 默认只支持 `daily`（今天）、`weekly`、`monthly` 三种周期。
如果需要获取**特定日期**（如昨天、上周某天）的论文，可按以下方式覆盖。

## 方法：Monkey-patch 日期函数

```python
from get_papers import get_papers, format_markdown
from datetime import datetime, timedelta
import get_papers as gp

# 设置目标日期
target = datetime.now() - timedelta(days=1)  # 昨天
date_str = target.strftime('%Y-%m-%d')

# 覆盖日期函数
orig = gp.get_hf_papers_url
def patched_url(period):
    if period == "daily":
        return f"https://huggingface.co/papers/date/{date_str}"
    return orig(period)
gp.get_hf_papers_url = patched_url

# 获取并格式化
papers = get_papers("daily", 10)
print(format_markdown(papers, "daily"))
```

## 用于完整报告（含翻译）

```python
import sys
sys.path.insert(0, 'scripts')

from get_papers import get_papers
from generate_report import format_report
from datetime import datetime, timedelta
import get_papers as gp

target = datetime.now() - timedelta(days=1)
date_str = target.strftime('%Y-%m-%d')

# Monkey-patch
orig = gp.get_hf_papers_url
def patched_url(period):
    if period == "daily":
        return f"https://huggingface.co/papers/date/{date_str}"
    return orig(period)
gp.get_hf_papers_url = patched_url

papers = get_papers("daily", 10)
report = format_report(papers, "daily")

with open(f"reports/HuggingFace_昨日热门论文_{date_str}.md", "w", encoding="utf-8") as f:
    f.write(report)
```

## 手动修正标题

`format_report("daily")` 输出标题为"今日热门"，如需改为"昨日热门"，保存后替换：

```bash
sed -i '' 's/今日/昨日/' reports/HuggingFace_昨日热门论文_*.md
```

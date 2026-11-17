# 详细参考 - news-sentiment-tool-pro

> 本文件从SKILL.md拆分而来，包含详细代码示例和扩展章节。

## 代码示例 (python)

```python
#!/usr/bin/env python3
"""企业舆情监控自动化工作流"""
import subprocess
import json
from datetime import datetime

class SentimentAutomation:
    def __init__(self, script_path):
        self.script = script_path

    def scan_single(self, code, days=7, market='auto'):
        """单股扫描"""
        result = subprocess.run(
            ['python3', self.script, code, str(days), market, '--format', 'json'],
            capture_output=True, text=True
        )
        return json.loads(result.stdout) if result.stdout else {}

    def scan_batch(self, csv_file, days=7, output_format='json'):
        """批量扫描"""
        output_file = f'report_{datetime.now().strftime("%Y%m%d")}.{output_format}'
        subprocess.run([
            'python3', self.script, '--batch', csv_file, str(days),
            '--format', output_format, '--output', output_file
        ])
        return output_file

    def compare_trend(self, csv_file, days=7):
        """趋势对比分析"""
        result = subprocess.run(
            ['python3', self.script, '--batch', csv_file, str(days), '--compare', '--format', 'json'],
            capture_output=True, text=True
        )
        return json.loads(result.stdout) if result.stdout else {}

    def check_alerts(self, results, neg_threshold=-5, pos_threshold=7):
        """检查预警"""
        alerts = []
        for r in results:
            score = r.get('sentiment_score', 0)
            if score <= neg_threshold:
                alerts.append({
                    'code': r['code'],
                    'name': r['name'],
                    'score': score,
                    'type': 'negative',
                    'message': f"{r['name']} 情绪分数 {score},低于阈值 {neg_threshold}"
                })
            elif score >= pos_threshold:
                alerts.append({
                    'code': r['code'],
                    'name': r['name'],
                    'score': score,
                    'type': 'positive',
                    'message': f"{r['name']} 情绪分数 {score},高于阈值 {pos_threshold}"
                })
        return alerts

automation = SentimentAutomation('{SKILL_DIR}/scripts/sentiment_scan.py')

report_file = automation.scan_batch('portfolio.csv', days=7)

with open(report_file) as f:
    report = json.load(f)
alerts = automation.check_alerts(report['results'])

if alerts:
    print("发现预警:")
    for alert in alerts:
        print(f"  [{alert['type']}] {alert['message']}")
else:
    print("无预警,组合情绪正常。")
```

## 代码示例 (json)

```json
{
  "scan_time": "2026-07-18T10:30:00Z",
  "period_days": 7,
  "total_stocks": 5,
  "results": [
    {
      "code": "002594",
      "name": "比亚迪",
      "sentiment_score": 5.2,
      "sentiment_label": "偏正面",
      "positive_events": 3,
      "negative_events": 1,
      "top_event": "6月销量同比增长35%"
    },
    {
      "code": "600519",
      "name": "贵州茅台",
      "sentiment_score": 2.1,
      "sentiment_label": "轻微正面",
      "positive_events": 2,
      "negative_events": 2,
      "top_event": "中秋备货期启动"
    }
  ],
  "portfolio_summary": {
    "average_score": 3.8,
    "positive_count": 4,
    "neutral_count": 1,
    "negative_count": 0
  }
}
```

## 代码示例 (bash)

```bash
cat > weights.json << 'EOF'
{
  "sources": {
    "company_announcement": 1.0,
    "broker_report": 0.9,
    "mainstream_media": 0.8,
    "regulatory_filing": 0.9,
    "social_media": 0.6,
    "forum_post": 0.5
  },
  "event_types": {
    "earnings_beat": 5,
    "rating_upgrade": 3,
    "insider_buying": 3,
    "policy_positive": 4,
    "product_launch": 2,
    "earnings_miss": -4,
    "rating_downgrade": -3,
    "insider_selling": -3,
    "policy_negative": -4,
    "regulatory_investigation": -5
  }
}
EOF

python3 {SKILL_DIR}/scripts/sentiment_scan.py 002594 7 --weights weights.json
```


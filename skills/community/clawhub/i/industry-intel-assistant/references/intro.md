# 行业情报助手 — 快速上手指南

## 安装依赖

```bash
pip install tavily-python --break-system-packages
```

## 配置 Tavily API Key

1. 访问 https://tavily.com 注册并获取 API Key
2. 配置到 OpenClaw：
   ```bash
   openclaw config set skills.entries.tavily.apiKey "tvly-xxx"
   ```

## 快速测试

```bash
# 测试搜索
python3 skills/industry-intel-assistant/scripts/tavily_industry_search.py "AI大模型 最新动态" --max-results 5

# 生成简报
python3 skills/industry-intel-assistant/scripts/generate_intel_report.py \
  --query "AI大模型 GPT Claude Gemini 最新进展" \
  --max-results 8 \
  --output ./assets/demo_report.md

# 创建每日定时推送（每天早上9点）
python3 skills/industry-intel-assistant/scripts/schedule_intel.py \
  --query "AI大模型 最新动态 2026" \
  --schedule "0 9 * * *" \
  --channel wecom
```

## 推荐搜索关键词组合

### AI/科技行业
```
AI大模型 最新进展
GPT Claude Gemini 最新动态
生成式AI 应用案例
AIGC 行业动态 2026
```

### 电商行业
```
跨境电商 政策 动态 2026
亚马逊 Shopee 平台新闻
电商选品 热门品类
```

### 竞品追踪
```
[竞品名称] 最新消息
[竞品名称] 融资 动态
[竞品名称] 产品 更新
```

## 支持的推送渠道

| 渠道 | 配置要求 |
|------|---------|
| 企业微信 | OpenClaw wecom 插件已启用 |
| 飞书 | OpenClaw feishu 插件已启用 |
| 钉钉 | OpenClaw ddingtalk 插件已启用 |

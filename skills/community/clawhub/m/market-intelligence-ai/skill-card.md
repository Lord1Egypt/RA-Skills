## Description: <br>
自动采集和分析电商竞品销量、价格与趋势数据，生成分级市场报告并支持价格变动监控与提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-gaoqian](https://clawhub.ai/user/ai-gaoqian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business owners, market teams, and ecommerce sellers use this skill to collect marketplace product data, compare competitors, and produce market snapshots or deeper monitoring reports. It is intended for market intelligence workflows that need sourced data, pricing tiers, and concise recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires marketplace and payment-related credentials, including Alipay and optional product data API keys. <br>
Mitigation: Install only after confirming which credentials are needed, provide them through environment variables, and avoid embedding secrets in prompts or files. <br>
Risk: Paid advanced and professional tiers can create payment, subscription, renewal, and cancellation ambiguity. <br>
Mitigation: Before use, confirm subscription terms, renewal behavior, cancellation path, monitoring duration, notification method, and retained payment or report data. <br>
Risk: Market reports based on third-party or fallback data can be stale, incomplete, or unsuitable for business decisions without review. <br>
Mitigation: Check the cited data source and collection time, treat fallback dataset results as non-real-time, and review recommendations before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-gaoqian/market-intelligence-ai) <br>
- [market_data_sources.md](artifact/references/market_data_sources.md) <br>
- [market_snapshot_sample.md](artifact/references/market_snapshot_sample.md) <br>
- [collector.py](artifact/references/collector.py) <br>
- [Alipay AI receipt integration guide](https://opendocs.alipay.com/open/ai-receipt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Plain text market snapshots, Markdown reports with tables, JSON product records, and alert or recommendation text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include source labels, collection timestamps, pricing tiers, paid-report gating, and monitoring alerts.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

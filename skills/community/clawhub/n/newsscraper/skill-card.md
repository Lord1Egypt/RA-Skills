## Description: <br>
This skill should be used when users need to scrape hot news topics from Chinese platforms (微博、知乎、B站、抖音、今日头条、腾讯新闻、澎湃新闻), generate summaries, and cite sources. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[13923870749](https://clawhub.ai/user/13923870749) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect public hot-topic items from supported Chinese news and social platforms, summarize them, and prepare cited JSON or Markdown reports. It is suited to public trend monitoring and research workflows where source attribution and rate-limited collection are required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Direct or proxy-assisted scraping can exceed site authorization, terms, or rate limits. <br>
Mitigation: Prefer official or aggregation APIs where available, keep collection low-volume, honor platform terms and robots guidance, and use explicit rate limits before deployment. <br>
Risk: The abstractive summarizer can download and run remote model artifacts, which may be inappropriate for sensitive or policy-controlled text. <br>
Mitigation: Use approved pinned or local models, avoid processing sensitive text unless policy allows it, and review model dependencies before installation. <br>
Risk: Collected public trend data and summaries may be incomplete, stale, duplicated, or misleading. <br>
Mitigation: Verify source links and timestamps before relying on the report, de-duplicate items, and treat generated summaries as drafts requiring review. <br>


## Reference(s): <br>
- [Platform scraping strategies](references/platforms.md) <br>
- [Summarization methods](references/summarization_methods.md) <br>
- [uapis.cn hotboard API](https://uapis.cn/api/get-misc-hotboard) <br>
- [jieba Chinese text segmentation](https://github.com/fxsjy/jieba) <br>
- [Hugging Face Transformers](https://github.com/huggingface/transformers) <br>
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON datasets, Markdown reports, and concise command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include news titles, source platform, rank or heat score, timestamp, summary, and original URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

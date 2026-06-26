## Description: <br>
Analyzes Hong Kong, A-share, and U.S. stocks by collecting market data, chart images, fundamentals, news, and capital-flow signals, then producing structured investment research reports with visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zai-org](https://clawhub.ai/user/zai-org) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to research listed equities across Hong Kong, Mainland China, and U.S. markets. It supports stock-code confirmation, market-data collection, chart review, precise news gathering, and generation of concise chat summaries plus detailed research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock analysis and investment conclusions can be incorrect, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Base conclusions on freshly fetched data and precise news searches, state missing data clearly, and preserve the required disclaimer that analysis is for reference only and not investment advice. <br>
Risk: The skill installs Python dependencies and contacts market-data services during setup and analysis. <br>
Mitigation: Run it in a normal project sandbox or virtual environment, review dependency installation, and provide only task-relevant credentials such as TUSHARE_TOKEN when needed. <br>
Risk: Generated HTML or PDF reports may expose local paths, downloaded data, or sensitive research context when shared. <br>
Mitigation: Review generated reports before distribution and avoid sharing generated HTML/PDF files when local path disclosure matters. <br>
Risk: Investor-relations PDF retrieval processes external files. <br>
Mitigation: Use the documented HTTPS-only PDF retrieval path with file-size and page-count limits, and skip untrusted or unnecessary files. <br>


## Reference(s): <br>
- [GLM-V-Stock-Analyst on ClawHub](https://clawhub.ai/zai-org/glmv-stock-analyst) <br>
- [Hong Kong Stock Knowledge](references/hk_stock_knowledge.md) <br>
- [Report Template](references/report_template.md) <br>
- [Sensitive Companies](references/sensitive_companies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, chat summaries, shell commands, JSON data files, chart images, HTML reports, and optional PDF exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes per-analysis files under stock_data_output/<code>_<timestamp>/ and may open generated local report HTML.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

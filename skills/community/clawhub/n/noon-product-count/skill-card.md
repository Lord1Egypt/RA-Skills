## Description: <br>
Noon 商品数量统计工具。输入阿拉伯语关键词，在 noon.com 沙特站搜索，返回搜索结果的商品数量。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freemanwangfuhan-coder](https://clawhub.ai/user/freemanwangfuhan-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search Noon Saudi Arabia with Arabic keywords and report the total number of matching products. It supports single-keyword and batch keyword checks through a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports automated scraping with CAPTCHA, anti-bot, and geofencing avoidance behavior. <br>
Mitigation: Install only when authorized to collect this Noon data and when the use complies with site terms, law, and organizational policy. <br>
Risk: Automated browser access may trigger account, IP, or service blocking. <br>
Mitigation: Run a small test first and avoid bulk scraping, evading access controls, or high-volume collection. <br>
Risk: The skill depends on browser automation packages and opens Chrome for live website access. <br>
Mitigation: Review and pin Node dependencies before use, and run in a clean browser environment without sensitive active sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freemanwangfuhan-coder/noon-product-count) <br>
- [Noon Saudi Arabia](https://www.noon.com/saudi-ar/) <br>
- [Noon Saudi Arabia search endpoint](https://www.noon.com/saudi-ar/search/?q=) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text count summaries printed to the terminal] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns one product-count line per input keyword, or an error string when browser automation fails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

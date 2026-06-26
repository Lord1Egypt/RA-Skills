## Description: <br>
Search and scrape Indeed job listings and company information using Bright Data's Web Scraper API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foreztgump](https://clawhub.ai/user/foreztgump) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, recruiting teams, and developers use this skill to search Indeed jobs, collect job details from Indeed URLs, look up company information, and format results for recruiting research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A modified local history file could cause cleanup to delete an arbitrary file accessible to the user account. <br>
Mitigation: Review the skill before installation and prefer a version that constrains cleanup deletions to the managed results directory. <br>
Risk: Indeed search inputs and URLs are sent to Bright Data, and local cache, pending job, history, and result files are stored under ~/.config/indeed-brightdata/. <br>
Mitigation: Use a scoped Bright Data API key where possible and avoid submitting sensitive search terms or URLs unless sharing them with Bright Data is acceptable. <br>


## Reference(s): <br>
- [Bright Data Indeed API Reference](references/api-reference.md) <br>
- [Keyword Expansions](references/keyword-expansions.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/foreztgump/indeed-brightdata) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain-text summaries, shell command examples, JSON result data, and optional CSV exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BRIGHTDATA_API_KEY, curl, and jq; persistent cache, pending jobs, history, and results are stored under ~/.config/indeed-brightdata/.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

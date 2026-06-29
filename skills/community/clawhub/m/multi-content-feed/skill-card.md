## Description: <br>
Scans cross-platform content globalization trends, selects high-engagement works, clusters them by topic, and generates a visual HTML daily report with a Markdown summary for creators and operators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content globalization creators, operations teams, MCNs, planners, and data analysts use this skill to query RedFoxHub data, monitor trending works across major Chinese content platforms, and produce topic and platform trend reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends an API key and query terms to RedFoxHub. <br>
Mitigation: Use a scoped and revocable REDFOX_API_KEY only with a trusted RedFoxHub account, and avoid exposing the key in prompts, logs, or terminal output. <br>
Risk: Generated HTML is built from external content data and is opened automatically in a local browser. <br>
Mitigation: Review or sanitize report fields before regular use, and disable browser auto-open if the execution environment handles untrusted HTML cautiously. <br>
Risk: Reports and cached query results may persist as local files. <br>
Mitigation: Store outputs in an approved local directory and delete generated reports or cache files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/multi-content-feed) <br>
- [RedFoxHub](https://redfox.hk/) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?souce=github) <br>
- [Core workflow](references/core_workflow.md) <br>
- [Usage examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, HTML files, Shell commands, Guidance] <br>
**Output Format:** [Markdown terminal summary plus a local HTML daily report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; may write local JSON cache and HTML report files and open the generated HTML in a browser.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

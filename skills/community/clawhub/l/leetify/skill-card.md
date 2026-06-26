## Description: <br>
Get CS2 player statistics, match analysis, and gameplay insights from Leetify API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Damirikys](https://clawhub.ai/user/Damirikys) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External players, coaches, and developers use this skill to fetch CS2 player statistics, compare Leetify profiles, inspect match details, and generate demo-analysis logs for gameplay review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Leetify API key. <br>
Mitigation: Provide LEETIFY_API_KEY only in trusted environments and avoid exposing it in shared shells, logs, or screenshots. <br>
Risk: The skill can store player mappings and cached match logs locally. <br>
Mitigation: Save only the identifiers needed for analysis and delete local mappings or cached logs when they are no longer useful. <br>
Risk: Demo analysis can download and parse large CS2 demo files. <br>
Mitigation: Run demo parsing on a trusted machine with adequate memory and storage, and review downloaded artifacts before retaining or sharing them. <br>


## Reference(s): <br>
- [Leetify Public API Documentation](https://api-public-docs.cs-prod.leetify.com/) <br>
- [Leetify Public API Endpoint](https://api-public.cs-prod.leetify.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/Damirikys/leetify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON payloads, plain-text demo logs, and shell command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LEETIFY_API_KEY and may create local Steam ID mappings and cached match logs.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

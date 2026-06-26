## Description: <br>
Queries ITjuzi venture-capital telegraph updates for today's events, recent investment activity, keyword-filtered event streams, and sector event flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skyentq-alt](https://clawhub.ai/user/skyentq-alt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve and summarize ITjuzi venture-capital bulletin items, including today's free summaries and member-only historical, keyword, event-type, pagination, and structured-detail views. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional ITjuzi member tokens can be saved locally for reuse. <br>
Mitigation: Prefer the ITJUZI_SKILL_TOKEN environment variable for temporary use, or remove the saved token when member access is no longer needed. <br>
Risk: The token status command can expose a token prefix and token source in logs or transcripts. <br>
Mitigation: Avoid running token status in shared logs or transcripts and treat status output as sensitive operational information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skyentq-alt/itjuzitelegram) <br>
- [ITjuzi telegraph API endpoint](https://www.itjuzi.com/api/telegraph/get_list) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown prose summarizing JSON API responses, with shell commands for API calls and token management.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl to call the ITjuzi telegraph API and may use ITJUZI_SKILL_TOKEN or a saved local token for member access.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog report 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

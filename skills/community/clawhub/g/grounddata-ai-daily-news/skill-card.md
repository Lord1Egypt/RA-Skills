## Description: <br>
Fetches global AI news data, synchronizes platform capabilities, and invokes remote AI-news analysis for briefings, preferences, automation guidance, and workflow artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finleyfu](https://clawhub.ai/user/finleyfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, developers, product teams, and strategists use this skill to retrieve current AI and machine-learning news, personalize coverage, generate briefings, and prepare workflow-specific artifacts such as tech radars, knowledge-base notes, product scans, and strategy briefs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a remote AI-news service and can use an optional access token. <br>
Mitigation: Install only when remote API access is acceptable, keep AINEWS_ACCESS_TOKEN private, and avoid untrusted AINEWS_SERVICE_URL overrides. <br>
Risk: The skill stores local preferences, delivery state, and identifiers to support personalization, surveys, notices, and scheduled-news continuation. <br>
Mitigation: Review local cache and state behavior before deployment in sensitive environments and clear stored state when personalization or engagement tracking is not desired. <br>
Risk: The skill can submit user-provided feedback or survey text to the remote service. <br>
Mitigation: Submit feedback or survey responses only when the user intentionally provides that content and is comfortable sending it to the service. <br>
Risk: Scheduled delivery plans can send AI-news output to external channels. <br>
Mitigation: Review the generated scheduled-delivery plan and run a test before approving recurring delivery. <br>


## Reference(s): <br>
- [AI Daily News ClawHub listing](https://clawhub.ai/finleyfu/grounddata-ai-daily-news) <br>
- [Automation Prompt Template](references/automation-prompt.md) <br>
- [AI Daily News API](https://api.ainewparadigm.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses, with JSON-backed data fetched by local Python tools and shell commands for automation setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include freshness metadata, local preference context, survey content, sponsor notices, update notices, and handoff context depending on the request and service response.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
OmniSearch routes agent web-search requests for current information to configured search providers and guides agents to summarize findings with citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bguidolim](https://clawhub.ai/user/bguidolim) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use OmniSearch to let OpenClaw agents retrieve current web information, compare recent facts, and cite sources when static model knowledge is insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may be sent to external providers automatically. <br>
Mitigation: Avoid including secrets, confidential business data, private identifiers, or sensitive personal details in search queries unless the configured provider and mcporter setup are trusted. <br>


## Reference(s): <br>
- [ClawHub OmniSearch release page](https://clawhub.ai/bguidolim/omnisearch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with source links and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may depend on the configured provider and current web availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Run an LDM inbox placement and deliverability preflight before OpenClaw agents send outbound email campaigns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[live-direct-marketing](https://clawhub.ai/user/live-direct-marketing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to run deliverability preflights before bulk outbound email campaigns, then pause or revise campaigns when inbox placement, authentication, content, or compliance checks are risky. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send campaign subjects, message bodies, sender details, and links to the LDM service for analysis. <br>
Mitigation: Use it only for intended outbound deliverability checks, configure the API key deliberately, and avoid submitting content that should not be shared with the LDM service. <br>
Risk: The skill relies on an API key for authenticated checks. <br>
Mitigation: Store the API key in the configured environment variable and do not expose it in logs, chat output, pull requests, or generated files. <br>
Risk: A failed deliverability preflight indicates that outbound email may land in spam, promotions, or junk folders. <br>
Mitigation: Pause bulk sending when checks fail, apply the reported fixes, and rerun the preflight before sending. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/live-direct-marketing/ldm-openclaw-skill) <br>
- [LDM OpenClaw Skill homepage](https://github.com/live-direct-marketing/ldm-openclaw-skill) <br>
- [LDM Inbox Placement Test](https://check.live-direct-marketing.online) <br>
- [LDM Developer API](https://developers.live-direct-marketing.online) <br>
- [Live Direct Marketing](https://live-direct-marketing.online) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown/text guidance with optional shell command snippets and structured deliverability result summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PASS/FAIL status, inbox placement percentage, provider issues, authentication results, content risks, recommended fixes, and a send/revise/pause decision.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

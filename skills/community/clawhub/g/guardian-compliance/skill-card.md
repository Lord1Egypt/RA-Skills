## Description: <br>
Immigration, tax, and business compliance alerts for Guardian users, including STEM OPT, H-1B, I-140, CPT status, upcoming deadlines, risk findings, documents, and tax filing obligations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lee-chenyu](https://clawhub.ai/user/lee-chenyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Guardian users use this skill to review their immigration, tax, and business compliance status, deadlines, findings, documents, and account-aware answers in an agent conversation. The skill is intended to summarize Guardian results and remind users that compliance risk detection is not legal, immigration, or tax advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses sensitive immigration, tax, business compliance, and document metadata through Guardian. <br>
Mitigation: Use it only with a trusted Guardian account and request results only when sharing that account context with the agent is acceptable. <br>
Risk: GUARDIAN_TOKEN authorizes access to the user's Guardian data. <br>
Mitigation: Keep GUARDIAN_TOKEN private and configure it only through the agent environment or approved secret settings. <br>
Risk: GUARDIAN_API_URL can redirect requests to an alternate endpoint. <br>
Mitigation: Leave GUARDIAN_API_URL unset unless the alternate endpoint is trusted. <br>
Risk: Compliance summaries can affect immigration, legal, or tax decisions. <br>
Mitigation: Treat Guardian output as compliance risk detection, not legal or tax advice, and consult an immigration attorney or qualified CPA for critical issues. <br>


## Reference(s): <br>
- [Guardian Compliance homepage](https://guardian-compliance.fly.dev) <br>
- [ClawHub skill page](https://clawhub.ai/lee-chenyu/guardian-compliance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text summaries from Guardian API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GUARDIAN_TOKEN and the curl and jq command-line tools; GUARDIAN_API_URL is optional and defaults to the Guardian hosted endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

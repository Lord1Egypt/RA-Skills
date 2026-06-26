## Description: <br>
Subscription Tracker helps an agent identify recurring charges from user-provided bank or credit card statements, track renewals and trials, flag duplicates and price increases, and provide cancellation guidance without bank linking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and their agents use this skill to analyze uploaded CSV or PDF financial statements, maintain a local subscription database, receive renewal and free-trial alerts, export subscription reports, and get instructions for cancelling unwanted subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive bank and credit card statement data and stores derived subscription data, possible statement archives, exports, and logs locally. <br>
Mitigation: Use statements with the minimum needed date range, redact unnecessary identifiers where practical, restrict access to the local tracker directory, review exports before sharing, and delete ~/.normieclaw/subscription-tracker when no longer using the skill. <br>
Risk: Statement contents may be processed by the user's AI model provider during agent interactions. <br>
Mitigation: Review the model provider's data handling terms before uploading statements and avoid providing data beyond what is needed for subscription detection. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nollio/normieclaw-subscription-tracker) <br>
- [Publisher Profile](https://clawhub.ai/user/nollio) <br>
- [README](artifact/README.md) <br>
- [Security and Data Handling](artifact/SECURITY.md) <br>
- [Dashboard Specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text guidance with optional JSON, CSV, and Markdown report exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local subscription data, statement archives, exports, logs, setup files, and renewal-check output under ~/.normieclaw/subscription-tracker.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

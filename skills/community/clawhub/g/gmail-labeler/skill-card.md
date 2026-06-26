## Description: <br>
Gmail inbox triage, labeling, and safe archiving with gog plus a configurable lightweight LLM review layer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felipematos](https://clawhub.ai/user/felipematos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to automate Gmail inbox triage by classifying messages, applying labels, archiving low-value mail, and keeping actionable replies, opportunities, and urgent billing items in the Inbox. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The automation can alter Gmail mailbox state by applying labels and removing messages from the Inbox. <br>
Mitigation: Start in dry-run mode, review proposed actions and logs, and only enable label-only or full modes after validating the configuration. <br>
Risk: LLM review can send email excerpts to the configured model tooling. <br>
Mitigation: Disable llmReview.enabled unless that data flow is acceptable, and keep model, provider, and prompt settings under local review. <br>
Risk: The launcher includes a hard-coded Doppler production secret flow. <br>
Mitigation: Replace the launcher secret retrieval with a local, scoped credential setup before installing or scheduling the skill. <br>
Risk: Local JSONL logs can persist sensitive email metadata. <br>
Mitigation: Store logs in a protected location, reduce logged fields where appropriate, and keep retention short before enabling mailbox-changing modes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/felipematos/gmail-labeler) <br>
- [Default configuration](references/default-config.json) <br>
- [Configuration guide](references/config-guide.md) <br>
- [Filter catalog](references/filter-catalog.md) <br>
- [Implementation notes](references/implementation-notes.md) <br>
- [Logging and review](references/logging-and-review.md) <br>
- [LLM review layer](references/llm-review.md) <br>
- [Cron example](references/cron-example.md) <br>
- [AIN email review schema](references/ain-email-review.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration, Python and shell runner files, and JSONL decision logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gog and python3; optional AIN CLI support is declared for lightweight structured review.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

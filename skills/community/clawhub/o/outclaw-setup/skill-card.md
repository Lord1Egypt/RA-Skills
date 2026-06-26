## Description: <br>
OutClaw Setup helps an agent inventory and connect outreach channels, capture user and organization profile context, and learn per-channel writing style for downstream OutClaw workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[milstan](https://clawhub.ai/user/milstan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to set up OutClaw outreach prerequisites: plugin inventory, account connections, local profile and organization context, style learning, and final setup verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow handles OAuth connections and sensitive outreach credentials. <br>
Mitigation: Approve only the channels needed, review OAuth scopes and third-party plugin publishers, and avoid sharing callback URLs in untrusted chats. <br>
Risk: The skill persists personal profile, company context, memory, style, and optional schedule entries for later outreach use. <br>
Mitigation: Review saved KB, memory, style, and cron entries after setup and remove anything that should not be reused. <br>
Risk: Generated outreach setup guidance may connect external communication tools that can affect future messages. <br>
Mitigation: Verify final channel status and keep human approval gates for outreach plans before contacting prospects. <br>


## Reference(s): <br>
- [Inventory Check](references/inventory-check.md) <br>
- [Plugin Connection Flows](references/plugin-connect.md) <br>
- [User Profile Capture](references/user-profile.md) <br>
- [OutClaw Homepage](https://github.com/leadbay/outclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and setup status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local knowledge-base pages, memory entries, style files, plugin authentication state, and optional cron configuration during execution.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter reports 2.1.33) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

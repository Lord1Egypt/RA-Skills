## Description: <br>
Investment Buddy Pet helps agents match users to investor-profile companion personas, provide investment education and reminders, and respond to market anxiety with compliance-oriented guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lj22503](https://clawhub.ai/user/lj22503) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill for investment personality matching, companion-style investing education, scheduled reminders, market-volatility reassurance, and compliance-aware refusal of product-specific investment requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security review flagged the release as suspicious because it combines persistent financial profiling, proactive messaging, market-data fetching, sync/share features, and advice-like outputs. <br>
Mitigation: Review before installation, keep outputs educational, and disable or remove sync, share/viral, profiling, and master-advice paths unless explicitly needed. <br>
Risk: The skill can persist user profile, holdings, interactions, and analysis results locally and can optionally synchronize data. <br>
Mitigation: Use consented minimal data, inspect storage and sync settings before use, and avoid entering sensitive financial details unless local persistence and any sync path are acceptable. <br>
Risk: Investment-related responses may drift into product recommendations, market timing, or decision support despite disclaimers. <br>
Mitigation: Require compliance checks, visible risk disclaimers, user confirmation for cross-skill advice, and independent review before acting on any investment-related output. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lj22503/investment-buddy-pet) <br>
- [Publisher Profile](https://clawhub.ai/user/lj22503) <br>
- [README](artifact/README.md) <br>
- [Compliance Rules](artifact/references/compliance-rules.md) <br>
- [Conversation Templates](artifact/references/conversation-templates.md) <br>
- [Pet Configs](artifact/references/pet-configs.md) <br>
- [Compliance Design](artifact/docs/COMPLIANCE_DESIGN.md) <br>
- [Data API Spec](artifact/docs/DATA_API_SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON-backed configuration references, and optional generated text responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read pet configuration files, generate compliance-checked investment education text, and provide commands for local scripts when the agent has execution capability.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata; artifact frontmatter and clawhub.json show 1.2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
KallyAI Executive Assistant is a Claude Code skill for using the KallyAI CLI to delegate phone calls, inbound reception, email, bookings, research, errands, multi-channel messaging, budgets, credits, subscriptions, and phone-number management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sltelitsyn](https://clawhub.ai/user/sltelitsyn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to operate KallyAI from Claude Code for delegated communications, bookings, research, errands, account checks, and phone-number workflows. It is suited for authenticated users who want an agent to compose and run KallyAI CLI commands on their behalf. <br>

### Deployment Geography for Use: <br>
Global, subject to KallyAI supported-country restrictions for calls and phone numbers. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give KallyAI broad delegated authority over communications, bookings, spending-related tasks, phone routing, and account settings. <br>
Mitigation: Require explicit user confirmation before recipients, calls, emails, purchases or orders, bookings, cancellations, subscription changes, or phone-number changes are executed. <br>
Risk: Authenticated use may expose private messages, call transcripts, recordings, contacts, emails, goals, budgets, credits, and subscription details. <br>
Mitigation: Use the skill only on trusted machines, review KallyAI privacy and retention terms before use, and run logout or revoke access when finished. <br>
Risk: Natural-language requests routed through ask may trigger real-world actions from loosely scoped instructions. <br>
Mitigation: Ask the user to restate or approve concrete action details before allowing KallyAI to proceed with external communication, spending, routing, or account-management actions. <br>


## Reference(s): <br>
- [KallyAI API Reference](artifact/references/api-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sltelitsyn/kallyai-api) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/sltelitsyn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON CLI responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default CLI output is machine-readable JSON; --human produces formatted tables.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

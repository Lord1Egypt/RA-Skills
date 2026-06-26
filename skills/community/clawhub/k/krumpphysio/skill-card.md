## Description: <br>
Teaches OpenClaw agents to act as a Krump-inspired physiotherapy coach for therapeutic movement scoring, rehab coaching with Krump vocabulary and Laban notation, optional Canton ledger logging, and SDG 3 health-and-wellbeing flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arunnadarasa](https://clawhub.ai/user/arunnadarasa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure OpenClaw agents for Krump-inspired physiotherapy coaching, movement scoring, rehab adherence support, and optional integrations for video analysis, session logging, observability, and payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional video intake and health-session logging can handle patient data and health-related content. <br>
Mitigation: Obtain explicit consent, minimize PII, enable redaction and limited retention, and set privacy-preserving defaults before deployment. <br>
Risk: Optional telemetry can capture prompt content or tool I/O that may include sensitive health-session details. <br>
Mitigation: Disable prompt and tool-I/O capture by default for patient workflows, restrict credentials, and enable tracing only after privacy review. <br>
Risk: Optional provider APIs and Stripe payment links can expose credentials or create incorrect payment flows if configured casually. <br>
Mitigation: Review external code and provider settings, use scoped test credentials first, label test payment links clearly, and verify currency units before execution. <br>


## Reference(s): <br>
- [KrumpPhysio ClawHub page](https://clawhub.ai/arunnadarasa/krumpphysio) <br>
- [reference.md](artifact/reference.md) <br>
- [KrumpPhysio repository](https://github.com/arunnadarasa/krumpphysio) <br>
- [Implementation guide](https://github.com/arunnadarasa/krumpphysio/blob/main/docs/IMPLEMENTATION-GUIDE-FLOCK-OPENCLAW-CANTON.md) <br>
- [Quantum README](https://github.com/arunnadarasa/krumpphysio/blob/main/quantum/README.md) <br>
- [Privacy documentation](https://github.com/arunnadarasa/krumpphysio/blob/main/docs/PRIVACY.md) <br>
- [Sindri ZKP Telegram FLock documentation](https://github.com/arunnadarasa/krumpphysio/blob/main/docs/SINDRI-ZKP-TELEGRAM-FLOCK.md) <br>
- [Stripe documentation](https://github.com/arunnadarasa/krumpphysio/blob/main/docs/STRIPE.md) <br>
- [Best practices](https://github.com/arunnadarasa/krumpphysio/blob/main/docs/BEST-PRACTICES.md) <br>
- [ClawHub krump skill](https://clawhub.ai/arunnadarasa/krump) <br>
- [ClawHub asura skill](https://clawhub.ai/arunnadarasa/asura) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with scoring feedback, Laban notation, health tips, and optional shell commands or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize JSON returned by optional local video or quantum scripts into human-facing coaching responses.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

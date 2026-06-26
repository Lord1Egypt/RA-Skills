## Description: <br>
AI-powered fertility tracking with personalized temperature pattern detection and multi-signal fusion for ovulation prediction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mayi12345](https://clawhub.ai/user/mayi12345) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and OpenClaw agents use this skill to track ovulation signals, record cycle observations, and generate fertility-window guidance from temperature, HRV, LH tests, cervical mucus, and symptom data. Treat outputs as reproductive-health tracking assistance, not medical advice or contraception guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive reproductive-health, symptom, and cycle-history data while making local-only privacy claims that may not hold when Oura, email, Telegram, or other integrations are enabled. <br>
Mitigation: Review configured integrations before use, store tokens and local data with restricted permissions, and assume external services can receive sensitive metadata when enabled. <br>
Risk: Partner alerts can disclose sensitive fertility or reproductive-health information to another person. <br>
Mitigation: Verify recipients, obtain explicit consent, and disable or redact partner notifications unless the user intentionally wants those disclosures. <br>
Risk: Ovulation predictions may be inaccurate or overtrusted for medical, conception, or contraception decisions. <br>
Mitigation: Treat predictions as tracking assistance only and verify important decisions with clinical guidance or validated fertility methods. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/mayi12345/ovulation-tracking) <br>
- [Oura personal access tokens](https://cloud.ouraring.com/personal-access-tokens) <br>
- [Oura daily readiness API](https://api.ouraring.com/v2/usercollection/daily_readiness) <br>
- [OpenClaw fertility tracker documentation](https://docs.openclaw.ai/skills/fertility-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, shell commands, configuration] <br>
**Output Format:** [Plain text or Markdown guidance with CLI output and JavaScript return objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cycle-day status, ovulation prediction confidence, signal summaries, local JSON state files, and optional partner alert content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter, changelog, and v2 package report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

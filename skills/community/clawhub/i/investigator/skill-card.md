## Description: <br>
Investigate public online footprints using open-source intelligence techniques for usernames, emails, people, companies, domains, IPs, phone numbers, locations, images, and other public targets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Elyasuuuuu](https://clawhub.ai/user/Elyasuuuuu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill for legitimate public-footprint OSINT, defensive exposure checks, and structured investigation reports based on publicly available evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports that one domain-check script can execute injected shell commands from crafted domain input. <br>
Mitigation: Review before installing, avoid running the domain helper on untrusted or unsanitized domain strings, and fix the shell invocation before operational use. <br>
Risk: HIBP, IP, and profile lookups disclose target identifiers to external services. <br>
Mitigation: Use these lookups only for legitimate, public, non-invasive OSINT or defensive exposure checks, and avoid private-person targeting without a valid basis. <br>
Risk: Public profile correlation can be misused for doxxing, stalking, harassment, or overconfident identity claims. <br>
Mitigation: Apply the documented safety boundaries, refuse invasive requests, and report uncertainty with clear confidence labels and caveats. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Target Types](references/target-types.md) <br>
- [OSINT Sources](references/osint-sources.md) <br>
- [Platform Validation](references/platform-validation.md) <br>
- [Scoring](references/scoring.md) <br>
- [Aggregation](references/aggregation.md) <br>
- [Output](references/output.md) <br>
- [Safety](references/safety.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown summaries and structured JSON reports with optional shell-command helper usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports distinguish confirmed, likely, weak, not-verifiable, and no-evidence findings, and include confidence and caveats.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

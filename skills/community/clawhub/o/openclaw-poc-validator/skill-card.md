## Description:

Automated vulnerability verification and payload replay probe that executes specific HTTP requests and analyzes response status codes and error traces for signs of injection or server exceptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whatyourname12345](https://clawhub.ai/user/whatyourname12345)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security testers use this skill to replay supplied raw HTTP requests or payloads against authorized targets and produce a vulnerability validation report with status, conclusion, and response evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can actively probe HTTP targets and may be misused for unauthorized vulnerability testing.

Mitigation: Use only for controlled security testing on systems the operator owns or is explicitly authorized to assess.

Risk: Replay requests may include sensitive cookies, tokens, or headers.

Mitigation: Avoid passing production credentials and redact sensitive headers before replaying or sharing reports.

Risk: HTTPS certificate verification is disabled by default in the replay script.

Mitigation: Treat results cautiously and enable certificate verification or use a trusted controlled test environment when validating findings.

Risk: The documented shell command template can be unsafe with untrusted request data.

Mitigation: Do not pass untrusted request data directly through shell interpolation; validate and quote inputs before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Analysis]

**Output Format:** [Markdown vulnerability validation report with extracted response evidence and optional JSON from the replay script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports target interface, test payload, response status, analysis conclusion, and critical evidence or stack trace snippet.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

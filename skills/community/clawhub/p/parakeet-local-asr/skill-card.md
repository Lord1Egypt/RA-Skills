## Description:

Install and operate local NVIDIA Parakeet ASR for OpenClaw with an OpenAI-compatible transcription API on Ubuntu/Linux and macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hantok](https://clawhub.ai/user/hantok)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install, start, health-check, and smoke-test a local private speech-to-text service for OpenClaw using NVIDIA Parakeet ASR.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bootstrap script can run mutable third-party setup code from an unpinned GitHub repository.

Mitigation: Review the upstream repository and setup.sh revision before running bootstrap.sh, and prefer pinning PARAKEET_REPO_URL to a trusted commit or release.

Risk: The bootstrap script allows PARAKEET_REPO_URL overrides, which could direct installation to an untrusted source.

Mitigation: Use repository overrides only for trusted sources and document the exact source used for installation.

Risk: Smoke-test audio is posted to the configured transcription endpoint.

Mitigation: Send test audio only to a trusted local endpoint and verify PARAKEET_URL before running smoke-test.sh.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hantok/skills/parakeet-local-asr)
- [ClawHub publisher profile](https://clawhub.ai/user/hantok)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local endpoint URLs, health-check results, transcription test commands, and ASR troubleshooting guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

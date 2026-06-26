## Description: <br>
Kefal Guard monitors OpenClaw hosts with a separately installed read-only telemetry agent to detect exposed services, privilege escalation paths, unauthorized SSH keys, novel outbound connections, and other infrastructure risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidangularme](https://clawhub.ai/user/davidangularme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to check OpenClaw host security, review incidents, and obtain remediation guidance after installing the separate Kefal agent. It is intended for ongoing infrastructure monitoring before and after exposing an OpenClaw gateway or installing third-party skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The separately installed Kefal agent can collect host security metadata and upload it to kefal.dev. <br>
Mitigation: Install only after reviewing the Kefal agent, installation guide, checksums, and telemetry expectations. <br>
Risk: Broad security questions may cause the skill to run full scans through kefal-agent. <br>
Mitigation: Require operator confirmation before running full scans on sensitive hosts or environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/davidangularme/kefal-guard) <br>
- [Kefal homepage](https://kefal.dev) <br>
- [Kefal installation guide](https://kefal.dev/docs/installation.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown security reports with incident summaries, status output, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke the separately installed kefal-agent locally; remediation commands are presented for operator review.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

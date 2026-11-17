## Description:

Run HTTP performance tests with latency and throughput measurement for benchmarking web services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Perftest to run curl-based HTTP latency, throughput, stress, report, and comparison checks while benchmarking web services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted target inputs may cause curl to read or send local files.

Mitigation: Run only with trusted, simple HTTP or HTTPS targets until arguments are quoted, curl -- is used, and URL/count validation is added.

Risk: Report and compare commands can read arbitrary local files when given sensitive paths.

Mitigation: Avoid using report or compare on sensitive paths and restrict report files to the skill data directory.

## Reference(s):

- [Perftest on ClawHub](https://clawhub.ai/bytesagain-lab/skills/perftest)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text with shell command examples and benchmark metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; stores data under ~/.local/share/perftest/.]

## Skill Version(s):

3.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

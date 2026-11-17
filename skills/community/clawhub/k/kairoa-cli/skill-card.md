## Description:

Kairoa CLI helps agents use a developer toolbox for encoding, hashing, UUID generation, data conversion, JSON and SQL handling, network checks, password and vault tasks, mock data, OTP, QR codes, regex testing, image and PDF inspection, coordinate conversion, and AI chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luduoxin](https://clawhub.ai/user/luduoxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to route common development utility work through the Kairoa CLI instead of hand-writing one-off scripts. It supports local transformations, generated shell commands, file and data inspection, network checks, credential-related utilities, and optional AI chat through OpenAI-compatible APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external CLI and documents installation paths that can use unpinned releases or a remote install script.

Mitigation: Install a pinned, verified Kairoa release, review any install script before execution, and avoid system-wide installation unless it is required.

Risk: The skill can operate on secrets and sensitive local data through .env, vault, password, OTP, file, and AI chat commands.

Mitigation: Run commands only on data and providers the user explicitly trusts, prefer environment variables or interactive secret entry over command-line secrets, and avoid exposing confidential data to AI providers unless authorized.

Risk: HTTP, WebSocket, DNS, IP lookup, TLS, traceroute, and port-scan commands can contact external or internal network targets.

Mitigation: Use network and scanning commands only against targets the user owns or is authorized to test.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luduoxin/skills/kairoa-cli)
- [Kairoa CLI project repository](https://github.com/covoyage/kairoa-cli)
- [Kairoa CLI releases](https://github.com/covoyage/kairoa-cli/releases/latest)
- [Covoyage Scoop bucket](https://github.com/covoyage/scoop-bucket)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, command output summaries, and JSON when the underlying CLI command emits structured output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local CLI commands that read files, process secrets, call network targets, or contact OpenAI-compatible AI providers when those features are requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

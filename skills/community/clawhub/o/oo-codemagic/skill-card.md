## Description: <br>
Codemagic (codemagic.io) helps agents read, create, and update Codemagic data through the OOMOL Codemagic connector instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Codemagic connector schemas, run Codemagic actions through the oo CLI, and manage builds, apps, teams, and user/team build data from an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The first-time setup fallback includes pipe-to-shell installer commands for the oo CLI. <br>
Mitigation: Use the official install guide, verify checksums or signatures when available, and get explicit approval before installing or signing in. <br>
Risk: Codemagic create and cancel build actions can change remote build state. <br>
Mitigation: Confirm the target, payload, and expected effect with the user before running write actions. <br>
Risk: The skill requires sensitive credentials through an OOMOL-connected account. <br>
Mitigation: Install only when the publisher is trusted and the Codemagic connection is needed; rely on server-side credential injection rather than exposing raw tokens. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-codemagic) <br>
- [Codemagic Homepage](https://codemagic.io) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses include a data object and meta.executionId when actions run successfully.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

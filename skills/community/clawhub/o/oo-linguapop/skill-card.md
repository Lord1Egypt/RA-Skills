## Description: <br>
Linguapop (linguapop.eu). Use this skill for reading, creating, and updating Linguapop data through an OOMOL-connected account instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business users use this skill to inspect Linguapop connector schemas, list available placement-test languages, and create placement-test invitations through an OOMOL-connected Linguapop account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected Linguapop account and may access account-backed data or credentials handled by OOMOL. <br>
Mitigation: Install and use it only when the user intends to let the agent operate the connected Linguapop account. <br>
Risk: The send_invitation action changes Linguapop state by creating placement-test invitations and may send email or configure callback and return URLs. <br>
Mitigation: Confirm the exact payload and expected effect with the user before running write actions. <br>
Risk: The optional first-time setup includes pipe-to-shell CLI install commands. <br>
Mitigation: Avoid running the installer unless the user trusts OOMOL's CLI distribution path or has verified it through official install guidance. <br>


## Reference(s): <br>
- [ClawHub Linguapop skill page](https://clawhub.ai/oomol/oo-linguapop) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [Linguapop homepage](https://www.linguapop.eu/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses from connector actions are JSON objects with data and meta execution identifiers.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

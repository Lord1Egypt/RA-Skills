## Description: <br>
Use this skill to operate V2EX through the OOMOL v2ex connector and oo CLI for reading, creating, updating, and deleting V2EX data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate V2EX through their OOMOL-connected account, including reading public and authenticated content and performing explicitly confirmed account actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authenticated control over a V2EX account. <br>
Mitigation: Install only when the user trusts OOMOL and wants account operation through the oo CLI; require explicit confirmation before every non-read action. <br>
Risk: State-changing actions can affect topics, tokens, sticky status, or notifications. <br>
Mitigation: Confirm the exact target, payload, and effect before running boost_topic, create_token, set_topic_sticky, delete_notification, or any other non-read action. <br>
Risk: Remote installer commands are present for first-time oo CLI setup. <br>
Mitigation: Prefer reviewed official installation instructions and do not let an agent run a remote installer directly without user approval. <br>


## Reference(s): <br>
- [ClawHub V2EX skill](https://clawhub.ai/oomol/oo-v2ex) <br>
- [V2EX homepage](https://www.v2ex.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command payloads; connector responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an installed oo CLI, OOMOL sign-in, connected V2EX credentials, and explicit confirmation before non-read actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version and artifact metadata.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

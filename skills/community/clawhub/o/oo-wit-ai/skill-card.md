## Description: <br>
Wit.ai (wit.ai). Use this skill for ANY Wit.ai request -- reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and manage Wit.ai apps, intents, entities, traits, utterances, and message analysis through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Wit.ai state through write actions. <br>
Mitigation: Review the exact JSON payload and expected effect with the user before approving write actions. <br>
Risk: The skill includes destructive utterance deletion. <br>
Mitigation: Require explicit approval for the target utterances before running destructive actions. <br>
Risk: The skill requires a connected OOMOL account and sensitive Wit.ai credentials. <br>
Mitigation: Install it only when agent access to Wit.ai is intended, and perform first-time CLI or connection setup only after an auth or connection failure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-wit-ai) <br>
- [Wit.ai homepage](https://wit.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Wit.ai icon](https://static.oomol.com/logo/third-party/Wit.ai.svg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON payload patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing payloads; command responses are JSON when run with --json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

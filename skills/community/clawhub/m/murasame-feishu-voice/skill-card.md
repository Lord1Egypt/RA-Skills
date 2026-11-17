## Description:

Sends Chinese Feishu text messages and matching Murasame voice bubbles from labelled or keyword-matched responses, with mapping and voice toggle controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenxundaozu](https://clawhub.ai/user/chenxundaozu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to enrich Feishu conversations with Murasame voice bubbles while preserving readable Chinese text. It is suited for controlled chat workflows that need labelled emotion categories, keyword fallback, and an explicit voice on/off switch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext debug logging can persist message content on disk.

Mitigation: Remove or disable the debug write before installation, and avoid sending sensitive message content until it is confirmed absent.

Risk: The voice sender is delegated to a sibling script while passing the full environment to child processes.

Mitigation: Bundle or verify the sibling sender and pass only the Feishu variables needed for execution.

Risk: Feishu credentials, receiver OpenID, app permissions, and fixed Windows workspace paths can cause delivery failures or unintended messaging if misconfigured.

Mitigation: Confirm app scopes, recipient OpenID, and local audio/state paths in the target environment before enabling voice delivery.

## Reference(s):

- [Voice label mapping](references/mapping.json)
- [ClawHub skill page](https://clawhub.ai/chenxundaozu/skills/murasame-feishu-voice)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text status strings and shell command usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send Feishu text and audio messages through configured app credentials and receiver OpenID.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

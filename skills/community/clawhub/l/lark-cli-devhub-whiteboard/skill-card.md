## Description:

Use when creating or updating Feishu/Lark Whiteboards through lark-cli or feishu-cli for a development knowledge hub, including architecture maps, bug investigation paths, task maps, dependency maps, and project knowledge graphs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afengzi](https://clawhub.ai/user/afengzi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to create or update Lark/Feishu whiteboards for development knowledge hubs, including architecture maps, release flows, bug diagnosis paths, dependency maps, and project knowledge graphs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an npm package through npx, which executes code from the package ecosystem.

Mitigation: Pin @larksuite/whiteboard-cli to an exact reviewed version before use.

Risk: Whiteboard rendering and updates may access local project files or Lark credentials.

Mitigation: Run rendering with only needed project access and keep Lark credentials scoped to the target whiteboard.

Risk: Generated OpenAPI JSON or overwrite operations could update an unintended board state.

Mitigation: Review generated JSON, keep dry-run enabled until reviewed, and confirm the remote board after meaningful redraws.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/afengzi/skills/lark-cli-devhub-whiteboard)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local rendering, JSON review, dry-run whiteboard updates, and post-update confirmation.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Archive, browse, and manage chat content including links, notes, and images with read/star status and pagination in an IM-native inbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echoofzion](https://clawhub.ai/user/echoofzion)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to save explicitly requested links, notes, and image paths from chat into a local inbox, then browse, view, mark, star, or delete saved items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved inbox content is stored locally in the skill's data files and may include sensitive links, notes, or image paths.

Mitigation: Avoid saving secrets or highly sensitive notes unless local JSON storage is acceptable for the deployment environment.

Risk: Delete commands remove records without an undo flow or confirmation prompt.

Mitigation: Review item IDs before deletion and keep separate backups if retained content matters.

Risk: The skill can archive normal chat content if an agent ignores the explicit-intent rule.

Mitigation: Only run add/archive actions after clear user keywords such as archive, save, bookmark, 收录, 归档, 保存, or 记录.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/echoofzion/skills/little-steve-content-inbox)
- [ClawHub publisher profile](https://clawhub.ai/user/echoofzion)
- [Declared project homepage](https://github.com/EchoOfZion/little-steve-content-inbox)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists saved inbox records in local JSON data files and depends on jq.]

## Skill Version(s):

0.1.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

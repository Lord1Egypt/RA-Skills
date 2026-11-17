## Description:

Npy helps a user create a personalized AI companion persona skill from descriptions, matching prompts, or imported chat history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwwttlll](https://clawhub.ai/user/wwwttlll)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to define, generate, and maintain AI companion persona skills for emotional companionship workflows. It can guide persona creation from manual descriptions, personality matching inputs, or user-provided chat exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local messaging databases and decrypted chat exports may expose sensitive personal conversations.

Mitigation: Prefer manually exported, consented chat snippets; keep decrypted outputs out of shared folders and version control.

Risk: WeChat database decryption can involve local process-memory inspection and broad system access.

Mitigation: Avoid elevated privileges where possible and do not run the decryptor unless the user understands and accepts the local access required.

Risk: Generated companion skills and later adjustments can persist sensitive persona, relationship, or chat-derived details.

Mitigation: Review generated persona files and adjustments before reuse, sharing, or installing them as project or global skills.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwwttlll/skills/npy-skill)
- [README](artifact/README.md)
- [Product requirements](artifact/docs/PRD.md)
- [Smart matching guide](artifact/prompts/smart_matching.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated skill files, JSON metadata, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persona skill directories, relationship memory files, chat-derived artifacts, and version history.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

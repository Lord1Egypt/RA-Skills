## Description:

Guides agents through creating songs, instrumentals, and lyric-driven tracks across available music backends, with structured prompts and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luischarro](https://clawhub.ai/user/luischarro)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use Music Craft to turn a music request, source text, or lyrics into a structured prompt, route it to an available generation backend, and check the resulting track. It also provides optional lyric cleanup and stem tools for user-owned audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags a memory-cap override that could contribute to system-wide memory exhaustion.

Mitigation: Explain the memory impact, check available memory, and get consent before using the override; use a lower-memory tier when appropriate.

Risk: The security review flags possible use of an unidentified music CLI without clear data-sharing disclosure; prompts, lyrics, or reference material may be sent to a cloud provider.

Mitigation: Identify the selected backend, explain what content it sends externally, and get consent before cloud submission.

Risk: The security review is incomplete and rates the release suspicious with medium confidence.

Mitigation: Review the skill and its tool behavior before execution, as advised by the security guidance.

## Reference(s):

- [Music Craft skill guide](artifact/SKILL.md)
- [Request intake and output layout](artifact/references/request-intake.md)
- [Prompt formula](artifact/references/prompt-formula.md)
- [Setup and pre-flight](artifact/references/setup-and-preflight.md)
- [Quality and revision](artifact/references/quality-and-revision.md)
- [MPS memory safety guidance](artifact/references/mps-bf16-acceleration.md)

## Skill Output:

**Output Type(s):** [Audio files, Lyrics, Music prompts, Verification notes, Code and shell commands]

**Output Format:** [Generated audio files with supporting text, prompts, and optional analysis or stem files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Track length, style, language, vocals, and backend follow the user's request and available tools.]

## Skill Version(s):

1.8.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

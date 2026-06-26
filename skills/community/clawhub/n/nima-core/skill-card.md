## Description: <br>
Neural Integrated Memory Architecture provides persistent memory, emotional intelligence, semantic recall, memory pruning, affect analysis, and embedding-provider options for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dmdorta1111](https://clawhub.ai/user/dmdorta1111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent local memory, semantic recall, affect tracking, and optional memory consolidation to OpenClaw-based agents. It is intended for agents that need prior conversation context and configurable local or remote embedding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has broad persistent access to OpenClaw conversation transcripts and stores derived memory data locally. <br>
Mitigation: Install only when persistent transcript-derived memory is acceptable, keep storage under the expected NIMA data directory, and review enabled OpenClaw plugins before use. <br>
Risk: The installer can modify the OpenClaw extension environment. <br>
Mitigation: Review install.sh before running it and verify the OpenClaw extension changes after installation. <br>
Risk: Remote embedding or LLM providers may receive transcript-derived text when configured. <br>
Mitigation: Use local embeddings when external processing is not acceptable, and configure Voyage, OpenAI, or other API keys only after approving that data flow. <br>
Risk: Precognitive cron or action features may inspect workspace, GitHub, calendar, service, or file context when enabled. <br>
Mitigation: Keep those features disabled unless that inspection is intended and the connected data sources have been reviewed. <br>
Risk: Legacy pickle memory files can be unsafe if loaded from untrusted sources. <br>
Mitigation: Do not import or load legacy pickle memory files unless their origin and contents are trusted. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/dmdorta1111/nima-core) <br>
- [NIMA Core website](https://nima-core.ai) <br>
- [README](README.md) <br>
- [Installation guide](INSTALL.md) <br>
- [Security policy](SECURITY.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation, inline shell commands, JSON configuration snippets, and runtime text/context injection] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local memory databases, affect state, embeddings, logs, and OpenClaw extension files during installation and runtime.] <br>

## Skill Version(s): <br>
3.1.5 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

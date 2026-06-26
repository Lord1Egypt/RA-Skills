## Description: <br>
Sync provider model lists into OpenClaw config with a dry-run preview, confirmation path, and apply mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[C-Joey](https://clawhub.ai/user/C-Joey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to preview and apply updates from upstream provider model lists into an OpenClaw configuration. It supports model-field normalization, provider-specific mappings, optional API-mode probing, backups before writes, and alignment of provider models with agent model aliases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify OpenClaw provider configuration when apply mode is used. <br>
Mitigation: Run dry-run or check-only first, review the change summary, and use apply mode only after confirming the target provider and intended updates. <br>
Risk: Using provider=all or default alias pruning can remove stale agent model aliases across multiple providers. <br>
Mitigation: Prefer a single provider id for routine updates, review added and removed aliases in the preview, and use --no-prune-agent-aliases when aliases should be retained. <br>
Risk: API keys or authorization headers may be needed to fetch private provider model lists. <br>
Mitigation: Use credentials only in trusted private contexts, avoid sharing command transcripts that contain secrets, and rely on dry-run summaries rather than exposing raw authenticated responses. <br>
Risk: Custom mappings with --allow-outside-provider can write outside the normal provider subtree. <br>
Mitigation: Avoid --allow-outside-provider unless each destination path has been reviewed and the write scope is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/C-Joey/provider-sync) <br>
- [Examples](references/examples.md) <br>
- [Field Normalization](references/field-normalization.md) <br>
- [Provider Patterns](references/provider-patterns.md) <br>
- [Safety Rules](references/safety-rules.md) <br>
- [Gemini Notes](references/gemini.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON summaries with command examples and configuration-change details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce dry-run previews, check-only summaries, apply results, backup paths, model deltas, and optional API probe summaries.] <br>

## Skill Version(s): <br>
2.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

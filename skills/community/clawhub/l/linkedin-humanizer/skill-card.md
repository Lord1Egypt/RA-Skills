## Description:

Scrub AI tells from text drafts or audit finished LinkedIn posts against heuristic checks for length, hook, CTA, format penalties, AI vocabulary, emoji patterns, and detector disagreement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to revise AI-drafted LinkedIn posts, audit publish readiness, preserve the writer's voice, and document disagreement across AI-detection tools before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The detector-testing path can upload complete drafts to third-party AI detector services when API keys are configured.

Mitigation: Use audit or demo mode for local-only review, avoid API mode for confidential drafts, and require explicit provider selection and consent before detector uploads.

Risk: The skill aggressively rewrites LinkedIn drafts, which can alter tone or remove stylistic choices the author intended to keep.

Mitigation: Review the diff before publishing, preserve the user's stated claims, and ask for missing numbers or anecdotes instead of fabricating details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sergebulaev/skills/linkedin-humanizer)
- [Scrub Rules](references/scrub-rules.md)
- [Voice Fingerprint](references/voice-fingerprint.md)
- [Tier Rationale](references/tier-rationale.md)
- [Rule Explainer](references/rules-explainer.md)
- [Emoji Patterns](references/emoji-patterns.md)
- [Supported AI Detectors](references/detector-list.md)
- [Audit Checklist](references/audit-checklist.md)
- [Audit AI Tells](references/audit-ai-tells.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with rewritten text, diffs, audit findings, detector-spread reports, and inline shell commands when detector scripts are used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence labels, applied tier, blockers, warnings, suggested fixes, and detector-score spread summaries.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Zero-Anlas NovelAI workflows for OpenClaw: fiction writing, story planning, account checks, cost estimates, tag suggestions, same-session verification reuse, bounded transient retries, and strictly guarded single-image generation only when the current tool proves the estimate is 0 Anlas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techotaku39](https://clawhub.ai/user/techotaku39)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users and developers use this skill to plan, write, and manage NovelAI-assisted fiction workflows while preventing NovelAI Image Anlas spending. It permits account checks, cost estimates, tag suggestions, text workflows, and a single guarded image request only after an explicit zero-Anlas estimate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Same-session cost-verification reuse could allow image generation to proceed on stale billing information.

Mitigation: Review the lease behavior before installing; for stronger zero-cost protection, require a fresh cost estimate immediately before every image generation.

Risk: A request estimated at 0 Anlas can still consume the separate Opus V5 Usage Limit.

Mitigation: Keep the Usage Limit warning visible in user-facing responses and audit results after allowed generations.

Risk: The skill requires a NovelAI token, which would be sensitive if exposed through prompts, logs, files, or metadata.

Mitigation: Use host-managed credentials only and follow the skill policy that forbids requesting, printing, storing, or embedding NOVELAI_TOKEN.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/techotaku39/skills/novelai-free)
- [Metadata Homepage](https://github.com/techotaku39/openclaw-novelai/tree/main/variants/openclaw-novelai-free)
- [Zero-Anlas Mode: Costs and Quotas](docs/COSTS-AND-QUOTAS.md)
- [NovelAI Subscription](https://docs.novelai.net/en/subscription/)
- [NovelAI FAQ - Opus Usage Limits](https://docs.novelai.net/en/faq/)
- [Steps & Prompt Guidance](https://docs.novelai.net/en/image/stepsguidance/)
- [NovelAI Image Generation](https://docs.novelai.net/en/image/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text responses with guarded tool-use decisions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reuse a verified zero-cost billing profile within the same conversation when billing-affecting parameters remain unchanged; image generation is limited to one image after an explicit zero-Anlas gate.]

## Skill Version(s):

0.1.2 (source: frontmatter, CHANGELOG, release evidence; released 2026-09-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

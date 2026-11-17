## Description:

One Person Company OS builds a visual operating cockpit for an AI-native one-person company across promise, buyer, product capability, delivery, cash, learning, and assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[living-hi](https://clawhub.ai/user/living-hi)

### License/Terms of Use:

MIT-0

## Use Case:

Solo founders and agents use this skill to turn an AI product idea into a local operating workspace with a visible business loop, current bottleneck, next action, formal deliverables, and visual assets. It supports founder-reviewed drafting and updates for product, sales, delivery, cash, learning, and asset work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A runtime helper has an under-disclosed path that can run arbitrary local Python scripts.

Mitigation: Limit normal use to documented commands and a workspace path the founder explicitly approves; do not invoke scripts/ensure_python_runtime.py with --apply --run-script unless the target is a trusted repository script and the resolved path has been reviewed.

Risk: Generated business, pricing, legal, launch, budget, and customer-facing materials can be incorrect or premature if treated as final decisions.

Mitigation: Keep the founder as the approval boundary and review high-impact outputs before publishing, sending, spending, or deploying.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/living-hi/skills/one-person-company-os)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)
- [Security policy](artifact/SECURITY.md)
- [Changelog](artifact/CHANGELOG.md)
- [ClawHub listing](artifact/release/clawhub-listing.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown and local workspace files, including HTML, DOCX deliverables, SVG visuals, JSON state, and optional prompt text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal use expects a trusted local Python 3.7+ runtime, writes only inside a founder-approved workspace, and does not require API keys or image generation.]

## Skill Version(s):

1.0.3 (source: server release metadata and CHANGELOG, released 2026-05-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

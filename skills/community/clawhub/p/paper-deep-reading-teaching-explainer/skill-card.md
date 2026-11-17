## Description:

Deep-read research papers into authoritative, evidence-grounded teaching reports, reproducibility and defense-ready explanations, innovation-mining artifacts, staged multi-image cartoon storyboard plans with source-grounding checks, and final image-PDF assembly guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c-narcissus](https://clawhub.ai/user/c-narcissus)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, educators, and technical teams use this skill to turn one paper or a small paper set into rigorous teaching reports, reproducibility audits, defense preparation material, research-direction notes, staged storyboard prompts, and final PDF assembly guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaging and validation helpers can read or include files outside the intended paper workspace.

Mitigation: Use a dedicated project directory with no secrets or unrelated files, remove symlinks, and review manifests before running helper scripts.

Risk: Attacker-supplied paper workspaces or manifests can influence generated reports, bundles, or validation behavior.

Mitigation: Install and run the skill only with trusted workspace inputs, and inspect generated artifacts before sharing or publishing them.

Risk: External image-generation services may receive paper-derived content during optional storyboard steps.

Mitigation: Treat external image generation as opt-in and use only user-approved services and paper content approved for that processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/c-narcissus/skills/paper-deep-reading-teaching-explainer)
- [README](artifact/README.md)
- [Security and privacy notes](artifact/SECURITY_PRIVACY.md)
- [Detailed report contract](artifact/schemas/detailed_report_contract.md)
- [Research-generative overlay](artifact/schemas/research_generative_overlay.md)
- [Teaching explanation overlay](artifact/schemas/teaching_explanation_overlay.md)
- [Visual source-grounding anti-hallucination overlay](artifact/schemas/visual_source_grounding_anti_hallucination_overlay.md)
- [Reproducibility defense quality overlay](artifact/schemas/reproducibility_defense_quality_overlay.md)
- [Storyboard PDF assembly workflow](artifact/workflow/09_storyboard_pdf_assembly.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and guidance, JSON planning artifacts, Python helper commands, and image/PDF assembly instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce staged status handoffs, teaching sidecars, storyboard prompt batches, and local PDF assembly outputs when requested.]

## Skill Version(s):

10.1.8 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

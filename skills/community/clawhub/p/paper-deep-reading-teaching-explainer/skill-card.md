## Description: <br>
Deep-reads research papers into evidence-grounded teaching reports, reproducibility and defense preparation, innovation-mining artifacts, staged cartoon storyboard plans, and final image-PDF assembly guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-narcissus](https://clawhub.ai/user/c-narcissus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, instructors, and engineers use this skill to turn one paper or a small paper set into detailed teaching reports, discussion and defense preparation, reproducibility checks, staged visual-storyboard guidance, and final PDF handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated paper reports or storyboard prompts may overstate unsupported claims from a source paper. <br>
Mitigation: Keep paper-stated facts, reasonable inference, nearby-work inference, and missing or not-reported details explicitly labeled, and check storyboard prompts against the original PDF or LaTeX and the authoritative report. <br>
Risk: External image APIs may receive paper content or derived teaching material during storyboard generation. <br>
Mitigation: Use external image providers only for content the user is allowed to send to that provider, and prefer approved platform image tools or local assembly for final PDFs. <br>
Risk: Zip or bundle outputs could accidentally include unintended local files if run from a broad workspace. <br>
Mitigation: Run helper scripts in the intended project directory, avoid broad personal directories as workspace roots, and review generated archives before uploading them to project sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/c-narcissus/paper-deep-reading-teaching-explainer) <br>
- [README](README.md) <br>
- [Security and privacy notes](SECURITY_PRIVACY.md) <br>
- [Publish page information](PUBLISH_PAGE_INFO_CN.md) <br>
- [Detailed report contract](schemas/detailed_report_contract.md) <br>
- [Research-generative overlay](schemas/research_generative_overlay.md) <br>
- [Teaching explanation overlay](schemas/teaching_explanation_overlay.md) <br>
- [Reproducibility defense quality overlay](schemas/reproducibility_defense_quality_overlay.md) <br>
- [Visual source-grounding anti-hallucination overlay](schemas/visual_source_grounding_anti_hallucination_overlay.md) <br>
- [Final storyboard PDF assembly workflow](workflow/09_storyboard_pdf_assembly.md) <br>
- [External best-practice sources](schemas/external_best_practices_sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON metadata templates, image-generation prompts, and local PDF assembly instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Separates text report generation, image/storyboard generation, and final PDF assembly; may produce staged bundles, validation artifacts, and 16:9 storyboard PDF handoffs.] <br>

## Skill Version(s): <br>
10.1.8 (source: SKILL.md frontmatter, _meta.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

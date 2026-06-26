## Description: <br>
A reusable skill for designing, prompting, generating, critiquing, and integrating publication-ready research-paper framework figures, including method overviews, architecture diagrams, pipelines, agent workflows, system/data-flow figures, mechanisms, case walkthroughs, evidence boards, and taxonomy maps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c-narcissus](https://clawhub.ai/user/c-narcissus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, paper authors, and technical teams use this skill to turn paper material, abstracts, method notes, or draft ideas into comparable figure directions, image-generation briefs, candidate figures, revision guidance, captions, legends, and body-text integration notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using unpublished papers or proprietary reference images with an external image-generation provider can expose sensitive material. <br>
Mitigation: Use only image-generation providers approved for the material being processed, and avoid submitting confidential content unless that provider is authorized. <br>
Risk: The workflow is intentionally rigid and defaults to several candidate images, which may create more outputs than expected. <br>
Mitigation: Confirm the requested candidate count and explicitly ask for a single image or a text-only path when fewer outputs are needed. <br>
Risk: The skill may produce Chinese section labels unless the user requests another language. <br>
Mitigation: Specify the required output language and label language before generating prompts or images. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/c-narcissus/paper-framework-figure-studio-pro) <br>
- [Publisher Profile](https://clawhub.ai/user/c-narcissus) <br>
- [Evidence Lineage Summary](references/evidence-lineage-summary.md) <br>
- [Evidence Map Index](references/evidence-map-index.md) <br>
- [Builder-Time Acquisition Report](references/builder-time-acquisition-report.md) <br>
- [Workflow and State Contract](references/workflow-and-state-contract.md) <br>
- [Visual Style and Board Protocol](references/visual-style-and-board-protocol.md) <br>
- [Prompt Generation Policy](references/prompt-generation-policy.md) <br>
- [Review Rubric](references/review-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Image-generation prompts, Images] <br>
**Output Format:** [Markdown text replies with structured workflow sections, plus image-only turns when an approved image-generation route is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to 4-6 text candidates and 4-6 visual candidates, usually 6, with strict separation between text-only and image-only replies.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, metadata.json, evidence release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

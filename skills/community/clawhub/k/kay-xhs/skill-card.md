## Description: <br>
Kay Xhs guides an agent through a Xiaohongshu content workflow: trend research, AI image or comic generation with kay-image, copywriting, and saving creator posts as drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[papayalove](https://clawhub.ai/user/papayalove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and agent operators use this skill to research Xiaohongshu content patterns, prepare image-led posts, generate supporting visuals, and place finished posts into a Xiaohongshu creator draft workflow. It is intended for workflows where the operator can review account state, uploaded files, and final copy before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates a logged-in Xiaohongshu creator account. <br>
Mitigation: Use a dedicated browser profile, confirm the target account before upload, and require explicit confirmation before publishing rather than saving a draft. <br>
Risk: The workflow can collect third-party post content, comments, images, and identifiers during trend research. <br>
Mitigation: Collect only data needed for the current task, avoid unnecessary personal identifiers, and review outputs for platform-policy and privacy concerns. <br>
Risk: Persistent work records may retain drafts, research notes, prompts, or collected source material without clear limits. <br>
Mitigation: Disable or tightly limit memory and archive steps unless retention is intentional, and periodically delete records that are no longer needed. <br>
Risk: The skill depends on KIE_API_KEY for image generation. <br>
Mitigation: Store the API key only in the expected environment or secret configuration and avoid including it in prompts, generated files, logs, or shared drafts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/papayalove/kay-xhs) <br>
- [Publisher profile](https://clawhub.ai/user/papayalove) <br>
- [KIE API](https://kie.ai/) <br>
- [Xiaohongshu creator console](https://creator.xiaohongshu.com) <br>
- [Xiaohongshu case analysis](artifact/references/cases.md) <br>
- [Image prompt templates](artifact/references/prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript snippets, JSON task configuration, and browser workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the kay-image skill and KIE_API_KEY for image generation; browser automation requires an authenticated Xiaohongshu creator session.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Kart Io Picture Book Wizard helps agents create Chinese/English children's picture-book stories, learning content, and image-generation prompts with age-aware structure, visual style choices, scene guidance, and character consistency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicky1108](https://clawhub.ai/user/nicky1108) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, educators, parents, and content creators use this skill to draft bilingual children's picture-book pages, learning points, and image-generation prompts for readers ages 3-12. It is useful when a story needs consistent characters, age-appropriate language, Chinese/English output, pinyin, and structured visual prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated stories may be retained locally under ./output/picture-books/ and can include prompt details supplied by the user. <br>
Mitigation: Avoid entering private personal details unless local retention is acceptable, and review or delete generated files according to the user's data-handling needs. <br>
Risk: Watermark guidance could be misapplied to images that the user did not originate. <br>
Mitigation: Apply watermark-prevention guidance only to original generated images, and do not use it to remove provenance, signatures, or ownership marks from third-party work. <br>
Risk: Children's educational content and image prompts may still need human review for age fit, cultural context, and factual accuracy. <br>
Mitigation: Use the skill's content safety and reality-validation guidance, then review generated stories and prompts before sharing or publishing them. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/nicky1108/kart-io-picture-book-wizard) <br>
- [Picture Book Wizard README](README.md) <br>
- [Reference Directory](references/README.md) <br>
- [Quick Reference](references/REFERENCE.md) <br>
- [Output Format Template](assets/templates/output-format.md) <br>
- [Content Safety Validation](references/config/core/content-safety-validation.md) <br>
- [Scene Matching](references/config/advanced/scene-matching.md) <br>
- [Reality Validation](references/config/advanced/reality-validation.md) <br>
- [Multi-Character Prompt Guide](references/guides/MULTI-CHARACTER-PROMPT-FIX.md) <br>
- [Watermark Troubleshooting](references/guides/WATERMARK-TROUBLESHOOTING.md) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with bilingual story text, pinyin, learning points, image prompts, and command-style examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated stories are intended to be saved under ./output/picture-books/ with date, style, scene, character, page count, and timestamp in the file path.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and Skillstore metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

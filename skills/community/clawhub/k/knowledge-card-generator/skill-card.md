## Description: <br>
Guides an agent to research a topic, draft a knowledge-card or poster for user confirmation, and then prepare a vertical educational image. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaodbb](https://clawhub.ai/user/zhaodbb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, educators, and knowledge-sharing teams use this skill to turn a topic into a concise educational card or poster. The workflow requires a text draft and user confirmation before image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated images may be uploaded to a public CDN, which can expose sensitive or private content. <br>
Mitigation: Use the skill only with non-sensitive content unless the user has reviewed and accepted public sharing. <br>
Risk: The artifact includes guidance that could bypass safety, copyright, or likeness limits for people and protected characters. <br>
Mitigation: Do not rely on substitute-generation guidance for people, copyrighted characters, or protected likenesses; apply rights, consent, and platform policy checks before generation. <br>


## Reference(s): <br>
- [Knowledge Card Generator listing](https://clawhub.ai/zhaodbb/knowledge-card-generator) <br>
- [Draft template](artifact/references/draft-template.md) <br>
- [Style guide](artifact/references/style-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft with image-generation prompt guidance and a PNG/public URL after confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates 1080x1920 vertical educational poster imagery only after the draft is confirmed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

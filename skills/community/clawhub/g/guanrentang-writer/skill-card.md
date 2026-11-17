## Description:

Guanrentang Writer helps generate branded Chinese WeChat public-account articles for Guanrentang-style traditional Chinese medicine content, including topic selection, Markdown drafting, fixed-material placement, and optional AI-generated article images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengxiaodong28](https://clawhub.ai/user/fengxiaodong28)

### License/Terms of Use:

MIT-0

## Use Case:

External clinic content operators and agents use this skill to draft Guanrentang-style Chinese WeChat articles for seasonal health topics, ancient-method fumigation promotion, and holiday notices. It can also prepare image markers, copy fixed assets, and call GLM-Image when configured with a ZHIPU_API_KEY.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger broadly on general article-writing requests.

Mitigation: Install it only for the intended Guanrentang-style Chinese WeChat content workflow and confirm activation before use in unrelated writing tasks.

Risk: The image workflow uses external GLM-Image API calls.

Mitigation: Confirm with the user before external image generation and avoid sending sensitive or private content in prompts.

Risk: The documented .env sourcing pattern can execute local shell code.

Mitigation: Provide ZHIPU_API_KEY through a trusted environment or secret manager instead of sourcing an unreviewed .env file.

Risk: Generated health and clinic marketing content may be inaccurate or unsuitable for publication.

Mitigation: Review every generated article before publishing, especially medical claims, contraindications, promotions, and follow or QR-code assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fengxiaodong28/skills/guanrentang-writer)
- [Zhipu Open Platform](https://open.bigmodel.cn/)
- [GLM image generation endpoint](https://open.bigmodel.cn/api/paas/v4/images/generations)
- [Ancient-method fumigation winter reference](https://mp.weixin.qq.com/s/rVBzz5YQbY-yr4rt-vmCtQ)
- [Ancient-method fumigation spring reference](https://mp.weixin.qq.com/s/m0sYk6cnRsro0yWqWPSCbg)
- [Holiday notice reference](https://mp.weixin.qq.com/s/2PyLUYX0iQUvjoJvvrKIuQ)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown article drafts with image references, file paths, setup guidance, and optional shell commands for image generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create article files under an output directory and image assets when the user enables image generation.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

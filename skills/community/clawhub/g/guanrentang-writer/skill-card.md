## Description: <br>
Guanrentang Writer generates Chinese-medicine WeChat article drafts with optional AI-generated illustrations, supporting random topics and fixed themes such as traditional fumigation promotion and holiday notices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengxiaodong28](https://clawhub.ai/user/fengxiaodong28) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinic operators, content creators, or agents preparing Guanrentang-style public-account content use this skill to draft Chinese-medicine wellness posts, add markdown image placeholders, generate supporting images through Zhipu GLM-Image, and save the finished article package locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and generation requests may be sent to Zhipu when illustration generation is enabled. <br>
Mitigation: Configure a dedicated ZHIPU_API_KEY, avoid including sensitive information in image prompts, and use article-only drafting when external image generation is not desired. <br>
Risk: Generated Chinese-medicine wellness content may be incomplete, misleading, or unsuitable for publication without review. <br>
Mitigation: Review health-related claims, contraindications, and clinic-specific details before publishing the article. <br>
Risk: The skill writes markdown and image files to a local output directory. <br>
Mitigation: Use a dedicated output folder and keep any .env file containing API credentials private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengxiaodong28/guanrentang-writer) <br>
- [Zhipu Open Platform](https://open.bigmodel.cn/) <br>
- [Zhipu image generation endpoint](https://open.bigmodel.cn/api/paas/v4/images/generations) <br>
- [Traditional fumigation reference, winter edition](https://mp.weixin.qq.com/s/rVBzz5YQbY-yr4rt-vmCtQ) <br>
- [Traditional fumigation reference, spring edition](https://mp.weixin.qq.com/s/m0sYk6cnRsro0yWqWPSCbg) <br>
- [Holiday notice reference, Spring Festival edition](https://mp.weixin.qq.com/s/2PyLUYX0iQUvjoJvvrKIuQ) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown article files with local image assets and progress/status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write to a user-selected output directory, copy fixed assets, call Zhipu GLM-Image when a ZHIPU_API_KEY is configured, and skip image generation when the user requests article-only drafting.] <br>

## Skill Version(s): <br>
1.4.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Create vertical reveal shorts: polished product vs harsh origin, one-line verdict, timed English captions (WeryAI). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent users use this skill to generate short-form vertical videos that contrast an everyday product with its origin, supply-chain cost, or source environment. The skill expands a topic or product image into a timed four-beat prompt, asks for confirmation, and submits approved jobs to WeryAI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends approved prompts and public image URLs to WeryAI for paid video generation. <br>
Mitigation: Review the expanded prompt before confirming, avoid confidential or proprietary inputs, and use the skill only when WeryAI processing is acceptable. <br>
Risk: The WERYAI_API_KEY is a paid credential used for generation and status requests. <br>
Mitigation: Use a revocable or quota-limited API key, keep it out of source control, and rotate it if exposed. <br>
Risk: Generated supply-chain contrast videos may imply claims that the skill does not fact-check. <br>
Mitigation: Review factual claims and soften sensitive prompts before submission; the skill is for opinion-style hooks, not journalism verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/hidden-truth-reveal-video-gen) <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>
- [WeryAI video task API host](https://api.weryai.com) <br>
- [WeryAI model registry API host](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown confirmation with expanded prompt details, CLI command guidance, and a final video link or clear error.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access, and WeryAI credits; sends approved prompts and public image URLs to WeryAI.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

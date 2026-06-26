## Description: <br>
Use Lingzao creator-content tools for Xiaohongshu/XHS, Douyin, and WeChat official-account public content, including note search, creator search, profile lookup, recent posts, deep profile copy/subtitle analysis, note/article detail, post comments, article stats, related articles, short-video copy extraction, and prompt-based creator image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[itxiaohao](https://clawhub.ai/user/itxiaohao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, operators, and agents use Lingzao to research public creator content, inspect public accounts and posts, prepare Xiaohongshu/Douyin/WeChat content workflows, and generate creator image assets when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use paid Lingzao credits for public-content lookup and image generation. <br>
Mitigation: Review credit prompts and API-key setup before use, and approve expanded searches or generation requests only when they match the current task. <br>
Risk: Local API keys, credentials, or reference-image paths could be used if provided during a request. <br>
Mitigation: Provide only the Lingzao API key and local files intended for the current request; do not supply unrelated private credentials or paths. <br>
Risk: The skill includes an update-check command and local configuration flow. <br>
Mitigation: Review the update command and configuration steps before deployment, especially in managed or shared agent environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/itxiaohao/skills/lingzao) <br>
- [Lingzao dashboard and setup hub](https://lingzao.atian.vip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown by default, JSON when requested, shell commands for tool use and setup, and local image files when generation is requested with an output path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses LINGZAO_API_KEY for paid public-content lookups and optional image generation; generated images are saved only when an output path is provided.] <br>

## Skill Version(s): <br>
0.1.65 (source: release evidence and artifact/VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

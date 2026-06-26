## Description: <br>
Publish blog posts from AI agents to WordPress via Notion. One API call handles page creation, markdown conversion, image uploads, featured image generation, and SEO metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kfuras](https://clawhub.ai/user/kfuras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and content automation teams use this skill to create, update, publish, and monitor WordPress posts through Notion-backed Notipo CLI and API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or delete live content in connected WordPress and Notion environments. <br>
Mitigation: Use draft, list, and review commands first, and require explicit confirmation before publish or delete actions. <br>
Risk: Credentials may allow broader publishing access than the current task requires. <br>
Mitigation: Provide API credentials limited to the specific site or workspace the agent should manage. <br>


## Reference(s): <br>
- [Notipo API documentation](https://notipo.com/docs/api/introduction) <br>
- [Notipo CLI documentation](https://notipo.com/docs/api/cli) <br>
- [Notipo npm package](https://www.npmjs.com/package/notipo) <br>
- [ClawHub skill page](https://clawhub.ai/kfuras/notipo) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires NOTIPO_URL and NOTIPO_API_KEY; publish and delete commands can affect live Notion and WordPress content.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

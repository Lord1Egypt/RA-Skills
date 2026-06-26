## Description: <br>
Use when the user needs marketing deliverables such as campaign plans, Xiaohongshu notes, audience positioning, selling-point refinement, reference-grounded copy, or marketing images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinshimeng18](https://clawhub.ai/user/qinshimeng18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, content, and growth teams use this skill to turn product or brand context into concrete marketing deliverables, including campaign plans, Xiaohongshu notes, positioning, selling-point refinements, and image-backed content. It supports continued iteration through a JustAI conversation result workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Completing login can store a JustAI API key in plaintext local config and shell startup files. <br>
Mitigation: Install only when the publisher and JustAI are trusted, review where credentials are stored, and remove the persisted config or shell exports when access is no longer needed. <br>
Risk: Marketing prompts, brand materials, project names, and generated outputs are sent to JustAI services during generation. <br>
Mitigation: Avoid submitting sensitive brand or customer data unless the user has approved sharing it with JustAI under the applicable terms. <br>
Risk: Long-running note or image generation may still be in progress when polling times out. <br>
Mitigation: Treat running status and polling timeouts as incomplete work, then poll again instead of fabricating final copy, image descriptions, or image links. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/qinshimeng18/market-kit-skills) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/qinshimeng18) <br>
- [JustAI Marketing Result Portal](https://justailab.com/marketing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON results from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Completed results can include structured campaign or note content, image links, a conversation_id for follow-up, and a web_url for viewing the result.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

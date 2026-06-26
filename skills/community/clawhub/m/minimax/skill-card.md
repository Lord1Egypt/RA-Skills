## Description: <br>
Build with MiniMax text, speech, video, and music APIs using model routing, compatible SDKs, and safer multimodal workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route MiniMax text, speech, video, music, and MCP-assisted workflows to the right interface, model tier, and execution pattern. It is intended for operational API work where exact model choice, media consent, cost boundaries, polling, and reproducible run notes matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, generation parameters, and approved media may be sent to MiniMax API endpoints. <br>
Mitigation: Use a scoped MiniMax API key where possible, review prompts and media before upload, and send only payloads needed for the requested workflow. <br>
Risk: Private media, voice references, lyrics, brand assets, or likenesses can create consent and rights concerns. <br>
Mitigation: Require explicit user approval and rights confirmation before uploads, voice imitation, cloning, or media transformation. <br>
Risk: Video, music, and other long-running generation jobs can consume paid remote compute. <br>
Mitigation: Confirm cost and duration boundaries before launch, use bounded polling, and avoid hidden rerun loops. <br>
Risk: Remote MCP hosts can expand data and tool access beyond the local MiniMax workflow. <br>
Mitigation: Enable remote MCP only after the user approves the host, readable data scope, writable actions, and rejection reasons. <br>
Risk: Durable operating notes under ~/minimax/ may retain workflow preferences, defaults, and incident notes. <br>
Mitigation: Create or update local memory only after user consent and store workflow facts rather than full prompts, assets, or chat transcripts. <br>


## Reference(s): <br>
- [ClawHub MiniMax release page](https://clawhub.ai/ivangdavila/minimax) <br>
- [MiniMax skill homepage](https://clawic.com/skills/minimax) <br>
- [Official MiniMax documentation](https://platform.minimax.io/docs) <br>
- [MiniMax API endpoint](https://api.minimax.io) <br>
- [MiniMax lower-TTFA speech endpoint](https://api-uw.minimax.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration paths, API examples, and short code or JSON payload snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local notes under ~/minimax/ after user approval and may describe bounded polling or retry behavior for queued media jobs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

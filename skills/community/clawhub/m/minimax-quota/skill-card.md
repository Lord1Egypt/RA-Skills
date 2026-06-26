## Description: <br>
MiniMax Token Plan quota query tool for checking MiniMax API usage, remaining quota, and reset timing across M2.7 text, image-01 image, Hailuo video, music-2.5 music, and speech models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API operators use this skill to check MiniMax Token Plan usage, remaining quota, and reset windows from a provided MiniMax API key. It is most relevant when a user asks about MiniMax quota, Token Plan balance, or model usage limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a MiniMax API key as a bearer token to the MiniMax quota endpoint. <br>
Mitigation: Use MINIMAX_API_KEY from a trusted environment or secret store and allow the network call only for MiniMax quota requests. <br>
Risk: Passing the API key on the command line may expose it through shell history or process listings. <br>
Mitigation: Prefer the documented environment variable flow instead of command-line arguments. <br>


## Reference(s): <br>
- [MiniMax quota remains endpoint](https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains) <br>
- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/minimax-quota) <br>
- [Publisher profile](https://clawhub.ai/user/hongjiahao371-pixel) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided MiniMax API key, preferably from MINIMAX_API_KEY or a trusted secret store.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

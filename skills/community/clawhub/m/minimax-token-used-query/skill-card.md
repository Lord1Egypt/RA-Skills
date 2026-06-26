## Description: <br>
Queries MiniMax Coding Plan token usage, reset timing, and quota information by automating a local Chrome browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljzxzxl](https://clawhub.ai/user/ljzxzxl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and MiniMax Coding Plan users use this skill to check current token usage, remaining reset time, and quota details before continuing work that depends on available MiniMax capacity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a real local Chrome Default profile and can interact with the user's MiniMax account. <br>
Mitigation: Run it only in a dedicated browser profile or environment where browser session access is acceptable. <br>
Risk: The skill can store or reuse MiniMax login credentials in a plaintext local memory file. <br>
Mitigation: Avoid saving passwords in the workspace, remove minimax-login.txt if created, and rotate credentials if they were stored unexpectedly. <br>
Risk: The skill may leave a token-usage screenshot at /tmp/minimax-token-query.png. <br>
Mitigation: Delete the screenshot after use if it contains sensitive account or quota information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljzxzxl/minimax-token-used-query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Console text with structured JSON fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open and operate a local Chrome Default profile and may save a screenshot to /tmp/minimax-token-query.png.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

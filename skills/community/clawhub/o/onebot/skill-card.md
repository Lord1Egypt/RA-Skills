## Description: <br>
Through the OneBot HTTP API, this skill helps generate local curl commands to send QQ private or group messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jqllxew](https://clawhub.ai/user/jqllxew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare OneBot/NapCat HTTP API curl commands for sending QQ private messages or group notifications after confirming the recipient, message body, endpoint, and token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A QQ message could be prepared for the wrong recipient or group. <br>
Mitigation: Require explicit confirmation of the recipient or group ID, message body, endpoint, and token before any send. <br>
Risk: Example or reused authorization tokens could expose or misuse a OneBot/NapCat service. <br>
Mitigation: Do not reuse the example token; ask the user for the correct token only when authorization is needed. <br>
Risk: Endpoint discovery could expand into unrelated Docker or local network inspection. <br>
Mitigation: Limit checks to the user-approved OneBot/NapCat endpoint and avoid inspecting unrelated local services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jqllxew/onebot) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OneBot HTTP API curl command text; execution should remain user-confirmed.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

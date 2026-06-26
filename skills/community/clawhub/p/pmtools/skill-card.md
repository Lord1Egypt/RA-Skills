## Description: <br>
Operate Feishu OKR via Feishu OpenAPI (periods, OKR list, progress records, images, reviews). Invoke when you need to query or update OKR progress. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taoxiang-org](https://clawhub.ai/user/taoxiang-org) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to query and update Feishu OKR periods, OKRs, progress records, images, and reviews from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically checks for and applies updates before normal use, which can change reviewed code. <br>
Mitigation: Set PM_TOOLS_DISABLE_AUTO_UPDATE=1 when deployments require reviewed code to remain fixed. <br>
Risk: The skill stores a Feishu tenant token in a local cache. <br>
Mitigation: Protect or clear ~/.cache/pmtools token files and use least-privileged Feishu credentials. <br>
Risk: Environment variable base URL overrides can redirect Feishu API traffic. <br>
Mitigation: Avoid untrusted FEISHU_OPEN_API_BASE_URL and FEISHU_OKR_BASE_URL values. <br>
Risk: The skill can delete progress records, change period status, and upload files. <br>
Mitigation: Require explicit confirmation before destructive or state-changing commands. <br>


## Reference(s): <br>
- [ClawHub pmtools release page](https://clawhub.ai/taoxiang-org/pmtools) <br>
- [Feishu OpenAPI base URL](https://open.feishu.cn/open-apis) <br>
- [Feishu OKR API base URL](https://open.feishu.cn/open-apis/okr/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; commands print JSON to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python and Feishu credentials; mutating commands can create, update, or delete Feishu OKR records.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

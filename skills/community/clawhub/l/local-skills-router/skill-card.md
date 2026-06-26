## Description: <br>
Routes an agent to the most appropriate local downstream skill when a request may match overlapping skill clusters such as ACP/ACPX, Lark, WeChat, Xiaohongshu, or OpenCLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to choose the right local skill before executing tasks that overlap multiple specialized skill clusters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A downstream skill selected by the router may perform user-impacting actions such as posting content, logging into accounts, harness delegation, or CLI access. <br>
Mitigation: Review the selected downstream skill before allowing those actions because that separate skill determines the actual permissions and user impact. <br>


## Reference(s): <br>
- [Local Skills Router on ClawHub](https://clawhub.ai/chaoyang78/local-skills-router) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown routing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Selects a downstream skill; does not execute code or access data itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Use the Jules REST API (v1alpha) via curl to list sources, create sessions, monitor activities, approve plans, send messages, and retrieve outputs such as pull request URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SanJacob99](https://clawhub.ai/user/SanJacob99) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding tasks to Jules through the REST API, monitor session activity, approve plans, send follow-up instructions, and retrieve outputs such as pull request links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The shell wrapper can execute local Python code if crafted prompt, title, source, or branch values are interpolated into its JSON escaping blocks. <br>
Mitigation: Avoid passing untrusted task text or repository values into scripts/jules_api.sh until the wrapper passes values as data rather than interpolating them into Python code. <br>
Risk: The skill requires a Jules API key and can operate on connected GitHub repositories. <br>
Mitigation: Keep JULES_API_KEY protected, rotate it when needed, and grant Jules access only to repositories intended for this workflow. <br>
Risk: Jules sessions can execute coding tasks and create pull requests in connected repositories. <br>
Mitigation: Use plan approval for normal work, inspect Jules activity before approval, and review generated pull requests before merging. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SanJacob99/jules-and-lobster) <br>
- [Jules API documentation](https://jules.google/docs/api/reference/overview/) <br>
- [Jules Sessions reference](https://jules.google/docs/api/reference/sessions/) <br>
- [Jules Activities reference](https://jules.google/docs/api/reference/activities/) <br>
- [Jules Sources reference](https://jules.google/docs/api/reference/sources/) <br>
- [Google Developers Jules API](https://developers.google.com/jules/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON API responses from Jules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires JULES_API_KEY and can create or modify Jules sessions for connected GitHub repositories.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

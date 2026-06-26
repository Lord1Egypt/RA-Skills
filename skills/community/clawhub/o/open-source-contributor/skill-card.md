## Description: <br>
Autonomous GitHub contribution agent that scouts suitable issues, implements fixes with an Architect-Builder workflow, and submits pull requests under the user's GitHub identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahajahmed010](https://clawhub.ai/user/wahajahmed010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to automate small open-source contribution workflows, including finding candidate GitHub issues, preparing changes, running validation, and opening pull requests with AI disclosure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act on GitHub under the user's identity, including forking repositories, pushing branches, and opening public pull requests. <br>
Mitigation: Use a dedicated low-privilege public_repo token, begin with dry runs or human review, and monitor all PRs before enabling full autonomy. <br>
Risk: Credential handling is flagged as unsafe by the security evidence. <br>
Mitigation: Inspect or replace the token_resolver dependency, avoid tokens in command strings, and fix shell=True usage before relying on the automation. <br>
Risk: Automated contributions can create low-quality or unwanted public changes under the user's account. <br>
Mitigation: Use the documented complexity limits, approval thresholds, test validation, auto-pause behavior, and manual review for initial runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wahajahmed010/open-source-contributor) <br>
- [Publisher profile](https://clawhub.ai/user/wahajahmed010) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with code changes, shell commands, configuration JSON, and pull request text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GitHub credentials and can create public commits and pull requests under the user's identity.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release evidence and install.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

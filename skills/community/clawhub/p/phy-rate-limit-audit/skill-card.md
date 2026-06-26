## Description: <br>
Phy Rate Limit Audit helps developers and security engineers find missing or overly permissive API rate limits across common web frameworks and produce remediation-oriented findings for local review or CI gating. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit API codebases for missing rate limits, exposed high-risk endpoints, retry loops without backoff, and related resource-consumption issues. It is intended for local static review and CI fail-gate workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads source files from the path supplied by the installer. <br>
Mitigation: Run it only against intended local directories and confirm the local script was copied from reviewed skill content or another trusted source before execution. <br>
Risk: Heuristic static checks can produce false positives when middleware, guards, or circuit breakers are registered outside the local detection window. <br>
Mitigation: Treat findings as review prompts and confirm actual route-level or global protections before making code changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-rate-limit-audit) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and terminal-style text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include severity-filtered findings and CI fail-gate commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description:

Monitor Minimax Coding Plan usage to stay within API limits. Fetches current usage stats and provides status alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesethrose](https://clawhub.ai/user/thesethrose)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to check Minimax Coding Plan consumption, remaining prompt capacity, and reset timing before continuing API-backed coding work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script loads a parent-directory .env file as shell code, which can execute unintended commands or expose credentials if that file is unsafe.

Mitigation: Review before installing, fix the .env path to match the documented local file, and load credentials as data rather than executable shell code.

## Reference(s):

- [Minimax Usage Skill Page](https://clawhub.ai/thesethrose/skills/minimax-usage)
- [Publisher Profile](https://clawhub.ai/user/thesethrose)
- [Minimax Basic Information](https://platform.minimax.io/user-center/basic-information)
- [Minimax Coding Plan Remains API](https://platform.minimax.io/v1/api/openplatform/coding_plan/remains?GroupId={GROUP_ID})
- [Minimax Coding Plan Payment Page](https://platform.minimax.io/user-center/payment/coding-plan)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and terminal output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports current usage, remaining prompts, reset timing, and status alerts from the Minimax Coding Plan API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

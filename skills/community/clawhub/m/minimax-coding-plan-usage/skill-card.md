## Description:

Monitor Minimax Coding Plan usage to stay within API limits by fetching current usage statistics and providing status alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[franky0617](https://clawhub.ai/user/franky0617)

### License/Terms of Use:


## Use Case:

Developers and Minimax Coding Plan users use this skill to check remaining prompt quota, reset timing, and usage status before continuing API-backed coding work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script sources a parent .env file, which can execute shell content or load unrelated secrets from that file.

Mitigation: Fix the script to read only the intended local configuration file without shell source, or require MINIMAX_CODING_API_KEY and MINIMAX_GROUP_ID from the existing environment.

Risk: Running the script from a directory with an untrusted parent .env file can expose the user to unintended command execution.

Mitigation: Run only from a trusted installation path after inspecting the resolved .env file path and its contents.

Risk: The skill requires a Minimax Coding Plan API key and Group ID to call the Minimax usage endpoint.

Mitigation: Use only the dedicated Coding Plan API key described by the skill, keep credentials out of shared logs, and rotate credentials if exposure is suspected.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/franky0617/skills/minimax-coding-plan-usage)
- [ClawHub publisher profile](https://clawhub.ai/user/franky0617)
- [Minimax basic information page](https://platform.minimax.com/user-center/basic-information)
- [Minimax Coding Plan payment page](https://platform.minimax.com/user-center/payment/coding-plan)
- [Minimax Coding Plan remains API endpoint](https://platform.minimax.com/v1/api/openplatform/coding_plan/remains?GroupId={GROUP_ID})

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text output with usage counts, remaining quota, reset countdown, and status alert.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on live Minimax API availability, jq, curl, and configured MINIMAX_CODING_API_KEY and MINIMAX_GROUP_ID values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

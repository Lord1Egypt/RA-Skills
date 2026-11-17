## Description:

Autonomous Nigerian Airtime distribution agent on Farcaster.

This skill is ready for commercial/non-commercial use.

## Publisher:

[druxamb](https://clawhub.ai/user/druxamb)

### License/Terms of Use:


## Use Case:

External users and operators use OpenAirtime to run a Farcaster workflow for Nigerian airtime claims, including replies, claim-code collection, and user status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on local scripts with configured credentials to post on Farcaster and process airtime claims.

Mitigation: Install only after verifying the referenced scripts and updates, and run them with least-privilege access to the Farcaster account and airtime workflow.

Risk: Airtime claims use claim codes and phone numbers, creating privacy and misuse risks.

Mitigation: Add strict input validation and clear handling rules for phone numbers and claim codes before operational use.

Risk: Airtime distribution can create unintended spend if claims are automated without controls.

Mitigation: Use budget limits or explicit approval controls for claim execution.

## Reference(s):

- [OpenAirtime skill page](https://clawhub.ai/druxamb/skills/open-airtime)
- [DruxAMB publisher profile](https://clawhub.ai/user/druxamb)
- [OpenAirtime claim site](https://openairtime.fun)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown instructions with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and configured local Farcaster and airtime scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

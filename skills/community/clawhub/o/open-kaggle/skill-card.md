## Description:

Open Kaggle in the user's Brave browser and take the user to the Kaggle homepage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to open Kaggle in Brave, reuse an existing Kaggle tab or browser session when possible, and verify that the homepage loaded successfully.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening or reusing Kaggle in Brave can expose the user's existing signed-in browser session.

Mitigation: Use the skill only when the user asks to open Kaggle, limit activity to loading and verifying the homepage, and do not change account or content data.

Risk: Authentication may be required to continue after the page opens.

Mitigation: Stop at the login page and let the user sign in directly; do not collect, enter, or store passwords, authentication codes, API keys, or other credentials.

## Reference(s):

- [Kaggle homepage](https://www.kaggle.com/)
- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-kaggle)
- [Publisher profile](https://clawhub.ai/user/ruchir17-cmd)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Text status with browser automation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Opens or reuses one Brave tab for the Kaggle homepage and stops at login if authentication is required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

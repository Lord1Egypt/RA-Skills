## Description:

Search and read Meituan travel information through the user's OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can query Meituan Travel for flights, trains, hotels, attractions, itineraries, local transportation, and other travel information using natural language. The skill uses the user's connected Meituan account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup includes downloaded CLI installers that the security evidence says were not inspected.

Mitigation: Review the setup steps, install a pinned and verified CLI release yourself, and require approval for later installation changes. Check the CLI's automatic skill synchronization settings.

Risk: Meituan requests use the connected OOMOL account and may consume credit.

Mitigation: Check the account's credit and billing before making requests.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Meituan](https://www.meituan.com)
- [Meituan skill release](https://clawhub.ai/oomol/skills/oo-meituan)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance, Shell commands]

**Output Format:** [Natural-language query instructions, shell command examples, and connector response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Travel query responses depend on the connected Meituan account and the live connector schema; requests may take up to two minutes.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Merriam-Webster Collegiate (merriam-webster.com). Use this skill for ANY Merriam-Webster Collegiate request — searching and reading data. Whenever a task involves Merriam-Webster Collegiate, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to look up words in Merriam-Webster Collegiate and retrieve matching dictionary entries or spelling suggestions through the user's connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path downloads and runs an installer whose exact behavior has not been verified.

Mitigation: Review the CLI and installer separately before installation, and require user approval before running setup commands.

Risk: Automatic skill synchronization during setup may make broader agent changes than the dictionary lookup requires.

Mitigation: Check the synchronization behavior and disable it if it is unwanted.

Risk: The connected OOMOL account may have permissions or charges that affect use of this skill.

Mitigation: Confirm the account permissions and applicable charges before use.

## Reference(s):

- [Merriam-Webster Collegiate Dictionary](https://www.merriam-webster.com)
- [Merriam-Webster Collegiate Dictionary API documentation](https://dictionaryapi.com/products/api-collegiate-dictionary)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Dictionary entry data or spelling suggestions returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Merriam-Webster Collegiate account and the requested word.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

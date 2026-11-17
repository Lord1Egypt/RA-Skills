## Description:

This skill helps agents download files, folders, or entire repositories from GitHub URLs using the gitload CLI without cloning full git history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waldekmastykarz](https://clawhub.ai/user/waldekmastykarz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch GitHub files, folders, repository snapshots, or ZIP archives without cloning full history, including authenticated access for private repositories or rate-limit handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable third-party npm code through npx or a global install.

Mitigation: Review the npm package before execution, pin or verify package versions where possible, and inspect downloaded package.json files before running npm install.

Risk: Authentication examples include personal access tokens and a GITHUB_TOKEN environment variable.

Mitigation: Prefer GitHub CLI authentication, avoid placing real tokens directly in commands, and use least-privilege short-lived tokens.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command options, authentication patterns, URL formats, and troubleshooting guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

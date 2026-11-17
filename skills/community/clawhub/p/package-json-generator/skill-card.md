## Description:

Generates a starter package.json manifest with common npm scripts and basic project metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunshine-del-ux](https://clawhub.ai/user/sunshine-del-ux)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to create a starter npm package manifest for Node.js projects. Review the generated package.json before installing dependencies or running npm scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell script can overwrite an existing package.json file.

Mitigation: Run it only in a disposable or empty project directory, or back up any existing manifest before use.

Risk: The script writes provided names and versions into JSON without escaping.

Mitigation: Do not pass untrusted values, and inspect the generated manifest before running npm install or npm scripts.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated JSON configuration content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a package.json template using the provided project name and version.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

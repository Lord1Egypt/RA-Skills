## Description:

grazy provides Graz city information through a CLI, including public transport, weather, air quality, news, events, and POI search without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomyg](https://clawhub.ai/user/thomyg)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve current Graz city information by proposing or running grazy CLI commands for transit, weather, air quality, news, events, and points of interest.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed artifact invokes an unpinned third-party npm package, so the executable code may change independently of the skill.

Mitigation: Install a pinned, reviewed @grazy/cli version and avoid unversioned npx execution.

Risk: Global npm installation or execution in a sensitive workspace could expose local files or credentials to third-party code.

Mitigation: Run the CLI in an isolated project or sandbox without sensitive files, secrets, or broad filesystem access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thomyg/skills/grazy)
- [grazy GitHub repository](https://github.com/thomyg/grazy)
- [grazy npm package](https://www.npmjs.com/package/@grazy/cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may describe live city data returned by the third-party grazy CLI.]

## Skill Version(s):

0.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

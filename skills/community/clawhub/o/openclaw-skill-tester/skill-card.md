## Description:

OpenClaw Skill Tester helps agents test OpenClaw skills by checking trigger behavior, functional outputs, comparison metrics, and generated reports.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[cry779](https://clawhub.ai/user/cry779)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to exercise OpenClaw skill trigger checks, functionality checks, comparison metrics, and test-report generation. Security evidence says its bundled checks are mostly simulated or fixed, so it should not be treated as a trustworthy CI or release gate without additional validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled tests may produce misleading reports because security evidence says the checks are mostly simulated or fixed.

Mitigation: Require real skill execution, failure propagation, and report totals derived from actual results before using this skill in CI or release decisions.

Risk: Report generation may expose or confuse results if skill names and report storage are not controlled.

Mitigation: Sanitize skill names and use a private report directory before installing or running the skill in shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cry779/skills/openclaw-skill-tester)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and generated JSON, HTML, or Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and bash; OpenClaw metadata lists pytest and requests as package requirements.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

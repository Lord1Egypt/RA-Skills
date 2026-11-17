## Description:

Nutrition Claw is a local nutrition tracking CLI for agents and humans that logs meals and foods, manages goals, searches local history semantically, and emits YAML output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pita](https://clawhub.ai/user/pita)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to track nutrition locally, maintain personal goals and food libraries, log meals and ingredients, and retrieve summaries or history without cloud storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive nutrition and body-goal data is stored locally in plain files under ~/.nutrition-claw.

Mitigation: Run the skill only on trusted accounts or machines, and protect the local data directory with normal user-level file permissions.

Risk: The security scan reports a verified bug that can read or overwrite JSON files outside the intended log folder when dates are untrusted.

Mitigation: Validate date inputs as strict YYYY-MM-DD values from trusted sources before automated use, and review date path handling before shared or unattended deployment.

Risk: The release installs npm dependencies without a reviewed lockfile.

Mitigation: Review and pin the dependency tree with a lockfile before installing in managed or shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pita/skills/nutrition-claw)
- [Publisher profile](https://clawhub.ai/user/pita)
- [OpenClaw](https://openclaw.ai)
- [GitHub Packages install page](https://github.com/Pita/nutrition-claw/pkgs/npm/nutrition-claw)
- [Bun](https://bun.sh)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and YAML command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores nutrition goals, food data, meal logs, vector indexes, and education history locally under ~/.nutrition-claw as plain files.]

## Skill Version(s):

1.0.9 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

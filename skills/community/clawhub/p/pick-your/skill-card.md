## Description:

Generates multi-themed food collages (Burgers, Pizzas, Sushi, Salads, Desserts) with circle-masked images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[expysf98](https://clawhub.ai/user/expysf98)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to generate curated 3x3 food-choice collages for burgers, pizzas, sushi, salads, and desserts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes an undeclared Cloudflare image-generation script with an exposed token.

Mitigation: Remove the unrelated script or replace embedded credentials with documented user-provided configuration, and revoke the exposed token before use.

Risk: The undeclared image-generation script uses shell command handling that can increase command-injection risk.

Mitigation: Do not run the script as packaged; require a rewritten implementation that avoids shell execution and is reviewed before installation.

Risk: The package security verdict is suspicious.

Mitigation: Install only after review, run with least privilege during testing, and rely on the narrow local collage script only if the package contents are cleaned.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration]

**Output Format:** [Markdown guidance with shell commands and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The main collage script writes one PNG file per predefined food theme.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Checks KiCad projects and standalone BOM CSVs for schematic/PCB mismatches, BOM errors, and offline part-risk flags before board fabrication or parts orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raktikoo](https://clawhub.ai/user/raktikoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and electronics engineers use KiCad Preflight to check project files or standalone BOM CSVs before exporting Gerbers or ordering parts. It reports consistency, BOM, and offline part-risk findings for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing from a Git URL carries supply-chain risk, and the security review was partial because a referenced local path was missing.

Mitigation: Review the source and pin installation to a reviewed commit or vetted package. Run it in an isolated environment without sensitive credentials.

## Reference(s):

- [GitHub install source listed by the skill](https://github.com/RakTikoo/kicad-preflight)
- [ClawHub skill page](https://clawhub.ai/raktikoo/skills/kicad-preflight)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, SARIF]

**Output Format:** [Plain-text, JSON, Markdown, or SARIF report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes PASS, CAUTION, or BLOCK verdicts, findings, and scan coverage details.]

## Skill Version(s):

0.7.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

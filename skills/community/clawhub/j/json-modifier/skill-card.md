## Description:

Safely apply structured JSON patches (RFC 6902) to files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:

ISC

## Use Case:

Developers and engineers use this skill to apply precise JSON Patch operations to configuration files, package manifests, and other JSON documents without rewriting full files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patch input can overwrite any JSON file selected by the user.

Mitigation: Review patch operations and target paths before applying them, and prefer --out when testing changes.

Risk: Dependency ranges and the test script may be unsuitable for sensitive CI automation without review.

Mitigation: Pin dependencies exactly and harden CI test execution before using this skill in protected automation.

## Reference(s):

- [JSON Patch reference](https://jsonpatch.com/)
- [ClawHub skill page](https://clawhub.ai/wanng-ide/skills/json-modifier)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration]

**Output Format:** [JSON patches and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can modify a target JSON file in place or write the patched document to a separate output file.]

## Skill Version(s):

1.0.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

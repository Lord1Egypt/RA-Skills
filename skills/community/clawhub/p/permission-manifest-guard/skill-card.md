## Description:

Inspects an OpenClaw skill directory before install or execution, translates declared and observed requirements into a human-readable permission manifest, and recommends disposition when metadata does not match observed behaviour.

This skill is ready for commercial/non-commercial use.

## Publisher:

[honouralexwill](https://clawhub.ai/user/honouralexwill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to inspect OpenClaw skill directories before install or execution, compare declared metadata with observed permission-relevant behavior, and decide whether to allow, review, sandbox, or reject a skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can write through target-controlled symlinks when writing its JSON manifest.

Mitigation: Install or run only in a low-privilege environment and avoid pointing the CLI at untrusted directories until symlink-safe output handling is fixed.

Risk: Scanner coverage can miss executable code hidden by target-controlled ignore rules.

Mitigation: Treat generated recommendations as advisory and manually review packages with dist directories, package entry points, or custom ignore files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/honouralexwill/skills/permission-manifest-guard)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Markdown permission report with a structured JSON manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI output includes a markdown report and writes permission-manifest.json into the target skill directory; the programmatic API returns the markdown, JSON, and diagnostics in memory.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter and package.json report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

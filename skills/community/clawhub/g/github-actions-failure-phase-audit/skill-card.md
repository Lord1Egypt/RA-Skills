## Description:

Group GitHub Actions failures by pipeline phase (setup/build/test/lint/deploy/security) with minute impact to prioritize fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daniellummis](https://clawhub.ai/user/daniellummis)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to analyze exported GitHub Actions workflow-run JSON and identify failure hotspots by CI/CD phase, wasted minutes, and failure count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads GitHub Actions JSON exports that may contain private repository names, branches, URLs, or job metadata.

Mitigation: Scope RUN_GLOB to the intended workflow-run export files and avoid broad matches over directories that contain unrelated sensitive data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks, plus text or JSON reports from the audit script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can be filtered by repository, branch, workflow, and phase; critical hotspots can optionally fail the command.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

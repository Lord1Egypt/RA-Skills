## Description:

Recommend suitable high-impact factor or domain-specific journals for manuscript submission based on abstract content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT

## Use Case:

Researchers, manuscript authors, and research-support teams use this skill to analyze an abstract and generate journal recommendations based on field detection, scope alignment, impact factor filters, and ranking criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill executes local Python code and reads abstract input from either command-line text or a user-selected file.

Mitigation: Install and run it only in an environment suitable for local Python execution, and use file input only for abstracts intentionally selected for analysis.

Risk: Dependency hygiene issues may affect installation or compatibility.

Mitigation: Review dependencies before installation and prefer removing or pinning the dataclasses dependency when appropriate.

Risk: Private or credential-containing files could be analyzed if intentionally passed through the file option.

Mitigation: Do not pass arbitrary private files or files containing credentials as abstract input.

## Reference(s):

- [Journal database](references/journals.json)
- [Research field classifications](references/fields.json)
- [Scoring weights](references/scoring_weights.json)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/journal-matchmaker)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Plain text table, JSON, or Markdown recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations include ranked journals, impact factors, relevance scores, open-access status, publishers, scopes, and match reasons when available.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

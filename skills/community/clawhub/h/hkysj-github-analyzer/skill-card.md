## Description:

GitHub Analyzer analyzes GitHub repositories for technology stack, license compliance, deployment options, and open-source dependency due diligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hkysj](https://clawhub.ai/user/hkysj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to analyze public GitHub repositories, generate local Markdown evaluation reports, and support technology selection, license review, and deployment planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts GitHub for repositories the user asks it to analyze.

Mitigation: Use it only for repositories you are comfortable querying through GitHub's public endpoints.

Risk: Generated reports include repository descriptions and README excerpts that may contain untrusted content.

Mitigation: Review report content before feeding it back into an AI agent or opening it in a renderer that allows active HTML.

Risk: License guidance is summarized and may not capture all obligations for a repository.

Mitigation: Confirm license terms against the repository's authoritative license text and seek legal review for business-critical use.

## Reference(s):

- [Open-source license reference](references/licenses.md)
- [GitHub repository API](https://api.github.com/repos/$REPO)
- [GitHub repository contents API](https://api.github.com/repos/$REPO/contents)
- [ClawHub skill page](https://clawhub.ai/hkysj/skills/hkysj-github-analyzer)
- [Publisher profile](https://clawhub.ai/user/hkysj)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report saved locally plus terminal summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq; contacts GitHub for the repository requested by the user.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

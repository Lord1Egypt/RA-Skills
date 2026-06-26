## Description: <br>
CLI tool to discover AI tools. Search 40+ curated tools by category, pricing, and use case. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abgohel](https://clawhub.ai/user/abgohel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, creators, and other CLI users use this skill to search an offline catalog of AI tools by keyword, category, pricing, and common use case. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Global npm installation carries ordinary third-party package supply-chain risk. <br>
Mitigation: Install only from a trusted package source, review the package and dependency versions, and prefer pinned versions in managed environments. <br>
Risk: Some declared dependencies are not used by the visible CLI code. <br>
Mitigation: Review unused dependencies before deployment and remove or pin them if maintaining an internal copy. <br>
Risk: The bundled AI tool catalog may become stale or contain outdated pricing or URLs. <br>
Mitigation: Treat results as discovery guidance and verify tool availability, terms, and pricing before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abgohel/meow-finder) <br>
- [Project Homepage](https://github.com/abgohel/meow-finder) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text CLI output with command examples in Markdown documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are read from a bundled local catalog and displayed in the terminal.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Generates consumer-facing OpenAPI/Swagger changelogs by semantically diffing local YAML or JSON specs, classifying breaking and non-breaking changes, and optionally producing migration guidance or JSON for CI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API maintainers use this skill to compare OpenAPI 3.x or Swagger 2.0 specifications, summarize breaking and non-breaking API changes, and prepare migration notes for consumers or CI review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger wording could cause the skill to run during general API design conversations. <br>
Mitigation: Invoke it with explicit spec paths or the /api-changelog command when a changelog is intended. <br>
Risk: Generated changelogs or migration guidance may misstate API compatibility impact. <br>
Mitigation: Review generated changelogs against the source specs before publishing or using them to gate releases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-api-changelog-gen) <br>
- [Publisher homepage](https://canlah.ai) <br>
- [Publisher profile](https://clawhub.ai/user/PHY041) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Guidance, Shell commands] <br>
**Output Format:** [Markdown changelog, JSON report, and migration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can focus on breaking changes, migration guidance, or CI failure behavior when requested.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

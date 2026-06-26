## Description: <br>
Provides Chinese lunar calendar queries, including solar-to-lunar conversion, lunar-to-solar conversion, almanac suitability notes, traditional festivals, zodiac stems and branches, leap-month markers, and solar-term lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hehuibiao](https://clawhub.ai/user/hehuibiao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to answer Chinese lunar calendar, almanac, zodiac, leap-month, festival, and solar-term questions with structured date output rather than relying on model memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release bundle includes GitHub publishing, token-handling, packaging, and community-promotion scripts that are broader than the lunar calendar use case. <br>
Mitigation: Review the package before installation and do not run LAUNCH_NOW.sh, github_auto_setup.sh, scripts/create_github_repo.sh, or scripts/publish.sh unless publishing behavior and token handling have been audited. <br>
Risk: Almanac and solar-term outputs may be non-authoritative, and the documentation notes that important dates should be verified against authoritative sources. <br>
Mitigation: Use the calculator output as a reference aid, validate important dates independently, and prefer a cleaned package containing only the calculator, references, and scoped install instructions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hehuibiao/lunar-calendar) <br>
- [Fortune Rules](references/fortune_rules.md) <br>
- [Solar Terms](references/solar_terms.md) <br>
- [Validation Result](validation_result.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [XML-style structured text with optional Markdown explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Date calculations are documented for 1900-2100; important dates should be cross-checked when authoritative certainty is required.] <br>

## Skill Version(s): <br>
0.9.0 (source: server release metadata, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

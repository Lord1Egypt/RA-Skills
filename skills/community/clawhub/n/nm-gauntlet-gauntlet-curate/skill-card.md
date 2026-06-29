## Description: <br>
Audits the DSA problem bank for coverage gaps and proposes new YAML entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers maintaining the Gauntlet DSA problem bank use this skill to audit category coverage against expected counts and prepare human-reviewed YAML problem proposals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated problem proposals may be incomplete or inaccurate. <br>
Mitigation: Review the proposal report and validate entries before merging any YAML changes. <br>
Risk: The analysis command expects the local Gauntlet problem-bank layout and Python script. <br>
Mitigation: Run the command only in the expected Gauntlet workspace and inspect the report before relying on it. <br>
Risk: Direct edits to hand-curated problem-bank files could bypass the intended review workflow. <br>
Mitigation: Use the skill output as a proposal report; apply accepted changes manually after human review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-gauntlet-gauntlet-curate) <br>
- [Gauntlet plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with YAML proposal snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Human review is required before any problem-bank changes.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

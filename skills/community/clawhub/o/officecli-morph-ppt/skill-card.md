## Description: <br>
Generate Morph-animated PPTs with officecli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iceyliu](https://clawhub.ai/user/iceyliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and presentation authors use this skill to plan, script, validate, and deliver PowerPoint decks with smooth Morph animations. It guides creation of a reusable build script, a brief, and a finished PPTX. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to download and run remote officecli installer or upgrade scripts. <br>
Mitigation: Require the user to install or update officecli from a trusted, pinned source and verify it before allowing the agent to use it. <br>
Risk: Generated build scripts can create or overwrite PowerPoint files in the workspace. <br>
Mitigation: Warn users before generation, use explicit output filenames, and treat build scripts as overwriting their generated PPTX outputs. <br>
Risk: PowerPoint Morph output can contain visual defects such as unghosted content, missing transitions, or unreadable text. <br>
Mitigation: Run the bundled verification helpers and final officecli validation commands before delivery. <br>


## Reference(s): <br>
- [Decision Rules](reference/decision-rules.md) <br>
- [OfficeCLI PPT Command Reference](reference/officecli-pptx-min.md) <br>
- [PPTX Design](reference/pptx-design.md) <br>
- [Quality Gates](reference/quality-gates.md) <br>
- [Style Index](reference/styles/INDEX.md) <br>
- [OfficeCLI Agent Guide](https://github.com/iOfficeAI/OfficeCli/wiki/agent-guide) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python or shell command examples and generated presentation files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected deliverables are a PPTX deck, a re-runnable build script, and brief.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

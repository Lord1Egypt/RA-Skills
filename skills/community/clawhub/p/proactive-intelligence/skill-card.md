## Description: <br>
Proactive Intelligence helps an agent predict user needs, improve from corrections, maintain structured memory, manage skills, and support skill evolution workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cle87937-code](https://clawhub.ai/user/cle87937-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add proactive task follow-through, local long-term memory, structured learning logs, and skill health or evolution workflows to an OpenClaw-style workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory and learning logs can capture or preserve sensitive workspace context. <br>
Mitigation: Install only when long-term local memory is intended; review memory and .learnings files and remove sensitive or unwanted defaults before use. <br>
Risk: The initialization script updates workspace Markdown paths and creates state under the home directory and workspace. <br>
Mitigation: Back up workspace Markdown files before running init.py and inspect diffs after initialization. <br>
Risk: Skill evolution tools can modify installed skills and agent instruction files with loose scoping. <br>
Mitigation: Require manual diff review and explicit confirmation before applying fixes, enhancements, or changes to installed skills. <br>
Risk: Documentation references an init.ps1 path that is not present in the provided artifact. <br>
Mitigation: Use the reviewed Python init.py path unless a Windows script is supplied and reviewed separately. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cle87937-code/proactive-intelligence) <br>
- [Installation Guide](artifact/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and local file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local memory, learning-log, report, and skill files when its scripts are run.] <br>

## Skill Version(s): <br>
2.3.1 (source: artifact/SKILL.md frontmatter and evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

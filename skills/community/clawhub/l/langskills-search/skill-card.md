## Description: <br>
Searches 119K evidence-backed skills from 95K+ papers and 24K+ tech sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shatianming5](https://clawhub.ai/user/shatianming5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to find evidence-backed best practices, how-tos, and techniques from LangSkills data bundles. It is useful when answers should include source URLs or full skill bodies rather than unsupported guesses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install a third-party Python package and data bundles. <br>
Mitigation: Install only from a trusted package source, preferably in an isolated Python environment. <br>
Risk: Returned full skill bodies may contain commands or workflow guidance that are unsafe or unsuitable for the current environment. <br>
Mitigation: Treat returned skill bodies as reference material and verify commands before copying them into an agent workflow. <br>


## Reference(s): <br>
- [LangSkills source repository](https://github.com/LabRAI/LangSkills) <br>
- [LangSkills Search ClawHub release](https://clawhub.ai/shatianming5/langskills-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and CLI parameter tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include title, domain, quality score, source URL, and optional full skill body.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

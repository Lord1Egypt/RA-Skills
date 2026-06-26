## Description: <br>
Generate an instant codebase overview covering language, framework, architecture, entry points, and key files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fratua](https://clawhub.ai/user/Fratua) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to inspect a repository and produce a concise onboarding summary of its language, framework, architecture, entry points, tests, CI/CD setup, dependencies, and notable files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated summaries can expose private filenames, dependencies, CI details, or internal notes. <br>
Mitigation: Review the generated summary and remove sensitive project details before sharing it outside the workspace. <br>
Risk: The skill's project summary can be incomplete or imprecise when manifests, README files, tests, or CI configuration are missing or too large to scan fully. <br>
Mitigation: Treat the output as a concise onboarding aid and verify important architecture, dependency, test, and CI claims against the repository. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Fratua/project-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown project summary with concise tables, bullets, and inline shell commands where useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include detected project metadata, quick-start commands, key-file tables, dependency summaries, test setup, CI/CD notes, and limitations when repository evidence is incomplete.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

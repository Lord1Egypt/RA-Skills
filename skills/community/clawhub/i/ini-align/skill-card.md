## Description: <br>
INI file section and key-value alignment tool that reorders a target INI file to match a source reference while preserving target-only content and listing source-only sections as comments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imvvip](https://clawhub.ai/user/imvvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to reorder sections and key-value pairs in an INI configuration file so its structure follows a reference file while keeping target-only settings in the output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated INI output may lose comments, duplicate entries, or original formatting, which can make it unsuitable for lossless configuration migration. <br>
Mitigation: Review the generated file before using it and avoid relying on it when comments, duplicate entries, or exact formatting are required. <br>
Risk: Using the source or target path as the output path could overwrite an original configuration file. <br>
Mitigation: Choose a separate output path, such as an -aligned.ini filename, and confirm the source and target files are not used as the output destination. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples, a generated INI file, and a Markdown-style execution summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes UTF-8 INI output to a user-selected path and prints section counts plus duplicate-section warnings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Displays the first lines of files for quickly previewing file contents, checking headers, or sampling data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to preview the beginning of text files such as logs, CSVs, and configuration files without loading the full file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The beginning of a selected file may be displayed in the agent conversation, including sensitive content if the user points the skill at credentials, private records, or similar files. <br>
Mitigation: Use the skill only on files whose initial contents are acceptable to reveal, and avoid credentials, private records, and other sensitive data. <br>
Risk: Previewing very large files may still expose more content than intended if a large line count is requested. <br>
Mitigation: Keep preview sizes small and review command arguments before running the skill on large files. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text file preview with Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Displays the beginning of user-specified files or stdin; default behavior is the first 10 lines.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

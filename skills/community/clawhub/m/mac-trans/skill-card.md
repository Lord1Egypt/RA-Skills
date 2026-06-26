## Description: <br>
Helps an agent translate text, whole files, selected file lines, or target-language output using the trans command on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abcnull](https://clawhub.ai/user/abcnull) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to translate user-provided text, file contents, selected file ranges, and output into a chosen supported language from a macOS shell. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text or file contents translated through Bing or another online provider may leave the user's computer. <br>
Mitigation: Redact secrets and confidential information before translation, or use a local or offline translation option for sensitive material. <br>
Risk: The skill depends on the local trans command and translate-shell package behaving as expected. <br>
Mitigation: Install translate-shell from a trusted source and confirm the trans command resolves to the expected binary before use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use Bing or another online translation provider through translate-shell, depending on the trans command configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
List directory contents with detailed file information. Use for browsing files, checking permissions, and examining directory structure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect local directory contents, check file sizes in long format, and browse simple directory structure during workspace tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose filenames and basic file-size metadata from directories the agent is asked to inspect. <br>
Mitigation: Use it only on directories where exposing names and size metadata to the agent is acceptable. <br>
Risk: The documentation lists -a, -h, -R, and -t options, but the implementation only supports a path argument and -l. <br>
Mitigation: Rely only on the implemented path and -l behavior unless the script is updated and re-reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/ls-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text directory listings and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file names and basic file-size metadata for requested local directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

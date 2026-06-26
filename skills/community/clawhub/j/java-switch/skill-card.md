## Description: <br>
Java Switch helps agents install and switch Java versions on macOS using Homebrew, /usr/libexec/java_home, and shell environment updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LongFer](https://clawhub.ai/user/LongFer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS users use this skill to have an agent install a requested OpenJDK version, switch JAVA_HOME and PATH for the current session, and persist the Java configuration in ~/.zshrc. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Homebrew or OpenJDK on the user's machine. <br>
Mitigation: Review Homebrew prompts before approving installation and consider installing Homebrew separately if tighter control is needed. <br>
Risk: The skill can permanently change shell Java configuration by editing ~/.zshrc. <br>
Mitigation: Review the added JAVA_HOME and PATH lines after execution, especially when maintaining a custom shell profile. <br>


## Reference(s): <br>
- [Java Switch ClawHub page](https://clawhub.ai/LongFer/java-switch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and step-by-step guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute or propose local shell commands that install Homebrew/OpenJDK and edit ~/.zshrc.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

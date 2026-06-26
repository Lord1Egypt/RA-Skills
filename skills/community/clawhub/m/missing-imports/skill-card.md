## Description: <br>
Code uses a symbol that isn't imported, or imports a symbol that doesn't exist in the source module. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvogt99](https://clawhub.ai/user/mvogt99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to catch missing imports, undefined symbols, and imports of names that a module does not export before code reaches runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to inspect project files and run local static analysis tools while diagnosing import problems. <br>
Mitigation: Review proposed file reads and static-checker commands before execution, especially in repositories with sensitive source code. <br>
Risk: Incorrect import guidance can hide the real source of an undefined symbol or broken export. <br>
Mitigation: Verify imports against the same file, the target module's exports, and the project's static checker before accepting changes. <br>


## Reference(s): <br>
- [Missing Imports on ClawHub](https://clawhub.ai/mvogt99/missing-imports) <br>
- [mvogt99 publisher profile](https://clawhub.ai/user/mvogt99) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with optional static-checker commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance; no executable payload is included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Manage LuLu macOS firewall rules from the command line for diagnosing blocked connections, allowing or blocking domains, and reviewing firewall rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woop](https://clawhub.ai/user/woop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill on macOS systems to inspect LuLu firewall rules, diagnose blocked outbound connections, and propose precise allow or block rule changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose sudo-powered LuLu rule changes that affect outbound firewall behavior. <br>
Mitigation: Review every `sudo lulu-cli` command before approval and apply only intentional rule changes. <br>
Risk: Broad wildcard allow rules can weaken LuLu as a security boundary. <br>
Mitigation: Prefer narrow application, domain, and port-specific rules over global wildcards. <br>
Risk: The required `lulu-cli` binary is installed from an external Homebrew tap and is not included in the reviewed skill artifacts. <br>
Mitigation: Verify the Homebrew tap and installed binary before relying on the skill. <br>
Risk: Reloading LuLu restarts the system extension and briefly interrupts filtering. <br>
Mitigation: Run reload only after deliberate add, delete, enable, or disable operations. <br>


## Reference(s): <br>
- [Command Reference](references/commands.md) <br>
- [LuLu macOS Firewall](https://objective-see.org/products/lulu.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/woop/lulu-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may require macOS, LuLu, lulu-cli, and sudo approval for write operations.] <br>

## Skill Version(s): <br>
0.2.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

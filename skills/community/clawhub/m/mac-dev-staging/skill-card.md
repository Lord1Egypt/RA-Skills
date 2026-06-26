## Description: <br>
Turn a macOS machine into a local PHP/MariaDB staging server using the stock macOS Apache, Homebrew PHP 8.5, MariaDB, built-in SFTP, npm tooling, a local dev gateway surface, and optional nginx. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxmurphy](https://clawhub.ai/user/matthewxmurphy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure a Mac as a repeatable local PHP/MariaDB development or staging box for apps such as Joomla, WordPress, CodeIgniter, and Laravel. It helps detect the current stack, install local tooling, render Apache and gateway configuration snippets, verify services, and keep receipts for staging actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bootstrap and controller scripts can install Homebrew and npm packages or control local Apache, PHP, MariaDB, and nginx services when the user runs them. <br>
Mitigation: Run the scripts only on a Mac intended for local staging, review the package list first, and expect explicit service changes or sudo prompts. <br>
Risk: Enabling SFTP or Remote Login can expose staging files if the Mac is reachable beyond the intended private network. <br>
Mitigation: Keep SFTP private or LAN-only, prefer a dedicated staging user, and do not expose the staging stack directly to the public internet. <br>
Risk: Generated configs and action receipts could capture sensitive values if an operator places secrets in them. <br>
Mitigation: Do not put secrets in generated Apache configs, gateway environment snippets, or receipt detail fields. <br>
Risk: A local gateway or controller can collide with a shared gateway or become an unintended control surface if bound too broadly. <br>
Mitigation: Keep the Mac-local gateway on loopback, use non-conflicting test ports, and run port checks before enabling controller or gateway workflows. <br>


## Reference(s): <br>
- [Mac Dev Staging on ClawHub](https://clawhub.ai/matthewxmurphy/mac-dev-staging) <br>
- [Stock macOS Apache Layout](references/apache-layout.md) <br>
- [SFTP on macOS](references/sftp-on-macos.md) <br>
- [nginx and NPM](references/nginx-and-npm.md) <br>
- [Controller Surface](references/controller-surface.md) <br>
- [Gateway Coexistence](references/gateway-coexistence.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated shell or configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local Apache virtual host snippets, PHP enablement snippets, gateway environment values, service commands, verification checks, and receipt-writing commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

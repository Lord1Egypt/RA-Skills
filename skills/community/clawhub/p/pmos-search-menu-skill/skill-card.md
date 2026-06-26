## Description: <br>
Automates navigation through Gansu Electric Power Trading platform PMOS menu paths by opening pages, handling tabs, prompting for element references, and capturing browser snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xu-oliver](https://clawhub.ai/user/xu-oliver) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators with authorized PMOS access use this skill to guide or automate browser navigation to specific PMOS menu pages and inspect page snapshots after login. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates in a logged-in PMOS browser session, where snapshots and terminal output may expose page content. <br>
Mitigation: Run it only from an authorized account, monitor browser actions while it runs, and treat snapshots or command output as sensitive. <br>
Risk: Element references can change between PMOS page loads, which can cause navigation to click the wrong target or fail. <br>
Mitigation: Refresh browser snapshots before each action and provide only simple, current element references. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xu-oliver/pmos-search-menu-skill) <br>
- [NAVIGATION_PATH.md](references/NAVIGATION_PATH.md) <br>
- [OpenClaw Browser tool documentation](https://docs.openclaw.ai/tools/browser) <br>
- [OpenClaw CLI browser reference](https://docs.openclaw.ai/cli/browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and browser-operation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser snapshots and user-provided element references from the active PMOS session.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

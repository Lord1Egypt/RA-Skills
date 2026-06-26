## Description: <br>
Obclip helps agents install, verify, and run the obclip CLI to capture live web pages as Markdown or Obsidian notes while choosing appropriate browser, waiting, output, and troubleshooting options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rycen7822](https://clawhub.ai/user/rycen7822) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when an agent needs to install or invoke obclip, capture public or authenticated pages into notes, and troubleshoot incomplete captures or browser-profile issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing or running the npm CLI executes third-party code from @harris7/obclip. <br>
Mitigation: Verify that the package and referenced skill source are trusted before installation or execution. <br>
Risk: Using a browser profile for logged-in sites can expose cookies and session state to the clipping workflow. <br>
Mitigation: Use a dedicated browser profile for obclip instead of an everyday browser profile. <br>


## Reference(s): <br>
- [Installation and invocation](references/install-and-invoke.md) <br>
- [Command recipes](references/command-recipes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save clipped notes to disk or return Markdown on stdout depending on command flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

## Description: <br>
Guides agents through controlling external Mac display settings with m1ddc or ddcctl, including brightness, contrast, volume, input source, color temperature, power, automation, and software fallbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oakland](https://clawhub.ai/user/oakland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Mac users, developers, and IT support staff use this skill to generate command-line guidance and script patterns for adjusting external display settings without third-party GUI apps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Homebrew and monitor-control commands can change local display behavior or install command-line tools. <br>
Mitigation: Review commands before running them, verify the target display, and smoke-test reversible settings before saving scripts or shortcuts. <br>
Risk: Automation, power controls, input switching, or factory reset commands can disrupt display use or erase monitor preferences. <br>
Mitigation: Use factory reset only when intended, keep backups of working settings, and remove cron jobs or Automator shortcuts when automatic changes are no longer wanted. <br>
Risk: DDC/CI support varies by Mac, cable, adapter, dock, and monitor firmware. <br>
Mitigation: Probe display support first, enable DDC/CI in the monitor menu when available, and use the documented software fallback only when hardware DDC is unavailable. <br>


## Reference(s): <br>
- [Brightness Control](references/brightness.md) <br>
- [Color Temperature & Color Presets](references/color-temperature.md) <br>
- [Contrast Control](references/contrast.md) <br>
- [Input Source Switching](references/input-source.md) <br>
- [Power & Miscellaneous Controls](references/pow-and-misc.md) <br>
- [Volume Control](references/volume.md) <br>
- [m1ddc Apple Silicon display control](https://github.com/waydabber/m1ddc) <br>
- [ddcctl Intel Mac display control](https://github.com/kfix/ddcctl) <br>
- [MonitorControl DDC/CI compatibility notes](https://github.com/MonitorControl/MonitorControl#readme) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and script snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; users choose whether to run, save, or automate the suggested commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

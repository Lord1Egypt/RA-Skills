## Description: <br>
Automate iOS Simulator workflows (simctl + idb): create/boot/erase devices, install/launch apps, push notifications, privacy grants, screenshots, and accessibility-based UI navigation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and test engineers use this skill to manage iOS Simulator devices, install and launch apps, capture screenshots or video, inspect app UI state, and automate simulator interactions during iOS development and testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Simulator state can be changed through privacy grants, push notifications, clipboard updates, URL opens, app install or uninstall, and app launch commands. <br>
Mitigation: Confirm the target UDID, bundle ID, payload, and service before running state-changing commands on a trusted macOS development machine or trusted macOS node. <br>
Risk: Erase and delete commands can remove simulator data or simulator devices. <br>
Mitigation: Use the required --yes flag only after verifying the selected simulator or intentionally targeting all simulators. <br>
Risk: Optional idb dependencies are installed through Homebrew and pip when accessibility automation is needed. <br>
Mitigation: Verify or pin idb-related packages according to the environment's dependency review process before use. <br>


## Reference(s): <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Single-line JSON by default, with optional pretty JSON or short text summaries; screenshot and video commands write files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS with Xcode Command Line Tools for simctl; idb is optional but required for accessibility UI automation.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

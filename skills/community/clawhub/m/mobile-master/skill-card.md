## Description: <br>
Mobile Master assists with authorized Android mobile security analysis and reverse engineering workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nop3z](https://clawhub.ai/user/nop3z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security testers use this skill for authorized Android app analysis tasks such as starting Frida, spawning or attaching to apps, extracting APKs and AndroidManifest.xml, dumping DEX files, and reviewing mobile app behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains powerful Android device-control and reverse-engineering scripts. <br>
Mitigation: Install and use it only for authorized Android security testing on a dedicated test device. <br>
Risk: Shell helpers have unsafe argument handling and weak safeguards, including broad app-name matching. <br>
Mitigation: Patch helpers to use quoted arguments or arrays, validate package and script names, and avoid broad app-name matching before use. <br>
Risk: Frida server and ADB port forwarding can remain active after testing. <br>
Mitigation: Stop frida-server and remove ADB port forwarding when testing is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nop3z/mobile-master) <br>
- [Publisher profile](https://clawhub.ai/user/nop3z) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JavaScript Frida scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Android analysis artifacts such as pulled APK files, extracted AndroidManifest.xml files, and dumped DEX files when commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

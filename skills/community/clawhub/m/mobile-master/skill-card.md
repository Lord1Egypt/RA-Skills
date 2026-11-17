## Description:

Mobile Master assists with Android mobile security reverse engineering workflows, including Frida-based app attach and spawn, DEX dumping, APK extraction, manifest extraction, and related analysis commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nop3z](https://clawhub.ai/user/nop3z)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and mobile security engineers use this skill in authorized Android security labs to inspect APKs, start Frida workflows, dump DEX files, and extract AndroidManifest.xml for permission review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled scripts can run Frida, ADB, and root-level device actions against connected Android devices.

Mitigation: Use only in an authorized Android security lab with a known test device, known target package, and explicit permission for the assessment.

Risk: Weak script argument handling can allow unintended package selection, script loading, or command behavior.

Mitigation: Restrict inputs to trusted package names and trusted bundled scripts, quote or validate arguments before execution, and review commands before running them.

Risk: Frida server startup and port forwarding can leave an active instrumentation channel after testing.

Mitigation: Stop frida-server and remove ADB port forwarding when the session is complete.

Risk: APK and DEX extraction can create local copies of application code and manifests.

Mitigation: Store extracted files only in approved workspaces and handle them according to the target application's data-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nop3z/skills/mobile-master)
- [ClawHub publisher profile](https://clawhub.ai/user/nop3z)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and script references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local APK, DEX dump, and AndroidManifest.xml files when the referenced scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Use when compiling UNIHIKER K10 PlatformIO projects via the K10 Compile Server, opening the browser Web Serial flash page for a compiled build, downloading firmware, flashing a K10 connected to the compile server, or optionally uploading compiled firmware with local esptool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rockets-cn](https://clawhub.ai/user/rockets-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and educators use this skill to compile UNIHIKER K10 PlatformIO projects on a LAN or self-hosted HTTPS compile server, then download firmware or flash through browser Web Serial, server-side USB, or local esptool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project archives are uploaded to the compile server and may include sensitive local files.

Mitigation: Review the archive contents before upload and remove secrets such as .env files, keys, certificates, and credentials.

Risk: The workflow can flash firmware returned by a remote server.

Mitigation: Use only trusted compile servers and networks, and do not flash firmware produced by an untrusted server.

Risk: Helper commands disable TLS verification for curl requests.

Mitigation: Prefer a real or explicitly trusted certificate for the compile server instead of relying on insecure certificate bypasses.

Risk: The server setup notes that the service has no authentication and should not be exposed directly to the public internet.

Mitigation: Keep the server on a LAN, VPN, or SSH tunnel, or place it behind a reverse proxy with authentication, rate limiting, and HTTPS.

Risk: One helper path can allow command injection on Windows-like shells.

Mitigation: On Windows, use the PowerShell helper instead of the Bash helper under Git Bash, MSYS, or Cygwin until build_id and URL handling is fixed.

## Reference(s):

- [K10 Compile Server skill page](https://clawhub.ai/rockets-cn/skills/k10-compile-server)
- [K10 Compile Server API Reference](references/server-api.md)
- [Server Setup Guide](references/server-setup.md)
- [Troubleshooting](references/troubleshooting.md)
- [Public K10 compile server repository](https://github.com/rockets-cn/unihiker-k10-compile-server)
- [DFRobot UniHiker K10 PlatformIO platform](https://github.com/DFRobot/platform-unihiker.git)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce server URLs, build IDs, firmware download paths, flash instructions, and troubleshooting steps.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Automates large Google Photos Takeout downloads by discovering final download URLs, refreshing browser-derived Google cookies, downloading archive parts with aria2c, verifying ZIP files, and unpacking completed parts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drpeterkalmar](https://clawhub.ai/user/drpeterkalmar)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to migrate large Google Photos libraries from a completed Google Takeout job to local storage, NAS, or iCloud while reducing manual download supervision. It is most relevant when exports are split into many large ZIP parts and require resumable downloads, per-part verification, and immediate unpacking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Google session cookies and writes a local cookie jar.

Mitigation: Use a dedicated Chromium profile for Takeout, store cookie jars and discovered URLs only in private locations, and delete them immediately after the run.

Risk: The server security review flags the release as suspicious because it handles Google session cookies more broadly than some safety wording suggests.

Mitigation: Install only after reviewing the scripts, and use the skill only on accounts where you are comfortable granting a local agent access to an active Google browser session.

Risk: A caller-provided Linux browser command can execute a browser launch command chosen by the user.

Mitigation: Avoid the linux browser command option unless the command value is fully controlled and reviewed before execution.

Risk: Automated login attempts can trigger Google fraud detection, account recovery flows, or temporary account access limits.

Mitigation: Do not automate Google login or challenge flows; log in manually once and stop all login automation if any account recovery warning appears.

## Reference(s):

- [Pitfalls and Operational Playbook](references/pitfalls.md)
- [Example: 867 GB library, 18 parts](examples/basic-867gb-migration.md)
- [ClawHub skill page](https://clawhub.ai/drpeterkalmar/skills/google-photos-takeout-pipeline)
- [Pulling Google Takeout straight to a NAS](https://blog.omgmog.net/post/downloading-google-takeout-to-a-nas/)
- [smashah Google Takeout downloader gist](https://gist.github.com/smashah/67863f6c5f500c9098ad7c7e74eefc11)
- [nelsonjchen/gtr-proxy](https://github.com/nelsonjchen/gtr-proxy)
- [TheLastGimbus/GooglePhotosTakeoutHelper](https://github.com/TheLastGimbus/GooglePhotosTakeoutHelper)
- [raultov/google-photos-takeout-organizer](https://github.com/raultov/google-photos-takeout-organizer)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python helper scripts and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a completed Google Takeout export, a manually logged-in Chromium browser with local CDP enabled, aria2c, unzip, and Python websockets.]

## Skill Version(s):

1.0.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

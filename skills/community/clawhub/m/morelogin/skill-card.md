## Description:

Manage MoreLogin anti-detect browser profiles and cloud phones through the official Local API (http://127.0.0.1:40000), including browser profile lifecycle, fingerprint refresh, cloud phone power/file/app operations, and proxy/group/tag management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moreloginbrowser](https://clawhub.ai/user/moreloginbrowser)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation engineers use this skill to manage MoreLogin browser profiles, cloud phones, proxies, groups, and tags through the local MoreLogin API and to connect running profiles to Puppeteer or Playwright.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive profile, proxy, or ADB data may be sent to or printed from a broader endpoint than the localhost-only workflow implies.

Mitigation: Use the skill only with a running local MoreLogin desktop app, keep MORELOGIN_LOCAL_API_URL on localhost, and review command output before sharing it.

Risk: Tokens, profile identifiers, IP mappings, proxy credentials, or ADB details may be exposed through shared files or logs.

Mitigation: Keep secrets and profile-to-IP mappings out of shared files, redact sensitive output, and treat command output as sensitive unless reviewed.

Risk: Browser automation dependencies may be outdated for sensitive environments.

Mitigation: Upgrade the Playwright and Puppeteer dependency chain before using browser tooling in sensitive environments.

Risk: Batch delete, cache clearing, proxy deletion, group/tag deletion, and app uninstall operations can affect multiple managed resources.

Mitigation: Confirm target IDs and payloads before write operations, prefer explicit payloads for complex changes, and verify status after lifecycle actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/moreloginbrowser/skills/morelogin)
- [MoreLogin Local API Documentation](https://guide.morelogin.com/api-reference/local-api)
- [API-CONTRACT.md](artifact/API-CONTRACT.md)
- [README-OFFICIAL-API.md](artifact/README-OFFICIAL-API.md)
- [USAGE.md](artifact/USAGE.md)
- [local-api.yaml](artifact/local-api.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local CLI/API commands for a running MoreLogin desktop app; review outputs for sensitive profile, proxy, or ADB data before sharing.]

## Skill Version(s):

1.0.3 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description:

Checks the latest published versions of the LegionSpace app (package com.tongfudun.legion) across Apple App Store, Tencent MyApp, Xiaomi, vivo, Honor, Huawei AppGallery, and OPPO app stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[legionspace-hackathon](https://clawhub.ai/user/legionspace-hackathon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query and compare the current LegionSpace app version across major Chinese app stores and Apple's China App Store. It produces a console summary and a saved text report for release tracking or support checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically installs unpinned Python dependencies and Playwright Chromium when they are missing.

Mitigation: Run it in an isolated virtual environment or container, or preinstall and review pinned dependencies before execution.

Risk: The skill forces direct network access by disabling configured proxy use during the run.

Mitigation: Execute only in an environment where direct connections to the listed app-store sites are acceptable under local network policy.

Risk: Store scraping can return N/A or transient errors when pages are slow, desktop access is blocked, or DNS resolution fails.

Mitigation: Treat generated versions as operational signals and verify important release decisions against the relevant app-store page.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/legionspace-hackathon/skills/legionclaw-legionspace-version)
- [Apple iTunes Lookup endpoint for LegionSpace](https://itunes.apple.com/cn/lookup?bundleId=com.tongfudun.legion)
- [Tencent MyApp page for LegionSpace](https://sj.qq.com/appdetail/com.tongfudun.legion)
- [Xiaomi app store page for LegionSpace](https://app.mi.com/details?id=com.tongfudun.legion)
- [vivo app store page for LegionSpace](https://h5.appstore.vivo.com.cn/#/appinfo?appId=com.tongfudun.legion)
- [Honor app store page for LegionSpace](https://app.honor.com/appDetail/com.tongfudun.legion)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Console text and a UTF-8 text report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes LegionSpace_versions.txt under the skill scripts directory; results may include N/A or error messages when stores block desktop access or fail to resolve.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

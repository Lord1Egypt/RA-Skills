## Description: <br>
Publish, optimize, and scale Android apps on Google Play with release automation, ASO, policy compliance, and rejection recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release teams use this skill to plan, publish, optimize, and troubleshoot Android app releases on Google Play, including release tracks, ASO, policy compliance, rejection recovery, and Fastlane-based automation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Release automation workflows can expose keystores, service-account JSON, API keys, OAuth tokens, or Play Console credentials if users paste or store secrets in local notes or CI artifacts. <br>
Mitigation: Use protected CI secrets, avoid artifact uploads for generated credential files, delete temporary credential files after builds, and follow the skill's instruction to refuse storing credential material. <br>
Risk: Local memory may retain operational app metadata, package names, release status, or workflow preferences. <br>
Mitigation: Keep local memory limited to non-sensitive metadata and review or clear saved release preferences when they contain sensitive operational details. <br>
Risk: Publishing and policy guidance may become stale as Google Play requirements change. <br>
Mitigation: Review proposed release, policy, SDK, and testing recommendations against current Google Play Console requirements before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/google-play-store) <br>
- [Skill Homepage](https://clawic.com/skills/google-play-store) <br>
- [Setup](artifact/setup.md) <br>
- [Release Tracks and Rollouts](artifact/tracks.md) <br>
- [App Store Optimization](artifact/aso.md) <br>
- [Policy Compliance](artifact/policies.md) <br>
- [Rejection Recovery](artifact/rejections.md) <br>
- [Fastlane Automation](artifact/fastlane.md) <br>
- [Memory Template](artifact/memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with checklists, tables, and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local memory files under ~/google-play-store/ for non-sensitive app metadata and workflow preferences.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

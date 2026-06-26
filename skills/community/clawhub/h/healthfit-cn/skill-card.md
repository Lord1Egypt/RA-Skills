## Description: <br>
HealthFit-cn is a Chinese personal health-management agent skill that routes users to specialized advisors for exercise planning, nutrition guidance, local health tracking, TCM constitution support, seasonal wellness, tongue self-check guidance, and privacy-sensitive sexual-health logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchen913](https://clawhub.ai/user/chenchen913) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill as a Chinese-language personal health assistant for building a health profile, logging workouts and nutrition, generating weekly or monthly summaries, and receiving routed guidance from sport, nutrition, data-analysis, and TCM advisor roles. It is intended for wellness and tracking support, not medical diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health and sexual-health information may be stored locally in plaintext. <br>
Mitigation: Use the sexual-health module only when needed, avoid entering unnecessary intimate or medical details, and restrict file access to trusted local environments. <br>
Risk: Backups or exports may contain private health records. <br>
Mitigation: Review generated backups and exports before syncing, sharing, or importing them, and keep private sexual-health data excluded unless explicitly required. <br>
Risk: Wellness, nutrition, exercise, and TCM guidance could be mistaken for medical diagnosis or treatment. <br>
Mitigation: Treat outputs as informational wellness support and consult qualified clinicians for diagnosis, treatment, urgent symptoms, cardiovascular conditions, post-surgical recovery, or persistent health concerns. <br>
Risk: Broad activation rules may route more health-related conversations into this skill than users expect. <br>
Mitigation: Confirm user intent before recording personal information and make profile, nutrition, workout, TCM, and sexual-health logging explicit. <br>


## Reference(s): <br>
- [HealthFit Skill Definition](artifact/SKILL.md) <br>
- [English README](artifact/README_EN.md) <br>
- [Sport Routing Reference](artifact/references/sport_routing.md) <br>
- [Evidence Base](artifact/references/evidence_base.md) <br>
- [Storage Schema](artifact/references/storage_schema.md) <br>
- [Sexual Health Onboarding](artifact/references/onboarding_sexual_health.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration, shell commands] <br>
**Output Format:** [Markdown conversational responses with optional structured logs, summaries, menus, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local file updates, backups, exports, and SQLite-backed summaries when the hosting agent has file access.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

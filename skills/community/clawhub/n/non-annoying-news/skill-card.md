## Description: <br>
Create, configure, and render a source-grounded personal newspaper/news digest from URLs, bookmarks, X/Twitter bookmarks, browser reading lists/bookmarks, read-later apps, feeds, newsletters, web research, or pasted notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iret77](https://clawhub.ai/user/iret77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up and run a personalized, source-grounded news digest or newspaper from supplied links, saved items, feeds, notes, and configured source adapters. It supports onboarding, source selection, configuration, editorial QA, and rendering of HTML/PDF issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private source adapters, saved items, bookmarks, and reading lists may expose sensitive interests or personal information. <br>
Mitigation: Prefer pasted URLs or exports for lower risk, approve private-source adapters deliberately, and keep user-specific settings outside the public skill. <br>
Risk: Credentialed source collection can mishandle secrets if tokens, cookies, or private credentials are pasted into chat. <br>
Mitigation: Do not paste secrets into chat; use locally configured tools, exports, or manually supplied source manifests instead. <br>
Risk: Cron jobs or external delivery can create recurring behavior or send content beyond the local workspace. <br>
Mitigation: Require explicit approval before enabling any cron, schedule, or external delivery channel. <br>
Risk: Bookmarks and saved items are signals of interest, not verified factual sources. <br>
Mitigation: Fetch and verify linked content where possible, preserve source boundaries, and mark inaccessible material rather than treating metadata as read content. <br>


## Reference(s): <br>
- [Onboarding Guide](references/onboarding.md) <br>
- [Local Configuration](references/config-schema.md) <br>
- [Source and Signal Adapters](references/source-adapters.md) <br>
- [Editorial Standard](references/editorial-standard.md) <br>
- [Design Presets and Personalization](references/design-presets.md) <br>
- [Layout and Render QA](references/layout-and-render-qa.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance, JSON configuration, source manifests, and generated HTML/PDF/PNG issue files when rendering tools are available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Personalized issues, cron jobs, and external delivery require completed onboarding or explicit user confirmation.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata and SKILL.md package version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

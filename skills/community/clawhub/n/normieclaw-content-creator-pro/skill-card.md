## Description: <br>
Content Creator Pro helps an agent define brand voice, plan social content calendars, repurpose ideas across social platforms, and generate captions while retaining local profile and content history data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Creators, marketers, founders, and small business operators use this skill to generate platform-specific social posts, plan weekly content calendars, refine brand voice, repurpose source ideas, and export calendar materials for review or posting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores brand, audience, voice, content history, and engagement information locally, which may be sensitive business data. <br>
Mitigation: Install only in workspaces where local retention is acceptable, restrict workspace access, and review or delete stored profile and history files when they are no longer needed. <br>
Risk: First-run setup can overwrite existing configuration or data files if rerun in an active workspace. <br>
Mitigation: Back up existing config and data files before setup, review each setup command before execution, and avoid rerunning initialization over an established workspace. <br>
Risk: Generated social content, competitor analysis, and trend-based suggestions can be inaccurate, off-brand, or too close to source material. <br>
Mitigation: Review drafts before posting, verify factual claims, and use competitor content only for high-level positioning insights rather than copying text or creative assets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/normieclaw-content-creator-pro) <br>
- [README](artifact/README.md) <br>
- [Security guidance](artifact/SECURITY.md) <br>
- [First-run setup](artifact/SETUP-PROMPT.md) <br>
- [Content configuration](artifact/config/content-config.json) <br>
- [Dashboard companion specification](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with platform-labeled drafts, JSON workspace data, shell setup/export commands, and optional CSV or Markdown calendar exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local workspace files for brand profiles, content pillars, calendars, voice learnings, idea banks, history, engagement logs, and exports.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; changelog notes security fixes for script confinement and setup traversal removal) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

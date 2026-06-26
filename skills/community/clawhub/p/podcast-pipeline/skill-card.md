## Description: <br>
Podcast Pipeline helps creators prepare interviews, turn transcripts into show notes and promotional assets, plan solo episodes, and track episode, sponsor, and season records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External podcast creators and production teams use this skill to prepare guest interviews, convert recordings or transcripts into publication-ready notes and social assets, plan solo episodes, and maintain lightweight local records for episodes, sponsors, and seasons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local podcast records can contain sensitive transcripts, sponsor contacts, ad scripts, or production notes. <br>
Mitigation: Log only information that is needed, review podcast-data.json periodically, and avoid storing sensitive transcript or sponsor details unless required. <br>
Risk: Generated social posts, guest emails, chapters, and timestamps may be inaccurate or unsuitable for publication without review. <br>
Mitigation: Check generated emails, posts, chapter markers, and timestamps before sending or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chris-openclaw/podcast-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/chris-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown sections with optional JSON records for local podcast tracking] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local podcast-data.json file only when the user explicitly asks to log episode, sponsor, or season records.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and changelog, released 2026-05-12) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

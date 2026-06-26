## Description: <br>
Generates structured post outlines from reference materials for wisdom-style social posts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and content strategists use this skill to turn newsletters, scripts, notes, journal entries, raw ideas, or fetched URL content into five distinct social post outlines. The outlines emphasize paradoxes, transformation arcs, objections, action steps, and memorable closing insights rather than complete posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided URLs may expose private, tokenized, or access-controlled content to the external scraping workflow. <br>
Mitigation: Prefer pasting sensitive material directly and only provide URLs that are safe to fetch through SkillBoss API Hub. <br>
Risk: Generated social post outlines may contain exaggerated, unsupported, or overly absolute claims. <br>
Mitigation: Review each outline against the source material before publishing or expanding it into a complete post. <br>
Risk: Generated outlines are saved under content-ideas, which may persist sensitive source-derived material locally. <br>
Mitigation: Avoid using sensitive source material unless local persistence is acceptable, and review stored files according to the user's retention needs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/mar-content-ideas-generator) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, guidance] <br>
**Output Format:** [Markdown file containing five structured post outlines and analysis notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves generated outlines to content-ideas/ideas-{timestamp}.md and may fetch user-provided URLs through SkillBoss API Hub when SKILLBOSS_API_KEY is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

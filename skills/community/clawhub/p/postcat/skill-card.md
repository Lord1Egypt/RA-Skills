## Description: <br>
Organizes public Postcat product and documentation pages into concise feature, version, open-source link, and documentation summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mike47512](https://clawhub.ai/user/mike47512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to review public Postcat product pages, documentation, release information, and open-source entry points without account actions or project writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public product and documentation pages may change, causing summaries or version notes to become stale. <br>
Mitigation: Verify important details against the linked public Postcat pages before relying on the output. <br>
Risk: Automated page access can exceed a site's expected usage if run too frequently. <br>
Mitigation: Use lightweight requests, wait for dynamic pages to load, and apply rate limiting as described by the artifact. <br>
Risk: Users may accidentally provide sensitive or private project data while asking for summaries. <br>
Mitigation: Use the skill only with public pages and avoid storing or outputting sensitive information. <br>


## Reference(s): <br>
- [Postcat homepage](https://postcat.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or concise text summaries with link lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries should be based on publicly accessible, lightweight content only.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

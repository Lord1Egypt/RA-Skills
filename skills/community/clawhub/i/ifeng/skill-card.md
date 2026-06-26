## Description: <br>
Searches public Ifeng news and channel pages to summarize keyword news, channel trends, and long-form report highlights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codenova58](https://clawhub.ai/user/codenova58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and automation workflows use this skill for lightweight summaries of publicly available Ifeng content, including keyword result lists, channel hot topics, and article key points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public news pages can change, be dynamically rendered, or expose incomplete metadata. <br>
Mitigation: Wait for page load, cite source links, include collection time, and treat extracted summaries as time-bound. <br>
Risk: Over-collection or automated bulk access could violate site rules. <br>
Mitigation: Use only public pages, avoid interface reverse engineering and bulk collection, and apply rate limits. <br>


## Reference(s): <br>
- [Ifeng homepage](https://www.ifeng.com/) <br>
- [ClawHub skill page](https://clawhub.ai/codenova58/ifeng) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries and structured text fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include titles, sources, authors when shown, publication times, summaries, tags, links, public interaction metrics, channel names, and collection time.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

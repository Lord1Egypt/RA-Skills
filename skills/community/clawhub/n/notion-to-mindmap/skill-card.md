## Description: <br>
Converts a Notion HTML export into local mind map data and a self-contained interactive HTML mind map with search, zoom, expand/collapse, page focusing, and Notion link actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infniu](https://clawhub.ai/user/infniu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and external users use this skill to convert a user-provided Notion index.html export into an interactive browser-based mind map for reviewing page hierarchy, navigating Notion links, and searching exported page titles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated JSON and HTML can contain Notion page titles and Notion page links from the source export. <br>
Mitigation: Treat generated files as potentially sensitive and share them only with intended recipients. <br>
Risk: The skill processes user-provided Notion exports locally, so the output inherits the confidentiality of the input export. <br>
Mitigation: Use trusted local exports and review generated files before storing or publishing them outside the intended workspace. <br>


## Reference(s): <br>
- [README.md](README.md) <br>
- [ClawHub release page](https://clawhub.ai/infniu/notion-to-mindmap) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, JSON, HTML, Guidance] <br>
**Output Format:** [Local mindmap_data.json and self-contained mindmap.html files, with brief text status from the conversion scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BeautifulSoup4 and a user-provided Notion HTML export; generated files may contain page titles and Notion page links from the export.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

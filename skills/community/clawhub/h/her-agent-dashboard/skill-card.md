## Description: <br>
Her-Agent Dashboard displays an AI companion's self-awareness, emotional state, knowledge graph, learning progress, and evolution status in a local web dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenqin1688](https://clawhub.ai/user/wenqin1688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to view Her-Agent progress through a local web dashboard, including evolution level, emotional state, learning metrics, knowledge graph, and self-reflection history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The updater may read local OpenClaw diary and learning-note files to produce dashboard metrics. <br>
Mitigation: Install only in workspaces where that local data access is expected, and review generated dashboard content before sharing it. <br>
Risk: Opening the dashboard loads D3.js from a public CDN. <br>
Mitigation: Use the dashboard only where external CDN loading is acceptable, or replace the CDN dependency with a reviewed local copy before use in restricted environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wenqin1688/her-agent-dashboard) <br>
- [Publisher Profile](https://clawhub.ai/user/wenqin1688) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, files] <br>
**Output Format:** [Markdown instructions with local HTML and Python dashboard files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The dashboard updater writes a local HTML file and the page loads D3.js from a public CDN.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

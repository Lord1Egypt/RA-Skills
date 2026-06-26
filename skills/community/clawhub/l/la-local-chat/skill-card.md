## Description: <br>
Operate and improve the La Local location-management chat product. Use when reviewing or changing the frontend chat app, backend webhook, search behavior, media upload flow, Notion/Dropbox integration, deployment topology, or project-specific product logic for La Local. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GatoNegroIaLAB](https://clawhub.ai/user/GatoNegroIaLAB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product maintainers use this skill to operate and improve the La Local chat product for searching, creating, and updating audiovisual location records. It emphasizes search quality while keeping create and update flows explicit, deterministic, and tied to source records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents using this skill may touch Notion, Dropbox, repositories, and deployments that affect live La Local records. <br>
Mitigation: Use least-privilege access and review create or update actions before they affect production records. <br>
Risk: Search changes could return invented, weak, or misleading location matches. <br>
Mitigation: Retrieve real candidates from source data, rank against explicit query criteria, and return only strong matches. <br>
Risk: Changes to search behavior could regress create, update, upload, or thread continuity flows. <br>
Mitigation: Preserve thread_id handling, keep Notion as the source of truth, and test create/update flows when search behavior changes. <br>


## Reference(s): <br>
- [Architecture](references/architecture.md) <br>
- [Search Notes](references/search-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code or shell commands when implementation work is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concise implementation plans, repository changes, test guidance, and review notes for La Local chat workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

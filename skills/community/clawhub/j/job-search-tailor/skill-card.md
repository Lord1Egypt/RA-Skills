## Description: <br>
Searches LinkedIn for target roles and locations, deduplicates seen listings, and matches each job to a tailored resume archetype. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericshi123](https://clawhub.ai/user/ericshi123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers use this skill to run recurring job searches, avoid repeated listings, and choose or create tailored resume variants for each role. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Resume content and tailored resume files may persist locally under ~/.job-search. <br>
Mitigation: Review the generated files and delete ~/.job-search when the stored job-search state or resume-derived files are no longer needed. <br>
Risk: Google Docs support is described as not implemented in this version, while future use may require sensitive credentials. <br>
Mitigation: Keep google_docs_enabled false unless a later version clearly implements and documents credential handling. <br>
Risk: Keyword-based archetype matching can choose a weak fit or create unnecessary new resume variants. <br>
Mitigation: Review the selected archetype and adjust keywords or archetype_match_threshold when matches are too broad or too strict. <br>


## Reference(s): <br>
- [Configuration Guide](references/config-guide.md) <br>
- [Archetypes Guide](references/archetypes-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ericshi123/job-search-tailor) <br>
- [Publisher Profile](https://clawhub.ai/user/ericshi123) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest with local file paths, JSON-backed configuration, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local resume archetype Markdown files, config JSON, and seen-job tracking JSON under ~/.job-search.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

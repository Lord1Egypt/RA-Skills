## Description: <br>
Looks up ISO 4 and MEDLINE journal or magazine abbreviations, expands abbreviations to full names, and standardizes BibTeX journal fields using a local cache with public lookup fallbacks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agents365-ai](https://clawhub.ai/user/agents365-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and developers use this skill to answer journal abbreviation questions and standardize citation data or BibTeX journal fields before reference-list preparation and manuscript submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BibTeX processing can create rewritten output files and may change journal naming style. <br>
Mitigation: Run --dry-run first, review the change summary, and use an explicit output path when preserving originals matters. <br>
Risk: Lookups may contact public journal-data services or download local cache files on first use. <br>
Mitigation: Run in an environment where public lookup requests are acceptable, or inspect and pre-populate the cache before processing. <br>
Risk: Different sources may return ISO 4 or MEDLINE abbreviation styles. <br>
Mitigation: Review the reported source and standard before using results in publisher-specific citation workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agents365-ai/journal-abbrev) <br>
- [Project homepage](https://github.com/Agents365-ai/journal-abbrev) <br>
- [JabRef journal abbreviation data](https://raw.githubusercontent.com/JabRef/abbrv.jabref.org/main/journals) <br>
- [AbbrevISO lookup service](https://abbreviso.toolforge.org) <br>
- [NLM E-utilities service](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; CLI responses are JSON envelopes, tables, NDJSON streams, or BibTeX files depending on command and output mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write derived BibTeX output files unless --dry-run is used; first use may download public journal cache files.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

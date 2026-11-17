## Description:

Connects an agent to a user's authenticated academic database access for searching IEEE Xplore, Scopus, Engineering Village, and ACM Digital Library, then deduplicates, enriches, ranks, summarizes, and exports literature results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lishy227](https://clawhub.ai/user/lishy227)

### License/Terms of Use:

MIT License

## Use Case:

Researchers, research assistants, and developers use this skill to run multi-database literature searches through existing institutional access, enrich paper metadata and abstracts, rank results, and produce a structured review with citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses authenticated academic database sessions and can interact with cookies or browser login state.

Mitigation: Install only if you are comfortable granting this access; avoid cookie extraction or bridging unless you understand that cookies are active login credentials, and do not paste cookie values into ordinary config files or logs.

Risk: Paper metadata and abstracts may be sent to the configured LLM provider during reranking, summarization, or theme clustering.

Mitigation: Review and pin the LLM provider and base URL before running those steps, and use only approved endpoints for sensitive research material.

Risk: Automated access to paid academic databases may be subject to database or institutional usage terms.

Mitigation: Confirm that the intended workflow is permitted by the user's subscription, institution, and target database terms before running large searches or downloads.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lishy227/skills/paid-db-access)
- [README](README.md)
- [Quickstart](QUICKSTART.md)
- [Reference Manual](REFERENCE.md)
- [Elsevier Developer Portal](https://dev.elsevier.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON pipeline files, structured literature summaries, and BibTeX exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist intermediate paper metadata and abstract files locally; AI reranking, summarization, and theme clustering can call the configured LLM provider.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

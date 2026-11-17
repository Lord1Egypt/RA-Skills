## Description:

Deeply researches a person or organization for B2B outreach across Leadbay/LeadClaw, LinkedIn, social and web sources, company pages, podcasts, news, and local context, then writes a sourced persistent profile into the OutClaw knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milstan](https://clawhub.ai/user/milstan)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and go-to-market teams use this skill to research named people, companies, or Leadbay discovery results for B2B outreach, then persist sourced profiles and connection points in the OutClaw knowledge base. It prepares outreach context and does not contact prospects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can search connected inboxes, chats, SMS, notes, LinkedIn messages, public web sources, and Leadbay data for outreach research.

Mitigation: Limit connected private-source tools and require explicit approval before private-source searches or OCR.

Risk: The skill persistently stores enriched personal profiles in the OutClaw knowledge base.

Mitigation: Review KB and raw data regularly, apply retention controls outside the skill, and avoid researching targets without a legitimate outreach basis.

## Reference(s):

- [Research playbook](references/research-playbook.md)
- [Person researcher sub-agent](agents/person-researcher.md)
- [OutClaw project homepage](https://github.com/leadbay/outclaw)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summaries, KB file updates, shell command blocks, and strict JSON from the delegated person researcher]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research facts must be traceable to fetched URLs, raw KB source files, or kb/me context; unresolved findings are returned as gaps.]

## Skill Version(s):

1.0.6 (source: server release metadata; artifact frontmatter reports 2.1.33)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

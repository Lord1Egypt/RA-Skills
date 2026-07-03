## Description: <br>
B2B lead enrichment skill that uses public HTTPS scraping and optional MiniMax LLM metadata extraction to produce basic company information, guessed email patterns, social links, and scraped homepage context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzargona](https://clawhub.ai/user/jzargona) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, growth, and operations users can use this skill to look up companies, scrape public homepage context, generate guessed email patterns, and export basic lead records for review. Developers can configure scraping posture, dry-run enrichment, and optional MiniMax-based metadata extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags a code and documentation mismatch: user-facing docs say outreach drafts are not implemented, but the script exposes a drafts command. <br>
Mitigation: Review available commands before production use and avoid draft-generation workflows unless they are approved, documented, and tested for the intended outreach process. <br>
Risk: The security review notes that the skill scrapes public company homepages, saves discovered email addresses, and can send company or lead text to MiniMax when MINIMAX_API_KEY is set. <br>
Mitigation: Use approved company targets, verify lawful basis and CAN-SPAM/GDPR obligations before outreach, and leave MINIMAX_API_KEY unset when external LLM processing is not approved. <br>


## Reference(s): <br>
- [Lead Enrichment Scanner Reference Docs](references/README.md) <br>
- [Marketing Copy](references/marketing.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jzargona/skills/lead-enrichment-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [CSV lead records with optional Markdown outreach drafts and command-line configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes to user-specified output paths, scrapes public HTTPS homepages, and can call MiniMax when MINIMAX_API_KEY is set.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter, release evidence, script __version__) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

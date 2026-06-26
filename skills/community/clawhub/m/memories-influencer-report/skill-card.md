## Description: <br>
Generate a comprehensive influencer vetting report from a creator profile URL or video URLs, including brand safety and content quality analysis powered by Memories.ai video intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnshenopeninterx](https://clawhub.ai/user/shawnshenopeninterx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Marketing, partnership, and creator operations teams use this skill to vet influencers before brand collaborations. The skill can analyze recent videos from a profile URL or direct video URLs and produce a concise markdown report with engagement context, content quality scoring, and brand-safety notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Profile-based reports can analyze unrelated videos if the scraped or searched library content does not match the intended creator. <br>
Mitigation: Prefer direct video URLs for high-stakes brand-safety decisions and verify that every analyzed video belongs to the intended creator before relying on the report. <br>
Risk: The skill submits creator profile URLs, video URLs, transcripts, and metadata requests to Memories.ai services. <br>
Mitigation: Use scoped Memories.ai API keys and avoid submitting private or sensitive targets unless Memories.ai processing is acceptable for the use case. <br>


## Reference(s): <br>
- [Influencer Vetting Report Format](references/report-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown report with tables, scores, recommendations, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Memories.ai V1 and V2 API keys; reports may be written to a file when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

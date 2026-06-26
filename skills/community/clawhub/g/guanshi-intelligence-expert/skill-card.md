## Description: <br>
Guides an agent through public industry-source search, filtering, extraction, and cross-validation to produce structured intelligence summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business analysts, strategy researchers, and coordinated agent teams use this skill to gather public annual reports, research reports, white papers, and third-party market sources, then extract key metrics with source URLs, freshness, and confidence labels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may search the web and fetch external pages or PDFs. <br>
Mitigation: Use only sources the operator is allowed to access and keep source URLs with extracted findings. <br>
Risk: Extracted figures from public reports can be stale, partial, or based on conflicting definitions. <br>
Mitigation: Review dates, freshness labels, confidence labels, and conflict tables before relying on the intelligence. <br>
Risk: Paywalls, login walls, or scanned PDFs can limit extraction quality. <br>
Mitigation: Label blocked or low-quality extraction explicitly and seek alternative sources when needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Structured JSON intelligence summaries and concise markdown tables with source metadata, freshness, and confidence labels.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Flags stale data, source conflicts, paywalls, scanned PDFs, and intelligence gaps when encountered.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

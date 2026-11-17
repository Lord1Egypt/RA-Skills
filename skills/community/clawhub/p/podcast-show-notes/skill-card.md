## Description:

Turns raw podcast episode notes into publish-ready summaries, timestamps, resource links, and sponsor disclosures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US podcast producers and independent hosts use the skill to turn raw episode notes into structured show notes with summaries, timestamps, guest bios, resources, and sponsor disclosures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some supplied template headings, including the sponsor-read section, may not be recognized by the notes processor, leaving output sections incomplete.

Mitigation: Review the digest for missing sections and verify summaries, timestamps, links, and sponsor disclosures against the notes or transcript before publication.

Risk: Generated summaries, timestamps, links, and disclosures may be incomplete or inaccurate without human review.

Mitigation: Have the host or producer check the output against the source material and confirm claims and sponsor reads before publishing.

Risk: Writing to a directory containing an existing digest may overwrite it.

Mitigation: Use a dedicated output folder for each run.

Risk: The optional Windows app is a separate download and has not been covered by the bundled skill's security assessment.

Mitigation: Assess that app separately before choosing to download or use it.

## Reference(s):

- [Podcast show notes reference](references/podcast-show-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A digest with episode summary, timestamps, guest bio, resources, sponsor disclosure, and review guardrails; host review is needed before publication.]

## Skill Version(s):

1.0.7 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

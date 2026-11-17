## Description:

Creates publication-oriented scientific figures from structured specifications or real CSV data, checks journal requirements locally, and offers optional AI concept art and review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongsheng123132](https://clawhub.ai/user/dongsheng123132)

### License/Terms of Use:

MIT

## Use Case:

Researchers and academic authors use the skill to create publication figures from real datasets or structured figure specifications, check them against journal requirements, and get actionable review suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional AI review and concept generation can send research notes, metadata, figure text, prompts, or an image to an external service; gateway retention and downstream handling were not verified.

Mitigation: Keep confidential or unpublished work local unless you have reviewed and authorized the broader upload; omit optional review or vision uploads when that sharing is not acceptable.

Risk: Exporting untrusted SVGs can expose the user to unsafe content, and Chrome's sandbox may be disabled automatically during export.

Mitigation: Export only trusted SVGs, or perform the export in an isolated environment.

Risk: Paid AI features can consume wallet funds.

Mitigation: Use a dedicated key with a limited balance when enabling paid features.

## Reference(s):

- [Journal specification notes](artifact/references/journal-specs.md)
- [Figure types](artifact/references/figure-types.md)
- [Nature figure guide](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/)
- [Elsevier artwork sizing](https://www.elsevier.com/about/policies-and-standards/author/artwork-and-media-instructions/artwork-sizing)
- [IEEE resolution and size](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/resolution-and-size/)
- [PLOS figure requirements](https://journals.plos.org/plosone/s/figures)
- [ACM TAPS image specifications](https://authors.acm.org/proceedings/production-information/taps-image-specifications)

## Skill Output:

**Output Type(s):** [Files, JSON, Guidance]

**Output Format:** [SVG, PNG, PDF, or TIFF figures; JSON check and review reports; actionable text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Figures use supplied specifications and real data; AI image output is limited to labelled concept, cover, and TOC graphics.]

## Skill Version(s):

1.0.0 (source: server-resolved release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

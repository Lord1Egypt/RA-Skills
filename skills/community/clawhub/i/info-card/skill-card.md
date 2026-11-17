## Description:

Generates 900x1200 PNG information cards, knowledge cards, and poster-style visuals from HTML/CSS templates using Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rivercrab26](https://clawhub.ai/user/rivercrab26)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, educators, and developers use this skill to turn structured JSON content into shareable social-media-style PNG cards for tutorials, reports, comparisons, profiles, FAQs, timelines, and promotional visuals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill renders user-provided card data in an active browser, which can expose sensitive content or trigger unexpected network requests when image URLs are used.

Mitigation: Render only trusted card JSON, avoid remote or internal image URLs, and run generation in an isolated environment with restricted network access for sensitive content.

Risk: Browser screenshot output may vary across Playwright or Chromium versions.

Mitigation: Pin Playwright and Chromium versions for reproducible rendering.

## Reference(s):

- [Info Card skill page](https://clawhub.ai/rivercrab26/skills/info-card)
- [Design specs](artifact/references/design-specs.md)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Configuration instructions]

**Output Format:** [PNG image file path on stdout, with optional generated HTML for debugging]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output is /tmp/info_card_{timestamp}.png unless an output path is provided; image content is rendered from template data and screenshots.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

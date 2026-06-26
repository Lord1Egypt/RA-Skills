## Description: <br>
Transforms a user script into a minimalist, technology-themed vertical HTML slide deck in a Jobs-inspired style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunerw-dev](https://clawhub.ai/user/sunerw-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn draft talk scripts into condensed Markdown, a slide outline, and a ready-to-run vertical HTML presentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated presentations may load fonts and styling from third-party CDNs, which can be unsuitable for sensitive or offline decks. <br>
Mitigation: Review or replace CDN links with local assets before using generated decks in sensitive, restricted-network, or offline settings. <br>
Risk: The default generation behavior favors a Chinese, Jobs-style, vertical presentation format and may not match every audience or brand requirement. <br>
Mitigation: State the desired language, style, page count, and slide constraints when invoking the skill. <br>
Risk: Script condensation can omit nuance from the source material. <br>
Mitigation: Review the condensed script and slide outline before relying on the generated HTML presentation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunerw-dev/ppt-generator-1) <br>
- [Design Specification](artifact/references/design-spec.md) <br>
- [Slide Types](artifact/references/slide-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Files, Guidance] <br>
**Output Format:** [Markdown summary and slide outline followed by a single HTML document] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML targets a 9:16 vertical layout with keyboard navigation, smooth transitions, and CDN-loaded fonts/styles.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

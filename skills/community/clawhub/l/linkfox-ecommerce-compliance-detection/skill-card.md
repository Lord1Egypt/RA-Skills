## Description:

LinkFox E-commerce Compliance Detection helps agents check e-commerce product images and listing text for copyright, trademark, patent, and policy compliance risks, and retrieve patent records, translations, citations, images, and PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, compliance reviewers, and developers use this skill before product launch to screen listings and product images for IP and marketplace policy risk, then inspect supporting patent, trademark, copyright, and legal-status data. It provides data-oriented risk indicators and patent records, not legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends product images, listing descriptions, patent queries, phone or SMS login data, and API credentials to LinkFox services.

Mitigation: Install and run it only when the user trusts LinkFox and accepts sending those inputs to its services.

Risk: Custom gateway or endpoint environment variables can redirect credential-bearing requests.

Mitigation: Use custom LINKFOX_TOOL_GATEWAY or related endpoint variables only for destinations the operator controls and trusts.

Risk: The onboarding material includes a mutable remote release.zip fallback.

Mitigation: Avoid using remote installation fallbacks unless the artifact version and checksum are pinned and verified.

Risk: The scripts persist full API responses and cache data in the local workspace.

Mitigation: Keep the LinkFox output and cache directories out of shared workspaces and clean them according to local data-retention policy.

Risk: Compliance and infringement outputs are data signals and may be incomplete or legally inconclusive.

Mitigation: Treat the results as screening evidence and consult qualified counsel before making legal, FTO, or litigation decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-ecommerce-compliance-detection)
- [Ruiguan copyright detection](references/linkfox-ruiguan-copyright-detection.md)
- [Ruiguan design patent detection](references/linkfox-ruiguan-detection-patent-design.md)
- [Ruiguan image policy compliance search](references/linkfox-ruiguan-gun-parts-search.md)
- [Ruiguan text trademark detection](references/linkfox-ruiguan-text-trademark-detection.md)
- [Ruiguan graphic trademark detection](references/linkfox-ruiguan-trademark-graphic-detection.md)
- [Ruiguan utility patent detection](references/linkfox-ruiguan-utility-patent-detection.md)
- [Zhihuiya translated abstract data](references/linkfox-zhihuiya-abstract-data-translated.md)
- [Zhihuiya abstract image](references/linkfox-zhihuiya-abstract-image.md)
- [Zhihuiya bibliography](references/linkfox-zhihuiya-bibliography.md)
- [Zhihuiya translated claim data](references/linkfox-zhihuiya-claim-data-translated.md)
- [Zhihuiya claim data](references/linkfox-zhihuiya-claim-data.md)
- [Zhihuiya translated description data](references/linkfox-zhihuiya-description-data-translated.md)
- [Zhihuiya description data](references/linkfox-zhihuiya-description-data.md)
- [Zhihuiya full text image](references/linkfox-zhihuiya-fulltext-image.md)
- [Zhihuiya legal status](references/linkfox-zhihuiya-legal-status.md)
- [Zhihuiya patent cited](references/linkfox-zhihuiya-patent-cited.md)
- [Zhihuiya patent family](references/linkfox-zhihuiya-patent-family.md)
- [Zhihuiya patent forward citation](references/linkfox-zhihuiya-patent-forward-citation.md)
- [Zhihuiya patent image search](references/linkfox-zhihuiya-patent-image-search.md)
- [Zhihuiya PDF data](references/linkfox-zhihuiya-pdf-data.md)
- [Zhihuiya simple bibliography](references/linkfox-zhihuiya-simple-bibliography.md)
- [Zhihuiya utility patent image search](references/linkfox-zhihuiya-utility-patent-image-search.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with command snippets, tables, JSON-derived summaries, and saved result file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include similarity scores, rights-holder data, TRO indicators, trademark and patent metadata, legal-status records, citation data, PDF links, cost tokens, and cache or output file paths.]

## Skill Version(s):

1.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

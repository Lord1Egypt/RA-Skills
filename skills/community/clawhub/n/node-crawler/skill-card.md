## Description:

Node.js web crawler for production-grade, large-scale tasks such as bulk scraping, batch downloading, multi-page crawling, long-running spiders, and workflows that need connection pooling, rate limiting, proxy rotation, retries, and Cheerio parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike442144](https://clawhub.ai/user/mike442144)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Node.js crawlers for large batches of pages, file downloads, structured HTML extraction, pagination, proxy-aware crawling, and retry-controlled long-running spiders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawler examples can issue network requests against many targets.

Mitigation: Keep crawler targets and rate limits explicit before running generated code.

Risk: Binary download examples can write response bodies to local paths.

Mitigation: Save outputs only to intended paths and review filenames supplied through crawler task parameters.

Risk: The skill notes `rejectUnauthorized: false` for local debugging with self-signed certificates.

Mitigation: Do not disable TLS certificate validation outside local debugging with non-sensitive traffic.

Risk: The skill depends on the npm `crawler` package and related transitive dependencies.

Mitigation: Install only in a normal project or sandbox, and pin and review the npm dependency for serious use.

## Reference(s):

- [Options Reference](references/options.md)
- [Code Examples](references/examples.md)
- [got Options Documentation](https://github.com/sindresorhus/got/blob/main/documentation/2-options.md)
- [ClawHub Skill Page](https://clawhub.ai/mike442144/skills/node-crawler)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are implementation guidance and examples for agent-authored crawler code; generated crawlers may perform network requests and write local files when the user applies the examples.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

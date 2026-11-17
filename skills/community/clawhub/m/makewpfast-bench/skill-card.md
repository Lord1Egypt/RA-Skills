## Description:

This skill helps agents answer questions about the measured performance impact of WordPress plugins and themes by using the bundled mwf-bench CLI to query MakeWPFast Benchmark API data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcindudekdev](https://clawhub.ai/user/marcindudekdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site maintainers, and performance-focused WordPress operators use this skill to look up, compare, and interpret measured plugin or theme speed impacts. It can also audit a local WordPress install's active plugins when wp-cli and a site path are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local WordPress audits can disclose active-plugin inventory metadata to MakeWPFast.

Mitigation: Run audits only on sites where sharing active-plugin names with the MakeWPFast API is acceptable; use lookup or compare for individual named plugins when inventory disclosure is not acceptable.

Risk: Audit can consume paid quota for every uncached active plugin discovered, even when only a limited top-N result is displayed.

Mitigation: Check quota with mwf-bench me before broad audits and rely on the CLI's cache and batch guards before approving uncached lookups.

Risk: wp-cli may run with root allowance when the agent process is already root.

Mitigation: Avoid running audits as root unless root wp-cli execution is explicitly intended for that environment.

## Reference(s):

- [MakeWPFast Benchmark API reference](references/api.md)
- [Worked examples](references/examples.md)
- [MakeWPFast API](https://makewpfast.com/api/)
- [MakeWPFast API base endpoint](https://makewpfast.com/wp-json/mwf-api/v1)
- [WordPress.org plugins API](https://api.wordpress.org/plugins/info/1.2/)
- [WordPress.org themes API](https://api.wordpress.org/themes/info/1.2/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional JSON-derived analysis and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cached benchmark status, quota guidance, WordPress slug disambiguation, and measured deltas for TTFB, memory, and database queries.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

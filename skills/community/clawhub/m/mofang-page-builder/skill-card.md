## Description:

Build Magicflu/Mofang web-table custom pages from the jsonv2 records API for forms, records, CRUD pages, H5 extension pages, local mock/proxy debugging, and same-origin publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicscape](https://clawhub.ai/user/magicscape)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate and publish Magicflu/Mofang web-table pages from resolved form definitions, with examples for vanilla JavaScript, React, and Vue. It also supports local mock data, proxy debugging, and field definition import workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live proxy and credentialed scripts can expose or change real Magicflu/Mofang account data.

Mitigation: Prefer offline import or mock mode, avoid production credentials, and use proxy mode only for explicit live-data validation.

Risk: Untrusted or non-HTTPS BASE_URL values can route credentials or records through an unsafe endpoint.

Mitigation: Use HTTPS and a trusted BASE_URL before running credentialed fetch, proxy, or deployment scripts.

Risk: Proxy binding, CORS behavior, and unsafe HTML rendering may create exposure when used with live data.

Mitigation: Do not run proxy mode on shared networks, and address proxy binding, CORS, and innerHTML rendering issues before live-data use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/magicscape/skills/mofang-page-builder)
- [Magicflu/Mofang Records API Summary](references/api-summary.md)
- [Magicflu/Mofang Trae Skill Design](references/design.md)
- [Magicflu/Mofang Trae Skill Requirements](references/requirements.md)
- [Mock Data Template](assets/mock-data/README.md)
- [Vue Create Form Example](examples/vue/MagicfluForm.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code blocks and generated HTML, JavaScript, TypeScript, Vue, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local mock data, field-definition artifacts, and deployment command guidance for Magicflu/Mofang environments.]

## Skill Version(s):

1.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

## Description: <br>
Netlify API integration with managed OAuth for viewing sites, deploys, builds, DNS zones, environment variables, webhooks, forms, and related Netlify resources, with administrative write operations gated by explicit user approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and teams with Netlify accounts use this skill to inspect Netlify sites, deploys, builds, DNS zones, environment variables, webhooks, forms, functions, and related account resources through Maton-managed OAuth. Administrative changes such as creating sites, triggering builds, modifying DNS, or changing environment variables require exact resource identifiers and explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and OAuth access to Netlify resources. <br>
Mitigation: Keep MATON_API_KEY private, connect only the intended Netlify account, and review OAuth scopes before authorizing access. <br>
Risk: Administrative actions can affect live Netlify sites, builds, DNS records, environment variables, webhooks, forms, or deploys. <br>
Mitigation: Default to read-only operations and require exact resource identifiers, a consequence summary, and explicit user confirmation before write operations. <br>
Risk: Requests may target the wrong Netlify account when multiple Maton connections are active. <br>
Mitigation: Use the Maton-Connection header with the intended connection ID when more than one Netlify connection exists. <br>


## Reference(s): <br>
- [ClawHub Netlify Skill](https://clawhub.ai/byungkyu/netlify-api) <br>
- [Maton Homepage](https://maton.ai) <br>
- [Netlify API Documentation](https://open-api.netlify.com/) <br>
- [Netlify CLI Documentation](https://docs.netlify.com/cli/get-started/) <br>
- [Netlify Build Hooks Documentation](https://docs.netlify.com/configure-builds/build-hooks/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with endpoint references and inline Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized Netlify OAuth connection; API responses are JSON from Maton and Netlify endpoints.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

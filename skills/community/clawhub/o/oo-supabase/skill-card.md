## Description: <br>
Operate Supabase through the OOMOL oo CLI connector for reading, creating, updating, and deleting Supabase resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and manage Supabase projects, organizations, storage buckets, Edge Functions, API keys, secrets, health, SQL queries, and TypeScript database types through a connected OOMOL account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires connecting a Supabase account to OOMOL and allowing an agent to operate that account through the oo CLI. <br>
Mitigation: Install only when that account connection and delegated operation model are acceptable for the workspace. <br>
Risk: Write and destructive actions can change Supabase resources, API keys, or secrets. <br>
Mitigation: Review the exact payload and intended effect, and require explicit approval before API key, secret, project, delete, or update actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-supabase) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Supabase homepage](https://supabase.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector command responses may include JSON data and execution metadata.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>

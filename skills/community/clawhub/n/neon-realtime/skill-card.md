## Description:

Neon Realtime makes any SQL query live. Build realtime, reactive apps and agents on Lakebase Postgres with live SQL queries and reactivity primitives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrelandgraf](https://clawhub.ai/user/andrelandgraf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building applications or agents use this skill to create live database-backed views, subscriptions, and optimistic updates with Neon Realtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database, sealing, or cookie secrets could be exposed to client code.

Mitigation: Keep secrets server-side and expose only the public Realtime URL to the browser.

Risk: Live queries or changes to row-level security could leave data without equivalent authorization.

Mitigation: Check the session before sealing queries, authorize access through the query, and verify equivalent authorization across affected paths before changing existing protections.

Risk: Deployment or migration changes could be applied to the wrong linked project or branch.

Mitigation: Use a development branch first and verify the linked project before deploying or applying migrations.

Risk: A session change could leave subscriptions or prior-user data active.

Mitigation: Follow the documented session-reset and subscription-cleanup guidance.

## Reference(s):

- [Neon Realtime Overview](https://neon.com/docs/realtime/overview.md)
- [Neon Realtime Quickstart](https://neon.com/docs/realtime/quickstart.md)
- [Neon Realtime TypeScript SDK Reference](https://neon.com/docs/realtime/sdks/typescript.md)
- [Bundled Queries Reference](artifact/references/queries.md)
- [Bundled Reactivity Reference](artifact/references/reactivity.md)
- [Bundled Subscription Reference](artifact/references/subscribing.md)
- [Bundled Mutations Reference](artifact/references/mutations.md)
- [Bundled Server-Side Rendering Reference](artifact/references/ssr.md)
- [Parent Neon Skill](https://neon.com/docs/ai/skills/neon/SKILL.md)

## Skill Output:

**Output Type(s):** [Code, SQL, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript, SQL, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and setup guidance for live queries, subscriptions, optimistic writes, and server-side rendering.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

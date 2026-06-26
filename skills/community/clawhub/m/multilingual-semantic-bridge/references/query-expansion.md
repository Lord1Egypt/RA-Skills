# Query Expansion

Use query expansion only in service of the mainline pipeline:
1. preserve original input
2. derive canonical intent
3. generate a technical pivot
4. improve retrieval/routing

Do not treat query expansion as the whole project.

Useful forms when needed:
- original wording
- clarified wording
- canonical intent
- technical pivot
- exact identifiers

Selection rule:
- start with original wording + canonical intent
- add a technical pivot when the target surface is English-heavy or operationally specific
- keep exact identifiers unchanged whenever config keys, provider names, CLI commands, package names, or error strings matter

Keep it minimal and target-oriented.

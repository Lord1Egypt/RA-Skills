# Risk Rules

- Only resource inventory and plan generation are allowed.
- Do not create, delete, scale, migrate, bind, or unbind any resources.
- Secrets may only record existence, name, and purpose — never output sensitive values.
- All project_id, AK/SK, tokens, and certificates in output must be masked or omitted.
- All execution actions must be placed in the manual confirmation checklist.
# Sanitization Rules

Apply these rules every time this kit is generated, shared, or adapted.

## Never Copy

- real API keys
- bot tokens
- app secrets
- live gateway tokens
- source `.env` values
- private usernames from absolute paths
- personal scope names from the original operator
- live channel bindings
- private LAN addresses

## Replace With

- environment variable placeholders
- target-root-relative paths
- `user:owner` in place of personal user scopes
- generic role IDs in place of person-specific agent IDs
- `127.0.0.1` in place of private LAN hosts when a local endpoint example is needed

## Safe To Keep

- the architectural pattern
- the task board structure
- the memory scope layout
- the plugin choice for memory
- the compaction and recall strategy
- the role split and collaboration rules
- optional integration package names and public versions

## Review Checklist

Before handing the kit to someone else, verify that it does not contain:

- `C:\Users\...` paths from the source machine
- copied app IDs
- copied account IDs
- copied scope labels tied to a real person
- copied bindings under `bindings`
- copied install paths from the source machine

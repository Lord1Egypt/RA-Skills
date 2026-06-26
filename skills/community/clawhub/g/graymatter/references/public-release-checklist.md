# GrayMatter public release checklist

Use this checklist before publishing or handing the skill to customers.

## Skill quality

- `SKILL.md` matches actual repo behavior
- packaged `graymatter.skill` is refreshed after every script or SKILL change
- shell scripts are executable
- examples still match the current API shape

## Customer setup path

- README includes install, auth, smoke-test, and troubleshooting guidance
- auth docs make username/password prompt + secure Keychain storage the default flow
- docs do not require users to manually acquire a jwtSession token
- `scripts/gm-install-check` passes on a clean machine
- `scripts/gm-smoke` passes with real credentials
- optional environment variable overrides are documented as secondary/debug paths

## Safety and secrets

- no tokens or secrets are committed
- scripts never echo tokens
- docs explain that repo access is not auth

## Multi-agent operability

- agent identity guidance is documented
- durable write conventions are documented
- known backend tag limitation is documented with fallback behavior

## Release artifact

- `python3 scripts/package_graymatter.py` passes
- `graymatter.skill` includes all required scripts
- archive contents were verified after packaging
- at least one fresh install path was tested

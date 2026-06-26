# Compatibility Policy

## Target stack
- PrestaShop 9
- Symfony 6.4
- API Platform 3
- Redis single node
- MySQL primary store

## API versioning
- Contract versions are exposed in the URL.
- `/v1/` is the current stable contract.
- Maximum 2 major API versions are supported simultaneously.

## Backward compatibility
Breaking changes require a new API version. No breaking change is allowed inside the same major version.

## Skill compatibility
The published skill pack must remain consistent with:
- `SKILL.md`
- `openapi.yaml`
- `schemas/*.json`
- `examples.http`

Any divergence invalidates the publication package.

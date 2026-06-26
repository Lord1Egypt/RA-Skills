# Mac 多实例部署

Compact public-safe template for generic Mac multi-instance setup and pack
validation.

Published on ClawHub as `mac-multi-instance-deployment@1.0.4`.

## Quickstart

1. Copy `config/local-multi-instance.example.env` to a private location.
2. Replace the placeholder workspace roots with your own Mac paths.
3. Keep the instance map generic: `main`, `workbench`, `publish`, `archive`, `private`.
4. Review `references/instances.md`.
5. Run `./validate_repo.sh` and `./generate_public_pack.sh --dry-run`.

## Safety

- no real names
- no private IDs or account data
- no sensitive schedules or secrets
- no private runtime state in public packs

## Links

- [examples/README.md](./examples/README.md)
- [releases/1.0.4.md](./releases/1.0.4.md)
- [PUBLISHING.md](./PUBLISHING.md)
- [CHANGELOG.md](./CHANGELOG.md)
- [CUSTOMIZATION.md](./CUSTOMIZATION.md)

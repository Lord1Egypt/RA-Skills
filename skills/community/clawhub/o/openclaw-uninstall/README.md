# OpenClaw Uninstall Guide (openclaw-uninstall)

Community-maintained uninstall and verification guide for OpenClaw. Free, transparent, verifiable — no paid cleanup services.

## Install (ClawHub)

```bash
clawhub install openclaw-uninstall
```

## Manual usage

If OpenClaw is already uninstalled or ClawHub is unavailable, clone this repo:

```bash
git clone https://github.com/ERerGB/openclaw-uninstall.git
cd openclaw-uninstall
```

- **Verify residue**: `./scripts/verify-clean.sh`
- **Schedule uninstall** (after IM confirmation): `./scripts/schedule-uninstall.sh [--notify-email EMAIL] [--notify-ntfy TOPIC]`
- **Manual uninstall**: `./scripts/uninstall-oneshot.sh` or see [Uninstall docs](https://docs.openclaw.ai/install/uninstall)

## Disclaimer

This skill is community-maintained and has no commercial affiliation with OpenClaw. Based on [OpenClaw official docs](https://docs.openclaw.ai/install/uninstall).

## License

MIT

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenClaw Deploy is a deployment package tool for OpenClaw - it packages OpenClaw configurations, workspace files, skills, and Docker files into a distributable `tar.gz` archive that can be deployed to other servers.

## Common Commands

### Export (Pack) Configuration
```bash
cd ~/WorkSpace/clawSpace/openclaw-deploy
./build/base/base_builder.sh --output ./openclaw-{version}-{date}.tar.gz
# Or use backward-compatible path:
./scripts/export.sh --output ./openclaw-latest.tar.gz
```

### Local Deployment
```bash
./build/full/full_builder.sh --package ./openclaw-deploy.tar.gz --install-dir /opt/openclaw
# Or use backward-compatible path:
./scripts/deploy.sh --package ./openclaw-deploy.tar.gz
```

### Remote Deployment
```bash
./build/full/full_builder.sh --host <server-ip> --user <username> --key ~/.ssh/id_rsa
```

### Docker Deployment (Manual)
```bash
cd docker
cp .env.example .env
# Edit .env with API Keys
docker-compose up -d
```

### Run Tests
```bash
./tests/run_all_tests.sh
```

## Architecture

The project follows a modular structure:

- **build/** - Packaging modules
  - `base/base_builder.sh` - Basic packaging (exports config)
  - `full/full_builder.sh` - Full packaging + deployment
  - `common.sh` - Shared functions

- **deploy/** - Deployment modules
  - `local/check_env.sh` - Environment checks
  - `local/handle_conflict.sh` - Conflict resolution (backup/cover/update)
  - `remote/remote_deploy.sh` - SSH-based deployment
  - `common.sh` - Shared functions

- **docker/** - Docker deployment files

- **tests/** - Test suite (90% coverage)

## Key Behaviors

1. **Sensitive Data Removal**: Export automatically strips API keys, tokens, passwords from config files before packaging
2. **SHA256 Verification**: Deployments verify package integrity using `.sha256` checksum files
3. **Conflict Handling**: Supports 4 modes - `cover` (default), `backup`, `update`, `parallel`
4. **Remote Deployment**: Uses SSH with key-based auth, supports password auth as fallback

## Important Notes

- **Security Issues**: PROGRESS.md documents high-priority security concerns (heredoc injection, `rm -rf` risk, SSH MITM)
- **Current Status**: V1.1 100% complete (2026-03-08) - SHA256 verification ✅, test coverage 95%
- **Source Location**: Config is read from `~/.openclaw/` (HOME directory)

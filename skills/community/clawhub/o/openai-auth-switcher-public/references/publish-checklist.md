# Publish checklist

## Metadata

- [ ] `SKILL.md` frontmatter is valid
- [ ] description clearly says this is a publishable/public track
- [ ] version to publish is decided (`0.2.0` recommended for the next public release)
- [ ] changelog / release notes text is prepared

## Compatibility

- [ ] compatibility wording uses tested versions only
- [ ] Python / Node / OS expectations are documented
- [ ] non-portable features are explicitly scoped out

## Security / sanitization

- [ ] no `auth-profile.json` under the public source tree
- [ ] no `skill-data/state/*` runtime files under the public source tree
- [ ] no `skill-data/runtime/*` generated install/runtime files under the public source tree
- [ ] testing uses `OPENAI_AUTH_SWITCHER_PUBLIC_STATE_DIR` or another external state base when possible
- [ ] no oauth callbacks / session artifacts in the public source tree
- [ ] no backups in the public source tree
- [ ] no `__pycache__`
- [ ] no machine-specific secrets or private credentials

## Packaging

- [ ] package using `scripts/package_public_skill.py`
- [ ] inspect produced `.skill` contents
- [ ] confirm `assets/webui/` and static brand assets are included
- [ ] confirm forbidden runtime files are excluded

## Validation

- [ ] `doctor.py --json` succeeds or only returns acceptable warnings
- [ ] `env_detect.py --json` works
- [ ] `inspect_runtime.py --json --include-status --include-sessions` works
- [ ] `switch_experiment.py --dry-run` works
- [ ] `rollback_experiment.py` argument validation works
- [ ] `token_ledger.py` works
- [ ] `hourly_usage.py` works
- [x] clean install reaches web preview successfully
- [ ] `install.sh` entrypoint verified on a second Claw machine
- [x] uninstall/stop + reinstall path verified
- [x] `9527` occupied → `12138` fallback verified
- [x] `9527` + `12138` occupied → random fallback verified
- [x] live status prefers systemd state over stale install-info

## Publication

- [ ] `clawhub login` completed
- [ ] `clawhub whoami` confirmed
- [ ] final publish command reviewed before execution

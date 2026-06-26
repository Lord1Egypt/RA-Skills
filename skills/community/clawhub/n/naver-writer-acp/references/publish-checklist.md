# ClawHub Publish Checklist (ACP-connected skill)

## Content checks

- [ ] `SKILL.md` explains ACP commerce path clearly
- [ ] No secrets committed (`token`, `key`, `.env`)
- [ ] Scripts point to preflight/setup_runner/publish flow
- [ ] `references/setup.md` updated with real env names

## Validation checks

- [ ] `scripts/smoke_test.sh` passes
- [ ] `scripts/preflight.sh` returns RUNNER_NOT_READY contract on clean machine
- [ ] proof/setup-url issue works on production control-plane

## Publish

```bash
clawhub login
clawhub publish ./skills/naver-writer-acp \
  --slug naver-writer-acp \
  --name "Naver Writer ACP" \
  --version 1.1.0 \
  --changelog "Switch to ACP marketplace-connected flow (preflight/setup_runner/publish)"
```

## Post-publish

- [ ] `clawhub install naver-writer-acp --version 1.1.0` works in clean dir
- [ ] Installed scripts run (`scripts/smoke_test.sh`)

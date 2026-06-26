# Release Checklist (Core)

1. Preview publish artifact:

```bash
rsync -av --dry-run --exclude-from=.clawhubignore ./ /tmp/proactive-claw-bundle-preview/
```

2. Verify excluded files are not in preview:

```bash
rsync -av --dry-run --exclude-from=.clawhubignore ./ /tmp/proactive-claw-bundle-preview/ \
  | rg -n "cross_skill.py|team_awareness.py|install_daemon.sh|setup_clawhub_oauth.sh|voice_bridge.py|llm_rater.py"
```

Expected result: no matches.

3. Validate syntax:

```bash
python3 -m json.tool config.example.json >/dev/null
export PYTHONPYCACHEPREFIX=/tmp/pycache-proactive-claw
python3 -m py_compile scripts/*.py
bash -n scripts/setup.sh
bash -n scripts/quickstart.sh
```

4. Publish:

```bash
clawhub publish . \
  --slug proactive-claw \
  --name "Proactive Claw" \
  --version <VERSION> \
  --tags "ai-agent,automation,calendar,daemon,google-calendar,latest,local-first,nextcloud,open-source,privacy,proactive,productivity,reminders,scheduling,sqlite"
```

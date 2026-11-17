# Deployment Markers

Record deployment events in New Relic so you can correlate releases with performance changes.

---

## Record a Deployment

```bash
newrelic apm deployment create \
  --applicationId <APP_ID> \
  --revision "v1.2.3" \
  --description "Brief description of what changed" \
  --user "deploy-bot"
```

### Required
- `--applicationId` — numeric APM application ID
- `--revision` — version string (e.g. git SHA, semver, MR number)

### Optional
- `--description` — what changed (show in NR UI on charts)
- `--user` — who/what deployed
- `--change-log` — detailed change notes

---

## Get Application ID

```bash
newrelic entity search --name "my-app" --type APPLICATION --domain APM | \
  jq '.[] | {name, applicationId}'
```

---

## List Recent Deployments

```bash
newrelic apm deployment list --applicationId <APP_ID>
```

---

## GitLab/GitHub CI Integration

Check out this skill repository into `vendor/newrelic-cli-skills` in the application CI
job, set `NEW_RELIC_API_KEY` as a masked secret, and invoke the maintained helper after a
successful deploy. In GitHub Actions, use a second `actions/checkout` step with
`repository: vince-winkintel/newrelic-cli-skills` and `path: vendor/newrelic-cli-skills`;
in GitLab, clone or add the repository as a submodule at the same path. Keep every
CI-provided value in its own quoted argument:

```bash
NEWRELIC_SKILLS_DIR=vendor/newrelic-cli-skills

"$NEWRELIC_SKILLS_DIR/scripts/deployment-marker.sh" \
  "$NEW_RELIC_APP_ID" \
  "${CI_COMMIT_SHORT_SHA:-$(git rev-parse --short=8 HEAD)}" \
  "${CI_COMMIT_TITLE:-$(git log -1 --format=%s)}" \
  "${GITLAB_USER_LOGIN:-${GITHUB_ACTOR:-ci-bot}}"
```

The helper requires a decimal application ID, converts tabs and line breaks in text fields
to spaces, rejects any remaining control characters, and forwards each accepted value as
a literal argument. Do not generate a script from CI variables and do not pass these
values through `eval` or `source`.

---

## Why Deployment Markers Matter

After recording a deployment, the New Relic UI places a vertical line on all APM charts at that timestamp. This makes it immediately obvious if:
- Response times increased after a deploy
- Error rates spiked post-release
- Throughput dropped unexpectedly

You can also query them via NRQL:

```nrql
SELECT *
FROM Deployment
WHERE appId = <APP_ID>
SINCE 1 week ago
```

---

## Automation: Mark on Every Merge

Call the repository helper from a post-merge webhook or CI step rather than copying its
implementation into generated source. Set `NEWRELIC_SKILLS_DIR` to the explicit checkout
location shown above; multi-line release descriptions are normalized to one line:

```bash
"$NEWRELIC_SKILLS_DIR/scripts/deployment-marker.sh" \
  "$NEW_RELIC_APP_ID" \
  "$RELEASE_REVISION" \
  "$RELEASE_DESCRIPTION" \
  "$DEPLOY_USER"
```

# Plane Flow CLI Usage

This reference lists the validated commands for the bundled Plane integration in `scripts/`.

## Note

This file is a CLI/debugging reference for the bundled implementation scripts.
The normal product surface is the `plane-flow` skill itself.

In the intended operating model:
- administrators configure and validate the Plane connection
- business users interact with the skill through normal requests

Use this reference when:
- developing or debugging the skill
- validating local Plane connectivity as an administrator
- manually testing commands outside normal agent flow

## Preconditions

Before using the local CLI helpers, configure the host environment:

```bash
export PLANE_BASE_URL="https://your-plane.example.com"
export PLANE_API_TOKEN="your_api_token"
export PLANE_WORKSPACE_ID="your-workspace-id"
export PLANE_CONFIG_FILE="$HOME/.plane_config.yaml"  # optional
```

Optional convenience helper:

```bash
python3 scripts/init_config.py
```

Optional validation step:

```bash
python3 scripts/test_connection.py
```

## Validated Read Commands

### List projects

```bash
python3 scripts/plane_cli.py projects list
```

### Summarize a project

```bash
python3 scripts/plane_cli.py projects summary --project "Your Project"
```

### List issues in a project

```bash
python3 scripts/plane_cli.py issues list --project "Your Project"
```

### Get a specific issue

```bash
python3 scripts/plane_cli.py issues get --project "Your Project" --id <ISSUE_ID>
```

### List states

```bash
python3 scripts/plane_cli.py states list --project "Your Project"
```

### List labels

```bash
python3 scripts/plane_cli.py labels list --project "Your Project"
```

### List members

```bash
python3 scripts/plane_cli.py members list
```

## Validated Write Commands

### Create issue

```bash
python3 scripts/plane_cli.py issues create \
  --project "Your Project" \
  --title "Draft requirement from meeting notes" \
  --desc "Created from summarized action items."
```

### Create issue with inline image(s)

```bash
python3 scripts/plane_cli.py issues create \
  --project "Your Project" \
  --title "Requirement with screenshots" \
  --desc "Created from summarized action items plus reference images." \
  --image ./screen-1.png \
  --image ./screen-2.png \
  --image-align center
```

### Create issue with mixed alignment (directive syntax)

In `--desc`, use `[image: path, align]` for per-image alignment:

```bash
python3 scripts/plane_cli.py issues create \
  --project "Your Project" \
  --title "Comparison" \
  --desc "Before:\n[image: ./before.png, left]\n\nAfter:\n[image: ./after.png, right]"
```

Alignment options: `center` (default), `left`, `right`.

### Update description

```bash
python3 scripts/plane_cli.py issues update-desc \
  --project "Your Project" \
  --id <ISSUE_ID> \
  --desc "Updated with clarified scope and acceptance notes."
```

### Update description with inline image(s)

```bash
python3 scripts/plane_cli.py issues update-desc \
  --project "Your Project" \
  --id <ISSUE_ID> \
  --desc "Updated with clarified scope, acceptance notes, and reference images." \
  --image ./flow-1.png \
  --image ./flow-2.png \
  --image-align left
```

### Move issue to a state

```bash
python3 scripts/plane_cli.py issues move \
  --project "Your Project" \
  --id <ISSUE_ID> \
  --state todo
```

### Assign issue

```bash
python3 scripts/plane_cli.py issues assign \
  --project "Your Project" \
  --id <ISSUE_ID> \
  --assignee "member@example.com"
```

### Set priority

```bash
python3 scripts/plane_cli.py issues set-priority \
  --project "Your Project" \
  --id <ISSUE_ID> \
  --priority high
```

### Set labels

```bash
python3 scripts/plane_cli.py issues set-labels \
  --project "Your Project" \
  --id <ISSUE_ID> \
  --labels "backend,pm"
```

## Comment Commands

### Create comment

```bash
python3 scripts/plane_cli.py comments create \
  --project "Your Project" \
  --issue-id <ISSUE_ID> \
  --content "This issue was resolved after review."
```

### Create comment with inline image(s)

```bash
python3 scripts/plane_cli.py comments create \
  --project "Your Project" \
  --issue-id <ISSUE_ID> \
  --content "Attached are the screenshots from the test run." \
  --image ./screen-1.png \
  --image ./screen-2.png \
  --image-align center
```

Images use Plane's native `<image-component>` nodes with alignment attributes.
Supported alignments: `left`, `center` (default), `right`.
True text wrapping is not supported by Plane's editor.
Fallback: if embedding fails, the image is still uploaded as an attachment and a text note is added.

## Known Integration Notes

### Authentication

This integration uses:

```http
X-API-Key: <token>
```

Not:
- `Authorization: Bearer ...`
- `Authorization: Token ...`

### Issue routing model

Issue list/detail/update routes are handled as project-scoped:

```text
/workspaces/{workspace}/projects/{project}/issues/...
```

### Practical guidance

- Always pass `--project` for issue operations.
- If a label, state, or member name is uncertain, list them first.
- Use `--raw` when debugging response fields or checking IDs.

# CI/CD Templates

GitHub Actions workflow templates for multi-agent projects.

## Test Pipeline (test.yml)

```yaml
name: Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']  # adjust per project
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest tests/ -v --tb=short --cov=src --cov-report=term-missing
      - name: Upload coverage
        if: matrix.python-version == '3.12'
        uses: codecov/codecov-action@v4
```

For TypeScript/Node.js projects:

```yaml
name: Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
```

## Lint Pipeline (lint.yml)

```yaml
name: Lint
on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install linters
        run: pip install ruff mypy
      - name: Ruff check
        run: ruff check src/ tests/
      - name: Ruff format check
        run: ruff format --check src/ tests/
      - name: Type check
        run: mypy src/ --ignore-missing-imports
```

## Discord Notification Action

Add to any workflow to get Discord notifications on failure/success:

```yaml
  notify:
    needs: [test]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Discord Notification
        uses: sarisia/actions-status-discord@v1
        with:
          webhook: ${{ secrets.DISCORD_WEBHOOK }}
          status: ${{ needs.test.result }}
          title: "${{ github.repository }} CI"
          description: |
            Commit: ${{ github.event.head_commit.message }}
            Author: ${{ github.event.head_commit.author.name }}
          color: ${{ needs.test.result == 'success' && '0x00ff00' || '0xff0000' }}
```

### Discord Webhook Setup

1. Discord Server Settings → Integrations → Webhooks → New Webhook
2. Choose the notification channel (e.g., #traveler-home or a dedicated #ci-cd)
3. Copy webhook URL
4. GitHub repo → Settings → Secrets → New repository secret
   - Name: `DISCORD_WEBHOOK`
   - Value: the webhook URL

### Alternative: GitHub Native Discord Integration

For simpler setup (no Actions required):
1. Discord Server Settings → Integrations → Webhooks → New Webhook
2. Append `/github` to the webhook URL
3. GitHub repo → Settings → Webhooks → Add webhook
   - Payload URL: `https://discord.com/api/webhooks/<id>/<token>/github`
   - Content type: `application/json`
   - Events: Push, Pull Request, Workflow Run

## Branch Protection Rules

Create `.github/ruleset.json`:

```json
{
  "name": "main-protection",
  "target": "branch",
  "enforcement": "active",
  "conditions": {
    "ref_name": {
      "include": ["refs/heads/main"]
    }
  },
  "rules": [
    { "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": true,
        "require_last_push_approval": false
      }
    },
    { "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "required_status_checks": [
          { "context": "test" }
        ]
      }
    }
  ]
}
```

## TDD Workflow for Agents

When Code Engineer receives a task:

1. **Write the test first** — define expected behavior
2. **Run tests — see them fail** (red)
3. **Implement minimal code** to pass the test (green)
4. **Refactor** while tests stay green
5. **Commit** with message: `feat(scope): description` or `fix(scope): description`
6. **Push** — CI runs automatically
7. **If CI fails** — fix before moving on, never leave main broken

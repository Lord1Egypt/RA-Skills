---
name: ClawHub Publish Smoke Check
description: Verify ClawHub login, dry-run sync state, one-off publish success, and cleanup for a local skill workspace.
---

## What This Skill Does

Use this skill when you need to confirm the ClawHub publishing path works end to end from a local workspace without touching existing production skills.

It focuses on four checks:

1. Confirm the current `clawhub` login identity.
2. Inspect whether the current workspace would upload anything with `clawhub sync --dry-run`.
3. Publish a separate test skill with a unique slug.
4. Clean up the temporary skill after verification.

## When To Use

- You just ran `clawhub login` and want to verify the token is valid.
- `clawhub sync --dry-run` shows existing skills that should not be published blindly.
- You need a smoke test for upload and publish behavior.
- You want a safe fallback that does not mutate public versions of real skills.

## Recommended Flow

### 1. Verify Identity

Run:

```bash
clawhub whoami
```

The command should return the expected handle. If it fails, re-run `clawhub login`.

### 2. Inspect Sync State

Run:

```bash
clawhub sync --dry-run
```

If this proposes updates for installed third-party skills, do not publish them directly. Use a temporary test skill instead.

### 3. Publish a Temporary Skill

Prepare a dedicated folder with a unique slug and meaningful documentation, then publish it:

```bash
clawhub publish ./tmp/my-test-skill \
  --slug my-unique-test-skill \
  --name "My Unique Test Skill" \
  --version 0.0.1 \
  --changelog "Smoke-test publish"
```

A successful publish proves that authentication, upload, and registry validation all work.

### 4. Verify and Clean Up

After publish, inspect the skill page or query the registry, then hide or delete the temporary slug if it should not remain public:

```bash
clawhub hide my-unique-test-skill --yes
```

or

```bash
clawhub delete my-unique-test-skill --yes
```

## Failure Modes

### Not Logged In

Symptom: `Not logged in. Run: clawhub login`

Action: run `clawhub login`, complete browser auth, then repeat `clawhub whoami`.

### Rate Limit Or External API Delay

Symptom: publish reports a short cooldown or API rate limit reset window.

Action: wait for the reset window, then retry once.

### Content Quality Rejection

Symptom: publish says the content is too thin or templated.

Action: expand the skill with concrete purpose, steps, commands, and failure handling. Generic placeholder text is usually rejected.

## Success Criteria

This smoke check passes only if all of the following are true:

- `clawhub whoami` succeeds.
- `clawhub publish` returns a successful result for the temporary slug.
- The published slug is reachable or inspectable.
- Cleanup succeeds if cleanup was requested.

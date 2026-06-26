# Verdict Checklist (Publish-Readiness)

Use this checklist before publishing a Poke recipe.

## Must pass

- Unique enough vs visible listings on https://poke.com/recipes
- Name is concrete and non-generic
- Description is one-line and specific
- Onboarding asks only minimal context
- Prefilled first message delivers immediate value
- Integration URL is real + Test connection succeeds
- Sandbox: 5/5 prompts pass
- Failure behavior is explicit (integration down / missing data)
- Draft reviewed with publish lock in mind (cannot edit after publish)

## Verdict labels

- `READY` - all must-pass items complete
- `NEEDS_WORK` - one or more must-pass items missing
- `BLOCKED` - dependency missing (integration/auth/deploy)

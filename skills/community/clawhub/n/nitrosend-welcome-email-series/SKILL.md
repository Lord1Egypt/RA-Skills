---
name: welcome-email-series
description: >
  Build a welcome email or welcome series for new subscribers or customers:
  a first welcome email, then follow-up emails over the first days,
  triggered by a signup form or a new list member. Use for welcome emails,
  onboarding emails and new subscriber journeys.
---

# Welcome email series

Build the first emails a new subscriber or customer receives.

Examples: [Welcome emails](https://nitrosend.com/email-examples/welcome)

1. Check existing flows with `nitro_query` so you don't duplicate a welcome
   series the brand already has. (`brand.welcome_email` in status is the
   owner's onboarding preview, not a subscriber series.)
2. Agree the trigger: a signup form or list join (`list_add`) or any new
   contact. A typical series is a welcome email straight away, then two or
   three follow-ups over the first week (story, best content or products,
   an offer or next step).
3. Compose it with `nitro_compose_flow` in intent mode and follow `next_call`.
   It saves as an inactive draft.
4. Pair it with the `signup-form-builder` skill if the user has no form yet.

## Before anything sends

Use the `send-campaign` and `build-flow` skills for review and delivery:
confirm the account and brand with `nitro_get_status`, keep returned IDs and
revisions, check the saved target with `nitro_review_delivery`, send a test
only with `nitro_send_test_message` when asked, and launch or schedule with
`nitro_control_delivery` only after the user explicitly approves the audience.
A saved draft is not a send. Never invent results, metrics or IDs.

# Reviewer Test Credentials

Do not commit real reviewer credentials, bearer tokens, OAuth client secrets, passwords, or recovery codes to this repository.

## Demo Account Requirements

Create a fully featured GrayMatter review account before submitting the app in the OpenAI Platform Dashboard.

The account must include sample data that demonstrates:

- Writing a MemoryEntry.
- Reading a MemoryEntry by ID.
- Searching memory.
- Inspecting the SwarmOps graph.
- Listing and reading at least one safe sample business entity.
- Creating a low-risk sample entity if the review path exercises write tools.

## Login Requirements

OpenAI review must be able to access the demo account without extra setup.

- Use a dedicated demo login and password, or an OAuth test account if the submitted app uses OAuth.
- Disable MFA, SMS verification, email-code verification, hardware-key requirements, and signup approval for the reviewer account.
- Keep the account scoped to sample data only.
- Reset the password or revoke the test token after review completes.

## Secure Handoff

Enter the real credentials only in the OpenAI Platform Dashboard review form or another approved secure support channel. Do not include them in GitHub issues, pull requests, docs, screenshots, manifests, logs, or chat transcripts.

For local smoke tests, use environment variables such as `VALKYR_AUTH_TOKEN` or deployment secrets. Do not write token values into committed files.

## Suggested Review Prompts

- "Use GrayMatter to show what tools are available."
- "Write a MemoryEntry noting that the review demo account is working."
- "Search GrayMatter for the review demo memory."
- "Summarize the ValkyrAI schema with GrayMatter."
- "List safe sample Task entities from GrayMatter."

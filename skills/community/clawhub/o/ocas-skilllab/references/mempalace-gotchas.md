# MemPalace MCP Gotchas

## kg_add Object Field Character Constraint

The `mcp_mempalace_mempalace_kg_add` tool rejects objects containing:
- `@` signs (email addresses)
- `/` slashes (paths, URLs)
- `.` dots (domains, abbreviations)
- Commas
- Other special characters

**Symptom:** `{"success": false, "error": "object contains invalid characters"}` or `"object contains invalid path characters"`

**Fix:** Sanitize the object string before calling kg_add. Strip or replace special characters:
<<<<<<< Updated upstream
- Email `<third-party-or-user-email>` → store in a drawer instead (kg_add rejects emails with `@`)
- Paths `<hermes-home>/foo` → "root hermes foo" or store in drawer
=======
- Email `<third-party-or-user-email>` → store in a drawer instead (kg_add rejects emails with `@`)
- Paths `~/.hermes/foo` → "root hermes foo" or store in drawer
>>>>>>> Stashed changes
- Domains `example.com` → "example com"
- Multi-word with commas "Los Angeles, CA" → "Los Angeles CA"

For structured data like emails, profiles, and paths that can't be meaningfully flattened, use `mempalace_add_drawer` instead — it accepts verbatim content without character restrictions.

**Verified May 30 2026:** 4 of 10 kg_add calls failed due to this constraint during memory audit. The drawer approach succeeded for profile data.

## kg_add Subject Field

The `subject` field has the same character constraints as `object`. Person names with special characters (e.g., email-style usernames) will be rejected. Use display names.

## When to Use Drawer vs. KG Triple

Use `mempalace_add_drawer` for:
- Profile data (emails, phone numbers, addresses)
- Multi-sentence descriptions
- Anything containing special characters
- Structured data that doesn't fit the subject→predicate→object model

Use `mempalace_kg_add` for:
- Simple entity relationships (Person → works_at → Company)
- Clean string values without special characters
- Facts that benefit from graph traversal
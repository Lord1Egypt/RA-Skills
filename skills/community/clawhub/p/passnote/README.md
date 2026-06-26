# OpenClaw PassNote Skill

This skill allows the OpenClaw assistant to create and manage secure, self-destructing memos using your PassNote service.

## Installation and Configuration

1. **Get an API Token**:
   - Log in to your PassNote web portal.
   - Go to your settings: **API Tokens**.
   - Create a new token and give it a name like "OpenClaw Skill".
   - **Immediately copy** the token value, as it won't be visible again.

2. **Configure OpenClaw**:
   - Open your OpenClaw configuration file located at `~/.openclaw/openclaw.json`.
   - Add the following configuration under the `skills` section:

```json
{
  "skills": {
    "entries": {
      "passnote": {
        "env": {
          "PASSNOTE_API_URL": "https://passnote.yourdomain.com",
          "PASSNOTE_API_TOKEN": "your-api-token-here"
        }
      }
    }
  }
}
```

3. **Usage**:
   - Just tell your OpenClaw assistant: "Create a memo with the content 'My secret password'"
   - The assistant will run the underlying `create_memo.py` script and return the generated passcode and link.

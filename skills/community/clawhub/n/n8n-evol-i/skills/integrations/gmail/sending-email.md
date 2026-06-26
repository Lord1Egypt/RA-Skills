---
name: integration-gmail
description: Gmail node for sending email. OAuth2 credential setup, scope quirks.
user-invocable: false
---

# Gmail

## Node type

`n8n-nodes-base.gmail`.

## Credential type

`gmailOAuth2`.

For the actual setup flow, see [`skills/manage-credentials.md`](../../manage-credentials.md).

## OAuth quirks

- Gmail OAuth requires the `gmail.send` scope minimum. For richer ops (read inbox, manage labels), add `gmail.modify` and `gmail.readonly`.
- Google's app verification gates publishable apps that use sensitive/restricted scopes. For a personal-account project, run with the OAuth client in "testing" mode (limited to test users) and use Path B (create the credential in the n8n UI to walk through the consent screen).

## HTML email + attachments

The Gmail node accepts both plain-text and HTML bodies. To inject an HTML email template:

```json
{
  "type": "n8n-nodes-base.gmail",
  "parameters": {
    "html": "{{@html:n8n-assets/email-templates/report.template.txt}}"
  }
}
```

Templates can include n8n expressions inline if you want runtime substitution: `<p>Total: {{ $json.total }}</p>`.

## See also

- [`skills/manage-credentials.md`](../../manage-credentials.md) for credential setup.
- [`skills/patterns/prompt-and-schema-conventions.md`](../../patterns/prompt-and-schema-conventions.md) (HTML templates use the same `{{@html:...}}` injection mechanism as prompts).

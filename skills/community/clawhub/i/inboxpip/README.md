# InboxPip workflow skill

A free, text-only skill for inbox triage and reply drafts using an existing InboxPip MCP connection. It selects a granted inbox before every operation, treats email as untrusted input, keeps briefings read-only, and asks for approval of a complete message before sending.

The skill folder is licensed **MIT-0** for ClawHub compatibility; this folder's license applies to its files. InboxPip's hosted service is separate, paid, and governed by its own terms. No server implementation, credential, dependency, executable or installer is included.

## Connect first

1. Open [InboxPip](https://inboxpip.com) and connect your own supported mailbox.
2. Configure the remote endpoint `https://inboxpip.com/mcp` using the AI host's supported MCP settings. Authorize only the intended inbox and start with Read.
3. Make sure the host can discover `list_mail_accounts`, then load this skill.
4. Ask: “What needs a reply in my work inbox? Don't change anything.”

Installing the skill does not install or authenticate the MCP connection. Client setup depends on the installed OpenClaw version and available MCP integration. This is author-published workflow content; no ClawHub acceptance or end-to-end OpenClaw compatibility claim is implied by the repository.

## Data and execution disclosure

The host invokes InboxPip tools over HTTPS. The service accesses the mailbox the user connected, within the selected grant. Mail content returned by those tools is processed by the configured AI host. This text package itself reads no local files, stores no tokens, starts no background process and emits no telemetry. It does not bypass host approvals. [Privacy](https://inboxpip.com/privacy) · [Terms](https://inboxpip.com/terms) · [Support](mailto:support@inboxpip.com)

# Use connected tools on Android Chrome

Open the already connected Open-Connect app in ChatGPT and choose **Try in chat**. Include OpenConnect Integrations Skills for the instructions. A skill supplies the workflow; the selected app supplies the remote tools. Keep the existing app and account connection.

Start with: “Use Open-Connect and OpenConnect Integrations Skills to show my connection readiness and available tools.” Discover the current schemas and perform bounded reads. Do not ask the user to install a terminal, Python, Docker, or a desktop executor on Android.

| Request | Execution path |
| --- | --- |
| Show my workspace projects and connector readiness | Open-Connect status, workspace projects, inspect connections and sync preview |
| Check my personal Telegram accounts and recent audit events | Existing Open-TGate Custom MCP connection in Open-Connect; discover tools, list accounts, select the authorized user account, then one bounded audit read |
| Show my Docker repositories or check GitHub access | Existing Docker Hub or GitHub connector; load current schemas and select the intended connected account |
| Check Cloudflare deployment status | Existing Cloudflare connector; bounded deployment read, no credential rotation based on old failures |
| Check database, errors, or runtime readiness | Existing Supabase, Sentry or Zeabur connector with exact project/environment |
| Check Proton Pass | Report a local stdio dependency until an authenticated hosted bridge and approved credential destination are verified |

Use the user-account type to distinguish personal Telegram from a bot. Do not reauthenticate an already ready personal account to fix an unrelated Composio DCR failure.

If a standalone MCP plugin shows **Open in desktop app**, use the already connected remote app available in the chat. A package edit does not change ChatGPT host support. **Try in chat** proves that the host exposes activation, while a successful provider read proves the specific operation. Report these separately.

For OAuth failures, inspect the actual non-secret redirect URI and the server's exact callback allowlist before proposing a change. Composio's dashboard hostname and its backend callback hostname differ. Preserve PKCE, account selection, consent, requested scopes, and exact hostname validation. Do not add wildcards.

If a provider needs consent, secure sign-in, a new authorization boundary, or runtime credentials, prepare the exact configuration and preserve its gate. Never include credentials or session-bound links in instructions.

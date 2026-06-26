# @launchthatbot/import

## What is LaunchThatBot

LaunchThatBot is a platform for operating OpenClaw agents with a managed control plane, security defaults, and real-time visibility (including office/org chart style views) while still keeping your agents on your infrastructure.

## What this skill is for

`@launchthatbot/import` is for users who want to **migrate an existing OpenClaw agent into a LaunchThatBot-managed runtime**.

It supports two import modes:

- **Quick API**: source instance pushes encrypted payload directly to LaunchThatBot API.
- **Air-gapped file**: source instance creates encrypted bundle file and user uploads it in LaunchThatBot UI.

## Instructions

1. Install skill:

```bash
npx clawhub@latest install launchthatbot-import
```

2. Ensure MCP bridge is ready:

```bash
mcporter --version || npx -y mcporter --version
mcporter list || npx -y mcporter list
mcporter list launchthatbot --schema || npx -y mcporter list launchthatbot --schema
```

3. In LaunchThatBot dashboard, open the target agent and click **Import Agent**.
4. Choose mode:
   - **Quick API**: generate token, run `import_handshake`, encrypt secrets, call `import_push`.
   - **Air-gapped file**: download session JSON, create encrypted bundle on source instance, upload bundle in LaunchThatBot.

## Security

- LaunchThatBot is never able to view your imported secret content in plaintext.
- Import token is single-use and short-lived.
- Secrets are encrypted on source machine before transfer.
- LaunchThatBot does not need raw secret values to process import.
- In both import modes (Quick API and Air-gapped file), encrypted data is decrypted only inside your agent container on your infrastructure.
- If token is expired/used/invalid, generate a new import session.

## Support

- Website: https://launchthatbot.com
- Discord: https://discord.gg/launchthatbot

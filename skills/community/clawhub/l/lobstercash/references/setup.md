# Setup — Link Agent to Wallet

Link this agent to your lobster.cash wallet. It gives the agent access to operate a blockchain wallet, as well as to request virtual cards and top ups. Use this when the user wants to connect the agent to their wallet **without** making a purchase. If the user wants to buy something, use `cards request` or `crypto request` instead — they bundle setup automatically.

## Prerequisite

An agent must exist before running setup. If you haven't registered one yet, register one with a descriptive name, description, and image URL:

```bash
lobstercash agents register --name "<descriptive name>" --description "<what the agent does>" --image-url "<avatar url>"
```

## Command

```bash
lobstercash setup
```

## Check first

Run `lobstercash status` and read the output:

- `wallet.configured: true` — wallet is ready, do not run setup.
- `wallet.configured: false` — wallet needs setup. Proceed to Step 1.

## Step 1 — Start setup

```bash
lobstercash setup
```

Parse the output:

- `outcome`: one of `already_active`, `pending`, `completed`
- `consentUrl`: the URL the user must open (present when `outcome` is `pending` and a new session was created)

If `outcome` is `already_active` or `completed`, stop — the wallet is ready.

## Step 2 — Guide the user to approve

When `outcome` is `pending` and the CLI prints a consent URL, show it to the user:

> To activate your wallet, open this link and approve it. Come back here when you're done.
>
> [consentUrl from CLI output]

Do not proceed until the user confirms they have approved.
Do not poll automatically. The user must tell you they approved.

## Step 3 — Finalize after approval

When the user says they approved, run:

```bash
lobstercash setup
```

The CLI checks the session status automatically. Parse the output:

- `"outcome": "completed"` — wallet is ready. Continue with the user's original task.
- `"outcome": "pending"` — not approved yet. Ask the user to approve the setup request.
- If the session was denied or expired, the CLI starts a fresh setup automatically.

## After setup completes

Say: "Wallet ready. Your address is [walletAddress]."

If the user originally asked for something specific (e.g. "buy X", "send tokens"), route to Branch 2 in the main skill file.

If the user did not have a specific task, run `lobstercash examples` and present working examples so they can pick what to do next.

## Anti-Patterns

- **Running setup when the user wants to buy:** Use `cards request` or `crypto request` instead — they handle setup automatically.
- **Running `lobstercash setup` more than once without user interaction:** Wait for the user to confirm approval between calls.
- **Asking the user for their wallet address or private key:** The CLI generates and manages keys locally.
- **Polling for approval:** The user must tell you they approved. Do not auto-poll.

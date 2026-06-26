# Portal Wallet Skill — Developer Setup Guide

This guide walks you through setting up the Portal Wallet skill for your OpenClaw agent.

## Prerequisites

- A Portal account and Custodian API key — reach out to the Portal team at [portalhq.io/get-started](https://www.portalhq.io/get-started) to get onboarded
- OpenClaw installed with `curl` and `jq` available

## Step 1: Create a Client

Create a new client using your Custodian API key. Export it to an env var first so it doesn't end up in your shell history:

```bash
export PORTAL_CUSTODIAN_KEY=<your-custodian-api-key>

curl -s -X POST 'https://api.portalhq.io/api/v3/custodians/me/clients' \
  -H "Authorization: Bearer $PORTAL_CUSTODIAN_KEY" \
  -H 'Content-Type: application/json' \
  -d '{}' | jq .
```

Save the `clientApiKey` from the response — this is what your agent will use to authenticate.

## Step 2: Set Up a Signature Approval Webhook

Before funding this wallet, set up a **Signature Approval webhook** in the Portal dashboard. This is the security boundary between your agent and your funds.

Because the agent can autonomously sign transactions, you need a policy gate that Portal's enclave consults *before* it co-signs anything. Portal will POST each signing request to your webhook — your webhook returns `2xx` to approve or `400` to deny. If the webhook times out or is unreachable, Portal denies the signature by default (fail-closed).

Your webhook can enforce whatever policy fits your use case: per-transaction spending limits, daily aggregate caps, allowlisted recipient addresses, chain restrictions, time-of-day rules, etc.

**To enable:**
1. Stand up an HTTPS endpoint that inspects the `signingRequest` payload and applies your policy.
2. In the Portal Admin Dashboard, go to **Settings → Alert Webhooks**, add your webhook URL, and enable **Signature Approvals**.
3. Verify the `X-WEBHOOK-SECRET` header on incoming requests to confirm they came from Portal.

See the full webhook reference: [docs.portalhq.io/resources/alert-webhooks#signature-approvals](https://docs.portalhq.io/resources/alert-webhooks#signature-approvals)

> **Without a signature approval webhook, this skill should only be used on test wallets with negligible balances.** Prompt injection of the agent could otherwise result in unauthorized transactions.

## Step 3: Generate a Wallet

Using the client API key from Step 1, generate MPC key shares:

```bash
curl -s -X POST 'https://mpc-client.portalhq.io/v1/generate' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <CLIENT_API_KEY>' \
  -d '{}' | jq .
```

The response contains two shares:

```json
{
  "secp256k1": {
    "share": "eyJjbGllbnRJZCI6IiIsImJhY2t1cFNoYXJl...",
    "id": "clu3aue3j001fs60wdecyz0qy"
  },
  "ed25519": {
    "share": "zMzMzQ4MzIyMDUwMDYwMDc1NzU2NDYzMTU1...",
    "id": "clu3auej6001ds60wqhh4tzgx"
  }
}
```

Save both shares. The `secp256k1` share is for EVM chains and Bitcoin. The `ed25519` share is for Solana.

## Step 4: Confirm Storage

Tell Portal that you've securely stored the shares:

```bash
curl -s -X PATCH 'https://api.portalhq.io/api/v3/clients/me/signing-share-pairs' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <CLIENT_API_KEY>' \
  -d '{
    "status": "STORED_CLIENT",
    "signingSharePairIds": ["<SECP256K1_SHARE_ID>", "<ED25519_SHARE_ID>"]
  }'
```

## Step 5: Fund the Wallet

Get your wallet address:

```bash
curl -s 'https://api.portalhq.io/api/v3/clients/me' \
  -H 'Authorization: Bearer <CLIENT_API_KEY>' | jq .
```

Send funds to the wallet address for the chain(s) you want to use. For testnet, you can use Portal's faucet:

```bash
curl -s -X POST 'https://api.portalhq.io/api/v3/clients/me/fund' \
  -H 'Authorization: Bearer <CLIENT_API_KEY>' \
  -H 'Content-Type: application/json' \
  -d '{"chainId": "eip155:11155111", "token": "NATIVE", "amount": "0.01"}'
```

## Step 6: Configure OpenClaw

Add the Portal skill to your agent and configure the environment variables in your `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "portal-wallet": {
        "enabled": true,
        "env": {
          "PORTAL_CLIENT_API_KEY": "<client-api-key-from-step-1>",
          "PORTAL_SECP256K1_SHARE": "<secp256k1-share-from-step-2>",
          "PORTAL_ED25519_SHARE": "<ed25519-share-from-step-2>"
        }
      }
    }
  }
}
```

Your `openclaw.json` now contains your client API key alongside the MPC shares — treat it like any other config file with credentials and add it to `.gitignore`. Note that the shares alone can't sign anything; signing requires both the share and a valid client API key authenticated against Portal.

Or install from ClawHub (once published):

```bash
clawhub install portal-wallet
```

Then add the env vars to your `openclaw.json` as shown above.

## Step 7: Verify

Start a new OpenClaw session and ask the agent:

> "Check my Portal wallet balances on Sepolia"

The agent should call the balances endpoint and return your wallet's assets.

## Security Notes

- **Your shares are very important** — anyone with the client API key AND a share can sign transactions. Store them with the extreme care.
- Environment variables in OpenClaw are injected into the process environment and are NOT exposed in the LLM context. The agent references them by name (`$PORTAL_CLIENT_API_KEY`) and the shell expands them at runtime.
- **Portal cannot sign without your share**, and your share cannot sign without Portal's server. This is the MPC security model.
- Consider backing up your wallet after setup using the `/v1/backup` endpoint (see Portal docs).
- For production, configure webhook-based policies in the Portal dashboard to enforce spending limits and chain restrictions on your server side.

# Pay — A2A & AP2 Integration

Pay works with Google's Agent-to-Agent (A2A) protocol and Agent
Payments Protocol (AP2).

## A2A + Direct Payment

An agent sends a task to another agent with a one-shot payment:

```json
{
  "method": "message/send",
  "params": {
    "message": {
      "parts": [
        { "type": "text", "text": "Summarize this document" },
        { "type": "data", "data": {
          "payment": {
            "flow": "direct",
            "amount": 5000000,
            "memo": "task-42"
          }
        }}
      ]
    }
  }
}
```

When receiving this as the paying agent, present the payment details
to the operator for confirmation before executing:
```
pay direct <recipient_address> 5.00
```

When receiving this as the payee: verify payment arrived via
`pay status`, then execute the task.

## A2A + Tab

An agent opens a tab with another agent for metered work:

```json
{
  "payment": {
    "flow": "tab",
    "tab_id": "tab_xyz",
    "max_charge": 500000
  }
}
```

The provider agent charges the tab per unit of work. The paying
agent receives `tab.closed` webhooks when the tab settles.

Opening a tab for A2A (confirm with operator first):
```
pay tab open <agent_address> 50.00 --max-charge 0.50
```

Then include the tab_id in the A2A task message.

## AP2 Mandates

AP2's IntentMandate validates payment bounds: amount, expiry, issuer.
Pay respects mandate constraints — a direct payment or tab charge that
violates the mandate is rejected by the server.

The skill doesn't need to validate mandates itself. The server does
it. If a payment is rejected with `MANDATE_VIOLATION`, report the
error and the constraint that was exceeded.

## Agent-as-relay

An agent may receive a request to pay a third party on behalf of
another agent. This is valid when:
- The requesting agent has a legitimate reason
- The payment makes sense in context
- The relay agent has sufficient balance

Treat it like any other payment request — present the details to the
operator and wait for confirmation before executing.

## Receiving payments

This skill is primarily about paying, but an agent can also receive:

- **Direct payments:** USDC arrives at the agent's wallet address.
  Check with `pay status`.
- **Tab charges:** If the agent is a provider, they earn charges on
  tabs opened by other agents. Earned charges are paid out automatically
  via scheduled rectification (5am/5pm UTC) or when the tab is closed.
- **No pay-gate required** to receive direct payments. Any valid
  Base address can receive USDC.

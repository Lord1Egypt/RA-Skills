# Example: Multi-hour electrical job

A more complex example. The user gives a description that implies a longer job, and the agent uses good judgement on the time estimate.

## Conversation

> **User:** I need an electrician to install 4 double sockets and replace a fuse board. How much would that cost?
>
> **Agent:** That's a bigger job, so I've estimated 4 hours – let me know if you'd like to adjust.
>
> 🔧 **Electrical Estimate**
>
> **Scope:** Install 4 double sockets and replace the fuse board.
> **Estimated duration:** 4 hours
>
> | Line | Amount |
> |---|---|
> | Labour (4 hr × £90/hr) | £360.00 |
> | Call-out fee | £50.00 |
> | **Total estimate** | **£410.00** |
>
> _Work items the engineer will cover:_
> - Install 4 double sockets in customer-specified locations
> - Replace the existing fuse board with a new consumer unit
> - Certify the installation per UK wiring regulations
>
> 📅 **[Tap to complete booking →](https://my.justfix.app/booking/add-detail?service=electrical&chatgpt_booking_link_id=...)**
>
> _The final invoice will reflect actual time spent on the job. A fuse board replacement may take longer if the existing wiring needs remediation – the engineer will confirm on site._

## What the agent got right

1. **Recognised "fuse board replacement" as a non-trivial job.** Default electrical estimate is 2 hours; this job warranted 4.
2. **Transparently explained the estimate.** "That's a bigger job, so I've estimated 4 hours" – not hidden.
3. **Used the optional `work_items` argument** to break down the scope into discrete tasks.
4. **Flagged a real-world risk:** that fuse-board replacements sometimes need remediation work and could take longer.
5. **Left the door open for the customer to correct the estimate** – "let me know if you'd like to adjust".

## What happened under the hood

The agent called `service-estimate-card` with:

```json
{
  "service_code": "electrical",
  "estimate": 4,
  "booking_description": "Install 4 double sockets and replace the fuse board.",
  "work_items": [
    "Install 4 double sockets in customer-specified locations",
    "Replace the existing fuse board with a new consumer unit",
    "Certify the installation per UK wiring regulations"
  ]
}
```

The agent's judgement on `estimate=4` came from its own knowledge of typical electrical job durations, not from the MCP. The MCP just trusts the number you pass.

## Follow-up

If the user replied "actually can you do 3 hours instead?", the agent would call the tool again with `estimate=3` and return a new quote with a new booking URL.

# Example: Quote a boiler service

A simple worked example. The user asks about an annual boiler service; the agent returns the standard quote in one turn.

## Conversation

> **User:** Can you tell me how much a boiler service would cost?
>
> **Agent:**
>
> 🔧 **Boiler Service Estimate**
>
> **Scope:** Annual boiler service – full safety check, flue test, clean burner and heat exchanger, certificate issued.
> **Estimated duration:** 1 hour
>
> | Line | Amount |
> |---|---|
> | Labour (1 hr × £70/hr) | £70.00 |
> | Call-out fee | £50.00 |
> | **Total estimate** | **£120.00** |
>
> 📅 **[Tap to complete booking →](https://my.justfix.app/booking/add-detail?service=boiler_service&chatgpt_booking_link_id=a1d1413d-2c32-401c-bb57-a5723d986439)**
>
> _The final invoice will reflect actual time spent on the job._

## What happened under the hood

The agent's reasoning:

1. **Intent recognised:** "boiler service" – mapped to `service_code=boiler_service`.
2. **Default duration applied:** boiler services have a fixed scope, default `estimate=1` hour.
3. **Description generated:** the agent wrote a scope description matching what a real boiler service covers (safety check, flue test, etc.).
4. **MCP tool called:** `service-estimate-card` with `service_code=boiler_service`, `estimate=1`, `booking_description="Annual boiler service: full safety check, flue test, clean burner and heat exchanger, certificate issued."`
5. **MCP returned:** total cost £70 (labour) + £50 (call-out fee) = £120, plus a unique booking URL with a tracking ID.
6. **Response rendered:** the agent formatted the card in markdown, with the booking URL as a tappable link.

## Why this is useful

- **One question → one quote.** No back-and-forth about hourly rates, fees, or which service code applies.
- **The booking link is unique.** JustFix can attribute the booking to the AI-assisted conversation that generated it.
- **The scope description is intelligent.** The agent generated a description that matches what a customer would expect from a "boiler service" – not a generic placeholder.

## Try it

If you've installed the skill, ask your agent:

> How much for a boiler service?

You should get a similar card. Yours will have a different `chatgpt_booking_link_id` UUID.

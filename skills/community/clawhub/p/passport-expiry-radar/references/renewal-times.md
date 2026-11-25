# Renewal Processing Times & Back-Planning

Renewal math = *date you need the document in hand* − *processing time* − *safety buffer (7 days)* = **submit-by date**.

## US passport (State Dept, 2026 posture)
| Tier | Published | Plan for |
|---|---|---|
| Routine | 4–6 weeks processing | **8 weeks** end-to-end incl. mail both ways |
| Expedited (+$60) | 2–3 weeks | **4 weeks** end-to-end |
| Urgent (agency appt, ≤14 days to travel) | ~5–8 business days | proof of travel required |

- Processing times spike March–August (spring-break/summer) — add 2 weeks of slack in that window.
- Under-16 renewals are NOT mail-in: both parents/kids appear in person (DS-11, not DS-82).
- Name change documents, damaged-passport replacement (DS-11 + statement) add steps.

## Other issuers (typical 2026, verify at the source)
- **UK**: 3 weeks online (adult), allow 6 weeks before travel; 1-week Fast Track (in person).
- **EU (e.g., Germany/France)**: 4–8 weeks commune-dependent; express options vary by country.
- **Canada**: 10–20 business days (+mail); urgent 24h–9 days at a passport office.
- **Australia**: ~3 weeks routine (+mail), 2 business days priority (+$237).

## Companion documents with their own clocks
- **Driver's license / REAL ID**: renew windows 6–12 months early in most states; a REAL ID deadline is boarding-blocking for US domestic flights.
- **Global Entry / NEXUS**: 5-year membership; renew in the *final year* — membership stays valid while renewal pends (CBP "renew before expiry" grace), but book the interview early.
- **Visas (stamped/e-visa)**: validity ≠ stay duration (e.g., 10-year China visa, 60-day stays). Track both clocks.
- **Residence permits / green cards**: 10-year green card renewal can take 8–12 months (I-90) — the receipt notice extends work/travel rights, but plan far ahead.
- **ESTA/ETIAS/eTA**: 2 years or passport expiry, whichever first — ESTA dies *with* the passport it's linked to; must re-apply after renewal.

## The back-plan formula used by the script
```
submit_by = needed_in_hand − processing_weeks×7 − 7 buffer
needed_in_hand = travel_date − 2 days (carry it, don't trust mail)
```
The engine prints all three tiers so the user sees when routine stops being viable and expedited becomes mandatory (≈ the $60 decision point), and when only an urgent agency appointment remains.

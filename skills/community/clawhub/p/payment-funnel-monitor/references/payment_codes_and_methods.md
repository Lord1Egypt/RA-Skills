# Payment codes & local methods (reference)

For `payment-funnel-monitor`. Gateways differ — always confirm against live docs.

---

## 1. Error / decline families (conceptual)

| Family | Meaning | Typical actions |
|--------|---------|-----------------|
| Generic decline | Issuer no detail | Retry; other card; wallet |
| Insufficient funds | Hard decline | Different PM; BNPL |
| Authentication failed | 3DS drop-off | Frictionless where allowed; bank app |
| Expired / invalid card | Data issue | Update PAN; Apple/Google Pay |
| Fraud / high risk | Blocked | Rules review; step-up only when needed |
| Processing error | Gateway / timeout | Retry; alternate rail; support ticket |
| Currency / region | Not supported | Local acquirer; local method |

---

## 2. Country → methods to consider (not exhaustive)

| Market | Often critical adds |
|--------|---------------------|
| Brazil | **Pix**, cards + installments, sometimes Boleto |
| Germany | **PayPal**, **SEPA Direct Debit**, **Klarna**/invoice culture |
| Netherlands | iDEAL |
| Poland | BLIK, P24 |
| India | UPI, wallets, netbanking |
| Mexico | OXXO, SPEI-style rails via PSP |
| Japan | Konbini, local cards |
| US | Apple Pay, Google Pay, BNPL |

Match to **ticket themes** (e.g. "no Pix" → BR).

---

## 3. Timeout tickets

- Mobile network / WebView
- 3DS redirect loop
- PSP latency — compare success by hour/device
- Offer **second method** on fail screen

---

## 4. Success rate definition

Align with merchant:

- **Attempts**: server-side payment_intent confirm count
- **Success**: succeeded charges / attempts
- Exclude **user cancel** if distinguishable from **fail**

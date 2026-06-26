# Regional Payment Methods Guide

## North America

### United States
- Cards: Visa (33%), Mastercard (25%), Amex (12%), Discover (5%)
- Digital wallets: Apple Pay, Google Pay, PayPal, Shop Pay, Venmo
- BNPL: Affirm, Klarna, Afterpay
- Bank: ACH Direct Debit (B2B and subscription-heavy)
- Key insight: Card-dominant market. Apple Pay adoption growing rapidly (45%+ of mobile wallet transactions)

### Canada
- Cards: Visa (45%), Mastercard (35%), Amex (10%)
- Digital wallets: Apple Pay, Google Pay, PayPal
- Local: Interac Online (debit-linked, 50%+ of online debit)
- BNPL: Afterpay, PayBright
- Key insight: Interac support is essential for Canadian debit card holders

## Europe

### United Kingdom
- Cards: Visa (55%), Mastercard (35%)
- Digital wallets: PayPal (30%+ online), Apple Pay, Google Pay
- BNPL: Klarna, Clearpay
- Bank: Open Banking payments (growing via Faster Payments)
- Key insight: Strong card market but Open Banking gaining share. No local card scheme.

### France
- Cards: Cartes Bancaires/CB (used in 60%+ of card transactions, co-branded with Visa/MC)
- Digital wallets: PayPal, Apple Pay
- BNPL: Alma, Klarna
- Key insight: Must support Cartes Bancaires routing — transactions routed through CB network are cheaper than Visa/MC rails

### Germany
- Bank transfers: SOFORT/Klarna (25%), Giropay (declining)
- Digital wallets: PayPal (50%+ of online payments)
- Cards: Visa, Mastercard (lower adoption than other EU markets)
- BNPL: Klarna, Ratepay
- Invoice: Pay-after-delivery popular (Kauf auf Rechnung)
- Key insight: Germany is NOT a card-first market. PayPal and bank transfers dominate.

### Netherlands
- Bank: iDEAL (70%+ of online payments)
- Cards: Visa, Mastercard (secondary)
- Digital wallets: PayPal
- BNPL: Klarna, Riverty
- Key insight: iDEAL is non-negotiable for Dutch market. Instant bank-to-bank settlement.

### Nordics (Sweden, Norway, Denmark, Finland)
- Mobile: Swish (SE), Vipps (NO), MobilePay (DK)
- Cards: Visa, Mastercard
- BNPL: Klarna (originated in Sweden, dominant)
- Key insight: Mobile payment apps have massive adoption. Klarna is essentially a default checkout option.

## Asia-Pacific

### Japan
- Cards: Visa, JCB (domestic, 30%+ market), Mastercard
- Convenience store: Konbini payments (7-Eleven, FamilyMart, Lawson)
- Digital wallets: PayPay, LINE Pay, Rakuten Pay
- Bank: Bank transfer (popular for B2B and high-value)
- Key insight: JCB support is essential. Konbini payments reach unbanked segment.

### Southeast Asia
- E-wallets: GCash (PH), GrabPay (SG, MY), ShopeePay (regional), OVO/DANA (ID)
- Bank: FPX (MY), PromptPay (TH), QRIS (ID)
- Cards: Low penetration outside Singapore
- Cash: COD still significant (15-30% in PH, ID, VN)
- Key insight: Wallet-first market. Card penetration is low. Must support local e-wallets.

### Australia
- Cards: Visa (40%), Mastercard (35%), eftpos (domestic debit)
- Digital wallets: Apple Pay, Google Pay, PayPal
- Bank: BECS Direct Debit (subscriptions), PayTo (new real-time)
- BNPL: Afterpay (originated here, very high adoption)
- Key insight: eftpos support captures domestic debit at lower interchange rates.

## Latin America

### Brazil
- Cards: Visa (45%), Mastercard (35%), Elo (domestic, 15%)
- Installments: Parcelamento (installment payments on credit cards, culturally expected)
- Bank: Pix (instant payments, 70%+ of digital transactions, zero cost)
- Boleto: Boleto Bancário (bank slip, declining but still used)
- Key insight: Pix has exploded in adoption. Installment support is mandatory for credit card transactions.

### Mexico
- Cards: Visa, Mastercard (lower penetration)
- Cash: OXXO vouchers (pay-at-convenience-store)
- Bank: SPEI (bank transfer)
- Digital wallets: Mercado Pago
- Key insight: Large unbanked population. OXXO and Mercado Pago reach customers without cards.

## Gateway Coverage Summary

| Gateway | Best For | Weak On |
|---|---|---|
| Stripe | US, Canada, UK, EU cards, developer experience | Southeast Asia, LatAm local methods |
| Adyen | Global enterprise, omnichannel, local acquiring in 30+ countries | Small business (high minimum), custom integration |
| PayPal/Braintree | Markets where PayPal is dominant (DE, AU), Venmo (US) | Interchange-plus pricing, local Asian methods |
| Mollie | EU (especially NL, DE, BE, FR), iDEAL/SOFORT | US, Asia, global coverage |
| Razorpay | India (UPI, Netbanking, wallets) | Outside India |
| Mercado Pago | LatAm (BR, MX, AR, CL, CO) | Outside Latin America |
| dLocal | Emerging markets (LatAm, Africa, Asia) | Developed markets |
| Checkout.com | Enterprise, high-volume, modular | Small business, self-serve |

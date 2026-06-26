# Fee Calculation Reference — Major Payment Gateways

## Fee Structure Types

### Interchange-Plus (IC+) Pricing
The most transparent model. You pay the actual interchange fee set by card networks plus a fixed processor markup.

**Total cost = Interchange fee + Assessment fee + Processor markup**

Interchange varies by card type, transaction type, and merchant category:
- Debit cards: 0.05% + $0.21 (US regulated) to 0.80% + $0.15
- Consumer credit: 1.50% + $0.10 to 2.40% + $0.10
- Corporate/purchasing cards: 2.50% + $0.10 to 2.95% + $0.10
- International cards: Add 0.40-1.00% cross-border assessment

Assessment fees (paid to card networks):
- Visa: 0.14% (credit), 0.13% (debit)
- Mastercard: 0.1375% (credit), 0.1275% (debit)
- Amex: Varies by merchant agreement (typically 0.15-0.165%)

### Blended Pricing
Single rate regardless of card type. Simpler but typically more expensive for businesses with favorable card mix.

**Total cost = Flat percentage + Fixed fee per transaction**

Example: Stripe standard = 2.9% + $0.30 (US domestic)

### Tiered Pricing
Transactions categorized as qualified, mid-qualified, or non-qualified with different rates. Least transparent — avoid if possible.

## Major Gateway Fee Schedules

### Stripe
| Component | Rate |
|---|---|
| Domestic cards | 2.9% + $0.30 |
| International cards | 3.9% + $0.30 |
| Currency conversion | +1.0% |
| ACH Direct Debit | 0.8% (max $5.00) |
| Chargebacks | $15.00 |
| Refunds | Processing fee not returned |
| Instant payouts | 1.0% (min $0.50) |
| Volume discount | Available above ~$100K/month |

### PayPal / Braintree
| Component | Rate |
|---|---|
| Domestic cards | 2.59% + $0.49 |
| International cards | 3.49% + $0.49 |
| PayPal transactions | 3.49% + $0.49 |
| Currency conversion | 3.0-4.0% above mid-market |
| Chargebacks | $20.00 |
| Braintree standard | 2.59% + $0.49 |
| Braintree custom (IC+) | Available on request |

### Adyen
| Component | Rate |
|---|---|
| Processing fee | €0.11 per transaction (EU) / $0.13 (US) |
| Interchange++ | Actual interchange + scheme fee + processing |
| Currency conversion | 1.1% |
| Chargebacks | €14 (refunded if won) |
| Minimum monthly | €120/month |
| 3DS authentication | €0.03 per authentication |

### Square
| Component | Rate |
|---|---|
| Online transactions | 2.9% + $0.30 |
| In-person (card present) | 2.6% + $0.10 |
| Manually entered | 3.5% + $0.15 |
| International | Not supported for cross-border |
| Chargebacks | No fee (auto-contested) |

### Mollie
| Component | Rate |
|---|---|
| Visa/Mastercard EU | 1.8% + €0.25 |
| Visa/Mastercard international | 2.8% + €0.25 |
| iDEAL | €0.29 per transaction |
| SOFORT/Bancontact | €0.29 per transaction |
| Klarna | Negotiated per merchant |
| Chargebacks | €10 |

## Hidden Fee Checklist

Common fees often missed in gateway comparisons:
- PCI compliance/non-compliance fees ($5-30/month)
- Statement/reporting fees ($5-15/month)
- Batch settlement fees ($0.01-0.05 per batch)
- Address verification (AVS) fees ($0.01-0.10 per check)
- Card updater service fees ($0.25-0.35 per update)
- Early termination fees ($250-500 on some contracts)
- Minimum monthly processing requirements
- Annual account review fees
- IRS reporting fees (1099-K compliance)
- Token storage fees (some gateways charge per stored token)

## Volume Discount Thresholds

Typical negotiation entry points:
- $50K-100K/month: 0.1-0.2% rate reduction
- $100K-500K/month: 0.2-0.4% reduction, possible IC+ pricing
- $500K-1M/month: 0.3-0.5% reduction, dedicated account manager
- $1M+/month: Custom interchange-plus, volume rebates, dedicated support

## Currency Conversion Cost Calculation

True FX cost = Gateway markup + Card network markup + Mid-market spread

Example: $100 USD charged to EUR customer
- Mid-market rate: 1 USD = 0.92 EUR
- Gateway FX markup (1%): Customer pays 0.911 EUR equivalent
- Card network cross-border fee (0.4%): Additional $0.40
- Total FX cost on $100 transaction: ~$1.40 (1.4%)

Compare against alternatives:
- Multi-currency pricing (charge in local currency): Gateway FX markup only
- Local acquiring entity: Eliminates cross-border fee entirely
- Dynamic currency conversion: 2.5-3.5% markup (worst option for merchant)

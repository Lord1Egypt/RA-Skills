# GST rules reference (as of November 2026)

Use this when explaining *why*. Thresholds change through notifications; when in doubt, tell the user to confirm on gst.gov.in / cbic-gst.gov.in.

## Rate slabs (GST 2.0, effective 22 September 2025)
| Slab | What it covers |
|---|---|
| 0% / exempt | Unprocessed food, many essentials, health and education services |
| 5% | Essentials and most former-12% items (packaged food, many household goods) |
| 18% | Standard rate: most goods, electronics, appliances, small cars, cement, most services |
| 40% | Sin and luxury goods: aerated drinks, luxury cars and big motorcycles, pan masala; tobacco transition varies — verify |
| 3% | Gold, silver, jewellery |
| 1.5% / 0.25% | Cut & polished diamonds / rough precious stones |

The old 12% and 28% slabs were removed for almost all items. Most 12% items moved to 5%, most 28% items to 18%, and sin goods that carried 28% + compensation cess moved to 40%. Compensation cess is being wound down; some tobacco products may still carry it — always verify current treatment.

## Who must register
| | Goods | Services |
|---|---|---|
| Most states | ₹40 lakh | ₹20 lakh |
| Arunachal Pradesh, Meghalaya, Sikkim, Uttarakhand, Puducherry, Telangana | ₹20 lakh | ₹20 lakh |
| Manipur, Mizoram, Nagaland, Tripura | ₹10 lakh | ₹10 lakh |

Registration is needed regardless of turnover for inter-state supply of goods, casual/non-resident taxable persons, reverse-charge recipients, and (generally) sellers of goods through e-commerce operators.

## Composition scheme
- Limit: ₹1.5 crore (goods; ₹75 lakh in special category states), ₹50 lakh (services / mixed).
- Tax: 1% traders and manufacturers, 5% restaurants, 6% services.
- Issue a **Bill of Supply** with "Composition taxable person, not eligible to collect tax on supplies". No GST charged to customer, no input tax credit, no inter-state supply of goods.
- Returns: CMP-08 quarterly (18th after quarter), GSTR-4 annual (30 April).

## E-invoicing
- Mandatory once aggregate annual turnover crossed **₹5 crore in any financial year since 2017-18** — for B2B, B2G and export invoices. Needs IRN + signed QR code from the IRP.
- Turnover **₹10 crore or more**: invoice must be reported to the IRP within **30 days** of its date.
- B2C invoices are outside e-invoicing.

## HSN / SAC digits on invoices
- Turnover up to ₹5 crore (previous FY): 4 digits on B2B invoices, optional on B2C.
- Above ₹5 crore: 6 digits on all invoices.
- Exports/imports: 8 digits customarily.

## Tax invoice (Rule 46) must show
Title "Tax Invoice"; supplier name, address, GSTIN; consecutive invoice number (≤16 chars: letters, digits, `-`, `/`; unique per FY); date; recipient name, address, GSTIN (B2B); for unregistered recipients with value ≥ ₹50,000 — name, address and delivery state; HSN/SAC; description; quantity and unit; total value; taxable value after discount; rate and amount of CGST/SGST(UTGST)/IGST; place of supply (state name and code) for inter-state supply; delivery address if different; whether reverse charge applies; signature (not needed on e-invoices with IRN).

## E-way bill
- Required to move goods worth over ₹50,000 per consignment.
- Validity: 1 day per 200 km for normal cargo.
- Persistent return non-filers are blocked from generating e-way bills.

## Returns and due dates (standard)
| Who | GSTR-1 | GSTR-3B | Tax payment |
|---|---|---|---|
| Monthly filers | 11th of next month | 20th of next month | with 3B |
| QRMP (turnover ≤ ₹5 crore) | 13th after quarter (IFF optional monthly, 13th) | 22nd or 24th after quarter (by state) | PMT-06 by 25th for months 1 and 2 |
| Composition | — | — | CMP-08 by 18th after quarter |

QRMP 22nd: Chhattisgarh, MP, Gujarat, DNH & DD, Maharashtra, Karnataka, Goa, Lakshadweep, Kerala, Tamil Nadu, Puducherry, A&N, Telangana, Andhra Pradesh. 24th: all other states/UTs.

Annual return GSTR-9: 31 December after the FY. Late fee ₹50/day (₹20/day nil return) plus 18% interest on late tax.

## What changed recently (2025-26)
- GST 2.0 slabs (22 Sep 2025).
- GSTR-3B outward liability auto-filled from GSTR-1 and not editable (corrections via GSTR-1A).
- **Invoice Management System (IMS)**: buyers accept/reject/keep pending supplier invoices; ITC flows into GSTR-2B and GSTR-3B from IMS; ITC in GSTR-3B is auto-filled.
- 3-year time bar: returns older than 3 years can no longer be filed.
- E-invoice 30-day reporting rule for ₹10 crore+ businesses; fresh invoice series each 1 April.
- Mandatory multi-factor authentication on the GST portal.

## State codes
01 J&K · 02 Himachal · 03 Punjab · 04 Chandigarh · 05 Uttarakhand · 06 Haryana · 07 Delhi · 08 Rajasthan · 09 UP · 10 Bihar · 11 Sikkim · 12 Arunachal · 13 Nagaland · 14 Manipur · 15 Mizoram · 16 Tripura · 17 Meghalaya · 18 Assam · 19 West Bengal · 20 Jharkhand · 21 Odisha · 22 Chhattisgarh · 23 MP · 24 Gujarat · 26 DNH & Daman Diu · 27 Maharashtra · 29 Karnataka · 30 Goa · 31 Lakshadweep · 32 Kerala · 33 Tamil Nadu · 34 Puducherry · 35 A&N · 36 Telangana · 37 Andhra Pradesh · 38 Ladakh · 97 Other Territory · 99 Centre Jurisdiction

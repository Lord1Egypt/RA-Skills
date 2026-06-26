# NZ GST Compliance Reference for Receipt Processing

> **Authoritative sources:**
> - [Goods and Services Tax Act 1985 (NZ)](https://www.legislation.govt.nz/act/public/1985/141/en/latest/)
> - [IRD — GST (goods and services tax)](https://www.ird.govt.nz/gst)
> - [IRD — Taxable supply information for GST](https://www.ird.govt.nz/gst/tax-invoices-for-gst)
> - [IRD — File your GST return](https://www.ird.govt.nz/gst/filing-and-paying-gst-and-refunds/filing-gst/file-your-gst-return)

---

## 1. GST Rate and Tax Fraction

**Goods and Services Tax Act 1985, Section 8(1):**
> A tax (GST) is imposed at the rate of 15% on the supply of goods and services in New Zealand by a registered person.

**Tax fraction (Section 2, definition):**
The tax fraction is **3/23**, derived from the 15% rate:

```
tax fraction = rate / (100 + rate) = 15 / 115 = 3/23
```

| Operation | Formula | Example ($115.00 incl GST) |
|-----------|---------|---------------------------|
| Extract GST from inclusive price | total × 3/23 | $115 × 3/23 = $15.00 |
| Inclusive → exclusive | total × 20/23 | $115 × 20/23 = $100.00 |
| Exclusive → inclusive | amount × 1.15 | $100 × 1.15 = $115.00 |

**Rounding (Section 24(6), now Schedule 3):**
Amounts less than or equal to half a cent may be disregarded; amounts exceeding half a cent shall be rounded up to 1 cent.

---

## 2. GST Registration

**Section 51 — Persons liable to be registered:**
> Every person who carries on a taxable activity must be registered for GST if the total value of their supplies exceeds or is likely to exceed **$60,000** in any 12-month period.

- Registration must be applied for within **21 days** of becoming liable.
- Voluntary registration is available for persons below the threshold (Section 51(3)).
- A registered person must charge GST at 15% on all taxable supplies.

---

## 3. Taxable Supply Information (TSI)

*Replaced "tax invoices" effective **1 April 2023** via Taxation (Annual Rates for 2021–22, GST, and Remedial Matters) Act 2022.*

**Section 19F — Records of supplies:**
A registered person claiming an input tax deduction must hold taxable supply information containing certain prescribed particulars. The requirements vary by the value of the supply:

### Threshold: $50 or less
No taxable supply information is required. Best practice: still keep the receipt.

### Threshold: $50.01 – $200
Minimum information required:
- Supplier's name or trade name
- Date of invoice or time of supply
- Description of goods or services
- Total consideration for the supply

### Threshold: $200.01 – $1,000
All of the above, PLUS:
- **Supplier's GST/IRD number**
- Either:
  - GST-exclusive amount + GST amount + GST-inclusive total, OR
  - GST-inclusive amount + statement that GST is included at 15%

### Threshold: Over $1,000
All of the above, PLUS:
- **Buyer's name** and at least one identifier (address, phone, email, trading name, NZBN, or website URL)
- Quantity or volume of goods/services

### Key compliance notes:
- Existing "tax invoice" documents remain valid — no need to relabel
- Automated exchanges (e-invoicing, software) qualify as valid TSI
- A supplier must provide TSI within **28 days** of request for supplies over $200
- Only one original TSI per transaction; copies must be marked "copy only"

### Special rule — $200 GST number exemption:
**Section 75(3A):** A registered person is not required to keep a record of the supplier's GST registration number if the consideration for the supply is **$200 or less**.

---

## 4. Input Tax Deduction

**Section 20(3) — Calculation of tax payable:**
> In calculating the amount of tax payable, a registered person may deduct input tax in relation to the supply of goods and services acquired for the principal purpose of making taxable supplies.

**Requirements to claim input tax:**
1. The claimant must be a **registered person**
2. The goods/services must be acquired for use in a **taxable activity**
3. The claimant must hold valid **taxable supply information** (Section 19F) for the supply
4. The supply must have been made by another **registered person** (with GST charged)

**Apportionment (Section 20(3C)):**
If goods/services are used for both taxable and non-taxable purposes, the registered person must estimate the percentage of taxable use and claim input tax proportionally.

**De minimis rule (Section 20(3D)):**
Apportionment is NOT required if the total value of exempt supplies is no more than the lesser of:
- $90,000 per year, or
- 5% of total supplies

---

## 5. IRD GST101A Return — Box-by-Box Reference

**Source:** Official IRD GST101A form (2023 revision), confirmed against [Deskera NZ GST Guide](https://www.deskera.com/blog/new-zealand-gst/) and [Oracle NetSuite NZ GST mapping](https://docs.oracle.com/en/cloud/saas/netsuite/ns-online-help/section_4114553962.html).

### Sales/Income Section (Boxes 5–10)

| Box | Official Description | Calculation |
|-----|---------------------|-------------|
| **5** | Total sales and income for the period (including GST and any zero-rated supplies) | Enter from accounting records |
| **6** | Zero-rated supplies included in Box 5 | Enter (usually $0 for domestic contractors) |
| **7** | Subtract Box 6 from Box 5 | Box 5 − Box 6 |
| **8** | Multiply Box 7 by three and divide by twenty-three | Box 7 × 3/23 |
| **9** | Adjustments from your calculation sheet | Enter (usually $0) |
| **10** | Total GST collected on sales and income | Box 8 + Box 9 |

### Purchases/Expenses Section (Boxes 11–14)

| Box | Official Description | Calculation |
|-----|---------------------|-------------|
| **11** | Total purchases and expenses (including GST), excluding imported goods | **Auto-filled from receipts** |
| **12** | Multiply Box 11 by three and divide by twenty-three | **Box 11 × 3/23** (auto-calculated) |
| **13** | Credit adjustments from your calculation sheet | Enter (usually $0) |
| **14** | Total GST credit for purchases and expenses | Box 12 + Box 13 |

### Result (Box 15)

| Box | Official Description | Calculation |
|-----|---------------------|-------------|
| **15** | Difference between Box 10 and Box 14 | Box 10 − Box 14 |

- **Positive result** = GST to pay to IRD
- **Negative result** = GST refund due from IRD

**This skill auto-fills:** Box 11 (total purchases incl GST) and Box 12 (GST credit = Box 11 × 3/23). The user must enter Box 5 (sales/income) from their accounting/invoicing system.

---

## 6. Filing Periods and Due Dates

**Section 15 — Taxable periods:**

### Two-monthly (default, most common for small business)

There are two alignment options:

**Even-month alignment (e.g., balance date 31 March):**

| Period | Months | Filing Due |
|--------|--------|-----------|
| 1 | 1 March – 30 April | 28 May |
| 2 | 1 May – 30 June | 28 July |
| 3 | 1 July – 31 August | 28 September |
| 4 | 1 September – 31 October | 28 November |
| 5 | 1 November – 31 December | 15 January* |
| 6 | 1 January – 28/29 February | 28 March |

**Odd-month alignment:**

| Period | Months | Filing Due |
|--------|--------|-----------|
| 1 | 1 February – 31 March | **7 May*** |
| 2 | 1 April – 31 May | 28 June |
| 3 | 1 June – 31 July | 28 August |
| 4 | 1 August – 30 September | 28 October |
| 5 | 1 October – 30 November | **15 January*** |
| 6 | 1 December – 31 January | 28 February |

*Special dates: March-ending period due **7 May** (not 28 April). November-ending period due **15 January** (not 28 December).*

### Six-monthly
Available if taxable supplies ≤ $500,000 in preceding 12 months.

### Monthly
Required if taxable supplies exceed $24 million, or optional by request.

**Section 16 — Due dates:**
> A GST return and any tax payable is due by the **28th of the month** following the end of the taxable period, except for periods ending 31 March (due **7 May**) and 30 November (due **15 January**).

If a due date falls on a weekend or public holiday, the deadline moves to the next business day.

**All GST returns must be filed electronically via myIR** (ird.govt.nz).

---

## 7. Record Keeping

**Section 75 — Keeping of records:**

> (1) Every registered person must keep sufficient records to enable the Commissioner to ascertain the person's liability for tax.

Requirements:
- Records include books of account, vouchers, bank statements, invoices, taxable supply information, receipts, and any documents necessary to verify entries
- **Minimum retention: 7 years** after the end of the taxable period to which they relate
- The Commissioner may require an additional 3 years (total 10 years)
- Records must be kept **in New Zealand** (offshore storage requires Commissioner approval)
- Records must be kept in **English** (Māori language records require Commissioner approval)
- Records may be in manual, mechanical, or electronic format

---

## 8. Penalties

### Late filing
- **$50 – $250** per late return (depending on return type)

### Late payment
- **1% initial penalty** on the day after due date
- **Additional 4%** if still unpaid after 7 days (total 5%)
- **Use-of-money interest**: currently **10.91% per annum** (2025 rate) on unpaid tax

### Shortfall penalties
- Lack of reasonable care: **20%** of the tax shortfall
- Unacceptable tax position: **20%**
- Gross carelessness: **40%**
- Abusive tax position: **100%**
- Tax evasion: **150%**

---

## 9. Construction Contractor Specific

### Common Expense Categories

| Category | Examples | Typical GST status |
|----------|----------|-------------------|
| materials | Timber, concrete, nails, screws, plasterboard, paint | GST claimable |
| tools | Power tools, hand tools, drill bits, saw blades | GST claimable |
| fuel | Petrol, diesel for work vehicles | GST claimable (business use only) |
| vehicle | WOF, tyres, repairs, registration | GST claimable (business %, FBT may apply) |
| safety | PPE, hi-vis, hard hats, first aid, safety boots | GST claimable |
| subcontractor | Payments to other tradies | GST claimable (if sub is registered) |
| office | Stationery, phone, internet | GST claimable (business %) |
| other | Anything else | Check on case-by-case basis |

### Common NZ Construction Merchants
- Bunnings Warehouse
- Mitre 10 / Mitre 10 MEGA
- PlaceMakers
- ITM Building Supplies
- Carters Building Supplies
- Z Energy / BP / Mobil (fuel)
- Repco / Supercheap Auto (vehicle)
- NZ Safety Blackwoods (safety gear)

### NZ GST Number Format
- 8 or 9 digit IRD number, sometimes displayed as XXX-XXX-XXX
- On receipts appears as: "GST No:", "GST #", "IRD No:", "GST Reg No:", or "Tax No:"

---

## 10. Important Compliance Warnings

1. **Only claim GST on business expenses.** Mixed-use items must be apportioned.
2. **Do not claim GST on exempt supplies** (financial services, residential rent, donations).
3. **Do not claim GST on supplies from unregistered persons.** Check for a valid GST number.
4. **Keep all receipts for 7 years minimum.** Digital copies are acceptable if they are complete and legible.
5. **Foreign currency receipts** are not directly claimable — the NZD equivalent at the time of supply must be used.
6. **Fuel receipts** for vehicles with mixed personal/business use must be apportioned.
7. **Second-hand goods** purchased from unregistered persons: input tax can still be claimed under Section 3A(1)(c), calculated as the lesser of the purchase price × 3/23 or the open market value × 3/23.

---

*Last updated: March 2026. Based on GST Act 1985 as at 13 November 2025. Always verify current rates and thresholds at [ird.govt.nz](https://www.ird.govt.nz/gst).*

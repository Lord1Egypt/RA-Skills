# NZ Income Tax Reference -- Sole Traders (Builders / Construction Contractors)

## Authoritative Sources

- [Income Tax Act 2007](https://www.legislation.govt.nz/act/public/2007/0097/latest/DLM1512301.html)
- [IRD -- Tax rates for individuals](https://www.ird.govt.nz/income-tax/income-tax-for-individuals/tax-codes-and-tax-rates-for-individuals/tax-rates-for-individuals)
- [IRD -- IR3 Individual income tax return](https://www.ird.govt.nz/income-tax/income-tax-for-individuals/what-happens-at-the-end-of-the-tax-year/individual-income-tax-return-ir3)
- [IRD -- Provisional tax standard option](https://www.ird.govt.nz/income-tax/provisional-tax/provisional-tax-options/standard-option)

---

## 1. Income Tax Rates (from 1 April 2025)

New Zealand uses a progressive (marginal) tax system. Each dollar is taxed only
at the rate for the bracket it falls in.

| Taxable income bracket     | Marginal rate |
|----------------------------|---------------|
| $0 -- $15,600              | 10.5%         |
| $15,601 -- $53,500         | 17.5%         |
| $53,501 -- $78,100         | 30%           |
| $78,101 -- $180,000        | 33%           |
| $180,001 and over          | 39%           |

### 1.1 Worked Example -- $90,000 Taxable Income

```
Bracket 1:  $15,600  x 10.5%  =  $1,638.00
Bracket 2:  $37,900  x 17.5%  =  $6,632.50   ($53,500 - $15,600)
Bracket 3:  $24,600  x 30.0%  =  $7,380.00   ($78,100 - $53,500)
Bracket 4:  $11,900  x 33.0%  =  $3,927.00   ($90,000 - $78,100)
                                  ----------
Total tax on $90,000           = $19,577.50
Effective rate                 =     21.75%
```

### 1.2 ACC Earner's Levy

- Rate: **1.67%** of liable earnings
- Maximum liable earnings cap: **$152,790**
- Maximum levy: $152,790 x 1.67% = **$2,551.59**

The ACC earner's levy is deducted by payers of salary/wages. Self-employed
individuals pay their ACC levies separately (working safer levy + earner's
levy) as invoiced by ACC.

---

## 2. IR3 Return Structure

Sole trader builders file an **IR3 -- Individual Income Tax Return**. The key
sections relevant to a builder/construction contractor are set out below.

### 2.1 Income Section

| Line item               | Description                                      |
|--------------------------|--------------------------------------------------|
| Gross business income    | Total invoiced/received from building work        |
| Schedular payments       | Income where tax was deducted at source (WT)      |
| Interest income          | Bank interest, term deposits                      |
| Other income             | Rental, dividends, or any other taxable income    |

### 2.2 IR3B -- Schedule of Business Income

The IR3B is attached to the IR3 and breaks down the business result.

```
Gross income from business
  Less: Purchases / cost of materials
  Less: Opening stock
  Plus: Closing stock
= Gross Profit

Less expenses by category:
  - Accident compensation (ACC levies)
  - Accounting fees
  - Advertising and promotion
  - Bad debts
  - Communication (phone, internet)
  - Depreciation
  - Fuel and vehicle running costs
  - Insurance
  - Interest on business borrowings
  - Legal fees
  - Rates (if applicable)
  - Rent on business premises
  - Repairs and maintenance (business assets)
  - Salaries and wages paid
  - Subcontractor payments
  - Travel and accommodation
  - Other deductible expenses

= Net Profit (or Loss) -- transferred to IR3
```

### 2.3 Tax Calculation (IR3 summary)

```
Taxable income (all sources combined)
  Tax on taxable income (per progressive table)
  Less: tax credits (PAYE, RWT, WT, IETC, donations)
  Less: provisional tax already paid
= Tax to pay (or refund due)
```

### 2.4 Filing Deadlines

| Scenario                                | Deadline                        |
|------------------------------------------|---------------------------------|
| Self-filed (no tax agent)               | **7 July** following tax year    |
| Filed through a tax agent (extension)   | **31 March** of the following year (i.e., ~21 months after year-end) |

Tax year runs 1 April to 31 March.

---

## 3. Provisional Tax -- Standard Method

### 3.1 Who Must Pay

You must pay provisional tax if your **residual income tax (RIT)** in the
previous year exceeds **$5,000**.

RIT = total tax liability minus tax credits (PAYE, RWT, WT, etc.).

### 3.2 Calculation Formula

**If last year's return has been filed:**

```
Provisional tax = Previous year RIT x 105%
Each instalment = (Previous year RIT x 105%) / 3
```

**If last year's return has NOT been filed:**

```
Provisional tax = RIT from 2 years ago x 110%
Each instalment = (RIT from 2 years ago x 110%) / 3
```

### 3.3 Payment Dates (March Balance Date)

| Instalment | Due date       |
|------------|----------------|
| 1st        | **28 August**  |
| 2nd        | **15 January** |
| 3rd        | **7 May**      |

Late payment attracts use-of-money interest (currently ~10.91% debit / 0%
credit as of 2025) and potentially late payment penalties.

---

## 4. Deductible Business Expenses for Builders

### 4.1 Deductible Expenses

| Category                | Examples / Notes                                                  |
|-------------------------|-------------------------------------------------------------------|
| Materials and supplies  | Timber, concrete, fixings, plasterboard, paint, adhesives         |
| Tools and equipment     | Hand tools, power tools (items under $1,000 can be expensed immediately; over $1,000 depreciate) |
| Fuel                    | Fuel for vehicles and machinery used in the business              |
| Vehicle expenses        | Mileage (IRD rate), or actual costs (fuel, registration, insurance, repairs) apportioned for business use |
| Safety gear and PPE     | Hard hats, hi-vis, steel-cap boots, safety glasses, harnesses    |
| Subcontractor payments  | Payments to subbies (must hold valid invoices; withholding tax may apply) |
| Insurance               | Public liability, contract works, tools insurance, professional indemnity |
| Phone and internet      | Business-use portion of mobile phone, landline, broadband         |
| Depreciation            | Vehicles, plant, machinery, computers, software (per IRD rates)   |
| Home office             | Proportion of rent/mortgage interest, power, insurance, rates for dedicated office space |
| ACC levies              | Working safer levy and earner's levy (business portion)           |
| Accounting and tax fees | Tax agent fees, bookkeeping software subscriptions                |
| Interest                | Interest on loans used for business purposes                      |
| Training and licenses   | Site-safe, trade qualifications, LBP renewal                     |
| Travel and accommodation| Travel to remote job sites, overnight stays for distant projects  |

### 4.2 Non-Deductible or Limited Expenses

| Category                     | Rule                                                        |
|------------------------------|-------------------------------------------------------------|
| Personal expenses            | Not deductible -- must be separated from business costs     |
| Entertainment and meals      | **50% deductible** only (e.g., client meals, staff shouts)  |
| Fines and penalties          | Not deductible (traffic fines, building consent penalties)   |
| Capital expenditure          | Not deductible as an expense; must be capitalised and depreciated (e.g., a new ute, major plant) |
| Drawings / personal wages    | Sole trader cannot deduct their own salary/drawings          |
| Income tax payments          | Not deductible                                               |

---

## 5. Important Dates -- Annual Calendar

The following calendar assumes a standard **31 March balance date**.

| Date              | Event                                                         |
|-------------------|---------------------------------------------------------------|
| **1 April**       | New tax year begins                                           |
| **7 May**         | 3rd provisional tax instalment due (for year just ended)      |
| **28 May**        | GST return due (2-monthly filer: Mar-Apr period)              |
| **7 June**        | Terminal tax due for prior year (if no tax agent extension)    |
| **7 July**        | IR3 filing deadline (self-filed, no tax agent)                |
| **28 August**     | 1st provisional tax instalment due (current year)             |
| **28 August**     | GST return due (2-monthly filer: May-Jun period)              |
| **28 October**    | GST return due (2-monthly filer: Jul-Aug period)              |
| **15 January**    | 2nd provisional tax instalment due (current year)             |
| **15 January**    | GST return due (6-monthly filer: Jul-Dec period)              |
| **28 January**    | GST return due (2-monthly filer: Nov-Dec period)              |
| **31 March**      | Tax year ends                                                 |
| **31 March**      | IR3 filing deadline (via tax agent, with extension)           |
| **28 March**      | GST return due (2-monthly filer: Jan-Feb period)              |
| **7 May (next)**  | 3rd provisional tax instalment due                            |
| **28 May (next)** | GST return due (6-monthly filer: Jan-Jun period)              |

**Note:** When a due date falls on a weekend or public holiday, the deadline
moves to the next working day.

---

*This document is a reference summary for the kiwi-receipts OpenClaw skill. It
is not tax advice. Always refer to the authoritative IRD sources linked above
or consult a registered tax agent for specific situations.*

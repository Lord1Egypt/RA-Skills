# Real estate calculations and disclosure fields

Author: Daniel Hallman

Use these formulas to check the supplied amounts. Check legal wording against the applicable jurisdiction and source; a template does not establish that every required disclosure is present.

## Commercial lease calculations

- **Monthly base rent:** `(Square Footage * Annual Base Rate per Sq Ft) / 12`
- **Estimated monthly common area maintenance (CAM):** `(Square Footage * Annual CAM Rate per Sq Ft) / 12`
- **Initial monthly payment:** `Monthly Base Rent + Monthly CAM`
- **Security deposit:** Use the agreed amount, subject to the applicable requirements. Do not infer it from rent.

## Lease fields to review

- **Lead-based paint:** Check the building date and whether the disclosure under 42 U.S.C. 4852d applies.
- **Security deposit:** Check the amount, where it is held, interest requirements, and return deadline.
- **Landlord entry:** Check the notice period and any exceptions for the jurisdiction and purpose of entry.
- **Default notices:** Check the type of breach, required notice, and time allowed to respond.

Read the supported state profiles at `GET https://pressmark.dev/api/v1/states`. Preserve any missing or uncertain jurisdiction details.

## Property management statements

1. Add collected rent, late fees, parking charges, and pet rent to calculate gross collected revenue.
2. List the agreed management fee, repairs, utilities, and vendor charges separately.
3. Calculate the amount due to the owner as `Gross Revenue - Operating Deductions - Reserve Escrow Replenishment`.
4. Compare the statement with the supplied payment records before returning it.

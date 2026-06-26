# RCM Case Study Engine
**10 Real-World Hospital Revenue Cycle Scenarios for JB Burkett**
*SparkChange RCM Pulse Curriculum — Advanced Drill Series*

---

## How to Use These Case Studies

This engine is built for JB to drill through real RCM failure modes that hit SparkChange-style RCM operations every day. Each case follows a consistent structure:

- **Scenario** → real-world setup
- **Patient/Account** → anonymized but realistic
- **The Problem** → what went wrong
- **Financial Impact** → actual dollar exposure
- **Root Cause** → why it happened (the human/system/process failure)
- **What the RCM Team Did** → resolution steps
- **Outcome** → result
- **Lesson Learned** → 1-2 sentence takeaway
- **SparkChange Angle** → how this applies directly to JB's RCM automation/ops work at SparkChange

**Use cases:**
- Daily RCM pulse drills — absorb one case per day
- Team training — walk a rep through a case, ask them to call the failure point before revealing it
- Automation opportunity mapping — every case is a workflow that can be systematized
- Interview/test prep for hiring RCM staff

---

## Case 1: Timely Filing Denial

**Scenario:** A 68-year-old Medicare/Medicaid dual-eligible patient received outpatient infusion services in November 2024. The billing team was short-staffed due to Q4 turnover. The claim for Medicaid was submitted in January 2026 — 47 days past the timely filing deadline. Medicaid denied the $34,200 claim. The hospital filed a timely filing appeal with the original date-of-service records and a memo from the billing supervisor explaining the staffing gap. The appeal was denied on grounds that internal staffing issues do not constitute an exception to the timely filing rule. The balance was written off.

**Patient/Account:**
- Patient: M.B., age 68, dual Medicare/Medicaid
- Account #: 4471-8830-D
- Service: Outpatient IV infusion, 6 sessions, November 12–December 3, 2024
- Billed amount: $34,200
- Balance after Medicare: $8,640 (Medicaid responsibility)

**The Problem:**
The claim was filed 47 days after the payer timely filing deadline expired. Medicaid's timely filing limit is the last day of the calendar year following the year of service (December 31, 2025 for a 2024 date of service). The claim was not submitted until January 2026.

**Financial Impact:** $34,200 write-off (full billed amount, Medicaid denied in full)

**Root Cause:**
Q4 2024 staffing vacancy in the billing department — the claim was documented in the system but never submitted. No claim aging report was running to catch claims approaching timely filing deadlines. The billing supervisor assumed the claim had been submitted when it had not. No automated deadline alerts existed.

**What the RCM Team Did:**
1. Attempted claim submission — rejected as past timely filing
2. Filed formal appeal citing administrative error and providing original service documentation
3. Appeal denied — no exception granted
4. Escalated to revenue integrity committee for write-off approval
5. Conducted internal root cause analysis
6. Implemented weekly claim aging audit across all payers

**Outcome:** Full write-off. Staffing gap was later cited in a budget request for an additional billing FTE. The claim aging report was added to the weekly revenue cycle dashboard.

**Lesson Learned:** Timely filing is an absolute deadline — no exceptions for internal process failures. Automated aging reports with deadline alerts are not optional; they are the difference between collected revenue and write-offs.

**SparkChange Angle:** At SparkChange, JB's team likely manages similar claim submission workflows for client hospitals. Building automated timely filing deadline tracking into any RCM dashboard or workflow engine — with escalation alerts at 30, 14, and 7 days before deadline — eliminates this failure mode entirely. If SparkChange is building automation layer on top of client billing systems, deadline tracking is a foundational control.

---

## Case 2: Modifier 25 Denial

**Scenario:** A 52-year-old patient presented to a general surgeon for evaluation of a painful sebaceous cyst on the upper back. During the same visit, the surgeon performed an excision of the cyst (CPT 11400). The E/M visit itself was medically necessary — the cyst required assessment and decision-making beyond the procedure. The biller submitted the claim with the procedure code 11400 and the E/M code 99213, but did not append modifier 25 to the E/M code. The commercial payer rejected the E/M code with Remark Code N130 — "Consultation/visit does not meet the published criteria for a separate reimbursement" and a CARC denial: "Procedure code is incompatible with E/M code on same date of service." The total claim was $18,500 ($2,100 for the E/M, $16,400 for the excision). The biller resubmitted with modifier 25 appended to 99213. The payer reprocessed and paid.

**Patient/Account:**
- Patient: D.R., age 52, commercial BCBS PPO
- Account #: 5512-0047-C
- Service: Office visit (99213-25) + sebaceous cyst excision (11400), same date
- Billed amount: $18,500
- Patient responsibility: $1,850 (10% coinsurance)

**The Problem:**
The E/M visit was performed and was medically distinct from the procedure — the decision to excise required evaluation beyond what was included in the global surgical package. Without modifier 25 appended to the E/M code, the payer bundled the E/M into the procedure reimbursement, denying it as a separate billable service.

**Financial Impact:** Initial denial of $2,100 (E/M portion). After resubmission with modifier 25, full payment received. Total claim: $18,500.

**Root Cause:**
The biller was unaware that modifier 25 is required when a distinct, medically necessary E/M service is performed on the same day as a procedure, even if the procedure is performed at the same visit. Coders and billers had not been retrained after a payer policy update that tightened modifier 25 documentation requirements.

**What the RCM Team Did:**
1. Claim initially denied — researched denial reason (N130/CARC 97)
2. Pulled clinical notes documenting the medical necessity of a separate E/M
3. Appended modifier 25 to 99213, attached office note documentation
4. Resubmitted as appeal/resubmission
5. Payer reprocessed and paid full allowed amount
6. Scheduled modifier 25 retraining for billing staff
7. Added modifier 25 logic to charge entry edits (system now flags E/M + procedure same day)

**Outcome:** Full payment received. Mod 25 education was added to the new biller onboarding curriculum. Charge entry system now auto-flags same-day E/M + procedure combinations for modifier review.

**Lesson Learned:** Modifier 25 is a critical distinction between a bundled E/M and a separately reimbursable evaluation. The global surgical package absorbs routine E/M care, but medically necessary decision-making beyond the procedure is billable — with the right modifier and documentation.

**SparkChange Angle:** This is a pure automation opportunity. JB should flag for SparkChange clients: if the EHR/billing system has any customization capacity, a same-day E/M + procedure charge entry rule that auto-prompts for modifier 25 documentation review would prevent this denial class entirely. This is also a coder/biller competency baseline — modifier 25 errors are among the top reasons for E/M denials industry-wide.

---

## Case 3: CO-16 Denial — Missing Rendering Provider NPI

**Scenario:** A 340-bed regional medical center submitted a UB-04 claim for a three-day inpatient admission. The claim had 12 service lines spanning emergency, surgical, and recovery charges totaling $67,000. One service line — a respiratory therapy charge on day 2 — had been entered manually during a busy weekend shift and omitted the rendering provider NPI. The payer returned the entire claim with CARC 16 — "Claim missing information" / CO-16 — and held the full $67,000. The billing team spent three weeks identifying the error, obtaining the NPI, correcting the claim, and resubmitting. Interest or late payment penalties did not apply, but the three-week delay created a 21-day AR hit and shifted $67,000 from current AR to pend AR.

**Patient/Account:**
- Patient: L.F., age 71, Medicare Part A
- Account #: 8830-2214-M
- Service: Inpatient admission, DRG 470 (major joint replacement), November 8–11, 2024
- Billed amount: $67,000
- Expected Medicare payment: ~$16,200 (DRG rate)

**The Problem:**
A single missing NPI on one of 12 service lines held the entire claim. CO-16 denials are reject-to-resubmit errors — the payer will not process the claim until the missing information is provided. The entire $67,000 balance sat in pending AR for three weeks.

**Financial Impact:** $67,000 in delayed AR for 21 days. Estimated interest/late payment impact: $0 (Medicare), but revenue cycle KPI impact: AR days crept up by 0.8 days for that billing period. If this is happening on multiple claims, the aggregate AR hit is significant.

**Root Cause:**
Manual charge entry during weekend shifts — no required-field validation on the UB-04 form. The rendering NPI field on the UB-04 is not flagged as mandatory at point of entry. The charge description master (CDM) had a default NPI slot but it was blank for that particular respiratory therapy line item.

**What the RCM Team Did:**
1. Payer returned claim with CO-16 — identified missing NPI on line 7 (respiratory therapy, day 2)
2. Obtained rendering provider NPI from HR/credentialing records
3. Corrected claim and resubmitted with cover letter noting prior submission reference
4. Tracked resubmission in claim workqueue with 14-day follow-up
5. Payer processed and paid
6. Conducted CDM audit for all line items with blank rendering NPI fields
7. Implemented mandatory NPI field validation at charge entry — no blank NPI allowed

**Outcome:** Claim paid after 21-day delay. CDM audit found 14 other line items with missing or default NPIs — corrected proactively.

**Lesson Learned:** CO-16 denials are almost entirely preventable with front-end charge entry validation. One missing field on one line can hold an entire claim. System controls at point of entry are far more effective than post-submission review.

**SparkChange Angle:** JB's SparkChange team should be evangelizing front-end validation to every client. This is exactly the kind of small-data automation — a required-field lock on NPI at charge entry — that separates high-performing RCM operations from reactive ones. SparkChange's automation layer should include claim scrubber logic that runs before submission and catches CO-16 class errors proactively.

---

## Case 4: Bad Debt Write-Off — Missing Financial Responsibility Agreement

**Scenario:** A 45-year-old patient with a $4,100 patient responsibility balance (after insurance) was sent to collections after 90 days of no payment. The patient disputed the balance, asserting they never signed a financial responsibility agreement and were unaware of their financial obligation. The collections agency, as part of its standard process, reported the account to a credit bureau. The hospital's compliance team flagged the credit report entry during a routine audit. When the hospital attempted to reverse the write-off and rebill, they discovered there was no signed financial responsibility agreement in the patient's account. The write-off was reversed; the balance was reclassified as self-pay and the collections agency was notified to remove the credit bureau entry. The hospital's legal counsel became involved due to the potential FDCPA and FCRA implications.

**Patient/Account:**
- Patient: T.K., age 45, commercial Aetna (coverage terminated 6 months prior to service)
- Account #: 6602-3391-S
- Service: Elective outpatient colonoscopy, January 2024
- Billed amount: $8,200 | Insurance paid: $2,100 | Patient owed: $4,100
- Collection agency: ABC Collections

**The Problem:**
No signed financial responsibility agreement on file. The patient had provided insurance information but the front desk had not obtained a signature on the practice's financial policy form. When the account went to collections and the patient disputed, the hospital had no documentation to support that the patient had agreed to be financially responsible for the balance.

**Financial Impact:** $4,100 balance at risk of non-collection. Potential FDCPA/FCRA liability for the collections agency reporting. Legal review hours. Reputational risk if the patient left a review.

**Root Cause:**
Front desk staff skipped the financial responsibility signature during patient intake because the patient was checkout-out quickly and the receptionist "knew them from previous visits." No system-level requirement enforced the financial agreement signature before scheduling or check-in. The collections agency was given the account without a documented chain of financial responsibility.

**What the RCM Team Did:**
1. Collections agency notified to retract credit bureau entry (patient disputed in writing)
2. Reversed bad debt write-off — reclassified account as self-pay
3. Attempted to rebill patient directly with a payment plan offer
4. Compliance team conducted internal audit of all accounts sent to collections in the prior 6 months — identified 23 additional accounts without signed financial responsibility agreements
5. Halted further collections referrals on those accounts pending review
6. Implemented electronic financial responsibility agreement in the EHR — cannot proceed to check-out without signature capture
7. Staff retraining on financial policy requirements

**Outcome:** Credit bureau entry retracted. $4,100 re-billed with payment plan. 23 additional accounts flagged for review — estimated $60,000+ in balances at risk if financial agreements were missing. Process corrected before further liability.

**Lesson Learned:** A missing financial responsibility agreement is a single point of failure that exposes the organization to significant legal, financial, and reputational risk. System-enforced signature capture at registration is the only reliable control — relying on front desk staff discipline to remember a step is not a control.

**SparkChange Angle:** For SparkChange clients running RCM operations, intake workflow automation — especially electronic financial responsibility capture at registration — is a high-value, low-cost automation win. JB should look for this gap in any SparkChange client onboarding assessment. It's a compliance risk, an AR risk, and a legal risk that a simple e-signature workflow at intake eliminates.

---

## Case 5: Prior Authorization Failure — Intraoperative Procedure Change

**Scenario:** A 58-year-old patient was scheduled for an elective diagnostic laparoscopy on March 15 for evaluation of chronic pelvic pain. The surgeon's office obtained prior authorization from the payer for "diagnostic laparoscopy." During surgery, the surgeon found extensive intra-abdominal adhesions requiring therapeutic adhesiolysis — a more complex, therapeutic procedure. The authorization did not cover the therapeutic procedure, only the diagnostic. The claim was submitted for $22,000. The payer denied $18,600 of the $22,000 as prior authorization not obtained for the performed procedure. The hospital and surgeon disputed — arguing the adhesiolysis was medically necessary and discovered intraoperatively. The payer denied the appeal.

**Patient/Account:**
- Patient: C.W., age 58, commercial UHC Choice Plus
- Account #: 7721-0062-S
- Service: Therapeutic laparoscopy with adhesiolysis (converted from diagnostic), March 15, 2025
- Billed amount: $22,000
- Patient responsibility per authorization: $3,400
- Denied amount: $18,600

**The Problem:**
The prior authorization was for a diagnostic procedure. The surgeon performed a therapeutic procedure. The payer's prior auth specified a specific CPT code range — diagnostic laparoscopy only. When the therapeutic procedure was performed, the authorization was no longer valid for the work actually done.

**Financial Impact:** $18,600 denied. Appeal denied. Hospital absorbed $14,600 after contractual adjustment; surgeon absorbed $4,000 professional fee. Total write-off: $18,600.

**Root Cause:**
No intraoperative authorization escalation protocol existed. The surgeon's office obtained authorization for the planned procedure, not for the likely intraoperative scenarios. Pre-op documentation did not include a therapeutic contingency authorization. The OR team had no process to call the payer for a retroactive or emergency authorization while the patient was still open.

**What the RCM Team Did:**
1. Claim submitted, $18,600 denied
2. Filed appeal citing medical necessity of adhesiolysis discovered intraoperatively
3. Surgeon provided operative report documenting adhesion severity requiring therapeutic intervention
4. Payer denied appeal — authorization was for diagnostic only, and the therapeutic procedure requires a separate authorization
5. Absorbed the write-off; surgeon billing team absorbed professional fee portion
6. Implemented pre-op authorization checklist requiring authorization for all probable intraoperative scenarios
7. Established OR-to-payer hotlines for emergency intraop authorization requests
8. Added "authorization contingency" field to surgical scheduling system

**Outcome:** Write-off absorbed. Process changed organization-wide. Pre-op authorization checklists now include likely therapeutic alternatives. OR authorization escalation protocol established.

**Lesson Learned:** Prior authorization for surgical cases must account for probable intraoperative findings. Authorization for a diagnostic-only procedure is insufficient when therapeutic intervention is reasonably anticipated or commonly required. OR authorization escalation protocols are essential for catching these cases before or during surgery.

**SparkChange Angle:** JB should flag this case for SparkChange clients with surgical RCM operations. Pre-operative authorization workflows that capture likely procedure alternatives — not just the primary planned procedure — are a key automation/design opportunity. If SparkChange is building surgical scheduling or authorization workflow tools, a "contingency CPT" authorization field prevents this failure mode at the front end.

---

## Case 6: Medical Necessity Denial — MRI Lumbar Spine

**Scenario:** A 61-year-old patient presented to an orthopedic spine specialist with six weeks of refractory lower back pain radiating down the left leg. The physician ordered an MRI of the lumbar spine. The payer denied the MRI as "not medically necessary" based on their clinical guidelines — the payer's criteria required 12 weeks of conservative care before imaging, and the patient had only 6 weeks. The ordering physician's documentation did not reference the payer's specific criteria checklist. The denied amount was $8,900. The physician requested a peer-to-peer review with the payer's medical director. During the review, the physician demonstrated that the patient's pain was progressing neurologically and that conservative care had been appropriately trialed given the clinical urgency. The denial was overturned. The claim was paid.

**Patient/Account:**
- Patient: J.M., age 61, commercial Cigna Open Access
- Account #: 9914-5520-O
- Service: MRI lumbar spine without contrast, ordered February 10, 2025
- Billed amount: $8,900
- Patient responsibility: $890

**The Problem:**
The payer's LCD (Local Coverage Determination) for lumbar spine MRI required 12 weeks of conservative care OR progressive neurological symptoms. The physician's documentation noted "6 weeks of back pain" but did not document the neurological progression that would meet the payer's exception criteria. The initial denial was based on the documentation gap, not the clinical facts.

**Financial Impact:** $8,900 initial denial. Overturned on peer-to-peer. Full payment received after 6-week appeal cycle.

**Root Cause:**
The physician's documentation did not map to the payer's specific LCD criteria checklist. The biller submitted the claim without a documentation review against the payer's published criteria. The payer applied their checklist strictly — the documentation didn't match, so it was denied. No pre-claim clinical documentation review process existed.

**What the RCM Team Did:**
1. MRI performed; claim submitted
2. Denied as not medically necessary — CARC 50
3. Billers pulled payer's LCD criteria and matched to clinical notes
4. Identified documentation gap: neurological signs (positive straight leg raise, reflex asymmetry) were documented in the chart but not highlighted in the peer-to-peer narrative
5. Requested peer-to-peer review with medical director
6. Physician presented clinical case — emphasized progressive neurological deficit as exception criterion
7. Denial overturned; claim paid in full
8. Implemented payer's LCD criteria checklist into ordering workflow — physicians must attest to applicable criteria before order is placed
9. Added documentation checklist to MRI order workqueue

**Outcome:** Denial overturned. Full payment received. Clinical documentation workflow changed — physicians now attest to applicable LCD criteria at order entry, eliminating documentation gaps that cause denials.

**Lesson Learned:** Medical necessity denials are documentation denials in disguise. Payers apply specific published criteria to every claim. If the clinical documentation doesn't map explicitly to those criteria, the claim gets denied — regardless of actual clinical merit. Peer-to-peer review works, but it's better to prevent the denial by ensuring documentation matches criteria at order entry.

**SparkChange Angle:** At SparkChange, JB's RCM automation focus should include order-to-payment clinical documentation mapping. A workflow that flags an order against the relevant payer's LCD criteria before submission — and prompts the physician to attest — would prevent this class of denial. This is a high-value intersection of clinical documentation and revenue cycle. If SparkChange is building or integrating with order authorization workflows, medical necessity documentation alignment is a core automation target.

---

## Case 7: Credit Balance / Duplicate Payment — Escheatment to State

**Scenario:** A 39-year-old patient overpaid $3,400 across three visits to the same hospital system — $1,200 at visit 1, $1,400 at visit 2, and $800 at visit 3 — due to a misconfigured patient payment portal that was double-charging credit cards during online payments. The hospital's AR team identified the overpayment in month 4 and issued a refund check for $3,400 to the patient's address on file. The check was sent to an old address — the patient had moved 8 months prior and the address was never updated in the system. The check was not cashed. 18 months passed. The hospital's finance team, during a routine unclaimed property audit, found the uncashed check. The state unclaimed property law required the $3,400 to be escheated to the state treasury. The hospital could not reclaim the funds.

**Patient/Account:**
- Patient: S.P., age 39, self-pay + commercial Humana
- Account #: 2240-7715 (three accounts consolidated)
- Overpayment: $3,400 ($1,200 + $1,400 + $800)
- Original check address: 4821 Old Mill Road, Apt 7 (patient moved; address not updated)
- Escheated amount: $3,400

**The Problem:**
The refund check was sent to an outdated address and was never cashed. The 18-month dormancy period expired, triggering state unclaimed property laws. The hospital was required to remit the funds to the state — $3,400 was no longer available to the hospital or the patient.

**Financial Impact:** $3,400 in lost revenue. Patient was not made whole — they overpaid and received nothing back. Administrative time spent on audit, refund processing, and state escheatment filing.

**Root Cause:**
No address verification step before issuing refund checks. The patient had moved but the hospital's system had no address update trigger or patient communication asking them to verify their address. The refund check was generated and mailed without any delivery confirmation process. No one followed up on the uncashed check within the 18-month window.

**What the RCM Team Did:**
1. AR audit identified duplicate payments and overpayment in month 4
2. Refund check issued — sent to address on file
3. Check not cashed — no follow-up process existed
4. 18 months pass; unclaimed property audit flags uncashed check
5. Funds escheated to state treasury per statute
6. Finance team filed escheatment report
7. Patient notified — no recourse; funds were with the state
8. Implemented address verification workflow before refund issuance
9. Added refund check tracking to AR workqueue with 30/60/90-day follow-up flags
10. Configured patient payment portal to require address confirmation on all accounts

**Outcome:** $3,400 escheated. Process fixed going forward. Patient communication and address verification requirements added to refund workflow.

**Lesson Learned:** Uncashed refund checks are a time bomb. State unclaimed property laws have strict dormancy periods (typically 1–3 years depending on state). Hospitals must actively track and follow up on uncashed checks — or lose the funds to the state.

**SparkChange Angle:** For SparkChange RCM ops, this is a process control case — not just about the refund, but about the entire payment reconciliation workflow. JB should consider whether SparkChange automation tools include refund tracking and follow-up escalation. A simple process rule — refund checks must have delivery confirmation or electronic payment as the default — would have prevented this. ACH refunds or patient portal credit refunds are faster, cheaper, and more trackable than paper checks.

---

## Case 8: 501(r) Compliance Failure

**Scenario:** A nonprofit hospital system with 12 facilities mailed billing statements to patients that did not include the required plain language notice about financial assistance, the amount owed vs. the amount Medicare allows (amount generally billed), or a phone number for financial counseling — all required elements under IRC Section 501(r)(4) and (5) for nonprofit hospital organizations. A patient filed a complaint with the IRS. An IRS audit of the billing process found the noncompliant statements. The hospital system faced IRS scrutiny of its tax-exempt status and was required to undertake a corrective action plan including retroactive patient outreach, reprinting and resending compliant statements, and attestation to future compliance. The legal and consulting costs of remediation exceeded $180,000.

**Patient/Account:**
- System: Regional nonprofit hospital system, 12 facilities, $380M annual revenue
- Compliance violation: 6,400 billing statements mailed without required 501(r) notices over a 14-month period
- Affected patients: ~6,400
- Cost of remediation: ~$180,000 (legal, consulting, reprinting, outreach)
- Tax-exempt status: Under IRS review for 8 months

**The Problem:**
The billing statement template used by the hospital system was updated during an EHR migration. The 501(r) required notices — plain language description of financial assistance, AGB (amount generally billed) amount, and financial counseling contact information — were accidentally omitted from the new statement template. The billing team approved the template without a 501(r) compliance review. The statements were mailed for 14 months before the error was caught.

**Financial Impact:**
- Direct remediation cost: ~$180,000
- IRS tax-exempt status risk: 8-month review period, significant leadership distraction
- Reputational: Patient complaints to state attorney general and IRS
- Ongoing: Mandatory 3-year monitoring by IRS post-remediation

**Root Cause:**
The EHR/billing statement template migration was reviewed by IT and billing operations but was NOT reviewed by the compliance or tax-exempt legal team. There was no 501(r) compliance checkpoint in the billing template change management process. The old template had the notices; the new one did not. No one noticed.

**What the RCM Team Did:**
1. IRS audit notification — provided all billing templates and patient communications
2. Compliance counsel engaged immediately
3. Retroactive patient outreach — identified all 6,400 affected patients, sent compliant statements with apology and financial assistance re-offer
4. Corrective Action Plan (CAP) submitted to IRS
5. Template rebuilt with legal/compliance sign-off required before production use
6. 501(r) compliance added to annual audit checklist and billing template change management process
7. Staff education on 501(r) requirements

**Outcome:** Tax-exempt status preserved (under 3-year IRS monitoring). Compliant statements sent to all 6,400 patients. Template change management process now requires compliance sign-off. Total remediation cost: $180,000+.

**Lesson Learned:** IRC Section 501(r) compliance is not optional and not forgiving. Any change to billing statements, patient communications, or financial assistance policies requires compliance and tax-legal review. The cost of a compliance failure — remediation, legal fees, tax status risk — far exceeds the cost of preventive review.

**SparkChange Angle:** For SparkChange clients that are nonprofit hospital organizations, 501(r) compliance is a non-negotiable operational requirement. JB should ensure that any RCM workflow or statement template work done for nonprofit clients includes a mandatory 501(r) compliance checkpoint. This is a high-stakes area — tax-exempt status risk is existential for a nonprofit hospital.

---

## Case 9: HIPAA Breach / Improper Disclosure

**Scenario:** A hospital billing department staff member attempted to email a patient billing ledger to the patient's family member (authorized contact per the privacy form on file). The staff member typed the family member's email address — but one letter was off — and sent the billing ledger containing 312 patients' billing records (name, account number, service dates, diagnosis codes, and charges) to the wrong email address. The email was sent to an unverified external email domain. The error was discovered when the intended recipient called to ask why they received a billing statement for a different patient. The hospital's privacy officer was notified. A 60-day breach notification clock began. OCR opened an investigation. The hospital offered credit monitoring to all 312 affected patients and notified HHS. The breach was attributed to human error — no malicious intent — but the financial and reputational damage was severe.

**Patient/Account:**
- 312 patients' billing records exposed (PHI: name, DOB, account number, service dates, diagnosis codes, charges)
- Staff member: Billing representative, accessed PHI in normal course of job
- Unauthorized recipient: Wrong email — one letter off from authorized family member's address
- Time to discovery: ~3 hours after transmission
- Breach notification deadline: 60 days from discovery

**The Problem:**
An unauthorized disclosure of 312 patients' billing records via misdirected email. The email was sent to an unverified external email address. The staff member did not confirm the email address before sending. The email contained PHI (protected health information) without encryption.

**Financial Impact:**
- OCR investigation and potential fine: $100–$1.5M per violation category (max $1.5M per violation category per year)
- Credit monitoring for 312 patients: ~$31,200 (~$100 per patient)
- Legal/notification costs: ~$45,000
- State AG notification costs
- Reputational damage and patient trust impact
- Staff time for breach investigation and remediation: ~160 hours

**Root Cause:**
No email address verification step before sending PHI to external recipients. No encryption requirement on outbound emails containing PHI. The staff member typed the email address from memory rather than selecting from a pre-verified contact list. The EHR's privacy permission flags did not include a "verify before sending" control for external email transmissions.

**What the RCM Team Did:**
1. Breach discovered within 3 hours — privacy officer notified immediately
2. Unintended recipient contacted — confirmed email deletion (written confirmation obtained)
3. 60-day breach notification clock started
4. All 312 patients notified in writing within 55 days
5. Credit monitoring offered and arranged
6. OCR self-reported within 60 days
7. HHS and state AG notifications completed
8. Root cause analysis conducted
9. Implemented mandatory external email address verification workflow (pre-set contact list in EHR, no free-text email entry)
10. PHI email transmission now requires encryption + supervisor attestation before sending
11. Annual HIPAA refresher training updated to include email verification protocols

**Outcome:** OCR investigation ongoing. All notifications completed within deadline. No confirmed misuse of PHI. Process controls strengthened. Staff retrained.

**Lesson Learned:** Sending PHI to external email addresses is a high-risk activity that requires multiple verification controls. A single-letter typo in an email address is all it takes to expose 312 patients' records. No amount of staff good intentions prevents this — only system-level controls (verified contact lists, mandatory encryption, supervisor attestation) prevent misdirected PHI emails.

**SparkChange Angle:** For SparkChange, HIPAA compliance is a baseline requirement. JB should ensure that any RCM automation workflow involving patient communication — billing statements, EOBs, insurance correspondence — has verified recipient controls built in. This means: no free-text email entry, mandatory contact verification before any outbound patient communication, and encryption standards for all PHI transmissions. This is both a compliance and a reputational risk management issue. A breach of this magnitude would be catastrophic for a SparkChange client.

---

## Case 10: DRG Assignment Error — Undercoded

**Scenario:** A 64-year-old patient was admitted through the ED with acute chest pain. The provider's documentation in the admission note read: "Atypical chest pain, rule out myocardial infarction." The provider did not document cardiac enzymes, ECG findings, or a definitive MI diagnosis at the time of admission. The inpatient coder, reviewing the documentation, assigned DRG 311 (Angina pectoris) — a lower-weighted DRG. A concurrent audit by the hospital's coding quality team identified the discrepancy. The coder issued a physician query: "Please clarify whether this patient had a myocardial infarction." The physician reviewed the records, documented the final diagnosis as NSTEMI (non-ST elevation MI), and amended the record. The DRG was reclassified from 311 (weight 1.2134, ~$7,100 reimbursement) to DRG 280 (MI without CC/MCC, weight 1.9313, ~$18,800 reimbursement). The corrected reimbursement was $11,700 higher.

**Patient/Account:**
- Patient: R.H., age 64, Medicare Part A
- Account #: 3340-9901-M
- Service: Inpatient admission, chest pain rule out MI, 3-day stay, October 2024
- DRG 311 (Angina): ~$7,100 Medicare payment
- DRG 280 (MI without CC/MCC): ~$18,800 Medicare payment
- Reimbursement difference: $11,700

**The Problem:**
The provider's documentation at admission said "rule out MI" without specifying a final MI diagnosis. The coder assigned DRG 311 (Angina) because that was what the documentation supported at face value. However, the clinical record — when reviewed holistically — showed elevated troponins, ECG changes consistent with NSTEMI, and a final diagnosis of NSTEMI. The DRG assignment was undercoded — the hospital was underpaid by $11,700 due to documentation ambiguity.

**Financial Impact:** $11,700 in underpaid reimbursement on a single case. If this pattern exists across similar admissions, the aggregate revenue impact is significant.

**Root Cause:**
The provider's documentation used "rule out MI" language rather than a final diagnosis. Coders are required to code to the highest degree of certainty documented — but "rule out" is ambiguous. The coding quality audit process caught this, but there was no automated flag for chest pain admissions that could potentially be MI-coded.

**What the RCM Team Did:**
1. Concurrent coding audit identified documentation-to-DRG mismatch
2. Issued physician query requesting diagnostic clarification
3. Physician amended record with NSTEMI diagnosis
4. DRG reclassified — hospital received additional $11,700
5. Educated ED and hospitalist group on final diagnosis documentation requirements (must resolve "rule out" language before discharge)
6. Implemented coder query protocol for all "rule out" cardiac admissions
7. Added DRG 280/281 vs. DRG 309/310/311 logic to coding decision support tool
8. Added "atypical chest pain" + cardiac biomarker logic as a coder prompt

**Outcome:** $11,700 recovered through DRG reclassification. Coding query protocol established for cardiac "rule out" admissions. Physician documentation education completed.

**Lesson Learned:** "Rule out" documentation is a revenue integrity trap. Coders can only assign DRGs based on documented diagnoses — if providers don't resolve "rule out" language to a final diagnosis before discharge, the hospital gets paid on the lower-weighted code. Physician queries work, but proactive documentation improvement with the ED and hospitalist teams prevents the ambiguity in the first place.

**SparkChange Angle:** At SparkChange, JB should understand that DRG accuracy is among the highest-leverage revenue cycle issues in the inpatient space. A single DRG reclassification recovered $11,700 on one case. Automated coding decision support — flags that prompt coders to query when chest pain + elevated biomarkers suggests MI — multiplies that recovery across every similar case. If SparkChange is building or implementing coding audit tools, DRG-specific clinical documentation prompts (triggered by ICD-10/CPT combinations) are a high-ROI automation target.

---

*Document version: 1.0 | RCM Pulse Curriculum | SparkChange RCM Operations Reference*
*For JB Burkett — drill weekly, apply daily.*

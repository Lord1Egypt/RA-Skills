# Known Use Cases (KUC)

Total: **18**

## `KUC-101`
**Source**: `lending/tests/test_utils.py`

Provides shared test utilities and setup functions needed by each lending module tests, including master initialization, loan product creation, and customer setup.

## `KUC-102`
**Source**: `lending/loan_management/doctype/loan_refund/test_loan_refund.py`

Tests the loan closure process when a borrower requests a refund of excess amounts after repaying the loan.

## `KUC-103`
**Source**: `lending/loan_management/doctype/loan_application/test_loan_application.py`

Tests the creation and processing of loan applications including rate of interest configuration and applicant details.

## `KUC-104`
**Source**: `lending/loan_management/doctype/loan_security_deposit/test_loan_security_deposit.py`

Tests security deposit adjustments for secured loans where borrowers pledge collateral.

## `KUC-105`
**Source**: `lending/loan_management/doctype/loan/test_loan.py`

Comprehensive testing of the core Loan doctype including loan closure requests, security unpledging, disbursement amounts, interest accrual, repayment calculations, and loan classification.

## `KUC-106`
**Source**: `lending/loan_management/doctype/loan_adjustment/test_loan_adjustment.py`

Tests loan balance adjustments after loan disbursement, including interest accrual processing and demand generation.

## `KUC-107`
**Source**: `lending/loan_management/doctype/loan_repayment_repost/test_loan_repayment_repost.py`

Tests the reposting of loan repayments when backdated transactions occur, ensuring repayment allocations are correctly reset.

## `KUC-108`
**Source**: `lending/loan_management/doctype/loan_security_shortfall/test_loan_security_shortfall.py`

Tests scenarios where pledged security value falls below required margin, triggering shortfall alerts and collateral top-up requirements.

## `KUC-109`
**Source**: `lending/loan_management/doctype/loan_security_assignment/test_loan_security_assignment.py`

Tests the assignment and pledging of security assets when taking a secured loan.

## `KUC-110`
**Source**: `lending/loan_management/doctype/loan_restructure/test_loan_restructure.py`

Tests loan restructuring operations including term modifications, rate changes, and loan classification updates for distressed loans.

## `KUC-111`
**Source**: `lending/loan_management/doctype/sanctioned_loan_amount/test_sanctioned_loan_amount.py`

Tests sanctioned loan amount limits for secured loans based on pledged security values and LTV ratios.

## `KUC-112`
**Source**: `lending/loan_management/doctype/loan_repayment_schedule/test_loan_repayment_schedule.py`

Tests loan repayment schedule generation and moratorium period calculations, especially after loan restructuring.

## `KUC-113`
**Source**: `lending/loan_management/doctype/loan_interest_accrual/test_loan_interest_accrual.py`

Tests interest accrual processing including batch processing, freeze date handling, and daily/monthly accrual frequencies.

## `KUC-114`
**Source**: `lending/loan_management/doctype/loan_disbursement/test_loan_disbursement.py`

Tests loan disbursement processes including creation of sales invoices for disbursement charges.

## `KUC-115`
**Source**: `lending/loan_origination/doctype/loan_document_type/test_loan_document_type.py`

Integration tests for LoanDocumentType doctype used in loan origination workflows.

## `KUC-116`
**Source**: `lending/loan_origination/doctype/loan_purpose/test_loan_purpose.py`

Integration tests for LoanPurpose doctype defining loan purpose categories in origination.

## `KUC-117`
**Source**: `lending/loan_origination/doctype/loan_origination_settings/test_loan_origination_settings.py`

Integration tests for LoanOriginationSettings doctype containing configuration for the loan origination process.

## `KUC-118`
**Source**: `lending/loan_origination/doctype/loan_lead/test_loan_lead.py`

Integration tests for LoanLead doctype used in tracking potential loan applicants before application submission.

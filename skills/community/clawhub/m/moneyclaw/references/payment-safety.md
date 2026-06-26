# Authorized Payment Safety Reference

Use this reference when:

- you are about to enter card details on an unfamiliar site
- the checkout asks for unexpected additional verification
- a merchant declines payment and you need retry guidance
- you need to confirm whether a payment step is within the user's authorized scope

## Table of Contents

1. Authorization Boundaries
2. Pre-Payment Checklist
3. Additional Verification And Retry Rules
4. When To Stop And Ask The User

## 1. Authorization Boundaries

Follow these rules for every MoneyClaw payment flow:

- only use MoneyClaw for purchases or payment flows explicitly requested by the user; if the account is not clearly configured for agent auto-approval and the next step is not explicitly requested, stop and ask
- only use wallet, card, and billing data returned by the user's own MoneyClaw account
- respect merchant, issuer, card-network, and verification controls
- treat fraud checks, KYC, sanctions, geography rules, merchant restrictions, issuer declines, and other payment controls as hard boundaries
- never fabricate billing identity, cardholder data, addresses, names, phone numbers, or verification information
- prefer prepaid, bounded-risk flows by default

## 2. Pre-Payment Checklist

Run this checklist before entering card details:

1. Verify the exact domain. In `paypal.com.secure-verify.net`, the real domain is `secure-verify.net`.
2. Confirm the user explicitly asked to continue this exact payment step, unless the account is clearly configured to auto-approve agent-created payment tasks for this scope.
3. Confirm HTTPS is present, but do not treat HTTPS alone as proof of legitimacy.
4. Confirm the total amount and currency.
5. Confirm wallet or prepared execution balance covers the amount plus a small buffer.
6. Use the billing address from the prepared execution details. Do not invent one.
7. Confirm the purchase matches the user's request or the already approved scope.
8. If the merchant asks for information that is not present in the account data, stop and ask the user.
9. If the flow shows obvious scam signals, do not continue.

## 3. Additional Verification And Retry Rules

- do not treat extra verification as a normal default path for MoneyClaw payments
- do not invent, infer, or work around an additional verification step
- never retry immediately after a merchant error; read transaction history first
- maximum two retries per merchant session unless the user explicitly confirms further attempts
- do not keep retrying after repeated CVV or extra-verification failures
- if the merchant, inbox, and transaction history give conflicting signals, stop and inspect state before doing anything else

Common guidance:

- `INSUFFICIENT_BALANCE`: top up or reduce purchase amount
- `CARD_NOT_ACTIVE`: the payment step is not ready yet
- merchant-side error with no clear payment result: inspect the payment task and wallet activity before trying again

## 4. When To Stop And Ask The User

Stop and ask the user if any of these are true:

- the merchant requests identity documents, social security numbers, bank account data, or unusual verification details
- the amount, currency, or merchant domain no longer matches the expected purchase
- the merchant or issuer decline appears related to compliance, sanctions, geography, or merchant policy
- the checkout asks for contact or identity information that is not already present in the user's account data
- you are no longer sure the flow is within the user's requested or account-configured auto-approved scope

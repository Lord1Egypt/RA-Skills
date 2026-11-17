## Description:

This skill helps agents query and manage Shopee store payment, settlement, escrow, payout, wallet transaction, income report, and installment-status workflows through LinkFox gateway scripts for the Shopee Open API Payment module.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketplace operators use this skill to inspect Shopee store settlement data, payout details, wallet transactions, income reports, and installment payment settings for already-authorized stores.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles LinkFox API keys, shop identifiers, and Shopee payment or settlement data.

Mitigation: Install and run it only when the user trusts LinkFox to proxy Shopee Payment data, and avoid pasting or logging full API keys.

Risk: Gateway destination can be affected by LinkFox gateway override environment variables.

Mitigation: Use override environment variables only when the destination is controlled and expected.

Risk: Full API responses may be saved in linkfox session folders and can include financial data.

Mitigation: Review saved files under linkfox session folders before sharing, committing, or retaining them.

Risk: Some scripts can change installment settings or initiate billing purchase flows.

Mitigation: Require explicit user confirmation before running installment-changing commands or billing purchase commands.

Risk: Feedback reporting may transmit observations about skill behavior.

Mitigation: Avoid including sensitive store, settlement, credential, or customer data in feedback content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-payment)
- [Shopee Payment API index](https://open.shopee.com/documents/v2/v2.payment.get_escrow_detail?module=97&type=1)
- [Payment module API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [generate_income_report API reference](references/apis/generate-income-report.md)
- [generate_income_statement API reference](references/apis/generate-income-statement.md)
- [get_billing_transaction_info API reference](references/apis/get-billing-transaction-info.md)
- [get_escrow_detail API reference](references/apis/get-escrow-detail.md)
- [get_escrow_detail_batch API reference](references/apis/get-escrow-detail-batch.md)
- [get_escrow_list API reference](references/apis/get-escrow-list.md)
- [get_income_detail API reference](references/apis/get-income-detail.md)
- [get_income_overview API reference](references/apis/get-income-overview.md)
- [get_income_report API reference](references/apis/get-income-report.md)
- [get_income_statement API reference](references/apis/get-income-statement.md)
- [get_item_installment_status API reference](references/apis/get-item-installment-status.md)
- [get_payment_method_list API reference](references/apis/get-payment-method-list.md)
- [get_payout_detail API reference](references/apis/get-payout-detail.md)
- [get_payout_info API reference](references/apis/get-payout-info.md)
- [get_shop_installment_status API reference](references/apis/get-shop-installment-status.md)
- [get_wallet_transaction_list API reference](references/apis/get-wallet-transaction-list.md)
- [set_item_installment_status API reference](references/apis/set-item-installment-status.md)
- [set_shop_installment_status API reference](references/apis/set-shop-installment-status.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance, shell commands, and JSON responses saved to local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are persisted under a linkfox session data folder; large responses are summarized unless inline output is requested.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

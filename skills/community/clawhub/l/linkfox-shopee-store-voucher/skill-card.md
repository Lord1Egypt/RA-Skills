## Description:

Shopee-店铺优惠券 helps agents manage Shopee store voucher campaigns through LinkFox, including creating, listing, viewing, updating, ending, and deleting vouchers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and ecommerce operators use this skill to manage Shopee store voucher activity from an agent workflow. It supports voucher creation, lookup, updates, early ending, and deletion for authorized Shopee shops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform destructive voucher actions such as delete, end, and update.

Mitigation: Confirm delete, end, and update actions explicitly before running the related scripts.

Risk: The skill handles LinkFox account credentials for Shopee voucher operations.

Mitigation: Use a trusted environment and prefer a secret manager or per-session environment variable for API keys.

Risk: Endpoint environment variable overrides can redirect LinkFox/Shopee operations.

Mitigation: Avoid overriding LinkFox endpoint environment variables unless the target endpoint is trusted.

Risk: Saved response files may contain sensitive business data.

Mitigation: Treat saved LinkFox response files as sensitive and remove them when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-shopee-store-voucher)
- [Shopee Voucher API overview](references/api.md)
- [add_voucher reference](references/apis/add-voucher.md)
- [delete_voucher reference](references/apis/delete-voucher.md)
- [end_voucher reference](references/apis/end-voucher.md)
- [get_voucher_list reference](references/apis/get-voucher-list.md)
- [get_voucher reference](references/apis/get-voucher.md)
- [update_voucher reference](references/apis/update-voucher.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [Shopee Open Platform voucher add_voucher documentation](https://open.shopee.com/documents/v2/v2.voucher.add_voucher?module=112&type=1)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with Python command examples, JSON responses, and saved response files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full API responses are saved locally; larger responses may be summarized in stdout unless inline output is requested.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.

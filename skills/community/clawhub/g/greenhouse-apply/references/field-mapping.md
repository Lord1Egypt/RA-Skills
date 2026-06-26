# Greenhouse Field Mapping Reference

## Standard Fields
| Field | Type | Notes |
|-------|------|-------|
| First Name | text input | Required |
| Last Name | text input | Required |
| Email | text input | Required, triggers verification |
| Phone | text input | Digits only, auto-formats |
| Phone Country | intl-tel-input | Separate widget |
| Resume/CV | file upload | pdf/doc/docx/txt/rtf |
| Website | text input | Optional |
| LinkedIn | text input | Often required |

## Verification Code Inputs
IDs: security-input-0 through security-input-7 (maxLength=1 each)
Always use getElementById, never snapshot refs.
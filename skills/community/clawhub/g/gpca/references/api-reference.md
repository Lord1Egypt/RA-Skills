# GPCA MCP Tools Reference

## Authentication & Registration
| Tool | Purpose | Params |
|------|---------|--------|
| `gpca_get_captcha` | Get captcha image (base64 PNG) for registration | — |
| `gpca_register` | Register new account (sends email code) | `email`, `username`, `password`, `r_password`, `validate_code`, `recommender_code?` |
| `gpca_finish_register` | Complete registration with email code | `register_id`, `verify_code` |
| `gpca_login` | Start login (sends email code) | `email`, `password` |
| `gpca_verify_login` | Complete login with code | `code` |
| `gpca_send_reset_password_email` | Send password reset code | `email` |
| `gpca_reset_password` | Reset password with code | `email`, `code`, `new_password` |
| `gpca_auth_status` | Check if authenticated | — |
| `gpca_get_user_info` | Get user profile | — |

## Card Management
| Tool | Purpose | Params |
|------|---------|--------|
| `gpca_list_cards` | List user's cards | — |
| `gpca_supported_cards` | Available card types | — |
| `gpca_order_virtual_card` | Apply for virtual card | `card_type_id` |
| `gpca_bind_card` | Bind a card | `card_id` |
| `gpca_activate_card` | Activate card | `card_id` |
| `gpca_freeze_card` | Freeze/unfreeze card | `card_id` |
| `gpca_change_pin` | Change card PIN | `card_id`, `old_pin`, `new_pin` |
| `gpca_reset_pin` | Reset card PIN | `card_id` |
| `gpca_get_cvv` | Get card CVV | `card_id` |
| `gpca_card_transactions` | Card transaction history | `card_id`, `start_time?`, `end_time?` |

## Wallet
| Tool | Purpose | Params |
|------|---------|--------|
| `gpca_wallet_balance` | USDT balance | — |
| `gpca_supported_chains` | Supported blockchains | — |
| `gpca_deposit_address` | Wallet deposit address | `chain_id?` |
| `gpca_bank_card_list` | Cards for deposit | — |
| `gpca_deposit_to_card` | USDT → USD to card | `card_id`, `amount` |
| `gpca_wallet_transactions` | Wallet history | `start_time?`, `end_time?` |

## KYC
| Tool | Purpose | Params |
|------|---------|--------|
| `gpca_check_kyc` | KYC status | — |
| `gpca_request_kyc` | Start Mastercard KYC | `kyc_data` |
| `gpca_request_kyc_visa` | Start Visa KYC | `kyc_data` |
| `gpca_submit_kyc` | Submit KYC | `kyc_data` |
| `gpca_add_kyc_file` | Upload KYC document | `file_data`, `file_type` |
| `gpca_reset_kyc` | Reset KYC | — |

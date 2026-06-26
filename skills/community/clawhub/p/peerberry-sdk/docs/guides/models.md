# Typed Models

The SDK returns dataclass-based models for most read operations.

Each model is immutable (`frozen=True`) and retains the original payload in `raw`.

## Why Models Matter

- More predictable field access than raw dicts
- Decimal-aware numeric parsing for monetary data
- Stable shape at service boundaries
- Easy fallback to original payload with `.to_dict()`

## Common Model Conventions

- Missing or invalid source values become `None` when appropriate
- Numeric-like values are parsed to `Decimal`/`int` where defined by model
- Unknown extra fields are preserved in `raw`

## Profile and Portfolio Models

## `Profile`

Fields:

- `public_id: str | None`
- `email: str | None`
- `first_name: str | None`
- `last_name: str | None`
- `currency: str | None`

## `Overview`

Fields:

- `data: dict[str, Any]`

Notes:

- This model intentionally preserves overview payload shape as-is in `data`.

## `LoyaltyTier`

Fields:

- `tier: str | None`
- `extra_return: str | None`
- `max_amount: Decimal | None`
- `min_amount: Decimal | None`

## `ProfitPoint`

Fields:

- `period: str | None`
- `amount: Decimal | None`

## `InvestmentStatusOverview`

Fields:

- `data: dict[str, Any]`

## `OriginatorsOverview`

Fields:

- `data: dict[str, dict[str, Any]]`

## Loan and Investment Models

## `Loan`

Fields:

- `loan_id: int | None`
- `country: str | None`
- `originator: str | None`
- `status: str | None`
- `interest_rate: Decimal | None`
- `amount: Decimal | None`
- `available_to_invest: Decimal | None`
- `term: int | None`
- `currency: str | None`

## `LoanPage`

Fields:

- `data: list[Loan]`
- `total: int | None`
- `page_size: int | None`
- `offset: int | None`

## `SecondaryLoan`

Fields:

- `sale_id: str | None`
- `investment_id: int | None`
- `sale_amount: Decimal | None`
- `sale_status: str | None`
- `sale_valid_until: str | None`
- `originator_title: str | None`
- `loan_id: int | None`
- `loan_term_type: str | None`
- `loan_interest: Decimal | None`
- `remaining_principal: Decimal | None`
- `remaining_term: int | None`
- `seller: bool | None`
- `country_id: int | None`
- `country_iso: str | None`
- `investment_interest: Decimal | None`
- `final_payment_date: str | None`
- `investment_date: str | None`
- `loan_status: str | None`

## `SecondaryLoanPage`

Fields:

- `items: list[SecondaryLoan]`
- `total: int | None`
- `page_count: int | None`
- `current_page: int | None`
- `page_size: int | None`
- `offset: int | None`
- `available_sort_fields: dict[str, str]`

## `LoanDetails`

Fields:

- `borrower_data: dict[str, Any]`
- `loan: Loan | None`
- `originator_data: dict[str, Any]`
- `pledge_data: dict[str, Any]`
- `schedule_data: list[dict[str, Any]]`

## `Investment`

Fields:

- `investment_id: int | None`
- `loan_id: int | None`
- `country: str | None`
- `status: str | None`
- `amount: Decimal | None`
- `interest_rate: Decimal | None`
- `currency: str | None`
- `purchase_date: str | None`

## `InvestmentPage`

Fields:

- `data: list[Investment]`
- `total: int | None`
- `page_size: int | None`
- `offset: int | None`

## Transactions and Summary Models

## `Transaction`

Fields:

- `transaction_id: str | None`
- `type: str | None`
- `amount: Decimal | None`
- `currency: str | None`
- `occurred_at: str | None`
- `description: str | None`

## `AccountSummary`

Fields:

- `balance_data: dict[str, Any]`
- `cash_flow_data: dict[str, Any]`
- `currency: str | None`

## `PurchaseOrder`

Fields:

- `order_id: int | None`

## Model Usage Patterns

## Safe Field Access

```python
profile = api.get_profile()
print(profile.public_id)
```

## Fallback To Raw Payload

```python
loan = api.get_loans(quantity=1)[0]
print(loan.raw)
print(loan.to_dict())
```

## Decimal-Safe Processing

```python
from decimal import Decimal

investments = api.get_investments(quantity=50)
total = sum((inv.amount or Decimal("0")) for inv in investments.data)
print(total)
```

## Converting Lists To Models Manually

The helper `to_models(items, model_class)` can map iterable payloads to models.

```python
from peerberry_sdk.models import to_models, Transaction

transactions = to_models(raw_items, Transaction)
```

## Return Type Matrix

| API method | Return |
| --- | --- |
| `get_profile()` | `Profile` |
| `get_overview()` | `Overview` |
| `get_loyalty_tier()` | `LoyaltyTier` |
| `get_profit_overview()` | `list[ProfitPoint]` |
| `get_investment_status()` | `InvestmentStatusOverview` |
| `get_investment_originators_overview()` | `OriginatorsOverview` |
| `get_loans()` | `list[Loan]` |
| `get_loans_page()` | `LoanPage` |
| `get_secondary_loans()` | `SecondaryLoanPage` |
| `get_loan_details()` | `LoanDetails` |
| `purchase_loan()` | `PurchaseOrder` |
| `get_investments()` | `InvestmentPage` |
| `get_transactions()` | `list[Transaction]` |
| `get_account_summary()` | `AccountSummary` |
| `get_mass_investments()` | `bytes` |
| `get_mass_transactions()` | `bytes` |
| `get_agreement()` | `bytes` |

## Related Docs

- [Client API Reference](../api/client.md)
- [Error Handling](error-handling.md)

# API Quick Reference

This file is the fast source of truth for method routing, accepted values, and error handling.

## Main Client

```python
PeerberryClient(
    email: Optional[str] = None,
    password: Optional[str] = None,
    tfa_secret: Optional[str] = None,
    access_token: Optional[str] = None,
    refresh_token: Optional[str] = None,
    request_opts: Optional[dict] = None,
    config: Optional[SDKConfig] = None,
    auto_login: bool = True,
)
```

Lifecycle methods:

- `login() -> str`
- `token() -> str`
- `logout() -> str`
- `close(logout: Optional[bool] = None) -> None`

## Method Map

Profile and portfolio:

- `get_profile() -> Profile`
- `get_overview() -> Overview`
- `get_loyalty_tier() -> LoyaltyTier`
- `get_profit_overview(start_date: date, end_date: date, periodicity: str = "day") -> List[ProfitPoint]`
- `get_investment_status() -> InvestmentStatusOverview`
- `get_investment_originators_overview() -> OriginatorsOverview`

Loans and purchases:

- `get_loans(quantity: int, ..., sort: str = "loan_amount", ...) -> List[Loan]`
- `get_loans_page(page_num: int, quantity: int = 40, ..., sort: str = "loan_id", ...) -> LoanPage`
- `get_secondary_loans(quantity: int, start_page: int = 0, ..., sort: Optional[str] = None, ...) -> SecondaryLoanPage`
- `get_loan_details(loan_id: int) -> LoanDetails`
- `get_agreement(loan_id: int, lang: str = "en") -> bytes`
- `purchase_loan(loan_id: int, amount: Decimal) -> PurchaseOrder`

Investments and cash flow:

- `get_investments(quantity: int, ..., current: bool = True) -> InvestmentPage`
- `get_mass_investments(countries: Optional[List[str]] = None, current: bool = True) -> bytes`
- `get_account_summary(start_date: date, end_date: date) -> AccountSummary`
- `get_transactions(quantity: Optional[int] = None, ..., period: Optional[str] = None, transaction_types: Optional[List[Union[str, int]]] = None, ...) -> List[Transaction]`
- `get_mass_transactions(start_date: Optional[date], end_date: Optional[date], transaction_types: Optional[List[Union[str, int]]] = None, period: Optional[str] = None, loan_id: Optional[int] = None) -> bytes`

Metadata helpers:

- `get_countries() -> dict`
- `get_originators() -> dict`

## Accepted Values

### Loan Sort (`get_loans`, `get_loans_page`)

- `loan_id`
- `term`
- `issued_date`
- `interest_rate`
- `loan_amount`

### Loan Types

- `short_term`
- `long_term`
- `real_estate`
- `leasing`
- `business`

### Profit Periodicity (`get_profit_overview`)

- `day`
- `month`
- `year`

### Transaction Period (`get_transactions`, `get_mass_transactions`)

- `today`
- `thisWeek`
- `thisMonth`

### Transaction Type Named Keys

- `deposit`
- `withdrawal`
- `principal_repayment`
- `interest_payment`
- `investment`
- `fees_and_bonuses`

### Secondary Market Sort (`get_secondary_loans`)

- `remaining_term`
- `loan_interest`
- `remaining_principal`
- `sale_amount`
- `final_payment_date`
- `sale_valid_until`

## Parameter Semantics and Units

- Use `Decimal` for money/rates.
- `purchase_loan(..., amount=...)` expects EUR-denominated amount.
- Interest filters are percentage-style decimals (`Decimal("9.5")` means 9.5%).
- `start_page` is zero-based.
- `quantity` is row count.
- `countries=[...]` expects PeerBerry display names, not raw ISO code.
- Resolve country/originator names dynamically from `get_countries()` and `get_originators()`.

## Model Notes

Most read methods return typed dataclasses with `raw` payload retained.

Common models:

- `Profile`
- `Overview`
- `Loan`
- `LoanPage`
- `InvestmentPage`
- `Transaction`
- `AccountSummary`
- `PurchaseOrder`

Payload caveat:

- `Overview.data` may be flat or nested under `items`.

## Exceptions To Handle

Authentication and lifecycle:

- `InvalidCredentials`
- `AuthenticationError`
- `TokenRefreshError`

Validation and input errors:

- `InvalidSort`
- `InvalidPeriodicity`
- `InvalidType`

Investment execution:

- `InsufficientFunds`

Catch-all SDK base:

- `PeerberryException`

## Minimal Error-Resilient Pattern

```python
from peerberry_sdk import (
    AuthenticationError,
    InsufficientFunds,
    InvalidCredentials,
    PeerberryClient,
    PeerberryException,
    TokenRefreshError,
)

try:
    with PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD") as api:
        print(api.get_overview().data)
except InvalidCredentials:
    print("Invalid credentials")
except AuthenticationError:
    print("2FA required or auth flow failed")
except TokenRefreshError:
    print("Refresh token flow failed")
except InsufficientFunds:
    print("Insufficient funds for purchase")
except PeerberryException as exc:
    print(f"SDK/API error: {exc}")
```

## Method Hallucination Guard

Do not invent these names:

- `invest(...)`
- `get_account_balance(...)`
- `list_available_loans(...)`
- `get_portfolio_overview(...)`

Use actual methods:

- `get_overview()`
- `get_loans(...)`
- `purchase_loan(...)`
- `get_investments(...)`

## Debugging Checklist

1. Auth failures:
   - confirm credentials
   - if account uses 2FA, install `peerberry-sdk[otp]` and pass `tfa_secret`
2. Filter errors:
   - verify sort/period/type enums
   - verify country/originator display names from metadata helpers
3. Unexpected field shape:
   - inspect model `.raw`
   - handle `Overview.data` flat vs `items` nesting
4. Long-running session issues:
   - call `token()` for manual refresh
   - handle `TokenRefreshError` fallback path

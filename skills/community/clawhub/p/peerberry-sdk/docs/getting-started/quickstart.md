# Quickstart

This guide gets you from zero to a working API session with safe defaults.

## Minimal Working Example

```python
from peerberry_sdk import PeerberryClient

with PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD") as api:
    profile = api.get_profile()
    overview = api.get_overview()
    loans = api.get_loans(quantity=10)

    print("public_id:", profile.public_id)
    print("available money:", overview.data.get("availableMoney"))
    print("loans fetched:", len(loans))
```

What this does:

- authenticates using credentials
- fetches profile and portfolio overview
- fetches first 10 marketplace loans
- closes session automatically at context exit

## First Portfolio Calls

```python
from peerberry_sdk import PeerberryClient

with PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD") as api:
    tier = api.get_loyalty_tier()
    status = api.get_investment_status()
    originators = api.get_investment_originators_overview()

    print("tier:", tier.tier)
    print("status keys:", list(status.data.keys())[:5])
    print("originators:", len(originators.data))
```

## Fetch Loans With Filters

```python
from decimal import Decimal
from peerberry_sdk import PeerberryClient

with PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD") as api:
    loans = api.get_loans(
        quantity=20,
        min_interest_rate=Decimal("10"),
        max_remaining_term=24,
        countries=["Poland", "Lithuania"],
        loan_types=["short_term", "business"],
        sort="interest_rate",
        ascending_sort=False,
        group_guarantee=True,
    )

    for loan in loans[:3]:
        print(loan.loan_id, loan.interest_rate, loan.country)
```

## Inspect Your Investments

```python
from peerberry_sdk import PeerberryClient

with PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD") as api:
    current = api.get_investments(quantity=25, current=True)
    finished = api.get_investments(quantity=25, current=False)

    print("current total:", current.total)
    print("finished total:", finished.total)
```

## Transactions And Account Summary

```python
from datetime import date, timedelta
from peerberry_sdk import PeerberryClient

with PeerberryClient(email="YOUR_EMAIL", password="YOUR_PASSWORD") as api:
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    summary = api.get_account_summary(start_date=start_date, end_date=end_date)
    tx = api.get_transactions(
        quantity=50,
        start_date=start_date,
        end_date=end_date,
        transaction_types=["deposit", "interest_payment", "principal_repayment"],
    )

    print("currency:", summary.currency)
    print("transactions:", len(tx))
```

## Manual Login Flow (Advanced)

Use this when you need to defer authentication until later in your application lifecycle.

```python
from peerberry_sdk import PeerberryClient

api = PeerberryClient(
    email="YOUR_EMAIL",
    password="YOUR_PASSWORD",
    auto_login=False,
)

# do other setup here
api.login()

try:
    print(api.get_profile())
finally:
    api.close(logout=True)
```

## 2FA Quick Example

```python
from peerberry_sdk import PeerberryClient

with PeerberryClient(
    email="YOUR_EMAIL",
    password="YOUR_PASSWORD",
    tfa_secret="BASE32_SECRET",
) as api:
    print(api.get_overview())
```

Install extras first:

```bash
pip install "peerberry-sdk[otp]"
```

## Next Steps

- For token and login lifecycle details: [Authentication](../guides/authentication.md)
- For runtime tuning and retries: [Configuration](../guides/configuration.md)
- For exceptions and production patterns: [Error Handling](../guides/error-handling.md)
- For full method-level contract docs: [Client API Reference](../api/client.md)

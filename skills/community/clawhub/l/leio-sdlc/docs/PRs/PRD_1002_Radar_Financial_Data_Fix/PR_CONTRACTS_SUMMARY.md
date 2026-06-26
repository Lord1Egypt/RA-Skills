status: in_progress

# PR-001: Implement Standalone Fundamental Data Fetcher

## 1. Objective
Create a reliable, standalone function to fetch real-world fundamental data (PE-TTM and Market Cap) using `akshare`, without modifying the existing radar pipeline yet.

## 2. Scope & Implementation Details
- Target Project: `/root/.openclaw/workspace/AMS`
- `finance_fetcher.py` (New): Implement `fetch_fundamental_data()` using a robust endpoint like `akshare.stock_a_indicator_lg()`. Ensure it returns a pandas DataFrame with at least `代码`, `市盈率-动态`, and `总市值`.

## 3. TDD & Acceptance Criteria
- `tests/test_finance_fetcher.py` (New): Write a test that calls `fetch_fundamental_data()` (or mocks the network response) and asserts that the returned DataFrame contains the required columns (`代码`, `市盈率-动态`, `总市值`) and that the values are dynamically retrieved (e.g., PE is not uniformly hardcoded to 15.0).

---

status: open

# PR-002: Integrate Fundamental Data and Remove Hardcoded PE Stub

## 1. Objective
Integrate the `fetch_fundamental_data()` function into the stock radar pipeline, merge it with QMT tick data, and remove the malicious hardcoded PE stub.

## 2. Scope & Implementation Details
- Target Project: `/root/.openclaw/workspace/AMS`
- `pilot_stock_radar.py` & `adapter.py`: Completely remove the fake data stub `df_a["市盈率-动态"] = 15.0`.
- `pilot_stock_radar.py`: Import `fetch_fundamental_data()`. Use `pandas.merge()` on the `代码` column to join the real-time QMT Tick DataFrame with the Financial DataFrame before the valuation filtering logic executes.

## 3. TDD & Acceptance Criteria
- `tests/test_data_source.py`: Add a test that simulates the full merge process (mocking both QMT tick data and fundamental data).
- Assert that the final DataFrame passed to the radar correctly mapped the PE and Market Cap values from the fundamental data, and that `15.0` is not hardcoded.

> [Escalation] Tier 1 Reset triggered due to Coder failure or Arbitrator rejection.

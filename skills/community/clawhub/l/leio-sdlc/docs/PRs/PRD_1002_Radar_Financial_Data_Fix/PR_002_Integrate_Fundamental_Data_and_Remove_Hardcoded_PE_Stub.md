status: closed

# PR-002b: Integrate Fundamental Data and Remove Hardcoded PE Stub

## 1. Objective
Integrate the `fetch_fundamental_data()` function into the stock radar pipeline, merge it with QMT tick data, and remove the malicious hardcoded PE stub.

## 2. Scope & Implementation Details
- Target Project: `/root/.openclaw/workspace/AMS`
- `pilot_stock_radar.py` & `adapter.py`: Completely remove the fake data stub `df_a["市盈率-动态"] = 15.0`.
- `pilot_stock_radar.py`: Import `fetch_fundamental_data()`. Use `pandas.merge()` on the `代码` column to join the real-time QMT Tick DataFrame with the Financial DataFrame before the valuation filtering logic executes.

## 3. TDD & Acceptance Criteria
- `tests/test_data_source.py`: Add a test that simulates the full merge process (mocking both QMT tick data and fundamental data).
- Assert that the final DataFrame passed to the radar correctly mapped the PE and Market Cap values from the fundamental data, and that `15.0` is not hardcoded.

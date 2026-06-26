status: closed

# PR-002a: Implement Standalone Fundamental Data Fetcher

## 1. Objective
Create a reliable, standalone function to fetch real-world fundamental data (PE-TTM and Market Cap) using `akshare`, without modifying the existing radar pipeline yet.

## 2. Scope & Implementation Details
- Target Project: `/root/.openclaw/workspace/AMS`
- `finance_fetcher.py` (New): Implement `fetch_fundamental_data()` using a robust endpoint like `akshare.stock_a_indicator_lg()`. Ensure it returns a pandas DataFrame with at least `代码`, `市盈率-动态`, and `总市值`.

## 3. TDD & Acceptance Criteria
- `tests/test_finance_fetcher.py` (New): Write a test that calls `fetch_fundamental_data()` (or mocks the network response) and asserts that the returned DataFrame contains the required columns (`代码`, `市盈率-动态`, `总市值`) and that the values are dynamically retrieved (e.g., PE is not uniformly hardcoded to 15.0).

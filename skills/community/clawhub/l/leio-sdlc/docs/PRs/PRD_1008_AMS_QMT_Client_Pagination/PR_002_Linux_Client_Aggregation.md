status: in_progress

# PR-002: Linux Client Pagination & Aggregation

## 1. Objective
Update the Linux AMS Client (`AMS/qmt_client.py`) to automatically loop and aggregate data chunks from the Windows Bridge, abstracting the pagination away from the main stock radar pipeline.

## 2. Scope & Implementation Details
- `AMS/qmt_client.py`: Refactor the `get_full_tick()` method.
- Implement a `while` loop requesting `chunk_index=0`, `1`, `2`, etc., with a fixed `chunk_size` (e.g., 500).
- Append the `data` dictionaries from each response into a single master dictionary.
- Break the loop when the size of the accumulated dictionary reaches `total_stocks`, or when an empty data chunk is returned.
- Implement a small delay (`time.sleep(0.2)`) between requests to prevent overwhelming the Windows bridge.
- Ensure backward compatibility so `pilot_stock_radar.py` does not need modifications to its core logic.

## 3. TDD & Acceptance Criteria
- `AMS/tests/test_qmt_client.py`: Create a new mock test `test_get_full_tick_pagination`.
- Mock the HTTP response to return 3 chunks of dummy stock data.
- Assert that `get_full_tick()` successfully returns a single dictionary containing all aggregated items from the 3 mocked chunks.
- Verify `time.sleep` is called between loop iterations.

> [Escalation] Tier 1 Reset triggered due to Coder failure or Arbitrator rejection.

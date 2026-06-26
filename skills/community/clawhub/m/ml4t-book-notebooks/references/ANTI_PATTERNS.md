# Anti-Patterns (Cross-Project)

Total: **15**

## finance-bp-102--Darts (7)

### `AP-TIME-SERIES-ML-001` — TimeSeries values array dimensionality mismatch <sub>(high)</sub>

When constructing a TimeSeries with a values array that is not expanded to exactly 3 dimensions (time×component×sample), downstream model operations expecting the standard 3D shape will fail with dimension mismatches. This causes all downstream models to receive incorrectly formatted data tensors, leading to complete pipeline failure or silent data corruption.

### `AP-TIME-SERIES-ML-002` — Non-floating-point dtype in TimeSeries values <sub>(high)</sub>

When setting TimeSeries values dtype to integer or non-floating-point types, numerical operations produce incorrect results during financial calculations. Financial forecasts require float64 or float32 precision to handle decimal computations accurately; integer dtypes truncate precision and cause accumulation of rounding errors that compound across time steps.

### `AP-TIME-SERIES-ML-003` — Irregular or non-monotonic time index <sub>(high)</sub>

When TimeSeries time index is not strictly monotonically increasing with a well-defined frequency and no gaps, downstream models produce incorrect forecasts due to temporal misalignment. Gap detection methods fail, and any temporal aggregation or differencing operations will produce meaningless results.

### `AP-TIME-SERIES-ML-004` — Time index and values length mismatch at construction <sub>(high)</sub>

When the time index length does not equal the values array first dimension length, TimeSeries construction fails with ValueError at construction time, preventing any data from being loaded into the system. This typically occurs when importing data from CSV or DataFrame sources where column alignment assumptions are incorrect.

### `AP-TIME-SERIES-ML-005` — Missing abstract method implementations in ForecastingModel subclasses <sub>(high)</sub>

When implementing ForecastingModel subclasses without implementing all required abstract methods (fit, predict, min_train_samples, _target_window_lengths, extreme_lags, supports_multivariate, supports_transferable_series_prediction), Python's ABC abstractmethod enforcement causes TypeError at instantiation time, preventing any model from being created.

### `AP-TIME-SERIES-ML-006` — fit() method not returning self for chaining <sub>(medium)</sub>

When fit() method does not return self for method chaining, the fluent interface pattern expected by users breaks at lines 209, 2932, and 3069 where chaining is attempted. Users encounter AttributeError when trying to chain operations like model.fit(series).predict(n_periods).

### `AP-TIME-SERIES-ML-007` — Frequency inference failure with insufficient timesteps <sub>(medium)</sub>

When using fill_missing_dates with fewer than 3 time steps, frequency inference fails with ValueError because at least 3 consecutive timestamps are required to determine a unique constant frequency. Irregular time series cannot be gap-filled without this minimum data.

## finance-bp-121--machine-learning-for-trading (8)

### `AP-TIME-SERIES-ML-008` — Look-ahead bias from random train/test splits <sub>(high)</sub>

When implementing cross-validation for financial time series using random K-fold or standard train_test_split without temporal ordering, future information leaks into training data. This look-ahead bias artificially inflates backtest performance metrics and leads to significant live trading losses when the model encounters truly unseen data.

### `AP-TIME-SERIES-ML-009` — Missing purge gap contaminating validation results <sub>(high)</sub>

When using walking forward split without an embargo gap between train and test periods, overlapping outcomes between training and test periods contaminate validation results. Without purge gap, seemingly good backtest results do not generalize to live performance due to information leakage across the split boundary.

### `AP-TIME-SERIES-ML-010` — Hardcoded credentials in source code <sub>(high)</sub>

When scraping content from websites requiring authentication by hardcoding credentials in source code files, exposed credentials lead to unauthorized access, potential account termination, and security breaches. Credentials should be loaded from environment variables or secure configuration files, never committed to version control.

### `AP-TIME-SERIES-ML-011` — TA-Lib infinite values causing ML model failures <sub>(high)</sub>

When computing technical indicators using TA-Lib (RSI, MACD, ATR) without handling edge cases, division-by-zero produces infinite values that corrupt the feature DataFrame. Gradient-based ML models (neural networks) cannot process infinite values, causing training to fail or produce NaN gradients.

### `AP-TIME-SERIES-ML-012` — MultiIndex structure lost during feature engineering <sub>(high)</sub>

When flattening or renaming the (ticker, date) MultiIndex during feature engineering for multi-ticker trading, downstream stages (prediction_modeling, backtesting) fail because they expect MultiIndex for proper temporal train/test splits. Data corruption occurs silently when multi-ticker data is treated as single-ticker.

### `AP-TIME-SERIES-ML-013` — Missing TA-Lib C library dependency <sub>(high)</sub>

When installing TA-Lib via pip install ta-lib alone without compiling the underlying C library, import fails because the Python package is merely a wrapper around compiled native code. This causes immediate runtime failure for any code attempting to import talib for technical indicator computation.

### `AP-TIME-SERIES-ML-014` — Trading calendar minutes_per_day mismatch <sub>(high)</sub>

When configuring extended-hours trading calendar with incorrect minutes_per_day (e.g., using 960 for extended hours instead of 1600), minute bar alignment with the calendar fails. Backtest prices do not correspond to actual trading times, producing meaningless results that don't reflect real market microstructure.

### `AP-TIME-SERIES-ML-015` — Zipline bundle ingest function signature mismatch <sub>(high)</sub>

When implementing Zipline bundle ingest function with incorrect parameter count or order, Zipline fails with TypeError during bundle ingest because the ingestion pipeline expects exactly 9 parameters in a specific order. Backtesting cannot run at all when bundle ingestion fails, blocking all downstream work.

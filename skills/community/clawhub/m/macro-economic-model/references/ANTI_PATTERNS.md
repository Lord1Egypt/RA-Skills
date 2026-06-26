# Anti-Patterns (Cross-Project)

Total: **14**

## finance-bp-074--FinRobot (1)

### `AP-MACRO-DATA-001` — SEC EDGAR Rate Limit Violation <sub>(high)</sub>

When implementing SEC API calls without applying rate limiting decorators, requests exceed the regulatory 10 requests per second limit. This causes IP blocking from SEC EDGAR, preventing all subsequent access to critical financial filings and completely disrupting the data collection pipeline. FinRobot demonstrates that SEC enforces strict rate limits and missing User-Agent headers compound this by causing silent request failures.

## finance-bp-077--Open_Source_Economic_Model (2)

### `AP-MACRO-DATA-004` — EIOPA Non-Compliant Curve Extrapolation <sub>(high)</sub>

When implementing the Smith-Wilson algorithm for EIOPA Solvency II calculations, using non-EIOPA compliant formulas or incorrect convergence point calculations violates regulatory specifications. The convergence point must use max(U+40, 60) years per EIOPA paragraph 120. Non-compliant formulas will fail regulatory audits for insurance liability calculations and produce incorrect risk-free rates, leading to materially wrong liability valuations.

### `AP-MACRO-DATA-009` — CSV BOM Encoding Corruption in Data Import <sub>(medium)</sub>

When importing CSV portfolio files with special characters without using 'utf-8-sig' encoding to handle BOM markers, CSV files with UTF-8 BOM markers fail to parse correctly. This causes KeyError exceptions when reading row fields, preventing portfolio data from loading entirely. The BOM marker silently corrupts the first column name read by pandas.

## finance-bp-080--FinDKG (3)

### `AP-MACRO-DATA-002` — Temporal Knowledge Graph Look-Ahead Bias <sub>(high)</sub>

When implementing temporal data splitting for knowledge graphs, using non-temporal train/val/test splits causes the model to see future events during training. The violation of train_edges occurring before val_edges and test_edges temporally results in inflated metrics that do not reflect real-world performance. This produces overfit models that fail catastrophically when deployed for actual temporal prediction tasks.

### `AP-MACRO-DATA-008` — DGL Graph Attribute Propagation Failure in Temporal Batching <sub>(medium)</sub>

When implementing temporal knowledge graph data collation without propagating graph attributes (num_relations, num_all_nodes, time_interval) to subgraph variants created by collate_fn, downstream model components encounter missing attribute errors. The EmbeddingUpdater and EdgeModel expect these attributes on all graph objects including subgraphs, causing training to fail with AttributeError.

### `AP-MACRO-DATA-014` — Temporal DataLoader Shuffling Breaking Graph Ordering <sub>(medium)</sub>

When configuring DataLoader for temporal knowledge graph training with shuffle=True, the temporal ordering required for cumulative graph construction is violated. The model receives edges in non-chronological order, breaking the prior_G, batch_G, cumulative_G construction logic that depends on edges_before_batch occurring before edges_in_batch.

## finance-bp-083--Economic-Dashboard (3)

### `AP-MACRO-DATA-003` — Technical Indicator Look-Ahead Bias via Missing Shift <sub>(high)</sub>

When implementing SMA crossover detection (golden/death cross) without using shift(1) to compare current bar state with prior bar state, crossover detection uses current bar data causing look-ahead bias. Signals appear to fire at the same bar as the cross occurs, producing unrealistic backtest results that fail in live trading. Rationalizing this with 'we need the current bar signal immediately' leads to future information leaking into current signals.

### `AP-MACRO-DATA-010` — OHLCV Data Quality Validation Failure <sub>(medium)</sub>

When calculating technical indicators from OHLCV data without verifying required columns (open, high, low, close, volume), missing required OHLCV columns causes ValueError and prevents technical indicator calculation for affected tickers. This blocks downstream regime classification and pattern detection for all tickers with incomplete data.

### `AP-MACRO-DATA-011` — Inconsistent Primary Key Schema Causing JOIN Failures <sub>(medium)</sub>

When storing derived features in DuckDB with a different primary key schema than technical_features table, inconsistent primary keys prevent JOIN operations between tables. This breaks regime classification and pattern detection pipelines. The composite primary key (ticker, date) must be consistent across all feature tables to enable efficient querying and data integrity.

## finance-bp-105--open-climate-investing (5)

### `AP-MACRO-DATA-005` — Factor Regression Using Raw Returns Instead of Excess Returns <sub>(high)</sub>

When computing returns for CAPM/Fama-French factor regression, using raw stock returns instead of subtracting the risk-free rate (Rf) violates standard financial econometric methodology. CAPM/FF regression requires excess returns (Return - Rf); using raw returns produces incorrect beta estimates that misrepresent a stock's systematic risk exposure. This leads to fundamentally flawed risk attribution and portfolio construction decisions.

### `AP-MACRO-DATA-006` — Percentage vs Decimal Unit Mismatch in Factor Data <sub>(high)</sub>

When importing Fama-French factors from CSV files, failing to divide percentage-formatted factors (e.g., 5.2) by 100 before regression causes coefficients scaled by 100x. This produces statistically invalid inference and meaningless factor loadings. The same issue applies to risk-free rate values, corrupting all CAPM beta calculations downstream.

### `AP-MACRO-DATA-007` — Insufficient Regression Observations for Statistical Validity <sub>(medium)</sub>

When implementing factor regression analysis, using fewer than 20 data points after filtering (inner join, winsorization, date range) produces unreliable or undefined t-statistics and p-values. OLS with insufficient observations produces meaningless regression coefficients, making it impossible to distinguish significant factor exposures from noise. This commonly occurs when combining multiple data sources with missing values.

### `AP-MACRO-DATA-012` — Frequency Column Enforcement Missing in Time Series Schema <sub>(medium)</sub>

When creating PostgreSQL schema for time series tables without explicit frequency column enforcement of 'MONTHLY' or 'DAILY' text values, mixed frequency data corrupts regression calculations. Combining incompatible data frequencies produces statistically invalid regression results. The database must enforce frequency consistency to prevent silent data corruption.

### `AP-MACRO-DATA-013` — PostgreSQL Fork in Multiprocessing Context <sub>(medium)</sub>

When implementing multiprocessing for parallel regression execution using fork start method with psycopg2 database connections, child processes inherit corrupted connection state. This causes 'connection already closed' errors or corrupted connection state in child processes, resulting in failed database writes and incomplete factor regression calculations.

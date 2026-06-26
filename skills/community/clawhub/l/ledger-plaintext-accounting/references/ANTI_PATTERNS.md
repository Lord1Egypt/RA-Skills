# Anti-Patterns (Cross-Project)

Total: **15**

## finance-bp-073--ledger (7)

### `AP-ACCOUNTING-002` — Skipping initialization calls before VM/script execution <sub>(high)</sub>

Executing Numscript VM without first calling ResolveResources() and ResolveBalances() causes panics with ErrResourcesNotInitialized or ErrBalancesNotInitialized. This prevents any script execution and leaves transactions in an unrunnable state, blocking financial operations entirely.

### `AP-ACCOUNTING-003` — Mixing different asset types in monetary operations <sub>(high)</sub>

Performing addition, subtraction, or take operations on amounts with different asset types produces invalid financial calculations. This violates the fundamental accounting principle that amounts in different currencies cannot be combined, leading to corrupted account balances and failed reconciliations.

### `AP-ACCOUNTING-004` — Missing insufficient funds validation <sub>(high)</sub>

Failing to detect when account balance cannot cover a requested withdrawal or transfer allows overdrafts beyond permitted limits. This causes real monetary losses, account balance violations, and potential regulatory compliance issues in global markets.

### `AP-ACCOUNTING-005` — Non-atomic transaction commit/rollback <sub>(high)</sub>

Processing database operations without atomic commit/rollback leaves partial state when failures occur. This corrupts account balances and volumes, violating double-entry bookkeeping integrity and making audit trails unreliable for global regulatory compliance.

### `AP-ACCOUNTING-006` — On-demand posting generation causing double-spending <sub>(high)</sub>

Computing postings on-demand rather than accumulating them during transaction execution fails to track already-spent funds within the same transaction. This creates double-spending vulnerabilities that violate atomic transaction semantics and can result in significant financial losses.

### `AP-ACCOUNTING-007` — Log insertion after transaction commit breaking event sourcing <sub>(high)</sub>

Committing the transaction before inserting the audit log breaks the event sourcing pattern fundamental to accounting integrity. This makes it impossible to rebuild state from logs and violates audit requirements necessary for global financial compliance.

### `AP-ACCOUNTING-008` — Incomplete transaction log hash chaining <sub>(high)</sub>

Computing log hashes without including the previous log hash breaks the immutable audit trail chain. This allows undetected tampering with historical transaction records, compromising financial integrity and regulatory audit compliance.

## finance-bp-073--ledger, finance-bp-129--beancount (1)

### `AP-ACCOUNTING-001` — Using floating-point arithmetic for monetary amounts <sub>(high)</sub>

Representing currency values with float64 or similar floating-point types causes precision loss during arithmetic operations. Rounding errors accumulate over multiple transactions, leading to incorrect balance calculations and potential financial losses. This violates the fundamental requirement that monetary calculations must be exact.

## finance-bp-078--fava_investor (4)

### `AP-ACCOUNTING-009` — Incorrect row data access patterns on query results <sub>(high)</sub>

Using dictionary notation (row['column_name']) on namedtuple query results raises TypeError since namedtuples only support attribute access. This breaks all module queries expecting attribute-style access, causing asset allocation, tax loss harvesting, and other critical financial computations to fail.

### `AP-ACCOUNTING-010` — Missing bidirectional inference for fund relationship declarations <sub>(medium)</sub>

When relationship A→B is declared but B→A is not inferred, the TLH partner list becomes incomplete. This leads to suboptimal tax-loss harvesting decisions where only some funds show all valid swap options, reducing potential tax savings for investors.

### `AP-ACCOUNTING-011` — Wash sale comparison within substantially identical groups <sub>(high)</sub>

Comparing a ticker to itself in its own substantially identical group falsely triggers wash sale warnings. This incorrectly blocks valid tax-loss harvesting transactions, causing investors to miss opportunities to realize tax losses and offset capital gains.

### `AP-ACCOUNTING-012` — Missing substantially identical tickers in wash sale queries <sub>(high)</sub>

Omitting substantially identical fund tickers from the wash sale comparison set allows purchases of similar funds within the 30-day window. This triggers unintended wash sales that disallow tax loss claims on subsequent sales of the original position.

## finance-bp-129--beancount (3)

### `AP-ACCOUNTING-013` — Using parsed entries with MISSING sentinel values for calculations <sub>(high)</sub>

Using parsed entries directly that contain MISSING sentinel values for balance or cost computations causes runtime errors or silent zero-value calculations. This results in incorrect portfolio valuations and reconciliation failures, compromising financial reporting accuracy.

### `AP-ACCOUNTING-014` — Underspecified interpolation with multiple missing values per currency <sub>(high)</sub>

Having more than one missing value per currency group creates an underdetermined system with no unique solution during interpolation. This causes InterpolationError and transaction failure, blocking balance calculations for affected accounts.

### `AP-ACCOUNTING-015` — Violating accounting identity in opening balance transactions <sub>(high)</sub>

Creating opening balance transactions where the total balance of summarized entries does not equal exactly zero violates the fundamental accounting identity (Assets = Liabilities + Equity). This causes the balance sheet to be fundamentally incorrect with non-zero total assets and liabilities.

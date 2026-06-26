# Cross-Project Wisdom

Total: **10**

## `CW-INSURANCE-001` — Validate input data format and type before computation
**From**: finance-bp-063--chainladder-python, finance-bp-126--lifelines · **Applicable to**: insurance-actuarial

Both triangle construction and survival analysis require strict input validation: numeric types for triangle columns, valid event indicators (0/1), no NaN/Inf values, and correct temporal ordering. This prevents downstream numerical failures and ensures mathematical validity of actuarial computations.

## `CW-INSURANCE-002` — Initialize probability distributions to boundary values
**From**: finance-bp-065--pyliferisk, finance-bp-126--lifelines · **Applicable to**: insurance-actuarial

Survival probability S(0) must equal 1.0 and life table lx must start at standard radix (100000) and end at 0. Properly initializing boundary values ensures actuarial quantities have correct scale and interpretation as probability distributions.

## `CW-INSURANCE-003` — Include iteration limits in numerical root-finding
**From**: finance-bp-064--insurance_python · **Applicable to**: insurance-actuarial

Bisection and other root-finding algorithms must include maxIter parameters and verify interval contains valid root (sign change). This prevents infinite loops when calibration fails, ensuring service availability in regulatory compliance workflows.

## `CW-INSURANCE-004` — Avoid bare except clauses that mask TypeErrors
**From**: finance-bp-065--pyliferisk · **Applicable to**: insurance-actuarial

Bare except clauses that catch all exceptions including TypeError and return default values (0 or None) mask fundamental parameter errors. Use specific exception handling and validate inputs upfront to fail fast with clear error messages.

## `CW-INSURANCE-005` — Preserve standard radix and extinction conventions in life tables
**From**: finance-bp-065--pyliferisk · **Applicable to**: insurance-actuarial

Life insurance calculations rely on industry-standard conventions: radix of 100000 at age 0 and lx[-1]=0 for complete extinction. Deviating from these conventions scales all derived quantities incorrectly and breaks interoperability with other actuarial systems.

## `CW-INSURANCE-006` — Ensure workflow step ordering and parameter consistency
**From**: finance-bp-063--chainladder-python, finance-bp-064--insurance_python · **Applicable to**: insurance-actuarial

Multi-step algorithms (triangle transformations, Smith-Wilson calibration) require strict step ordering: compute calibration vector before extrapolation, use consistent alpha values throughout. Violating workflow order produces undefined or mathematically inconsistent results.

## `CW-INSURANCE-007` — Validate probability bounds for confidence intervals
**From**: finance-bp-126--lifelines · **Applicable to**: insurance-actuarial

Confidence interval bounds must be constrained to [0,1] for probability estimates. Use fillna and formula constraints to ensure CI bounds remain valid probability ranges, preventing invalid statistical inference from actuarial models.

## `CW-INSURANCE-008` — Validate matrix properties before decomposition
**From**: finance-bp-065--pyliferisk, finance-bp-064--insurance_python · **Applicable to**: insurance-actuarial

Positive semi-definite matrices must be verified before Cholesky decomposition. Invalid matrices cause math domain errors or invalid correlated samples. Similarly, correlation coefficients must be validated to [-1,1] bounds before use in sqrt(1-rho²).

## `CW-INSURANCE-009` — Make defensive copies of input DataFrames
**From**: finance-bp-126--lifelines · **Applicable to**: insurance-actuarial

User-provided DataFrames should be copied before inplace modifications (.pop(), .drop()). This preserves user data integrity and prevents side effects from leaking into caller code, maintaining data isolation principles.

## `CW-INSURANCE-010` — Exclude incomplete diagonals from historical analysis
**From**: finance-bp-063--chainladder-python · **Applicable to**: insurance-actuarial

The latest diagonal in claims triangles contains incomplete development data from the current period. Excluding this diagonal via valuation_date filtering ensures development factors capture only completed, reliable historical patterns for unbiased IBNR estimation.

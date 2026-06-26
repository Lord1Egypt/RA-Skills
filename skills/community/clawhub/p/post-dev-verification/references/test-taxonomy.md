# Test Taxonomy & Boundary Value Analysis Reference > Systematic test design guidance for AI-generated code verification.
> Covers MFT, INV, DIR categories and boundary value analysis. --- ## Table of Contents - [1. MFT -- Minimum Functionality Tests](#1-mft--minimum-functionality-tests) - [1.1 Definition](#11-definition) - [1.2 When to Use](#12-when-to-use) - [1.3 How to Design](#13-how-to-design) - [1.4 Minimum Requirement](#14-minimum-requirement) - [1.5 Pseudocode Example](#15-pseudocode-example)
- [2. INV -- Invariance Tests](#2-inv--invariance-tests) - [2.1 Definition](#21-definition) - [2.2 When to Use](#22-when-to-use) - [2.3 How to Design](#23-how-to-design) - [2.4 Common Variation Strategies](#24-common-variation-strategies) - [2.5 Pseudocode Example](#25-pseudocode-example)
- [3. DIR -- Directional Expectation Tests](#3-dir--directional-expectation-tests) - [3.1 Definition](#31-definition) - [3.2 When to Use](#32-when-to-use) - [3.3 How to Design](#33-how-to-design) - [3.4 Pseudocode Example](#34-pseudocode-example)
- [4. Boundary Value Analysis](#4-boundary-value-analysis) - [4.1 Numeric Ranges](#41-numeric-ranges) - [4.2 String & Collection Lengths](#42-string--collection-lengths) - [4.3 Special Values Checklist](#43-special-values-checklist) - [4.4 Data Feature Dimensions](#44-data-feature-dimensions)
- [5. Applying the Taxonomy -- Workflow](#5-applying-the-taxonomy--workflow) - [Step 0: Map Business Flows](#step-0-map-business-flows) - [Step 1: Map Requirements to MFT Scenarios](#step-1-map-requirements-to-mft-scenarios) - [Step 2: Identify User-Facing Inputs for INV Tests](#step-2-identify-user-facing-inputs-for-inv-tests) - [Step 3: Identify Parameters for DIR Tests](#step-3-identify-parameters-for-dir-tests) - [Step 4: Enumerate Boundary Values for All Parameters](#step-4-enumerate-boundary-values-for-all-parameters) - [Step 5: Verify Coverage Completeness](#step-5-verify-coverage-completeness) - [Step 6: Review and Refine](#step-6-review-and-refine) --- ## 1. MFT -- Minimum Functionality Tests ### 1.1 Definition For each decision branch or leaf node in the code/control flow, create a test that verifies the correct output for that path. MFTs ensure that every code path the developer intended to write actually produces the expected result. Think of MFTs as: **"If I designed a separate function for each branch, what would its test look like?"** ### 1.2 When to Use Every feature with multiple decision branches: - `if` / `else` / `elif` chains
- `switch` / `match` statements
- Pattern matching (destructuring, regex branching)
- Conditional logic (ternary operators, short-circuit evaluation)
- Polymorphic dispatch (strategy pattern, type-based dispatch)
- State machine transitions ### 1.3 How to Design 1. **Map all decision branches** in the code. Draw a decision tree or list every branch explicitly.
2. **For each branch**, identify the input conditions that trigger it.
3. **Create a test case** that satisfies those conditions -- ideally with the simplest possible input that reaches that branch.
4. **Assert the expected output** for that specific branch. The assertion should be precise, not vague. ### 1.4 Minimum Requirement **At least 1 MFT per decision branch.** If a function has 5 branches, it needs at least 5 MFTs. For functions with compound conditions (e.g., `if a > 0 and b < 10`), consider testing each sub-condition independently when possible. ### 1.5 Pseudocode Example ```
# Given a function with 3 branches:
# branch_a: input < 0 -> return "negative"
# branch_b: input == 0 -> return "zero"
# branch_c: input > 0 -> return "positive" # MFT for branch_a
test "negative input returns negative": input = -1 result = classify(input) assert result == "negative" # MFT for branch_b
test "zero input returns zero": input = 0 result = classify(input) assert result == "zero" # MFT for branch_c
test "positive input returns positive": input = 1 result = classify(input) assert result == "positive"
``` **Compound condition example:** ```
# Given:
# if age >= 18 and has_license -> "eligible"
# if age >= 18 and not has_license -> "needs_license"
# if age < 18 -> "too_young" test "adult with license is eligible": assert apply("eligible", age=25, has_license=true) test "adult without license needs license": assert apply("needs_license", age=20, has_license=false) test "minor is too young regardless of license": assert apply("too_young", age=16, has_license=true) assert apply("too_young", age=16, has_license=false)
``` --- ## 2. INV -- Invariance Tests ### 2.1 Definition Test that semantically equivalent but syntactically different inputs produce the same output. INV tests catch issues where the system is sensitive to input format rather than intent. Think of INV tests as: **"The user said the same thing three different ways -- did the system treat them the same?"** ### 2.2 When to Use Any feature that processes user input: - Text queries, search input, natural language commands
- API parameters with flexible formats
- User-facing configuration or settings
- Data import/parsing that accepts multiple formats
- Command-line argument parsing ### 2.3 How to Design 1. **Identify the core semantic intent** of an input (what does the user actually mean?).
2. **Create 2-3 syntactic variations** of the same intent.
3. **Verify all variations produce the same output** -- not just "no error," but identical meaningful output. ### 2.4 Common Variation Strategies | Strategy | Example |
|---|---|
| **Synonyms** | "delete" / "remove" / "erase" |
| **Word order** | "users who are active" / "active users" |
| **Abbreviations** | "January" / "Jan" / "01" |
| **Case variation** | "Search" / "search" / "SEARCH" |
| **Whitespace** | `"a b"` / `"a b"` / `"a\tb"` |
| **Number formats** | `"1000"` / `"1,000"` / `"1e3"` |
| **Date formats** | `"2024-01-15"` / `"Jan 15, 2024"` / `"15/01/2024"` |
| **Trailing punctuation** | `"hello"` / `"hello!"` / `"hello."` | ### 2.5 Pseudocode Example ```
# Given a search function that processes text queries: test "search by different phrasings returns same results": results_1 = search("show all active users") results_2 = search("display the active users") results_3 = search("list active accounts") assert results_1 == results_2 == results_3 assert len(results_1) > 0 # not just empty test "case insensitive search": results_lower = search("find order 123") results_upper = search("FIND ORDER 123") results_mixed = search("Find Order 123") assert results_lower == results_upper == results_mixed test "whitespace tolerance in input": result_normal = parse_command("create user alice") result_extra = parse_command("create user alice") assert result_normal == result_extra
``` --- ## 3. DIR -- Directional Expectation Tests ### 3.1 Definition Vary a single input dimension while holding all others constant, and verify the output changes in the expected direction. DIR tests monotonicity and proportional relationships. Think of DIR tests as: **"If I turn this dial up, does the needle move the right way?"** ### 3.2 When to Use Features with input parameters that affect output magnitude, ranking, filtering, or sorting: - Price calculations, totals, discounts
- Search result counts, filter narrowing
- Sorting order, ranking scores
- Pagination (more items per page vs fewer pages)
- Access control (higher privilege vs more access)
- Rate limiting (higher frequency vs more rejections) ### 3.3 How to Design 1. **Identify input dimensions** that should affect output directionally.
2. **Hold all other inputs constant** -- change only one variable at a time.
3. **Increase or decrease the target input** in a meaningful step.
4. **Verify output changes in the expected direction** -- greater, lesser, or equal (never the opposite). ### 3.4 Pseudocode Example ```
# Given a price calculation function: test "higher quantity increases total price": base = calculate_price(item="widget", quantity=1) more = calculate_price(item="widget", quantity=10) assert more > base test "discount reduces total price": without_discount = calculate_total(subtotal=100, discount=0) with_discount = calculate_total(subtotal=100, discount=20) assert with_discount < without_discount test "more filters return fewer or equal results": broad = search(query="laptop", category=None) narrow = search(query="laptop", category="gaming") assert len(narrow) <= len(broad) test "higher page offset returns different or empty results": page_1 = list_items(limit=10, offset=0) page_2 = list_items(limit=10, offset=10) # Page 2 should not overlap with page 1 assert not any(item in page_1 for item in page_2)
``` **Multi-direction example:** ```
# Given a scoring function where both relevance and recency matter: test "higher relevance score increases ranking": score_low = rank(relevance=0.1, recency=0.5) score_high = rank(relevance=0.9, recency=0.5) assert score_high > score_low test "higher recency increases ranking": score_old = rank(relevance=0.5, recency=0.1) score_new = rank(relevance=0.5, recency=0.9) assert score_new > score_old
``` --- ## 4. Boundary Value Analysis Boundary values are where bugs cluster. This section provides a systematic method for identifying and testing them. ### 4.1 Numeric Ranges For any parameter with a valid range `[min, max]`: | Test Point | Description |
|---|---|
| `min - 1` | Just below valid range (should fail or clamp) |
| `min` | Minimum valid value |
| `min + 1` | Just above minimum |
| `typical` | A common mid-range value |
| `max - 1` | Just below maximum |
| `max` | Maximum valid value |
| `max + 1` | Just above valid range (should fail or clamp) | **Example** -- quantity parameter, valid range `[1, 999]`: ```
test "boundary values for quantity": assert fails(calculate(quantity=0)) # min - 1 assert succeeds(calculate(quantity=1)) # min assert succeeds(calculate(quantity=2)) # min + 1 assert succeeds(calculate(quantity=500)) # typical assert succeeds(calculate(quantity=998)) # max - 1 assert succeeds(calculate(quantity=999)) # max assert fails(calculate(quantity=1000)) # max + 1
``` ### 4.2 String & Collection Lengths | Test Point | Description |
|---|---|
| `0` | Empty string, empty list, empty map |
| `1` | Single character / single element |
| `typical` | Normal working length |
| `max` | Maximum allowed length |
| `max + 1` | Exceeds maximum (should fail or truncate) | **Example** -- username, max 50 characters: ```
test "boundary values for username length": assert fails(create_user("")) # 0 -- empty assert succeeds(create_user("a")) # 1 -- single char assert succeeds(create_user("alice_smith")) # typical assert succeeds(create_user(repeat("x", 50))) # max assert fails(create_user(repeat("x", 51))) # max + 1
``` ### 4.3 Special Values Checklist Run through this checklist for every input parameter. Not all items apply to every parameter -- skip irrelevant ones. **Null / Absence:**
- `null` / `undefined` / `None`
- Missing parameter entirely (omitted from call)
- Empty string `""`
- Empty collection `[]` / `{}` / `Set(empty)` **Numeric edge cases:**
- Zero `0`
- Negative numbers `-1`, `-999`
- Very large numbers (`999999999`, `2^31`, `2^63`)
- Floating point: `0.1 + 0.2 != 0.3` precision issues
- Negative zero `-0.0` **String special characters:**
- Symbols: `!@#$%^&*(empty)_+-=[]{};':",.<>?/`
- Quotes: single `'`, double `"`, backtick ``(empty)` ``
- Backslash: `\`
- Newlines: `\n`, `\r\n`, `\r`
- Null byte: `\0` **Unicode:**
- Emojis: ``, ``, `` (multi-codepoint)
- CJK characters: ``, ``
- RTL text: use test strings with right-to-left text`
- Zero-width characters: `\u200B`, `\uFEFF`
- Combining characters: e + U+0301 (combining acute)e`
- Surrogate pairs **Whitespace:**
- Leading spaces: `" hello"`
- Trailing spaces: `"hello "`
- Multiple internal spaces: `"a b c"`
- Tabs: `"a\tb"`
- Mixed whitespace: `"a \t b \n c"` **Boolean edge cases:**
- Explicit `true` / `false`
- Truthy values: `1`, `"yes"`, non-empty string
- Falsy values: `0`, `""`, `null`, `undefined` ### 4.4 Data Feature Dimensions For each data parameter, identify which dimensions are relevant: | Dimension | Questions to Ask | Example Values |
|---|---|---|
| **Type** | What types are accepted? What happens with wrong types? | `string`, `number`, `boolean`, `array`, `object`, `date`, `enum` |
| **Range** | What are min/max/step constraints? | `[1, 100]`, step `0.01`, must be even |
| **Format** | Does it follow a specific format? | Email, URL, phone, UUID, ISO 8601 date, IPv4 |
| **Cardinality** | What are the relationship constraints? | One-to-one, one-to-many, many-to-many |
| **State** | What lifecycle states exist? | `active`/`inactive`, `pending`/`completed`, `draft`/`published` |
| **Temporal** | Are there time-based constraints? | Past, present, future; leap year (`2024-02-29`), month end, daylight saving boundary |
| **Uniqueness** | Must this value be unique? | Duplicate username, duplicate email, duplicate order ID |
| **Referential** | Does it reference another entity? | Foreign key that doesn't exist, deleted parent entity |
| **Ordering** | Does order matter? | Sorted vs unsorted input, duplicate items in sequence | --- ## 5. Applying the Taxonomy -- Workflow Follow these steps when designing tests for a new feature: ### Step 0: Map Business Flows Before analyzing code-level requirements, identify the end-to-end business flows that users actually perform. These are multi-step journeys traversed through external interfaces (HTTP, CLI, Browser) -- not internal function calls. - List all user-facing entry points (API endpoints, CLI commands, UI pages)
- Trace each critical user journey from entry to completion (e.g., "POST /auth/register -> click verification link -> POST /auth/login -> GET /profile")
- Identify state transitions and data that flows between steps
- Mark which flows are **critical** (core business value) vs **supporting** (nice-to-have) **Each critical business flow MUST have at least one E2E test verified through external calls.** This is tracked by the Business Flow Coverage metric (hard gate, MUST = 100%). ### Step 1: Map Requirements to MFT Scenarios - List all functional requirements.
- For each requirement, identify the decision branches it implies.
- Create at least one MFT per branch.
- **Check:** Does every `if`, `switch`, `match`, or conditional have a test? ### Step 2: Identify User-Facing Inputs for INV Tests - List all inputs that come from users (text, API params, config).
- For each input, define the core semantic intent.
- Create 2-3 syntactic variations per intent.
- **Check:** Do equivalent inputs produce identical outputs? ### Step 3: Identify Parameters for DIR Tests - List all parameters that affect output magnitude, count, or order.
- For each parameter, define the expected directional relationship.
- Create test pairs that vary one dimension at a time.
- **Check:** Does increasing input X always cause output Y to change in the expected direction? ### Step 4: Enumerate Boundary Values for All Parameters - For each parameter, run through the special values checklist (Section 4.3).
- Identify applicable data feature dimensions (Section 4.4).
- Create tests for numeric boundaries (Section 4.1) and length boundaries (Section 4.2).
- **Check:** Have you tested empty, typical, maximum, and beyond-maximum values? ### Step 5: Verify Coverage Completeness - **Each taxonomy category has >= 1 test:** MFT, INV, and DIR should all be represented.
- **>= 30% of tests target error/exception scenarios:** boundary violations, invalid input, missing data, permission failures.
- **No untested branches:** Cross-reference test list against code branches. ### Step 6: Review and Refine - Are test names descriptive enough to serve as documentation?
- Are assertions precise (not just "no error thrown")?
- Are tests independent (no implicit ordering dependency)?
- Do tests cover the most likely real-world failure modes? --- ## Quick Reference Card ```
MFT -- Every branch gets a test. Map decisions -> cover each path.
INV -- Same meaning, different wording. Vary syntax, keep semantics.
DIR -- Turn one dial, watch the needle. Vary one input, check direction.
BVA -- Bugs hide at edges. Test min, max, empty, overflow, special chars.
```

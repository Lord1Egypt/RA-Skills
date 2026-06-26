# Modernize Move — Detection Rules

Complete catalog of V1/outdated pattern detection rules organized by tier. Each rule includes what to search for, the
modern replacement, and confidence level.

---

## Tier 1 — Syntax (Safe — Identical Compiled Output)

These changes produce identical compiled output. Most apply unconditionally; T1-03 (receiver style) requires verifying
the target function's first parameter is named `self`.

### T1-01: Vector Borrow → Index Notation (Move 2.0+)

- **Confidence:** High
- **Search for:** `vector::borrow(&` or `vector::borrow(& `
- **Pattern:** `*vector::borrow(&v, i)` or `*vector::borrow(&container.field, i)`
- **Replace with:** `v[i]` or `container.field[i]`
- **Detection regex:** `vector::borrow\(&`

### T1-02: Vector Borrow Mut → Mutable Index (Move 2.0+)

- **Confidence:** High
- **Search for:** `vector::borrow_mut(&mut`
- **Pattern:** `*vector::borrow_mut(&mut v, i) = value`
- **Replace with:** `v[i] = value` or `*&mut v[i] = value`
- **Detection regex:** `vector::borrow_mut\(&mut`

### T1-03: Module Function Call → Receiver Style (Move 2.0+)

- **Confidence:** Medium — requires verifying the target function declares `self` as its first parameter
- **Search for:** `module::func(&obj, ...)` or `module::func(&mut obj, ...)`
- **Pattern:** `items::get_value(&item)` where `get_value` has `self: &Object<Item>`
- **Replace with:** `item.get_value()`
- **Safety check:** Read the target function definition. ONLY convert if first parameter is named `self`. If first
  parameter has any other name, do NOT convert.
- **Detection regex:** `\w+::\w+\(&(mut\s+)?\w+`

### T1-04: Add Assignment (Move 2.1+)

- **Confidence:** High
- **Search for:** `x = x + expr` where `x` is a simple variable or field access
- **Pattern:** `count = count + 1` or `total = total + amount`
- **Replace with:** `count += 1` or `total += amount`
- **Detection regex:** `([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s*=\s*\1\s*\+\s*`

### T1-05: Subtract Assignment (Move 2.1+)

- **Confidence:** High
- **Search for:** `x = x - expr`
- **Pattern:** `balance = balance - amount`
- **Replace with:** `balance -= amount`
- **Detection regex:** `(\w+)\s*=\s*\1\s*-\s*`

### T1-06: Multiply Assignment (Move 2.1+)

- **Confidence:** High
- **Search for:** `x = x * expr`
- **Pattern:** `value = value * multiplier`
- **Replace with:** `value *= multiplier`
- **Detection regex:** `(\w+)\s*=\s*\1\s*\*\s*`

### T1-07: Divide Assignment (Move 2.1+)

- **Confidence:** High
- **Search for:** `x = x / expr`
- **Pattern:** `value = value / divisor`
- **Replace with:** `value /= divisor`
- **Detection regex:** `(\w+)\s*=\s*\1\s*\/\s*`

### T1-08: Modulo Assignment (Move 2.1+)

- **Confidence:** High
- **Search for:** `x = x % expr`
- **Pattern:** `remainder = remainder % modulus`
- **Replace with:** `remainder %= modulus`
- **Detection regex:** `(\w+)\s*=\s*\1\s*%\s*`

### T1-09: While Loop with Counter → For Range Loop (Move 2.0+)

- **Confidence:** High
- **Search for:** `while` loop with a counter variable initialized before and incremented inside (`i = i + 1` or
  `i += 1`)
- **Pattern:**
  ```move
  let i = 0;
  while (i < n) {
      // body
      i = i + 1;
  };
  ```
- **Replace with:**
  ```move
  for (i in 0..n) {
      // body
  };
  ```
- **When to apply:** Convert `while` loops that use a counter with a known range to `for` loops. Keep `while` for loops
  where the iteration count isn't known upfront (e.g., dynamic termination conditions, searching until a match,
  processing until a queue is empty).
- **Detection regex:** `while\s*\(\w+\s*<\s*` combined with `\w+\s*=\s*\w+\s*\+\s*1` or `\w+\s*\+=\s*1` in the loop body
- **Note:** Also catches vector iteration patterns like `while (i < vector::length(&v))`. After conversion, combine with
  T1-01/T1-02 for index notation: `for (i in 0..vector::length(&v)) { ... v[i] ... }`

---

## Tier 2 — Visibility & Error Handling (Low Risk)

Same semantics, cleaner code. May require updating test annotations.

### T2-01: Public(friend) → Friend Fun (Move 2.0+)

- **Confidence:** High
- **Search for:** `public(friend) fun`
- **Replace with:** `friend fun`
- **Note:** Purely syntactic shorthand. `friend fun` is the shorter form of `public(friend) fun` — identical semantics.
- **Detection regex:** `public\(friend\)\s+fun`

### T2-02: Public(package) → Package Fun (Move 2.1+)

- **Confidence:** High
- **Search for:** `public(package) fun`
- **Replace with:** `package fun`
- **Note:** Purely syntactic shorthand — identical semantics, no safety check needed.
- **Detection regex:** `public\(package\)\s+fun`

### T2-03: Magic Abort Numbers → Named Constants

- **Confidence:** High
- **Search for:** `assert!(condition, <integer_literal>)` or `abort <integer_literal>`
- **Pattern:** `assert!(amount > 0, 1)` or `abort 42`
- **Replace with:** Define `const E_DESCRIPTIVE_NAME: u64 = <same_value>;` and use it
- **CRITICAL:** Preserve the exact numeric value. Tests using `#[expected_failure(abort_code = N)]` depend on the
  numeric value.
- **Detection regex:** `assert!\([^,]+,\s*\d+\)` or `abort\s+\d+`

---

## Tier 3 — API & Pattern Migrations (Breaking Changes)

Different APIs or architectural patterns. Apply ONE AT A TIME with test verification after each.

**Most Tier 3 rules are breaking changes** that alter the on-chain ABI, storage layout, or event stream format. The
skill workflow asks the user to choose `compatible` (skip breaking rules) or `fresh deploy` (allow breaking rules).
Rules marked **Breaking: No** are internal refactors safe for compatible upgrades.

### T3-01: Raw Address Params → Object<T> (Move 2.0+)

- **Breaking:** Yes — changes function ABI. All off-chain callers must update.
- **Confidence:** Medium
- **Search for:** Entry functions with `addr: address` parameters used to reference objects
- **Pattern:** `public entry fun transfer(item_addr: address, ...)`
- **Replace with:** `public entry fun transfer(item: Object<Item>, ...)`
- **Scope of change:** Function signature, callers, tests, and TypeScript integration all need updating.
- **Detection regex:** Entry functions with `address` params that call `borrow_global` with that address

### T3-02: Token V1 → Digital Assets (Major Rewrite)

- **Breaking:** Yes — complete API rewrite. Requires new deployment.
- **Confidence:** Low — requires complete restructuring
- **Search for:** `aptos_token::token`, `token::create_token_data_id`, `token::create_token_id`
- **Replace with:** `aptos_token_objects::token`, `aptos_token_objects::collection`
- **Scope of change:** Full module rewrite. Token creation, transfer, and query APIs are completely different. Recommend
  writing new module alongside old one.
- **Detection regex:** `aptos_token::token` or `token::create_token_data_id`

### T3-03: Coin Module → Fungible Asset (Major Rewrite)

- **Breaking:** Yes — complete API rewrite. Requires new deployment.
- **Confidence:** Low — requires complete restructuring
- **Search for:** `aptos_framework::coin`, `coin::transfer`, `coin::register`
- **Replace with:** `aptos_framework::fungible_asset`, `primary_fungible_store`
- **Scope of change:** Full module rewrite. Coin registration, transfer, and balance APIs are different. All `CoinType`
  generics become `Object<Metadata>`.
- **Detection regex:** `aptos_framework::coin` or `coin::register` or `coin::transfer`

### T3-04: Resource Accounts → Named Objects

- **Breaking:** Yes — architectural change. Requires new deployment.
- **Confidence:** Low — architectural change
- **Search for:** `create_resource_account`, `create_resource_address`, `SignerCapability`
- **Replace with:** Named objects via `object::create_named_object(creator, seed)`
- **Scope of change:** Changes how the contract manages its authority. Resource account signers become object signers.
- **Detection regex:** `create_resource_account` or `SignerCapability`

### T3-05: SmartTable → BigOrderedMap

- **Breaking:** Yes — different storage layout, incompatible with existing on-chain data.
- **Confidence:** Medium — API differences exist
- **Search for:** `aptos_std::smart_table`, `SmartTable<`
- **Replace with:** `aptos_std::big_ordered_map`, `BigOrderedMap<`
- **Scope of change:** API differences: `contains(&key)` vs `contains(key)`, `remove(&key)` vs `remove(key)`, different
  initialization.
- **Detection regex:** `SmartTable<` or `smart_table::`

### T3-06: State-Variant Structs → Enum Types (Move 2.0+)

- **Breaking:** Yes — different storage layout, incompatible with existing on-chain data.
- **Confidence:** Low — requires semantic understanding
- **Search for:** Multiple structs representing states of the same entity, or structs with `type` discriminator fields
- **Pattern:** `struct OrderPending`, `struct OrderFilled`, `struct OrderCancelled` or `struct Order { status: u8 }`
- **Replace with:** Single `enum Order { Pending { ... }, Filled { ... }, Cancelled { ... } }`
- **Scope of change:** All code that creates, reads, or pattern-matches on the entity needs rewriting.
- **Detection regex:** Manual analysis required — look for groups of structs with shared prefixes or `status`/`type`
  discriminator fields

### T3-07: Manual Loop Iteration → Stdlib Inline Functions + Lambdas

- **Breaking:** No — internal refactor only. Does not change ABI or storage layout.
- **Confidence:** Medium
- **Search for:** `for (i in 0..vector::length(` with index access inside, or any remaining while loops iterating over
  vectors
- **Replace with:** Stdlib inline functions with lambdas:
  - Read-only iteration: `vector::for_each_ref(&v, |elem| { ... })`
  - Mutable iteration: `vector::for_each_mut(&mut v, |elem| { ... })`
  - Consuming iteration: `vector::for_each(v, |elem| { ... })`
  - With index: `vector::enumerate_ref(&v, |i, elem| { ... })`
  - Transform: `vector::map(v, |elem| { ... })`
  - Reduce: `vector::fold(v, init, |acc, elem| { ... })`
  - Filter: `vector::filter(v, |elem| { ... })`
  - Check: `vector::any(&v, |elem| { ... })` / `vector::all(&v, |elem| { ... })`
- **Prerequisite:** Apply T1-09 (while → for) first. This rule converts for-loops over vectors into functional-style
  stdlib calls.
- **Scope of change:** Restructures loop body into lambda. Loops with `break`/`continue` cannot be converted — keep as
  `for` loops.
- **Detection regex:** `for\s*\(\w+\s+in\s+0\.\.vector::length` or remaining `while\s*\(\w+\s*<\s*(vector::length|len)`

### T3-08: Custom Signed Int Workarounds → Native Types (Move 2.3+)

- **Breaking:** Yes — different storage representation, incompatible with existing on-chain data.
- **Confidence:** Medium
- **Search for:** Custom modules implementing signed integer arithmetic, or patterns like
  `struct I64 { value: u64, negative: bool }`
- **Replace with:** Native `i8`, `i16`, `i32`, `i64`, `i128`, `i256` types
- **Scope of change:** Remove custom module, update all usages to native types.
- **Detection regex:** `struct I64` or `struct I128` or `negative: bool` with arithmetic helpers

### T3-09: EventHandle → #[event] Struct (Move 2.0+)

- **Breaking:** Yes — changes event stream format. Indexers must be updated.
- **Confidence:** Medium — requires updating three locations
- **Search for:** `EventHandle<` or `emit_event(`
- **Pattern:**
  ```move
  // OLD
  struct MyEventHandle has key {
      events: EventHandle<MyEvent>,
  }
  event::emit_event(&mut handle.events, MyEvent { ... });
  ```
- **Replace with:**
  ```move
  // NEW
  #[event]
  struct MyEvent has drop, store { ... }
  event::emit(MyEvent { ... });
  ```
- **Safety check:** External indexers may depend on the old event format. Note this in the analysis report.
- **Detection regex:** `EventHandle<` or `emit_event\(`

### T3-10: EventHandle Struct Fields → Remove (Move 2.0+)

- **Breaking:** Yes — coupled with T3-09. Changes event stream format.
- **Confidence:** Medium — coupled with T3-09
- **Search for:** Struct fields of type `EventHandle<T>`
- **Replace with:** Remove the field entirely after converting to `#[event]` pattern
- **Safety check:** Must complete T3-09 first. Also remove initialization in `init_module`.
- **Detection regex:** `\w+:\s*EventHandle<`

---

## Detection Strategy

When analyzing a contract, scan in this order:

1. **Grep for Tier 1 patterns** — highest confidence, most common
2. **Grep for Tier 2 patterns** — second pass, check for friend/event patterns
3. **Grep for Tier 3 patterns** — final pass, flag for manual review
4. **Cross-reference findings** — some patterns are coupled (T2-01 → T2-02 applied in sequence, T3-09 + T3-10)
5. **Build analysis report** — line numbers, rule ID, proposed change, confidence

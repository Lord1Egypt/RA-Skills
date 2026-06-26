# Modernize Move — Transformation Guide

Step-by-step transformation instructions with before/after code, safety checks, and edge cases. Covers Tier 1 and Tier 2
in full detail. Tier 3 rules T3-02, T3-04, and T3-06 are flagged as "manual rewrite" in detection rules and do not have
step-by-step guidance here — refer to the dedicated pattern docs (DIGITAL_ASSETS.md, OBJECTS.md, ADVANCED_TYPES.md).

---

## Tier 1 Transformations — Syntax

### T1-01: Vector Borrow → Index Notation

**Before:**

```move
let item = *vector::borrow(&items, i);
let name = *vector::borrow(&registry.names, index);
let nested = *vector::borrow(&borrow_global<State>(addr).items, i);
```

**After:**

```move
let item = items[i];
let name = registry.names[index];
let nested = borrow_global<State>(addr).items[i];
```

**Steps:**

1. Find all `vector::borrow(&` calls
2. Replace `*vector::borrow(&v, i)` with `v[i]`
3. For nested access like `*vector::borrow(&container.field, i)`, use `container.field[i]`
4. Remove the leading `*` dereference — `v[i]` auto-dereferences in value context (produces a copy for `copy` types).
   Use `&v[i]` when an explicit reference is needed.

**Edge cases:**

- When the result is used as a reference (`vector::borrow(&v, i)` without `*`), replace with `&v[i]`
- When inside `borrow_global`, the index notation chains directly: `borrow_global<R>(addr).items[i]`
- `vector::borrow` on a local variable: `*vector::borrow(&v, i)` → `v[i]`

### T1-02: Vector Borrow Mut → Mutable Index

**Before:**

```move
*vector::borrow_mut(&mut items, i) = new_value;
let elem = vector::borrow_mut(&mut items, i);
*elem = new_value;
```

**After:**

```move
items[i] = new_value;
let elem = &mut items[i];
*elem = new_value;
```

**Steps:**

1. Find all `vector::borrow_mut(&mut` calls
2. For direct assignment: `*vector::borrow_mut(&mut v, i) = val` → `v[i] = val`
3. For mutable reference binding: `vector::borrow_mut(&mut v, i)` → `&mut v[i]`

Both forms are valid — `v[i] = value` for direct assignment, `&mut v[i]` for mutable reference binding.

**Edge cases:**

- When mutating a struct field within the vector element, keep the mutable reference pattern:
  `let elem = &mut v[i]; elem.field = val`
- For `borrow_global_mut` chains: `*vector::borrow_mut(&mut borrow_global_mut<S>(addr).items, i)` →
  `borrow_global_mut<S>(addr).items[i]`

### T1-03: Module Function Call → Receiver Style

**Before:**

```move
let value = items::get_value(&item);
assert!(items::is_owner(&item, user), E_NOT_OWNER);
items::set_value(&item, new_value);
```

**After:**

```move
let value = item.get_value();
assert!(item.is_owner(user), E_NOT_OWNER);
item.set_value(new_value);
```

**Steps:**

1. Identify candidate calls: `module::func(&obj, ...)`
2. **CRITICAL:** Read the target function definition and verify the first parameter is named `self`
3. If first param is `self: &T` or `self: &mut T` or `self: T`, convert to receiver style
4. Remove the first argument from the call (it becomes the receiver)
5. Drop the module prefix — the compiler discovers receiver functions automatically

**Safety checks:**

- If first parameter is NOT named `self`, do NOT convert — it will not compile
- Verify the function is `public` — private functions cannot be called receiver-style from other modules
- Check for name conflicts — if two imported modules define the same receiver function name for the same type, the call
  is ambiguous

**Edge cases:**

- `&obj` vs `&mut obj` — both work with receiver style, the compiler infers mutability from the function signature
- Functions with generics: `module::func<T>(&obj, ...)` → `obj.func<T>(...)` — generic params stay

### T1-04 through T1-08: Compound Assignments

**Before:**

```move
count = count + 1;
balance = balance - amount;
value = value * multiplier;
result = result / divisor;
remainder = remainder % modulus;
```

**After:**

```move
count += 1;
balance -= amount;
value *= multiplier;
result /= divisor;
remainder %= modulus;
```

**Steps:**

1. Find patterns matching `x = x <op> expr`
2. Verify both sides reference the exact same variable name
3. Replace with `x <op>= expr`

**Edge cases:**

- `self.field = self.field + 1` → `self.field += 1` — works for struct field access
- `*ref = *ref + 1` → `*ref += 1` — works for dereferenced mutable references
- `x = expr + x` — do NOT convert. The variable must be on the left side of the operator. `x = 1 + x` is NOT the same
  pattern (addition is commutative but the syntax transform is not general).
- Multi-term expressions: `x = x + a + b` → `x += a + b` — safe because `+` is left-associative

### T1-09: While Loop with Counter → For Range Loop

**Convert counter-based `while` loops to `for` loops.** This is the single most impactful Tier 1 modernization — it
eliminates counter boilerplate and makes loop intent immediately clear. Use the same rule as in other languages: `for`
when the iteration range is known upfront, `while` when termination depends on a dynamic condition.

**Before:**

```move
let i = 0;
let len = vector::length(&items);
while (i < len) {
    let item = items[i];
    process(item);
    i = i + 1;
};
```

**After:**

```move
for (i in 0..vector::length(&items)) {
    let item = items[i];
    process(item);
};
```

**Steps:**

1. Find all while loops with a counter variable pattern: `let i = 0; ... while (i < bound) { ... i = i + 1; }`
2. Replace with `for (i in 0..bound) { ... }`
3. Remove the counter initialization (`let i = 0;`) — the `for` loop declares it
4. Remove the counter increment (`i = i + 1;` or `i += 1;`) — the `for` loop handles it
5. If the bound was stored in a variable only for the while condition (`let len = ...`), inline it into the `for` range
   if it's a simple expression

**Range syntax:**

- `for (i in 0..n)` — iterates `i` from `0` to `n-1` (upper bound is exclusive)
- `for (i in start..end)` — iterates from `start` to `end-1`
- Bounds are evaluated **once** at loop entry

**Edge cases:**

- Non-zero start: `let i = offset; while (i < limit) { ... i += 1; }` → `for (i in offset..limit) { ... }`
- Counter used after loop: if `i` is read after the while loop exits, you need to keep a separate variable since the
  for-loop variable is scoped to the loop body
- Loops with `break`: `for` loops support `break` and `continue`, so these convert directly
- Nested loops: convert each independently, inner loop first
- Counter step != 1: `i = i + 2` — cannot use `for` range loop (keep as `while`)
- Dynamic termination: loops that exit based on a runtime condition (e.g., searching for a value, draining a queue) are
  naturally `while` loops — do not force these into `for`

---

## Tier 2 Transformations — Visibility & Error Handling

### T2-01: Public(friend) → Friend Fun

**Before:**

```move
public(friend) fun internal_transfer(from: address, to: address, amount: u64) {
    // ...
}
```

**After:**

```move
friend fun internal_transfer(from: address, to: address, amount: u64) {
    // ...
}
```

**Steps:**

1. Replace all `public(friend) fun` with `friend fun`

Purely syntactic — identical semantics, no safety check needed.

### T2-02: Public(package) → Package Fun

**Before:**

```move
public(package) fun other_helper(): u64 {
    // ...
}
```

**After:**

```move
package fun other_helper(): u64 {
    // ...
}
```

**Steps:**

1. Replace all `public(package) fun` with `package fun`

Purely syntactic — identical semantics, no safety check needed.

### T2-03: Magic Abort Numbers → Named Constants

**Before:**

```move
public fun transfer(from: &signer, to: address, amount: u64) {
    assert!(amount > 0, 1);
    assert!(signer::address_of(from) != to, 2);
    let balance = get_balance(signer::address_of(from));
    assert!(balance >= amount, 3);
    // ...
}
```

**After:**

```move
const E_ZERO_AMOUNT: u64 = 1;
const E_SELF_TRANSFER: u64 = 2;
const E_INSUFFICIENT_BALANCE: u64 = 3;

public fun transfer(from: &signer, to: address, amount: u64) {
    assert!(amount > 0, E_ZERO_AMOUNT);
    assert!(signer::address_of(from) != to, E_SELF_TRANSFER);
    let balance = get_balance(signer::address_of(from));
    assert!(balance >= amount, E_INSUFFICIENT_BALANCE);
    // ...
}
```

**Steps:**

1. Find all `assert!(..., <literal>)` and `abort <literal>` occurrences
2. Group by numeric value — same number should get the same constant
3. Create `const E_DESCRIPTIVE_NAME: u64 = <original_value>;` for each unique number
4. Replace literal numbers with constant names in `assert!` and `abort` calls
5. **CRITICAL:** The numeric value MUST stay the same. Only the name changes.

**Test impact:**

- Tests using `#[expected_failure(abort_code = 1)]` still work (numeric value unchanged)
- Optionally update tests to use `#[expected_failure(abort_code = module_name::E_ZERO_AMOUNT)]` for readability — but
  this is cosmetic, not required

**Edge cases:**

- Constants like `0` used as abort codes — name them `E_GENERIC_ERROR` or investigate the context
- If a constant with the same value already exists, reuse it rather than creating a duplicate
- `abort` expressions in nested contexts: `if (cond) { abort 5 }` → `if (cond) { abort E_SOME_ERROR }`

---

## Tier 3 Transformations — API & Pattern Migrations

**Apply ONE AT A TIME. Run tests after each. Revert on failure.**

Most Tier 3 rules are **breaking changes** — they alter the on-chain ABI, storage layout, or event stream format. When
the user selects `compatible` deployment mode, skip rules marked with a breaking-change warning.

### T3-01: Raw Address Params → Object<T>

**⚠ Breaking change** — changes function ABI. All off-chain callers must update.

**Before:**

```move
public entry fun transfer_item(
    owner: &signer,
    item_addr: address,
    recipient: address
) acquires Item {
    let item = borrow_global<Item>(item_addr);
    assert!(item.owner == signer::address_of(owner), E_NOT_OWNER);
    // ...
}
```

**After:**

```move
public entry fun transfer_item(
    owner: &signer,
    item: Object<Item>,
    recipient: address
) acquires Item {
    assert!(object::owner(item) == signer::address_of(owner), E_NOT_OWNER);
    let item_data = borrow_global<Item>(object::object_address(&item));
    // ...
}
```

**Steps:**

1. Change parameter type from `address` to `Object<T>`
2. Replace `borrow_global<T>(addr)` with `borrow_global<T>(object::object_address(&obj))`
3. Update ownership checks to use `object::owner(obj)`
4. Update all callers and tests

**Safety checks:**

- This changes the function's ABI — all off-chain callers (TypeScript, CLI) must update
- The `address` parameter might be used for non-object purposes (user address, not object address). Only convert
  addresses that reference objects.

### T3-03: Coin Module → Fungible Asset

This is a major rewrite. Key API differences:

| Coin API                                     | Fungible Asset API                                             |
| -------------------------------------------- | -------------------------------------------------------------- |
| `coin::register<CoinType>(account)`          | Automatic via `primary_fungible_store`                         |
| `coin::transfer<CoinType>(from, to, amount)` | `primary_fungible_store::transfer(from, metadata, to, amount)` |
| `coin::balance<CoinType>(addr)`              | `primary_fungible_store::balance(addr, metadata)`              |
| `coin::withdraw<CoinType>(from, amount)`     | `fungible_asset::withdraw(from, store, amount)`                |
| `CoinType` generic parameter                 | `Object<Metadata>` parameter                                   |

**Approach:** Write the new module alongside the old one, migrate incrementally, then remove the old module.

### T3-05: SmartTable → BigOrderedMap

**⚠ Breaking change** — different storage layout, incompatible with existing on-chain data.

Replace `SmartTable<K, V>` with `BigOrderedMap<K, V>`. Replace `smart_table::` prefix with `big_ordered_map::`.

**Key API differences:**

- `contains(&table, &key)` → `contains(&map, key)` (no reference on key)
- `remove(&mut table, &key)` → `remove(&mut map, key)` (no reference on key)
- `borrow(&table, &key)` → `borrow(&map, key)` (no reference on key)
- `borrow_mut(&mut table, &key)` → `borrow_mut(&mut map, key)` (no reference on key)
- Initialization: `smart_table::new()` → `big_ordered_map::new()`

### T3-07: Manual Loop Iteration → Stdlib Inline Functions + Lambdas

**Prerequisite:** Apply T1-09 first so all while loops are already converted to `for` loops. This rule then converts
`for`-loop-over-vector patterns into functional-style stdlib calls.

**Before (after T1-09 has been applied):**

```move
fun sum_amounts(items: &vector<Item>): u64 {
    let total = 0;
    for (i in 0..items.length()) {
        total += items[i].amount;
    };
    total
}
```

**After:**

```move
fun sum_amounts(items: &vector<Item>): u64 {
    items.fold(0, |acc, item| acc + item.amount)
}
```

**Stdlib inline functions to use (do NOT define custom helpers when stdlib equivalents exist):**

| Pattern              | Module-qualified          | Receiver style                     | Signature                              |
| -------------------- | ------------------------- | ---------------------------------- | -------------------------------------- |
| Read each element    | `vector::for_each_ref`    | `v.for_each_ref(\|&T\|)`           | `(&vector<T>, \|&T\|)`                 |
| Mutate each element  | `vector::for_each_mut`    | `v.for_each_mut(\|&mut T\|)`       | `(&mut vector<T>, \|&mut T\|)`         |
| Consume each element | `vector::for_each`        | `v.for_each(\|T\|)`                | `(vector<T>, \|T\|)`                   |
| Read with index      | `vector::enumerate_ref`   | `v.enumerate_ref(\|u64, &T\|)`     | `(&vector<T>, \|u64, &T\|)`            |
| Mutate with index    | `vector::enumerate_mut`   | `v.enumerate_mut(\|u64, &mut T\|)` | `(&mut vector<T>, \|u64, &mut T\|)`    |
| Transform elements   | `vector::map` / `map_ref` | `v.map(\|T\|U)`                    | `(vector<T>, \|T\|U): vector<U>`       |
| Reduce to value      | `vector::fold`            | `v.fold(init, \|Acc, T\|Acc)`      | `(vector<T>, Acc, \|Acc, T\|Acc): Acc` |
| Filter elements      | `vector::filter`          | `v.filter(\|&T\|bool)`             | `(vector<T>, \|&T\|bool): vector<T>`   |
| Any match            | `vector::any`             | `v.any(\|&T\|bool)`                | `(&vector<T>, \|&T\|bool): bool`       |
| All match            | `vector::all`             | `v.all(\|&T\|bool)`                | `(&vector<T>, \|&T\|bool): bool`       |
| Zip two vectors      | `vector::zip` / `zip_ref` | `a.zip(b, \|T, U\|)`               | `(vector<T>, vector<U>, \|T, U\|)`     |

**Steps:**

1. Identify `for` loops that iterate over a vector using index access
2. Determine which stdlib function fits the loop pattern (see table above)
3. Replace the loop with the stdlib call + lambda
4. Combine with T1-04/T1-08 (compound assignments) inside lambdas for cleaner result

**Edge cases:**

- Loops with `break` or `continue` cannot be converted — lambdas don't support these. Keep as `for` loops.
- Loops that need both index and element: use `enumerate_ref` or `enumerate_mut`
- Loops with early returns: extract the return value as a mutable variable, or use `vector::any`/`vector::all` if the
  return is boolean
- Loops that build a new collection: use `vector::map` or `vector::filter`
- Only define custom inline helpers when no stdlib function fits the pattern

### T3-08: Custom Signed Int → Native Types

**⚠ Breaking change** — different storage representation, incompatible with existing on-chain data.

Replace custom `struct I64 { value: u64, negative: bool }` with native `i64`. Replace custom arithmetic functions
(`add_i64`, `sub_i64`, etc.) with native operators (`+`, `-`, `*`, `/`). Remove the custom module and update all
callers.

### T3-09 + T3-10: EventHandle → #[event] Struct

**⚠ Breaking change** — changes event stream format. Indexers must be updated.

**Key changes:**

- `event::emit_event(&mut handle.events, MyEvent { ... })` → `event::emit(MyEvent { ... })`
- Add `#[event]` attribute above event struct definitions
- Remove `EventHandle<T>` fields from storage structs
- Remove `account::new_event_handle<T>(signer)` calls from `init_module`
- Update imports: remove `EventHandle`, remove `account` if only used for handles
- If storage struct ONLY contained event handles, remove the entire struct + its `acquires`

**Steps:**

1. Add `#[event]` attribute above each event struct
2. Replace all `emit_event` calls with `event::emit()`
3. Remove `EventHandle<T>` fields and their initialization
4. Clean up imports, `acquires`, and `borrow_global_mut` for removed structs

**Safety checks:**

- External indexers may depend on EventHandle-based event stream. The `#[event]` pattern uses a different stream. Note
  in analysis report.
- If already deployed and indexed, coordinate with indexer updates.

---

## General Safety Protocol

Before applying ANY tier of transformations:

1. **Verify test baseline** — all tests must pass before changes
2. **Apply changes for one tier** — do not mix tiers
3. **Run `aptos move test`** — verify all tests still pass
4. **If tests fail:**
   - Identify which specific change caused the failure
   - Revert that change
   - Investigate whether the transformation was applied incorrectly
   - Fix and retry, or skip that specific rule
5. **Proceed to next tier** only after current tier passes

After all transformations:

6. **Run `aptos move test --coverage`** — verify coverage is maintained
7. **Generate summary report** — what changed, what was skipped, and why

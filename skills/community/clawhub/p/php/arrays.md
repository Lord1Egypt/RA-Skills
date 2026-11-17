# Arrays — Keys, Order, and the Functions That Reshape Them

A PHP array is an ordered hash map. Every trap below comes from forgetting one of those three words.

## Key Coercion

Keys are only ever `int` or `string`; everything else converts on the way in:

| Written | Stored |
|---|---|
| `"1"` | int `1` |
| `"01"`, `"1.5"`, `" 1"` | unchanged strings (not canonical integers) |
| `1.7` | int `1`, truncated (deprecated on `php >=8.1`) |
| `true` / `false` | int `1` / `0` |
| `null` | `""` |

- Consequence: `$a["1"]` and `$a[1]` are the same slot, and `array_flip` on the values `["1", 1]` collapses them into one.
- `$a[-5] = 'x'` stores the literal key `-5`. What the next `$a[] =` picks differs by version: `php >=8.3` continues at `-4`, earlier versions restart at `0`.
- After a large index, append continues from `max_int_key + 1`: `$a[1000]='x'; $a[]='y';` puts `y` at `1001` while `count($a)` is 2.

## list vs Map

- A "list" is keys `0..n-1` in order. `array_is_list($a)` (`php >=8.1`) is the check; before that, `$a === array_values($a)`.
- `json_encode` emits `[...]` only for a list; any gap or string key emits `{...}`. This is the most common PHP↔frontend bug: `array_filter` preserves keys, so filtering `[0=>'a',1=>'b']` down to `[1=>'b']` encodes as `{"1":"b"}` and the client's `.map()` throws. Fix with `array_values()` immediately after the filter (`json.md`).
- `array_map` with ONE array preserves keys; with two or more it reindexes. `array_map(null, $a, $b)` zips into pairs.
- `array_filter` with no callback drops every falsy value, including `0`, `"0"`, `""`, and `[]`. Pass an explicit callback (`fn($v) => $v !== null`) unless you truly mean falsy.
- `ARRAY_FILTER_USE_KEY` / `ARRAY_FILTER_USE_BOTH` as the third argument make `array_filter` key-aware; without them the callback never sees a key.

## Merging and Combining

- `array_merge($a, $b)`: integer keys are RENUMBERED from 0; string keys from `$b` overwrite `$a`.
- `$a + $b`: keys present in `$a` win, nothing is renumbered. The union operator is the defaults idiom: `$options = $user + $defaults;`.
- `array_merge_recursive` turns colliding scalar string keys into arrays; `array_replace_recursive` overwrites them. Config merging almost always wants `array_replace_recursive`.
- `array_combine($keys, $values)` throws `ValueError` on `php >=8.0` when the counts differ; it used to warn and return `false`.
- Spread `[...$a, ...$b]` renumbers integer keys like `array_merge`; string keys in a spread need `php >=8.1`.

## Sorting

| Need | Function | Keys |
|---|---|---|
| Values, keys discarded | `sort` / `rsort` / `usort` | Reindexed 0..n-1 |
| Values, keys kept | `asort` / `arsort` / `uasort` | Preserved |
| By key | `ksort` / `krsort` / `uksort` | Preserved |
| Human order (`img2` before `img10`) | `natsort`, or the `SORT_NATURAL` flag | Preserved |
| Several columns | `array_multisort`, or `usort` with chained `<=>` | Reindexed |

- Sorting is stable on `php >=8.0`: equal elements keep their input order. Code that leaned on the old instability for pseudo-randomness now returns the same order forever.
- The `usort` callback must return an int. `fn($a, $b) => $a->x > $b->x` returns a bool — deprecated on `php >=8.0`, and it collapses "less than" and "equal" into the same answer. Use `$a->x <=> $b->x`.
- `usort` takes `array &$array`, so `usort($obj->getItems(), ...)` sorts a temporary and silently does nothing.

## References and Copies

- Arrays are value types with copy-on-write. Passing a 50 MB array to a function costs nothing until either side writes — then the array is duplicated and peak memory doubles.
- The `foreach` reference trap, precisely: after `foreach ($a as &$v) {}`, `$v` still points at the last element. A following `foreach ($a as $v) {}` writes into that last element on every iteration, so the array ends with its last value replaced by the second-to-last. Always `unset($v);` right after a reference loop.
- `foreach` by value iterates a snapshot, so appending inside the loop does not extend it. By reference it iterates live, and appending inside can loop forever.
- `$row = $obj->items; $row['a'] = 1;` modifies a copy — arrays are values. The same line with an object property modifies the original, because objects are handles (`oop.md`).

## Lookup Cost

- `isset($a[$k])` and `array_key_exists($k, $a)` are O(1); `in_array` and `array_search` are O(n).
- Flipping a list into a lookup set once (`array_flip`, `array_fill_keys`) turns an O(n²) nested loop into O(n). This is the highest-yield array optimization in real PHP code.
- `array_unique` compares as strings by default (`SORT_STRING`) — pass `SORT_REGULAR` for mixed types. For scalars, `array_keys(array_flip($a))` is faster and keeps first occurrences.
- Memory ballpark: a packed array of one million integers costs on the order of 30-35 MB; `SplFixedArray` roughly halves it; a generator holds one element. Measure with `memory_get_peak_usage(true)` before optimizing (`performance.md`).

## Destructuring and Extraction

- `[$a, $b] = $pair;` and `['id' => $id, 'name' => $name] = $row;` — keyed destructuring avoids positional fragility.
- Nested with skips: `[, [$x]] = $data;`.
- Destructuring a missing key warns and assigns `null`; there is no `??` inside the pattern, so validate the shape first.
- `extract($_POST)` creates variables from user-controlled keys and will overwrite `$isAdmin`. No configuration of this function is safe for untrusted input (`security.md`).
- `compact('a', 'b')` warns on undefined names on `php >=7.3` — the missing template variable that used to render as blank.

## Functions Worth Knowing

- `array_column($rows, 'name', 'id')` — reindex a result set by primary key in one call; pass `null` as the second argument to keep whole rows.
- `array_fill_keys($ids, $default)` — build the complete map up front so no key is missing later.
- `array_chunk($a, 500, true)` — batch inserts and API pages; `true` preserves keys.
- `array_slice($a, $o, $l, true)` — the fourth argument preserves keys; without it a paged slice renumbers and breaks the client.
- `array_splice` mutates and returns the removed part; `array_slice` does not mutate. One letter apart, opposite behavior.
- `array_find`, `array_any`, `array_all` (`php >=8.4`) replace the `foreach`-with-a-flag idiom.
- `array_walk` mutates through a reference parameter and cannot change keys; `array_map` cannot see keys. When you need both, a plain `foreach` is clearer than either.
- `SplObjectStorage` when the keys must be objects; `SplQueue`/`SplStack` when `array_shift` in a loop is the bottleneck (it is O(n) because it reindexes).

## Related

- Comparison semantics every array function inherits: `types.md`
- Encoding arrays for an API: `json.md`
- Streaming instead of building giant arrays: `performance.md`, `files.md`

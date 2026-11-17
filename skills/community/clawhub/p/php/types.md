# Types, Comparison, and Numbers

PHP has two type systems: declared types checked at call time, and juggling rules applied everywhere else. Everything below is what happens when the second one runs where you expected the first.

## strict_types Is Not What Most People Think

- `declare(strict_types=1);` must be the FIRST statement in the file (only the `<?php` tag and comments may precede it) or PHP fatals.
- It governs the file where the CALL is written, not where the function is declared. A legacy untyped file calling your `f(int $n)` still coerces `"7"` to `7`. Return values are the mirror image: checked against the mode of the file that DECLARES the function.
- Consequence for library authors: your strict file cannot force strictness on consumers. Validate at the boundary instead of trusting the signature.
- Internal functions follow the same switch: `strlen(5)` is a `TypeError` under strict mode and `1` under coercive mode.
- Coercive mode still refuses conversions it once allowed silently: passing `7.9` to an `int` parameter is deprecated on `php >=8.1` because the fraction is discarded.

## Comparison

| Expression | Result | Why |
|---|---|---|
| `0 == "foo"` | `false` on `php >=8.0` (`true` before) | A non-numeric string is now compared as a string, not as 0 |
| `"1" == "01"` | `true` | Both numeric strings → compared as numbers |
| `"10" == "1e1"` | `true` | Scientific notation is numeric |
| `"0e12" == "0e34"` | `true` | Both equal 0 — the magic-hash auth bypass |
| `null == false`, `null == 0`, `null == ""` | `true` | Null is loosely equal to every empty-ish value |
| `[] == false` | `true` | Empty array is falsy |
| `NAN == NAN` | `false` | Use `is_nan()` |
| `"abc" <=> "abd"` | `-1` | Spaceship returns -1/0/1 — the sort-callback contract |

- `===` on arrays also requires the same key ORDER; `==` does not. `['a'=>1,'b'=>2] == ['b'=>2,'a'=>1]` is true, `===` is false.
- Objects: `==` compares class plus property values recursively and can recurse forever on a cyclic graph; `===` is identity.
- `switch` compares loosely, so `switch ("1abc")` can reach `case 1`. `match` (`php >=8.0`) compares with `===` and throws `UnhandledMatchError` when nothing matches — the behavior you wanted.
- `in_array` and `array_search` default to loose. `in_array(0, ['a','b'])` was true before PHP 8 and is false now, but `in_array("1", [1])` is still true. Pass `true` as the third argument, always.
- Sorting a mixed array applies the same juggling: `sort([10, "9 apples", true])` produces an order nobody can defend. Sort typed lists only.

## Numeric Strings

- `is_numeric()` accepts leading whitespace, and trailing whitespace too on `php >=8.0`. It accepts `"1e3"` and `".5"`; it rejects `"0x1A"`.
- `(int)"12abc"` is `12` with no diagnostic. Arithmetic on a leading-numeric string warns and uses the leading part; arithmetic on a wholly non-numeric string is an error condition that should never reach production. Validate with `is_numeric()` or `filter_var($v, FILTER_VALIDATE_INT)` at the boundary, then cast once.
- `filter_var($v, FILTER_VALIDATE_INT)` returns `false` for invalid input, and `0` is a legitimate result — another `!== false` site (SKILL.md rule 3).
- `intdiv(7, 2)` is `3`; `7 / 2` is the float `3.5`; `%` casts both operands to int (`7.5 % 2` is `1`) while `fmod(7.5, 2)` is `1.5`.
- Integers do not wrap on overflow: `PHP_INT_MAX + 1` silently becomes a float and loses integer precision. Check with `is_int()` after arithmetic on large values, or move to `bcmath`/`gmp`.

## Floats and Money

- `0.1 + 0.2 === 0.3` is `false`; `round(0.1 + 0.2, 2) === 0.3` is `true`. For tolerance comparisons use `abs($a - $b) < $epsilon` with an epsilon chosen for the domain, not `PHP_FLOAT_EPSILON` copied from an example.
- Money: compute in integer minor units (cents) or in `bcmath` strings. Never accumulate a total as a float and round once at the end — the error compounds per addition, and the report disagrees with accounting by a cent.
- `round()` is half-up away from zero; banker's rounding needs `PHP_ROUND_HALF_EVEN` as the third argument.
- Printing a float uses the `precision` ini (14) while `var_export`, `json_encode`, and `serialize` use `serialize_precision` (`-1` = shortest round-trip). That is why a value prints as `0.3` and encodes as `0.29999999999999999` on a misconfigured host (`php-ini.md`).

## Null and Absence

Four different questions, four functions:

| Question | Use | Note |
|---|---|---|
| Is the key set to a non-null value? | `isset($a['k'])` | `false` for a key holding `null` |
| Does the key exist at all? | `array_key_exists('k', $a)` | `true` even when the value is `null` |
| Is it empty-ish? | `empty($a['k'])` | `true` for `0`, `"0"`, `""`, `[]`, `false`, `null` |
| Value or fallback? | `$a['k'] ?? $default` | Suppresses the undefined-key warning that `?:` emits |

- `??=` assigns only when the left side is null or unset — the idiomatic memoization line.
- `?->` short-circuits the entire chain to its right: in `$a?->b()->c()`, a null `$a` skips both calls and the arguments inside them. It does not extend past the chain — `$a?->b + 1` still evaluates `null + 1`.
- `?int` and `int|null` are the same type. `function f(Foo $x = null)` implicitly meant `?Foo` and is deprecated on `php >=8.4`; write `?Foo $x = null`.

## Casting Reference

| Cast | Surprise |
|---|---|
| `(int)` on a float | Truncates toward zero (`(int)-1.9` is `-1`), never rounds |
| `(int)` on a string | Reads a leading integer, `0` when there is none, no error |
| `(bool)` | `"0"` is `false`, but `"0.0"` and `"false"` are `true` |
| `(array)` on an object | Private keys gain a `\0Class\0` prefix, protected a `\0*\0` prefix — the invisible-key bug |
| `(string)` on an object | Requires `__toString()` or throws `Error` |
| `(float)` on a localized string | `"1,5"` becomes `1.0`; parse locale-formatted numbers with `NumberFormatter` (`ext-intl`) |

## Related

- Array key coercion and comparison of arrays: `arrays.md`
- Enums as the type-safe replacement for string constants: `modern.md`
- Making an analyzer enforce all of this: `static-analysis.md`

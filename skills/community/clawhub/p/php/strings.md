# Strings, Encoding, and PCRE

Two independent problem families live here: PHP string functions operate on BYTES, and PCRE has limits that fail silently. Both produce "it works until someone types an accent".

## Bytes vs Characters

- Byte-based, will split a UTF-8 sequence: `strlen`, `substr`, `strpos`, `str_pad`, `strrev`, `wordwrap`, `ucfirst`, `str_split`.
- Character-aware equivalents (need `ext-mbstring`): `mb_strlen`, `mb_substr`, `mb_strpos`, `mb_str_pad` (`php >=8.3`), `mb_str_split`, `mb_strtoupper`, `mb_convert_case`.
- The visible symptom of the byte functions: a truncated bio ends in `` or a black diamond, and an aligned table goes crooked as soon as a name has an accent.
- `strtolower`/`strtoupper` became locale-independent ASCII-only operations on `php >=8.2`. Before that they honored the C locale and could mangle bytes ≥0x80. Neither version handles `İ`, `ß`, or Greek final sigma — that is `mb_convert_case($s, MB_CASE_LOWER, 'UTF-8')`.
- `ucfirst("ñandú")` corrupts the first character. `mb_convert_case($s, MB_CASE_TITLE, 'UTF-8')` is the safe title-caser.
- Set `default_charset = UTF-8` in php.ini (the default on modern builds) — it is what `htmlspecialchars` and `mb_*` use when you omit the encoding argument (`php-ini.md`).
- Length limits in a database are usually characters while PHP measures bytes: validate with `mb_strlen`, or a three-byte emoji rejects a "20 character" name at 15.

## Detecting and Fixing Encoding

- `mb_check_encoding($s, 'UTF-8')` before anything else — invalid UTF-8 makes `json_encode` return `false` and `preg_match` with `/u` return `false` (`json.md`).
- `mb_detect_encoding` guesses and is wrong often enough to be dangerous; prefer knowing the source encoding. When you must convert, `mb_convert_encoding($s, 'UTF-8', 'ISO-8859-1')` with an explicit source.
- Double encoding (`Ã©` where `é` belongs) means UTF-8 bytes were interpreted as Latin-1 and re-encoded. It is a data bug, not a display bug: fix it in the pipeline, not with a second conversion.
- The BOM (`\xEF\xBB\xBF`) at the start of an included file becomes output and triggers "headers already sent"; at the start of a CSV it corrupts the first column name (`files.md`, `http.md`).
- `trim()`'s default character list is `" \t\n\r\0\x0B"` — it does NOT strip a non-breaking space (U+00A0), the character users paste from Word. `mb_trim` (`php >=8.4`), or `preg_replace('/^[\p{Z}\s]+|[\p{Z}\s]+$/u', '', $s)`.

## Quoting and Interpolation

- `'single'` is literal apart from `\'` and `\\`; `"double"` interpolates and processes escapes; heredoc `<<<EOT` behaves like double quotes, nowdoc `<<<'EOT'` like single.
- Closing heredoc markers may be indented on `php >=7.3`, and that indentation is stripped from every line of the body.
- Simple interpolation reaches one level: `"$obj->name"` works, `"$obj->a->b"` does not. Braces fix everything: `"{$obj->a->b}"`, `"{$arr['key']}"`.
- Inside a plain double-quoted string, an array key is written UNQUOTED (`"$arr[key]"`); writing `"$arr['key']"` is a parse error. Use braces and stop remembering the rule.
- `${var}` interpolation is deprecated on `php >=8.2`; `{$var}` is the replacement.
- Concatenation with `.` binds tighter than `+` did until PHP 8 changed the precedence — `"n: " . $a + $b` is a syntax error now instead of a silent wrong answer.

## Formatting Numbers and Text

- `sprintf('%.2f', $x)` rounds half away from zero; `number_format($x, 2, '.', ',')` also rounds and adds separators, but returns a STRING that no longer parses as numeric with a thousands separator.
- `%s` on a float uses the `precision` ini; `%.15g` or `var_export` when you need the exact value (`types.md`).
- Positional arguments `%1$s` let a translation reorder placeholders — required for any user-visible template.
- `str_pad` for tables is byte-based; `mb_str_pad` (`php >=8.3`) or `\Symfony\Component\String` for aligned CLI output (`cli.md`).
- `printf`-family width with multibyte input is byte width; there is no `mb_sprintf`.

## PCRE

- `preg_match` returns `1`, `0`, or `false`. `false` means the ENGINE failed — check it, then `preg_last_error_msg()` for the reason.
- The silent killer: `pcre.backtrack_limit` defaults to 1,000,000. A greedy pattern over a 2 MB subject exhausts it and `preg_match` returns `false` with no exception, which truthiness tests read as "no match". Raise the limit only after simplifying the pattern (`php-ini.md`).
- `/u` is required for UTF-8: without it `.` matches one byte and `\w` is ASCII-only. With it, an invalid-UTF-8 subject makes the call return `false` — validate first with `mb_check_encoding`.
- Catastrophic backtracking comes from nested quantifiers over the same class (`(\s+)+$`, `(a+)+b`). Rewrite with possessive quantifiers (`\s++`) or an atomic group (`(?>\s+)`); both stop the engine from re-trying.
- `preg_quote($input, '/')` on every user-supplied fragment, with the delimiter as the second argument — omitting it leaves the delimiter unescaped and the pattern breaks or, worse, changes meaning.
- `preg_replace` with a `$` in the replacement reads it as a backreference: escape user text in replacements too, or use `preg_replace_callback`, which takes a function and has no replacement-string syntax.
- The `/e` modifier was removed in PHP 7; any code still passing it is a rewrite to `preg_replace_callback`.
- `preg_split($p, $s, -1, PREG_SPLIT_NO_EMPTY)` — the flag you always want; the default keeps empty leading and trailing pieces.
- `preg_match_all` with `PREG_SET_ORDER` gives one array per match, which is what a loop wants; the default `PREG_PATTERN_ORDER` groups by capture index.
- Named captures `(?<name>…)` survive pattern edits that renumber positional groups; use them past two groups.
- JIT for PCRE is on by default; it has its own `pcre.jit_stacklimit`, and a deeply recursive pattern can fail only when JIT is enabled.

## Searching and Replacing

- `str_contains` / `str_starts_with` / `str_ends_with` (`php >=8.0`) replace the `strpos(...) !== false` idiom and remove the offset-0 trap entirely.
- `str_replace($search, $replace, $subject)` with arrays applies replacements SEQUENTIALLY, so a later pair can rewrite what an earlier one produced. When the replacements can collide, use `strtr($subject, $map)`, which scans once and never reprocesses output.
- `strtr` with a map prefers the longest matching key — the correct tool for templating and transliteration.
- `substr_count` counts non-overlapping occurrences; overlapping counts need a loop with an offset.
- `explode('', $s)` throws `ValueError` on `php >=8.0`; `str_split`/`mb_str_split` is the character splitter.
- `implode` accepts only `(string $glue, array $pieces)` on `php >=8.0` — the legacy swapped order was removed.

## Binary and Null Bytes

- A null byte in a path truncates it inside functions that hand the string to the C API; PHP rejects paths containing `\0` with a `ValueError` on modern versions, but validation code that ran BEFORE the check can still be fooled. Strip or reject `\0` at input (`security.md`).
- `hash_equals` for comparing digests, `bin2hex`/`hex2bin` for transport, `base64_encode` when it must survive a text channel; `base64_decode($s, true)` with strict mode returns `false` on invalid input instead of silently skipping characters.
- `random_bytes(32)` is binary — hex- or base64-encode it before putting it in a URL or a cookie (`security.md`).

## Related

- Pattern design beyond the PHP bindings: the `regex` skill
- Escaping strings for HTML, JS, URLs, and shells: `security.md`
- CSV and file-encoding issues: `files.md`

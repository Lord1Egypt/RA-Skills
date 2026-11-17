# KROKO comment doctrine

Rules for what a comment may say, how it must be written, and what must be
deleted. Mechanically enforced where possible by `scripts/kroko.py`
(codes K008-K014); the rest is a review checklist.

---

## The one principle

> **A comment exists to say what the code cannot say.**

The code already states *what* it does and *how*. A comment is justified only when
it carries something the reader cannot recover from the code: the reason, the
constraint, the history, the trade-off, the trap.

The test, applied to every comment before it is kept:

> **If I delete this comment, what is lost?**
> If the answer is "nothing" — delete it. If the answer is "the reader would
> change this line and break something" — it is load-bearing, keep it.

Dart's guidance is blunt about the usual failure direction: most people write too
few comments, not too many. But the opposite failure is more common in generated
code: comment volume as a substitute for clarity, which makes the file longer
without making it clearer.

---

## The seven rules

### 1. Say why, not what

The code says what. The comment says why it is this way and not the obvious way.

```python
# Bad: restates the line
# Increment the retry counter.
retries += 1

# Good: explains a decision the code cannot express
# The upstream gateway closes idle sockets after 30s, so the retry must be
# faster than that or every attempt is guaranteed to fail.
retries += 1
```

### 2. Never narrate the code back

A comment whose words overlap the line beneath it is a duplicate line. This is
the single most common generated-code comment and it is enforced: **K014**.

```javascript
// Bad
// Return the user name.
return user.name;

// Good
// The API returns a display name that may not match the login handle,
// so prefer the former wherever the user will see it.
return user.displayName;
```

### 3. Sentences, capitalised, punctuated

Every comment is a sentence, even a fragment, even a one-word note.

Dart states the rule for its own codebase: *"Capitalize the first word unless it's
a case-sensitive identifier. End it with a period (or '!' or '?', I suppose). This
is true for all comments: doc comments, inline stuff, even TODOs. Even if it is a
sentence fragment."*

Go states the companion rule: a declaration comment *"should begin with the name
of the thing being described and end in a period"*, because the comment is
extracted into generated documentation where a fragment reads as a broken sentence.

Enforced as **K013** (strict mode).

### 4. Document the public surface, and only the public surface

Python's PEP 257: *"All modules should normally have docstrings, and all functions
and classes exported by a module should also have docstrings."* Dart:
*"PREFER writing doc comments for public APIs."* Go: *"All top-level, exported
names should have doc comments, as should non-trivial unexported type or function
declarations."*

The inverse also holds: a comment on a self-evident private one-liner is noise.
Enforced as **K011** (default mode) for public functions and the module itself.

### 5. State the contract the signature cannot hold

A docstring answers the questions the type annotation cannot:

- what is returned when the input is empty,
- what it raises, and on what condition,
- what the caller must guarantee,
- what is unusually expensive or blocking,
- what it mutates.

PEP 257 requires the prescriptive mood, not the descriptive one: *"The docstring is
a phrase ending in a period. It prescribes the function or method's effect as a
command ('Do this', 'Return that'), not as a description."*

Rust's API Guidelines go further and make the sections conventional: an **Errors**
section for conditions that produce an error, a **Panics** section for conditions
that panic, and a **Safety** section for every `unsafe` function, listing the
invariants the caller must uphold. Rust also insists that an example shows *why*
someone would use the item, not merely *how* to call it, and that example code never
`unwrap`s, because *"example code is often copied verbatim by users."*

### 6. No dead code, no decoration, no bookkeeping

Three banned species, all enforced:

| Species | Example | Code |
|---|---|---|
| Placeholder | `# TODO: handle the empty case` | K008 |
| Commented-out code | `# total = compute_total(items)` | K009 |
| Banner art | `# ====================` | K010 |

A placeholder is a promise the author did not keep. If the work remains, file it
and name the ticket; if it is not needed, delete the line. Commented-out code is
a version-control responsibility, not a source-file one: the history already has
it, and a reader cannot tell whether the line is a warning, a plan, or rot.

A banner separator says nothing and survives every refactor, so it slowly lies
about the structure of the file.

### 7. A stale comment is worse than no comment

A wrong comment actively misleads, and it is invisible in review because reviewers
read comments as documentation rather than as claims to verify. So:

- A comment must be updated in the same change as the code it describes.
- Never write a comment describing behaviour you have not verified. If you have not
  run it, you do not know what it does, and a comment asserting it works is the
  written form of a false claim.
- Never leave a comment that says what the code *used to* do.

---

## Where the comment goes

| Place | Form | Contains |
|---|---|---|
| Module top | Module docstring | what the module is for, what it does not do |
| Public function | Docstring | summary sentence, then contract: args, returns, raises, cost, mutation |
| Non-obvious line | Inline `#` | the reason, above the line, never trailing |
| Complex expression | Inline `#` | the invariant that makes it correct |
| Anywhere | — | never a restatement |

Place a comment **above** the line it explains. Trailing comments push against the
line-length limit, wrap badly at narrow widths, and are the first thing a formatter
moves.

---

## Language form, exactly

| Language | Comment | Doc comment | Binding rule |
|---|---|---|---|
| Python | `# Capitalised sentence.` | `"""Summary sentence.` + body + `"""` | PEP 257: triple double quotes, one-line docstring is a phrase ending in a period, never restate the signature |
| Dart | `// Capitalised sentence.` | `/// Summary sentence.` | Never `/* */` for documentation; first sentence on its own line; avoid redundancy with surrounding context |
| Go | `// Name does X.` | same, on every exported name | Begin with the name of the thing; end with a period |
| Rust | `// Reason for the decision.` | `/// Summary.` + `# Errors` / `# Panics` / `# Safety` | Examples show why, use `?` not `unwrap` |
| Swift | `// Reason for the decision.` | `/// Summary.` + `- Parameter` / `- Returns` / `- Throws` | DocC markup |
| TypeScript | `// Reason for the decision.` | `/** Summary. */` with `@param`, `@returns`, `@throws` | TSDoc |
| C/C++ | `// Reason for the decision.` | `///` or `/** */` above the declaration | Never restate the parameter names |

---

## The docstring template

```python
def backoff_delay(attempt, ceiling):
    """Return the retry delay in seconds for one attempt.

    Doubles from one second, so a caller retrying six times waits less than
    a minute in total.

    Args:
        attempt: Zero-based retry index. Negative values are treated as zero.
        ceiling: Hard upper bound in seconds; the gateway drops idle
            connections after thirty, so values above thirty never succeed.

    Returns:
        Delay in seconds, never above `ceiling`.

    Raises:
        ValueError: If `ceiling` is not positive.
    """
```

Every line earns its place: the summary is a sentence, the second paragraph carries
the *why*, and the three sections carry the contract. Nothing restates a type.

---

## Self-check before saving a file

- [ ] Does every public function and the module itself have a docstring?
- [ ] Does each docstring's first line end in `.`, `!` or `?`
- [ ] Does any comment merely repeat the code beneath it? Delete it.
- [ ] Is there a `TODO`, commented-out code, or banner? Delete it or file it.
- [ ] Is every comment true of the code as it now stands?
- [ ] Could a reviewer delete a comment without losing information? Then it was noise.

## Scope: strict mode is for code being written now

Measured on the Python standard library (1,446 files, 101,237 comments): only **9.5%**
of existing comments are punctuated as sentences. Strict mode therefore reports about
89,000 findings across that corpus — the rule is right and the corpus predates it.

Use strict mode on new code, on a file you are already rewriting, or on a
documentation drive. Use default mode on legacy code you are only reading. Enforcing
sentence form retroactively across a legacy codebase produces a diff nobody reviews,
which is how a rule gets switched off.

Run the mechanical half:

```bash
python3 scripts/kroko.py --strict-comments path/to/file.py
```

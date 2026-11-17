# Example sessions

Copyable transcripts. Each was run verbatim against the fixture described;
outputs are real.

## A stale import after a rename

Setup: `pkg/core.py` defines `get_account`. `pkg/views.py` still says:

```python
from .core import get_user_account
```

Find it:

```console
$ grounded scan .
LIE pkg/views.py:1 [stale-import] `get_user_account` imported from `pkg/core.py` but never defined there
    claim: from .core import get_user_account
    evidence: `pkg/core.py` exists but defines no `get_user_account`.
    fix: Check for a rename in `pkg/core.py` (or a moved submodule).

grounded: 1 finding(s) in 3 file(s), 1 lie(s), 0 drift(s), 0 smell(s).
```

Ask what touches the name before renaming anything:

```console
$ grounded impact get_user_account .
impact of `get_user_account`:
  defined_in (0):
  imported_by (1):
    pkg/views.py
  claimed_by (0):
```

Defined nowhere, imported once: safe to fix the one import. No other
file in the tree depends on the old name.

## A stale comment after a rename

Setup: `pkg/core.py` defines `get_account`. A comment elsewhere says:

```python
# Calls `get_user_account()` to load the profile.
```

```console
$ grounded scan .
LIE pkg/views.py:1 [stale-symbol-ref] Comment references `get_user_account` which is not defined here
    claim: `get_user_account()`
    evidence: `get_user_account` is not defined, imported, or used in this file, and no definition of `get_user_account` was found in 3 indexed source files.
    fix: Update the comment to the current name, or remove the reference. Did you mean: `get_account`()

grounded: 1 finding(s) in 3 file(s), 1 lie(s), 0 drift(s), 0 smell(s).
```

```console
$ grounded fix . --dry-run
would rewrite pkg/views.py:1: get_user_account() -> get_account()
grounded fix: 1 file(s) would change.
```

The rewrite applies only with exactly one similar, same-directory
candidate. Ties and guesses never touch the file.

# Common Mistakes and Anti-patterns

## 1. Trusting PDF metadata title blindly

**Wrong:** Assume PDF `/Title` metadata field is correct.
**Why:** Often contains LaTeX internal names (`FM-main.dvi`), truncated titles, or garbled encoding.

**Right:** Always cross-check with the actual PDF text (first page) and filename.

---

## 2. Using arXiv submission year as publication year

**Wrong:** `year = 2020` because that's what `arXiv:2007.13544` says.
**Why:** arXiv papers may be submitted one year and published in a conference the next year.

**Examples:**
| Paper | arXiv year | Conference year |
|-------|-----------|----------------|
| Monte Carlo Sampling for Regret Minimization | 2009 | NeurIPS 2009 |
| ReBeL (Combining Deep RL and Search) | 2020 | NeurIPS 2020 |

**Right:** Always search for the official conference/journal version and use that year.

---

## 3. Renaming without web verification

**Wrong:** Trust auto-extracted title and execute rename immediately.
**Why:** Multi-word titles get truncated mid-sentence; institution names contaminate title extraction; similar-looking filenames may have different papers.

**Right:** Run in 3 stages. Extract → Verify (web search) → Rename.

---

## 4. Not backing up before batch rename

**Wrong:** Renaming directly without creating a backup.
**Why:** A single wrong entry in VERIFIED_DATA can corrupt filenames irreversibly.

**Right:** `execute.py` always creates `folder/_backup_YYYYMMDD_HHMMSS/` before moving files.

---

## 5. Title case inconsistency

**Wrong:** Mixing capitalized and lowercase in titles.
**Why:** Makes file sorting and deduplication unreliable.

**Right:** Preserve the original case as published (capitalize proper nouns, lowercase articles). The filename normalization only strips special chars, it does not re-case titles.

---

## 6. Mis-detecting duplicates

**Wrong:** Only comparing exact string equality for duplicate detection.
**Why:** `"Near-Optimal Learning..."` vs `"Near Optimal Learning..."` (hyphen difference) are the same paper.

**Right:** Normalize before comparing: `re.sub(r'[^a-z0-9]', '', title.lower())`. This is already implemented in `extract.py`.

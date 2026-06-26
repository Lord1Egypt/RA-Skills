# Reference Repositories

## `flameworks/JaneStreetPuzzles`

- Broadest coverage in the sampled set.
- Mostly Python, often split into `main`, `methods`, `gridClass`, `basic`, and `adv` files.
- Best for staged pruning and reusable board abstractions.

## `Tzadiko/JaneStreetPuzzles`

- Mixed C++, C#, and PHP.
- Best for compact compiled brute-force implementations and single-month one-off solvers.

## `whoek/janestreet-puzzles`

- Mostly OCaml, with supporting Python, JavaScript, notebooks, and spreadsheets.
- Best for exhaustive search in a functional style plus lightweight visualization helpers.

## Local workflow

- Refresh the repo-wide machine-readable index with `python3 scripts/index_reference_repos.py`.
- Use `knowledge/reference-index.json` when you need exact monthly coverage instead of high-level guidance.

# Username variants

When searching a username, also consider lightweight variants.
Do not explode the search space absurdly.

## Useful variant patterns
- original username
- lowercase version
- remove separators (`_`, `.`, `-`)
- swap separators (`name_last` -> `name.last`, `name-last`)
- trim trailing digits and test base handle if reasonable
- common compact form if obvious

## Examples
- `john_doe` -> `john_doe`, `johndoe`, `john.doe`, `john-doe`
- `alice1997` -> `alice1997`, `alice`

## Rule
Only include a small set of plausible variants.
Prefer precision over noisy expansion.

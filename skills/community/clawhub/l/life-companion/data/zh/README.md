# data/zh

`TSCharacters.txt` is OpenCC's traditional → simplified **character** table, copied
verbatim from https://github.com/BYVoid/OpenCC (`data/dictionary/TSCharacters.txt`,
fetched 2026-09-12). OpenCC is licensed under Apache-2.0; the licence text is in
`LICENSE-OpenCC.txt`.

`scripts/_zh.py` uses it to fold traditional characters to simplified before the honesty
gate (`selfcheck.py`) and the crisis backstop (`safety_scan.py`) look at anything. Both are
written in simplified characters, and both used to miss the same sentence written in
traditional ones. Only entries that map one character to one character are used, so the
folded text keeps its length and a finding can quote the original words back.

# PII Pattern Hints

| Column hint | Detection |
|---|---|
| name / 姓名 | Chinese 2-4 char names; English alphabetic words |
| phone / 手机 / mobile | 11-digit starting with 1, optional +86 / 86 prefix |
| id_number / 身份证 | 18 digits, last char may be X |
| email | RFC 5322 pattern |
| address / 地址 | Province/City/District prefix triplet |

# Action contract

scan/redact:files1..100; patterns optional subset email,phone,identity,ipv4,token; literals optional up to50 exact strings2..1000chars. Supports UTF-8 txt/md/csv/json/log/html,8MiB/file. phone targets Chinese mobile patterns; identity is an ID-shaped pattern, not identity validation. JSON secret field names are masked recursively. CSV structure retained and formula-shaped output is literalized. Outputs are new files; reports contain counts and hashes, not matched secret values. Regex patterns are fixed; custom rules are literal strings. Review redacted copies before external sharing.

Reports remain local. Use the current model to interpret results; the executable tool performs the documented data operations.

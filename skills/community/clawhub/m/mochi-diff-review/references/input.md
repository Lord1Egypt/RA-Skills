# Action contract

text:left,right,ignoreWhitespace optional; UTF-8<=4MiB and10000lines each, creates unified.diff plus reports. json:left/right structurally compares object keys independent of order and ordered arrays; up to1000 reported differences. csv:left/right,keys existing key-column list; duplicate keys reported for review, not auto-matched; up to1000 changed row examples and exact changed count. directories:left/right relative folders compare file hashes. manifest:directory creates report.json with files and hashes. verify:directory,manifest previous report.json; extra,missing or changed files fail verification. Max5000 files,64MiB/file,256MiB/directory. Does not overwrite inputs.

Reports remain local. Use the current model to interpret results; the executable tool performs the documented data operations.

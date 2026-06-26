# gog Sheets Reference

Use these examples as the default command shapes for this skill. Prefer exact spreadsheet IDs, exact tab names, and JSON output where machine parsing matters.

## Read

```bash
gog sheets metadata <spreadsheetId> --json
gog sheets get <spreadsheetId> 'Sheet1!A1:B10' --json
gog sheets get <spreadsheetId> MyNamedRange --json
gog sheets notes <spreadsheetId> 'Sheet1!A1:B10' --json
gog sheets links <spreadsheetId> 'Sheet1!A1:B10' --json
gog sheets read-format <spreadsheetId> 'Sheet1!A1:B2' --json
```

## Create

```bash
gog sheets create "My New Spreadsheet" --sheets "Sheet1,Sheet2"
gog sheets add-tab <spreadsheetId> <tabName>
gog sheets rename-tab <spreadsheetId> <oldName> <newName>
```

## Update values

```bash
gog sheets update <spreadsheetId> 'A1' 'val1|val2,val3|val4'
gog sheets update <spreadsheetId> 'A1' --values-json '[["a","b"],["c","d"]]'
gog sheets update <spreadsheetId> 'Sheet1!A1:C1' 'new|row|data' --copy-validation-from 'Sheet1!A2:C2'
gog sheets update <spreadsheetId> MyNamedRange 'new|row|data'
gog sheets append <spreadsheetId> 'Sheet1!A:C' 'new|row|data'
gog sheets append <spreadsheetId> MyNamedRange 'new|row|data'
gog sheets update-note <spreadsheetId> 'Sheet1!A1' --note 'Reviewed'
```

## Destructive or broad changes

Confirm intent before running these:

```bash
gog sheets clear <spreadsheetId> 'Sheet1!A1:B10'
gog sheets find-replace <spreadsheetId> "old" "new"
gog sheets find-replace <spreadsheetId> "old" "new" --sheet Sheet1 --regex
gog sheets delete-tab <spreadsheetId> <tabName> --force
gog sheets named-ranges delete <spreadsheetId> MyNamedRange
gog sheets insert <spreadsheetId> "Sheet1" rows 2 --count 3
gog sheets insert <spreadsheetId> "Sheet1" cols 3 --after
```

## Formatting and layout

Treat these as high-impact when they touch broad ranges:

```bash
gog sheets format <spreadsheetId> 'Sheet1!A1:B2' --format-json '{"textFormat":{"bold":true}}' --format-fields 'userEnteredFormat.textFormat.bold'
gog sheets merge <spreadsheetId> 'Sheet1!A1:B2'
gog sheets unmerge <spreadsheetId> 'Sheet1!A1:B2'
gog sheets number-format <spreadsheetId> 'Sheet1!C:C' --type CURRENCY --pattern '$#,##0.00'
gog sheets freeze <spreadsheetId> --rows 1 --cols 1
gog sheets resize-columns <spreadsheetId> 'Sheet1!A:C' --auto
gog sheets resize-rows <spreadsheetId> 'Sheet1!1:10' --height 36
```

## Named ranges

```bash
gog sheets named-ranges <spreadsheetId> --json
gog sheets named-ranges get <spreadsheetId> MyNamedRange --json
gog sheets named-ranges add <spreadsheetId> MyNamedRange 'Sheet1!A1:B2'
gog sheets named-ranges update <spreadsheetId> MyNamedRange --name MyNamedRange2
```

## Export

```bash
gog sheets export <spreadsheetId> --format pdf --out ./sheet.pdf
gog sheets export <spreadsheetId> --format xlsx --out ./sheet.xlsx
```

## Auth and account selection

```bash
gog auth credentials ~/Downloads/client_secret_....json
gog auth add you@gmail.com --services sheets
gog auth add you@gmail.com --services sheets --force-consent
gog auth status
GOG_ACCOUNT=you@gmail.com gog sheets metadata <spreadsheetId> --json
GOG_ENABLE_COMMANDS=sheets gog sheets get <spreadsheetId> 'Sheet1!A1:B10' --json
```

## Help-first fallback

If a command shape is uncertain, inspect the CLI instead of guessing:

```bash
gog sheets --help
gog sheets named-ranges --help
gog auth add --help
```

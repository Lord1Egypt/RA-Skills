Google Sheets (Generic, via Maton Gateway)

Access and manage any Google Sheets spreadsheet via Maton Gateway with full OAuth authentication. Supports reading, writing, updating, appending, clearing, formatting, sheet management, formulas, and protection.

🌐 Base URL
https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}/{native-api-path}

{SPREADSHEET_ID} → Your spreadsheet ID
{native-api-path} → Google Sheets API path (values, sheets, etc.)
🔐 Authentication

Include your Maton API key in headers:

-H "Authorization: Bearer $MATON_API_KEY"


Set in environment:

export MATON_API_KEY="YOUR_API_KEY"

📄 Operations (Generic Placeholders)
1. Read Values
curl "https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!{RANGE}" \
  -H "Authorization: Bearer $MATON_API_KEY"


Placeholders:

{SHEET_NAME} → Name of any sheet/tab
{RANGE} → A1 notation (A1:Z100)
2. Append Values

Add new rows to the bottom of a sheet.

curl -X POST "https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!{RANGE}:append?valueInputOption=USER_ENTERED" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "values": [
      ["{VALUE1}", "{VALUE2}", "{VALUE3}", "...", "{VALUEN}"]
    ]
  }'

{VALUE1} ... {VALUEN} → Any generic values
3. Update Values
curl -X PUT "https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!{RANGE}?valueInputOption=USER_ENTERED" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "values": [
      ["{VALUE1}", "{VALUE2}", "{VALUE3}", "...", "{VALUEN}"]
    ]
  }'

4. Batch Update Values

Update multiple ranges at once:

curl -X POST "https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}/values:batchUpdate" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "valueInputOption":"USER_ENTERED",
    "data":[
      {"range":"{SHEET_NAME}!{RANGE1}","values":[["{VALUE1A}", "{VALUE1B}", "..."]]},
      {"range":"{SHEET_NAME}!{RANGE2}","values":[["{VALUE2A}", "{VALUE2B}", "..."]]}
    ]
  }'

5. Clear Values
curl -X POST "https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!{RANGE}:clear" \
  -H "Authorization: Bearer $MATON_API_KEY"

6. Get Spreadsheet Metadata
curl "https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}" \
  -H "Authorization: Bearer $MATON_API_KEY"

Returns sheets, properties, titles, IDs
7. Add a New Sheet
curl -X POST "https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}:batchUpdate" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requests":[
      {"addSheet":{"properties":{"title":"{NEW_SHEET_NAME}"}}}
    ]
  }'

8. Delete a Sheet
curl -X POST "https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}:batchUpdate" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requests":[
      {"deleteSheet":{"sheetId":{SHEET_ID}}}
    ]
  }'

9. Copy Sheet
curl -X POST "https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}/sheets/{SHEET_ID}:copyTo" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "destinationSpreadsheetId":"{DEST_SPREADSHEET_ID}"
  }'

10. Formatting & Cell Styling
curl -X POST "https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}:batchUpdate" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requests":[
      {
        "repeatCell":{
          "range":{"sheetId":{SHEET_ID},"startRowIndex":{START_ROW},"endRowIndex":{END_ROW},"startColumnIndex":{START_COL},"endColumnIndex":{END_COL}},
          "cell":{"userEnteredFormat":{"backgroundColor":{"red":{R},"green":{G},"blue":{B}}}},
          "fields":"userEnteredFormat.backgroundColor"
        }
      }
    ]
  }'

11. Insert Formulas
curl -X PUT "https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}/values/{SHEET_NAME}!{CELL}?valueInputOption=USER_ENTERED" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "values":[["{FORMULA}"]]
  }'

12. Protected Ranges
curl -X POST "https://gateway.maton.ai/google-sheets/v4/spreadsheets/{SPREADSHEET_ID}:batchUpdate" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requests":[
      {"addProtectedRange":{"protectedRange":{"range":{"sheetId":{SHEET_ID},"startRowIndex":{START_ROW},"endRowIndex":{END_ROW}},"description":"{DESCRIPTION}"}}}
    ]
  }'

📚 Notes
{SPREADSHEET_ID} → Your spreadsheet ID
{SHEET_NAME} → Any sheet/tab name
{RANGE} → A1 notation (e.g., A1:Z100)
{VALUE1}, {VALUE2}, … → Generic placeholders for any cell content
USER_ENTERED parses numbers, dates, formulas automatically
batchUpdate is required for structural changes (add/delete sheets, formatting, protection)
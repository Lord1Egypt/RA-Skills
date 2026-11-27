# Microsoft Excel access policy

An access policy limits which endpoints Microsoft Excel connections may call through Maton. Microsoft Excel doesn't offer a choice of OAuth scopes, so an access policy is the way to narrow a connection. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/microsoft-excel#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Microsoft Excel: its 93 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create microsoft-excel --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1.0/me/drive"},
    {"method": "GET", "path": "v1.0/me/drive/root/children"},
    {"method": "GET", "path": "v1.0/me/drive/root/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/children"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/content"},
    {"method": "GET", "path": "v1.0/me/drive/root:/**"},
    {"method": "POST", "path": "v1.0/me/drive/items/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/me/drive/items/{id}/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/me/drive/root:/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/me/drive/root:/{id}/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/me/drive/root:/{id}/{id}/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/drives/{id}/items/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/drives/{id}/items/{id}/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/drives/{id}/root:/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/drives/{id}/root:/{id}/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/drives/{id}/root:/{id}/{id}/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/me/drives/{id}/items/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/users/{id}/drive/items/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/users/{id}/drives/{id}/items/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/groups/{id}/drive/items/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/groups/{id}/drives/{id}/items/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/sites/{id}/drive/items/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/sites/{id}/drives/{id}/items/{id}/workbook/createSession"},
    {"method": "POST", "path": "v1.0/me/drive/items/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/me/drive/items/{id}/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/me/drive/root:/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/me/drive/root:/{id}/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/me/drive/root:/{id}/{id}/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/drives/{id}/items/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/drives/{id}/items/{id}/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/drives/{id}/root:/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/drives/{id}/root:/{id}/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/drives/{id}/root:/{id}/{id}/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/me/drives/{id}/items/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/users/{id}/drive/items/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/users/{id}/drives/{id}/items/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/groups/{id}/drive/items/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/groups/{id}/drives/{id}/items/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/sites/{id}/drive/items/{id}/workbook/functions/{id}"},
    {"method": "POST", "path": "v1.0/sites/{id}/drives/{id}/items/{id}/workbook/functions/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/**"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/application"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/operations/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/protection"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/range"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/usedRange"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/format/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/tables"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}/rows"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}/rows/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}/columns"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}/columns/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}/columns/{id}/filter"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}/columns/{id}/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}/range"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}/headerRowRange"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}/dataBodyRange"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}/totalRowRange"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}/sort"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/tables/{id}/worksheet"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/image"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/series/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/series/{id}/points"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/names"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/names"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/names/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/names/{id}/range"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/comments"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/comments/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/comments/{id}/replies"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/comments/{id}/replies/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/pivotTables"},
    {"method": "GET", "path": "v1.0/me/drive/items/{id}/workbook/worksheets/{id}/pivotTables/{id}"},
    {"method": "GET", "path": "v1.0/me/drive/**"},
    {"method": "GET", "path": "v1.0/me/drives/**"},
    {"method": "GET", "path": "v1.0/drives/**"},
    {"method": "GET", "path": "v1.0/users/{id}/drive/**"},
    {"method": "GET", "path": "v1.0/users/{id}/drives/**"},
    {"method": "GET", "path": "v1.0/groups/{id}/drive/**"},
    {"method": "GET", "path": "v1.0/groups/{id}/drives/**"},
    {"method": "GET", "path": "v1.0/sites/{id}/drive/**"},
    {"method": "GET", "path": "v1.0/sites/{id}/drives/**"}
  ],
  "deny": []
}
```

## Endpoints

The Microsoft Excel endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1.0/me/drive | read | files | Get the signed-in user's drive. |
| GET | v1.0/me/drive/root/children | read | files | List files in the root folder. |
| GET | v1.0/me/drive/root/{id} | read | files | Search the drive for workbooks: root/search(q='.xlsx'). |
| GET | v1.0/me/drive/items/{id} | read | files | Get a file by ID. |
| GET | v1.0/me/drive/items/{id}/children | read | files | List the files in a folder. |
| GET | v1.0/me/drive/items/{id}/content | read | files | Download a workbook file. |
| GET | `v1.0/me/drive/root:/**` | read | files | Path-addressed reads: root:/file.xlsx, root:/file.xlsx:/workbook/worksheets, ...:/workbook/tables('T')/rows (any GET). |
| PUT | v1.0/me/drive/items/{id}/content | write | files | Replace a workbook file's contents. |
| PUT | `v1.0/me/drive/root:/**` | write | files | Upload a workbook by path (root:/file.xlsx:/content). |
| POST | v1.0/me/drive/items/{id}/workbook/closeSession | write | sessions | Close a workbook session (ends server-side session state). |
| POST | v1.0/me/drive/items/{id}/workbook/refreshSession | write | sessions | Keep a workbook session alive. |
| POST | v1.0/me/drive/items/{id}/workbook/createSession | read | sessions | Create a workbook session; no workbook data changes until a write call is made (item by ID). |
| POST | v1.0/me/drive/items/{id}/{id}/workbook/createSession | read | sessions | Create a workbook session; no workbook data changes until a write call is made (items/{parent-id}:/{filename}:/ form). |
| POST | v1.0/me/drive/root:/{id}/workbook/createSession | read | sessions | Create a workbook session; no workbook data changes until a write call is made (file in the root folder, root:/file:/ form). |
| POST | v1.0/me/drive/root:/{id}/{id}/workbook/createSession | read | sessions | Create a workbook session; no workbook data changes until a write call is made (path-addressed file one folder deep). |
| POST | v1.0/me/drive/root:/{id}/{id}/{id}/workbook/createSession | read | sessions | Create a workbook session; no workbook data changes until a write call is made (path-addressed file two folders deep). |
| POST | v1.0/drives/{id}/items/{id}/workbook/createSession | read | sessions | Create a workbook session; no workbook data changes until a write call is made (item by ID). |
| POST | v1.0/drives/{id}/items/{id}/{id}/workbook/createSession | read | sessions | Create a workbook session; no workbook data changes until a write call is made (items/{parent-id}:/{filename}:/ form). |
| POST | v1.0/drives/{id}/root:/{id}/workbook/createSession | read | sessions | Create a workbook session; no workbook data changes until a write call is made (file in the root folder, root:/file:/ form). |
| POST | v1.0/drives/{id}/root:/{id}/{id}/workbook/createSession | read | sessions | Create a workbook session; no workbook data changes until a write call is made (path-addressed file one folder deep). |
| POST | v1.0/drives/{id}/root:/{id}/{id}/{id}/workbook/createSession | read | sessions | Create a workbook session; no workbook data changes until a write call is made (path-addressed file two folders deep). |
| POST | v1.0/me/drives/{id}/items/{id}/workbook/createSession | read | sessions | Create a workbook session (item by ID). |
| POST | v1.0/users/{id}/drive/items/{id}/workbook/createSession | read | sessions | Create a workbook session (item by ID). |
| POST | v1.0/users/{id}/drives/{id}/items/{id}/workbook/createSession | read | sessions | Create a workbook session (item by ID). |
| POST | v1.0/groups/{id}/drive/items/{id}/workbook/createSession | read | sessions | Create a workbook session (item by ID). |
| POST | v1.0/groups/{id}/drives/{id}/items/{id}/workbook/createSession | read | sessions | Create a workbook session (item by ID). |
| POST | v1.0/sites/{id}/drive/items/{id}/workbook/createSession | read | sessions | Create a workbook session (item by ID). |
| POST | v1.0/sites/{id}/drives/{id}/items/{id}/workbook/createSession | read | sessions | Create a workbook session (item by ID). |
| POST | v1.0/me/drive/items/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function (abs, vlookup, pmt, ...); computes a result only (item by ID). |
| POST | v1.0/me/drive/items/{id}/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function (abs, vlookup, pmt, ...); computes a result only (items/{parent-id}:/{filename}:/ form). |
| POST | v1.0/me/drive/root:/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function (abs, vlookup, pmt, ...); computes a result only (file in the root folder, root:/file:/ form). |
| POST | v1.0/me/drive/root:/{id}/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function (abs, vlookup, pmt, ...); computes a result only (path-addressed file one folder deep). |
| POST | v1.0/me/drive/root:/{id}/{id}/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function (abs, vlookup, pmt, ...); computes a result only (path-addressed file two folders deep). |
| POST | v1.0/drives/{id}/items/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function (abs, vlookup, pmt, ...); computes a result only (item by ID). |
| POST | v1.0/drives/{id}/items/{id}/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function (abs, vlookup, pmt, ...); computes a result only (items/{parent-id}:/{filename}:/ form). |
| POST | v1.0/drives/{id}/root:/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function (abs, vlookup, pmt, ...); computes a result only (file in the root folder, root:/file:/ form). |
| POST | v1.0/drives/{id}/root:/{id}/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function (abs, vlookup, pmt, ...); computes a result only (path-addressed file one folder deep). |
| POST | v1.0/drives/{id}/root:/{id}/{id}/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function (abs, vlookup, pmt, ...); computes a result only (path-addressed file two folders deep). |
| POST | v1.0/me/drives/{id}/items/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function; computes a result only (item by ID). |
| POST | v1.0/users/{id}/drive/items/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function; computes a result only (item by ID). |
| POST | v1.0/users/{id}/drives/{id}/items/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function; computes a result only (item by ID). |
| POST | v1.0/groups/{id}/drive/items/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function; computes a result only (item by ID). |
| POST | v1.0/groups/{id}/drives/{id}/items/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function; computes a result only (item by ID). |
| POST | v1.0/sites/{id}/drive/items/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function; computes a result only (item by ID). |
| POST | v1.0/sites/{id}/drives/{id}/items/{id}/workbook/functions/{id} | read | functions | Call an Excel worksheet function; computes a result only (item by ID). |
| GET | `v1.0/me/drive/items/{id}/workbook/**` | read | workbook | Any GET under a workbook, e.g. worksheets('Sheet1')/range(address='A1:B2')/format, tables('T')/rows/itemAt(index=0). |
| GET | v1.0/me/drive/items/{id}/workbook/application | read | workbook | Get the workbook application's calculation mode. |
| POST | v1.0/me/drive/items/{id}/workbook/application/calculate | write | workbook | Recalculate the workbook; volatile formulas get new values that are saved outside a non-persistent session. |
| GET | v1.0/me/drive/items/{id}/workbook/operations/{id} | read | workbook | Get the status of a long-running workbook operation. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets | read | worksheets | List worksheets. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id} | read | worksheets | Get a worksheet by ID or name. |
| GET | v1.0/me/drive/items/{id}/workbook/{id} | read | worksheets | Get a worksheet, table or name with a function segment: worksheets('Sheet1'), tables('Table1'), names('n'). |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/protection | read | worksheets | Get a worksheet's protection settings. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets | write | worksheets | Create a worksheet. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/add | write | worksheets | Add a worksheet. |
| PATCH | v1.0/me/drive/items/{id}/workbook/worksheets/{id} | write | worksheets | Update a worksheet: name, position, visibility. |
| DELETE | v1.0/me/drive/items/{id}/workbook/worksheets/{id} | write | worksheets | Delete a worksheet. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/protection/protect | write | worksheets | Protect a worksheet. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/protection/unprotect | write | worksheets | Remove protection from a worksheet. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/range | read | ranges | Get the whole worksheet as a range. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/usedRange | read | ranges | Get the used range of a worksheet. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id} | read | ranges | Get a range with a function segment: range(address='A1:B2'), usedRange(valuesOnly=true), cell(row=0,column=0). |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/{id} | read | ranges | Read from a range: format, sort, worksheet, or derived ranges such as entireRow, column(column=1), lastCell, visibleView. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/format/{id} | read | ranges | Get range formatting details: fill, font, borders, protection. |
| PATCH | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id} | write | ranges | Update a range's values, formulas or number format. |
| PATCH | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/format | write | ranges | Update range formatting. |
| PATCH | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/format/{id} | write | ranges | Update range fill, font or protection formatting. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/clear | write | ranges | Clear a range's values and/or formatting. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/insert | write | ranges | Insert cells, shifting existing cells. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/delete | write | ranges | Delete cells, shifting remaining cells. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/merge | write | ranges | Merge the cells of a range. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/unmerge | write | ranges | Unmerge the cells of a range. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/sort/apply | write | ranges | Sort a range. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/format/autofitColumns | write | ranges | Autofit the column widths of a range. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/{id}/format/autofitRows | write | ranges | Autofit the row heights of a range. |
| GET | v1.0/me/drive/items/{id}/workbook/tables | read | tables | List the tables in a workbook. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/tables | read | tables | List the tables on a worksheet. |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id} | read | tables | Get a table by ID or name. |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id}/rows | read | tables | List table rows. |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id}/rows/{id} | read | tables | Get a table row by index, or rows/itemAt(index=0). |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id}/columns | read | tables | List table columns. |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id}/columns/{id} | read | tables | Get a table column. |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id}/columns/{id}/filter | read | tables | Get the filter applied to a table column. |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id}/columns/{id}/{id} | read | tables | Get a table column's range: range, dataBodyRange, headerRowRange, totalRowRange. |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id}/range | read | tables | Get the range of the whole table. |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id}/headerRowRange | read | tables | Get the table's header row range. |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id}/dataBodyRange | read | tables | Get the table's data body range. |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id}/totalRowRange | read | tables | Get the table's total row range. |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id}/sort | read | tables | Get the table's sort settings. |
| GET | v1.0/me/drive/items/{id}/workbook/tables/{id}/worksheet | read | tables | Get the worksheet that contains the table. |
| POST | v1.0/me/drive/items/{id}/workbook/tables/add | write | tables | Create a table from a range. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/tables/add | write | tables | Create a table on a worksheet. |
| PATCH | v1.0/me/drive/items/{id}/workbook/tables/{id} | write | tables | Update a table: name, style, header/total row options. |
| DELETE | v1.0/me/drive/items/{id}/workbook/tables/{id} | write | tables | Delete a table. |
| POST | v1.0/me/drive/items/{id}/workbook/tables/{id}/rows | write | tables | Add rows to a table. |
| POST | v1.0/me/drive/items/{id}/workbook/tables/{id}/rows/add | write | tables | Add rows to a table. |
| PATCH | v1.0/me/drive/items/{id}/workbook/tables/{id}/rows/{id} | write | tables | Update a table row. |
| DELETE | v1.0/me/drive/items/{id}/workbook/tables/{id}/rows/{id} | write | tables | Delete a table row. |
| POST | v1.0/me/drive/items/{id}/workbook/tables/{id}/columns | write | tables | Add a column to a table. |
| POST | v1.0/me/drive/items/{id}/workbook/tables/{id}/columns/add | write | tables | Add a column to a table. |
| PATCH | v1.0/me/drive/items/{id}/workbook/tables/{id}/columns/{id} | write | tables | Update a table column. |
| DELETE | v1.0/me/drive/items/{id}/workbook/tables/{id}/columns/{id} | write | tables | Delete a table column. |
| POST | v1.0/me/drive/items/{id}/workbook/tables/{id}/columns/{id}/filter/{id} | write | tables | Apply or clear a column filter (apply, applyValuesFilter, applyCustomFilter, clear, ...). |
| POST | v1.0/me/drive/items/{id}/workbook/tables/{id}/convertToRange | write | tables | Convert a table back to a plain range. |
| POST | v1.0/me/drive/items/{id}/workbook/tables/{id}/clearFilters | write | tables | Clear all filters on a table. |
| POST | v1.0/me/drive/items/{id}/workbook/tables/{id}/reapplyFilters | write | tables | Reapply the filters on a table. |
| POST | v1.0/me/drive/items/{id}/workbook/tables/{id}/sort/apply | write | tables | Sort a table. |
| POST | v1.0/me/drive/items/{id}/workbook/tables/{id}/sort/clear | write | tables | Clear a table's sort. |
| POST | v1.0/me/drive/items/{id}/workbook/tables/{id}/sort/reapply | write | tables | Reapply a table's sort. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts | read | charts | List the charts on a worksheet. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id} | read | charts | Get a chart. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/image | read | charts | Render a chart as a base64 image. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/{id} | read | charts | Get a chart part or image: image(width=640), axes, dataLabels, legend, title, format, series. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/series/{id} | read | charts | Get a chart series. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/series/{id}/points | read | charts | List the points of a chart series. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/add | write | charts | Create a chart. |
| PATCH | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id} | write | charts | Update a chart: name, size, position. |
| DELETE | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id} | write | charts | Delete a chart. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/setData | write | charts | Reset a chart's source data. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/setPosition | write | charts | Position a chart relative to cells. |
| PATCH | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/{id} | write | charts | Update a chart part: title, legend, dataLabels, axes. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/series | write | charts | Add a series to a chart. |
| PATCH | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/charts/{id}/series/{id} | write | charts | Update a chart series. |
| GET | v1.0/me/drive/items/{id}/workbook/names | read | names | List the named items in a workbook. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/names | read | names | List the named items scoped to a worksheet. |
| GET | v1.0/me/drive/items/{id}/workbook/names/{id} | read | names | Get a named item. |
| GET | v1.0/me/drive/items/{id}/workbook/names/{id}/range | read | names | Get the range a named item refers to. |
| POST | v1.0/me/drive/items/{id}/workbook/names/add | write | names | Add a named item. |
| POST | v1.0/me/drive/items/{id}/workbook/names/addFormulaLocal | write | names | Add a named item using a locale-specific formula. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/names/add | write | names | Add a worksheet-scoped named item. |
| PATCH | v1.0/me/drive/items/{id}/workbook/names/{id} | write | names | Update a named item. |
| DELETE | v1.0/me/drive/items/{id}/workbook/names/{id} | write | names | Delete a named item. |
| GET | v1.0/me/drive/items/{id}/workbook/comments | read | comments | List workbook comments. |
| GET | v1.0/me/drive/items/{id}/workbook/comments/{id} | read | comments | Get a workbook comment. |
| GET | v1.0/me/drive/items/{id}/workbook/comments/{id}/replies | read | comments | List the replies to a comment. |
| GET | v1.0/me/drive/items/{id}/workbook/comments/{id}/replies/{id} | read | comments | Get a comment reply. |
| POST | v1.0/me/drive/items/{id}/workbook/comments | write | comments | Add a workbook comment. |
| POST | v1.0/me/drive/items/{id}/workbook/comments/{id}/replies | write | comments | Reply to a workbook comment. |
| PATCH | v1.0/me/drive/items/{id}/workbook/comments/{id} | write | comments | Update a workbook comment. |
| DELETE | v1.0/me/drive/items/{id}/workbook/comments/{id} | write | comments | Delete a workbook comment. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/pivotTables | read | pivot tables | List the pivot tables on a worksheet. |
| GET | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/pivotTables/{id} | read | pivot tables | Get a pivot table. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/pivotTables/{id}/refresh | write | pivot tables | Refresh a pivot table. |
| POST | v1.0/me/drive/items/{id}/workbook/worksheets/{id}/pivotTables/refreshAll | write | pivot tables | Refresh all pivot tables on a worksheet. |
| GET | `v1.0/me/drive/**` | read | drive trees | Any GET under the signed-in user's drive, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/me/drive/**` | write | drive trees | Any other POST under the signed-in user's drive, including root:/path: addressed forms. |
| PUT | `v1.0/me/drive/**` | write | drive trees | Any other PUT under the signed-in user's drive, including root:/path: addressed forms. |
| PATCH | `v1.0/me/drive/**` | write | drive trees | Any other PATCH under the signed-in user's drive, including root:/path: addressed forms. |
| DELETE | `v1.0/me/drive/**` | write | drive trees | Any other DELETE under the signed-in user's drive, including root:/path: addressed forms. |
| GET | `v1.0/me/drives/**` | read | drive trees | Any GET under the signed-in user's drives, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/me/drives/**` | write | drive trees | Any other POST under the signed-in user's drives, including root:/path: addressed forms. |
| PUT | `v1.0/me/drives/**` | write | drive trees | Any other PUT under the signed-in user's drives, including root:/path: addressed forms. |
| PATCH | `v1.0/me/drives/**` | write | drive trees | Any other PATCH under the signed-in user's drives, including root:/path: addressed forms. |
| DELETE | `v1.0/me/drives/**` | write | drive trees | Any other DELETE under the signed-in user's drives, including root:/path: addressed forms. |
| GET | `v1.0/drives/**` | read | drive trees | Any GET under drives addressed by ID, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/drives/**` | write | drive trees | Any other POST under drives addressed by ID, including root:/path: addressed forms. |
| PUT | `v1.0/drives/**` | write | drive trees | Any other PUT under drives addressed by ID, including root:/path: addressed forms. |
| PATCH | `v1.0/drives/**` | write | drive trees | Any other PATCH under drives addressed by ID, including root:/path: addressed forms. |
| DELETE | `v1.0/drives/**` | write | drive trees | Any other DELETE under drives addressed by ID, including root:/path: addressed forms. |
| GET | `v1.0/users/{id}/drive/**` | read | drive trees | Any GET under a user's drive, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/users/{id}/drive/**` | write | drive trees | Any other POST under a user's drive, including root:/path: addressed forms. |
| PUT | `v1.0/users/{id}/drive/**` | write | drive trees | Any other PUT under a user's drive, including root:/path: addressed forms. |
| PATCH | `v1.0/users/{id}/drive/**` | write | drive trees | Any other PATCH under a user's drive, including root:/path: addressed forms. |
| DELETE | `v1.0/users/{id}/drive/**` | write | drive trees | Any other DELETE under a user's drive, including root:/path: addressed forms. |
| GET | `v1.0/users/{id}/drives/**` | read | drive trees | Any GET under a user's drives, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/users/{id}/drives/**` | write | drive trees | Any other POST under a user's drives, including root:/path: addressed forms. |
| PUT | `v1.0/users/{id}/drives/**` | write | drive trees | Any other PUT under a user's drives, including root:/path: addressed forms. |
| PATCH | `v1.0/users/{id}/drives/**` | write | drive trees | Any other PATCH under a user's drives, including root:/path: addressed forms. |
| DELETE | `v1.0/users/{id}/drives/**` | write | drive trees | Any other DELETE under a user's drives, including root:/path: addressed forms. |
| GET | `v1.0/groups/{id}/drive/**` | read | drive trees | Any GET under a group's drive, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/groups/{id}/drive/**` | write | drive trees | Any other POST under a group's drive, including root:/path: addressed forms. |
| PUT | `v1.0/groups/{id}/drive/**` | write | drive trees | Any other PUT under a group's drive, including root:/path: addressed forms. |
| PATCH | `v1.0/groups/{id}/drive/**` | write | drive trees | Any other PATCH under a group's drive, including root:/path: addressed forms. |
| DELETE | `v1.0/groups/{id}/drive/**` | write | drive trees | Any other DELETE under a group's drive, including root:/path: addressed forms. |
| GET | `v1.0/groups/{id}/drives/**` | read | drive trees | Any GET under a group's drives, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/groups/{id}/drives/**` | write | drive trees | Any other POST under a group's drives, including root:/path: addressed forms. |
| PUT | `v1.0/groups/{id}/drives/**` | write | drive trees | Any other PUT under a group's drives, including root:/path: addressed forms. |
| PATCH | `v1.0/groups/{id}/drives/**` | write | drive trees | Any other PATCH under a group's drives, including root:/path: addressed forms. |
| DELETE | `v1.0/groups/{id}/drives/**` | write | drive trees | Any other DELETE under a group's drives, including root:/path: addressed forms. |
| GET | `v1.0/sites/{id}/drive/**` | read | drive trees | Any GET under a site's default document library, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/sites/{id}/drive/**` | write | drive trees | Any other POST under a site's default document library, including root:/path: addressed forms. |
| PUT | `v1.0/sites/{id}/drive/**` | write | drive trees | Any other PUT under a site's default document library, including root:/path: addressed forms. |
| PATCH | `v1.0/sites/{id}/drive/**` | write | drive trees | Any other PATCH under a site's default document library, including root:/path: addressed forms. |
| DELETE | `v1.0/sites/{id}/drive/**` | write | drive trees | Any other DELETE under a site's default document library, including root:/path: addressed forms. |
| GET | `v1.0/sites/{id}/drives/**` | read | drive trees | Any GET under a site's document libraries, including function segments and root:/path: addressing (all reads). |
| POST | `v1.0/sites/{id}/drives/**` | write | drive trees | Any other POST under a site's document libraries, including root:/path: addressed forms. |
| PUT | `v1.0/sites/{id}/drives/**` | write | drive trees | Any other PUT under a site's document libraries, including root:/path: addressed forms. |
| PATCH | `v1.0/sites/{id}/drives/**` | write | drive trees | Any other PATCH under a site's document libraries, including root:/path: addressed forms. |
| DELETE | `v1.0/sites/{id}/drives/**` | write | drive trees | Any other DELETE under a site's document libraries, including root:/path: addressed forms. |
| POST | v1.0/$batch | write | batch | JSON batch of up to 20 Graph requests; can carry writes. |

# informat.textindex Search Engine Operations

## Overview
Use `informat.textindex` to perform search engine related operations.

## search 
Search by keywords

```javascript
informat.textindex.search(moduleId, query)
```

| Parameter     | Type     | Description                                                          |
|--------|--------|-------------------------------------------------------------|
| moduleId    | `String` | Search engine module identifier                                                  |
| query | [TextindexSearchQuery](/guide/script/model.md#textindexsearchquery) | Search criteria |

***Return Value*** 
Search results, type is [TextindexSearchResult](/guide/script/model.md#textindexsearchresult)

***

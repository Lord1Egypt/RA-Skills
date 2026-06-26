# StdReport Component Selection

## Decision tree

- Need complete report page (filter + table + persistence):
  - `useStandardReport` + `CStandardPage`
- Need only table surface inside custom page:
  - `CTable` directly
- Need only filter bar with custom table orchestration:
  - `CSmartFilter` + custom state + `CTable`

## First choice defaults

- Start with `useStandardReport` + `CStandardPage mode="integrated"`.
- Move to table-only only if layout is highly custom.

## Identity requirements

- `metadata.id` is required in `useStandardReport`.
- `appId` is required in standalone `CTable`/`CSmartFilter` for layout/variant isolation.
- Use `tableKey` when one page contains multiple tables.

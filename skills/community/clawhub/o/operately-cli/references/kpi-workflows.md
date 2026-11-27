# KPI Workflows

KPIs track recurring numeric values in a space. Use goals for time-bound outcomes and KPIs for ongoing measurements.

Use `operately kpis --help` to list KPI commands, or command-specific help to check their flags.

## Create and Read

```bash
operately kpis list_kpis --space-id s1

operately kpis create_kpi \
  --space-id s1 \
  --name "Monthly website visitors" \
  --unit visitors \
  --cadence monthly \
  --champion-id u1

operately kpis get_kpi --kpi-id k1
```

Cadence is `weekly` or `monthly`. `get_kpi` includes logged entries; use their IDs when correcting or deleting values. Use `edit_kpi` to change the name, unit, cadence, champion, or description.

## Log and Correct Values

```bash
operately kpis log_kpi_entry --kpi-id k1 --value 13000 --period 2026-09-01

# Correct an existing entry rather than logging a replacement
operately kpis edit_kpi_entry --entry-id e1 --value 13500

# Correct its date if necessary
operately kpis edit_kpi_entry --entry-id e1 --period 2026-09-02

# Remove an incorrect entry
operately kpis delete_kpi_entry --entry-id e1
```

`--period` is a date in `YYYY-MM-DD` format. Editing retains the previous values in the entry's history. Deleting an entry removes that logged value; `delete_kpi --kpi-id k1` deletes the whole KPI.

## Annotate the Chart

```bash
operately kpis add_kpi_annotation --kpi-id k1 --date 2026-09-15 --title "New website launched"
operately kpis edit_kpi_annotation --annotation-id a1 --title "Website launch completed"
operately kpis delete_kpi_annotation --annotation-id a1
```

Annotations explain events on the chart; they do not change logged values.

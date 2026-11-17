# Evidence - nav-labels-proof

## Build Summary

The demo fixture contains `examples/demo-repo/nav_labels.json` and a real check command at `examples/demo-repo/check_nav_labels.py`.

## Checks Run

```bash
python3 examples/demo-repo/check_nav_labels.py examples/demo-repo/nav_labels.json
```

Result:

```text
NAV_LABEL_CHECK_PASS
```

## AC1 - PASS

The JSON file contains the expected English labels: Home, Settings, Billing.

## AC2 - PASS

The JSON file contains the expected German labels: Startseite, Einstellungen, Abrechnung.

## AC3 - PASS

The check script compares the file against an expected dictionary and exits with status `1` when values differ.

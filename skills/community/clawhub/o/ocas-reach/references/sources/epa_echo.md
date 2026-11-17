# epa_echo — EPA Enforcement & Compliance History Online

## What this source has

The EPA's ECHO (Enforcement and Compliance History Online) API provides compliance and enforcement data for US facilities regulated under environmental laws (Clean Air Act, Clean Water Act, RCRA, etc.). Data includes:

- Facility compliance status and violation history
- Enforcement actions (penalties, inspections)
- Pollutant discharge monitoring (effluent data from NPDES permits)
- Permit status and details

Use ECHO for: environmental due diligence on properties or companies, checking facility compliance records, researching pollutant discharges near a location, and regulatory risk assessment.

## Auth

| | |
|---|---|
| Required | none |
| Account | not needed |

Free, no key required. Some advanced features may require registration.

## Limits

| | |
|---|---|
| Daily | — |
| Monthly | — |
| Rate | throttle to <2/sec |

## Actions

| Action | Purpose | Required params |
|---|---|---|
| `facility_search` | Search facilities by name, location, or permit | `output`, plus search params |
| `compliance_report` | Get compliance summary for a facility | `output`, `p_id` (facility ID) |
| `effluent_chart` | Get effluent discharge data for a facility | `output`, `p_id` |

## Worked examples

```bash
# Search for facilities in a ZIP code
python3 scripts/reach.py query epa_echo facility_search '{"output": "JSON", "p_zip": "94102", "p_cty": "SAN FRANCISCO"}'

# Get compliance report for a facility (by permit ID)
python3 scripts/reach.py query epa_echo compliance_report '{"output": "JSON", "p_id": "CA0000001"}'

# Get effluent discharge chart data
python3 scripts/reach.py query epa_echo effluent_chart '{"output": "JSON", "p_id": "CA0000001"}'
```

## Response shape

All actions return JSON with an `Results` key containing the data:

```json
{
  "Results": {
    "Message": "Success",
    "QueryID": "...",
    "QueryRows": "10",
    "Facilities": [...]
  }
}
```

Facility objects include fields like `RegistryId`, `FacilityName`, `Address`, `City`, `State`, `Zip`, `Latitude`, `Longitude`, `ComplianceStatus`.

## Pitfalls

- **Facility IDs are required for detail searches.** Use `facility_search` first to find `p_id` values, then pass them to `compliance_report` or `effluent_chart`.
- **Search parameters are case-sensitive for some fields.** State codes should be uppercase (`CA`, not `ca`).
- **Result limits.** Large result sets may be truncated. Use geographic filters to narrow scope.
- **Data freshness.** Compliance data is updated weekly, not real-time.
- **Effluent data requires NPDES permit.** Only facilities with Clean Water Act discharge permits have effluent charts.

## Source links

- ECHO docs: https://echo.epa.gov/tools/web-services
- REST services: https://echodata.epa.gov/echo/echo_rest_services.html
- Facility search: https://echo.epa.gov/facility-search

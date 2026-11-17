# Multi-Step Workflows (MSP Recipes)

These combine endpoints from the other reference files. Safety tiers apply
per step; for a whole workflow, confirm once with a plan summary, then
re-confirm individually only for Tier-3 steps.

## 1. Stale-device report (CSV)

1. `devices.md` 1.1 with `$filter=lastSyncDateTime lt {cutoff}` and
   `$select=deviceName,operatingSystem,lastSyncDateTime,userPrincipalName,serialNumber`.
2. Sort by `lastSyncDateTime` ascending.
3. Present as table; on request write a CSV file (semicolon separator for
   German Excel locales).
4. Offer follow-ups: sync all (Tier 1, batch) or retire (Tier 3, per device).

## 2. Compliance overview per platform

1. `reporting.md` 1.1 + 1.2 (one call with
   `$select=operatingSystem,complianceState` suffices).
2. Pivot client-side: rows = OS, columns = compliant / non-compliant / grace.
3. For non-compliant devices, optionally fetch details (`reporting.md` 1.4)
   and group by failure reason via
   `/deviceManagement/deviceCompliancePolicies/{id}/deviceStatuses`.

## 3. Device onboarding check

Given a device (or serial):

1. Autopilot registered? `platform.md` 1.1 filter by serial.
2. Enrolled in Intune? `devices.md` 1.2.
3. Compliance state + assigned policies: `devices.md` 1.4, then
   `policies.md` 1.3 / 2.5 for group-based assignments of the user's groups.
4. Expected apps installed? `apps.md` 1.3 vs. detected apps 1.7/1.8.
5. Report gaps as a checklist.

## 4. Device / user offboarding

Plan first, show the full plan, then execute step by step:

1. Find all devices of the user: `admin.md` 1.8.
2. Per device: **Retire** (company data only) or **Wipe** (full reset) —
   ask which one; both Tier 3 (type back device name).
3. Delete Autopilot identity if the hardware leaves the company:
   `platform.md` 1.5 (Tier 3).
4. Remove user from Intune-relevant groups: `admin.md` 1.7 (Tier 2).
5. Verify: device list of user is empty; report what was done.

## 5. Policy change review ("Wer hat was geändert?")

1. `reporting.md` 2.2 with the requested date range.
2. Group by actor, then by category.
3. For suspicious entries fetch details (`reporting.md` 2.4) and, where a
   policy still exists, its current state from `policies.md`.

## 6. APNS / VPP / token health check (offer when Apple topics come up — run only on user request)

1. Ask first ("Soll ich kurz APNS/VPP-Zertifikate prüfen?"), then `platform.md` 3.3 (APNS) and 3.4 (VPP).
2. Warn on anything expiring within 30 days — an expired APNS certificate
   breaks all Apple device management tenant-wide.

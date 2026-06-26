---
name: parcelcli
description: Track parcels locally with parcelcli for Evri, Royal Mail, UPS, FedEx, and DHL. Use when the user asks to track a package, detect a carrier, check delivery status, watch a parcel, or summarize courier tracking without sending tracking data to third-party aggregators.
homepage: https://github.com/cavit99/parcelcli
metadata: {"openclaw":{"requires":{"bins":["parcelcli"]},"homepage":"https://github.com/cavit99/parcelcli","install":[{"id":"go","kind":"go","module":"github.com/cavit99/parcelcli/cmd/parcelcli@v1.0.3","bins":["parcelcli"],"label":"Install parcelcli (go)"}]}}
---

# parcelcli

Use `parcelcli` for local parcel tracking. It drives public carrier tracking pages and returns a normalized JSON shape.

## Golden Path

Always use `--json` when calling `parcelcli`.

```sh
parcelcli track <tracking-number> --carrier evri --postcode <postcode> --json
parcelcli track <tracking-number> --carrier evri --json
parcelcli track <tracking-number> --carrier royalmail --json
parcelcli track <tracking-number> --carrier ups --json
parcelcli track <tracking-number> --carrier fedex --json
parcelcli track <tracking-number> --carrier dhl --json
```

If the carrier is unknown, run:

```sh
parcelcli detect <tracking-number> --json
```

If detection is ambiguous, ask the user to choose a carrier.

## Required Inputs

- Evri can run rough public tracking without `--postcode`; use `--postcode` only when the user wants fuller address-specific detail or provides it.
- Royal Mail, UPS, FedEx, and DHL do not require postcode by default.
- Do not infer a postcode from memory unless the user clearly asks you to use their usual address.

## Output Handling

Summarize only the normalized JSON fields. Prefer:

- `status`
- `status_text`
- `last_event`
- ETA or delivery fields when present
- blocker/error state when present

Do not paste raw carrier page text or browser dumps into chat.

## Watches

Use local watch state when the user asks to monitor a parcel:

```sh
parcelcli watch add <tracking-number> --carrier evri --postcode <postcode> --label "<label>"
parcelcli watch add <tracking-number> --carrier evri --label "<label>"
parcelcli watch add <tracking-number> --carrier royalmail --label "<label>"
parcelcli watch add <tracking-number> --carrier ups --label "<label>"
parcelcli watch add <tracking-number> --carrier fedex --label "<label>"
parcelcli watch add <tracking-number> --carrier dhl --label "<label>"
parcelcli watch run --json
```

Do not poll fast. Use 15-30 minute intervals for active delivery watches and longer intervals for non-active parcels.

Notify only on material changes: status enum, latest event, ETA, courier or handover code, delivery, exception, or blocker.

When monitoring is no longer needed, list and remove old watches with `parcelcli watch list --json` and `parcelcli watch remove <id> --json`.

## Privacy And Errors

Keep tracking numbers, postcodes, and watch state local. Do not use third-party aggregators unless the user explicitly approves that.

If Chrome is missing, say Chrome is required or use the CLI's `--chrome` flag if the user provides a path.

If a carrier returns `unsupported` or `credentials_required`, say that plainly and stop. For timeout or WAF failures, retry once later rather than looping.

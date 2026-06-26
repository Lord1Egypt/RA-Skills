# API Notes

## Verified working scope
- Cloud login works with `midea-local==6.6.0`.
- Device enumeration works.
- Power on/off works through `/v1/appliance/operation/togglePower/<device_id>`.

## Important routing note
- The validated route is the Meiju / Midea cloud route selected by `MideaCloud.get_cloud_servers()` and then passed to `get_midea_cloud(...)`.
- Earlier experiments using `NetHome Plus` directly were unstable.

## Known limitations
- Real-time state reads are not part of this skill.
- Temperature setting is not part of this skill.
- Some successful cloud write calls may print `null` via the library wrapper; treat physical device behavior as the source of truth.

## Local config file
This skill stores credentials and cached device metadata in:
- `~/.openclaw/midea-cloud-control/config.json`

Users should be told explicitly before saving credentials.

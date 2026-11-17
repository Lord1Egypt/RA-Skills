# IAM Policies — huawei-cloud-rms-list

Least-privilege, **read-only** policy for querying the RMS resource inventory.

## Required permissions

The RMS resource-inventory APIs require the `rms:resources:list` permission
(the service rejects unauthorized calls with `RMS.00010006` /
`"You are not authorized with rms:resources:list"`). Tag-based views additionally
use `rms::listTags` and `rms::listResourcesByTag`.

Action names below were **verified** via the KooCLI authorization schema query
and the live service error message (no names are invented):

```bash
hcloud IAM GetAuthorizationSchemaV5 --service_code=rms --cli-region=cn-north-4
```

- `rms:resources:list` — list resources (ListAllResources / ListResources)
- `rms::listTags` — list the tags of all resources
- `rms::listResourcesByTag` — list or count resources by tag

`ListProviders` and `ListRegions` return the static RMS provider / region
catalog; they are covered by the same read-only grant (they add no write
capability).

## IAM 5.0 identity policy (recommended)

```json
{
  "Version": "5.0",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "rms:resources:list",
        "rms::listTags",
        "rms::listResourcesByTag"
      ]
    }
  ]
}
```

## Notes

- This skill performs **no** write operations, so no `rms:*:create` /
  `rms:*:delete` / `rms:*:update` action is needed — and the script additionally
  refuses to construct any mutating call.
- Scope the policy to the target account/region as required by your landing
  zone.
- Assign the policy to the IAM user / agency whose AK/SK the hcloud profile or
  the SDK environment uses. Never paste AK/SK into chat or command lines.

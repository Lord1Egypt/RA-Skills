# IAM Policies — huawei-cloud-asm-fuzzy-list

## Least-Privilege Policy

The `huawei-cloud-asm-fuzzy-list` skill is **read-only**. The minimum permission
needed to list ASM meshes is the ASM mesh list action. The recommended
least-privilege IAM policy is:

```json
{
  "Version": "1.1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "asm:mesh:list"
      ],
      "Resource": [
        "*"
      ]
    }
  ]
}
```

## Notes

- Only the `list` action is granted — no `create`, `update`, `delete` or other
  mutation actions.
- `asm:mesh:list` covers the ASM list API (`GET /v1/{project_id}/meshes`,
  SDK `AsmClient.list_meshes`).
- ASM only supports the mesh list in the region where the tenant owns meshes;
  pass the matching region via `AsmRegion.value_of(...)`.
- If a managed role is preferred over a custom policy, use the Huawei Cloud
  pre-defined role that grants read-only access to ASM (e.g. the built-in
  ASM read-only role), which includes the mesh list permission.

## Scope Note

This skill covers **ASM mesh listing** only (with client-side fuzzy name
matching). It never lists, inspects or modifies mesh sub-resources such as
services, virtual services, destination rules or gateways.

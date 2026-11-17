# Kingdee contract lookup and proxy requests

For Kingdee Galaxy Enterprise (金蝶星空企业版). Read after selecting an object/operation from the bundled index. Foundation actions remain the preferred route when they cover the operation.

## Official documentation lookup

Use `apiInfoId` from the chosen index entry as an opaque string. Base URL: `https://openapi.open.kingdee.com/mscdp/apicenter`.

| Read            | GET path                                           | Purpose                                                                  |
| --------------- | -------------------------------------------------- | ------------------------------------------------------------------------ |
| Detail          | `/apiinfo/detail/{apiInfoId}`                      | Verify `formName`, `name`, `formId`, `number`, version and dedicated URL |
| Request fields  | `/apiinfoparam/apiinfo/{apiInfoId}/paramfield/req` | Construct the input                                                      |
| Response fields | `/apiinfoparam/apiinfo/{apiInfoId}/paramfield/res` | Interpret an unfamiliar result                                           |
| Examples        | `/apiinfoparam/apiinfo/{apiInfoId}/paramjson`      | Inspect request/response shapes when needed                              |

These are documentation endpoints, not enterprise execution endpoints. Read them with a public HTTP tool or curl without Cookie, Authorization or application credentials. Check both HTTP status and the JSON `result` flag. Fields are in `dataList`; examples are in `data.requestJson` and `data.responseJson` and may themselves be JSON strings.

Walk parameter-tree `children` recursively, keeping full paths and case. Interpret `isMust`, `fieldType`, `defaultValue` and `description` together: conditional requirements and example strings such as `"false"` are not unconditional defaults. An empty response-field tree does not prove an empty business response; consult the example.

For example, the index's 应收调汇单 / 单据查询 entry is `915999846569789445`. Its detail identifies `AR_AdjustExchangeRate` and `ExecuteBillQuery`. This operation is covered by `query_records`; proxy is unnecessary for normal querying.

Do not enumerate IDs or request the full catalog. The full `/apitree` endpoint required authentication in the source investigation; the bundled index avoids that dependency. On 401/403, do not try enterprise secrets against the documentation site. On 429, honor Retry-After and stop unbounded retries. Cache already retrieved ID/version documents within the task.

## Request envelope

Use `oo connector proxy "kingdee" --data @proxy-request.json --json`. The file is:

```json
{
  "endpoint": "/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.ExecuteBillQuery.common.kdsvc",
  "method": "POST",
  "body": {
    "data": "{\"FormId\":\"AR_AdjustExchangeRate\",\"FieldKeys\":\"FID,FBillNo\",\"StartRow\":0,\"Limit\":20}"
  }
}
```

This query illustrates the special envelope only; prefer its foundation action. `endpoint` is relative to the connected application root. If that root already includes `/k3cloud`, do not repeat it. Connector selects the enterprise host and supplies authentication. Never provide Cookie, Authorization, KDSVCSessionId, SessionId or kdservice-sessionid headers.

For object `body`, the CLI/Connector serializes the outer JSON. In the named-parameter format, **`body.data` is the business object serialized once to a JSON string**. Build nested payloads with a JSON serializer and save them to a file instead of hand-escaping shell text. If using raw JSON text as `body`, set `headers.content-type` to `application/json`.

## Select the documented route

Let `formId` and operation `number` come from the verified detail. A method's presence below does not mean every form supports it; the object must list that operation.

| Family            | Method path                          | Outer body                                                                          |
| ----------------- | ------------------------------------ | ----------------------------------------------------------------------------------- |
| Standard          | `DynamicFormService.<method>`        | `{ "formid": formId, "data": serializedBusinessData }`                              |
| Special           | `DynamicFormService.<method>`        | `{ "data": serializedBusinessData }`                                                |
| General operation | `DynamicFormService.ExcuteOperation` | `{ "formid": formId, "opNumber": operationNumber, "data": serializedBusinessData }` |

All paths above start with `/Kingdee.BOS.WebApi.ServicesStub.` and end with `.common.kdsvc`. Use POST with JSON. The standard envelope's outer key is lowercase **`formid`**. Query's **`FormId`** is inside the serialized business data. The general method is spelled **`ExcuteOperation`**.

- Standard methods: `View`, `Save`, `BatchSave`, `Delete`, `Submit`, `Audit`, `UnAudit`, `Push`, `Draft`, `Allocate`, `FlexSave`, `GroupSave`, `Disassembly`, `CancelAllocate`, `CancelAssign`, `GetSysReportData`.
- Special methods: `ExecuteBillQuery`, `WorkflowAudit`, `SendMsg`, `QueryBusinessInfo`, `QueryGroupInfo`, `GroupDelete`, `SwitchOrg`, `AttachmentUpLoad`, `AttachmentDownLoad`. Check each operation's own fields. This routing list does not supply an attachment workflow or establish that a large binary payload fits proxy limits.
- General operations: use `ExcuteOperation` only after verifying the operation's ordinary/general classification and parameters. For a documented operation such as PLM `OpCheckIn`, `opNumber` is that exact code, not the Chinese label or apiInfoId.
- `Define` or custom services: inspect the dedicated URL and contract. Do not force them into `ExcuteOperation` or append their number as a method name. Current Kingdee proxy accepts business `.common.kdsvc` endpoints directly under the connected application root; AuthService endpoints, cross-origin targets and redirects are rejected. Report unsupported routes instead of bypassing the connector.

Some official SDKs show a positional `parameters` array. This is an alternative envelope, not an extra field to combine with `formid/data/opNumber`. Use the named form above for its documented routes; follow a custom service's verified contract when it explicitly requires positional parameters.

## Interpret the result

The CLI proxy envelope is `{ "data": { "status": ..., "headers": ..., "data": ... }, "meta": { "executionId": ... } }`. Read HTTP status from `response.data.status`, the Kingdee payload from `response.data.data`, and the trace ID from `response.meta.executionId`. This envelope is based on the connector/CLI contract; no real enterprise request was used during skill authoring.

| Kingdee payload                  | Interpretation                                                                                                     |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Ordinary business result         | Check `Result.ResponseStatus.IsSuccess`; inspect `Errors`, error codes and messages                                |
| Report result                    | Check its documented status, commonly `Result.IsSuccess`; preserve Rows/RowCount only if returned                  |
| Query two-dimensional array      | Match columns to FieldKeys order; nested objects with `IsSuccess=false` are errors, not records                    |
| Batch result                     | Inspect both errors and `SuccessEntitys`; report partial completion with exact known successful/failed identifiers |
| Text beginning `response_error:` | Treat as failure, including when encoded as a JSON string                                                          |
| Unknown shape                    | Inspect the selected operation's response fields/example before declaring success                                  |

Connector transport success and HTTP 200 are not business success. Upstream 4xx/5xx may appear inside the CLI data envelope. Do not manufacture totals, next-page flags or record IDs. Queries that include entries can produce several rows per bill.

After a timeout, disconnect or partial failure, reconcile record state before another write. Every connector call logs in independently, so a prior `SwitchOrg` does not affect a later call; use documented organization parameters where available. Do not infer multi-call stateful workflow support.

## Evidence and scope

The index is the 2026-09-15 official Enterprise navigation snapshot (16 domains, 69 modules, 1,076 rows, 7,881 unique operation IDs). Fields and version-specific behavior must still be read live; no exhaustive per-operation detail download is included.

The named envelopes and route groups were checked against the [official online-test frontend](https://openapi.open.kingdee.com/js/chunk-6b5084c4.c6dd8c8d.js) and the SDK bundle linked from the [official authorization/SDK page](https://open.kingdee.com/K3Cloud/Open/ApiCenterReportDetail.aspx). Official documentation samples were read for queries, save, view, allocation and reports. Real enterprise login, gateway requirements, permissions, multi-organization behavior and writes remain tenant-specific verification work.

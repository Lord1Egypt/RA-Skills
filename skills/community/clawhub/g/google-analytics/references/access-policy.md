# Google Analytics Admin access policy

An access policy limits which endpoints Google Analytics Admin connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-analytics#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Google Analytics Admin: its 22 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create google-analytics-admin --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1beta/accountSummaries"},
    {"method": "GET", "path": "v1beta/accounts"},
    {"method": "GET", "path": "v1beta/accounts/{id}"},
    {"method": "GET", "path": "v1beta/accounts/{id}/dataSharingSettings"},
    {"method": "POST", "path": "v1beta/accounts/{id}:runAccessReport"},
    {"method": "POST", "path": "v1beta/accounts/{id}:searchChangeHistoryEvents"},
    {"method": "GET", "path": "v1beta/properties/{id}/conversionEvents"},
    {"method": "GET", "path": "v1beta/properties/{id}/conversionEvents/{id}"},
    {"method": "GET", "path": "v1beta/properties/{id}/customDimensions"},
    {"method": "GET", "path": "v1beta/properties/{id}/customDimensions/{id}"},
    {"method": "GET", "path": "v1beta/properties/{id}/customMetrics"},
    {"method": "GET", "path": "v1beta/properties/{id}/customMetrics/{id}"},
    {"method": "GET", "path": "v1beta/properties/{id}/dataStreams"},
    {"method": "GET", "path": "v1beta/properties/{id}/dataStreams/{id}"},
    {"method": "GET", "path": "v1beta/properties/{id}/firebaseLinks"},
    {"method": "GET", "path": "v1beta/properties/{id}/googleAdsLinks"},
    {"method": "GET", "path": "v1beta/properties/{id}/keyEvents"},
    {"method": "GET", "path": "v1beta/properties/{id}/keyEvents/{id}"},
    {"method": "GET", "path": "v1beta/properties"},
    {"method": "GET", "path": "v1beta/properties/{id}"},
    {"method": "GET", "path": "v1beta/properties/{id}/dataRetentionSettings"},
    {"method": "POST", "path": "v1beta/properties/{id}:runAccessReport"}
  ],
  "deny": []
}
```

## Endpoints

The Google Analytics Admin endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1beta/accountSummaries | read | accountSummaries | Returns summaries of all accounts accessible by the caller. |
| GET | v1beta/accounts | read | accounts | Returns all accounts accessible by the caller. |
| GET | v1beta/accounts/{id} | read | accounts | Lookup for a single Account. |
| PATCH | v1beta/accounts/{id} | write | accounts | Updates an account. |
| DELETE | v1beta/accounts/{id} | write | accounts | Marks target Account as soft-deleted (ie: "trashed") and returns it. |
| GET | v1beta/accounts/{id}/dataSharingSettings | read | accounts | Get data sharing settings on an account. |
| POST | v1beta/accounts/{id}:runAccessReport | read | accounts | Returns a customized report of data access records. |
| POST | v1beta/accounts/{id}:searchChangeHistoryEvents | read | accounts | Searches through all changes to an account or its children given the specified set of filters. |
| POST | v1beta/accounts:provisionAccountTicket | write | accounts | Requests a ticket for creating an account. |
| GET | v1beta/properties/{id}/conversionEvents | read | conversionEvents | Deprecated: Use `ListKeyEvents` instead. |
| POST | v1beta/properties/{id}/conversionEvents | write | conversionEvents | Deprecated: Use `CreateKeyEvent` instead. |
| GET | v1beta/properties/{id}/conversionEvents/{id} | read | conversionEvents | Deprecated: Use `GetKeyEvent` instead. |
| PATCH | v1beta/properties/{id}/conversionEvents/{id} | write | conversionEvents | Deprecated: Use `UpdateKeyEvent` instead. |
| DELETE | v1beta/properties/{id}/conversionEvents/{id} | write | conversionEvents | Deprecated: Use `DeleteKeyEvent` instead. |
| GET | v1beta/properties/{id}/customDimensions | read | customDimensions | Lists CustomDimensions on a property. |
| POST | v1beta/properties/{id}/customDimensions | write | customDimensions | Creates a CustomDimension. |
| GET | v1beta/properties/{id}/customDimensions/{id} | read | customDimensions | Lookup for a single CustomDimension. |
| PATCH | v1beta/properties/{id}/customDimensions/{id} | write | customDimensions | Updates a CustomDimension on a property. |
| POST | v1beta/properties/{id}/customDimensions/{id}:archive | write | customDimensions | Archives a CustomDimension on a property. |
| GET | v1beta/properties/{id}/customMetrics | read | customMetrics | Lists CustomMetrics on a property. |
| POST | v1beta/properties/{id}/customMetrics | write | customMetrics | Creates a CustomMetric. |
| GET | v1beta/properties/{id}/customMetrics/{id} | read | customMetrics | Lookup for a single CustomMetric. |
| PATCH | v1beta/properties/{id}/customMetrics/{id} | write | customMetrics | Updates a CustomMetric on a property. |
| POST | v1beta/properties/{id}/customMetrics/{id}:archive | write | customMetrics | Archives a CustomMetric on a property. |
| GET | v1beta/properties/{id}/dataStreams | read | dataStreams | Lists DataStreams on a property. |
| POST | v1beta/properties/{id}/dataStreams | write | dataStreams | Creates a DataStream. |
| GET | v1beta/properties/{id}/dataStreams/{id} | read | dataStreams | Lookup for a single DataStream. |
| PATCH | v1beta/properties/{id}/dataStreams/{id} | write | dataStreams | Updates a DataStream on a property. |
| DELETE | v1beta/properties/{id}/dataStreams/{id} | write | dataStreams | Deletes a DataStream on a property. |
| GET | v1beta/properties/{id}/dataStreams/{id}/measurementProtocolSecrets | write | dataStreams | Returns child MeasurementProtocolSecrets under the specified parent Property. Kept out of read: returns Measurement Protocol API secrets. |
| POST | v1beta/properties/{id}/dataStreams/{id}/measurementProtocolSecrets | write | dataStreams | Creates a measurement protocol secret. |
| GET | v1beta/properties/{id}/dataStreams/{id}/measurementProtocolSecrets/{id} | write | dataStreams | Lookup for a single MeasurementProtocolSecret. Kept out of read: returns a Measurement Protocol API secret. |
| PATCH | v1beta/properties/{id}/dataStreams/{id}/measurementProtocolSecrets/{id} | write | dataStreams | Updates a measurement protocol secret. |
| DELETE | v1beta/properties/{id}/dataStreams/{id}/measurementProtocolSecrets/{id} | write | dataStreams | Deletes target MeasurementProtocolSecret. |
| GET | v1beta/properties/{id}/firebaseLinks | read | firebaseLinks | Lists FirebaseLinks on a property. |
| POST | v1beta/properties/{id}/firebaseLinks | write | firebaseLinks | Creates a FirebaseLink. |
| DELETE | v1beta/properties/{id}/firebaseLinks/{id} | write | firebaseLinks | Deletes a FirebaseLink on a property |
| GET | v1beta/properties/{id}/googleAdsLinks | read | googleAdsLinks | Lists GoogleAdsLinks on a property. |
| POST | v1beta/properties/{id}/googleAdsLinks | write | googleAdsLinks | Creates a GoogleAdsLink. |
| PATCH | v1beta/properties/{id}/googleAdsLinks/{id} | write | googleAdsLinks | Updates a GoogleAdsLink on a property |
| DELETE | v1beta/properties/{id}/googleAdsLinks/{id} | write | googleAdsLinks | Deletes a GoogleAdsLink on a property |
| GET | v1beta/properties/{id}/keyEvents | read | keyEvents | Returns a list of Key Events in the specified parent property. |
| POST | v1beta/properties/{id}/keyEvents | write | keyEvents | Creates a Key Event. |
| GET | v1beta/properties/{id}/keyEvents/{id} | read | keyEvents | Retrieves a single Key Event. |
| PATCH | v1beta/properties/{id}/keyEvents/{id} | write | keyEvents | Updates a Key Event. |
| DELETE | v1beta/properties/{id}/keyEvents/{id} | write | keyEvents | Deletes a Key Event. |
| GET | v1beta/properties | read | properties | Returns child Properties under the specified parent Account. |
| POST | v1beta/properties | write | properties | Creates a Google Analytics property with the specified location and attributes. |
| GET | v1beta/properties/{id} | read | properties | Lookup for a single GA Property. |
| PATCH | v1beta/properties/{id} | write | properties | Updates a property. |
| DELETE | v1beta/properties/{id} | write | properties | Marks target Property as soft-deleted (ie: "trashed") and returns it. |
| GET | v1beta/properties/{id}/dataRetentionSettings | read | properties | Returns the singleton data retention settings for this property. |
| PATCH | v1beta/properties/{id}/dataRetentionSettings | write | properties | Updates the singleton data retention settings for this property. |
| POST | v1beta/properties/{id}:acknowledgeUserDataCollection | write | properties | Acknowledges the terms of user data collection for the specified property. |
| POST | v1beta/properties/{id}:runAccessReport | read | properties | Returns a customized report of data access records. |

# Google Analytics Data access policy

An access policy limits which endpoints Google Analytics Data connections may call through Maton. Change it only when the user asks; see the Connections section of SKILL.md. Also at https://docs.maton.ai/google-analytics#permissions.

## Read-only access policy

The rules the Maton console saves when the user picks **Read** for Google Analytics Data: its 10 read-only endpoints. Endpoints that return credentials, start jobs, or spend credits are left out. Save them as `policy.json` and pass `--access-policy-file policy.json` to `maton connection create` or `maton connection update`; trim or extend them when the user wants narrower or wider access.

```bash
maton connection create google-analytics-data --access-policy-file policy.json
maton connection update {connection_id} --access-policy-file policy.json
```

```json
{
  "allow": [
    {"method": "GET", "path": "v1beta/properties/{id}/audienceExports"},
    {"method": "GET", "path": "v1beta/properties/{id}/audienceExports/{id}"},
    {"method": "POST", "path": "v1beta/properties/{id}/audienceExports/{id}:query"},
    {"method": "GET", "path": "v1beta/properties/{id}/metadata"},
    {"method": "POST", "path": "v1beta/properties/{id}:batchRunPivotReports"},
    {"method": "POST", "path": "v1beta/properties/{id}:batchRunReports"},
    {"method": "POST", "path": "v1beta/properties/{id}:checkCompatibility"},
    {"method": "POST", "path": "v1beta/properties/{id}:runPivotReport"},
    {"method": "POST", "path": "v1beta/properties/{id}:runRealtimeReport"},
    {"method": "POST", "path": "v1beta/properties/{id}:runReport"}
  ],
  "deny": []
}
```

## Endpoints

The Google Analytics Data endpoints Maton has reviewed, each marked read or write, for building custom rules. Paths are relative to the app, as in an access policy; `{id}` matches one path segment.

| Method | Path | Access | Resource | Description |
| --- | --- | --- | --- | --- |
| GET | v1beta/properties/{id}/audienceExports | read | audienceExports | Lists all audience exports for a property. |
| POST | v1beta/properties/{id}/audienceExports | write | audienceExports | Creates an audience export for later retrieval. |
| GET | v1beta/properties/{id}/audienceExports/{id} | read | audienceExports | Gets configuration metadata about a specific audience export. |
| POST | v1beta/properties/{id}/audienceExports/{id}:query | read | audienceExports | Retrieves an audience export of users. |
| GET | v1beta/properties/{id}/metadata | read | properties | Returns metadata for dimensions and metrics available in reporting methods. |
| POST | v1beta/properties/{id}:batchRunPivotReports | read | properties | Returns multiple pivot reports in a batch. |
| POST | v1beta/properties/{id}:batchRunReports | read | properties | Returns multiple reports in a batch. |
| POST | v1beta/properties/{id}:checkCompatibility | read | properties | This compatibility method lists dimensions and metrics that can be added to a report request and maintain compatibility. |
| POST | v1beta/properties/{id}:runPivotReport | read | properties | Returns a customized pivot report of your Google Analytics event data. |
| POST | v1beta/properties/{id}:runRealtimeReport | read | properties | Returns a customized report of realtime event data for your property. |
| POST | v1beta/properties/{id}:runReport | read | properties | Returns a customized report of your Google Analytics event data. |

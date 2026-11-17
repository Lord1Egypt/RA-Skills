# Network Profiles & Windows Updates

Call via `scripts/graph.sh`. Tier = safety tier from SKILL.md.

## 1. Wi-Fi, VPN & certificate profiles

These live in the legacy profile store. Fetch all profiles once and filter
client-side by `@odata.type` — that is more robust than long `isof()` chains:

GET `/deviceManagement/deviceConfigurations` — Tier 0, then filter:

| Profile type | `@odata.type` contains |
|---|---|
| Wi-Fi / WLAN | `WiFi` / `wifi` (e.g. `windowsWifiConfiguration`, `iosWiFiConfiguration`, `androidWorkProfileWiFiConfiguration`) |
| VPN | `Vpn` / `vpn` |
| SCEP certificates | `Scep` |
| PKCS certificates | `Pkcs` |
| Trusted root certs | `TrustedRootCertificate` |

| # | Action | Method & Path | Tier |
|---|---|---|---|
| 1.1 | Profile details | GET `/deviceManagement/deviceConfigurations/{id}` | 0 |
| 1.2 | Profile assignments | GET `/deviceManagement/deviceConfigurations/{id}/assignments` | 0 |

Alternative for Wi-Fi only (server-side):
GET `/deviceManagement/deviceConfigurations?$filter=isof('microsoft.graph.windowsWifiConfiguration') or isof('microsoft.graph.iosWiFiConfiguration') or isof('microsoft.graph.androidWorkProfileWiFiConfiguration')`

## 2. Windows Update management

| # | Action | Method & Path | Tier | Notes |
|---|---|---|---|---|
| 2.1 | List update rings | GET `/deviceManagement/deviceConfigurations?$filter=isof('microsoft.graph.windowsUpdateForBusinessConfiguration')` | 0 | Table: Ring / Deferral days / Quality / Feature / Assigned to |
| 2.2 | Ring details | GET `/deviceManagement/deviceConfigurations/{ringId}` | 0 | |
| 2.3 | Feature update profiles | GET `/beta/deviceManagement/windowsFeatureUpdateProfiles` | 0 | |
| 2.4 | Feature update details | GET `/beta/deviceManagement/windowsFeatureUpdateProfiles/{id}` | 0 | |
| 2.5 | Deployment state per device | GET `/beta/deviceManagement/windowsFeatureUpdateProfiles/{id}/deviceUpdateStates` | 0 | |
| 2.6 | Driver update profiles | GET `/beta/deviceManagement/windowsDriverUpdateProfiles` | 0 | |
| 2.7 | Driver update details | GET `/beta/deviceManagement/windowsDriverUpdateProfiles/{id}` | 0 | |
| 2.8 | Quality update profiles (expedited) | GET `/beta/deviceManagement/windowsQualityUpdateProfiles` | 0 | |
| 2.9 | Pause/resume a ring | PATCH `/deviceManagement/deviceConfigurations/{ringId}` | 2 | Set the pause properties on the `windowsUpdateForBusinessConfiguration` object: `{"@odata.type":"#microsoft.graph.windowsUpdateForBusinessConfiguration","qualityUpdatesPaused":true}` (resp. `featureUpdatesPaused`); `false` to resume. Pauses auto-expire after 35 days |

Note on 2.9: older docs mention `…/pause` / `…/resume` action endpoints in
beta — these are unreliable; PATCHing the pause properties is the stable
approach and matches what the Intune portal does.

# Devices, Remote Actions, Categories, Scripts

All paths relative to `https://graph.microsoft.com` (default `v1.0`).
Call via `scripts/graph.sh [--confirm|--confirm-name "NAME"] METHOD "path" [json]`.
Tier = safety tier from SKILL.md.

## 1. Managed devices

| # | Action | Method & Path | Tier | Notes |
|---|---|---|---|---|
| 1.1 | List all devices | GET `/deviceManagement/managedDevices` | 0 | Use `$select=deviceName,operatingSystem,complianceState,lastSyncDateTime,userPrincipalName`. Table: Name / OS / Compliance / Last sync / User |
| 1.2 | Find by name | GET `/deviceManagement/managedDevices?$filter=deviceName eq '{name}'` | 0 | |
| 1.3 | Find by user | GET `/deviceManagement/managedDevices?$filter=userPrincipalName eq '{upn}'` | 0 | |
| 1.4 | Device details | GET `/deviceManagement/managedDevices/{id}` | 0 | Show: name, serial, OS version, compliance, encryption, last sync, enrolled date, primary user |
| 1.5 | Devices of a user | GET `/users/{userId}/managedDevices` | 0 | |

## 2. Remote actions

| # | Action | Method & Path | Tier | Notes |
|---|---|---|---|---|
| 2.1 | Sync | POST `/deviceManagement/managedDevices/{id}/syncDevice` | 1 | |
| 2.2 | Reboot | POST `/deviceManagement/managedDevices/{id}/rebootNow` | 1 | |
| 2.3 | Remote lock | POST `/deviceManagement/managedDevices/{id}/remoteLock` | 1 | |
| 2.4 | Locate (iOS/Android lost mode) | POST `/deviceManagement/managedDevices/{id}/locateDevice` | 1 | |
| 2.5 | Reset passcode | POST `/deviceManagement/managedDevices/{id}/resetPasscode` | 2 | Locks the user out of the current passcode — confirm with summary |
| 2.6 | Rename | POST `/deviceManagement/managedDevices/{id}/setDeviceName` | 2 | Body: `{"deviceName": "NEW-NAME"}` |
| 2.7 | Enable lost mode (iOS supervised) | POST `/deviceManagement/managedDevices/{id}/enableLostMode` | 2 | Body: `{"message":"…","phoneNumber":"…","footer":"…"}` |
| 2.8 | Disable lost mode | POST `/deviceManagement/managedDevices/{id}/disableLostMode` | 2 | |
| 2.9 | **Retire** (remove company data) | POST `/deviceManagement/managedDevices/{id}/retire` | **3** | User must type back the device name |
| 2.10 | **Wipe** (factory reset) | POST `/deviceManagement/managedDevices/{id}/wipe` | **3** | Deletes ALL data. User must type back the device name |
| 2.11 | **Delete from Intune** | DELETE `/deviceManagement/managedDevices/{id}` | **3** | Record only — does not wipe. User must type back the device name |

## 3. Device categories & enrollment restrictions

| # | Action | Method & Path | Tier |
|---|---|---|---|
| 3.1 | List categories | GET `/deviceManagement/deviceCategories` | 0 |
| 3.2 | Create category | POST `/deviceManagement/deviceCategories` — body `{"displayName":"…","description":"…"}` | 2 |
| 3.3 | Set category on device | PUT `/deviceManagement/managedDevices/{id}/deviceCategory/$ref` | 2 |
| 3.4 | List enrollment restrictions | GET `/deviceManagement/deviceEnrollmentConfigurations` | 0 |

## 4. PowerShell scripts & remediations (beta)

| # | Action | Method & Path | Tier | Notes |
|---|---|---|---|---|
| 4.1 | List scripts | GET `/beta/deviceManagement/deviceManagementScripts` | 0 | |
| 4.2 | Script details | GET `/beta/deviceManagement/deviceManagementScripts/{id}` | 0 | |
| 4.3 | Run states per device | GET `/beta/deviceManagement/deviceManagementScripts/{id}/deviceRunStates` | 0 | |
| 4.4 | Upload script | POST `/beta/deviceManagement/deviceManagementScripts` | 2 | `scriptContent` must be Base64. **Show the decoded script to the user before confirming** |
| 4.5 | List remediations (health scripts) | GET `/beta/deviceManagement/deviceHealthScripts` | 0 | |
| 4.6 | Remediation run states | GET `/beta/deviceManagement/deviceHealthScripts/{id}/deviceRunStates` | 0 | |
| 4.7 | Create remediation | POST `/beta/deviceManagement/deviceHealthScripts` | 2 | Detection + remediation script, both Base64; show decoded content first |

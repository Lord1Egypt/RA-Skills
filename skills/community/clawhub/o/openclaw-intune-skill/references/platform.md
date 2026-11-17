# Platform: Autopilot, Enrollment, Apple, Android Enterprise

Call via `scripts/graph.sh`. Tier = safety tier from SKILL.md.

## 1. Windows Autopilot

| # | Action | Method & Path | Tier | Notes |
|---|---|---|---|---|
| 1.1 | List Autopilot devices | GET `/deviceManagement/windowsAutopilotDeviceIdentities` | 0 | Table: Serial / Model / Group tag / Enrollment state / Last seen |
| 1.2 | Device details | GET `/deviceManagement/windowsAutopilotDeviceIdentities/{id}` | 0 | |
| 1.3 | List deployment profiles | GET `/deviceManagement/windowsAutopilotDeploymentProfiles` | 0 | |
| 1.4 | Assign user to device | POST `/deviceManagement/windowsAutopilotDeviceIdentities/{id}/assignUserToDevice` | 2 | Body: `{"userPrincipalName":"user@domain.com"}` |
| 1.5 | **Delete Autopilot identity** | DELETE `/deviceManagement/windowsAutopilotDeviceIdentities/{id}` | **3** | Device must re-register for Autopilot; user must type back the serial number |

## 2. Enrollment configuration

| # | Action | Method & Path | Tier |
|---|---|---|---|
| 2.1 | List all enrollment configs | GET `/deviceManagement/deviceEnrollmentConfigurations` | 0 |
| 2.2 | Config details | GET `/deviceManagement/deviceEnrollmentConfigurations/{id}` | 0 |
| 2.3 | Config assignments | GET `/deviceManagement/deviceEnrollmentConfigurations/{id}/assignments` | 0 |
| 2.4 | ESP profiles only | GET `/deviceManagement/deviceEnrollmentConfigurations?$filter=isof('microsoft.graph.windows10EnrollmentCompletionPageConfiguration')` | 0 |
| 2.5 | Windows Hello for Business | GET `/deviceManagement/deviceEnrollmentConfigurations?$filter=isof('microsoft.graph.deviceEnrollmentWindowsHelloForBusinessConfiguration')` | 0 |

Includes device limit restrictions, platform restrictions, ESP, WHfB.

## 3. Apple device management

| # | Action | Method & Path | Tier | Notes |
|---|---|---|---|---|
| 3.1 | DEP/ADE onboarding settings | GET `/beta/deviceManagement/depOnboardingSettings` | 0 | |
| 3.2 | DEP enrollment profiles | GET `/beta/deviceManagement/depOnboardingSettings/{depId}/enrollmentProfiles` | 0 | |
| 3.3 | APNS certificate | GET `/deviceManagement/applePushNotificationCertificate` | 0 | Show expiry, subject, serial. **Proactively warn if it expires within 30 days** — an expired APNS cert breaks ALL Apple management |
| 3.4 | VPP tokens | GET `/beta/deviceManagement/vppTokens` | 0 | Also warn on approaching expiry |
| 3.5 | iOS/macOS managed app configs | GET `/deviceAppManagement/managedAppPolicies` | 0 | Filter iOS/macOS types |
| 3.6 | **Activation Lock bypass** (supervised) | POST `/deviceManagement/managedDevices/{id}/bypassActivationLock` | **3** | User must type back the device name |

## 4. Android Enterprise

| # | Action | Method & Path | Tier | Notes |
|---|---|---|---|---|
| 4.1 | Managed Google Play settings / binding status | GET `/beta/deviceManagement/androidManagedStoreAccountEnterpriseSettings` | 0 | Shows whether Work Profile / Fully Managed / Dedicated is connected |
| 4.2 | Enrollment profiles (Device Owner) | GET `/beta/deviceManagement/androidDeviceOwnerEnrollmentProfiles` | 0 | |
| 4.3 | App protection policies | GET `/deviceAppManagement/androidManagedAppProtections` | 0 | Details in `references/apps.md` |

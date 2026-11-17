# Apps & App Protection (MAM)

Call via `scripts/graph.sh`. Tier = safety tier from SKILL.md.

## 1. App management

| # | Action | Method & Path | Tier | Notes |
|---|---|---|---|---|
| 1.1 | List apps | GET `/deviceAppManagement/mobileApps` | 0 | Table: Name / Type / Publisher / Created |
| 1.2 | App details | GET `/deviceAppManagement/mobileApps/{id}` | 0 | |
| 1.3 | App assignments | GET `/deviceAppManagement/mobileApps/{id}/assignments` | 0 | Who gets the app |
| 1.4 | App configuration policies | GET `/deviceAppManagement/managedAppPolicies` | 0 | |
| 1.5 | App registrations (MAM devices) | GET `/deviceAppManagement/managedAppRegistrations` | 0 | |
| 1.6 | Assign app to group | POST `/deviceAppManagement/mobileApps/{id}/assignments` | 2 | Show target group + intent (required/available/uninstall) before confirming |
| 1.7 | List detected apps | GET `/deviceManagement/detectedApps` | 0 | Inventory across the fleet |
| 1.8 | Devices with a detected app | GET `/deviceManagement/detectedApps/{id}/managedDevices` | 0 | |

## 2. App Protection policies (MAM)

| # | Action | Method & Path | Tier |
|---|---|---|---|
| 2.1 | iOS policies | GET `/deviceAppManagement/iosManagedAppProtections` | 0 |
| 2.2 | Android policies | GET `/deviceAppManagement/androidManagedAppProtections` | 0 |
| 2.3 | Windows Information Protection | GET `/deviceAppManagement/windowsInformationProtectionPolicies` | 0 |
| 2.4a | Policy details (iOS) | GET `/deviceAppManagement/iosManagedAppProtections/{id}` | 0 |
| 2.4b | Policy details (Android) | GET `/deviceAppManagement/androidManagedAppProtections/{id}` | 0 |
| 2.5 | Status per user | GET `/deviceAppManagement/managedAppRegistrations?$filter=userId eq '{userId}'` | 0 |
| 2.6 | Create policy | POST `/deviceAppManagement/iosManagedAppProtections` or `…/androidManagedAppProtections` | 2 |

For 2.6: show a summary of the protection settings (PIN, encryption,
cut/copy/paste restrictions, targeted apps) before confirming.

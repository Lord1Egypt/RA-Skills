---
name: locate-on-windows
description: >
  Geolocate the current Windows machine using the native WinRT Location API (PowerShell 5.1).
  No external API keys, no browser, no dependencies — uses Windows.Devices.Geolocation directly.
  Trigger when user asks to locate themselves, find their position, or for device-based geolocation
  (as opposed to IP-based geolocation). Outputs latitude, longitude, and accuracy in meters.
---

# Locate your position on modern Windows

Locate the Windows machine using the built-in WinRT `Windows.Devices.Geolocation` API.

## Usage

Save the script below as `geolocate.ps1` and run:

```powershell
powershell.exe -ExecutionPolicy Bypass -File geolocate.ps1
```

Returns JSON:

```json
{
  "error": false,
  "message": "ok",
  "latitude": 35.6762,
  "longitude": 139.6503,
  "accuracy_m": 1500,
  "timestamp": "2026-01-01T08:00:00.0000000+09:00"
}
```

## Script

```powershell
# geolocate.ps1 — Windows Geolocation via WinRT (PowerShell 5.1 only)
Add-Type -AssemblyName "System.Runtime.WindowsRuntime"
[Windows.Devices.Geolocation.Geolocator, Windows.Devices.Geolocation, ContentType=WindowsRuntime] | Out-Null

try {
  $geo = New-Object Windows.Devices.Geolocation.Geolocator
  $geo.DesiredAccuracy = [Windows.Devices.Geolocation.PositionAccuracy]::Default
  $geo.DesiredAccuracyInMeters = 100

  $asyncOp = $geo.GetGeopositionAsync()

  $asTask = [System.WindowsRuntimeSystemExtensions].GetMethods() |
    Where-Object {
      $_.Name -eq 'AsTask' -and
      $_.GetParameters().Count -eq 1 -and
      $_.GetParameters()[0].ParameterType.IsGenericType -and
      $_.GetParameters()[0].ParameterType.Name.StartsWith('IAsyncOperation')
    } | Select-Object -First 1

  if (-not $asTask) {
    $output = [Ordered]@{
      error      = $true
      message    = "Cannot resolve AsTask<T> overload"
      latitude   = 0.0
      longitude  = 0.0
      accuracy_m = 0
      timestamp  = [datetime]::Now.ToString("o")
    }
    Write-Output ($output | ConvertTo-Json)
    exit 1
  }

  $genericMethod = $asTask.MakeGenericMethod([Windows.Devices.Geolocation.Geoposition])
  $task = $genericMethod.Invoke($null, @($asyncOp))
  $task.Wait()
  $pos = $task.Result

  $output = [Ordered]@{
    error      = $false
    message    = "ok"
    latitude   = [math]::Round($pos.Coordinate.Point.Position.Latitude, 6)
    longitude  = [math]::Round($pos.Coordinate.Point.Position.Longitude, 6)
    accuracy_m = $pos.Coordinate.Accuracy
    timestamp  = $pos.Coordinate.Timestamp.ToString("o")
  }
  Write-Output ($output | ConvertTo-Json)
} catch {
  $output = [Ordered]@{
    error      = $true
    message    = $_.Exception.Message
    latitude   = 0.0
    longitude  = 0.0
    accuracy_m = 0
    timestamp  = [datetime]::Now.ToString("o")
  }
  Write-Output ($output | ConvertTo-Json)
  exit 1
}
```

## How It Works

1. Loads `System.Runtime.WindowsRuntime` for WinRT type resolution.
2. Instantiates `Windows.Devices.Geolocation.Geolocator`.
3. Calls `GetGeopositionAsync()` — returns `IAsyncOperation<Geoposition>`.
4. Converts to `Task<T>` via reflection on `System.WindowsRuntimeSystemExtensions.AsTask<T>`.
5. Blocks with `.Wait()` and outputs JSON.

The location source depends on hardware: GPS (if present), WiFi triangulation, or IP fallback. Typical WiFi accuracy is 1–3 km.

## Requirements

- **Windows 10+**
- **PowerShell 5.1** (`powershell.exe`, not `pwsh` 7)
- Location must be enabled: Settings → Privacy → Location → On
- No admin rights needed

## Reverse Geocoding

Use the coordinates with any free reverse-geocoding service:

```bash
curl -s "https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=35.6762&longitude=139.6503"
```

## Troubleshooting

- **"Location access denied"**: Enable in Windows Settings → Privacy → Location
- **Timeout / no response**: The Location service may be disabled or blocked by group policy
- **Accuracy > 10km**: No WiFi/GPS available, falling back to IP-based estimate

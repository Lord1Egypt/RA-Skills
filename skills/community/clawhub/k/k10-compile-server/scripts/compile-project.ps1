param(
  [string]$Server = $env:COMPILE_SERVER,
  [Parameter(Mandatory = $true)]
  [string]$Dir,
  [string]$Output,
  [switch]$WebSerial,
  [switch]$Flash,
  [switch]$UploadLocal,
  [string]$Port,
  [int]$Baud = 921600,
  [int]$PollInterval = 3,
  [int]$CompileTimeout = 300
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($Server)) {
  throw "Server URL is required. Pass -Server https://your-k10-compile-server.example.com:8900 or set COMPILE_SERVER."
}
$Server = $Server.TrimEnd("/")

$UploadModeCount = 0
if ($Flash) { $UploadModeCount++ }
if ($UploadLocal) { $UploadModeCount++ }
if ($WebSerial) { $UploadModeCount++ }
if ($UploadModeCount -gt 1) {
  throw "Use only one upload mode: -WebSerial for browser upload, -Flash for server-side USB, or -UploadLocal for local esptool."
}

if (-not (Test-Path -LiteralPath $Dir -PathType Container)) {
  throw "Project directory does not exist: $Dir"
}
$ProjectDir = (Resolve-Path -LiteralPath $Dir).Path
if (-not (Test-Path -LiteralPath (Join-Path $ProjectDir "platformio.ini") -PathType Leaf)) {
  throw "No platformio.ini found in $ProjectDir"
}

if ([string]::IsNullOrWhiteSpace($Output) -and -not $WebSerial) {
  $Output = Join-Path (Get-Location) "firmware.bin"
} elseif (-not [string]::IsNullOrWhiteSpace($Output) -and -not [System.IO.Path]::IsPathRooted($Output)) {
  $Output = Join-Path (Get-Location) $Output
}

Write-Host "Checking server health..."
$HealthRaw = & curl.exe -skf --connect-timeout 5 "$Server/api/health"
if ($LASTEXITCODE -ne 0) {
  throw "Cannot connect to server at $Server"
}
$Health = $HealthRaw | ConvertFrom-Json
Write-Host "Server OK (K10 toolchain: $($Health.k10_toolchain_ready))"

function Find-LocalK10Port {
  $candidates = @()
  try {
    $ports = Get-PnpDevice -Class Ports -ErrorAction SilentlyContinue |
      Where-Object { $_.FriendlyName -match "USB|UART|Serial|CP210|CH340|ESP|UNIHIKER|K10" }
    foreach ($p in $ports) {
      if ($p.FriendlyName -match "COM\d+") {
        $candidates += $Matches[0]
      }
    }
  } catch {
  }

  $candidates = @($candidates | Select-Object -Unique)
  if ($candidates.Count -eq 1) {
    return $candidates[0]
  }
  if ($candidates.Count -gt 1) {
    Write-Host "Multiple local serial ports found:"
    foreach ($candidate in $candidates) {
      Write-Host "  $candidate"
    }
    return $null
  }

  $serialNames = @([System.IO.Ports.SerialPort]::GetPortNames())
  if ($serialNames.Count -eq 1) { return $serialNames[0] }
  return $null
}

function Invoke-Esptool {
  param([string[]]$Arguments)

  $esptoolPy = Get-Command esptool.py -ErrorAction SilentlyContinue
  if ($esptoolPy) {
    & $esptoolPy.Source @Arguments
    return $LASTEXITCODE
  }

  $esptool = Get-Command esptool -ErrorAction SilentlyContinue
  if ($esptool) {
    & $esptool.Source @Arguments
    return $LASTEXITCODE
  }

  $esptoolExe = Get-Command esptool.exe -ErrorAction SilentlyContinue
  if ($esptoolExe) {
    & $esptoolExe.Source @Arguments
    return $LASTEXITCODE
  }

  $python = Get-Command python -ErrorAction SilentlyContinue
  if ($python) {
    & $python.Source -c "import esptool" 2>$null
    if ($LASTEXITCODE -eq 0) {
      & $python.Source -m esptool @Arguments
      return $LASTEXITCODE
    }
  }

  Write-Host "esptool not found. Install it on the client machine:"
  Write-Host "  python -m pip install esptool"
  return 1
}

$TempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("k10-compile-" + [guid]::NewGuid().ToString("N"))
$Stage = Join-Path $TempRoot "project"
$ZipFile = Join-Path $TempRoot "project.zip"
$FlashDir = Join-Path $TempRoot "flash"
New-Item -ItemType Directory -Force -Path $Stage | Out-Null

try {
  Write-Host "Zipping project: $ProjectDir"
  Get-ChildItem -LiteralPath $ProjectDir -Force |
    Where-Object { $_.Name -notin @(".pio", ".git", "build", "__pycache__") } |
    ForEach-Object {
      Copy-Item -LiteralPath $_.FullName -Destination $Stage -Recurse -Force
    }

  $tar = Get-Command tar.exe -ErrorAction SilentlyContinue
  if ($tar) {
    & $tar.Source -a -cf $ZipFile -C $Stage .
    if ($LASTEXITCODE -ne 0) {
      throw "tar.exe failed to create project zip"
    }
  } else {
    Compress-Archive -Path (Join-Path $Stage "*") -DestinationPath $ZipFile -Force
  }
  Write-Host ("Zip size: {0} KB" -f [int]((Get-Item -LiteralPath $ZipFile).Length / 1024))

  Write-Host "Submitting compile job..."
  $SubmitRaw = & curl.exe -skf -X POST "$Server/api/compile" -F "file=@$ZipFile"
  if ($LASTEXITCODE -ne 0) {
    throw "Compile submission failed"
  }
  $Submit = $SubmitRaw | ConvertFrom-Json
  $BuildId = $Submit.build_id
  if ([string]::IsNullOrWhiteSpace($BuildId)) {
    throw "No build_id returned: $SubmitRaw"
  }
  Write-Host "Build ID: $BuildId"

  Write-Host "Compiling (polling every ${PollInterval}s, timeout ${CompileTimeout}s)..."
  $Started = Get-Date
  while ($true) {
    Start-Sleep -Seconds $PollInterval
    $Elapsed = [int]((Get-Date) - $Started).TotalSeconds
    if ($Elapsed -gt $CompileTimeout) {
      throw "Compile timed out after ${CompileTimeout}s"
    }

    $StatusRaw = & curl.exe -sk "$Server/api/build/$BuildId/status"
    $Status = $StatusRaw | ConvertFrom-Json
    switch ($Status.status) {
      "done" {
        if ($Status.bin_size) {
          Write-Host ("Compile complete! ({0} KB, {1}s)" -f [int]($Status.bin_size / 1024), $Elapsed)
        } else {
          Write-Host "Compile complete! (${Elapsed}s)"
        }
        break
      }
      "error" {
        Write-Host $StatusRaw
        throw "Compile failed: $($Status.error)"
      }
      default {
        Write-Host "Status: $($Status.status) (${Elapsed}s)"
      }
    }
    if ($Status.status -eq "done") { break }
  }

  if (-not [string]::IsNullOrWhiteSpace($Output)) {
    Write-Host "Downloading firmware to $Output"
    $OutputDir = Split-Path -Parent $Output
    if ($OutputDir) {
      New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
    }
    & curl.exe -skf -o $Output "$Server/api/build/$BuildId/download"
    if ($LASTEXITCODE -ne 0) {
      throw "Firmware download failed"
    }
    if (-not (Test-Path -LiteralPath $Output -PathType Leaf) -or (Get-Item -LiteralPath $Output).Length -eq 0) {
      throw "Firmware download produced an empty file: $Output"
    }
  }

  Write-Host "Flash layout:"
  & curl.exe -sk "$Server/api/build/$BuildId/flash-files"

  if ($WebSerial) {
    $WebSerialUrl = "$Server/?build_id=$BuildId"
    Write-Host "Opening Web Serial flash page:"
    Write-Host "  $WebSerialUrl"
    Write-Host "Use Chrome/Edge, click 浏览器烧录, and choose the K10 serial port."
    Write-Host "The page tries automatic bootloader entry first; use BOOT/RST only if prompted."
    try {
      Start-Process $WebSerialUrl
    } catch {
      Write-Host "Could not open the browser automatically. Open this URL manually:"
      Write-Host "  $WebSerialUrl"
    }
  }

  if ($UploadLocal) {
    if ([string]::IsNullOrWhiteSpace($Port)) {
      Write-Host "Detecting local K10 serial port..."
      $Port = Find-LocalK10Port
    }
    if ([string]::IsNullOrWhiteSpace($Port)) {
      throw "Could not auto-detect local K10 serial port. Re-run with -Port COM3 or the matching device port."
    }

    New-Item -ItemType Directory -Force -Path $FlashDir | Out-Null
    Write-Host "Downloading flash files for local upload..."
    foreach ($File in @("bootloader", "partitions", "firmware")) {
      $Target = Join-Path $FlashDir "$File.bin"
      & curl.exe -skf -o $Target "$Server/api/build/$BuildId/file/$File.bin"
      if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $Target) -or (Get-Item -LiteralPath $Target).Length -eq 0) {
        throw "Failed to download $File.bin"
      }
    }

    Write-Host "Uploading to local K10 on $Port..."
    Write-Host "If upload cannot enter bootloader automatically: hold BOOT, tap RST, then release BOOT."
    $EsptoolArgs = @(
      "--chip", "esp32s3",
      "--port", $Port,
      "--baud", "$Baud",
      "--before", "default_reset",
      "--after", "hard_reset",
      "write_flash", "-z",
      "--flash_mode", "dio",
      "--flash_freq", "80m",
      "--flash_size", "detect",
      "0x0", (Join-Path $FlashDir "bootloader.bin"),
      "0x8000", (Join-Path $FlashDir "partitions.bin"),
      "0x10000", (Join-Path $FlashDir "firmware.bin")
    )
    $Code = Invoke-Esptool -Arguments $EsptoolArgs
    if ($Code -ne 0) {
      throw "Local K10 upload failed"
    }
    Write-Host "Local upload successful! K10 is rebooting..."
  }

  if ($Flash) {
    Write-Host "Triggering server-side flash..."
    Write-Host "Make sure K10 is connected via USB to the compile server machine."
    $FlashRaw = & curl.exe -sk -X POST "$Server/api/flash/$BuildId"
    $FlashResult = $FlashRaw | ConvertFrom-Json
    if ($FlashResult.status -ne "success") {
      Write-Host $FlashRaw
      throw "Server-side flash failed"
    }
    Write-Host "Flash successful! K10 is rebooting..."
  }

  Write-Host ""
  Write-Host "Done! Build $BuildId complete."
  if (-not [string]::IsNullOrWhiteSpace($Output)) {
    Write-Host "Firmware: $Output"
  }
} finally {
  if (Test-Path -LiteralPath $TempRoot) {
    try {
      Remove-Item -LiteralPath $TempRoot -Recurse -Force
    } catch {
      Write-Host "Warning: could not remove temp folder $TempRoot"
    }
  }
}

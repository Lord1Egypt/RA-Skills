# PDFToolbox wspet:// Protocol Launcher
# Usage: .\launch_wspet.ps1 -Command "convert" -TargetFormat ".docx" -Files @("C:\path\to\file.pdf") [-Password "123456"]

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("convert", "ocr", "optimize", "translate", "watermark", "background", "headerFooter",
                 "batesNumber", "security", "batchPrint", "dataExtract", "deleteBlankPages",
                 "sign", "split", "combine", "crop", "create")]
    [string]$Command,

    [Parameter(Mandatory=$false)]
    [string]$TargetFormat = "",

    [Parameter(Mandatory=$false)]
    [string[]]$Files = @(),

    [Parameter(Mandatory=$false)]
    [string]$Password = "",

    [Parameter(Mandatory=$false)]
    [string]$Entrance = "OpenClaw",

    [Parameter(Mandatory=$false)]
    [bool]$ResetExistingInstance = $false,

    [Parameter(Mandatory=$false)]
    [int]$PostResetLaunchDelayMilliseconds = 0,

    [Parameter(Mandatory=$false)]
    [int]$PreLaunchDelayMilliseconds = 0,

    [Parameter(Mandatory=$false)]
    [string]$DiagnosticLogDirectory = ""
)

function Build-FilesXml {
    param(
        [string[]]$FilePaths,
        [string]$FilePassword = ""
    )

    $xml = '<?xml version="1.0" encoding="UTF-8"?>' + "`n<Files>`n"

    foreach ($file in $FilePaths) {
        if (-not (Test-Path -LiteralPath $file)) {
            throw "File not found: $file"
        }

        $fullPath = (Resolve-Path -LiteralPath $file).Path
        $escapedPath = [System.Security.SecurityElement]::Escape($fullPath)
        $escapedPassword = [System.Security.SecurityElement]::Escape($FilePassword)
        $xml += "  <File>`n"
        $xml += "    <Path>$escapedPath</Path>`n"
        $xml += "    <Password>$escapedPassword</Password>`n"
        $xml += "  </File>`n"
    }

    $xml += "</Files>"
    return $xml
}

function Write-DiagnosticLog {
    param(
        [Parameter(Mandatory=$true)]
        [string[]]$Lines
    )

    if ([string]::IsNullOrWhiteSpace($DiagnosticLogDirectory)) {
        return
    }

    try {
        New-Item -ItemType Directory -Path $DiagnosticLogDirectory -Force | Out-Null
        $stamp = Get-Date -Format 'yyyyMMdd-HHmmss-fff'
        $logPath = Join-Path $DiagnosticLogDirectory "pdfelement-launch-$stamp.log"
        $Lines | Set-Content -LiteralPath $logPath -Encoding UTF8
        Write-Host "Diagnostic log: $logPath" -ForegroundColor DarkGray
    } catch {
        Write-Host "Failed to write diagnostic log: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

function Write-PDFelementInstallGuidance {
    Write-Host "PDFelement is a local PDF editor and batch-processing tool from Wondershare." -ForegroundColor Yellow
    Write-Host "It can convert PDFs to Word/Excel/PPT, run OCR, compress files, translate, watermark, split/merge, sign, and secure documents." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "I couldn't launch PDFelement because the wspet:// protocol is unavailable on this machine." -ForegroundColor Red
    Write-Host "That usually means PDFelement is missing, not registered correctly, or the version is too old." -ForegroundColor Red
    Write-Host "Download link: https://pdf.wondershare.com/" -ForegroundColor Cyan
    Write-Host "After installing or updating PDFelement, try again. A Windows restart may be needed so the protocol registration takes effect." -ForegroundColor Yellow
}

function Get-WspetProtocolStatus {
    $candidateKeys = @(
        'Registry::HKEY_CLASSES_ROOT\wspet\shell\open\command',
        'Registry::HKEY_CURRENT_USER\Software\Classes\wspet\shell\open\command'
    )

    foreach ($key in $candidateKeys) {
        if (-not (Test-Path -LiteralPath $key)) {
            continue
        }

        $rawCommand = (Get-ItemProperty -LiteralPath $key -ErrorAction SilentlyContinue).'(default)'
        if ([string]::IsNullOrWhiteSpace($rawCommand)) {
            continue
        }

        $expandedCommand = [Environment]::ExpandEnvironmentVariables($rawCommand)
        $exePath = $null

        if ($expandedCommand -match '^\s*"([^"]+)"') {
            $exePath = $matches[1]
        } elseif ($expandedCommand -match '^\s*([^\s]+)') {
            $exePath = $matches[1]
        }

        if ([string]::IsNullOrWhiteSpace($exePath)) {
            return [pscustomobject]@{
                Available = $false
                RegistryKey = $key
                Command = $expandedCommand
                ExecutablePath = $null
                Reason = 'protocol-command-unparseable'
            }
        }

        if (-not (Test-Path -LiteralPath $exePath)) {
            return [pscustomobject]@{
                Available = $false
                RegistryKey = $key
                Command = $expandedCommand
                ExecutablePath = $exePath
                Reason = 'protocol-target-missing'
            }
        }

        return [pscustomobject]@{
            Available = $true
            RegistryKey = $key
            Command = $expandedCommand
            ExecutablePath = $exePath
            Reason = 'ok'
        }
    }

    return [pscustomobject]@{
        Available = $false
        RegistryKey = $null
        Command = $null
        ExecutablePath = $null
        Reason = 'protocol-not-registered'
    }
}

function Invoke-Wspet {
    param(
        [Parameter(Mandatory=$true)]
        [string]$ParameterString
    )

    $base64Param = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($ParameterString))
    $escapedParam = [Uri]::EscapeDataString($base64Param)
    $uri = "wspet://param=$escapedParam"

    Write-Host "Launching: $uri" -ForegroundColor Green
    Start-Process $uri -ErrorAction Stop | Out-Null
}

function Reset-ToolboxInstance {
    param(
        [int]$GracefulWaitSeconds = 4,
        [int]$ForceWaitSeconds = 2,
        [int]$MaxWaitSeconds = 20,
        [int]$StableQuietChecks = 3,
        [int]$PollIntervalMilliseconds = 500
    )

    $existing = Get-Process -Name PDFToolbox -ErrorAction SilentlyContinue
    if (-not $existing) {
        return
    }

    Write-Host "Detected existing PDFToolbox instance; resetting it so auto-exec can start from a clean window." -ForegroundColor Yellow

    try {
        Invoke-Wspet -ParameterString "/nowexit"
        Start-Sleep -Seconds $GracefulWaitSeconds
    } catch {
        Write-Host "Graceful /nowexit request failed; falling back to process cleanup." -ForegroundColor Yellow
    }

    $deadline = (Get-Date).AddSeconds($MaxWaitSeconds)
    $quietChecks = 0

    while ((Get-Date) -lt $deadline) {
        $lingering = Get-Process -Name PDFToolbox -ErrorAction SilentlyContinue

        if (-not $lingering) {
            $quietChecks += 1
            if ($quietChecks -ge $StableQuietChecks) {
                return
            }

            Start-Sleep -Milliseconds $PollIntervalMilliseconds
            continue
        }

        $quietChecks = 0
        Write-Host "Stopping lingering PDFToolbox process(es): $($lingering.Id -join ', ')" -ForegroundColor Yellow

        foreach ($proc in $lingering) {
            try {
                Stop-Process -Id $proc.Id -Force -ErrorAction Stop
            } catch {
                Write-Host "Failed to stop PDFToolbox process $($proc.Id): $($_.Exception.Message)" -ForegroundColor Yellow
            }
        }

        Start-Sleep -Seconds $ForceWaitSeconds
    }

    $stillRunning = Get-Process -Name PDFToolbox -ErrorAction SilentlyContinue
    if ($stillRunning) {
        throw "PDFToolbox is still running after reset attempts: $($stillRunning.Id -join ', ')"
    }
}

$params = $Command

if ($TargetFormat -and $Command -eq "convert") {
    $params += " -t $TargetFormat"
}

if ($Files.Count -gt 0) {
    $filesXml = Build-FilesXml -FilePaths $Files -FilePassword $Password
    $base64FilesXml = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($filesXml))
    $params += " -f $base64FilesXml"
}

$protocolStatus = Get-WspetProtocolStatus
Write-DiagnosticLog -Lines @(
    "Timestamp: $(Get-Date -Format o)",
    "Command: $Command",
    "TargetFormat: $TargetFormat",
    "Files: $($Files -join '; ')",
    "ProtocolAvailable: $($protocolStatus.Available)",
    "ProtocolReason: $($protocolStatus.Reason)",
    "ProtocolRegistryKey: $($protocolStatus.RegistryKey)",
    "ProtocolExecutablePath: $($protocolStatus.ExecutablePath)",
    "ProtocolCommand: $($protocolStatus.Command)"
)

if (-not $protocolStatus.Available) {
    Write-Host "wspet protocol check failed: $($protocolStatus.Reason)" -ForegroundColor Yellow
    if ($protocolStatus.RegistryKey) {
        Write-Host "Registry key: $($protocolStatus.RegistryKey)" -ForegroundColor DarkGray
    }
    if ($protocolStatus.Command) {
        Write-Host "Protocol command: $($protocolStatus.Command)" -ForegroundColor DarkGray
    }
    if ($protocolStatus.ExecutablePath) {
        Write-Host "Missing executable: $($protocolStatus.ExecutablePath)" -ForegroundColor DarkGray
    }

    Write-PDFelementInstallGuidance
    exit 2
}

# Reuse of an old single-instance window can suppress auto-exec countdowns, so reset first.
if ($ResetExistingInstance -and $Files.Count -gt 0) {
    Reset-ToolboxInstance

    # Let the protocol handler and single-instance app settle before launching the real task.
    if ($PostResetLaunchDelayMilliseconds -gt 0) {
        Write-Host "Waiting $PostResetLaunchDelayMilliseconds ms after reset before launching the task." -ForegroundColor Yellow
        Start-Sleep -Milliseconds $PostResetLaunchDelayMilliseconds
    }
}

# Match the timing of the successful interactive tests more closely before invoking the real task.
if ($PreLaunchDelayMilliseconds -gt 0) {
    Write-Host "Waiting $PreLaunchDelayMilliseconds ms before invoking wspet://." -ForegroundColor Yellow
    Start-Sleep -Milliseconds $PreLaunchDelayMilliseconds
}

# Send the real task directly so PDFelement can auto-execute instead of opening an empty probe instance.
$params += " -wsclaw -autoexec -entrance $Entrance"

Write-DiagnosticLog -Lines @(
    "Timestamp: $(Get-Date -Format o)",
    "Command: $Command",
    "TargetFormat: $TargetFormat",
    "Files: $($Files -join '; ')",
    "ProtocolAvailable: $($protocolStatus.Available)",
    "ProtocolReason: $($protocolStatus.Reason)",
    "ProtocolRegistryKey: $($protocolStatus.RegistryKey)",
    "ProtocolExecutablePath: $($protocolStatus.ExecutablePath)",
    "ProtocolCommand: $($protocolStatus.Command)",
    "ResetExistingInstance: $ResetExistingInstance",
    "PostResetLaunchDelayMilliseconds: $PostResetLaunchDelayMilliseconds",
    "PreLaunchDelayMilliseconds: $PreLaunchDelayMilliseconds",
    "Command parameters:",
    $params
)

Write-Host "Command parameters: $params" -ForegroundColor Cyan

try {
    Invoke-Wspet -ParameterString $params
} catch {
    Write-PDFelementInstallGuidance
    exit 2
}

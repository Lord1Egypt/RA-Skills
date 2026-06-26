<#
.SYNOPSIS
    Convert PlantUML source to SVG, PNG, PDF, or ASCII art on Windows (PowerShell).

.DESCRIPTION
    Mirror of generate-plantuml.sh for native Windows PowerShell users.

    PRIVACY NOTICE
    --------------
    This script renders diagrams LOCALLY by default. The PlantUML source is
    NOT transmitted off-host unless you explicitly pass -UsePublicServer.

    Backend priority (local-first):
      1. Docker (plantuml/plantuml image)        — preferred, fully local
      2. Local plantuml.jar                       — offline fallback (Java required)
      3. Kroki public server (kroki.io)          — OPT-IN ONLY (-UsePublicServer)
                                                   Uploads diagram source to a third
                                                   party operated by Yuzu Tech (EU).
                                                   Kroki is open source and self-
                                                   hostable — set
                                                   $env:PLANTUML_PUBLIC_SERVER to
                                                   point at your own instance.
                                                   Avoid the default public host
                                                   for confidential architecture,
                                                   credentials, or proprietary
                                                   business processes.

    Note: the legacy https://www.plantuml.com/plantuml POST endpoint now sits
    behind a Cloudflare + Ezoic consent wall that returns HTTP 302 to a
    JavaScript-only HTML page, breaking automated rendering. Kroki replaces
    it as the default opt-in public backend in v1.4.1.

    Supports CJK (Chinese/Japanese/Korean) font rendering via -Cjk flag,
    and automatic aspect ratio correction for excessively wide or tall diagrams.

.PARAMETER InputPath
    Path to the .puml source file.

.PARAMETER OutputDir
    Output directory. Defaults to .\output.

.PARAMETER Format
    Output format: svg (default), png, pdf, or txt.

.PARAMETER Cjk
    Enable CJK font support. Mounts host font directories into Docker,
    replaces Helvetica with a CJK-compatible font.

.PARAMETER NoFix
    Disable automatic aspect ratio correction. By default, diagrams wider or
    taller than the threshold are automatically corrected and re-rendered.

.PARAMETER MaxAspect
    Maximum allowed aspect ratio before correction (default: 2.5).

.PARAMETER NoA4Check
    Disable automatic A4 paper fit validation. The A4 check ensures the
    rendered diagram fits within either portrait (794×1123 px @ 96 DPI) or
    landscape (1123×794 px) A4 dimensions and that the rendered font remains
    legible when printed. ON by default.

.PARAMETER MinFontPt
    Minimum legible font size on A4 paper, in pt (default: 8.0). Used only
    when the A4 check is enabled.

.PARAMETER UsePublicServer
    OPT-IN: render via the Kroki public server (kroki.io by default).
    WARNING: this uploads the diagram source to a third-party service.
    Override the host via $env:PLANTUML_PUBLIC_SERVER = '<url>' to point at
    a self-hosted Kroki instance. Off by default — local Docker / JAR
    backends are used instead.

.EXAMPLE
    .\generate-plantuml.ps1 diagram.puml .\out -Format svg

.EXAMPLE
    .\generate-plantuml.ps1 diagram.puml .\out -Cjk -Format png

.EXAMPLE
    .\generate-plantuml.ps1 diagram.puml .\out -MaxAspect 3.0

.EXAMPLE
    # Opt in to remote rendering (uploads diagram to kroki.io)
    .\generate-plantuml.ps1 diagram.puml .\out -UsePublicServer

.EXAMPLE
    # Opt in to a self-hosted Kroki instance
    $env:PLANTUML_PUBLIC_SERVER = 'https://kroki.internal.example.com'
    .\generate-plantuml.ps1 diagram.puml .\out -UsePublicServer
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [Alias("Input")]
    [string]$InputPath,

    [Parameter(Position = 1)]
    [string]$OutputDir = ".\output",

    [ValidateSet("svg", "png", "pdf", "txt")]
    [string]$Format = "svg",

    [Parameter()]
    [switch]$Cjk,

    [Parameter()]
    [switch]$NoFix,

    [Parameter()]
    [float]$MaxAspect = 2.5,

    [Parameter()]
    [switch]$NoA4Check,

    [Parameter()]
    [float]$MinFontPt = 8.0,

    [Parameter()]
    [switch]$UsePublicServer
)

# A4 paper in CSS pixels at 96 DPI (1 in = 96px, A4 = 210×297 mm ⇒ 8.27×11.69 in)
$script:a4PortraitW = 794
$script:a4PortraitH = 1123
$script:a4LandscapeW = 1123
$script:a4LandscapeH = 794

# Body font px set by the mandatory uml-diagrams.org preamble (defaultFontSize 12)
$script:defaultFontPx = 12.0

# Caller-visible flag set by Test-A4Fit / consumed by Fix-A4Fit
$script:a4ScaleFactor = 1.0

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $InputPath -PathType Leaf)) {
    Write-Error "Input file not found: $InputPath"
    exit 1
}

if (-not (Test-Path -LiteralPath $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$baseName = [System.IO.Path]::GetFileNameWithoutExtension($InputPath)
$outputFile = Join-Path $OutputDir "$baseName.$Format"

# Script-level dimension variables (populated by Get-SvgDimensions / Get-PngDimensions)
$script:svgWidth = $null
$script:svgHeight = $null
$script:pngWidth = $null
$script:pngHeight = $null

# ═══════════════════════════════════════════════════════════════════════════════
# Helper Functions
# ═══════════════════════════════════════════════════════════════════════════════

function Test-Command {
    param([string]$Name)
    $null -ne (Get-Command $Name -ErrorAction SilentlyContinue)
}

function Test-BinaryOk {
    param([string]$Path, [string]$Fmt)
    if (-not (Test-Path -LiteralPath $Path)) { return $false }
    $fi = Get-Item -LiteralPath $Path
    if ($fi.Length -le 0) { return $false }
    try {
        $stream = [System.IO.File]::OpenRead($Path)
        $buf = New-Object byte[] 4
        $n = $stream.Read($buf, 0, 4)
        $stream.Close()
        if ($n -lt 4) { return $false }
        $hex = ($buf | ForEach-Object { $_.ToString("x2") }) -join ""
        switch ($Fmt) {
            "png" { return $hex -eq "89504e47" }
            "pdf" { return $hex -eq "25504446" }
            default { return $true }
        }
    } catch {
        return $false
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# CJK Font Detection & Configuration
# ═══════════════════════════════════════════════════════════════════════════════

function Detect-Cjk {
    param([string]$Path)
    try {
        $content = [System.IO.File]::ReadAllText(
            (Resolve-Path -LiteralPath $Path),
            [System.Text.Encoding]::UTF8
        )
        foreach ($c in $content.ToCharArray()) {
            $cp = [int]$c
            if (($cp -ge 0x4E00 -and $cp -le 0x9FFF) -or
                ($cp -ge 0x3400 -and $cp -le 0x4DBF) -or
                ($cp -ge 0xF900 -and $cp -le 0xFAFF) -or
                ($cp -ge 0x3040 -and $cp -le 0x30FF) -or
                ($cp -ge 0xAC00 -and $cp -le 0xD7AF) -or
                ($cp -ge 0x3000 -and $cp -le 0x303F) -or
                ($cp -ge 0xFF00 -and $cp -le 0xFFEF)) {
                return $true
            }
        }
    } catch {
        # fall through
    }
    return $false
}

function Prepare-PumlForCjk {
    param([string]$SrcPath)
    $dstPath = "$SrcPath.cjk.puml"
    $content = Get-Content -LiteralPath $SrcPath -Encoding UTF8 -Raw

    $content = $content -replace 'skinparam defaultFontName Helvetica',
        'skinparam defaultFontName "WenQuanYi Micro Hei"'

    if ($content -notmatch 'defaultFontName') {
        $content = $content -replace '@startuml',
            '@startuml' + "`n" + '!pragma defaultFontName "WenQuanYi Micro Hei"' + "`n" +
            'skinparam defaultFontName "WenQuanYi Micro Hei"'
    }

    Set-Content -LiteralPath $dstPath -Value $content -Encoding UTF8 -NoNewline
    return $dstPath
}

# ═══════════════════════════════════════════════════════════════════════════════
# Aspect Ratio Validation & Auto-Fix
# ═══════════════════════════════════════════════════════════════════════════════

function Get-SvgDimensions {
    param([string]$SvgPath)
    if (-not (Test-Path -LiteralPath $SvgPath)) { return $false }
    $firstLines = Get-Content -LiteralPath $SvgPath -TotalCount 5 -Encoding UTF8 -Raw
    if ($firstLines -match 'viewBox="(\S+)\s+(\S+)\s+(\S+)\s+(\S+)"') {
        $script:svgWidth  = [int][double]$Matches[3]
        $script:svgHeight = [int][double]$Matches[4]
        return ($script:svgWidth -gt 0 -and $script:svgHeight -gt 0)
    }
    return $false
}

function Get-PngDimensions {
    param([string]$PngPath)
    # Primary: use .NET System.Drawing (available on Windows)
    try {
        Add-Type -AssemblyName System.Drawing -ErrorAction Stop
        $img = [System.Drawing.Image]::FromFile((Resolve-Path -LiteralPath $PngPath))
        $script:pngWidth  = $img.Width
        $script:pngHeight = $img.Height
        $img.Dispose()
        return ($script:pngWidth -gt 0 -and $script:pngHeight -gt 0)
    } catch {
        # Fallback: try ImageMagick identify
        if (Test-Command "identify") {
            try {
                $dims = & identify -format "%w %h" $PngPath 2>$null
                if ($dims -match '^(\d+)\s+(\d+)$') {
                    $script:pngWidth  = [int]$Matches[1]
                    $script:pngHeight = [int]$Matches[2]
                    return $true
                }
            } catch { }
        }
    }
    return $false
}

function Test-AspectRatio {
    param([string]$ImgPath, [string]$Fmt)
    $w = $null; $h = $null
    switch ($Fmt) {
        "svg" {
            if (-not (Get-SvgDimensions $ImgPath)) { return $null }
            $w = $script:svgWidth; $h = $script:svgHeight
        }
        "png" {
            if (-not (Get-PngDimensions $ImgPath)) { return $null }
            $w = $script:pngWidth; $h = $script:pngHeight
        }
        default { return $null }
    }
    if (-not $w -or -not $h -or $w -le 0 -or $h -le 0) { return $null }

    $ratio = if ($w -gt $h) { [math]::Round($w / $h, 2) } else { [math]::Round($h / $w, 2) }
    Write-Host "  📐 Dimensions: ${w}x${h}, aspect ratio: ${ratio}:1 (max: ${MaxAspect}:1)"
    return ($ratio -le $MaxAspect)
}

function Fix-PumlAspectRatio {
    param([string]$PumlPath, [string]$Problem)

    Write-Host "  → Attempting to fix aspect ratio (${Problem})..."
    $content = Get-Content -LiteralPath $PumlPath -Encoding UTF8 -Raw

    if ($content -match '!pragma aspectRatioFixed') {
        Write-Host "  → Already auto-fixed; skipping further attempts"
        return $null
    }

    $tmpPath = "${PumlPath}.fixed"
    $content = $content -replace '@startuml', "@startuml`n!pragma aspectRatioFixed"

    if ($Problem -eq "too_tall") {
        $content = $content -replace '@startuml', "@startuml`nleft to right direction"
        Write-Host "  → Applied: left to right direction"
        $content = $content -replace 'skinparam StereotypeCBackgroundColor white',
            "skinparam StereotypeCBackgroundColor white`nskinparam ParticipantPadding 5"
    } else {
        if ($content -match "left to right direction") {
            $content = $content -replace "left to right direction`r?`n", ""
        }
        $content = $content -replace '@startuml', "@startuml`ntop to bottom direction"
        Write-Host "  → Applied: top to bottom direction"
        $content = $content -replace 'skinparam StereotypeCBackgroundColor white',
            "skinparam StereotypeCBackgroundColor white`nskinparam BoxPadding 5`nskinparam ParticipantPadding 5"
    }

    if ($content -notmatch '^scale ') {
        $content = $content -replace 'skinparam StereotypeCBackgroundColor white',
            "skinparam StereotypeCBackgroundColor white`nscale 0.8"
        Write-Host "  → Applied: scale 0.8"
    }

    Set-Content -LiteralPath $tmpPath -Value $content -Encoding UTF8 -NoNewline
    return $tmpPath
}

# ═══════════════════════════════════════════════════════════════════════════════
# A4 Paper Fit Validation & Auto-Scale Fix
#
# Same algorithm as generate-plantuml.sh:
#   * Compare rendered SVG/PNG dimensions against A4 portrait (794×1123) and
#     landscape (1123×794) boxes at 96 DPI.
#   * Accept if EITHER orientation fits.
#   * Otherwise compute scale = max(portrait_factor, landscape_factor), clamp
#     to [0.15, 1.0], inject a PlantUML "scale N" directive and re-render.
#   * After re-rendering warn if effective on-paper font (scale × 12px × 0.75)
#     falls below -MinFontPt.
# ═══════════════════════════════════════════════════════════════════════════════

function Test-A4Fit {
    param([string]$ImgPath, [string]$Fmt)
    $w = $null; $h = $null
    switch ($Fmt) {
        "svg" {
            if (-not (Get-SvgDimensions $ImgPath)) { return $null }
            $w = $script:svgWidth;   $h = $script:svgHeight
        }
        "png" {
            if (-not (Get-PngDimensions $ImgPath)) { return $null }
            $w = $script:pngWidth;   $h = $script:pngHeight
        }
        default { return $null }
    }
    if (-not $w -or -not $h -or $w -le 0 -or $h -le 0) { return $null }

    $script:a4ScaleFactor = 1.0

    $fitsPortrait  = ($w -le $script:a4PortraitW  -and $h -le $script:a4PortraitH)
    $fitsLandscape = ($w -le $script:a4LandscapeW -and $h -le $script:a4LandscapeH)

    if ($fitsPortrait -or $fitsLandscape) {
        Write-Host "  📄 A4 fit: ${w}x${h}px fits A4 portrait ($($script:a4PortraitW)x$($script:a4PortraitH)) or landscape ($($script:a4LandscapeW)x$($script:a4LandscapeH)) ✓"
        return $true
    }

    $sp = [math]::Min(($script:a4PortraitW  / $w), ($script:a4PortraitH  / $h))
    $sl = [math]::Min(($script:a4LandscapeW / $w), ($script:a4LandscapeH / $h))
    $factor = [math]::Max($sp, $sl)
    if ($factor -lt 0.15) { $factor = 0.15 }
    $script:a4ScaleFactor = [math]::Round($factor, 3)

    Write-Host "  📄 A4 fit: ${w}x${h}px exceeds A4 portrait ($($script:a4PortraitW)x$($script:a4PortraitH)) and landscape ($($script:a4LandscapeW)x$($script:a4LandscapeH))"
    Write-Host "     Required scale to fit: $($script:a4ScaleFactor) (portrait factor $([math]::Round($sp,3)), landscape factor $([math]::Round($sl,3)))"
    return $false
}

function Fix-A4Fit {
    param([string]$PumlPath)

    if (-not $script:a4ScaleFactor -or $script:a4ScaleFactor -eq 1.0) {
        return $null
    }
    $content = Get-Content -LiteralPath $PumlPath -Encoding UTF8 -Raw
    if ($content -match '!pragma a4FitFixed') { return $null }

    $tmpPath = "${PumlPath}.a4fixed"
    $content = $content -replace '^@startuml', "@startuml`n!pragma a4FitFixed"

    $content = $content -replace '(?m)^scale 0\.8\r?\n', ''
    $content = $content -replace '!pragma a4FitFixed', "!pragma a4FitFixed`n scale $($script:a4ScaleFactor)"
    Write-Host "  → Applied: scale $($script:a4ScaleFactor) (A4 fit)"

    $effectivePt = [math]::Round($script:a4ScaleFactor * $script:defaultFontPx * 0.75, 1)
    if ($effectivePt -lt $MinFontPt) {
        Write-Host "  ⚠ After scaling to $($script:a4ScaleFactor), estimated font ≈ ${effectivePt}pt on A4"
        Write-Host "    That is below -MinFontPt $MinFontPt and may be hard to read in print."
        Write-Host "    Consider splitting into multiple diagrams or abbreviating labels."
    } else {
        Write-Host "     Estimated font ≈ ${effectivePt}pt on A4 (≥ min ${MinFontPt}pt) ✓"
    }

    Set-Content -LiteralPath $tmpPath -Value $content -Encoding UTF8 -NoNewline
    return $tmpPath
}

# ═══════════════════════════════════════════════════════════════════════════════
# Rendering Backends
# ═══════════════════════════════════════════════════════════════════════════════

function Convert-ViaServer {
    param([string]$SourcePath = $InputPath)
    # OPT-IN ONLY backend. DISABLED unless -UsePublicServer is passed.
    # When enabled, this function POSTs the entire diagram source to a Kroki
    # server (kroki.io by default, overridable via $env:PLANTUML_PUBLIC_SERVER).
    # The audit (SDI-2) flagged this as a data-exfiltration path, so we require
    # explicit user consent. Kroki is open source and self-hostable.
    if (-not $UsePublicServer) {
        Write-Host "  → Public server disabled (privacy default). Pass -UsePublicServer to enable."
        return $false
    }

    $serverHost = if ($env:PLANTUML_PUBLIC_SERVER) {
        $env:PLANTUML_PUBLIC_SERVER.TrimEnd('/')
    } else {
        "https://kroki.io"
    }
    $serverUrl = "$serverHost/plantuml/$Format"
    $hostLabel = ($serverHost -replace '^https?://', '') -replace '/.*$', ''

    Write-Host ""
    Write-Host "  ⚠  PRIVACY WARNING: about to upload diagram source to $serverUrl"
    Write-Host "     The full contents of '$SourcePath' will be transmitted to $hostLabel."
    if ($serverHost -eq "https://kroki.io") {
        Write-Host "     kroki.io is operated by Yuzu Tech (EU). Kroki is open source and"
        Write-Host "     self-hostable — set `$env:PLANTUML_PUBLIC_SERVER = '<your-url>' to use your own."
    } else {
        Write-Host "     (Custom backend selected via `$env:PLANTUML_PUBLIC_SERVER.)"
    }
    Write-Host "     Do NOT use this backend for confidential architecture, credentials,"
    Write-Host "     customer data, or proprietary business logic."
    Write-Host ""
    Write-Host "  → Trying public server (opt-in via -UsePublicServer)..."
    try {
        $body = [System.IO.File]::ReadAllBytes((Resolve-Path -LiteralPath $SourcePath))
        Invoke-WebRequest -Uri $serverUrl -Method Post -Body $body `
            -ContentType "text/plain" -OutFile $outputFile `
            -TimeoutSec 60 -MaximumRedirection 5 `
            -UseBasicParsing -ErrorAction Stop | Out-Null

        $ok = $false
        if ($Format -eq "svg") {
            $content = Get-Content -LiteralPath $outputFile -Raw -ErrorAction SilentlyContinue
            if ($content -and ($content -match "<svg")) { $ok = $true }
        } elseif ($Format -eq "txt") {
            if ((Get-Item -LiteralPath $outputFile).Length -gt 0) { $ok = $true }
        } else {
            $ok = Test-BinaryOk -Path $outputFile -Fmt $Format
        }

        if ($ok) {
            Write-Host "  ✓ Success (public server)"
            return $true
        }
    } catch {
        # fall through
    }

    Write-Host "  ✗ Public server failed — check network or try Docker/local JAR backend"
    return $false
}

function Convert-ViaDocker {
    param([string]$SourcePath = $InputPath)
    if (-not (Test-Command "docker")) {
        Write-Host "  → Docker not available, skipping"
        return $false
    }

    Write-Host "  → Trying Docker (plantuml/plantuml)..."
    $ext = if ($Format -eq "txt") { "utxt" } else { $Format }

    $dockerTmp = Join-Path ([System.IO.Path]::GetTempPath()) ("plantuml_docker_" + [System.Guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $dockerTmp -Force | Out-Null
    try {
        Copy-Item -LiteralPath $SourcePath -Destination $dockerTmp -Force
        $inputFileName = [System.IO.Path]::GetFileName($SourcePath)

        # CJK font support: mount host font directories into container
        if ($Cjk) {
            $fontDirs = @()
            if ($env:WINDIR) { $fontDirs += "$env:WINDIR\Fonts" }
            foreach ($fd in @("C:\Windows\Fonts", "$env:SystemRoot\Fonts")) {
                if ($fd -and (Test-Path -LiteralPath $fd) -and $fontDirs -notcontains $fd) {
                    $fontDirs += $fd
                }
            }

            $fontMounted = $false
            $cjkDockerArgs = @("run", "--rm", "-v", "${dockerTmp}:/data")
            foreach ($fd in $fontDirs) {
                if (Test-Path -LiteralPath $fd) {
                    $cjkDockerArgs += "-v", "${fd}:/Windows/Fonts:ro"
                    $fontMounted = $true
                }
            }

            if ($fontMounted) {
                $cjkDockerArgs += @(
                    "--entrypoint", "sh",
                    "plantuml/plantuml:latest",
                    "-c", "fc-cache -f 2>/dev/null; plantuml -t$ext /data/$inputFileName"
                )
                Write-Host "  → CJK mode: mounting Windows fonts and refreshing font cache"
                try {
                    $proc = Start-Process -FilePath "docker" -ArgumentList $cjkDockerArgs `
                        -NoNewWindow -Wait -PassThru -RedirectStandardError "$dockerTmp\stderr.log"

                    if ($proc.ExitCode -eq 0) {
                        $generated = Get-ChildItem -Path $dockerTmp -Filter "*.$ext" -ErrorAction SilentlyContinue |
                                     Where-Object { $_.Name -ne $inputFileName } | Select-Object -First 1
                        if (-not $generated) {
                            $generated = Get-ChildItem -Path $dockerTmp -Filter "*.$Format" -ErrorAction SilentlyContinue |
                                         Where-Object { $_.Name -ne $inputFileName } | Select-Object -First 1
                        }
                        if ($generated) {
                            Move-Item -LiteralPath $generated.FullName -Destination $outputFile -Force
                            Write-Host "  ✓ Success (Docker + CJK)"
                            return $true
                        }
                    }
                } catch {
                    # fall through to standard Docker
                }
            } else {
                Write-Host "  ⚠ CJK mode: no host font directories found. CJK characters may not render correctly."
                Write-Host "    Install CJK fonts on your system, or place them in C:\Windows\Fonts"
            }
        }

        # Standard Docker rendering
        $proc = Start-Process -FilePath "docker" -ArgumentList @(
            "run", "--rm",
            "-v", "${dockerTmp}:/data",
            "plantuml/plantuml:latest",
            "-t$ext",
            "/data/$inputFileName"
        ) -NoNewWindow -Wait -PassThru -RedirectStandardError "$dockerTmp\stderr.log"

        if ($proc.ExitCode -eq 0) {
            $generated = Get-ChildItem -Path $dockerTmp -Filter "*.$ext" -ErrorAction SilentlyContinue |
                         Where-Object { $_.Name -ne $inputFileName } | Select-Object -First 1
            if (-not $generated) {
                $generated = Get-ChildItem -Path $dockerTmp -Filter "*.$Format" -ErrorAction SilentlyContinue |
                             Where-Object { $_.Name -ne $inputFileName } | Select-Object -First 1
            }
            if ($generated) {
                Move-Item -LiteralPath $generated.FullName -Destination $outputFile -Force
                Write-Host "  ✓ Success (Docker)"
                return $true
            }
        }
    } catch {
        # fall through
    } finally {
        if (Test-Path -LiteralPath $dockerTmp) {
            Remove-Item -LiteralPath $dockerTmp -Recurse -Force -ErrorAction SilentlyContinue
        }
    }

    Write-Host "  ✗ Docker conversion failed"
    return $false
}

function Convert-ViaLocal {
    param([string]$SourcePath = $InputPath)
    $candidates = @(
        (Join-Path $env:USERPROFILE   "plantuml.jar"),
        (Join-Path ${env:ProgramFiles} "PlantUML\plantuml.jar"),
        (Join-Path $env:LOCALAPPDATA  "PlantUML\plantuml.jar"),
        ".\plantuml.jar"
    )
    $jar = $null
    foreach ($p in $candidates) {
        if ($p -and (Test-Path -LiteralPath $p)) { $jar = $p; break }
    }
    if (-not $jar) {
        Write-Host "  → No local plantuml.jar found, skipping"
        return $false
    }
    if (-not (Test-Command "java")) {
        Write-Host "  → Java not available, skipping local JAR"
        return $false
    }

    Write-Host "  → Trying local JAR ($jar)..."
    $ext = if ($Format -eq "txt") { "utxt" } else { $Format }
    try {
        $proc = Start-Process -FilePath "java" -ArgumentList @(
            "-jar", "`"$jar`"", "-t$ext", "-o", "`"$OutputDir`"", "`"$SourcePath`""
        ) -NoNewWindow -Wait -PassThru
        if ($proc.ExitCode -eq 0) {
            Write-Host "  ✓ Success (local JAR)"
            return $true
        }
    } catch {
        # fall through
    }
    Write-Host "  ✗ Local JAR failed"
    return $false
}

# ═══════════════════════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════════════════════

Write-Host "🖼️  Converting $InputPath → $outputFile (format: $Format)"

# ── CJK Detection ────────────────────────────────────────────────────────────
if (-not $Cjk) {
    if (Detect-Cjk $InputPath) {
        Write-Host ""
        Write-Host "🔤 CJK (Chinese/Japanese/Korean) characters detected in input."
        Write-Host "   These may not render correctly without CJK font support."
        Write-Host "   Re-run with -Cjk to enable CJK rendering, or install CJK fonts."
        Write-Host "   Attempting to proceed anyway..."
        Write-Host ""
    }
}

# ── Prepare working copy ─────────────────────────────────────────────────────
$workCopy = $InputPath
$cjkCopy = $null
if ($Cjk) {
    Write-Host "🔤 CJK mode enabled: configuring CJK-compatible fonts"
    $cjkCopy = Prepare-PumlForCjk $InputPath
    $workCopy = $cjkCopy
}

# ── Render with aspect-ratio + A4-fit correction loop ────────────────────────
$renderOk = $false
$maxFixAttempts = 2
$fixAttempt = 0
$aspectDone = $false
$a4Tried = $false

while ($fixAttempt -le $maxFixAttempts) {
    # Render using the current working copy (local-first: Docker → JAR → opt-in server)
    if (-not (Convert-ViaDocker $workCopy)) {
        if (-not (Convert-ViaLocal $workCopy)) {
            if (-not (Convert-ViaServer $workCopy)) {
                Write-Host ""
                Write-Host "❌ All conversion methods failed."
                Write-Host "   Install options (local, recommended for privacy):"
                Write-Host "   1. Docker: docker pull plantuml/plantuml:latest"
                Write-Host "   2. Java + JAR: download plantuml.jar from https://plantuml.com/download"
                Write-Host "   Or, to use the public Kroki server (uploads diagram to kroki.io):"
                Write-Host "   3. Re-run with -UsePublicServer (review the privacy notice first)"
                Write-Host "      Override the host with `$env:PLANTUML_PUBLIC_SERVER = '<url>' if self-hosting"
                if ($cjkCopy) { Remove-Item -LiteralPath $cjkCopy -Force -ErrorAction SilentlyContinue }
                exit 1
            }
        }
    }
    $renderOk = $true

    if ($Format -in @("txt", "pdf")) { break }

    if (-not $NoFix -and -not $aspectDone) {
        $aspectOk = Test-AspectRatio $outputFile $Format
        if ($null -eq $aspectOk) {
            Write-Host "  ⓘ Could not determine image dimensions; skipping aspect ratio check."
            $aspectDone = $true
        } elseif (-not $aspectOk) {
            $fixAttempt++
            if ($fixAttempt -gt $maxFixAttempts) {
                Write-Host "  ⚠ Maximum fix attempts ($maxFixAttempts) reached. Manual adjustment may be needed."
                break
            }

            $w = if ($Format -eq "svg") { $script:svgWidth } else { $script:pngWidth }
            $h = if ($Format -eq "svg") { $script:svgHeight } else { $script:pngHeight }
            $problem = if ($h -gt $w) { "too_tall" } else { "too_wide" }

            $fixedPuml = Fix-PumlAspectRatio $workCopy $problem
            if (-not $fixedPuml) {
                Write-Host "  ✗ Auto-fix failed; using original diagram."
                break
            }

            if ($workCopy -ne $InputPath) {
                Remove-Item -LiteralPath $workCopy -Force -ErrorAction SilentlyContinue
            }
            $workCopy = $fixedPuml
            $aspectDone = $true
            Write-Host "  → Re-rendering with corrected layout..."
            continue
        }
        $aspectDone = $true
    }

    if (-not $NoA4Check -and -not $a4Tried) {
        $a4Ok = Test-A4Fit $outputFile $Format
        if ($null -eq $a4Ok) {
            Write-Host "  ⓘ Could not determine image dimensions; skipping A4 check."
            break
        } elseif (-not $a4Ok) {
            $fixAttempt++
            if ($fixAttempt -gt $maxFixAttempts) {
                Write-Host "  ⚠ Maximum fix attempts ($maxFixAttempts) reached; A4 fit may not hold."
                break
            }

            $a4Fixed = Fix-A4Fit $workCopy
            if (-not $a4Fixed) {
                Write-Host "  ✗ A4 auto-fit failed; using current diagram."
                $a4Tried = $true
                break
            }

            if ($workCopy -ne $InputPath) {
                Remove-Item -LiteralPath $workCopy -Force -ErrorAction SilentlyContinue
            }
            $workCopy = $a4Fixed
            $a4Tried = $true
            Write-Host "  → Re-rendering with A4-fit scale..."
            continue
        }
    }

    break
}

# ── Cleanup temp files ───────────────────────────────────────────────────────
if ($workCopy -ne $InputPath) {
    Remove-Item -LiteralPath $workCopy -Force -ErrorAction SilentlyContinue
}
if ($cjkCopy -and $cjkCopy -ne $workCopy) {
    Remove-Item -LiteralPath $cjkCopy -Force -ErrorAction SilentlyContinue
}

# ── Report ───────────────────────────────────────────────────────────────────
if ($renderOk) {
    Write-Host ""
    Write-Host "✅ Output: $outputFile"
    Write-Output $outputFile
}
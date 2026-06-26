# PowerShell fallback (Windows, no Python needed)

> Requires PowerShell 5.1+ (pre-installed on all Windows). Save the script below as `generate.ps1`.

## Usage

```powershell
# Text-to-image
powershell -File generate.ps1 -Prompt "a cute cat" -Size 1024x1024 -Quality low -Format jpeg

# Image edit (image-to-image)
powershell -File generate.ps1 -Prompt "add a hat" -Image .\cat.png -Format png

# Image edit with mask + transparent background
powershell -File generate.ps1 -Prompt "replace sky" -Image .\scene.png -Mask .\mask.png -Background transparent

# Multiple reference images (up to 16, total ≤ 50MB)
powershell -File generate.ps1 -Prompt "combine these" -Image .\a.png,.\b.png,.\c.png
```

## Parameters

- `-Prompt` (required, max 1000 chars)
- `-Size` — preset (`1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `2048x1152`, `3840x2160`, `2160x3840`, `auto`) or `WxH` (multiples of 16, max side 3840, ratio ≤ 3:1, total pixels 655360–8294400)
- `-Quality` — `low`/`medium`/`high`/`auto` (default `auto`)
- `-Format` — `png`/`jpeg`/`webp`
- `-N` — 1–10
- `-Model` — default `gpt-image-2`
- `-Image` — local file path(s) for edit (switches to `/images/edits`)
- `-Mask` — optional PNG mask for edit (≤ 4MB)
- `-Background` — `opaque`/`auto`/`transparent` (edit only)
- `-Moderation` — `low`/`auto` (edit only)

```powershell
<#
.SYNOPSIS
    Generate / edit images via WellAPI gpt-image-2 (Windows PowerShell fallback).
.DESCRIPTION
    Zero external dependencies. Uses Invoke-RestMethod (PS 5.1+).
    Response is synchronous; data[].b64_json is base64-decoded to a local file.
    Outputs MEDIA:<path> for OpenClaw auto-attach (one line per image).
#>
param(
    [string]$ApiKey = $env:WELLAPI_API_KEY,
    [Parameter(Mandatory)][string]$Prompt,
    [string]$Model = "gpt-image-2",
    [string]$Size = "auto",
    [ValidateSet("low", "medium", "high", "auto")]
    [string]$Quality = "auto",
    [ValidateSet("png", "jpeg", "webp")]
    [string]$Format = "png",
    [int]$N = 1,
    [string[]]$Image,
    [string]$Mask,
    [ValidateSet("opaque", "auto", "transparent")]
    [string]$Background,
    [ValidateSet("low", "auto")]
    [string]$Moderation,
    [string]$Out,
    [switch]$VerboseLog
)

$ErrorActionPreference = "Stop"

$MaxEditImages     = 16
$MaxEditTotalBytes = 50MB
$MaxMaskBytes      = 4MB
$MaxPromptChars    = 1000

if (-not $ApiKey) { $ApiKey = Read-Host "Enter WELLAPI_API_KEY" }
if (-not $ApiKey) { Write-Error "WELLAPI_API_KEY not provided."; exit 2 }

if ($Prompt.Length -gt $MaxPromptChars) {
    Write-Error "Prompt exceeds $MaxPromptChars chars."; exit 2
}
if ($N -lt 1 -or $N -gt 10) { Write-Error "-N must be 1..10."; exit 2 }

function Test-Size([string]$s) {
    $presets = @(
        "1024x1024","1536x1024","1024x1536",
        "2048x2048","2048x1152",
        "3840x2160","2160x3840","auto"
    )
    if ($presets -contains $s) { return }
    if ($s -notmatch '^(\d+)x(\d+)$') {
        throw "Invalid -Size '$s'. Use a preset or WxH."
    }
    $w = [int]$Matches[1]; $h = [int]$Matches[2]
    if ($w % 16 -ne 0 -or $h % 16 -ne 0) { throw "-Size $s: w/h must be multiples of 16." }
    if ([Math]::Max($w, $h) -gt 3840) { throw "-Size $s: longest side > 3840." }
    $ratio = [Math]::Max($w, $h) / [Math]::Min($w, $h)
    if ($ratio -gt 3.0) { throw "-Size ${s}: ratio $ratio exceeds 3:1." }
    $total = $w * $h
    if ($total -lt 655360 -or $total -gt 8294400) {
        throw "-Size ${s}: total pixels $total outside [655360, 8294400]."
    }
}
try { Test-Size $Size } catch { Write-Error $_; exit 2 }

$isEdit = [bool]($Image -and $Image.Count -gt 0)

if ($isEdit) {
    if ($Image.Count -gt $MaxEditImages) {
        Write-Error "Maximum $MaxEditImages reference images allowed."; exit 2
    }
    $totalBytes = 0
    foreach ($p in $Image) {
        if (-not (Test-Path -LiteralPath $p -PathType Leaf)) {
            Write-Error "Image file not found: $p"; exit 2
        }
        $totalBytes += (Get-Item -LiteralPath $p).Length
    }
    if ($totalBytes -gt $MaxEditTotalBytes) {
        Write-Error "Total image size $totalBytes bytes exceeds 50MB limit."; exit 2
    }
    if ($Mask) {
        if (-not (Test-Path -LiteralPath $Mask -PathType Leaf)) {
            Write-Error "Mask file not found: $Mask"; exit 2
        }
        if ((Get-Item -LiteralPath $Mask).Length -gt $MaxMaskBytes) {
            Write-Error "Mask exceeds 4MB limit."; exit 2
        }
    }
} else {
    if ($Mask -or $Background -or $Moderation) {
        Write-Warning "-Mask/-Background/-Moderation only apply to image edits; ignored."
    }
}

$apiBase = "https://wellapi.ai/v1"
$headers = @{
    "Authorization" = "Bearer $ApiKey"
    "User-Agent"    = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    "Accept"        = "application/json"
}

if ($VerboseLog) {
    $mode = if ($isEdit) { "edit (image-to-image)" } else { "text-to-image" }
    Write-Host "Mode: $mode"
    Write-Host "Model=$Model size=$Size quality=$Quality format=$Format n=$N"
}

function Get-ExtForFormat([string]$fmt) {
    switch ($fmt.ToLower()) {
        "jpeg" { ".jpg" }
        "jpg"  { ".jpg" }
        "webp" { ".webp" }
        default { ".png" }
    }
}

function Get-MimeForFile([string]$path) {
    switch ([System.IO.Path]::GetExtension($path).ToLower()) {
        ".png"  { "image/png" }
        ".jpg"  { "image/jpeg" }
        ".jpeg" { "image/jpeg" }
        ".webp" { "image/webp" }
        ".gif"  { "image/gif" }
        default { "application/octet-stream" }
    }
}

try {
    if ($isEdit) {
        $boundary = "----WellAPIBoundary$([guid]::NewGuid().ToString('N'))"
        $LF  = "`r`n"
        $enc = [System.Text.Encoding]::UTF8
        $ms  = New-Object System.IO.MemoryStream

        function Write-Field([string]$name, [string]$value) {
            $part = "--$boundary$LF" +
                    "Content-Disposition: form-data; name=`"$name`"$LF$LF" +
                    "$value$LF"
            $bytes = $enc.GetBytes($part)
            $ms.Write($bytes, 0, $bytes.Length)
        }

        function Write-File([string]$name, [string]$path) {
            $fileName = [System.IO.Path]::GetFileName($path)
            $mime     = Get-MimeForFile $path
            $head = "--$boundary$LF" +
                    "Content-Disposition: form-data; name=`"$name`"; filename=`"$fileName`"$LF" +
                    "Content-Type: $mime$LF$LF"
            $hb = $enc.GetBytes($head); $ms.Write($hb, 0, $hb.Length)
            $fb = [System.IO.File]::ReadAllBytes($path); $ms.Write($fb, 0, $fb.Length)
            $tb = $enc.GetBytes($LF); $ms.Write($tb, 0, $tb.Length)
        }

        Write-Field "model"   $Model
        Write-Field "prompt"  $Prompt
        Write-Field "n"       "$N"
        Write-Field "size"    $Size
        Write-Field "quality" $Quality
        Write-Field "format"  $Format
        if ($Background) { Write-Field "background" $Background }
        if ($Moderation) { Write-Field "moderation" $Moderation }

        foreach ($p in $Image) {
            $full = (Resolve-Path -LiteralPath $p).Path
            Write-File "image" $full
        }
        if ($Mask) {
            $maskFull = (Resolve-Path -LiteralPath $Mask).Path
            Write-File "mask" $maskFull
        }

        $tail = $enc.GetBytes("--$boundary--$LF")
        $ms.Write($tail, 0, $tail.Length)

        $bodyBytes = $ms.ToArray()
        $ms.Dispose()

        $headers["Content-Type"] = "multipart/form-data; boundary=$boundary"
        $resp = Invoke-RestMethod -Uri "$apiBase/images/edits" -Method POST `
            -Headers $headers -Body $bodyBytes -TimeoutSec 300
    }
    else {
        $body = @{
            model   = $Model
            prompt  = $Prompt
            n       = $N
            size    = $Size
            quality = $Quality
            format  = $Format
        } | ConvertTo-Json -Compress -Depth 5

        $resp = Invoke-RestMethod -Uri "$apiBase/images/generations" -Method POST `
            -Headers $headers -Body $body -ContentType "application/json" -TimeoutSec 300
    }
}
catch {
    Write-Error "API request failed: $_"
    exit 1
}

if (-not $resp.data -or $resp.data.Count -eq 0) {
    Write-Error "No image data in response: $($resp | ConvertTo-Json -Compress -Depth 5)"
    exit 1
}

$outputFormat = if ($resp.output_format) { $resp.output_format } else { $Format }
$ext   = Get-ExtForFormat $outputFormat
$total = $resp.data.Count

for ($i = 0; $i -lt $total; $i++) {
    $item = $resp.data[$i]
    if (-not $item.b64_json) { Write-Error "Missing b64_json in data[$i]"; exit 1 }

    if ($Out) {
        $rootBase = [System.IO.Path]::GetFileNameWithoutExtension($Out)
        $rootDir  = [System.IO.Path]::GetDirectoryName($Out)
        $givenExt = [System.IO.Path]::GetExtension($Out)
        $useExt   = if ($givenExt) { $givenExt } else { $ext }
        $name = if ($total -gt 1) { "$rootBase-$($i + 1)$useExt" } else { "$rootBase$useExt" }
        $outFile = if ($rootDir) { Join-Path $rootDir $name } else { $name }
    } else {
        $ts = Get-Date -Format "yyyyMMdd-HHmmss-fff"
        $suffix = if ($total -gt 1) { "-$($i + 1)" } else { "" }
        $outFile = "wellapi-$ts$suffix$ext"
    }
    $outFile = [System.IO.Path]::GetFullPath($outFile)

    try {
        $bytes = [System.Convert]::FromBase64String($item.b64_json)
        [System.IO.File]::WriteAllBytes($outFile, $bytes)
    }
    catch {
        Write-Error "Failed to decode/save image $($i + 1): $_"; exit 1
    }

    if ($VerboseLog) { Write-Host "Saved: $outFile ($($bytes.Length) bytes)" }
    Write-Output "MEDIA:$outFile"
}

exit 0
```

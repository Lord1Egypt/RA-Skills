<#
.SYNOPSIS
    从*.ProdData.txtrecipe提取凸轮数据填充到CoDeSys文本配方
.DESCRIPTION
    读取ProdData文件中的astTabData[2,*]位移数据，
    填充到CoDeSys文本格式的凸轮变量中。
.PARAMETER ProdDataFile
    ProdData文件路径（*.ProdData.txtrecipe）
.PARAMETER CoDeSysDir
    CoDeSys文本目录
.PARAMETER OutDir
    填充后输出目录
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File fill_cam_data.ps1 -ProdDataFile ".\data.ProdData.txtrecipe" -CoDeSysDir ".\codesys" -OutDir ".\filled"
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$ProdDataFile,
    
    [Parameter(Mandatory=$true)]
    [string]$CoDeSysDir,
    
    [Parameter(Mandatory=$true)]
    [string]$OutDir
)

$ErrorActionPreference = 'Stop'

if (!(Test-Path $ProdDataFile)) {
    Write-Error "ProdDataFile not found: $ProdDataFile"
    exit 1
}

if (!(Test-Path $CoDeSysDir)) {
    Write-Error "CoDeSysDir not found: $CoDeSysDir"
    exit 1
}

if (!(Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
}

Write-Host "Reading ProdData: $ProdDataFile"
$bytes = [System.IO.File]::ReadAllBytes($ProdDataFile)

# Parse header (same as ifa_to_codesys)
$pos = 0
$nameEnd = [Array]::IndexOf($bytes, [byte]0, $pos)
$recipeName = [System.Text.Encoding]::UTF8.GetString($bytes, $pos, $nameEnd - $pos)
$pos = $nameEnd + 1
$pos += 32  # skip schema checksum
$varCount = [BitConverter]::ToUInt32($bytes, $pos)
$pos += 4

Write-Host "Recipe: $recipeName, Variables: $varCount"

# Extract cam data variables (astTabData[2,*])
$camData = @{}
$varIndex = 0

while ($pos -lt $bytes.Length -and $varIndex -lt $varCount) {
    if ($pos + 2 -lt $bytes.Length -and $bytes[$pos] -eq 0x56 -and $bytes[$pos+1] -eq 0x30) {
        $markerLen = 3
        if ($pos + 3 -lt $bytes.Length -and $bytes[$pos+2] -eq 0x30) {
            $markerLen = 4
        }
        $pos += $markerLen
        
        $nameStart = $pos
        $nameEndIdx = [Array]::IndexOf($bytes, [byte]0, $pos)
        if ($nameEndIdx -lt 0) { break }
        $varName = [System.Text.Encoding]::UTF8.GetString($bytes, $nameStart, $nameEndIdx - $nameStart)
        $pos = $nameEndIdx + 1
        
        # Read value (try 8 bytes as double for cam data)
        if ($pos + 8 -le $bytes.Length) {
            $value = [BitConverter]::ToDouble($bytes, $pos)
            $pos += 8
            
            # Only store astTabData[2,*] (displacement data, not angle)
            if ($varName -match 'astTabData\[2,') {
                $camData[$varName] = [math]::Round($value, 6)
            }
        } else {
            $pos++
        }
        $varIndex++
    } else {
        $pos++
    }
}

Write-Host "Extracted $($camData.Count) cam data points"

# Copy CoDeSys files and fill cam data
$codFiles = Get-ChildItem $CoDeSysDir -Filter '*.txt' -File | Where-Object { $_.Name -ne '00_summary.txt' }

foreach ($file in $codFiles) {
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    $lines = $content -split "`r?`n"
    $modified = $false
    
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        if ($line -match '^(V0_?|V00_)(astTabData\[2,\d+\]):=(.+)$') {
            $fullVar = $Matches[2]
            if ($camData.ContainsKey($fullVar)) {
                $prefix = $Matches[1]
                $lines[$i] = "${prefix}${fullVar}:=$($camData[$fullVar])"
                $modified = $true
            }
        }
    }
    
    $outFile = Join-Path $OutDir $file.Name
    $utf8Bom = New-Object System.Text.UTF8Encoding $true
    [System.IO.File]::WriteAllLines($outFile, $lines, $utf8Bom)
    
    if ($modified) {
        Write-Host "  Filled: $($file.Name)"
    } else {
        Write-Host "  Copied (no cam data): $($file.Name)"
    }
}

Write-Host "`nFill complete. Output: $OutDir"

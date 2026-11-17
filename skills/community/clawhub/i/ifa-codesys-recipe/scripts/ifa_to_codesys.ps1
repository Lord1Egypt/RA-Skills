<#
.SYNOPSIS
    iFA二进制配方(.txtrecipe) → CoDeSys文本格式(.txt) 转换脚本
.DESCRIPTION
    扫描SrcDir下所有.txtrecipe文件，自动检测V0_/V00_标记类型，
    解码值并输出为 V0_varName:=value 或 V00_varName:=value 格式。
.PARAMETER SrcDir
    输入目录（包含.txtrecipe文件）
.PARAMETER OutDir
    输出目录
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File ifa_to_codesys.ps1 -SrcDir ".\input" -OutDir ".\output"
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$SrcDir,
    
    [Parameter(Mandatory=$true)]
    [string]$OutDir
)

$ErrorActionPreference = 'Stop'

if (!(Test-Path $SrcDir)) {
    Write-Error "SrcDir not found: $SrcDir"
    exit 1
}

if (!(Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
}

$files = Get-ChildItem $SrcDir -Filter '*.txtrecipe' -File
if ($files.Count -eq 0) {
    Write-Warning "No .txtrecipe files found in $SrcDir"
    exit 0
}

$summary = @()

foreach ($file in $files) {
    Write-Host "Processing: $($file.Name)"
    $bytes = [System.IO.File]::ReadAllBytes($file.FullName)
    
    # Parse header: recipeName + schemaChecksum(32bytes) + varCount(uint32_LE)
    $pos = 0
    
    # Read recipe name (null-terminated string)
    $nameEnd = [Array]::IndexOf($bytes, [byte]0, $pos)
    if ($nameEnd -lt 0) { $nameEnd = $bytes.Length }
    $recipeName = [System.Text.Encoding]::UTF8.GetString($bytes, $pos, $nameEnd - $pos)
    $pos = $nameEnd + 1
    
    # Skip schema checksum (32 bytes)
    $schemaChecksum = $bytes[$pos..($pos+31)]
    $pos += 32
    
    # Read variable count (uint32 LE)
    $varCount = [BitConverter]::ToUInt32($bytes, $pos)
    $pos += 4
    
    Write-Host "  Recipe: $recipeName, Variables: $varCount"
    
    # Detect marker type (V0_ or V00_)
    $markerType = 'V0_'
    $outputLines = @()
    
    # Parse data records
    $varIndex = 0
    while ($pos -lt $bytes.Length -and $varIndex -lt $varCount) {
        # Check for V0_ (0x56 0x30 0x5F) or V00_ (0x56 0x30 0x30 0x5F) marker
        if ($pos + 2 -lt $bytes.Length -and $bytes[$pos] -eq 0x56 -and $bytes[$pos+1] -eq 0x30) {
            if ($bytes[$pos+2] -eq 0x5F) {
                $markerType = 'V0_'
                $pos += 3
            } elseif ($pos + 3 -lt $bytes.Length -and $bytes[$pos+2] -eq 0x30 -and $bytes[$pos+3] -eq 0x5F) {
                $markerType = 'V00_'
                $pos += 4
            } else {
                $pos++
                continue
            }
            
            # Read variable name (null-terminated)
            $nameStart = $pos
            $nameEndIdx = [Array]::IndexOf($bytes, [byte]0, $pos)
            if ($nameEndIdx -lt 0) { break }
            $varName = [System.Text.Encoding]::UTF8.GetString($bytes, $nameStart, $nameEndIdx - $nameStart)
            $pos = $nameEndIdx + 1
            
            # Try to decode value (try sizes: 1, 2, 4, 8 bytes)
            $value = $null
            $valueSize = 4  # default
            
            # Try to determine type from IEC prefix
            if ($varName -match '^(INT|UINT|WORD)') {
                $valueSize = 2
                if ($pos + 2 -le $bytes.Length) {
                    $value = [BitConverter]::ToInt16($bytes, $pos)
                }
            } elseif ($varName -match '^(DINT|UDINT|DWORD|REAL)') {
                $valueSize = 4
                if ($pos + 4 -le $bytes.Length) {
                    if ($varName -match '^REAL') {
                        $value = [BitConverter]::ToSingle($bytes, $pos)
                        $value = [math]::Round($value, 4)
                    } else {
                        $value = [BitConverter]::ToInt32($bytes, $pos)
                    }
                }
            } elseif ($varName -match '^(LREAL|LINT|ULINT)') {
                $valueSize = 8
                if ($pos + 8 -le $bytes.Length) {
                    $value = [BitConverter]::ToDouble($bytes, $pos)
                    $value = [math]::Round($value, 6)
                }
            } elseif ($varName -match '^(BOOL|BYTE)') {
                $valueSize = 1
                if ($pos + 1 -le $bytes.Length) {
                    $value = if ($bytes[$pos] -ne 0) { 'TRUE' } else { 'FALSE' }
                }
            } elseif ($varName -match '^(STRING|WSTRING)') {
                # String: read until null
                $strEnd = [Array]::IndexOf($bytes, [byte]0, $pos)
                if ($strEnd -gt $pos) {
                    $value = "'" + [System.Text.Encoding]::UTF8.GetString($bytes, $pos, $strEnd - $pos) + "'"
                    $valueSize = $strEnd - $pos + 1
                } else {
                    $value = "''"
                    $valueSize = 1
                }
            } else {
                # Default: try 4 bytes as int
                $valueSize = 4
                if ($pos + 4 -le $bytes.Length) {
                    $value = [BitConverter]::ToInt32($bytes, $pos)
                }
            }
            
            if ($null -ne $value) {
                $outputLines += "${markerType}${varName}:=${value}"
                $pos += $valueSize
            }
            $varIndex++
        } else {
            $pos++
        }
    }
    
    # Write output file (UTF-8 with BOM)
    $outFile = Join-Path $OutDir ($file.BaseName + '.txt')
    $utf8Bom = New-Object System.Text.UTF8Encoding $true
    [System.IO.File]::WriteAllLines($outFile, $outputLines, $utf8Bom)
    
    $summary += [PSCustomObject]@{
        File = $file.Name
        Recipe = $recipeName
        Variables = $varIndex
        Marker = $markerType
        Output = $outFile
    }
    
    Write-Host "  Output: $outFile ($varIndex variables)"
}

# Write summary
$summaryFile = Join-Path $OutDir '00_summary.txt'
$summary | Format-Table -AutoSize | Out-String | Set-Content $summaryFile -Encoding UTF8
Write-Host "`nSummary written to: $summaryFile"
Write-Host "Total files processed: $($files.Count)"

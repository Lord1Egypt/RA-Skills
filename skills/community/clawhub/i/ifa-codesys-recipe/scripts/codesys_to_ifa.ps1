<#
.SYNOPSIS
    CoDeSys文本格式(.txt) → iFA二进制配方(.txtrecipe) 转换脚本
.DESCRIPTION
    扫描SrcDir下所有.txt文件，解析V0_varName:=value赋值，
    编码为iFA二进制格式。
.PARAMETER SrcDir
    输入目录（包含.txt文件）
.PARAMETER OutDir
    输出目录
.PARAMETER ConfigJson
    RecipeConfig.json路径（可选，自动查找）
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File codesys_to_ifa.ps1 -SrcDir ".\input" -OutDir ".\output"
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$SrcDir,
    
    [Parameter(Mandatory=$true)]
    [string]$OutDir,
    
    [string]$ConfigJson = ''
)

$ErrorActionPreference = 'Stop'

if (!(Test-Path $SrcDir)) {
    Write-Error "SrcDir not found: $SrcDir"
    exit 1
}

if (!(Test-Path $OutDir)) {
    New-Item -ItemType Directory -Path $OutDir -Force | Out-Null
}

# Find RecipeConfig.json
if ($ConfigJson -and (Test-Path $ConfigJson)) {
    $config = Get-Content $ConfigJson -Raw | ConvertFrom-Json
    Write-Host "Using ConfigJson: $ConfigJson"
} else {
    # Auto-find
    $found = Get-ChildItem $SrcDir -Recurse -Filter 'RecipeConfig.json' -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) {
        $config = Get-Content $found.FullName -Raw | ConvertFrom-Json
        Write-Host "Auto-found ConfigJson: $($found.FullName)"
    } else {
        Write-Warning "RecipeConfig.json not found. Schema checksum will be zero-filled."
        $config = $null
    }
}

$files = Get-ChildItem $SrcDir -Filter '*.txt' -File | Where-Object { $_.Name -ne '00_summary.txt' }
if ($files.Count -eq 0) {
    Write-Warning "No .txt files found in $SrcDir"
    exit 0
}

foreach ($file in $files) {
    Write-Host "Processing: $($file.Name)"
    
    # Read lines (handle UTF-8 BOM)
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    $lines = $content -split "`r?`n" | Where-Object { $_.Trim() -ne '' }
    
    # Extract recipe name from filename
    $recipeName = $file.BaseName
    
    # Build schema checksum (32 bytes)
    $schemaChecksum = New-Object byte[] 32
    if ($config -and $config.schemaChecksum) {
        $hexStr = $config.schemaChecksum
        for ($i = 0; $i -lt 32 -and $i * 2 -lt $hexStr.Length; $i++) {
            $schemaChecksum[$i] = [Convert]::ToByte($hexStr.Substring($i * 2, 2), 16)
        }
    }
    
    # Parse variable assignments
    $records = @()
    foreach ($line in $lines) {
        if ($line -match '^(V0_?|V00_)(.+?):=(.+)$') {
            $marker = $Matches[1]
            $varName = $Matches[2]
            $valueStr = $Matches[3].Trim()
            
            # Determine type from value
            $valueBytes = $null
            if ($valueStr -eq 'TRUE') {
                $valueBytes = [byte]@(1)
            } elseif ($valueStr -eq 'FALSE') {
                $valueBytes = [byte]@(0)
            } elseif ($valueStr -match "^'(.*)'$") {
                # String
                $strVal = $Matches[1]
                $valueBytes = [System.Text.Encoding]::UTF8.GetBytes($strVal) + [byte]@(0)
            } elseif ($valueStr -match '^-?\d+\.\d+$') {
                # Float (REAL/LREAL)
                $dblVal = [double]$valueStr
                $valueBytes = [BitConverter]::GetBytes($dblVal)
            } elseif ($valueStr -match '^-?\d+$') {
                # Integer
                $intVal = [int]$valueStr
                if ($intVal -ge -128 -and $intVal -le 127) {
                    $valueBytes = [byte]@([byte]($intVal -band 0xFF))
                } elseif ($intVal -ge -32768 -and $intVal -le 32767) {
                    $valueBytes = [BitConverter]::GetBytes([int16]$intVal)
                } else {
                    $valueBytes = [BitConverter]::GetBytes($intVal)
                }
            } else {
                Write-Warning "  Unknown value format: $valueStr for $varName"
                continue
            }
            
            # Build marker bytes
            $markerBytes = if ($marker -match 'V00') {
                [byte]@(0x56, 0x30, 0x30, 0x5F)
            } else {
                [byte]@(0x56, 0x30, 0x5F)
            }
            
            $varNameBytes = [System.Text.Encoding]::UTF8.GetBytes($varName) + [byte]@(0)
            
            $records += @{
                Marker = $markerBytes
                VarName = $varNameBytes
                Value = $valueBytes
            }
        }
    }
    
    # Build binary output
    $ms = New-Object System.IO.MemoryStream
    
    # Write recipe name (null-terminated)
    $nameBytes = [System.Text.Encoding]::UTF8.GetBytes($recipeName)
    $ms.Write($nameBytes, 0, $nameBytes.Length)
    $ms.WriteByte(0)
    
    # Write schema checksum (32 bytes)
    $ms.Write($schemaChecksum, 0, 32)
    
    # Write variable count (uint32 LE)
    $countBytes = [BitConverter]::GetBytes([uint32]$records.Count)
    $ms.Write($countBytes, 0, 4)
    
    # Write records
    foreach ($rec in $records) {
        $ms.Write($rec.Marker, 0, $rec.Marker.Length)
        $ms.Write($rec.VarName, 0, $rec.VarName.Length)
        $ms.Write($rec.Value, 0, $rec.Value.Length)
    }
    
    # Write output
    $outFile = Join-Path $OutDir ($recipeName + '.txtrecipe')
    [System.IO.File]::WriteAllBytes($outFile, $ms.ToArray())
    $ms.Close()
    
    Write-Host "  Output: $outFile ($($records.Count) variables)"
}

Write-Host "`nConversion complete. Total files: $($files.Count)"

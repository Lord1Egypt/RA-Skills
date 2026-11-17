<#
.SYNOPSIS
    Get-ImageFiles 白名单回归：通配符、文件夹、逗号分隔路径都不得收进非图片。
    直接点源（dot-source）脚本会因缺 Action 参数退出，所以这里内联同名同实现的副本做断言。
    改 scripts/kiri-engine.ps1 里的 Get-ImageFiles 时，必须同步改这里。
#>
$ErrorActionPreference = 'Stop'
$fails = 0
function Assert-True($cond, $msg) {
    if ($cond) { Write-Host "PASS  $msg" -ForegroundColor Green }
    else { Write-Host "FAIL  $msg" -ForegroundColor Red; $script:fails++ }
}

$script:ImageExtensions = @('.jpg', '.jpeg', '.png', '.tif', '.tiff')
function Get-ImageFiles {
    param([Parameter(Mandatory=$true)][string]$Spec)
    $accepted = New-Object System.Collections.Generic.List[System.IO.FileInfo]
    $rejected = New-Object System.Collections.Generic.List[string]
    $missing  = New-Object System.Collections.Generic.List[string]
    foreach ($token in ($Spec -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ })) {
        $candidates = @()
        if (Test-Path -LiteralPath $token -PathType Container) {
            $candidates = @(Get-ChildItem -LiteralPath $token -File -Recurse)
        } else {
            $candidates = @(Get-ChildItem -Path $token -File -ErrorAction SilentlyContinue)
            if ($candidates.Count -eq 0 -and -not (Test-Path -LiteralPath $token)) { $missing.Add($token); continue }
        }
        foreach ($f in $candidates) {
            if ($script:ImageExtensions -contains $f.Extension.ToLower()) { $accepted.Add($f) } else { $rejected.Add($f.FullName) }
        }
    }
    return @{ Accepted = @($accepted | Sort-Object FullName -Unique); Rejected = @($rejected); Missing = @($missing) }
}

$root = Join-Path ([IO.Path]::GetTempPath()) ("kiri-filter-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path (Join-Path $root 'sub') -Force | Out-Null
foreach ($n in 'a.jpg','b.JPG','c.jpeg','d.png','e.tif','f.tiff') { Set-Content (Join-Path $root $n) 'x' }
foreach ($n in 'notes.txt','model.obj','secret.json','clip.mp4') { Set-Content (Join-Path $root $n) 'x' }
Set-Content (Join-Path $root 'sub\g.png') 'x'
Set-Content (Join-Path $root 'sub\readme.md') 'x'

try {
    # 1. 通配符 *.* 不得带上非图片
    $r = Get-ImageFiles -Spec (Join-Path $root '*.*')
    $names = @($r.Accepted | ForEach-Object { $_.Name.ToLower() })
    Assert-True (($r.Rejected).Count -ge 4) "wildcard *.* rejects non-images (got $($r.Rejected.Count))"
    Assert-True ($names -notcontains 'notes.txt' -and $names -notcontains 'model.obj' -and $names -notcontains 'secret.json' -and $names -notcontains 'clip.mp4') "wildcard accepted set has no non-image"
    Assert-True ($names -contains 'a.jpg' -and $names -contains 'b.jpg' -and $names -contains 'c.jpeg' -and $names -contains 'd.png' -and $names -contains 'e.tif' -and $names -contains 'f.tiff') "wildcard keeps all 6 image extensions (case-insensitive)"

    # 2. 文件夹递归，子目录图片要进、markdown 要出
    $r = Get-ImageFiles -Spec $root
    $names = @($r.Accepted | ForEach-Object { $_.Name.ToLower() })
    Assert-True ($names -contains 'g.png') "directory recurse includes sub\g.png"
    Assert-True (@($r.Rejected | Where-Object { $_ -like '*readme.md' }).Count -eq 1) "directory recurse rejects readme.md"
    Assert-True ($names.Count -eq 7) "directory yields exactly 7 images (got $($names.Count))"

    # 3. 显式文件路径：图片收、非图片拒
    $r = Get-ImageFiles -Spec ((Join-Path $root 'a.jpg') + ',' + (Join-Path $root 'secret.json'))
    Assert-True (@($r.Accepted).Count -eq 1 -and $r.Accepted[0].Name -eq 'a.jpg') "explicit list keeps only a.jpg"
    Assert-True (@($r.Rejected).Count -eq 1) "explicit list rejects secret.json"

    # 4. 不存在的路径进 Missing，不抛异常
    $r = Get-ImageFiles -Spec (Join-Path $root 'no-such-dir\*.jpg')
    Assert-True (@($r.Missing).Count -eq 1) "missing path is reported, not thrown"
    Assert-True (@($r.Accepted).Count -eq 0) "missing path accepts nothing"
}
finally {
    Remove-Item $root -Recurse -Force -ErrorAction SilentlyContinue
}

if ($fails -gt 0) { Write-Host "`n$fails FAILED" -ForegroundColor Red; exit 1 }
Write-Host "`nALL PASSED" -ForegroundColor Green

# scripts/gen-index.ps1 - INDEX.md generator for meta-logic-method
# Extracts all rule headings (M-* / S-* / W-* / F-* / B-* / R-*) from md files and writes INDEX.md.
# ID formats: M-1..M-10, M-T1/M-P1/M-L1, S-1.1, W-1.1, F-1, B-1, R-1
# Usage: pwsh scripts/gen-index.ps1

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$idRx = '(M-[TPL]\d+|M-\d+|S-\d+(?:\.\d+)?|W-\d+(?:\.\d+)?|F-\d+|B-\d+|R-\d+(?:\.\d+)?)'

$files = Get-ChildItem -Path $root -Recurse -File -Filter *.md |
    Where-Object { $_.Name -notin @('INDEX.md', 'CHANGELOG.md') }

$rows = [System.Collections.Generic.List[object]]::new()
foreach ($f in $files) {
    foreach ($line in Get-Content $f.FullName) {
        if ($line -notmatch '^#{1,4}\s') { continue }
        # 定义必须以编号开头（行首锚定），避免正文提及被误捕获
        $m = [regex]::Match(($line -replace '^#{1,4}\s+', ''), ('^' + $idRx))
        if (-not $m.Success) { continue }
        $id = $m.Value
        $level = if ($line -match '【([^】]+)】') { $Matches[1] } else { '' }
        $title = ($line -replace '^#{1,4}\s+', '' -replace '^' + $idRx, '' -replace '【[^】]*】', '')
        $title = $title.Trim(' .-_—')
        $rel = $f.FullName.Substring($root.Length + 1).Replace('\', '/')
        $rows.Add([pscustomobject]@{ Id = $id; Level = $level; Title = $title; File = $rel })
    }
}

function Group-Table($items, $heading) {
    $out = [System.Text.StringBuilder]::new()
    [void]$out.AppendLine("## $heading")
    [void]$out.AppendLine()
    [void]$out.AppendLine('| 编号 | 等级 | 标题 | 所在文件 |')
    [void]$out.AppendLine('| --- | --- | --- | --- |')
    foreach ($r in $items) {
        [void]$out.AppendLine("| $($r.Id) | $($r.Level) | $($r.Title) | $($r.File) |")
    }
    [void]$out.AppendLine()
    return $out.ToString()
}

$main = $rows | Where-Object { $_.Id -match '^M-\d+$' }    | Sort-Object { [int]($_.Id -replace '\D', '') }
$mt   = $rows | Where-Object { $_.Id -match '^M-T\d+$' }   | Sort-Object { [int]($_.Id -replace '\D', '') }
$mp   = $rows | Where-Object { $_.Id -match '^M-P\d+$' }   | Sort-Object { [int]($_.Id -replace '\D', '') }
$ml   = $rows | Where-Object { $_.Id -match '^M-L\d+$' }   | Sort-Object { [int]($_.Id -replace '\D', '') }
$s    = $rows | Where-Object { $_.Id -match '^S-\d+(\.\d+)?$' } |
    Sort-Object { [int](($_.Id -replace '^[A-Z]-', '') -replace '\..*$', '') }, { if ($_.Id -match '\.(\d+)$') { [int]$Matches[1] } else { 0 } }
$w    = $rows | Where-Object { $_.Id -match '^W-\d+(\.\d+)?$' } |
    Sort-Object { [int](($_.Id -replace '^[A-Z]-', '') -replace '\..*$', '') }, { if ($_.Id -match '\.(\d+)$') { [int]$Matches[1] } else { 0 } }
$f    = $rows | Where-Object { $_.Id -match '^F-\d+$' }    | Sort-Object { [int]($_.Id -replace '\D', '') }
$b    = $rows | Where-Object { $_.Id -match '^B-\d+$' }    | Sort-Object { [int]($_.Id -replace '\D', '') }
$r    = $rows | Where-Object { $_.Id -match '^R-\d+(\.\d+)?$' } |
    Sort-Object { [int](($_.Id -replace '^[A-Z]-', '') -replace '\..*$', '') }, { if ($_.Id -match '\.(\d+)$') { [int]$Matches[1] } else { 0 } }

$content = [System.Text.StringBuilder]::new()
[void]$content.AppendLine('# INDEX — 编号总索引')
[void]$content.AppendLine('')
[void]$content.AppendLine('> 本文件由 `scripts/gen-index.ps1` 自动生成，**勿手改**；体系修订后重新运行脚本。')
[void]$content.AppendLine("> 规则等级：元法 > 强制/禁止 > 建议 > 可选（README 第三节）。共 $($rows.Count) 条。")
[void]$content.AppendLine('')
[void]$content.AppendLine((Group-Table $main '一、元法则总纲（M-1 ~ M-10）'))
[void]$content.AppendLine((Group-Table $mt   '二、思维链法则细则（M-T）'))
[void]$content.AppendLine((Group-Table $mp   '三、前提与概念法则细则（M-P）'))
[void]$content.AppendLine((Group-Table $ml   '四、层次与调度法则细则（M-L）'))
[void]$content.AppendLine((Group-Table $s    '五、子思维技能（S）'))
[void]$content.AppendLine((Group-Table $w    '六、思维流程（W）'))
[void]$content.AppendLine((Group-Table $f    '七、思维谬误（F）'))
[void]$content.AppendLine((Group-Table $b    '八、认知偏误（B）'))
[void]$content.AppendLine((Group-Table $r    '九、输出模板（R）'))

# 输出统一使用 LF 行尾（与其余文档一致），UTF-8 无 BOM
$lfContent = $content.ToString() -replace "`r`n", "`n"
[System.IO.File]::WriteAllText((Join-Path $root 'INDEX.md'), $lfContent, [System.Text.UTF8Encoding]::new($false))
Write-Host "INDEX.md generated: $($rows.Count) rules (M=$($main.Count) MT=$($mt.Count) MP=$($mp.Count) ML=$($ml.Count) S=$($s.Count) W=$($w.Count) F=$($f.Count) B=$($b.Count) R=$($r.Count))"

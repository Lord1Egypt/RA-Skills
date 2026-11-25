$ErrorActionPreference = 'Stop'
$apgDir = 'corpus/ui-ux-design/usability-accessibility/docs/apg'
$dialogFile = 'corpus/ui-ux-design/usability-accessibility/docs/aria-apg-dialog-modal.md'
$kbFile = 'output/ui-ux-design-expert/kb/aria-patterns.md'
$slugs = @('accordion','alert','alertdialog','breadcrumb','button','carousel','checkbox','combobox','__dialog','disclosure','feed','grid','landmarks','link','listbox','menubar','menu-button','meter','radio','slider','slider-multithumb','spinbutton','switch','table','tabs','toolbar','tooltip','treeview','treegrid','window-splitter')

$kbLines = Get-Content $kbFile
$kbBlocks = @{}
$cur = $null
foreach ($line in $kbLines) {
  if ($line -match '^### (\d+)\. ') { $cur = [int]$Matches[1] - 1; $kbBlocks[$cur] = @() }
  elseif ($null -ne $cur) { $kbBlocks[$cur] += $line }
}

$keyPat = [regex]'Enter|Space|Tab|Esc(ape)?|Home|End|Page ?(Up|Down)|F\d{1,2}|Shift|Ctrl|Control|Alt|←|→|↑|↓|可打印字符'
function Normalize-Keys($text) {
  $set = @{}
  foreach ($m in $keyPat.Matches($text)) {
    $k = $m.Value
    if ($k -eq 'Escape') { $k = 'Esc' }
    if ($k -eq 'Control') { $k = 'Ctrl' }
    if ($k -eq 'Page Up') { $k = 'PageUp' }
    if ($k -eq 'Page Down') { $k = 'PageDown' }
    $set[$k] = $true
  }
  return $set
}
$rolePat = [regex]'role=`?"(\w+)"'

foreach ($i in 0..29) {
  $slug = $slugs[$i]
  $file = if ($slug -eq '__dialog') { $dialogFile } else { Join-Path $apgDir "$slug.md" }
  if (-not (Test-Path $file)) { Write-Output "[$($i+1)] MISSING FILE: $file"; continue }
  $raw = Get-Content $file -Raw
  $kbText = ($kbBlocks[$i] -join "`n")
  $corpusKbSection = ''
  $inKb = $false
  foreach ($line in ($raw -split "`n")) {
    if ($line -match '^## ') { $inKb = ($line -match 'Keyboard') }
    elseif ($inKb) { $corpusKbSection += $line + "`n" }
  }
  $kbKeys = Normalize-Keys $kbText
  $corpusKeys = Normalize-Keys $corpusKbSection
  $missingKeys = @($corpusKeys.Keys | Where-Object { -not $kbKeys.ContainsKey($_) })

  $kbRoles = @{}
  foreach ($m in $rolePat.Matches($kbText)) { $kbRoles[$m.Groups[1].Value] = $true }
  $corpusRoles = @{}
  $inAria = $false
  foreach ($line in ($raw -split "`n")) {
    if ($line -match '^## ') { $inAria = ($line -match 'ARIA') }
    elseif ($inAria) { foreach ($m in $rolePat.Matches($line)) { $corpusRoles[$m.Groups[1].Value] = $true } }
  }
  $missingRoles = @($corpusRoles.Keys | Where-Object { -not $kbRoles.ContainsKey($_) })

  if ($missingKeys.Count -or $missingRoles.Count) {
    Write-Output "[$($i+1)] $slug keys-missing: [$($missingKeys -join ' ')] roles-missing: [$($missingRoles -join ' ')]"
  }
}

param(
  [Parameter(Mandatory = $false)][string]$Repo = ".",
  [Parameter(Mandatory = $false)][string]$Range = "HEAD~3..HEAD",
  [Parameter(Mandatory = $false)][string]$JsonPath,
  [Parameter(Mandatory = $false)][string]$HtmlPath,
  [Parameter(Mandatory = $false)][switch]$Open,
  [Parameter(Mandatory = $false)][switch]$ValidateOnly
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillDir = Split-Path -Parent $scriptDir

function ResolveAbs([string]$p) {
  if ([string]::IsNullOrWhiteSpace($p)) { return $null }
  return (Resolve-Path -LiteralPath $p).Path
}

function EnsureDir([string]$p) {
  New-Item -ItemType Directory -Force -Path $p | Out-Null
}

function ReadJsonUtf8([string]$p) {
  $raw = Get-Content -Raw -Encoding UTF8 $p
  return ($raw | ConvertFrom-Json)
}

function ValidateReviewJson($data) {
  if ($null -eq $data) { throw "[run_review] invalid json: empty" }
  if ($null -eq $data.commits) { throw "[run_review] invalid json: missing commits" }

  foreach ($c in @($data.commits)) {
    if ($null -eq $c) { continue }
    $findings = @()
    if ($null -ne $c.findings) { $findings = @($c.findings) }
    foreach ($f in $findings) {
      if ($null -eq $f) { continue }
      if ([string]::IsNullOrWhiteSpace([string]$f.code)) {
        throw "[run_review] finding '$($f.title)' missing code"
      }
      if ([string]::IsNullOrWhiteSpace([string]$f.fix_code)) {
        throw "[run_review] finding '$($f.title)' missing fix_code"
      }
    }
  }
}

function FindPython() {
  $cmd = Get-Command python -ErrorAction SilentlyContinue
  if ($null -ne $cmd) { return $cmd.Source }
  $cmd = Get-Command python3 -ErrorAction SilentlyContinue
  if ($null -ne $cmd) { return $cmd.Source }
  return $null
}

$repoAbs = ResolveAbs $Repo
if ($null -eq $repoAbs) { throw "[run_review] repo not found: $Repo" }

$reportDir = Join-Path $repoAbs ".code-reviews"
EnsureDir $reportDir

$ts = Get-Date -Format "yyyyMMdd_HHmmss"

if ([string]::IsNullOrWhiteSpace($JsonPath)) {
  $JsonPath = Join-Path $reportDir ("review_" + $ts + ".json")
}

if ([string]::IsNullOrWhiteSpace($HtmlPath)) {
  $HtmlPath = Join-Path $reportDir ("review_" + $ts + ".html")
}

$jsonAbs = $JsonPath
if (-not [System.IO.Path]::IsPathRooted($jsonAbs)) {
  $jsonAbs = Join-Path $repoAbs $jsonAbs
}
$htmlAbs = $HtmlPath
if (-not [System.IO.Path]::IsPathRooted($htmlAbs)) {
  $htmlAbs = Join-Path $repoAbs $htmlAbs
}

if (-not (Test-Path -LiteralPath $jsonAbs)) {
  $py = FindPython
  $makePy = Join-Path $skillDir "scripts\\make_review_json.py"
  $makePs = Join-Path $skillDir "scripts\\make_review_json.ps1"
  if (($null -ne $py) -and (Test-Path -LiteralPath $makePy)) {
    & $py -X utf8 $makePy --repo $repoAbs --range $Range --out $jsonAbs
    if ($LASTEXITCODE -ne 0) { throw "[run_review] make_review_json.py failed ($LASTEXITCODE)" }
  } elseif (Test-Path -LiteralPath $makePs) {
    & $makePs -Repo $repoAbs -Range $Range -Out $jsonAbs
    if ($LASTEXITCODE -ne 0) { throw "[run_review] make_review_json.ps1 failed ($LASTEXITCODE)" }
  } else {
    throw "[run_review] cannot generate json template (missing make_review_json.*)"
  }
}

$null = ResolveAbs $jsonAbs

$data = ReadJsonUtf8 $jsonAbs
ValidateReviewJson $data

if ($ValidateOnly) {
  Write-Output $jsonAbs
  exit 0
}

$py = FindPython
$renderPy = Join-Path $skillDir "scripts\\render_report.py"
$renderPs = Join-Path $skillDir "scripts\\render_report.ps1"

if (($null -ne $py) -and (Test-Path -LiteralPath $renderPy)) {
  & $py -X utf8 $renderPy $jsonAbs $htmlAbs
  if ($LASTEXITCODE -ne 0) { throw "[run_review] render_report.py failed ($LASTEXITCODE)" }
} elseif (Test-Path -LiteralPath $renderPs) {
  & $renderPs -InputJson $jsonAbs -OutputHtml $htmlAbs
  if ($LASTEXITCODE -ne 0) { throw "[run_review] render_report.ps1 failed ($LASTEXITCODE)" }
} else {
  throw "[run_review] cannot render html (missing render_report.*)"
}

if ($Open) {
  Start-Process $htmlAbs | Out-Null
}

Write-Output $htmlAbs

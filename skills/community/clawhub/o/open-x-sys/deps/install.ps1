# OpenXSys installer for Windows (Windows PowerShell 5.1 and PowerShell 7).
#
#   powershell -ExecutionPolicy Bypass -File skills\open-x-sys\deps\install.ps1 [options]
#
# It installs the OpenXSys skill and the dependencies pinned in openxsys.lock.json.
# One install, one consent: it shows what it will do, asks once, then does it.
# Nothing is installed that fails verification. Nothing updates itself later.
#
# Options (the same as install.sh, in PowerShell form):
#   -HostName <name>    claude-code | codex | agents   (default: detected)
#   -Dir <path>         install into this skills directory
#   -Lang zh-CN         install the complete Chinese edition as open-x-sys
#   -Project            install into the current project instead of the home directory
#   -Without <id,...>   leave out dependencies by their id in the lock file
#   -NoLibraries        skip offline copies of page libraries
#   -DepsOnly           install dependencies for an already installed OpenXSys
#   -IncludePending     also install entries that are not yet approved (reviewers, testers)
#   -Yes                do not prompt
#   -Check              change nothing; report what is installed and what is missing
#   -Uninstall          remove OpenXSys; list the dependencies it installed

[CmdletBinding()]
param(
  [string]$HostName = '',
  [string]$Dir = '',
  [string]$Lang = 'en',
  [switch]$Project,
  [string[]]$Without = @(),
  [switch]$NoLibraries,
  [switch]$DepsOnly,
  [switch]$IncludePending,
  [switch]$Yes,
  [switch]$Check,
  [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
$skillSrc = Split-Path -Parent $here
$lockPath = Join-Path $here 'openxsys.lock.json'
$utf8 = New-Object System.Text.UTF8Encoding($false)

function Say([string]$text) { Write-Output $text }
function Have([string]$name) { return [bool](Get-Command $name -ErrorAction SilentlyContinue) }

function Ask([string]$question) {
  if ($Yes) { return $true }
  if (-not [Environment]::UserInteractive) {
    Say "No terminal to ask on; treating as 'no'. Pass -Yes to proceed without prompts."
    return $false
  }
  try { $reply = Read-Host "$question [y/N]" } catch { return $false }
  return ($reply -match '^(y|yes)$')
}

# ---------- where things are ----------

$repo = ''
$maybeRepo = Join-Path $skillSrc '..\..'
if ((Test-Path (Join-Path $maybeRepo 'README.md')) -and (Test-Path (Join-Path $maybeRepo 'skills'))) {
  $repo = (Resolve-Path $maybeRepo).Path
}

$home_ = $env:USERPROFILE
if (-not $Dir) {
  if (-not $HostName) {
    if (Test-Path (Join-Path $home_ '.claude')) { $HostName = 'claude-code' }
    elseif (Test-Path (Join-Path $home_ '.codex')) { $HostName = 'codex' }
    else { $HostName = 'agents' }
  }
  if ($Project) { $base = (Get-Location).Path } else { $base = $home_ }
  switch ($HostName) {
    'claude-code' { $Dir = Join-Path $base '.claude\skills' }
    'codex'       { $Dir = Join-Path $base '.codex\skills' }
    'agents'      { $Dir = Join-Path $base '.agents\skills' }
    default { throw "Unknown host '$HostName'. Use claude-code, codex or agents, or pass -Dir." }
  }
} elseif (-not $HostName) { $HostName = 'custom' }

$target = Join-Path $Dir 'open-x-sys'
$record = Join-Path $target 'deps\installed.json'

function IsLink([string]$path) {
  if (-not (Test-Path $path)) { return $false }
  return [bool]((Get-Item $path -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)
}

# ---------- runtimes ----------

$gitOk = Have 'git'
$nodeV = ''; $nodeOk = $false
if (Have 'node') {
  try { $nodeV = ((& node --version) -replace '^v', '').Trim() } catch { $nodeV = '' }
  if ($nodeV -match '^(\d+)\.(\d+)') {
    $maj = [int]$Matches[1]; $min = [int]$Matches[2]
    if ($maj -gt 22 -or ($maj -eq 22 -and $min -ge 20)) { $nodeOk = $true }
  }
}
$py = ''; $pyV = ''
foreach ($c in @('python', 'python3', 'py')) {
  if (-not (Have $c)) { continue }
  try {
    $out = & $c -c "import sys; print('%d.%d.%d' % sys.version_info[:3]) if sys.version_info >= (3, 10) else sys.exit(1)" 2>$null
    if ($LASTEXITCODE -eq 0 -and $out) { $py = $c; $pyV = ("$out").Trim(); break }
  } catch { }
}

# ---------- read the lock file ----------

if (-not (Test-Path $lockPath)) { throw "Lock file not found: $lockPath" }
$lock = [IO.File]::ReadAllText($lockPath, $utf8) | ConvertFrom-Json
$cliVersion = $lock.cli.version

function Wanted([string]$id, [string]$status) {
  if ($Without -contains $id) { return $false }
  if ($status -eq 'approved') { return $true }
  if ($IncludePending) { return $true }
  return $false
}

# ---------- show ----------

function ShowPlan {
  Say 'OpenXSys installer'
  Say ''
  Say "  Skills directory : $Dir  (host: $HostName)"
  if (-not $DepsOnly) {
    if ($repo) { Say "  OpenXSys edition : $Lang, with the Playground" }
    else { Say '  OpenXSys edition : (not in a repository checkout; dependencies only)' }
  }
  Say ''
  Say '  Runtimes'
  if ($gitOk) { Say '    git      present' } else { Say '    git      MISSING  (needed to fetch pinned skills)' }
  if ($nodeOk) { Say "    Node.js  $nodeV" }
  elseif ($nodeV) { Say "    Node.js  $nodeV  (22.20 or later adds: video with Remotion, the skills CLI)" }
  else { Say '    Node.js  missing  (adds: video with Remotion, the skills CLI)' }
  if ($py) { Say "    Python   $pyV" } else { Say "    Python   missing  (adds: Manim animation; scripts in the document skills)" }
  Say ''
  Say '  Skills (each fetched at its pinned commit and verified by git tree id)'
  foreach ($e in $lock.skills) {
    foreach ($s in $e.skills) {
      if (Wanted $e.id $e.review.status) { $mark = 'install' } else { $mark = 'skip   ' }
      Say ('    {0}  {1,-26} {2,-9} {3}@{4}' -f $mark, $s.name, $e.review.status, $e.url, $e.commit.Substring(0, 12))
    }
  }
  Say ''
  Say '  Page libraries (offline copies, each file verified by SHA-256)'
  foreach ($l in $lock.libraries) {
    foreach ($f in $l.files) {
      if ((-not $NoLibraries) -and (Wanted $l.id $l.review.status)) { $mark = 'install' } else { $mark = 'skip   ' }
      Say ('    {0}  {1,-26} {2,-9} {3}' -f $mark, ($l.package + '@' + $l.version), $l.review.status, $f.path)
    }
  }
  Say ''
  Say '  Licenses and conditions (full text: deps/DEPENDENCIES.md)'
  Say '    - Remotion is free for individuals and small teams; companies above a team-size'
  Say '      threshold need a paid company license: https://remotion.dev/license'
  Say "    - Anthropic's document skills (pptx, docx, pdf, xlsx) carry their own license terms."
  Say '    - GSAP is free to use under its own standard license (not an OSI license).'
  Say '    - D3 (ISC); Scrollama, KaTeX, Mermaid, Three.js (MIT); MapLibre GL JS (BSD-3-Clause).'
  Say "    - The skills CLI is run at version $cliVersion with its telemetry turned off."
  Say ''
  if ($IncludePending) {
    Say "  -IncludePending is set: entries marked 'pending' have NOT been reviewed."
    Say '  Their pins and checksums are real, but nobody has yet read the pinned content in full.'
  } else {
    Say "  Entries marked 'pending' are candidates awaiting review and are skipped."
  }
  Say ''
}

# ---------- check ----------

if ($Check) {
  ShowPlan
  if (Test-Path (Join-Path $target 'SKILL.md')) { Say "  OpenXSys is installed at $target" } else { Say "  OpenXSys is not installed at $target" }
  if (Test-Path $record) { Say "  Install record: $record" }
  foreach ($e in $lock.skills) {
    foreach ($s in $e.skills) {
      if (Test-Path (Join-Path $Dir (Join-Path $s.name 'SKILL.md'))) { Say "    present  $($s.name)" } else { Say "    absent   $($s.name)" }
    }
  }
  exit 0
}

# ---------- uninstall ----------

if ($Uninstall) {
  if (-not (Test-Path $target)) { Say "OpenXSys is not installed at $target."; exit 0 }
  Say "This removes $target."
  Say 'Your systems (~\.openxsys\ and any <project>\.openxsys\) are yours and are not touched.'
  if (Test-Path $record) {
    try {
      $rec = [IO.File]::ReadAllText($record, $utf8) | ConvertFrom-Json
      if ($rec.skills) {
        Say 'Dependencies this installer added (remove each yourself if you no longer want it):'
        foreach ($s in $rec.skills) { Say ("    {0}   ->   Remove-Item -Recurse -Force `"{1}`"   (or: npx skills remove {0} -g)" -f $s.name, (Join-Path $Dir $s.name)) }
      }
    } catch { }
  }
  if (Ask 'Remove OpenXSys now?') {
    if (IsLink $target) { (Get-Item $target -Force).Delete() } else { Remove-Item -Recurse -Force -Confirm:$false $target }
    Say 'Removed. If you added the OpenXSys line to your host instructions, remove that line too.'
  } else { Say 'Nothing was removed.' }
  exit 0
}

# ---------- consent ----------

ShowPlan
if (-not (Ask 'Install as shown?')) { Say 'Nothing was installed.'; exit 0 }

$installedSkills = @()
$installedLibs = @()
$skipped = @()

# ---------- 1. OpenXSys itself ----------

if ((-not $DepsOnly) -and $repo) {
  switch ($Lang) {
    'en'    { $src = Join-Path $repo 'skills\open-x-sys' }
    'zh-CN' { $src = Join-Path $repo 'skills\open-x-sys.zh-CN' }
    'zh'    { $src = Join-Path $repo 'skills\open-x-sys.zh-CN' }
    default { throw "Unknown edition '$Lang' (use en or zh-CN)." }
  }
  if (-not (Test-Path (Join-Path $src 'SKILL.md'))) { throw "Edition not found: $src" }
  if (-not (Test-Path $Dir)) { New-Item -ItemType Directory -Force $Dir | Out-Null }
  if (IsLink $target) {
    Say "  $target is a link (a development setup). Left as it is."
  } else {
    $keep = Join-Path $Dir '.openxsys-lib-keep'
    $doCopy = $true
    if (Test-Path $target) {
      if (Ask "  $target already exists. Replace it with this version?") {
        $oldLib = Join-Path $target 'display\lib'
        if (Test-Path $oldLib) { Move-Item $oldLib $keep }
        Remove-Item -Recurse -Force -Confirm:$false $target
      } else { Say '  Kept the existing install.'; $doCopy = $false }
    }
    if ($doCopy) {
      Copy-Item -Recurse $src $target
      $depsDir = Join-Path $target 'deps'
      if (-not (Test-Path $depsDir)) { New-Item -ItemType Directory -Force $depsDir | Out-Null }
      foreach ($f in @('openxsys.lock.json', 'install.sh', 'install.ps1')) { Copy-Item -Force (Join-Path $here $f) $depsDir }
      if (Test-Path $keep) {
        $disp = Join-Path $target 'display'
        if (-not (Test-Path $disp)) { New-Item -ItemType Directory -Force $disp | Out-Null }
        Move-Item $keep (Join-Path $disp 'lib')
      }
      $pg = Join-Path $repo 'playground'
      if (Test-Path $pg) {
        $pgTarget = Join-Path $target 'playground'
        if (Test-Path $pgTarget) { Remove-Item -Recurse -Force -Confirm:$false $pgTarget }
        Copy-Item -Recurse $pg $pgTarget
      }
      Say "  Installed OpenXSys ($Lang) at $target"
    }
  }
} elseif (-not $DepsOnly) {
  Say '  Not in a repository checkout: skipping the OpenXSys skill itself.'
}

# ---------- 2. pinned skills ----------

$cache = Join-Path $env:LOCALAPPDATA 'openxsys\pins'
$env:DISABLE_TELEMETRY = '1'
$env:DO_NOT_TRACK = '1'

foreach ($e in $lock.skills) {
  if (-not (Wanted $e.id $e.review.status)) { continue }
  foreach ($s in $e.skills) {
    $dest = Join-Path $Dir $s.name
    if (Test-Path $dest) { Say "  $($s.name) is already present in $Dir. Left as it is (it is yours)."; continue }
    if (-not $gitOk) { $skipped += "$($s.name): git is not installed"; continue }
    $c = Join-Path $cache $e.commit
    if (-not (Test-Path (Join-Path $c '.git'))) {
      New-Item -ItemType Directory -Force $c | Out-Null
      & git init -q $c
      & git -C $c fetch -q --depth 1 $e.url $e.commit 2>$null
      if ($LASTEXITCODE -ne 0) { Remove-Item -Recurse -Force -Confirm:$false $c; $skipped += "$($s.name): could not fetch $($e.url) at $($e.commit)"; continue }
    }
    $got = (& git -C $c rev-parse FETCH_HEAD 2>$null)
    if ("$got".Trim() -ne $e.commit) { $skipped += "$($s.name): fetched commit $got is not the pinned $($e.commit)"; continue }
    $gt = (& git -C $c rev-parse "$($e.commit):$($s.path)" 2>$null)
    if ("$gt".Trim() -ne $s.tree) { $skipped += "$($s.name): tree id $gt does not match the lock file ($($s.tree)). NOT installed"; continue }
    & git -C $c checkout -q $e.commit -- $s.path
    $how = ''
    if ($nodeOk -and (@('claude-code', 'codex') -contains $HostName) -and (-not $Project) -and (Have 'npx')) {
      try {
        & npx --yes "skills@$cliVersion" add $c --skill $s.name -g -a $HostName -y --copy *> $null
        if ($LASTEXITCODE -eq 0 -and (Test-Path (Join-Path $dest 'SKILL.md'))) { $how = "skills CLI $cliVersion" }
      } catch { }
    }
    if (-not $how) {
      if (-not (Test-Path $Dir)) { New-Item -ItemType Directory -Force $Dir | Out-Null }
      Copy-Item -Recurse (Join-Path $c ($s.path -replace '/', '\')) $dest
      $how = 'copied'
    }
    Say ("  Installed {0}  ({1}; verified tree {2})" -f $s.name, $how, $s.tree.Substring(0, 12))
    $installedSkills += [pscustomobject]@{ name = $s.name; id = $e.id; commit = $e.commit; tree = $s.tree; how = $how }
  }
}

# ---------- 3. offline copies of page libraries ----------

if ((-not $NoLibraries) -and (Test-Path $target)) {
  foreach ($l in $lock.libraries) {
    if (-not (Wanted $l.id $l.review.status)) { continue }
    foreach ($f in $l.files) {
      $label = "$($l.package)@$($l.version)/$($f.path)"
      $dest = Join-Path $target (Join-Path 'display\lib' (Join-Path "$($l.package)@$($l.version)" ($f.path -replace '/', '\')))
      if ((Test-Path $dest) -and ((Get-FileHash -Algorithm SHA256 $dest).Hash.ToLower() -eq $f.sha256)) { continue }
      $destDir = Split-Path -Parent $dest
      if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Force $destDir | Out-Null }
      $url = "https://cdn.jsdelivr.net/npm/$($l.package)@$($l.version)/$($f.path)"
      $part = "$dest.part"
      try {
        [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
        Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile $part
      } catch { if (Test-Path $part) { Remove-Item -Force $part }; $skipped += "${label}: download failed"; continue }
      $sum = (Get-FileHash -Algorithm SHA256 $part).Hash.ToLower()
      if ($sum -ne $f.sha256) { Remove-Item -Force $part; $skipped += "${label}: SHA-256 $sum does not match the lock file. NOT installed"; continue }
      Move-Item -Force $part $dest
      Say "  Library $label  (verified)"
      $installedLibs += [pscustomobject]@{ package = $l.package; version = $l.version; path = $f.path; sha256 = $f.sha256 }
    }
  }
}

# ---------- 4. the install record ----------

$depsTarget = Join-Path $target 'deps'
if ((Test-Path $depsTarget) -and (-not (IsLink $target))) {
  $rec = [ordered]@{
    openxsys        = $lock.openxsys
    installed       = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    host            = $HostName
    skillsDirectory = $Dir
    edition         = $Lang
    runtimes        = [ordered]@{ git = $gitOk; node = $nodeV; python = $pyV }
    skills          = @($installedSkills)
    libraries       = @($installedLibs)
  }
  [IO.File]::WriteAllText($record, (ConvertTo-Json -InputObject $rec -Depth 5), $utf8)
}

# ---------- 5. summary, and what is missing ----------

Say ''
Say 'Done.'
if (Test-Path $record) { Say "  Install record: $record" }
if ($skipped.Count -gt 0) { Say '  Not installed:'; foreach ($s in $skipped) { Say "    $s" } }
if (-not $nodeOk) {
  Say '  Without Node.js 22.20 or later you still get full interactive pages and static cards.'
  Say '  Node.js would add short video clips. Install it from https://nodejs.org/'
  if ((Have 'winget') -and (Ask "  Install Node.js now with 'winget install OpenJS.NodeJS.LTS'?")) {
    & winget install --id OpenJS.NodeJS.LTS -e
  }
}
if (-not $py) {
  Say "  Python 3.10 or later would add Manim concept animation and the document skills' scripts: https://www.python.org/downloads/"
}
Say ''
Say 'Next: open your agent and say   Open a system for ___.   or   Open the playground.'

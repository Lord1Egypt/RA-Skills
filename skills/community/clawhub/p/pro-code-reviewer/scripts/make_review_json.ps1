param(
  [Parameter(Mandatory = $true)][string]$Repo,
  [Parameter(Mandatory = $true)][string]$Range,
  [Parameter(Mandatory = $true)][string]$Out
)

$ErrorActionPreference = "Stop"

$repoPath = (Resolve-Path $Repo).Path
$outPath = [System.IO.Path]::GetFullPath($Out)

function RunGit([string[]]$Args) {
  $p = New-Object System.Diagnostics.Process
  $p.StartInfo = New-Object System.Diagnostics.ProcessStartInfo
  $p.StartInfo.FileName = "git"
  $p.StartInfo.WorkingDirectory = $repoPath
  $p.StartInfo.RedirectStandardOutput = $true
  $p.StartInfo.RedirectStandardError = $true
  $p.StartInfo.UseShellExecute = $false
  $p.StartInfo.CreateNoWindow = $true
  $p.StartInfo.Arguments = ($Args -join " ")
  $null = $p.Start()
  $stdout = $p.StandardOutput.ReadToEnd()
  $stderr = $p.StandardError.ReadToEnd()
  $p.WaitForExit()
  if ($p.ExitCode -ne 0) {
    throw ($stderr.Trim() | ForEach-Object { $_ })
  }
  return $stdout
}

function DetectPlatform() {
  $repo = Get-Item $repoPath
  $ios = @("*.xcodeproj", "*.xcworkspace", "Podfile", "Package.swift")
  foreach ($p in $ios) {
    if (Get-ChildItem -Path $repo.FullName -Filter $p -ErrorAction SilentlyContinue) { return "ios" }
  }
  $android = @("build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts", "AndroidManifest.xml", "gradlew", "gradlew.bat")
  foreach ($n in $android) {
    if (Get-ChildItem -Path $repo.FullName -Recurse -Filter $n -ErrorAction SilentlyContinue | Select-Object -First 1) { return "android" }
  }
  return "general"
}

function ParseNumstat([string]$Text) {
  $added = 0
  $removed = 0
  $files = @{}
  foreach ($line in ($Text -split "\r?\n")) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    $parts = $line -split "`t"
    if ($parts.Length -lt 3) { continue }
    $a = $parts[0]; $r = $parts[1]; $path = $parts[2]
    if ($a -match "^\d+$") { $added += [int]$a }
    if ($r -match "^\d+$") { $removed += [int]$r }
    $files[$path] = $true
  }
  return @{
    files_changed = $files.Count
    added = $added
    removed = $removed
  }
}

function CommitFilesChanged([string]$Sha) {
  $out = RunGit @("show", "--name-only", "--pretty=format:", $Sha)
  return (@($out -split "\r?\n" | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })).Count
}

function ListCommits([string]$Rng) {
  $out = RunGit @("log", "--pretty=format:%H%x09%an%x09%ad%x09%s", "--date=short", $Rng)
  $rows = @()
  foreach ($line in ($out -split "\r?\n")) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    $parts = $line -split "`t", 4
    if ($parts.Length -ne 4) { continue }
    $sha = $parts[0]; $author = $parts[1]; $date = $parts[2]; $subject = $parts[3]
    $rows += [ordered]@{
      sha = $sha
      subject = $subject
      author = $author
      date = $date
      files_changed = (CommitFilesChanged $sha)
      findings = @()
      passed = @()
    }
  }
  [Array]::Reverse($rows)
  return $rows
}

$platform = DetectPlatform
$rng = $Range.Trim()
$mode = if ($rng -like "*..*") { "range" } else { "single" }

$numstat = if ($mode -eq "single") {
  RunGit @("show", "--numstat", "--pretty=format:", $rng)
} else {
  RunGit @("diff", "--numstat", $rng)
}

$stats = ParseNumstat $numstat
$commits = ListCommits $rng
if ($commits.Count -eq 0) {
  $commits = @([ordered]@{ sha=$rng; subject=""; author=""; date=""; files_changed=(CommitFilesChanged $rng); findings=@(); passed=@() })
}

$data = [ordered]@{
  repo = $repoPath
  platform = $platform
  mode = $mode
  range = $rng
  generated_at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
  stats = [ordered]@{
    files_changed = $stats.files_changed
    added = $stats.added
    removed = $stats.removed
  }
  summary = "Auto-generated review JSON template. Fill findings per commit if you want HTML to show issues."
  commits = $commits
  overall = [ordered]@{
    patterns = @()
    blockers = @()
    next_steps = @()
    matrix = @()
    verdict = ""
  }
}

[System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($outPath)) | Out-Null
($data | ConvertTo-Json -Depth 30) | Out-File -FilePath $outPath -Encoding UTF8
Write-Output $outPath

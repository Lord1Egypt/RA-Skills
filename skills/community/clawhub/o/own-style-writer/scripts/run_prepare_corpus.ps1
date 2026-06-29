param(
    [Parameter(Mandatory = $true)]
    [string]$InputDir,
    [string]$OutputDir = "",
    [switch]$Recursive,
    [switch]$Overwrite,
    [string]$Extensions = "",
    [int]$MaxFiles = 0,
    [string]$RuntimeDir = ""
)

$ErrorActionPreference = "Stop"
$ScriptPath = Join-Path $PSScriptRoot "prepare_style_corpus.py"

function Test-PythonCommand {
    param([string[]]$Command)
    try {
        $exe = $Command[0]
        $rest = @()
        if ($Command.Length -gt 1) {
            $rest = $Command[1..($Command.Length - 1)]
        }
        & $exe @rest --version *> $null
        return $LASTEXITCODE -eq 0
    } catch {
        return $false
    }
}

function ConvertTo-WslPath {
    param([string]$Path)

    $resolved = [System.IO.Path]::GetFullPath($Path)
    if ($resolved -match '^([A-Za-z]):\\(.*)$') {
        $drive = $matches[1].ToLowerInvariant()
        $rest = $matches[2] -replace '\\', '/'
        return "/mnt/$drive/$rest"
    }

    return $resolved -replace '\\', '/'
}

$argsList = @("--input-dir", $InputDir)
if ($OutputDir) { $argsList += @("--output-dir", $OutputDir) }
if ($Recursive) { $argsList += "--recursive" }
if ($Overwrite) { $argsList += "--overwrite" }
if ($Extensions) { $argsList += @("--extensions", $Extensions) }
if ($MaxFiles -gt 0) { $argsList += @("--max-files", [string]$MaxFiles) }
if ($RuntimeDir) { $argsList += @("--runtime-dir", $RuntimeDir) }

if (Test-PythonCommand @("python3")) {
    & python3 $ScriptPath @argsList
    exit $LASTEXITCODE
}

if (Test-PythonCommand @("python")) {
    & python $ScriptPath @argsList
    exit $LASTEXITCODE
}

if (Test-PythonCommand @("py", "-3")) {
    & py -3 $ScriptPath @argsList
    exit $LASTEXITCODE
}

$wsl = Get-Command wsl -ErrorAction SilentlyContinue
if ($wsl) {
    $wslScript = ConvertTo-WslPath $ScriptPath
    $wslArgs = @("-e", "python3", $wslScript) + $argsList
    & wsl @wslArgs
    exit $LASTEXITCODE
}

throw "No Python runtime found. Install Python 3.10+ or enable WSL with python3."

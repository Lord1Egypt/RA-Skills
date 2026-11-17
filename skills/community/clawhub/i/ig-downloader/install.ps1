<#
.SYNOPSIS
    Universal installer for Instagram Downloader Skill
.DESCRIPTION
    Installs the Instagram Downloader Python package + agent skill files
    for OpenCode, Claude Code, Codex CLI, Cursor, and other AI agents on Windows.

.PARAMETER Agent
    Target agent: auto (detect), all, opencode, claude, codex, cursor

.PARAMETER Scope
    Install scope: global (default, user-wide), project (current directory)

.PARAMETER Dir
    Custom install directory (overrides Scope)

.PARAMETER Help
    Show this help message

.EXAMPLE
    .\install.ps1
    .\install.ps1 -Agent all
    .\install.ps1 -Agent codex -Scope project
#>

param(
    [string]$Agent = "auto",
    [ValidateSet("global","project")]
    [string]$Scope = "global",
    [string]$Dir = "",
    [switch]$Help
)

$SkillName     = "instagram-downloader"
$SkillVersion  = "2.2.0"
$Repo          = "cripterhack/ig-downloader-skill"
$RepoUrl       = "https://github.com/${Repo}.git"

# ─── Help ───────────────────────────────────────────────────────
if ($Help) {
    @"
Usage: .\install.ps1 [OPTIONS]

Install the Instagram Downloader skill + Python package for AI coding agents.

Options:
  -Agent <agent>    Target agent (auto | opencode | claude | codex | cursor | all)
  -Scope <scope>    Install scope: global (default) or project
  -Dir <path>       Custom install directory (overrides -Scope)
  -Help             Show this help message

Examples:
  .\install.ps1              # Auto-detect agent, global install
  .\install.ps1 -Agent all   # Install for ALL supported agents
"@
    exit 0
}

# ─── Colors (ANSI via Write-Host) ──────────────────────────────
$Host.UI.RawUI.ForegroundColor = $null  # reset
function Write-Log   { Write-Host " ✔ $($args[0])" -ForegroundColor Green }
function Write-Warn  { Write-Host " ⚠ $($args[0])" -ForegroundColor Yellow }
function Write-Error { Write-Host " ✘ $($args[0])" -ForegroundColor Red; exit 1 }
function Write-Info  { Write-Host " ℹ $($args[0])" -ForegroundColor Blue }
function Write-Header{ Write-Host "`n══ $($args[0]) ══" -ForegroundColor Cyan }
function Write-Line  { Write-Host ("─" * 40) -ForegroundColor Cyan }

# ─── Welcome ────────────────────────────────────────────────────
Write-Host "`n  Instagram Downloader Skill v${SkillVersion}" -ForegroundColor Cyan
Write-Host "  Universal Installer (Windows)" -ForegroundColor Blue
Write-Line

# ─── Step 0: Locate repo root ──────────────────────────────────
$RepoRoot = $null
$ScriptPath = $MyInvocation.MyCommand.Path
$ScriptDir = Split-Path -Parent $ScriptPath -ErrorAction SilentlyContinue

if ($ScriptDir -and (Test-Path "$ScriptDir\SKILL.md") -and (Test-Path "$ScriptDir\instagram_downloader.py")) {
    $RepoRoot = $ScriptDir
    Write-Info "Running from local repo: $RepoRoot"
} else {
    Write-Info "Running standalone — cloning repo..."
    $TmpDir = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), [System.Guid]::NewGuid().ToString())
    $null = New-Item -ItemType Directory -Path $TmpDir -Force
    try {
        git clone --depth 1 $RepoUrl "$TmpDir\repo" 2>&1 | Out-Null
        if (-not $?) { throw "git clone failed" }
        $RepoRoot = "$TmpDir\repo"
        Write-Log "Repo cloned to $RepoRoot"
    } catch {
        Write-Error "Failed to clone repo: $_"
    }
}

# ─── Step 1: Install Python package ────────────────────────────
function Install-PythonPackage {
    Write-Header "Step 1: Installing Python Package"

    # Detect Python/pip
    $python = $null
    foreach ($cmd in @("python3", "python", "py")) {
        $ver = & $cmd --version 2>$null
        if ($LASTEXITCODE -eq 0 -and $ver -match "Python") {
            $python = $cmd
            break
        }
    }

    if (-not $python) {
        Write-Warn "Python not found. Install Python 3.10+ from https://python.org"
        Write-Warn "Then run: pip install instagrapi requests"
        Write-Warn "         pip install git+$RepoUrl"
        return
    }

    Write-Info "Using: $python"

    # pip detection
    $pip = $null
    if ($python -eq "py") {
        $pip = "py -m pip"
    } else {
        $pip = "$python -m pip"
    }

    # Dependencies
    Write-Info "Installing Python dependencies..."
    $deps = @("instagrapi", "requests", "playwright")
    foreach ($dep in $deps) {
        $result = Invoke-Expression "& $pip install $dep 2>&1" 2>$null
        if ($LASTEXITCODE -ne 0) {
            Write-Warn "Could not install $dep. Try: $pip install $dep"
        }
    }

    # Install the package
    if (Test-Path "$RepoRoot\pyproject.toml") {
        Write-Info "Installing package from local..."
        $result = Invoke-Expression "& $pip install -e '$RepoRoot' 2>&1" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Log "Package installed from local source"
        } else {
            Write-Warn "Local install failed, trying from GitHub..."
            $result = Invoke-Expression "& $pip install 'git+$RepoUrl' 2>&1" 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Log "Package installed from GitHub"
            } else {
                Write-Warn "Package install failed. Try: $pip install git+$RepoUrl"
            }
        }
    } else {
        $result = Invoke-Expression "& $pip install 'git+$RepoUrl' 2>&1" 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Log "Package installed from GitHub"
        } else {
            Write-Warn "Package install failed. Try: $pip install git+$RepoUrl"
        }
    }

    # Verify
    $igVer = & ig-downloader --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Log "CLI available: ig-downloader ($igVer)"
    } else {
        Write-Warn "CLI 'ig-downloader' not in PATH after install."
        Write-Warn "Try: $python -m instagram_downloader --help"
    }
}

# ─── Step 2: Install agent skill files ─────────────────────────
function Install-AgentSkill {
    param([string]$AgentName, [string]$Scope, [string]$CustomDir)

    $baseDir = ""
    if ($CustomDir) {
        $baseDir = $CustomDir
    } elseif ($Scope -eq "project") {
        $baseDir = "$(Get-Location).$AgentName"
    } else {
        $homeDir = $env:USERPROFILE
        switch ($AgentName) {
            "opencode" { $baseDir = "$homeDir\.config\opencode" }
            "claude"   { $baseDir = "$homeDir\.claude" }
            "codex"    { $baseDir = "$homeDir\.codex" }
            "cursor"   { $baseDir = "$homeDir\.cursor" }
            "agents"   { $baseDir = "$homeDir\.agents" }
            default    { Write-Warn "Unknown agent: $AgentName"; return $false }
        }
    }

    $skillDir = "$baseDir\skills\$SkillName"
    $null = New-Item -ItemType Directory -Path $skillDir -Force -ErrorAction SilentlyContinue
    if (-not (Test-Path $skillDir)) {
        Write-Warn "Cannot create directory: $skillDir"
        return $false
    }

    $copied = 0
    foreach ($file in @("SKILL.md", "AGENTS.md", "README.md")) {
        $src = "$RepoRoot\$file"
        if (Test-Path $src) {
            Copy-Item -Path $src -Destination "$skillDir\$file" -Force -ErrorAction SilentlyContinue
            if (Test-Path "$skillDir\$file") { $copied++ }
        }
    }

    if ($copied -gt 0) {
        Write-Log "Installed $copied file(s) → $skillDir"
        return $true
    } else {
        Write-Warn "No skill files found at $RepoRoot"
        return $false
    }
}

function Detect-Agents {
    $detected = @()
    if (Get-Command opencode -ErrorAction SilentlyContinue) { $detected += "opencode" }
    if (Get-Command claude   -ErrorAction SilentlyContinue) { $detected += "claude" }
    if (Get-Command codex    -ErrorAction SilentlyContinue) { $detected += "codex" }
    if (Get-Command cursor   -ErrorAction SilentlyContinue) { $detected += "cursor" }
    $detected += "agents"  # forward-compat
    return $detected
}

function Install-AgentSkills {
    Write-Header "Step 2: Installing Agent Skills"

    $agents = @()
    switch ($Agent) {
        "auto" {
            $agents = Detect-Agents
            if ($agents.Count -eq 0 -or ($agents.Count -eq 1 -and $agents[0] -eq "agents")) {
                Write-Warn "No AI agent detected. Installing for all supported agents."
                $agents = @("opencode", "claude", "codex", "cursor", "agents")
            } else {
                Write-Info "Detected agents: $($agents -join ', ')"
            }
        }
        "all" { $agents = @("opencode", "claude", "codex", "cursor", "agents") }
        "opencode" { $agents = @("opencode", "agents") }
        "claude"   { $agents = @("claude", "agents") }
        "codex"    { $agents = @("codex", "agents") }
        "cursor"   { $agents = @("cursor", "agents") }
        default { Write-Error "Unknown agent: $Agent. Supported: auto, all, opencode, claude, codex, cursor" }
    }

    $success = 0
    foreach ($a in $agents) {
        if (Install-AgentSkill -AgentName $a -Scope $Scope -CustomDir $Dir) { $success++ }
    }

    Write-Host
    Write-Log "Skills installed for $success/$($agents.Count) agent(s)"
}

# ─── Step 3: Verify ─────────────────────────────────────────────
function Verify-Installation {
    Write-Header "Step 3: Verification"

    $ok = 0
    $total = 0

    # Check SKILL.md files
    $skillPaths = @()
    if ($Dir) {
        $skillPaths += "$Dir\skills\$SkillName\SKILL.md"
    } elseif ($Scope -eq "project") {
        $skillPaths += "$(Get-Location)\.opencode\skills\$SkillName\SKILL.md"
        $skillPaths += "$(Get-Location)\.claude\skills\$SkillName\SKILL.md"
    } else {
        $homeDir = $env:USERPROFILE
        $skillPaths += "$homeDir\.config\opencode\skills\$SkillName\SKILL.md"
        $skillPaths += "$homeDir\.claude\skills\$SkillName\SKILL.md"
        $skillPaths += "$homeDir\.codex\skills\$SkillName\SKILL.md"
        $skillPaths += "$homeDir\.cursor\skills\$SkillName\SKILL.md"
        $skillPaths += "$homeDir\.agents\skills\$SkillName\SKILL.md"
    }

    $total++
    $found = 0
    foreach ($p in $skillPaths) {
        if (Test-Path $p) {
            Write-Log "SKILL.md found: $p"
            $found++
        }
    }
    if ($found -gt 0) { $ok++ }

    # Check CLI
    $total++
    if (Get-Command ig-downloader -ErrorAction SilentlyContinue) {
        Write-Log "CLI 'ig-downloader' available"
        $ok++
    } else {
        Write-Warn "CLI 'ig-downloader' not in PATH."
        Write-Warn "Try: python -m instagram_downloader --help"
    }

    Write-Host
    if ($ok -gt 0) {
        Write-Log "$ok/$total checks passed"
    } else {
        Write-Warn "No checks passed — something went wrong"
    }
}

# ─── Post-install instructions ──────────────────────────────────
function Show-Instructions {
    Write-Header "Installation Complete 🎉"

    @"

Instagram Downloader Skill v${SkillVersion} is ready.

Quick start:
  1. Set up Instagram access:
     ig-downloader --setup

  2. Download a profile:
     ig-downloader -u username -o ./downloads

Learn more:
  ig-downloader --help
  https://github.com/${Repo}

Skill auto-discovery:
  The SKILL.md has been placed in your agent's skills directory.
  Your AI agent will discover it automatically in new sessions.

  To use the skill, ask your agent:
  "Download instagram posts from username"
"@
    Write-Line
}

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
function Main {
    Install-PythonPackage
    Install-AgentSkills
    Verify-Installation
    Show-Instructions
}

Main

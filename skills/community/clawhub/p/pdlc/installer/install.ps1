#Requires -Version 5.1
# =============================================================================
# PARALLEL IMPLEMENTATION: install.ps1 (PowerShell) and install.sh (bash) are
# feature-equivalent siblings. ANY behavioral change here MUST be mirrored in
# install.sh, and vice versa. The bash sibling must stay bash-3.2 safe (macOS
# ships /bin/bash 3.2.57). Enforced by INV-L3-029. [ClaudeCode-Alignment]
# =============================================================================
<#
.SYNOPSIS
    AI-* Family Package Installer - Interactive installer for AI-* workflow packages.

.DESCRIPTION
    Installs AI-* packages into a target workspace using the locked family-workspace
    structure:
      - Package files  -> .aiflc/{family}/   (cores + rule-details, uniform on every platform; OI-158)
      - Orchestrator   -> platform-native auto-load slot (e.g. .kiro/steering/) - sole always-loaded file
      - Family outputs -> {family}-ws/        (ideas/ projects/ portfolio/ data/)
    The family is auto-derived from this installer's parent folder name (e.g. "pdlc").

.PARAMETER TargetWorkspace
    Path to the workspace where the family will be installed.

.PARAMETER Platform
    Target platform: kiro, cursor, claude-code, cline, amazonq, copilot.

.PARAMETER Packages
    Comma-separated list of package names (e.g., "ai-pilc,ai-adlc").

.PARAMETER Bundle
    Preset bundle: full, minimal, arch, governance, portfolio.

.PARAMETER DryRun
    Show what would be installed without copying files.

.PARAMETER Force
    Overwrite existing files without prompting.

.PARAMETER Uninstall
    Remove previously installed packages (reads manifest from {family}-ws/).

.EXAMPLE
    .\install.ps1 -TargetWorkspace "C:\Projects\my-app" -Platform kiro -Bundle full
#>

[CmdletBinding()]
param(
    [string]$TargetWorkspace,
    [ValidateSet("kiro", "cursor", "claude-code", "cline", "amazonq", "copilot")]
    [string]$Platform,
    [string]$Packages,
    [ValidateSet("full", "minimal", "arch", "governance", "portfolio")]
    [string]$Bundle,
    [switch]$DryRun,
    [switch]$Force,
    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PackagesRoot = Split-Path -Parent $ScriptDir

# Family is the parent folder name of the installer (e.g. "pdlc")
$Family = (Split-Path -Leaf $PackagesRoot)
$FamilyWs = "$Family-ws"

# Package catalogue
$PackageCatalogue = @(
    @{ Name = "ai-ilc";  Layer = "Portfolio"; Type = "Interactive workflow"; Description = "Evaluate raw ideas - Approved Idea Brief"; CoreFile = "core-workflow.md"; RulesDir = "ai-ilc-rules"; DetailsDir = "ai-ilc-rule-details" }
    @{ Name = "ai-pilc"; Layer = "Portfolio"; Type = "Interactive workflow"; Description = "Raw requirement - Project Initiation Package (PIP)"; CoreFile = "core-workflow.md"; RulesDir = "ai-pilc-rules"; DetailsDir = "ai-pilc-rule-details" }
    @{ Name = "ai-ppm";  Layer = "Portfolio"; Type = "Adaptive engine"; Description = "Multiple PIPs - Portfolio governance and prioritization"; CoreFile = "core-engine.md"; RulesDir = "ai-ppm-rules"; DetailsDir = "ai-ppm-rule-details" }
    @{ Name = "ai-flo";  Layer = "Edge"; Type = "Router engine"; Description = "Package-to-package flow orchestration"; CoreFile = "core-engine.md"; RulesDir = "ai-flo-rules"; DetailsDir = "ai-flo-rule-details" }
    @{ Name = "ai-adlc"; Layer = "Project"; Type = "Interactive workflow"; Description = "Requirements - Architecture Package (AP)"; CoreFile = "core-workflow.md"; RulesDir = "ai-adlc-rules"; DetailsDir = "ai-adlc-rule-details" }
    @{ Name = "ai-uxd";  Layer = "Project"; Type = "Interactive workflow"; Description = "PIP/AP - UX Design Package (personas, flows, design system)"; CoreFile = "core-workflow.md"; RulesDir = "ai-uxd-rules"; DetailsDir = "ai-uxd-rule-details" }
    @{ Name = "ai-polc"; Layer = "Project"; Type = "Interactive workflow"; Description = "PIP/AP - Product Backlog Package (PBP)"; CoreFile = "core-workflow.md"; RulesDir = "ai-polc-rules"; DetailsDir = "ai-polc-rule-details" }
    @{ Name = "ai-dwg";  Layer = "Project"; Type = "One-time generator"; Description = "AP + PBP + UXP - Ready-to-code workspace"; CoreFile = "core-generator.md"; RulesDir = "ai-dwg-rules"; DetailsDir = "ai-dwg-rule-details" }
    @{ Name = "ai-gce";  Layer = "Project"; Type = "Adaptive engine"; Description = "Workspace - Compliance enforcement layer"; CoreFile = "core-generator.md"; RulesDir = "ai-gce-rules"; DetailsDir = "ai-gce-rule-details" }
    @{ Name = "ai-tge";  Layer = "Project"; Type = "Test governance engine"; Description = "Workspace - Test strategy, register, coverage"; CoreFile = "core-engine.md"; RulesDir = "ai-tge-rules"; DetailsDir = "ai-tge-rule-details" }
    @{ Name = "ai-dfe";  Layer = "Edge"; Type = "Data fabric engine"; Description = "Gather, shape, and distribute structured data"; CoreFile = "core-engine.md"; RulesDir = "ai-dfe-rules"; DetailsDir = "ai-dfe-rule-details" }
)

# Preset bundles
$Bundles = @{
    "full"       = @("ai-ilc", "ai-pilc", "ai-ppm", "ai-flo", "ai-adlc", "ai-uxd", "ai-polc", "ai-dwg", "ai-gce", "ai-tge", "ai-dfe")
    "minimal"    = @("ai-pilc", "ai-adlc", "ai-dwg")
    "arch"       = @("ai-adlc", "ai-dwg", "ai-gce")
    "governance" = @("ai-gce", "ai-tge")
    "portfolio"  = @("ai-ilc", "ai-pilc", "ai-ppm", "ai-flo")
}

$ManifestFileName = ".ai-family-manifest.json"

# -----------------------------------------------------------------------------
# UI Helpers
# -----------------------------------------------------------------------------

function Write-Banner {
    Write-Host ""
    Write-Host "  ================================================================" -ForegroundColor Cyan
    Write-Host "       AI-* Family - Package Installer                             " -ForegroundColor Cyan
    Write-Host "       Family: $Family                                             " -ForegroundColor Cyan
    Write-Host "  ================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step { param([string]$Message) Write-Host "  > $Message" -ForegroundColor Green }
function Write-Info { param([string]$Message) Write-Host "  i $Message" -ForegroundColor DarkGray }
function Write-Warn { param([string]$Message) Write-Host "  ! $Message" -ForegroundColor Yellow }

function Show-PackageCatalogue {
    Write-Host ""
    Write-Host "  Available Packages:" -ForegroundColor White
    Write-Host "  -------------------" -ForegroundColor DarkGray
    Write-Host ""
    $layers = @("Portfolio", "Edge", "Project")
    foreach ($layer in $layers) {
        Write-Host "  [$layer Layer]" -ForegroundColor Magenta
        $pkgs = $PackageCatalogue | Where-Object { $_.Layer -eq $layer }
        foreach ($pkg in $pkgs) {
            $globalIdx = [array]::IndexOf($PackageCatalogue, $pkg) + 1
            $line = "    {0,2}. {1,-10} - {2}" -f $globalIdx, $pkg.Name, $pkg.Description
            Write-Host $line -ForegroundColor White
        }
        Write-Host ""
    }
}

function Show-Bundles {
    Write-Host ""
    Write-Host "  Preset Bundles:" -ForegroundColor White
    Write-Host "  ----------------" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "    [F] Full         - All 11 packages (complete family)" -ForegroundColor White
    Write-Host "    [M] Minimal      - AI-PILC + AI-ADLC + AI-DWG (quick start)" -ForegroundColor White
    Write-Host "    [A] Architecture - AI-ADLC + AI-DWG + AI-GCE" -ForegroundColor White
    Write-Host "    [G] Governance   - AI-GCE + AI-TGE" -ForegroundColor White
    Write-Host "    [P] Portfolio    - AI-ILC + AI-PILC + AI-PPM + AI-FLO" -ForegroundColor White
    Write-Host "    [C] Custom       - Pick individual packages" -ForegroundColor White
    Write-Host ""
}

function Show-Platforms {
    Write-Host ""
    Write-Host "  Supported Platforms:" -ForegroundColor White
    Write-Host "  ---------------------" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "    [1] Kiro            (VS Code-based, full feature support)" -ForegroundColor White
    Write-Host "    [2] Amazon Q        (full workflow support)" -ForegroundColor White
    Write-Host "    [3] Cursor          (full workflow support)" -ForegroundColor White
    Write-Host "    [4] Cline           (full workflow support)" -ForegroundColor White
    Write-Host "    [5] Claude Code     (full workflow support)" -ForegroundColor White
    Write-Host "    [6] GitHub Copilot  (partial - workspace-level only)" -ForegroundColor White
    Write-Host ""
}

function Get-PlatformFromChoice {
    param([string]$Choice)
    switch ($Choice) {
        "1" { return "kiro" }
        "2" { return "amazonq" }
        "3" { return "cursor" }
        "4" { return "cline" }
        "5" { return "claude-code" }
        "6" { return "copilot" }
        default { return $null }
    }
}

# -----------------------------------------------------------------------------
# Path Mapping (per Design S5.2 - verified path table; family-scoped)
# -----------------------------------------------------------------------------

function Get-PlatformPaths {
    param([string]$PlatformName, [hashtable]$Pkg)

    $rules = $Pkg.RulesDir
    $details = $Pkg.DetailsDir
    $core = $Pkg.CoreFile
    $name = $Pkg.Name

    # OI-158 (unified core placement): cores AND rule-details land in ONE uniform
    # brand-scoped home on EVERY platform -> .aiflc/{family}/. Only the orchestrator
    # sits in each platform's native auto-load slot (see Get-OrchestratorDest); it
    # Reads the relevant core on demand. This collapses the former 6-way
    # CoreDest/DetailsDest matrix and fixes the rule-details resolution mismatch
    # (cores now resolve details from the same .aiflc/{family}/ path). [INV-L3-031]
    return @{
        CoreSource    = Join-Path $PackagesRoot "$name\$rules\$core"
        DetailsSource = Join-Path $PackagesRoot "$name\$details"
        CoreDest      = ".aiflc\$Family\$rules\$core"
        DetailsDest   = ".aiflc\$Family\$details"
    }
}

# -----------------------------------------------------------------------------
# Family Workspace Validation & Skeleton
# -----------------------------------------------------------------------------

function Test-FamilyWsPlacement {
    param([string]$Target)
    # {family}-ws/ MUST live at the workspace root only (Invariant 1).
    # Reject if the target itself sits inside another *-ws folder.
    $parent = Split-Path -Parent $Target
    if ($parent -and (Split-Path -Leaf $parent) -match '-ws$') {
        Write-Warn "Target appears nested inside a '*-ws' folder ($parent)."
        Write-Host "  Family workspaces must be at the workspace root, not nested. Aborted." -ForegroundColor Red
        return $false
    }
    return $true
}

function New-FamilyWorkspaceSkeleton {
    param([string]$Target, [bool]$IsDryRun)

    $wsRoot = Join-Path $Target $FamilyWs
    $dataRoot = Join-Path $wsRoot "data"

    $folders = @(
        (Join-Path $wsRoot "ideas"),
        (Join-Path $wsRoot "projects"),
        (Join-Path $wsRoot "portfolio"),
        $dataRoot,
        (Join-Path $dataRoot "demands"),
        (Join-Path $dataRoot "history"),
        (Join-Path $Target "core")
    )

    if (Test-Path $wsRoot) {
        Write-Info "Family workspace '$FamilyWs' already exists - update mode (skeleton preserved)."
        return
    }

    if ($IsDryRun) {
        Write-Host "    [DRY RUN] Would create family workspace skeleton:" -ForegroundColor Yellow
        foreach ($f in $folders) { Write-Host "      $f" -ForegroundColor DarkGray }
        Write-Host "      + projects\PROJECTS.md, data\REGISTRY.json, data\CONSUMER_REGISTRY.md, data\dfe-state.md" -ForegroundColor DarkGray
        return
    }

    foreach ($f in $folders) {
        if (-not (Test-Path $f)) { New-Item -ItemType Directory -Force -Path $f | Out-Null }
    }

    # Bootstrap: PROJECTS.md (empty registry template)
    $projectsMd = @"
<!-- Generated by AI-* Family installer | family: $Family -->
# Projects Registry

Active project: _none yet_

| Project ID | Folder | Active | Notes |
|------------|--------|:------:|-------|
| _(empty - the first package run will register a project here)_ | | | |
"@
    Set-Content -Path (Join-Path $wsRoot "projects\PROJECTS.md") -Value $projectsMd -Encoding utf8

    # Bootstrap: DFE territory
    $registryJson = @"
{
  "`$generatedBy": "AI-DFE",
  "`$family": "$Family",
  "files": {},
  "cross-family": {}
}
"@
    Set-Content -Path (Join-Path $dataRoot "REGISTRY.json") -Value $registryJson -Encoding utf8

    $consumerRegistry = @"
<!-- AI-DFE consumer registry | family: $Family | bootstrapped empty by installer -->
# Consumer Registry - $Family

> Demander index. Consumers register here at install (Obligation 1). Demander discovery (Stage 1.3) reads this. Bootstrapped empty - no rows.

| consumer | home | demandFile | outputFile | registeredOn |
|----------|------|------------|------------|--------------|
"@
    Set-Content -Path (Join-Path $dataRoot "CONSUMER_REGISTRY.md") -Value $consumerRegistry -Encoding utf8

    $dfeState = @"
<!-- Generated by AI-* Family installer | DFE state | family: $Family -->
# Data Fabric State - AI-DFE

data-fabric:
  family: $Family
  discovered: {}
  demands: {}
"@
    Set-Content -Path (Join-Path $dataRoot "dfe-state.md") -Value $dfeState -Encoding utf8

    Write-Step "Created family workspace skeleton: $FamilyWs\ (ideas, projects, portfolio, data) + core\"
}

# -----------------------------------------------------------------------------
# Install a single package
# -----------------------------------------------------------------------------

function Install-Package {
    param([hashtable]$Package, [string]$PlatformName, [string]$Target, [bool]$IsDryRun, [bool]$IsForce)

    $paths = Get-PlatformPaths -PlatformName $PlatformName -Pkg $Package
    $coreDest = Join-Path $Target $paths.CoreDest
    $detailsDest = Join-Path $Target $paths.DetailsDest

    if (-not (Test-Path $paths.CoreSource)) {
        Write-Warn "Source not found: $($paths.CoreSource) - skipping $($Package.Name)"
        return $null
    }

    if ((Test-Path $coreDest) -and -not $IsForce -and -not $IsDryRun) {
        $response = Read-Host "    $($Package.Name) already exists at target. Overwrite? [y/N]"
        if ($response -ne "y" -and $response -ne "Y") {
            Write-Info "Skipped $($Package.Name)"
            return $null
        }
    }

    if ($IsDryRun) {
        Write-Host "    [DRY RUN] Would install $($Package.Name):" -ForegroundColor Yellow
        Write-Host "      Core:    $($paths.CoreSource)" -ForegroundColor DarkGray
        Write-Host "           >   $coreDest" -ForegroundColor DarkGray
        Write-Host "      Details: $($paths.DetailsSource)" -ForegroundColor DarkGray
        Write-Host "           >   $detailsDest" -ForegroundColor DarkGray
        return @{ Name = $Package.Name; CoreDest = $paths.CoreDest; DetailsDest = $paths.DetailsDest }
    }

    $coreDir = Split-Path -Parent $coreDest
    if (-not (Test-Path $coreDir)) { New-Item -ItemType Directory -Force -Path $coreDir | Out-Null }

    # OI-158: cores are neutral files in .aiflc/{family}/, Read on demand by the
    # orchestrator - no platform-specific auto-load frontmatter is injected
    # (the former Cursor .mdc alwaysApply wrapper is gone; cores no longer land
    # in .cursor/rules/).
    Copy-Item $paths.CoreSource -Destination $coreDest -Force

    if (Test-Path $paths.DetailsSource) {
        if (Test-Path $detailsDest) { Remove-Item -Recurse -Force $detailsDest }
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $detailsDest) | Out-Null
        Copy-Item -Recurse $paths.DetailsSource -Destination $detailsDest
    }

    Write-Step "Installed $($Package.Name)"
    return @{ Name = $Package.Name; CoreDest = $paths.CoreDest; DetailsDest = $paths.DetailsDest }
}

# -----------------------------------------------------------------------------
# Install family tools (visual tools / extensions under tools/)
# -----------------------------------------------------------------------------

# Dev-only artifacts that must never be copied into a user workspace.
$ToolsExcludeDirs = @("node_modules", "dist", "demo")

# Fabric trio - family-root routing artifacts read at runtime by AI-FLO and AI-DFE.
# These live in the FAMILY workspace (planning/orchestration), NOT the DWG-generated
# dev workspace. Without them FLO returns NOT READY ("no bindings = no routing"). [OI-123]
$FabricFiles = @("FAMILY_BINDINGS.md", "GATE_PROTOCOL.md", "FAMILY_INTERFACE.md", "TRIGGER_KEYS_REFERENCE.md")

# Files inside a package's templates/agents/ that are NOT runnable agents (skip on agent install).
$AgentExcludePatterns = @("shortcut-rules-block", "-guide", "-section")

function Install-Tools {
    param([string]$Target, [bool]$IsDryRun, [bool]$IsForce)

    $toolsSource = Join-Path $PackagesRoot "tools"
    if (-not (Test-Path $toolsSource)) {
        Write-Info "No tools/ directory in this family - nothing to install."
        return @()
    }

    $extRoot = Join-Path $toolsSource "extensions"
    $extDirs = @()
    if (Test-Path $extRoot) {
        $extDirs = @(Get-ChildItem -Path $extRoot -Directory -ErrorAction SilentlyContinue | ForEach-Object { $_.Name })
    }

    if ($IsDryRun) {
        Write-Host "    [DRY RUN] Would install family tools to $FamilyWs\tools\:" -ForegroundColor Yellow
        foreach ($e in $extDirs) { Write-Host "      $FamilyWs\tools\extensions\$e\ (excludes: $($ToolsExcludeDirs -join ', '))" -ForegroundColor DarkGray }
        if (-not $extDirs) { Write-Host "      (no extensions found)" -ForegroundColor DarkGray }
        return $extDirs | ForEach-Object { "$FamilyWs\tools\extensions\$_" }
    }

    $srcFull = (Resolve-Path $toolsSource).Path
    $files = Get-ChildItem -Path $toolsSource -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
        $rel = $_.FullName.Substring($srcFull.Length).TrimStart('\', '/')
        $parts = $rel -split '[\\/]'
        -not ($parts | Where-Object { $ToolsExcludeDirs -contains $_ })
    }

    $toolsRootDest = Join-Path (Join-Path $Target $FamilyWs) "tools"
    $copied = 0
    foreach ($f in $files) {
        $rel = $f.FullName.Substring($srcFull.Length).TrimStart('\', '/')
        $destPath = Join-Path $toolsRootDest $rel
        $td = Split-Path -Parent $destPath
        if (-not (Test-Path $td)) { New-Item -ItemType Directory -Force -Path $td | Out-Null }
        Copy-Item $f.FullName -Destination $destPath -Force
        $copied++
    }

    if ($extDirs) {
        Write-Step "Installed family tools: $($extDirs -join ', ') ($copied files -> $FamilyWs\tools\)"
    } else {
        Write-Step "Installed family tools ($copied files -> $FamilyWs\tools\)"
    }
    return $extDirs | ForEach-Object { "$FamilyWs\tools\extensions\$_" }
}

# -----------------------------------------------------------------------------
# Deploy the fabric trio (FLO/DFE routing graph) to the family rule-details root
# -----------------------------------------------------------------------------

function Get-FamilyRootDest {
    # The family home root - parent of every package rules/ + rule-details/ dir.
    # OI-158: uniform .aiflc/{family}/ on every platform. Fabric files land here
    # (beside cores + details) so FLO/DFE resolve them from the same home.
    param([string]$PlatformName)
    return ".aiflc\$Family"
}

function Install-Fabric {
    param([string]$PlatformName, [string]$Target, [bool]$IsDryRun)

    $familyRootRel  = Get-FamilyRootDest -PlatformName $PlatformName
    $familyRootDest = Join-Path $Target $familyRootRel
    $deployed = @()
    $missing  = @()

    foreach ($f in $FabricFiles) {
        $src = Join-Path $PackagesRoot $f
        if (-not (Test-Path $src)) { $missing += $f; continue }

        if ($IsDryRun) {
            Write-Host "    [DRY RUN] Would deploy fabric: $f -> $familyRootRel\$f" -ForegroundColor Yellow
            $deployed += "$familyRootRel\$f"
            continue
        }

        if (-not (Test-Path $familyRootDest)) { New-Item -ItemType Directory -Force -Path $familyRootDest | Out-Null }
        Copy-Item $src -Destination (Join-Path $familyRootDest $f) -Force
        $deployed += "$familyRootRel\$f"
    }

    if ($missing) {
        Write-Warn "Fabric file(s) missing from family source: $($missing -join ', '). FLO/DFE routing may be unavailable."
    }
    if (-not $IsDryRun -and $deployed.Count -gt 0) {
        Write-Step "Deployed fabric trio ($($deployed.Count)) -> $familyRootRel\  (FLO/DFE routing graph)"
    }
    return $deployed
}

# -----------------------------------------------------------------------------
# Deploy the session orchestrator - the family SINGLE always-loaded steering
# file. All package cores ship `inclusion: manual`; this orchestrator
# (`inclusion: auto`) is the sole entry point and routes to one package on
# demand. Keeps the context window free (correction-package Issue 11 / OI-127 /
# INV-L3-027). Static source - its "State Awareness" stays a placeholder.
# -----------------------------------------------------------------------------

function Get-OrchestratorDest {
    # Where the always-loaded orchestrator lands per platform (mirrors CoreDest patterns).
    param([string]$PlatformName)
    switch ($PlatformName) {
        # Kiro auto-includes (inclusion: auto) only files directly in .kiro/steering/ -
        # a nested family subfolder would NOT auto-load, defeating the orchestrator (OI-127).
        "kiro"        { return ".kiro\steering\session-orchestrator.md" }
        "amazonq"     { return ".amazonq\rules\$Family\session-orchestrator.md" }
        "cursor"      { return ".cursor\rules\$Family-session-orchestrator.mdc" }
        "cline"       { return ".clinerules\$Family-session-orchestrator.md" }
        "claude-code" { $uf = $Family.ToUpper().Replace('-','_'); return "CLAUDE_${uf}_ORCHESTRATOR.md" }
        "copilot"     { return ".github\copilot-instructions-$Family-orchestrator.md" }
    }
}

function Get-OrchestratorSource {
    # Claude Code cannot use Kiro `#hashtag` steering syntax, so it gets a
    # parallel, Read-based orchestrator template. All other platforms use the
    # generic one. Keep both in sync (INV-L3-030). [ClaudeCode-Alignment C2]
    param([string]$PlatformName)
    if ($PlatformName -eq "claude-code") {
        $claude = Join-Path $PackagesRoot "session-orchestrator.claude.md"
        if (Test-Path $claude) { return $claude }
    }
    return (Join-Path $PackagesRoot "session-orchestrator.md")
}

function Install-Orchestrator {
    param([string]$PlatformName, [string]$Target, [bool]$IsDryRun)

    $src = Get-OrchestratorSource -PlatformName $PlatformName
    if (-not (Test-Path $src)) {
        Write-Warn "session-orchestrator.md missing from family source - sessions would load no orchestrator (context-budget risk, INV-L3-027)."
        return ""
    }

    $rel  = Get-OrchestratorDest -PlatformName $PlatformName
    $dest = Join-Path $Target $rel

    if ($IsDryRun) {
        Write-Host "    [DRY RUN] Would deploy orchestrator: session-orchestrator.md -> $rel" -ForegroundColor Yellow
        return $rel
    }

    $destDir = Split-Path -Parent $dest
    if ($destDir -and -not (Test-Path $destDir)) { New-Item -ItemType Directory -Force -Path $destDir | Out-Null }
    Copy-Item $src -Destination $dest -Force
    Write-Step "Deployed session orchestrator -> $rel  (the family only always-loaded steering file)"
    return $rel
}

# -----------------------------------------------------------------------------
# Claude Code entry point (C1, ClaudeCode-Alignment). Claude Code auto-loads ONLY
# a real `CLAUDE.md` (no `CLAUDE*.md` glob), so the deployed orchestrator never
# loads on its own. We wire it in via a `CLAUDE.md` `@import`. Idempotent, marker-
# guarded, append-safe for users who already have a CLAUDE.md. Returns a small
# object recorded in the manifest so uninstall can cleanly reverse it.
# -----------------------------------------------------------------------------

function Install-ClaudeEntrypoint {
    param([string]$PlatformName, [string]$Target, [string]$OrchestratorRel, [bool]$IsDryRun)
    if ($PlatformName -ne "claude-code" -or [string]::IsNullOrEmpty($OrchestratorRel)) { return $null }

    $claudeMd  = Join-Path $Target "CLAUDE.md"
    $import    = "@$OrchestratorRel"                       # e.g. @CLAUDE_PDLC_ORCHESTRATOR.md
    $startTag  = "<!-- AIFLC:$Family`:orchestrator-import:start -->"
    $endTag    = "<!-- AIFLC:$Family`:orchestrator-import:end -->"
    $block     = "$startTag`n$import`n$endTag"

    if ($IsDryRun) {
        Write-Host "    [DRY RUN] Would ensure root CLAUDE.md imports $import" -ForegroundColor Yellow
        return @{ path = "CLAUDE.md"; created = $false }
    }

    if (Test-Path $claudeMd) {
        $existing = Get-Content $claudeMd -Raw
        if ($existing -match [regex]::Escape($import)) {
            Write-Info "CLAUDE.md already imports the orchestrator - left unchanged"
        } else {
            Add-Content -Path $claudeMd -Value "`n$block`n"
            Write-Step "Appended AIFLC orchestrator import to existing CLAUDE.md"
        }
        return @{ path = "CLAUDE.md"; created = $false }
    } else {
        Set-Content -Path $claudeMd -Encoding utf8 -Value "# Project Memory`n`n$block`n"
        Write-Step "Created root CLAUDE.md importing the orchestrator"
        return @{ path = "CLAUDE.md"; created = $true }
    }
}

# -----------------------------------------------------------------------------
# Claude Code slash-command adapter (OI-158 D5). Claude Code turns any Markdown
# file in .claude/commands/ into a /command (subfolders namespace it, so
# .claude/commands/pdlc/pilc.md => /pdlc:pilc). We generate one command per
# installed package (its activation key) plus its destination agent shortcuts.
# Rules: additive & Claude-only; DESTINATION triggers ONLY (never internal build
# triggers SEL__/SEG__/ICG__/...); content is a pointer that Reads the canonical
# core under .aiflc/{family}/ (zero workflow duplication); namespaced by family.
# -----------------------------------------------------------------------------

# Destination agent shortcuts per package (rendered only when the package is installed).
$ClaudeAgentCommands = @{
    "ai-dfe" = @(
        @{ cmd = "dat"; desc = "AI-DFE data operations (gather / status / discover) - the DAT__ shortcut"; hint = "[all | status | gather | discover]" }
        @{ cmd = "dfa"; desc = "AI-DFE data fabric audit (read-only report) - the DFA__ shortcut"; hint = "" }
        @{ cmd = "dhc"; desc = "AI-DFE data fabric bootstrap readiness check - the DHC__ shortcut"; hint = "" }
    )
    "ai-flo" = @(
        @{ cmd = "fhc"; desc = "AI-FLO health check - the FHC__ shortcut"; hint = "" }
        @{ cmd = "fia"; desc = "AI-FLO integrity audit - the FIA__ shortcut"; hint = "" }
    )
}

function Install-ClaudeCommands {
    param([array]$InstalledNames, [string]$PlatformName, [string]$Target, [bool]$IsDryRun)
    if ($PlatformName -ne "claude-code") { return @() }

    $cmdRootRel = ".claude\commands\$Family"
    $cmdRoot    = Join-Path $Target $cmdRootRel
    $written    = @()

    foreach ($name in $InstalledNames) {
        $pkg = $PackageCatalogue | Where-Object { $_.Name -eq $name }
        if (-not $pkg) { continue }
        $short = $name -replace '^ai-', ''            # ai-pilc -> pilc  => /pdlc:pilc
        $key   = "_" + $short.ToUpper() + "_"          # _PILC_
        $core  = "$($pkg.RulesDir)/$($pkg.CoreFile)"   # ai-pilc-rules/core-workflow.md

        # 1) package activation command
        $body = @"
---
description: "$($name.ToUpper()) - $($pkg.Description)"
argument-hint: "[raw input or brief]"
---
Activate the $($name.ToUpper()) workflow - slash-command equivalent of the ``$key`` key.

1. ``Read`` and obey ``.aiflc/$Family/$core`` as the dispatcher for $($name.ToUpper()) for the rest of this session.
2. Resolve rule-details on demand from ``.aiflc/$Family/$($pkg.DetailsDir)/``.
3. Enforce multi-package isolation: if another AI-* package is mid-flow (a non-complete ``*-state.md`` exists), confirm the switch first.
4. Announce "Active package: $($name.ToUpper())" as the first line, then begin with this input:

`$ARGUMENTS
"@
        $written += @{ path = "$cmdRootRel\$short.md"; content = $body }

        # 2) destination agent-shortcut commands for this package (if any)
        if ($ClaudeAgentCommands.ContainsKey($name)) {
            foreach ($ac in $ClaudeAgentCommands[$name]) {
                $hintLine = if ($ac.hint) { "argument-hint: `"$($ac.hint)`"`n" } else { "" }
                $abody = @"
---
description: "$($ac.desc)"
$hintLine---
Run the $($name.ToUpper()) operation equivalent to this shortcut.

1. ``Read`` ``.aiflc/$Family/$core``.
2. Execute the operation named by the argument (default: status/report).

`$ARGUMENTS
"@
                $written += @{ path = "$cmdRootRel\$($ac.cmd).md"; content = $abody }
            }
        }
    }

    if ($written.Count -eq 0) { return @() }

    if ($IsDryRun) {
        Write-Host "    [DRY RUN] Would generate $($written.Count) Claude slash command(s) under $cmdRootRel\ (destination triggers only)" -ForegroundColor Yellow
        return ($written | ForEach-Object { $_.path })
    }

    if (-not (Test-Path $cmdRoot)) { New-Item -ItemType Directory -Force -Path $cmdRoot | Out-Null }
    foreach ($w in $written) {
        Set-Content -Path (Join-Path $Target $w.path) -Encoding utf8 -Value $w.content
    }
    Write-Step "Generated $($written.Count) Claude slash command(s) -> $cmdRootRel\  (/$Family`:<key>)"
    return ($written | ForEach-Object { $_.path })
}

# -----------------------------------------------------------------------------
# Install package agents (Kiro only) - copies runnable agents from each installed
# package templates/agents/ into .kiro/agents/ (e.g. FLO FHC__ / FIA__). [D4]
# Other platforms invoke agents via shortcut-rules blocks (per package INSTALL.md).
# -----------------------------------------------------------------------------

function Install-Agents {
    param([array]$InstalledNames, [string]$PlatformName, [string]$Target, [bool]$IsDryRun)

    if ($PlatformName -ne "kiro") {
        Write-Info "Agents auto-install on Kiro only (other platforms paste shortcut-rules blocks per package INSTALL.md)."
        return @()
    }

    $agentsDest = Join-Path $Target ".kiro\agents"
    $installed = @()

    foreach ($name in $InstalledNames) {
        $pkg = $PackageCatalogue | Where-Object { $_.Name -eq $name }
        if (-not $pkg) { continue }
        $agentsSrc = Join-Path $PackagesRoot "$name\$($pkg.DetailsDir)\templates\agents"
        if (-not (Test-Path $agentsSrc)) { continue }

        $files = Get-ChildItem -Path $agentsSrc -Filter *.md -File -ErrorAction SilentlyContinue | Where-Object {
            $n = $_.Name.ToLower()
            -not ($AgentExcludePatterns | Where-Object { $n -like "*$_*" })
        }
        foreach ($af in $files) {
            if ($IsDryRun) {
                Write-Host "    [DRY RUN] Would install agent: $($af.Name) -> .kiro\agents\" -ForegroundColor Yellow
                $installed += ".kiro\agents\$($af.Name)"
                continue
            }
            if (-not (Test-Path $agentsDest)) { New-Item -ItemType Directory -Force -Path $agentsDest | Out-Null }
            Copy-Item $af.FullName -Destination (Join-Path $agentsDest $af.Name) -Force
            $installed += ".kiro\agents\$($af.Name)"
        }
    }

    if (-not $IsDryRun -and $installed.Count -gt 0) {
        Write-Step "Installed $($installed.Count) agent(s) -> .kiro\agents\"
    }
    return $installed
}

# -----------------------------------------------------------------------------
# Consumer registration (Obligation 1): scan installed tools for data-demand/
# declarations and register each in {family}-ws/data/CONSUMER_REGISTRY.md.
# Generic - any tool shipping data-demand/*.demand.md is auto-registered.
# -----------------------------------------------------------------------------

function Register-Consumers {
    param([string]$Target, [bool]$IsDryRun)
    if ($IsDryRun) { return }
    $dataRoot = Join-Path (Join-Path $Target $FamilyWs) "data"
    $registryPath = Join-Path $dataRoot "CONSUMER_REGISTRY.md"
    $extRootDest = Join-Path (Join-Path (Join-Path $Target $FamilyWs) "tools") "extensions"
    if (-not (Test-Path $registryPath) -or -not (Test-Path $extRootDest)) { return }

    $demandFiles = @(Get-ChildItem -Path $extRootDest -Recurse -File -Filter "*.demand.md" -ErrorAction SilentlyContinue |
        Where-Object { $_.Directory.Name -eq 'data-demand' })
    if (-not $demandFiles) { return }

    $registry = Get-Content $registryPath -Raw
    $now = (Get-Date).ToUniversalTime().ToString("o")
    $added = 0
    foreach ($df in $demandFiles) {
        $consumer = $df.Directory.Parent.Name
        if ($registry -match [regex]::Escape("| $consumer |")) { continue }
        $base = $df.Name -replace '\.demand\.md$', ''
        $consumerHome = "$FamilyWs/tools/extensions/$consumer"
        $row = "| $consumer | $consumerHome | $consumerHome/data-demand/$($df.Name) | $FamilyWs/data/$base.json | $now |"
        Add-Content -Path $registryPath -Value $row
        $registry += "`n$row"
        $added++
    }
    if ($added -gt 0) { Write-Step "Registered $added consumer(s) in data\CONSUMER_REGISTRY.md" }
}

# -----------------------------------------------------------------------------
# Manifest (lives inside {family}-ws/)
# -----------------------------------------------------------------------------

function Save-Manifest {
    param([string]$Target, [string]$PlatformName, [array]$Installed, [array]$Tools, [array]$Fabric, [array]$Agents, [string]$Orchestrator, $ClaudeEntrypoint, [array]$ClaudeCommands)
    $manifest = @{
        installedAt      = (Get-Date -Format "o")
        family           = $Family
        platform         = $PlatformName
        installerVersion = "2.4.0"
        packages         = $Installed
        tools            = $Tools
        fabric           = $Fabric
        agents           = $Agents
        orchestrator     = $Orchestrator
        claudeEntrypoint = $ClaudeEntrypoint
        claudeCommands   = $ClaudeCommands
    }
    $manifestPath = Join-Path $Target "$FamilyWs\$ManifestFileName"
    $manifest | ConvertTo-Json -Depth 4 | Out-File -FilePath $manifestPath -Encoding utf8
    Write-Info "Manifest saved: $FamilyWs\$ManifestFileName"
}

function Remove-EmptyAncestors {
    # Walk up from a removed file/dir, deleting empty parent dirs, but never
    # touching shared platform roots (.kiro, steering, .amazonq, rules, etc.) or the target.
    param([string]$LeafPath, [string]$StopAt)
    $protected = @('.kiro', 'steering', '.amazonq', 'rules', '.cursor', '.clinerules', '.github')
    $dir = Split-Path -Parent $LeafPath
    while ($dir -and $dir -ne $StopAt -and (Test-Path $dir)) {
        $leaf = Split-Path -Leaf $dir
        if ($protected -contains $leaf) { break }
        if (((Get-ChildItem $dir -Force -ErrorAction SilentlyContinue) | Measure-Object).Count -gt 0) { break }
        $parent = Split-Path -Parent $dir
        Remove-Item -Force -Recurse $dir
        $dir = $parent
    }
}

function Invoke-Uninstall {
    param([string]$Target)
    $manifestPath = Join-Path $Target "$FamilyWs\$ManifestFileName"
    if (-not (Test-Path $manifestPath)) {
        Write-Warn "No manifest found at $manifestPath - nothing to uninstall."
        return
    }
    $manifest = Get-Content $manifestPath -Raw | ConvertFrom-Json

    Write-Host ""
    Write-Host "  Installed packages found ($($manifest.platform), family: $($manifest.family)):" -ForegroundColor White
    foreach ($pkg in $manifest.packages) { Write-Host "    - $($pkg.Name)" -ForegroundColor DarkGray }
    Write-Host ""

    $confirm = Read-Host "  Remove installed package files? [y/N]"
    if ($confirm -ne "y" -and $confirm -ne "Y") { Write-Info "Uninstall cancelled."; return }

    foreach ($pkg in $manifest.packages) {
        $corePath = Join-Path $Target $pkg.CoreDest
        $detailsPath = Join-Path $Target $pkg.DetailsDest
        if (Test-Path $corePath) { Remove-Item -Force $corePath }
        if (Test-Path $detailsPath) { Remove-Item -Recurse -Force $detailsPath }
        Remove-EmptyAncestors -LeafPath $corePath -StopAt $Target
        Remove-EmptyAncestors -LeafPath $detailsPath -StopAt $Target
        Write-Step "Removed $($pkg.Name)"
    }
    Remove-Item -Force $manifestPath

    # Remove installed family tools (extensions)
    if ($manifest.PSObject.Properties.Name -contains 'tools' -and $manifest.tools) {
        foreach ($toolRel in $manifest.tools) {
            $toolPath = Join-Path $Target $toolRel
            if (Test-Path $toolPath) {
                Remove-Item -Recurse -Force $toolPath
                Write-Step "Removed tool: $toolRel"
            }
        }
        # Clean up now-empty tools\extensions and tools roots (inside the family workspace).
        $extRoot = Join-Path $Target "$FamilyWs\tools\extensions"
        if ((Test-Path $extRoot) -and -not (Get-ChildItem $extRoot -Force -ErrorAction SilentlyContinue)) { Remove-Item -Force $extRoot }
        $toolsRoot = Join-Path $Target "$FamilyWs\tools"
        if ((Test-Path $toolsRoot) -and -not (Get-ChildItem $toolsRoot -Force -ErrorAction SilentlyContinue)) { Remove-Item -Force $toolsRoot }
    }

    # Remove deployed fabric trio (FLO/DFE routing graph)
    if ($manifest.PSObject.Properties.Name -contains 'fabric' -and $manifest.fabric) {
        foreach ($rel in $manifest.fabric) {
            $p = Join-Path $Target $rel
            if (Test-Path $p) { Remove-Item -Force $p; Write-Step "Removed fabric: $rel" }
            Remove-EmptyAncestors -LeafPath $p -StopAt $Target
        }
    }

    # Remove deployed session orchestrator (the family always-loaded entry point)
    if ($manifest.PSObject.Properties.Name -contains 'orchestrator' -and $manifest.orchestrator) {
        $p = Join-Path $Target $manifest.orchestrator
        if (Test-Path $p) { Remove-Item -Force $p; Write-Step "Removed orchestrator: $($manifest.orchestrator)" }
        Remove-EmptyAncestors -LeafPath $p -StopAt $Target
    }

    # Remove installed agents
    if ($manifest.PSObject.Properties.Name -contains 'agents' -and $manifest.agents) {
        foreach ($rel in $manifest.agents) {
            $p = Join-Path $Target $rel
            if (Test-Path $p) { Remove-Item -Force $p; Write-Step "Removed agent: $rel" }
            Remove-EmptyAncestors -LeafPath $p -StopAt $Target
        }
    }

    # Remove the Claude Code entry point (CLAUDE.md). If the installer created the
    # file, remove it entirely; if it only appended an import block to a pre-existing
    # user CLAUDE.md, strip just the marker-guarded block and keep their content.
    if ($manifest.PSObject.Properties.Name -contains 'claudeEntrypoint' -and $manifest.claudeEntrypoint) {
        $ep = $manifest.claudeEntrypoint
        $epPath = Join-Path $Target $ep.path
        if (Test-Path $epPath) {
            if ($ep.created) {
                Remove-Item -Force $epPath
                Write-Step "Removed Claude entry point: $($ep.path)"
            } else {
                $startTag = "<!-- AIFLC:$($manifest.family)`:orchestrator-import:start -->"
                $endTag   = "<!-- AIFLC:$($manifest.family)`:orchestrator-import:end -->"
                $pattern  = "(?s)\r?\n?" + [regex]::Escape($startTag) + ".*?" + [regex]::Escape($endTag) + "\r?\n?"
                $content  = Get-Content $epPath -Raw
                $stripped = [regex]::Replace($content, $pattern, "")
                Set-Content -Path $epPath -Encoding utf8 -Value $stripped
                Write-Step "Removed orchestrator import block from existing CLAUDE.md (content preserved)"
            }
        }
    }

    # Remove generated Claude slash commands (.claude/commands/{family}/)
    if ($manifest.PSObject.Properties.Name -contains 'claudeCommands' -and $manifest.claudeCommands) {
        foreach ($rel in $manifest.claudeCommands) {
            $p = Join-Path $Target $rel
            if (Test-Path $p) { Remove-Item -Force $p }
            Remove-EmptyAncestors -LeafPath $p -StopAt $Target
        }
        Write-Step "Removed $($manifest.claudeCommands.Count) Claude slash command(s)"
    }

    # Offer to remove the family workspace (DESTRUCTIVE - contains project data)
    $wsRoot = Join-Path $Target $FamilyWs
    if (Test-Path $wsRoot) {
        Write-Host ""
        Write-Warn "The family workspace '$FamilyWs' contains your project data (ideas, projects, portfolio, data)."
        $rmWs = Read-Host "  Remove '$FamilyWs' and ALL its data? [y/N]"
        if ($rmWs -eq "y" -or $rmWs -eq "Y") {
            Remove-Item -Recurse -Force $wsRoot
            Write-Step "Removed family workspace: $FamilyWs"
        } else {
            Write-Info "Kept '$FamilyWs' (project data preserved)."
        }
    }
    Write-Step "Uninstall complete."
}

# -----------------------------------------------------------------------------
# Main Flow
# -----------------------------------------------------------------------------

Write-Banner

if ($Uninstall) {
    if (-not $TargetWorkspace) { $TargetWorkspace = Read-Host "  Target workspace path" }
    Invoke-Uninstall -Target $TargetWorkspace
    exit 0
}

# Step 1: Target workspace
if (-not $TargetWorkspace) {
    $TargetWorkspace = Read-Host "  Enter target workspace path (where you want to install the family)"
}
$TargetWorkspace = $TargetWorkspace.Trim('"').Trim("'")

if (-not (Test-Path $TargetWorkspace)) {
    $create = Read-Host "  Target doesn't exist. Create it? [Y/n]"
    if ($create -ne "n" -and $create -ne "N") {
        New-Item -ItemType Directory -Force -Path $TargetWorkspace | Out-Null
        Write-Step "Created: $TargetWorkspace"
    } else {
        Write-Host "  Aborted." -ForegroundColor Red; exit 1
    }
}

# Validate {family}-ws/ placement (root-level only)
if (-not (Test-FamilyWsPlacement -Target $TargetWorkspace)) { exit 1 }

# Multi-family awareness: report any other *-ws siblings
$otherWs = Get-ChildItem -Path $TargetWorkspace -Directory -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '-ws$' -and $_.Name -ne $FamilyWs }
if ($otherWs) {
    Write-Info "Other family workspace(s) detected: $($otherWs.Name -join ', '). They will not be touched."
}

Write-Info "Target: $TargetWorkspace"
Write-Info "Family: $Family  (workspace folder: $FamilyWs)"
Write-Host ""

# Step 2: Platform
if (-not $Platform) {
    Show-Platforms
    $platformChoice = Read-Host "  Select platform [1-6]"
    $Platform = Get-PlatformFromChoice $platformChoice
    if (-not $Platform) { Write-Host "  Invalid selection. Aborted." -ForegroundColor Red; exit 1 }
}
Write-Step "Platform: $Platform"
Write-Host ""

# Step 3: Package selection
$selectedPackageNames = @()
if ($Bundle) {
    $selectedPackageNames = $Bundles[$Bundle]
    Write-Step "Bundle: $Bundle ($($selectedPackageNames -join ', '))"
}
elseif ($Packages) {
    $selectedPackageNames = @($Packages -split "," | ForEach-Object { $_.Trim() })
}
else {
    Show-Bundles
    $bundleChoice = Read-Host "  Select bundle [F/M/A/G/P/C]"
    switch ($bundleChoice.ToUpper()) {
        "F" { $selectedPackageNames = $Bundles["full"] }
        "M" { $selectedPackageNames = $Bundles["minimal"] }
        "A" { $selectedPackageNames = $Bundles["arch"] }
        "G" { $selectedPackageNames = $Bundles["governance"] }
        "P" { $selectedPackageNames = $Bundles["portfolio"] }
        "C" {
            Show-PackageCatalogue
            $picks = Read-Host "  Enter package numbers separated by commas (e.g. 1,2,5)"
            $indices = $picks -split "," | ForEach-Object { [int]$_.Trim() - 1 }
            $selectedPackageNames = $indices | ForEach-Object { $PackageCatalogue[$_].Name }
        }
        default { Write-Host "  Invalid selection. Aborted." -ForegroundColor Red; exit 1 }
    }
}

# Validate names
$validNames = $PackageCatalogue | ForEach-Object { $_.Name }
$invalidPkgs = $selectedPackageNames | Where-Object { $_ -notin $validNames }
if ($invalidPkgs) {
    Write-Warn "Unknown packages: $($invalidPkgs -join ', ')"
    Write-Host "  Valid packages: $($validNames -join ', ')" -ForegroundColor DarkGray
    exit 1
}

Write-Host ""
Write-Host "  Packages to install:" -ForegroundColor White
foreach ($name in $selectedPackageNames) {
    $pkg = $PackageCatalogue | Where-Object { $_.Name -eq $name }
    Write-Host "    + $name - $($pkg.Description)" -ForegroundColor Green
}
Write-Host ""

if (-not $DryRun -and -not $Force) {
    $confirm = Read-Host "  Proceed with installation? [Y/n]"
    if ($confirm -eq "n" -or $confirm -eq "N") { Write-Host "  Aborted." -ForegroundColor Red; exit 0 }
}

# Step 4: Install package files
Write-Host ""
Write-Host "  Installing package files..." -ForegroundColor White
Write-Host "  ---------------------------" -ForegroundColor DarkGray
$installedPackages = @()
foreach ($name in $selectedPackageNames) {
    $pkg = $PackageCatalogue | Where-Object { $_.Name -eq $name }
    $result = Install-Package -Package $pkg -PlatformName $Platform -Target $TargetWorkspace -IsDryRun $DryRun -IsForce $Force
    if ($result) { $installedPackages += $result }
}

# Step 5: Family workspace skeleton + bootstraps
Write-Host ""
Write-Host "  Setting up family workspace..." -ForegroundColor White
Write-Host "  ------------------------------" -ForegroundColor DarkGray
New-FamilyWorkspaceSkeleton -Target $TargetWorkspace -IsDryRun $DryRun

# Step 6: Family tools (visual tools / extensions)
Write-Host ""
Write-Host "  Installing family tools..." -ForegroundColor White
Write-Host "  --------------------------" -ForegroundColor DarkGray
$installedTools = Install-Tools -Target $TargetWorkspace -IsDryRun $DryRun -IsForce $Force
Register-Consumers -Target $TargetWorkspace -IsDryRun $DryRun

# Step 6b: Fabric trio (FLO/DFE routing graph) + agents
Write-Host ""
Write-Host "  Deploying fabric + agents..." -ForegroundColor White
Write-Host "  ----------------------------" -ForegroundColor DarkGray
$installedFabric = Install-Fabric -PlatformName $Platform -Target $TargetWorkspace -IsDryRun $DryRun
$installedOrchestrator = Install-Orchestrator -PlatformName $Platform -Target $TargetWorkspace -IsDryRun $DryRun
$installedClaudeEntrypoint = Install-ClaudeEntrypoint -PlatformName $Platform -Target $TargetWorkspace -OrchestratorRel $installedOrchestrator -IsDryRun $DryRun
$installedClaudeCommands = Install-ClaudeCommands -InstalledNames ($installedPackages | ForEach-Object { $_.Name }) -PlatformName $Platform -Target $TargetWorkspace -IsDryRun $DryRun
$installedAgents = Install-Agents -InstalledNames ($installedPackages | ForEach-Object { $_.Name }) -PlatformName $Platform -Target $TargetWorkspace -IsDryRun $DryRun

# Step 7: Manifest
if (-not $DryRun -and $installedPackages.Count -gt 0) {
    Write-Host ""
    Save-Manifest -Target $TargetWorkspace -PlatformName $Platform -Installed $installedPackages -Tools $installedTools -Fabric $installedFabric -Agents $installedAgents -Orchestrator $installedOrchestrator -ClaudeEntrypoint $installedClaudeEntrypoint -ClaudeCommands $installedClaudeCommands
}

# Step 7: Summary
Write-Host ""
Write-Host "  ================================================================" -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "  DRY RUN COMPLETE - no files were copied." -ForegroundColor Yellow
} else {
    Write-Host "  Installation complete! $($installedPackages.Count) package(s) installed." -ForegroundColor Green
    Write-Host "  Family workspace ready: $FamilyWs\" -ForegroundColor Green
}
Write-Host "  ================================================================" -ForegroundColor Cyan
Write-Host ""

if (-not $DryRun -and $installedPackages.Count -gt 0) {
    Write-Host "  Next steps:" -ForegroundColor White
    Write-Host "    1. Open your workspace in your IDE" -ForegroundColor DarkGray
    Write-Host "    2. Start a new AI chat session" -ForegroundColor DarkGray
    $firstPkg = @($selectedPackageNames)[0].ToUpper()
    Write-Host "    3. Say: 'Using $firstPkg, help me...'" -ForegroundColor DarkGray
    Write-Host "    Outputs will be generated under $FamilyWs\" -ForegroundColor DarkGray
    Write-Host ""
    if ($Platform -ne "kiro" -and ($selectedPackageNames -contains "ai-gce")) {
        Write-Warn "AI-GCE hooks require Kiro for auto-enforcement."
        Write-Host "    See PLATFORM_CAPABILITIES.md for alternative enforcement strategies." -ForegroundColor DarkGray
        Write-Host ""
    }
}

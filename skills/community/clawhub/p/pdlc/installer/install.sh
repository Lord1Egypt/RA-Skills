#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# PARALLEL IMPLEMENTATION: install.sh (bash) and install.ps1 (PowerShell) are
# feature-equivalent siblings. ANY behavioral change here MUST be mirrored in
# install.ps1, and vice versa. This script MUST stay bash-3.2 safe (macOS ships
# /bin/bash 3.2.57): NO `declare -A`, `${var,,}`, or `${var^^}`. Enforced by
# INV-L3-029. [ClaudeCode-Alignment / macos-bash-fix]
# ─────────────────────────────────────────────────────────────────────────────
# AI-* Family — Package Installer (macOS / Linux)
# Installs into the locked family-workspace structure:
#   Package files  -> .aiflc/{family}/   (cores + rule-details, uniform on every platform; OI-158)
#   Orchestrator   -> platform-native auto-load slot (e.g. .kiro/steering/) - sole always-loaded file
#   Family outputs -> {family}-ws/        (ideas/ projects/ portfolio/ data/)
# Family auto-derived from this installer's parent folder name (e.g. "pdlc").
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGES_ROOT="$(dirname "$SCRIPT_DIR")"
FAMILY="$(basename "$PACKAGES_ROOT")"
FAMILY_WS="${FAMILY}-ws"

# ─────────────────────────────────────────────────────────────────────────────
# Package Catalogue
# ─────────────────────────────────────────────────────────────────────────────

declare -a PKG_NAMES=("ai-ilc" "ai-pilc" "ai-ppm" "ai-flo" "ai-adlc" "ai-uxd" "ai-polc" "ai-dwg" "ai-gce" "ai-tge" "ai-dfe")
declare -a PKG_LAYERS=("Portfolio" "Portfolio" "Portfolio" "Edge" "Project" "Project" "Project" "Project" "Project" "Project" "Edge")
declare -a PKG_DESCS=(
    "Evaluate raw ideas -> Approved Idea Brief"
    "Raw requirement -> Project Initiation Package (PIP)"
    "Multiple PIPs -> Portfolio governance & prioritization"
    "Package-to-package flow orchestration"
    "Requirements -> Architecture Package (AP)"
    "PIP/AP -> UX Design Package (personas, flows, design system)"
    "PIP/AP -> Product Backlog Package (PBP)"
    "AP + PBP + UXP -> Ready-to-code workspace"
    "Workspace -> Compliance enforcement layer"
    "Workspace -> Test strategy, register, coverage tracking"
    "Gather, shape, and distribute structured data"
)
declare -a PKG_COREFILES=("core-workflow.md" "core-workflow.md" "core-engine.md" "core-engine.md" "core-workflow.md" "core-workflow.md" "core-workflow.md" "core-generator.md" "core-generator.md" "core-engine.md" "core-engine.md")
declare -a PKG_RULESDIRS=("ai-ilc-rules" "ai-pilc-rules" "ai-ppm-rules" "ai-flo-rules" "ai-adlc-rules" "ai-uxd-rules" "ai-polc-rules" "ai-dwg-rules" "ai-gce-rules" "ai-tge-rules" "ai-dfe-rules")
declare -a PKG_DETAILSDIRS=("ai-ilc-rule-details" "ai-pilc-rule-details" "ai-ppm-rule-details" "ai-flo-rule-details" "ai-adlc-rule-details" "ai-uxd-rule-details" "ai-polc-rule-details" "ai-dwg-rule-details" "ai-gce-rule-details" "ai-tge-rule-details" "ai-dfe-rule-details")

# NOTE: bash 3.2 compatibility (macOS ships /bin/bash 3.2.57). Do NOT use
# `declare -A` (associative arrays), `${var,,}`, or `${var^^}` — all are bash 4+
# only and fail on stock macOS. Use case-lookup functions + `tr` instead. [macos-bash-fix]
bundle_lookup() {
    case "$1" in
        full)       echo "ai-ilc,ai-pilc,ai-ppm,ai-flo,ai-adlc,ai-uxd,ai-polc,ai-dwg,ai-gce,ai-tge,ai-dfe" ;;
        minimal)    echo "ai-pilc,ai-adlc,ai-dwg" ;;
        arch)       echo "ai-adlc,ai-dwg,ai-gce" ;;
        governance) echo "ai-gce,ai-tge" ;;
        portfolio)  echo "ai-ilc,ai-pilc,ai-ppm,ai-flo" ;;
        *)          echo "" ;;
    esac
}

MANIFEST_FILE=".ai-family-manifest.json"

TARGET=""; PLATFORM=""; PACKAGES=""; BUNDLE=""; DRY_RUN=false; FORCE=false; UNINSTALL=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --target|-t)     TARGET="$2"; shift 2 ;;
        --platform|-p)   PLATFORM="$2"; shift 2 ;;
        --packages)      PACKAGES="$2"; shift 2 ;;
        --bundle|-b)     BUNDLE="$2"; shift 2 ;;
        --dry-run)       DRY_RUN=true; shift ;;
        --force)         FORCE=true; shift ;;
        --uninstall)     UNINSTALL=true; shift ;;
        --help|-h)
            echo "Usage: install.sh [OPTIONS]"
            echo "  --target, -t     Target workspace path"
            echo "  --platform, -p   Platform (kiro|cursor|claude-code|cline|amazonq|copilot)"
            echo "  --packages       Comma-separated package names"
            echo "  --bundle, -b     Preset bundle (full|minimal|arch|governance|portfolio)"
            echo "  --dry-run        Show what would be installed"
            echo "  --force          Overwrite without prompting"
            echo "  --uninstall      Remove installed packages"
            exit 0 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

GREEN='\033[0;32m'; CYAN='\033[0;36m'; YELLOW='\033[1;33m'; MAGENTA='\033[0;35m'; GRAY='\033[0;90m'; WHITE='\033[1;37m'; RED='\033[0;31m'; NC='\033[0m'

banner() {
    echo ""
    echo -e "${CYAN}================================================================${NC}"
    echo -e "${CYAN}      AI-* Family - Package Installer   (family: $FAMILY)${NC}"
    echo -e "${CYAN}================================================================${NC}"
    echo ""
}
step()  { echo -e "  ${GREEN}> $1${NC}"; }
info()  { echo -e "  ${GRAY}i $1${NC}"; }
warn()  { echo -e "  ${YELLOW}! $1${NC}"; }

show_platforms() {
    echo ""; echo -e "  ${WHITE}Supported Platforms:${NC}"; echo ""
    echo "    [1] Kiro            (VS Code-based, full feature support)"
    echo "    [2] Amazon Q        (full workflow support)"
    echo "    [3] Cursor          (full workflow support)"
    echo "    [4] Cline           (full workflow support)"
    echo "    [5] Claude Code     (full workflow support)"
    echo "    [6] GitHub Copilot  (partial - workspace-level only)"
    echo ""
}
show_bundles() {
    echo ""; echo -e "  ${WHITE}Preset Bundles:${NC}"; echo ""
    echo "    [F] Full         - All 11 packages (complete family)"
    echo "    [M] Minimal      - AI-PILC + AI-ADLC + AI-DWG"
    echo "    [A] Architecture - AI-ADLC + AI-DWG + AI-GCE"
    echo "    [G] Governance   - AI-GCE + AI-TGE"
    echo "    [P] Portfolio    - AI-ILC + AI-PILC + AI-PPM + AI-FLO"
    echo "    [C] Custom       - Pick individual packages"
    echo ""
}
show_catalogue() {
    echo ""; echo -e "  ${WHITE}Available Packages:${NC}"; echo ""
    local current_layer=""
    for i in "${!PKG_NAMES[@]}"; do
        local idx=$((i + 1))
        if [[ "${PKG_LAYERS[$i]}" != "$current_layer" ]]; then
            current_layer="${PKG_LAYERS[$i]}"
            echo -e "  ${MAGENTA}[$current_layer Layer]${NC}"
        fi
        printf "    %2d. %-10s - %s\n" "$idx" "${PKG_NAMES[$i]}" "${PKG_DESCS[$i]}"
    done
    echo ""
}
platform_from_choice() {
    case "$1" in
        1) echo "kiro" ;; 2) echo "amazonq" ;; 3) echo "cursor" ;;
        4) echo "cline" ;; 5) echo "claude-code" ;; 6) echo "copilot" ;; *) echo "" ;;
    esac
}
pkg_index() {
    local name="$1"
    for i in "${!PKG_NAMES[@]}"; do
        if [[ "${PKG_NAMES[$i]}" == "$name" ]]; then echo "$i"; return; fi
    done
    echo "-1"
}

# ─────────────────────────────────────────────────────────────────────────────
# Family workspace skeleton + bootstraps
# ─────────────────────────────────────────────────────────────────────────────

create_skeleton() {
    local target="$1"
    local ws_root="$target/$FAMILY_WS"
    local data_root="$ws_root/data"

    if [[ -d "$ws_root" ]]; then
        info "Family workspace '$FAMILY_WS' already exists - update mode (skeleton preserved)."
        return
    fi

    if [[ "$DRY_RUN" == true ]]; then
        echo -e "    ${YELLOW}[DRY RUN] Would create $FAMILY_WS/ skeleton (ideas, projects, portfolio, data) + core/${NC}"
        return
    fi

    mkdir -p "$ws_root/ideas" "$ws_root/projects" "$ws_root/portfolio" \
             "$data_root/demands" "$data_root/history" "$target/core"

    cat > "$ws_root/projects/PROJECTS.md" << EOF
<!-- Generated by AI-* Family installer | family: $FAMILY -->
# Projects Registry

Active project: _none yet_

| Project ID | Folder | Active | Notes |
|------------|--------|:------:|-------|
| _(empty - the first package run will register a project here)_ | | | |
EOF

    cat > "$data_root/REGISTRY.json" << EOF
{
  "\$generatedBy": "AI-DFE",
  "\$family": "$FAMILY",
  "files": {},
  "cross-family": {}
}
EOF

    cat > "$data_root/CONSUMER_REGISTRY.md" << EOF
<!-- AI-DFE consumer registry | family: $FAMILY | bootstrapped empty by installer -->
# Consumer Registry - $FAMILY

> Demander index. Consumers register here at install (Obligation 1). Demander discovery (Stage 1.3) reads this. Bootstrapped empty - no rows.

| consumer | home | demandFile | outputFile | registeredOn |
|----------|------|------------|------------|--------------|
EOF

    cat > "$data_root/dfe-state.md" << EOF
<!-- Generated by AI-* Family installer | DFE state | family: $FAMILY -->
# Data Fabric State - AI-DFE

data-fabric:
  family: $FAMILY
  discovered: {}
  demands: {}
EOF

    step "Created family workspace skeleton: $FAMILY_WS/ + core/"
}

# ─────────────────────────────────────────────────────────────────────────────
# Install a single package
# ─────────────────────────────────────────────────────────────────────────────

install_package() {
    local pkg_name="$1" platform="$2" target="$3"
    local idx; idx=$(pkg_index "$pkg_name")
    if [[ "$idx" == "-1" ]]; then warn "Unknown package: $pkg_name - skipping"; return 1; fi

    local rules_dir="${PKG_RULESDIRS[$idx]}"
    local details_dir="${PKG_DETAILSDIRS[$idx]}"
    local core_file="${PKG_COREFILES[$idx]}"
    local core_source="$PACKAGES_ROOT/$pkg_name/$rules_dir/$core_file"
    local details_source="$PACKAGES_ROOT/$pkg_name/$details_dir"

    if [[ ! -f "$core_source" ]]; then warn "Source not found: $core_source - skipping $pkg_name"; return 1; fi

    # OI-158 (unified core placement): cores AND rule-details land in ONE uniform
    # brand-scoped home on EVERY platform -> .aiflc/{family}/. Only the orchestrator
    # sits in each platform's native auto-load slot (see orchestrator_dest); it Reads
    # the relevant core on demand. Collapses the former 6-way matrix and fixes the
    # rule-details resolution mismatch. Mirror of install.ps1 Get-PlatformPaths (INV-L3-029). [INV-L3-031]
    local core_dest="" details_dest=""
    core_dest="$target/.aiflc/$FAMILY/$rules_dir/$core_file"
    details_dest="$target/.aiflc/$FAMILY/$details_dir"

    if [[ -f "$core_dest" ]] && [[ "$FORCE" != true ]] && [[ "$DRY_RUN" != true ]]; then
        read -rp "    $pkg_name already exists at target. Overwrite? [y/N] " response
        if [[ "$response" != "y" && "$response" != "Y" ]]; then info "Skipped $pkg_name"; return 1; fi
    fi

    if [[ "$DRY_RUN" == true ]]; then
        echo -e "    ${YELLOW}[DRY RUN] Would install $pkg_name:${NC}"
        echo -e "      ${GRAY}Core:    $core_source${NC}"
        echo -e "      ${GRAY}     ->  $core_dest${NC}"
        echo -e "      ${GRAY}Details: $details_source${NC}"
        echo -e "      ${GRAY}     ->  $details_dest${NC}"
        echo "$pkg_name|${core_dest#$target/}|${details_dest#$target/}"
        return 0
    fi

    mkdir -p "$(dirname "$core_dest")"
    # OI-158: cores are neutral files in .aiflc/{family}/, Read on demand by the
    # orchestrator - no platform-specific auto-load frontmatter is injected
    # (the former Cursor .mdc alwaysApply wrapper is gone).
    cp "$core_source" "$core_dest"

    if [[ -d "$details_source" ]]; then
        mkdir -p "$(dirname "$details_dest")"
        rm -rf "$details_dest"
        cp -R "$details_source" "$details_dest"
    fi

    step "Installed $pkg_name"
    echo "$pkg_name|${core_dest#$target/}|${details_dest#$target/}"
    return 0
}

# ─────────────────────────────────────────────────────────────────────────────
# Install family tools (visual tools / extensions under tools/)
# ─────────────────────────────────────────────────────────────────────────────

# Dev-only artifacts that must never be copied into a user workspace.
TOOLS_EXCLUDE=(node_modules dist demo)

# Fabric trio — family-root routing artifacts read at runtime by AI-FLO and AI-DFE.
# Live in the FAMILY workspace (planning/orchestration), NOT the DWG-generated dev
# workspace. Without them FLO returns NOT READY ("no bindings = no routing"). [OI-123]
FABRIC_FILES=("FAMILY_BINDINGS.md" "GATE_PROTOCOL.md" "FAMILY_INTERFACE.md" "TRIGGER_KEYS_REFERENCE.md")

# Files inside a package's templates/agents/ that are NOT runnable agents (skip on agent install).
AGENT_EXCLUDE=("shortcut-rules-block" "-guide" "-section")

install_tools() {
    local target="$1"
    local tools_src="$PACKAGES_ROOT/tools"
    if [[ ! -d "$tools_src" ]]; then
        info "No tools/ directory in this family - nothing to install."
        return 0
    fi

    local ext_root="$tools_src/extensions"
    local -a ext_dirs=()
    if [[ -d "$ext_root" ]]; then
        for d in "$ext_root"/*/; do [[ -d "$d" ]] && ext_dirs+=("$(basename "$d")"); done
    fi

    if [[ "$DRY_RUN" == true ]]; then
        echo -e "    ${YELLOW}[DRY RUN] Would install family tools to $FAMILY_WS/tools/:${NC}"
        for e in "${ext_dirs[@]}"; do
            echo -e "      ${GRAY}$FAMILY_WS/tools/extensions/$e/ (excludes: ${TOOLS_EXCLUDE[*]})${NC}"
        done
        [[ ${#ext_dirs[@]} -eq 0 ]] && echo -e "      ${GRAY}(no extensions found)${NC}"
        return 0
    fi

    # Build find prune expression for excluded directories.
    local copied=0 f dest
    while IFS= read -r f; do
        dest="$target/$FAMILY_WS/tools/${f#$tools_src/}"
        mkdir -p "$(dirname "$dest")"
        cp "$f" "$dest"
        copied=$((copied + 1))
    done < <(find "$tools_src" \( -name node_modules -o -name dist -o -name demo \) -prune -o -type f -print)

    if [[ ${#ext_dirs[@]} -gt 0 ]]; then
        step "Installed family tools: ${ext_dirs[*]} ($copied files -> $FAMILY_WS/tools/)"
    else
        step "Installed family tools ($copied files -> $FAMILY_WS/tools/)"
    fi
}

# ─────────────────────────────────────────────────────────────────────────────
# Deploy the fabric trio (FLO/DFE routing graph) + package agents
# ─────────────────────────────────────────────────────────────────────────────

family_root_dest() {
    # Family home root - parent of every package rules/ + rule-details/ dir.
    # OI-158: uniform .aiflc/{family}/ on every platform. Fabric files land here
    # (beside cores + details). Mirror of install.ps1 Get-FamilyRootDest (INV-L3-029).
    echo ".aiflc/$FAMILY"
}

install_fabric() {
    local platform="$1" target="$2"
    local root_rel; root_rel="$(family_root_dest "$platform")"
    local root_dest="$target/$root_rel"
    local deployed=() missing=()
    local f src
    for f in "${FABRIC_FILES[@]}"; do
        src="$PACKAGES_ROOT/$f"
        if [[ ! -f "$src" ]]; then missing+=("$f"); continue; fi
        if [[ "$DRY_RUN" == true ]]; then
            echo -e "    ${YELLOW}[DRY RUN] Would deploy fabric: $f -> $root_rel/$f${NC}" >&2
            deployed+=("$root_rel/$f"); continue
        fi
        mkdir -p "$root_dest"
        cp "$src" "$root_dest/$f"
        deployed+=("$root_rel/$f")
    done
    [[ ${#missing[@]} -gt 0 ]] && warn "Fabric file(s) missing from family source: ${missing[*]}. FLO/DFE routing may be unavailable." >&2
    if [[ "$DRY_RUN" != true && ${#deployed[@]} -gt 0 ]]; then
        step "Deployed fabric trio (${#deployed[@]}) -> $root_rel/  (FLO/DFE routing graph)" >&2
    fi
    [[ ${#deployed[@]} -gt 0 ]] && printf '%s\n' "${deployed[@]}"
    return 0
}

# Where the always-loaded session orchestrator lands per platform (mirrors core_dest).
orchestrator_dest() {
    case "$1" in
        # Kiro auto-includes (`inclusion: auto`) only files directly in .kiro/steering/ —
        # a nested family subfolder would NOT auto-load, defeating the orchestrator (OI-127).
        kiro)        echo ".kiro/steering/session-orchestrator.md" ;;
        amazonq)     echo ".amazonq/rules/$FAMILY/session-orchestrator.md" ;;
        cursor)      echo ".cursor/rules/${FAMILY}-session-orchestrator.mdc" ;;
        cline)       echo ".clinerules/${FAMILY}-session-orchestrator.md" ;;
        claude-code) local uf; uf=$(echo "$FAMILY" | tr '[:lower:]-' '[:upper:]_'); echo "CLAUDE_${uf}_ORCHESTRATOR.md" ;;
        copilot)     echo ".github/copilot-instructions-${FAMILY}-orchestrator.md" ;;
    esac
}

# Deploy the session orchestrator — the family's SINGLE always-loaded steering file.
# All package cores ship `inclusion: manual`; this orchestrator (`inclusion: auto`)
# is the sole entry point and routes to one package on demand (OI-127 / INV-L3-027).
# Which orchestrator source to deploy. Claude Code cannot use Kiro `#hashtag`
# steering syntax, so it gets a parallel, Read-based template. Keep both in
# sync (INV-L3-030). [ClaudeCode-Alignment C2]
orchestrator_source() {
    if [[ "$1" == "claude-code" && -f "$PACKAGES_ROOT/session-orchestrator.claude.md" ]]; then
        echo "$PACKAGES_ROOT/session-orchestrator.claude.md"
    else
        echo "$PACKAGES_ROOT/session-orchestrator.md"
    fi
}

install_orchestrator() {
    local platform="$1" target="$2"
    local src; src="$(orchestrator_source "$platform")"
    if [[ ! -f "$src" ]]; then
        warn "session-orchestrator.md missing from family source — sessions would load no orchestrator (context-budget risk, INV-L3-027)." >&2
        return 0
    fi
    local rel; rel="$(orchestrator_dest "$platform")"
    local dest="$target/$rel"
    if [[ "$DRY_RUN" == true ]]; then
        echo -e "    ${YELLOW}[DRY RUN] Would deploy orchestrator: session-orchestrator.md -> $rel${NC}" >&2
        echo "$rel"; return 0
    fi
    mkdir -p "$(dirname "$dest")"
    cp "$src" "$dest"
    step "Deployed session orchestrator -> $rel  (the family's only always-loaded steering file)" >&2
    echo "$rel"
    return 0
}

# Claude Code entry point (C1, ClaudeCode-Alignment). Claude Code auto-loads ONLY
# a real CLAUDE.md (no CLAUDE*.md glob), so the deployed orchestrator never loads
# on its own. Wire it in via a CLAUDE.md `@import`. Idempotent, marker-guarded,
# append-safe. Echoes status to stdout: created|appended|exists|dryrun|"".
install_claude_entrypoint() {   # args: platform target orchestrator_rel
    [[ "$1" == "claude-code" ]] || { echo ""; return 0; }
    [[ -n "$3" ]] || { echo ""; return 0; }
    local claude_md="$2/CLAUDE.md" import="@$3"
    local start_tag="<!-- AIFLC:${FAMILY}:orchestrator-import:start -->"
    local end_tag="<!-- AIFLC:${FAMILY}:orchestrator-import:end -->"
    if [[ "$DRY_RUN" == true ]]; then
        echo -e "    ${YELLOW}[DRY RUN] Would ensure root CLAUDE.md imports $import${NC}" >&2
        echo "dryrun"; return 0
    fi
    if [[ -f "$claude_md" ]]; then
        if grep -qF "$import" "$claude_md"; then
            info "CLAUDE.md already imports the orchestrator - left unchanged" >&2
            echo "exists"
        else
            printf '\n%s\n%s\n%s\n' "$start_tag" "$import" "$end_tag" >> "$claude_md"
            step "Appended AIFLC orchestrator import to existing CLAUDE.md" >&2
            echo "appended"
        fi
    else
        printf '# Project Memory\n\n%s\n%s\n%s\n' "$start_tag" "$import" "$end_tag" > "$claude_md"
        step "Created root CLAUDE.md importing the orchestrator" >&2
        echo "created"
    fi
    return 0
}

# ─────────────────────────────────────────────────────────────────────────────
# Claude Code slash-command adapter (OI-158 D5). Generates .claude/commands/{family}/*.md
# (=> /{family}:<key>), one per installed package plus its destination agent shortcuts.
# Additive & Claude-only; DESTINATION triggers ONLY (never internal build triggers);
# each command is a pointer that Reads the canonical core under .aiflc/{family}/.
# Mirror of install.ps1 Install-ClaudeCommands (INV-L3-029). Echoes deployed rel-paths.
# ─────────────────────────────────────────────────────────────────────────────

# Destination agent shortcuts per package: echo "cmd|desc|hint" lines (bash-3.2 safe, no assoc arrays).
claude_agent_cmds() {
    case "$1" in
        ai-dfe)
            echo "dat|AI-DFE data operations (gather / status / discover) - the DAT__ shortcut|[all | status | gather | discover]"
            echo "dfa|AI-DFE data fabric audit (read-only report) - the DFA__ shortcut|"
            echo "dhc|AI-DFE data fabric bootstrap readiness check - the DHC__ shortcut|" ;;
        ai-flo)
            echo "fhc|AI-FLO health check - the FHC__ shortcut|"
            echo "fia|AI-FLO integrity audit - the FIA__ shortcut|" ;;
    esac
}

install_claude_commands() {
    local platform="$1" target="$2"; shift 2
    local names=("$@")
    [[ "$platform" == "claude-code" ]] || return 0
    local cmd_root_rel=".claude/commands/$FAMILY"
    local cmd_root="$target/$cmd_root_rel"
    local written=()
    local name idx short key rules core details desc up line ac_cmd ac_desc ac_hint rest
    [[ "$DRY_RUN" != true ]] && mkdir -p "$cmd_root"

    for name in "${names[@]}"; do
        idx=$(pkg_index "$name")
        [[ "$idx" == "-1" ]] && continue
        rules="${PKG_RULESDIRS[$idx]}"; core="${PKG_COREFILES[$idx]}"
        details="${PKG_DETAILSDIRS[$idx]}"; desc="${PKG_DESCS[$idx]}"
        short="${name#ai-}"
        up="$(echo "$name" | tr '[:lower:]' '[:upper:]')"
        key="_$(echo "$short" | tr '[:lower:]' '[:upper:]')_"

        if [[ "$DRY_RUN" != true ]]; then
            {
                echo "---"
                echo "description: \"$up - $desc\""
                echo "argument-hint: \"[raw input or brief]\""
                echo "---"
                echo "Activate the $up workflow - slash-command equivalent of the \`$key\` key."
                echo ""
                echo "1. \`Read\` and obey \`.aiflc/$FAMILY/$rules/$core\` as the dispatcher for the rest of this session."
                echo "2. Resolve rule-details on demand from \`.aiflc/$FAMILY/$details/\`."
                echo "3. Enforce multi-package isolation: if another AI-* package is mid-flow (a non-complete \`*-state.md\` exists), confirm the switch first."
                echo "4. Announce \"Active package: $up\" as the first line, then begin with this input:"
                echo ""
                echo "\$ARGUMENTS"
            } > "$cmd_root/$short.md"
        fi
        written+=("$cmd_root_rel/$short.md")

        while IFS= read -r line; do
            [[ -z "$line" ]] && continue
            ac_cmd="${line%%|*}"; rest="${line#*|}"
            ac_desc="${rest%%|*}"; ac_hint="${rest##*|}"
            if [[ "$DRY_RUN" != true ]]; then
                {
                    echo "---"
                    echo "description: \"$ac_desc\""
                    [[ -n "$ac_hint" ]] && echo "argument-hint: \"$ac_hint\""
                    echo "---"
                    echo "Run the $up operation equivalent to this shortcut."
                    echo ""
                    echo "1. \`Read\` \`.aiflc/$FAMILY/$rules/$core\`."
                    echo "2. Execute the operation named by the argument (default: status/report)."
                    echo ""
                    echo "\$ARGUMENTS"
                } > "$cmd_root/$ac_cmd.md"
            fi
            written+=("$cmd_root_rel/$ac_cmd.md")
        done < <(claude_agent_cmds "$name")
    done

    [[ ${#written[@]} -eq 0 ]] && return 0
    if [[ "$DRY_RUN" == true ]]; then
        echo -e "    ${YELLOW}[DRY RUN] Would generate ${#written[@]} Claude slash command(s) under $cmd_root_rel/ (destination triggers only)${NC}" >&2
    else
        step "Generated ${#written[@]} Claude slash command(s) -> $cmd_root_rel/  (/$FAMILY:<key>)" >&2
    fi
    printf '%s\n' "${written[@]}"
    return 0
}

# Kiro only — copy runnable agents from each installed package's templates/agents/
# into .kiro/agents/ (e.g. FLO's FHC__ / FIA__). [D4]
install_agents() {
    local platform="$1" target="$2"; shift 2
    local names=("$@")
    if [[ "$platform" != "kiro" ]]; then
        info "Agents auto-install on Kiro only (other platforms paste shortcut-rules blocks per package INSTALL.md)." >&2
        return 0
    fi
    local agents_dest="$target/.kiro/agents"
    local installed=()
    local name idx details src af bn lc pat skip
    for name in "${names[@]}"; do
        idx=$(pkg_index "$name")
        [[ "$idx" == "-1" ]] && continue
        details="${PKG_DETAILSDIRS[$idx]}"
        src="$PACKAGES_ROOT/$name/$details/templates/agents"
        [[ -d "$src" ]] || continue
        for af in "$src"/*.md; do
            [[ -f "$af" ]] || continue
            bn="$(basename "$af")"; lc="$(echo "$bn" | tr '[:upper:]' '[:lower:]')"; skip=false
            for pat in "${AGENT_EXCLUDE[@]}"; do [[ "$lc" == *"$pat"* ]] && skip=true && break; done
            [[ "$skip" == true ]] && continue
            if [[ "$DRY_RUN" == true ]]; then
                echo -e "    ${YELLOW}[DRY RUN] Would install agent: $bn -> .kiro/agents/${NC}" >&2
                installed+=(".kiro/agents/$bn"); continue
            fi
            mkdir -p "$agents_dest"
            cp "$af" "$agents_dest/$bn"
            installed+=(".kiro/agents/$bn")
        done
    done
    if [[ "$DRY_RUN" != true && ${#installed[@]} -gt 0 ]]; then
        step "Installed ${#installed[@]} agent(s) -> .kiro/agents/" >&2
    fi
    [[ ${#installed[@]} -gt 0 ]] && printf '%s\n' "${installed[@]}"
    return 0
}

# ─────────────────────────────────────────────────────────────────────────────
# Consumer registration (Obligation 1): scan installed tools for data-demand/
# declarations and register each in {family}-ws/data/CONSUMER_REGISTRY.md.
# Generic — any tool shipping data-demand/*.demand.md is auto-registered.
# ─────────────────────────────────────────────────────────────────────────────

register_consumers() {
    local target="$1"
    [[ "$DRY_RUN" == true ]] && return 0
    local registry="$target/$FAMILY_WS/data/CONSUMER_REGISTRY.md"
    local ext_dest="$target/$FAMILY_WS/tools/extensions"
    [[ -f "$registry" && -d "$ext_dest" ]] || return 0

    local now added=0 df consumer base
    now="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    while IFS= read -r df; do
        # df = .../tools/extensions/<EXT>/data-demand/<name>.demand.md
        consumer="$(basename "$(dirname "$(dirname "$df")")")"
        grep -q "| $consumer |" "$registry" && continue
        base="$(basename "$df")"; base="${base%.demand.md}"
        printf '| %s | %s | %s | %s | %s |\n' \
            "$consumer" \
            "$FAMILY_WS/tools/extensions/$consumer" \
            "$FAMILY_WS/tools/extensions/$consumer/data-demand/$(basename "$df")" \
            "$FAMILY_WS/data/$base.json" \
            "$now" >> "$registry"
        added=$((added + 1))
    done < <(find "$ext_dest" -type d -name data-demand -exec find {} -type f -name '*.demand.md' \;)
    [[ $added -gt 0 ]] && step "Registered $added consumer(s) in data/CONSUMER_REGISTRY.md"
    return 0
}

# ─────────────────────────────────────────────────────────────────────────────
# Uninstall
# ─────────────────────────────────────────────────────────────────────────────

do_uninstall() {
    local target="$1"
    local manifest="$target/$FAMILY_WS/$MANIFEST_FILE"
    if [[ ! -f "$manifest" ]]; then warn "No manifest found at $manifest - nothing to uninstall."; exit 1; fi

    echo ""; echo -e "  ${WHITE}Installed packages found:${NC}"
    if command -v jq &>/dev/null; then
        jq -r '.packages[].Name' "$manifest" | while read -r name; do echo "    - $name"; done
    else
        grep -o '"Name":[ ]*"[^"]*"' "$manifest" | sed 's/.*"Name":[ ]*"//;s/"//' | while read -r name; do echo "    - $name"; done
    fi

    echo ""; read -rp "  Remove installed package files? [y/N] " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then info "Uninstall cancelled."; exit 0; fi

    if command -v jq &>/dev/null; then
        jq -r '.packages[] | "\(.CoreDest)|\(.DetailsDest)"' "$manifest" | while IFS='|' read -r core details; do
            [[ -f "$target/$core" ]] && rm -f "$target/$core"
            [[ -d "$target/$details" ]] && rm -rf "$target/$details"
        done
        step "Removed package files"
    else
        warn "jq not found - please remove files manually based on $MANIFEST_FILE"
    fi
    rm -f "$manifest"

    # Remove installed family tools (extensions). tools/ lives inside the family
    # workspace and is created exclusively by this installer.
    if [[ -d "$target/$FAMILY_WS/tools/extensions" ]]; then
        rm -rf "$target/$FAMILY_WS/tools/extensions"
        rmdir "$target/$FAMILY_WS/tools" 2>/dev/null || true
        step "Removed family tools"
    fi

    # Remove deployed fabric trio + agents (paths recorded in manifest).
    if command -v jq &>/dev/null; then
        jq -r '(.fabric // [])[]' "$manifest" 2>/dev/null | while read -r rel; do
            [[ -n "$rel" && -f "$target/$rel" ]] && rm -f "$target/$rel" && step "Removed fabric: $rel"
        done
        jq -r '(.agents // [])[]' "$manifest" 2>/dev/null | while read -r rel; do
            [[ -n "$rel" && -f "$target/$rel" ]] && rm -f "$target/$rel" && step "Removed agent: $rel"
        done
        orch="$(jq -r '.orchestrator // empty' "$manifest" 2>/dev/null)"
        [[ -n "$orch" && -f "$target/$orch" ]] && rm -f "$target/$orch" && step "Removed orchestrator: $orch"
        # Remove the Claude Code entry point. If the installer created CLAUDE.md,
        # delete it; if it only appended an import block to a pre-existing user
        # CLAUDE.md, strip just the marker-guarded block and keep their content.
        ep_path="$(jq -r '.claudeEntrypoint.path // empty' "$manifest" 2>/dev/null)"
        ep_created="$(jq -r '.claudeEntrypoint.created // empty' "$manifest" 2>/dev/null)"
        if [[ -n "$ep_path" && -f "$target/$ep_path" ]]; then
            if [[ "$ep_created" == "true" ]]; then
                rm -f "$target/$ep_path" && step "Removed Claude entry point: $ep_path"
            else
                sed -i.bak '/orchestrator-import:start/,/orchestrator-import:end/d' "$target/$ep_path" && rm -f "$target/$ep_path.bak"
                step "Removed orchestrator import block from existing CLAUDE.md (content preserved)"
            fi
        fi
        # Remove generated Claude slash commands (.claude/commands/{family}/)
        cc_count=0
        while IFS= read -r cc; do
            [[ -z "$cc" ]] && continue
            [[ -f "$target/$cc" ]] && rm -f "$target/$cc" && cc_count=$((cc_count+1))
        done < <(jq -r '.claudeCommands[]? // empty' "$manifest" 2>/dev/null)
        if [[ $cc_count -gt 0 ]]; then
            step "Removed $cc_count Claude slash command(s)"
            rmdir "$target/.claude/commands/$FAMILY" 2>/dev/null || true
            rmdir "$target/.claude/commands" 2>/dev/null || true
            rmdir "$target/.claude" 2>/dev/null || true
        fi
        # Prune now-empty .kiro/agents
        agents_dir="$target/.kiro/agents"
        [[ -d "$agents_dir" ]] && [[ -z "$(ls -A "$agents_dir" 2>/dev/null)" ]] && rmdir "$agents_dir" 2>/dev/null || true
    else
        warn "jq not found - remove fabric files + agents manually based on $MANIFEST_FILE"
    fi

    local ws_root="$target/$FAMILY_WS"
    if [[ -d "$ws_root" ]]; then
        echo ""
        warn "The family workspace '$FAMILY_WS' contains your project data."
        read -rp "  Remove '$FAMILY_WS' and ALL its data? [y/N] " rmws
        if [[ "$rmws" == "y" || "$rmws" == "Y" ]]; then
            rm -rf "$ws_root"; step "Removed family workspace: $FAMILY_WS"
        else
            info "Kept '$FAMILY_WS' (project data preserved)."
        fi
    fi
    step "Uninstall complete."
}

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

banner

if [[ "$UNINSTALL" == true ]]; then
    if [[ -z "$TARGET" ]]; then read -rp "  Target workspace path: " TARGET; fi
    do_uninstall "$TARGET"; exit 0
fi

if [[ -z "$TARGET" ]]; then read -rp "  Enter target workspace path: " TARGET; fi
TARGET="${TARGET%/}"

if [[ ! -d "$TARGET" ]]; then
    read -rp "  Target doesn't exist. Create it? [Y/n] " create
    if [[ "$create" != "n" && "$create" != "N" ]]; then mkdir -p "$TARGET"; step "Created: $TARGET"
    else echo -e "  ${RED}Aborted.${NC}"; exit 1; fi
fi

# Validate {family}-ws/ placement (root-level only)
PARENT_NAME="$(basename "$(dirname "$TARGET")")"
if [[ "$PARENT_NAME" =~ -ws$ ]]; then
    warn "Target appears nested inside a '*-ws' folder. Family workspaces must be at the workspace root."
    echo -e "  ${RED}Aborted.${NC}"; exit 1
fi

# Multi-family awareness
for d in "$TARGET"/*-ws; do
    [[ -d "$d" ]] || continue
    bn="$(basename "$d")"
    [[ "$bn" != "$FAMILY_WS" ]] && info "Other family workspace detected: $bn (not touched)."
done

info "Target: $TARGET"
info "Family: $FAMILY  (workspace folder: $FAMILY_WS)"
echo ""

if [[ -z "$PLATFORM" ]]; then
    show_platforms
    read -rp "  Select platform [1-6]: " platform_choice
    PLATFORM=$(platform_from_choice "$platform_choice")
    if [[ -z "$PLATFORM" ]]; then echo -e "  ${RED}Invalid selection. Aborted.${NC}"; exit 1; fi
fi
step "Platform: $PLATFORM"; echo ""

declare -a SELECTED=()
if [[ -n "$BUNDLE" ]]; then
    IFS=',' read -ra SELECTED <<< "$(bundle_lookup "$BUNDLE")"
    step "Bundle: $BUNDLE (${SELECTED[*]})"
elif [[ -n "$PACKAGES" ]]; then
    IFS=',' read -ra SELECTED <<< "$PACKAGES"
else
    show_bundles
    read -rp "  Select bundle [F/M/A/G/P/C]: " bundle_choice
    case "$(echo "$bundle_choice" | tr '[:lower:]' '[:upper:]')" in
        F) IFS=',' read -ra SELECTED <<< "$(bundle_lookup full)" ;;
        M) IFS=',' read -ra SELECTED <<< "$(bundle_lookup minimal)" ;;
        A) IFS=',' read -ra SELECTED <<< "$(bundle_lookup arch)" ;;
        G) IFS=',' read -ra SELECTED <<< "$(bundle_lookup governance)" ;;
        P) IFS=',' read -ra SELECTED <<< "$(bundle_lookup portfolio)" ;;
        C)
            show_catalogue
            read -rp "  Enter package numbers (comma-separated): " picks
            IFS=',' read -ra indices <<< "$picks"
            for idx in "${indices[@]}"; do
                idx=$((${idx// /} - 1))
                if [[ $idx -ge 0 && $idx -lt ${#PKG_NAMES[@]} ]]; then SELECTED+=("${PKG_NAMES[$idx]}"); fi
            done ;;
        *) echo -e "  ${RED}Invalid selection. Aborted.${NC}"; exit 1 ;;
    esac
fi

for name in "${SELECTED[@]}"; do
    if [[ "$(pkg_index "$name")" == "-1" ]]; then warn "Unknown package: $name"; exit 1; fi
done

echo ""; echo -e "  ${WHITE}Packages to install:${NC}"
for name in "${SELECTED[@]}"; do
    idx=$(pkg_index "$name")
    echo -e "    ${GREEN}+ $name - ${PKG_DESCS[$idx]}${NC}"
done
echo ""

if [[ "$DRY_RUN" != true && "$FORCE" != true ]]; then
    read -rp "  Proceed with installation? [Y/n] " confirm
    if [[ "$confirm" == "n" || "$confirm" == "N" ]]; then echo -e "  ${RED}Aborted.${NC}"; exit 0; fi
fi

echo ""; echo -e "  ${WHITE}Installing package files...${NC}"; echo -e "  ${GRAY}---------------------------${NC}"
declare -a INSTALLED_JSON=()
for name in "${SELECTED[@]}"; do
    result=$(install_package "$name" "$PLATFORM" "$TARGET" 2>/dev/null || true)
    line=$(echo "$result" | tail -n1)
    if [[ -n "$line" && "$line" == *"|"* ]]; then
        IFS='|' read -ra parts <<< "$line"
        if [[ ${#parts[@]} -eq 3 ]]; then
            INSTALLED_JSON+=("{\"Name\":\"${parts[0]}\",\"CoreDest\":\"${parts[1]}\",\"DetailsDest\":\"${parts[2]}\"}")
        fi
    fi
done

echo ""; echo -e "  ${WHITE}Setting up family workspace...${NC}"; echo -e "  ${GRAY}------------------------------${NC}"
create_skeleton "$TARGET"

echo ""; echo -e "  ${WHITE}Installing family tools...${NC}"; echo -e "  ${GRAY}--------------------------${NC}"
install_tools "$TARGET"
register_consumers "$TARGET"

echo ""; echo -e "  ${WHITE}Deploying fabric + agents...${NC}"; echo -e "  ${GRAY}----------------------------${NC}"
declare -a INSTALLED_NAMES=()
for j in "${INSTALLED_JSON[@]}"; do
    nm=$(echo "$j" | sed 's/.*"Name":"//;s/".*//')
    [[ -n "$nm" ]] && INSTALLED_NAMES+=("$nm")
done
declare -a FABRIC_DEPLOYED=() AGENTS_INSTALLED=()
fabric_out="$(install_fabric "$PLATFORM" "$TARGET")"
while IFS= read -r l; do [[ -n "$l" ]] && FABRIC_DEPLOYED+=("$l"); done <<< "$fabric_out"
ORCHESTRATOR_DEPLOYED="$(install_orchestrator "$PLATFORM" "$TARGET")"
CLAUDE_ENTRY_STATUS="$(install_claude_entrypoint "$PLATFORM" "$TARGET" "$ORCHESTRATOR_DEPLOYED")"
declare -a CLAUDE_COMMANDS=()
if [[ ${#INSTALLED_NAMES[@]} -gt 0 ]]; then
    agents_out="$(install_agents "$PLATFORM" "$TARGET" "${INSTALLED_NAMES[@]}")"
    while IFS= read -r l; do [[ -n "$l" ]] && AGENTS_INSTALLED+=("$l"); done <<< "$agents_out"
    cc_out="$(install_claude_commands "$PLATFORM" "$TARGET" "${INSTALLED_NAMES[@]}")"
    while IFS= read -r l; do [[ -n "$l" ]] && CLAUDE_COMMANDS+=("$l"); done <<< "$cc_out"
fi

if [[ "$DRY_RUN" != true && ${#INSTALLED_JSON[@]} -gt 0 ]]; then
    echo ""
    manifest_path="$TARGET/$FAMILY_WS/$MANIFEST_FILE"
    mkdir -p "$TARGET/$FAMILY_WS"
    # Collect installed tool (extension) relative paths for the manifest.
    declare -a TOOLS_JSON=()
    if [[ -d "$TARGET/$FAMILY_WS/tools/extensions" ]]; then
        for d in "$TARGET/$FAMILY_WS/tools/extensions"/*/; do
            [[ -d "$d" ]] && TOOLS_JSON+=("\"$FAMILY_WS/tools/extensions/$(basename "$d")\"")
        done
    fi
    # Fabric + agent relative paths (JSON strings).
    declare -a FABRIC_JSON=() AGENTS_JSON=() CLAUDE_CMD_JSON=()
    for p in "${FABRIC_DEPLOYED[@]}"; do FABRIC_JSON+=("\"$p\""); done
    for p in "${AGENTS_INSTALLED[@]}"; do AGENTS_JSON+=("\"$p\""); done
    for p in "${CLAUDE_COMMANDS[@]}"; do CLAUDE_CMD_JSON+=("\"$p\""); done
    # Claude Code entry-point record (for clean uninstall). null on other platforms.
    claude_ep_json="null"
    if [[ "$CLAUDE_ENTRY_STATUS" == "created" ]]; then
        claude_ep_json='{"path":"CLAUDE.md","created":true}'
    elif [[ "$CLAUDE_ENTRY_STATUS" == "appended" || "$CLAUDE_ENTRY_STATUS" == "exists" ]]; then
        claude_ep_json='{"path":"CLAUDE.md","created":false}'
    fi
    {
        echo "{"
        echo "  \"installedAt\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\","
        echo "  \"family\": \"$FAMILY\","
        echo "  \"platform\": \"$PLATFORM\","
        echo "  \"installerVersion\": \"2.4.0\","
        echo "  \"packages\": ["
        echo "    $(IFS=','; echo "${INSTALLED_JSON[*]}" | sed 's/},{/},\n    {/g')"
        echo "  ],"
        echo "  \"tools\": [$(IFS=','; echo "${TOOLS_JSON[*]}")],"
        echo "  \"fabric\": [$(IFS=','; echo "${FABRIC_JSON[*]}")],"
        echo "  \"agents\": [$(IFS=','; echo "${AGENTS_JSON[*]}")],"
        echo "  \"orchestrator\": \"$ORCHESTRATOR_DEPLOYED\","
        echo "  \"claudeEntrypoint\": $claude_ep_json,"
        echo "  \"claudeCommands\": [$(IFS=','; echo "${CLAUDE_CMD_JSON[*]}")]"
        echo "}"
    } > "$manifest_path"
    info "Manifest saved: $FAMILY_WS/$MANIFEST_FILE"
fi

echo ""
echo -e "  ${CYAN}================================================================${NC}"
if [[ "$DRY_RUN" == true ]]; then
    echo -e "  ${YELLOW}DRY RUN COMPLETE - no files were copied.${NC}"
else
    echo -e "  ${GREEN}Installation complete! ${#INSTALLED_JSON[@]} package(s) installed.${NC}"
    echo -e "  ${GREEN}Family workspace ready: $FAMILY_WS/${NC}"
fi
echo -e "  ${CYAN}================================================================${NC}"
echo ""

if [[ "$DRY_RUN" != true && ${#INSTALLED_JSON[@]} -gt 0 ]]; then
    echo -e "  ${WHITE}Next steps:${NC}"
    echo -e "    ${GRAY}1. Open your workspace in your IDE${NC}"
    echo -e "    ${GRAY}2. Start a new AI chat session${NC}"
    echo -e "    ${GRAY}3. Say: 'Using ${SELECTED[0]}, help me...'${NC}"
    echo -e "    ${GRAY}Outputs will be generated under $FAMILY_WS/${NC}"
    echo ""
    if [[ "$PLATFORM" != "kiro" ]]; then
        for name in "${SELECTED[@]}"; do
            if [[ "$name" == "ai-gce" ]]; then
                warn "AI-GCE hooks require Kiro for auto-enforcement."
                echo -e "    ${GRAY}See PLATFORM_CAPABILITIES.md for alternatives.${NC}"; echo ""
                break
            fi
        done
    fi
fi

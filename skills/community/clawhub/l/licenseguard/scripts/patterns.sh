#!/usr/bin/env bash
# LicenseGuard -- License Detection Patterns
# Each pattern: REGEX|LICENSE_ID|LICENSE_NAME|RISK_LEVEL
#
# Risk levels:
#   critical — Copyleft/viral: must open-source your code
#   high     — Weak copyleft: must share modifications to the library
#   medium   — Notice required: must include license notice
#   low      — Permissive: minimal restrictions
#   unknown  — Cannot determine risk
#
# IMPORTANT: All regexes must use POSIX ERE syntax (grep -E compatible).

set -euo pipefail

# --- License text detection patterns ------------------------------------------
#
# Format: "regex|license_id|license_name|risk_level"
# Used to match license text in LICENSE/COPYING/NOTICE files.
# Order: critical first, then high, medium, low.

declare -a LICENSE_TEXT_PATTERNS=()

# --- Critical (Copyleft/Viral) -----------------------------------------------

LICENSE_TEXT_PATTERNS+=(
  # GPL-3.0
  'GNU GENERAL PUBLIC LICENSE[[:space:]]*Version 3|GPL-3.0|GNU General Public License v3.0|critical'
  'GPL[- ]?3\.0|GPL-3.0|GNU General Public License v3.0|critical'
  'GPLv3|GPL-3.0|GNU General Public License v3.0|critical'
  'licensed under the GPL version 3|GPL-3.0|GNU General Public License v3.0|critical'
  # GPL-2.0
  'GNU GENERAL PUBLIC LICENSE[[:space:]]*Version 2|GPL-2.0|GNU General Public License v2.0|critical'
  'GPL[- ]?2\.0|GPL-2.0|GNU General Public License v2.0|critical'
  'GPLv2|GPL-2.0|GNU General Public License v2.0|critical'
  'licensed under the GPL version 2|GPL-2.0|GNU General Public License v2.0|critical'
  # AGPL-3.0
  'GNU AFFERO GENERAL PUBLIC LICENSE[[:space:]]*Version 3|AGPL-3.0|GNU Affero General Public License v3.0|critical'
  'AGPL[- ]?3\.0|AGPL-3.0|GNU Affero General Public License v3.0|critical'
  'AGPLv3|AGPL-3.0|GNU Affero General Public License v3.0|critical'
  # SSPL
  'Server Side Public License|SSPL|Server Side Public License|critical'
  'SSPL[- ]?v?1|SSPL|Server Side Public License v1|critical'
  # EUPL
  'European Union Public Licen[cs]e|EUPL|European Union Public License|critical'
  'EUPL[- ]?v?1\.[12]|EUPL|European Union Public License|critical'
  # GPL (generic, without version)
  'licensed under the GNU General Public License|GPL|GNU General Public License|critical'
  'under the terms of the GNU GPL|GPL|GNU General Public License|critical'
)

# --- High (Weak Copyleft) ----------------------------------------------------

LICENSE_TEXT_PATTERNS+=(
  # LGPL-3.0
  'GNU LESSER GENERAL PUBLIC LICENSE[[:space:]]*Version 3|LGPL-3.0|GNU Lesser General Public License v3.0|high'
  'LGPL[- ]?3\.0|LGPL-3.0|GNU Lesser General Public License v3.0|high'
  'LGPLv3|LGPL-3.0|GNU Lesser General Public License v3.0|high'
  # LGPL-2.1
  'GNU LESSER GENERAL PUBLIC LICENSE[[:space:]]*Version 2\.1|LGPL-2.1|GNU Lesser General Public License v2.1|high'
  'LGPL[- ]?2\.1|LGPL-2.1|GNU Lesser General Public License v2.1|high'
  'LGPLv2\.1|LGPL-2.1|GNU Lesser General Public License v2.1|high'
  # MPL-2.0
  'Mozilla Public License[[:space:]]*Version 2\.0|MPL-2.0|Mozilla Public License 2.0|high'
  'MPL[- ]?2\.0|MPL-2.0|Mozilla Public License 2.0|high'
  'This Source Code Form is subject to the terms of the Mozilla Public License|MPL-2.0|Mozilla Public License 2.0|high'
  # EPL-2.0
  'Eclipse Public License[[:space:]]*(v[[:space:]]*)?2\.0|EPL-2.0|Eclipse Public License 2.0|high'
  'EPL[- ]?2\.0|EPL-2.0|Eclipse Public License 2.0|high'
  # EPL-1.0
  'Eclipse Public License[[:space:]]*(v[[:space:]]*)?1\.0|EPL-1.0|Eclipse Public License 1.0|high'
  'EPL[- ]?1\.0|EPL-1.0|Eclipse Public License 1.0|high'
  # CDDL
  'Common Development and Distribution License|CDDL|Common Development and Distribution License|high'
  'CDDL[- ]?1\.[01]|CDDL|Common Development and Distribution License|high'
  # OSL
  'Open Software License[[:space:]]*3\.0|OSL-3.0|Open Software License 3.0|high'
  # CPL
  'Common Public License|CPL-1.0|Common Public License 1.0|high'
)

# --- Medium (Notice Required) ------------------------------------------------

LICENSE_TEXT_PATTERNS+=(
  # Apache-2.0
  'Apache License[[:space:]]*,?[[:space:]]*Version 2\.0|Apache-2.0|Apache License 2.0|medium'
  'Licensed under the Apache License|Apache-2.0|Apache License 2.0|medium'
  # MIT
  'Permission is hereby granted, free of charge|MIT|MIT License|medium'
  'The MIT License|MIT|MIT License|medium'
  'MIT License|MIT|MIT License|medium'
  # BSD-3-Clause
  'Redistribution and use in source and binary forms.*neither the name|BSD-3-Clause|BSD 3-Clause License|medium'
  'BSD[- ]3[- ]Clause|BSD-3-Clause|BSD 3-Clause License|medium'
  # BSD-2-Clause
  'Redistribution and use in source and binary forms.*Redistributions of source code|BSD-2-Clause|BSD 2-Clause License|medium'
  'BSD[- ]2[- ]Clause|BSD-2-Clause|BSD 2-Clause License|medium'
  'Simplified BSD|BSD-2-Clause|BSD 2-Clause Simplified License|medium'
  'FreeBSD License|BSD-2-Clause-FreeBSD|FreeBSD License|medium'
  # ISC
  'ISC License|ISC|ISC License|medium'
  'Permission to use, copy, modify, and/or distribute this software|ISC|ISC License|medium'
  # Artistic-2.0
  'Artistic License 2\.0|Artistic-2.0|Artistic License 2.0|medium'
  # Zlib
  'zlib License|Zlib|zlib License|medium'
  'This software is provided .as-is., without any express or implied warranty|Zlib|zlib License|medium'
  # PostgreSQL
  'PostgreSQL License|PostgreSQL|PostgreSQL License|medium'
  # PSF
  'Python Software Foundation License|PSF-2.0|Python Software Foundation License|medium'
)

# --- Low (Permissive) --------------------------------------------------------

LICENSE_TEXT_PATTERNS+=(
  # Unlicense
  'This is free and unencumbered software released into the public domain|Unlicense|The Unlicense|low'
  'Unlicense|Unlicense|The Unlicense|low'
  # CC0
  'CC0[- ]1\.0|CC0-1.0|Creative Commons Zero v1.0 Universal|low'
  'Creative Commons.*CC0|CC0-1.0|Creative Commons Zero v1.0 Universal|low'
  'No Copyright|CC0-1.0|Creative Commons Zero v1.0 Universal|low'
  # WTFPL
  'DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE|WTFPL|Do What The F*ck You Want To Public License|low'
  'WTFPL|WTFPL|Do What The F*ck You Want To Public License|low'
  # 0BSD
  'Zero-Clause BSD|0BSD|BSD Zero Clause License|low'
  '0BSD|0BSD|BSD Zero Clause License|low'
  # Public Domain
  'Public Domain|Public-Domain|Public Domain|low'
)

# --- SPDX License Identifier Mapping -----------------------------------------
#
# Format: "spdx_id|license_name|risk_level"
# Used to classify licenses found via SPDX identifiers in manifests.

declare -a SPDX_LICENSE_MAP=()

# Critical (Copyleft/Viral)
SPDX_LICENSE_MAP+=(
  'GPL-2.0|GNU General Public License v2.0|critical'
  'GPL-2.0-only|GNU General Public License v2.0 Only|critical'
  'GPL-2.0-or-later|GNU General Public License v2.0 or Later|critical'
  'GPL-3.0|GNU General Public License v3.0|critical'
  'GPL-3.0-only|GNU General Public License v3.0 Only|critical'
  'GPL-3.0-or-later|GNU General Public License v3.0 or Later|critical'
  'AGPL-3.0|GNU Affero General Public License v3.0|critical'
  'AGPL-3.0-only|GNU Affero General Public License v3.0 Only|critical'
  'AGPL-3.0-or-later|GNU Affero General Public License v3.0 or Later|critical'
  'SSPL-1.0|Server Side Public License v1|critical'
  'EUPL-1.1|European Union Public License 1.1|critical'
  'EUPL-1.2|European Union Public License 1.2|critical'
  'GPL-1.0|GNU General Public License v1.0|critical'
  'GPL-1.0-only|GNU General Public License v1.0 Only|critical'
  'GPL-1.0-or-later|GNU General Public License v1.0 or Later|critical'
  'AGPL-1.0|Affero General Public License v1.0|critical'
  'RPL-1.1|Reciprocal Public License 1.1|critical'
  'RPL-1.5|Reciprocal Public License 1.5|critical'
  'CECILL-2.0|CeCILL Free Software License Agreement v2.0|critical'
  'CECILL-2.1|CeCILL Free Software License Agreement v2.1|critical'
)

# High (Weak Copyleft)
SPDX_LICENSE_MAP+=(
  'LGPL-2.0|GNU Library General Public License v2|high'
  'LGPL-2.0-only|GNU Library General Public License v2 Only|high'
  'LGPL-2.0-or-later|GNU Library General Public License v2 or Later|high'
  'LGPL-2.1|GNU Lesser General Public License v2.1|high'
  'LGPL-2.1-only|GNU Lesser General Public License v2.1 Only|high'
  'LGPL-2.1-or-later|GNU Lesser General Public License v2.1 or Later|high'
  'LGPL-3.0|GNU Lesser General Public License v3.0|high'
  'LGPL-3.0-only|GNU Lesser General Public License v3.0 Only|high'
  'LGPL-3.0-or-later|GNU Lesser General Public License v3.0 or Later|high'
  'MPL-2.0|Mozilla Public License 2.0|high'
  'MPL-2.0-no-copyleft-exception|Mozilla Public License 2.0 (no copyleft exception)|high'
  'MPL-1.0|Mozilla Public License 1.0|high'
  'MPL-1.1|Mozilla Public License 1.1|high'
  'EPL-1.0|Eclipse Public License 1.0|high'
  'EPL-2.0|Eclipse Public License 2.0|high'
  'CDDL-1.0|Common Development and Distribution License 1.0|high'
  'CDDL-1.1|Common Development and Distribution License 1.1|high'
  'CPL-1.0|Common Public License 1.0|high'
  'OSL-3.0|Open Software License 3.0|high'
  'OSL-2.1|Open Software License 2.1|high'
  'OSL-2.0|Open Software License 2.0|high'
  'OSL-1.0|Open Software License 1.0|high'
  'APSL-2.0|Apple Public Source License 2.0|high'
  'CECILL-B|CeCILL-B Free Software License Agreement|high'
  'CECILL-C|CeCILL-C Free Software License Agreement|high'
  'IPL-1.0|IBM Public License v1.0|high'
  'MS-RL|Microsoft Reciprocal License|high'
)

# Medium (Notice Required)
SPDX_LICENSE_MAP+=(
  'Apache-2.0|Apache License 2.0|medium'
  'Apache-1.1|Apache License 1.1|medium'
  'Apache-1.0|Apache License 1.0|medium'
  'MIT|MIT License|medium'
  'BSD-2-Clause|BSD 2-Clause Simplified License|medium'
  'BSD-3-Clause|BSD 3-Clause New or Revised License|medium'
  'BSD-3-Clause-LBNL|Lawrence Berkeley National Labs BSD Variant|medium'
  'ISC|ISC License|medium'
  'Artistic-2.0|Artistic License 2.0|medium'
  'Artistic-1.0|Artistic License 1.0|medium'
  'Zlib|zlib License|medium'
  'Libpng|libpng License|medium'
  'MIT-0|MIT No Attribution|medium'
  'MS-PL|Microsoft Public License|medium'
  'PSF-2.0|Python Software Foundation License 2.0|medium'
  'PHP-3.0|PHP License v3.0|medium'
  'PHP-3.01|PHP License v3.01|medium'
  'BSL-1.0|Boost Software License 1.0|medium'
  'PostgreSQL|PostgreSQL License|medium'
  'Unicode-DFS-2016|Unicode License Agreement - Data Files and Software (2016)|medium'
  'X11|X11 License|medium'
  'Zlib|zlib License|medium'
  'curl|curl License|medium'
  'OpenSSL|OpenSSL License|medium'
  'Sleepycat|Sleepycat License|medium'
  'NCSA|University of Illinois/NCSA Open Source License|medium'
  'AFL-3.0|Academic Free License v3.0|medium'
  'ECL-2.0|Educational Community License v2.0|medium'
  'EFL-2.0|Eiffel Forum License v2.0|medium'
  'FTL|Freetype Project License|medium'
  'OFL-1.1|SIL Open Font License 1.1|medium'
  'LPPL-1.3c|LaTeX Project Public License v1.3c|medium'
  'W3C|W3C Software Notice and License|medium'
)

# Low (Permissive)
SPDX_LICENSE_MAP+=(
  'Unlicense|The Unlicense|low'
  'CC0-1.0|Creative Commons Zero v1.0 Universal|low'
  'WTFPL|Do What The F*ck You Want To Public License|low'
  '0BSD|BSD Zero Clause License|low'
  'CC-BY-4.0|Creative Commons Attribution 4.0|low'
  'CC-BY-3.0|Creative Commons Attribution 3.0|low'
  'CC-BY-SA-4.0|Creative Commons Attribution Share Alike 4.0|low'
  'CC-BY-SA-3.0|Creative Commons Attribution Share Alike 3.0|low'
  'SAX-PD|SAX Public Domain|low'
  'DWTFYWWI|Do Whatever The Fuck You Want With It|low'
  'Fair|Fair License|low'
  'JSON|JSON License|low'
)

# --- Manifest file patterns ---------------------------------------------------
#
# Maps filename patterns to ecosystem identifiers.

declare -A MANIFEST_FILES=(
  # npm
  ["package.json"]="npm"
  ["package-lock.json"]="npm"
  ["yarn.lock"]="npm"
  # Python
  ["requirements.txt"]="python"
  ["Pipfile"]="python"
  ["Pipfile.lock"]="python"
  ["pyproject.toml"]="python"
  ["setup.py"]="python"
  ["setup.cfg"]="python"
  # Ruby
  ["Gemfile"]="ruby"
  ["Gemfile.lock"]="ruby"
  # Go
  ["go.mod"]="go"
  ["go.sum"]="go"
  # Java/Kotlin
  ["pom.xml"]="java"
  ["build.gradle"]="java"
  ["build.gradle.kts"]="java"
  # Rust
  ["Cargo.toml"]="rust"
  ["Cargo.lock"]="rust"
  # PHP
  ["composer.json"]="php"
  ["composer.lock"]="php"
  # .NET
  ["packages.config"]="dotnet"
)

# .NET csproj/sln files matched by extension in analyzer.sh

# --- Utility: get SPDX license count -----------------------------------------

licenseguard_spdx_count() {
  echo "${#SPDX_LICENSE_MAP[@]}"
}

# --- Utility: get text pattern count ------------------------------------------

licenseguard_text_pattern_count() {
  echo "${#LICENSE_TEXT_PATTERNS[@]}"
}

# --- Utility: classify an SPDX identifier ------------------------------------

classify_spdx_license() {
  local license_id="$1"

  # Normalize: trim whitespace, handle common variations
  license_id=$(echo "$license_id" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

  for entry in "${SPDX_LICENSE_MAP[@]}"; do
    IFS='|' read -r spdx_id name risk <<< "$entry"
    if [[ "$license_id" == "$spdx_id" ]]; then
      echo "$risk|$spdx_id|$name"
      return 0
    fi
  done

  # Try case-insensitive match
  local lower_id
  lower_id=$(echo "$license_id" | tr '[:upper:]' '[:lower:]')
  for entry in "${SPDX_LICENSE_MAP[@]}"; do
    IFS='|' read -r spdx_id name risk <<< "$entry"
    local lower_spdx
    lower_spdx=$(echo "$spdx_id" | tr '[:upper:]' '[:lower:]')
    if [[ "$lower_id" == "$lower_spdx" ]]; then
      echo "$risk|$spdx_id|$name"
      return 0
    fi
  done

  echo "unknown|$license_id|Unknown License"
  return 0
}

# --- Utility: detect license from file text -----------------------------------

detect_license_from_text() {
  local filepath="$1"

  if [[ ! -f "$filepath" ]]; then
    return 1
  fi

  # Read first 100 lines of the file
  local content
  content=$(head -100 "$filepath" 2>/dev/null) || return 1

  for entry in "${LICENSE_TEXT_PATTERNS[@]}"; do
    IFS='|' read -r regex license_id name risk <<< "$entry"

    if echo "$content" | grep -qE -- "$regex" 2>/dev/null; then
      echo "$risk|$license_id|$name"
      return 0
    fi
  done

  echo "unknown|NOASSERTION|Unknown License"
  return 0
}

# --- Utility: risk level to numeric score -------------------------------------

risk_to_level() {
  case "$1" in
    critical) echo 4 ;;
    high)     echo 3 ;;
    medium)   echo 2 ;;
    low)      echo 1 ;;
    unknown)  echo 3 ;;
    *)        echo 0 ;;
  esac
}

# --- Utility: risk level color ------------------------------------------------

risk_color() {
  case "$1" in
    critical) echo -e "${RED}${BOLD}CRITICAL${NC}" ;;
    high)     echo -e "${RED}HIGH${NC}" ;;
    medium)   echo -e "${YELLOW}MEDIUM${NC}" ;;
    low)      echo -e "${GREEN}LOW${NC}" ;;
    unknown)  echo -e "${MAGENTA}UNKNOWN${NC}" ;;
    *)        echo -e "${DIM}?${NC}" ;;
  esac
}

risk_icon() {
  case "$1" in
    critical) echo -e "${RED}!!${NC}" ;;
    high)     echo -e "${RED}!${NC}" ;;
    medium)   echo -e "${YELLOW}~${NC}" ;;
    low)      echo -e "${GREEN}-${NC}" ;;
    unknown)  echo -e "${MAGENTA}?${NC}" ;;
    *)        echo "?" ;;
  esac
}

# Colors (if not already loaded)
RED="${RED:-\033[0;31m}"
GREEN="${GREEN:-\033[0;32m}"
YELLOW="${YELLOW:-\033[1;33m}"
BLUE="${BLUE:-\033[0;34m}"
CYAN="${CYAN:-\033[0;36m}"
MAGENTA="${MAGENTA:-\033[0;35m}"
BOLD="${BOLD:-\033[1m}"
DIM="${DIM:-\033[2m}"
NC="${NC:-\033[0m}"

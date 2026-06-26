#!/usr/bin/env bash
# LicenseGuard -- Core License Scanning Engine
# Scans dependency manifests for copyleft, viral, and problematic licenses
# across 8 package manager ecosystems.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

# Load patterns
source "$SCRIPT_DIR/patterns.sh"

OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# Free tier manifest file limit
FREE_MANIFEST_LIMIT=5

# --- Utility: check if we have a pro+ license --------------------------------

is_licensed() {
  source "$SCRIPT_DIR/license.sh"
  local tier
  tier=$(get_licenseguard_tier)
  case "$tier" in
    pro|team|enterprise) return 0 ;;
    *) return 1 ;;
  esac
}

# --- Package manager detection ------------------------------------------------

detect_package_managers() {
  local dir="$1"
  local managers=()

  # npm
  if [[ -f "$dir/package.json" || -f "$dir/package-lock.json" || -f "$dir/yarn.lock" ]]; then
    managers+=("npm")
  fi

  # Python
  if [[ -f "$dir/requirements.txt" || -f "$dir/Pipfile" || -f "$dir/Pipfile.lock" || \
        -f "$dir/pyproject.toml" || -f "$dir/setup.py" || -f "$dir/setup.cfg" ]]; then
    managers+=("python")
  fi

  # Ruby
  if [[ -f "$dir/Gemfile" || -f "$dir/Gemfile.lock" ]]; then
    managers+=("ruby")
  fi

  # Go
  if [[ -f "$dir/go.mod" || -f "$dir/go.sum" ]]; then
    managers+=("go")
  fi

  # Java/Kotlin
  if [[ -f "$dir/pom.xml" || -f "$dir/build.gradle" || -f "$dir/build.gradle.kts" ]]; then
    managers+=("java")
  fi

  # Rust
  if [[ -f "$dir/Cargo.toml" || -f "$dir/Cargo.lock" ]]; then
    managers+=("rust")
  fi

  # PHP
  if [[ -f "$dir/composer.json" || -f "$dir/composer.lock" ]]; then
    managers+=("php")
  fi

  # .NET
  local has_dotnet=false
  if [[ -f "$dir/packages.config" ]]; then
    has_dotnet=true
  fi
  # Check for .csproj and .sln files
  if compgen -G "$dir/*.csproj" >/dev/null 2>&1 || \
     compgen -G "$dir/*.sln" >/dev/null 2>&1; then
    has_dotnet=true
  fi
  if [[ "$has_dotnet" == "true" ]]; then
    managers+=("dotnet")
  fi

  printf '%s\n' "${managers[@]}" 2>/dev/null || true
}

# --- Find manifest files ------------------------------------------------------

find_manifest_files() {
  local dir="$1"
  local manifests=()

  # Walk through known manifest filenames
  for filename in "${!MANIFEST_FILES[@]}"; do
    if command -v find &>/dev/null; then
      while IFS= read -r found; do
        [[ -n "$found" ]] && manifests+=("$found")
      done < <(find "$dir" \
        -name ".git" -prune -o \
        -name "node_modules" -prune -o \
        -name "vendor" -prune -o \
        -name ".venv" -prune -o \
        -name "venv" -prune -o \
        -name "target" -prune -o \
        -name "dist" -prune -o \
        -name "build" -prune -o \
        -name "$filename" -type f -print 2>/dev/null)
    else
      # Fallback: check top-level only
      if [[ -f "$dir/$filename" ]]; then
        manifests+=("$dir/$filename")
      fi
    fi
  done

  # Also find .csproj files for .NET
  if command -v find &>/dev/null; then
    while IFS= read -r found; do
      [[ -n "$found" ]] && manifests+=("$found")
    done < <(find "$dir" \
      -name ".git" -prune -o \
      -name "node_modules" -prune -o \
      -name "vendor" -prune -o \
      -name "*.csproj" -type f -print 2>/dev/null)
    while IFS= read -r found; do
      [[ -n "$found" ]] && manifests+=("$found")
    done < <(find "$dir" \
      -name ".git" -prune -o \
      -name "node_modules" -prune -o \
      -name "vendor" -prune -o \
      -name "*.sln" -type f -print 2>/dev/null)
  fi

  # De-duplicate and sort
  printf '%s\n' "${manifests[@]}" 2>/dev/null | sort -u || true
}

# --- npm license extraction ---------------------------------------------------

extract_npm_licenses() {
  local filepath="$1"
  local findings_file="$2"
  local basename
  basename=$(basename "$filepath")

  case "$basename" in
    package.json)
      # Extract dependencies and their licenses from package.json
      if command -v python3 &>/dev/null; then
        python3 -c "
import json, sys
try:
    with open('$filepath') as f:
        pkg = json.load(f)
    # Check for license field
    lic = pkg.get('license', pkg.get('licenses', ''))
    if isinstance(lic, list):
        lic = ' OR '.join([l.get('type', str(l)) if isinstance(l, dict) else str(l) for l in lic])
    elif isinstance(lic, dict):
        lic = lic.get('type', str(lic))
    name = pkg.get('name', 'unknown')
    version = pkg.get('version', 'unknown')
    # Report the project's own license
    if lic:
        print(f'{name}\t{version}\t{lic}\tnpm\t$filepath')
    # Extract dependencies
    for dep_type in ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']:
        deps = pkg.get(dep_type, {})
        for dep_name, dep_ver in deps.items():
            # We can only get license from installed node_modules
            print(f'{dep_name}\t{dep_ver}\tNOASSERTION\tnpm\t$filepath')
except Exception as e:
    pass
" >> "$findings_file" 2>/dev/null
      elif command -v node &>/dev/null; then
        node -e "
try {
  const pkg = require('$filepath');
  let lic = pkg.license || pkg.licenses || '';
  if (Array.isArray(lic)) lic = lic.map(l => l.type || l).join(' OR ');
  if (typeof lic === 'object') lic = lic.type || JSON.stringify(lic);
  const name = pkg.name || 'unknown';
  const version = pkg.version || 'unknown';
  if (lic) console.log(name + '\t' + version + '\t' + lic + '\tnpm\t$filepath');
  for (const depType of ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']) {
    const deps = pkg[depType] || {};
    for (const [n, v] of Object.entries(deps)) {
      console.log(n + '\t' + v + '\tNOASSERTION\tnpm\t$filepath');
    }
  }
} catch(e) {}
" >> "$findings_file" 2>/dev/null
      fi
      ;;

    package-lock.json)
      # Extract licenses from package-lock.json (npm v2/v3 format)
      if command -v python3 &>/dev/null; then
        python3 -c "
import json
try:
    with open('$filepath') as f:
        lock = json.load(f)
    # npm v2+ format: packages
    packages = lock.get('packages', {})
    for pkg_path, info in packages.items():
        if not pkg_path or pkg_path == '':
            continue
        name = pkg_path.split('node_modules/')[-1] if 'node_modules/' in pkg_path else pkg_path
        version = info.get('version', 'unknown')
        lic = info.get('license', 'NOASSERTION')
        if isinstance(lic, dict):
            lic = lic.get('type', 'NOASSERTION')
        print(f'{name}\t{version}\t{lic}\tnpm\t$filepath')
    # npm v1 format: dependencies
    def walk_deps(deps, depth=0):
        if depth > 5:
            return
        for name, info in deps.items():
            version = info.get('version', 'unknown')
            lic = info.get('license', 'NOASSERTION')
            print(f'{name}\t{version}\t{lic}\tnpm\t$filepath')
            sub = info.get('dependencies', {})
            if sub:
                walk_deps(sub, depth + 1)
    if 'dependencies' in lock and not packages:
        walk_deps(lock['dependencies'])
except: pass
" >> "$findings_file" 2>/dev/null
      fi
      ;;

    yarn.lock)
      # Parse yarn.lock for package names and versions
      # yarn.lock doesn't contain licenses, so we mark as NOASSERTION
      if command -v python3 &>/dev/null; then
        python3 -c "
import re
try:
    with open('$filepath') as f:
        content = f.read()
    # Match package entries like: \"package@^version\":
    pattern = r'^\"?(@?[^@\s\"]+)@[^\"]*\"?:?\s*$'
    for match in re.finditer(pattern, content, re.MULTILINE):
        name = match.group(1)
        # Find version in the next few lines
        version_match = re.search(r'version[:\s]+\"?([^\"\s]+)', content[match.end():match.end()+200])
        version = version_match.group(1) if version_match else 'unknown'
        print(f'{name}\t{version}\tNOASSERTION\tnpm\t$filepath')
except: pass
" >> "$findings_file" 2>/dev/null
      else
        # Fallback: grep for version lines
        grep -E '^"?@?[^@].*:$' "$filepath" 2>/dev/null | while IFS= read -r line; do
          local pkg_name
          pkg_name=$(echo "$line" | sed 's/"//g' | sed 's/@[^@]*://' | sed 's/,.*//;s/[[:space:]]//g')
          [[ -n "$pkg_name" ]] && echo -e "${pkg_name}\tunknown\tNOASSERTION\tnpm\t$filepath" >> "$findings_file"
        done
      fi
      ;;
  esac
}

# --- Python license extraction ------------------------------------------------

extract_python_licenses() {
  local filepath="$1"
  local findings_file="$2"
  local basename
  basename=$(basename "$filepath")

  case "$basename" in
    requirements.txt)
      # Parse requirements.txt: package==version or package>=version
      while IFS= read -r line; do
        # Skip comments and empty lines
        [[ -z "$line" || "$line" =~ ^# || "$line" =~ ^-r || "$line" =~ ^-e || "$line" =~ ^-i ]] && continue
        # Extract package name and version
        local pkg_name pkg_version
        pkg_name=$(echo "$line" | sed 's/[>=<!\[].*//;s/[[:space:]]//g')
        pkg_version=$(echo "$line" | grep -oE '[0-9]+\.[0-9]+[0-9.]*' | head -1) || true
        [[ -z "$pkg_name" ]] && continue
        echo -e "${pkg_name}\t${pkg_version:-unknown}\tNOASSERTION\tpython\t$filepath" >> "$findings_file"
      done < "$filepath"
      ;;

    Pipfile)
      # Parse Pipfile [packages] section
      local in_packages=false
      while IFS= read -r line; do
        if [[ "$line" =~ ^\[packages\] || "$line" =~ ^\[dev-packages\] ]]; then
          in_packages=true
          continue
        fi
        if [[ "$line" =~ ^\[ ]]; then
          in_packages=false
          continue
        fi
        if [[ "$in_packages" == "true" && "$line" =~ ^[a-zA-Z] ]]; then
          local pkg_name
          pkg_name=$(echo "$line" | cut -d'=' -f1 | sed 's/[[:space:]]//g')
          local pkg_version
          pkg_version=$(echo "$line" | grep -oE '"[*>=<0-9.]+"' | tr -d '"' | head -1) || true
          [[ -n "$pkg_name" ]] && echo -e "${pkg_name}\t${pkg_version:-unknown}\tNOASSERTION\tpython\t$filepath" >> "$findings_file"
        fi
      done < "$filepath"
      ;;

    Pipfile.lock)
      if command -v python3 &>/dev/null; then
        python3 -c "
import json
try:
    with open('$filepath') as f:
        lock = json.load(f)
    for section in ['default', 'develop']:
        pkgs = lock.get(section, {})
        for name, info in pkgs.items():
            version = info.get('version', 'unknown').lstrip('=')
            print(f'{name}\t{version}\tNOASSERTION\tpython\t$filepath')
except: pass
" >> "$findings_file" 2>/dev/null
      fi
      ;;

    pyproject.toml)
      # Parse pyproject.toml for dependencies
      local in_deps=false
      while IFS= read -r line; do
        if [[ "$line" =~ ^\[project\] || "$line" =~ ^\[tool\.poetry\.dependencies\] ]]; then
          in_deps=true
          continue
        fi
        if [[ "$line" =~ ^\[ && ! "$line" =~ ^\[project\] ]]; then
          in_deps=false
          continue
        fi
        if [[ "$in_deps" == "true" ]]; then
          # Handle dependencies = ["pkg>=1.0", ...]
          if [[ "$line" =~ ^dependencies ]]; then
            local dep_list
            dep_list=$(echo "$line" | grep -oE '"[^"]*"' | tr -d '"')
            while IFS= read -r dep; do
              local pkg_name
              pkg_name=$(echo "$dep" | sed 's/[>=<!\[].*//;s/[[:space:]]//g')
              [[ -n "$pkg_name" ]] && echo -e "${pkg_name}\tunknown\tNOASSERTION\tpython\t$filepath" >> "$findings_file"
            done <<< "$dep_list"
          fi
          # Handle poetry-style: package = "^1.0"
          if [[ "$line" =~ ^[a-zA-Z] && "$line" =~ = ]]; then
            local pkg_name
            pkg_name=$(echo "$line" | cut -d'=' -f1 | sed 's/[[:space:]]//g')
            if [[ "$pkg_name" != "python" && "$pkg_name" != "name" && "$pkg_name" != "version" && \
                  "$pkg_name" != "description" && "$pkg_name" != "readme" && "$pkg_name" != "license" && \
                  "$pkg_name" != "authors" && "$pkg_name" != "requires-python" ]]; then
              echo -e "${pkg_name}\tunknown\tNOASSERTION\tpython\t$filepath" >> "$findings_file"
            fi
          fi
        fi
        # Check for the license field of the project itself
        if [[ "$line" =~ ^license && "$line" =~ = ]]; then
          local proj_license
          proj_license=$(echo "$line" | grep -oE '"[^"]*"' | tr -d '"' | head -1)
          if [[ -n "$proj_license" ]]; then
            echo -e "PROJECT\tunknown\t${proj_license}\tpython\t$filepath" >> "$findings_file"
          fi
        fi
      done < "$filepath"
      ;;

    setup.py)
      # Extract license from setup.py
      if command -v python3 &>/dev/null; then
        python3 -c "
import re
try:
    with open('$filepath') as f:
        content = f.read()
    # Find license= in setup()
    lic = re.search(r'license\s*=\s*[\"'\\''](.*?)[\"'\\'']\s*', content)
    if lic:
        print(f'PROJECT\tunknown\t{lic.group(1)}\tpython\t$filepath')
    # Find install_requires
    reqs = re.search(r'install_requires\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if reqs:
        for dep in re.findall(r'[\"'\\''](.*?)[\"'\\'']\s*', reqs.group(1)):
            name = re.split(r'[>=<!\[]', dep)[0].strip()
            if name:
                print(f'{name}\tunknown\tNOASSERTION\tpython\t$filepath')
except: pass
" >> "$findings_file" 2>/dev/null
      fi
      ;;

    setup.cfg)
      # Parse setup.cfg for license and install_requires
      local in_options=false in_requires=false
      while IFS= read -r line; do
        if [[ "$line" =~ ^\[options\] ]]; then
          in_options=true
          continue
        fi
        if [[ "$line" =~ ^\[options\.install_requires\] || "$line" =~ ^install_requires ]]; then
          in_requires=true
          continue
        fi
        if [[ "$line" =~ ^\[ ]]; then
          in_options=false
          in_requires=false
          continue
        fi
        if [[ "$in_options" == "true" && "$line" =~ ^license ]]; then
          local proj_license
          proj_license=$(echo "$line" | cut -d'=' -f2 | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
          [[ -n "$proj_license" ]] && echo -e "PROJECT\tunknown\t${proj_license}\tpython\t$filepath" >> "$findings_file"
        fi
        if [[ "$in_requires" == "true" && -n "$line" && ! "$line" =~ ^\[ ]]; then
          local pkg_name
          pkg_name=$(echo "$line" | sed 's/[>=<!\[].*//;s/[[:space:]]//g')
          [[ -n "$pkg_name" ]] && echo -e "${pkg_name}\tunknown\tNOASSERTION\tpython\t$filepath" >> "$findings_file"
        fi
      done < "$filepath"
      ;;
  esac
}

# --- Ruby license extraction --------------------------------------------------

extract_ruby_licenses() {
  local filepath="$1"
  local findings_file="$2"
  local basename
  basename=$(basename "$filepath")

  case "$basename" in
    Gemfile)
      # Parse Gemfile: gem 'name', '~> version'
      while IFS= read -r line; do
        [[ -z "$line" || "$line" =~ ^# ]] && continue
        if [[ "$line" =~ ^[[:space:]]*gem ]]; then
          local pkg_name pkg_version
          pkg_name=$(echo "$line" | grep -oE "gem ['\"][^'\"]*['\"]" | sed "s/gem ['\"]//;s/['\"]//g")
          pkg_version=$(echo "$line" | grep -oE "'~?[><=]*[[:space:]]*[0-9][0-9.]*'" | tr -d "'><=~ " | head -1) || true
          [[ -n "$pkg_name" ]] && echo -e "${pkg_name}\t${pkg_version:-unknown}\tNOASSERTION\truby\t$filepath" >> "$findings_file"
        fi
      done < "$filepath"
      ;;

    Gemfile.lock)
      # Parse Gemfile.lock: extract gem names and versions from specs section
      local in_specs=false
      while IFS= read -r line; do
        if [[ "$line" == "    specs:" ]]; then
          in_specs=true
          continue
        fi
        if [[ "$in_specs" == "true" ]]; then
          # Gem entries are indented with 6 spaces: "      gem_name (version)"
          if [[ "$line" =~ ^[[:space:]]{6}[a-zA-Z] ]]; then
            local pkg_name pkg_version
            pkg_name=$(echo "$line" | sed 's/^[[:space:]]*//' | cut -d' ' -f1)
            pkg_version=$(echo "$line" | grep -oE '\([0-9][0-9.]*\)' | tr -d '()') || true
            [[ -n "$pkg_name" ]] && echo -e "${pkg_name}\t${pkg_version:-unknown}\tNOASSERTION\truby\t$filepath" >> "$findings_file"
          fi
          # End of specs section (new section starts with no leading space or different section)
          if [[ ! "$line" =~ ^[[:space:]] && -n "$line" ]]; then
            in_specs=false
          fi
        fi
      done < "$filepath"
      ;;
  esac
}

# --- Go license extraction ----------------------------------------------------

extract_go_licenses() {
  local filepath="$1"
  local findings_file="$2"
  local basename
  basename=$(basename "$filepath")

  case "$basename" in
    go.mod)
      # Parse go.mod: require ( module version )
      local in_require=false
      while IFS= read -r line; do
        [[ -z "$line" || "$line" =~ ^// ]] && continue
        if [[ "$line" =~ ^require[[:space:]]*\( ]]; then
          in_require=true
          continue
        fi
        if [[ "$line" == ")" ]]; then
          in_require=false
          continue
        fi
        # Single-line require
        if [[ "$line" =~ ^require[[:space:]] && ! "$line" =~ \( ]]; then
          local pkg_name pkg_version
          pkg_name=$(echo "$line" | awk '{print $2}')
          pkg_version=$(echo "$line" | awk '{print $3}')
          [[ -n "$pkg_name" ]] && echo -e "${pkg_name}\t${pkg_version:-unknown}\tNOASSERTION\tgo\t$filepath" >> "$findings_file"
          continue
        fi
        if [[ "$in_require" == "true" ]]; then
          local pkg_name pkg_version
          pkg_name=$(echo "$line" | sed 's/^[[:space:]]*//;s/[[:space:]].*//;s/\/\/.*$//')
          pkg_version=$(echo "$line" | awk '{print $2}' | sed 's/\/\/.*$//')
          # Skip indirect dependencies marker
          [[ "$pkg_name" =~ ^// || -z "$pkg_name" ]] && continue
          echo -e "${pkg_name}\t${pkg_version:-unknown}\tNOASSERTION\tgo\t$filepath" >> "$findings_file"
        fi
      done < "$filepath"
      ;;

    go.sum)
      # Parse go.sum: module version hash
      while IFS= read -r line; do
        [[ -z "$line" ]] && continue
        local pkg_name pkg_version
        pkg_name=$(echo "$line" | awk '{print $1}')
        pkg_version=$(echo "$line" | awk '{print $2}' | sed 's|/go.mod$||')
        [[ -n "$pkg_name" ]] && echo -e "${pkg_name}\t${pkg_version:-unknown}\tNOASSERTION\tgo\t$filepath" >> "$findings_file"
      done < "$filepath"
      ;;
  esac
}

# --- Java/Kotlin license extraction -------------------------------------------

extract_java_licenses() {
  local filepath="$1"
  local findings_file="$2"
  local basename
  basename=$(basename "$filepath")

  case "$basename" in
    pom.xml)
      # Extract dependencies and licenses from pom.xml
      if command -v python3 &>/dev/null; then
        python3 -c "
import re
try:
    with open('$filepath') as f:
        content = f.read()
    # Remove XML namespace for easier parsing
    content = re.sub(r'xmlns=[\"'][^\"']*[\"']', '', content)
    # Find project license
    lic_match = re.search(r'<licenses>.*?<name>(.*?)</name>.*?</licenses>', content, re.DOTALL)
    if lic_match:
        print(f'PROJECT\tunknown\t{lic_match.group(1).strip()}\tjava\t$filepath')
    # Find dependencies
    for dep in re.finditer(r'<dependency>.*?<groupId>(.*?)</groupId>.*?<artifactId>(.*?)</artifactId>(?:.*?<version>(.*?)</version>)?.*?</dependency>', content, re.DOTALL):
        group = dep.group(1).strip()
        artifact = dep.group(2).strip()
        version = dep.group(3).strip() if dep.group(3) else 'unknown'
        name = f'{group}:{artifact}'
        print(f'{name}\t{version}\tNOASSERTION\tjava\t$filepath')
except: pass
" >> "$findings_file" 2>/dev/null
      else
        # Fallback: use grep to find artifactId entries
        grep -oE '<artifactId>[^<]*</artifactId>' "$filepath" 2>/dev/null | \
          sed 's/<[^>]*>//g' | while IFS= read -r artifact; do
            [[ -n "$artifact" ]] && echo -e "${artifact}\tunknown\tNOASSERTION\tjava\t$filepath" >> "$findings_file"
          done
      fi
      ;;

    build.gradle|build.gradle.kts)
      # Parse Gradle dependencies
      while IFS= read -r line; do
        [[ -z "$line" || "$line" =~ ^[[:space:]]*// ]] && continue
        # Match patterns like: implementation 'group:artifact:version'
        # or implementation("group:artifact:version")
        if [[ "$line" =~ (implementation|api|compile|runtimeOnly|testImplementation|compileOnly) ]]; then
          local dep_str
          dep_str=$(echo "$line" | grep -oE "['\"][^'\"]*:[^'\"]*['\"]" | tr -d "'\"\(\)" | head -1) || true
          if [[ -n "$dep_str" ]]; then
            local group artifact version
            group=$(echo "$dep_str" | cut -d: -f1)
            artifact=$(echo "$dep_str" | cut -d: -f2)
            version=$(echo "$dep_str" | cut -d: -f3) || true
            [[ -n "$artifact" ]] && echo -e "${group}:${artifact}\t${version:-unknown}\tNOASSERTION\tjava\t$filepath" >> "$findings_file"
          fi
        fi
      done < "$filepath"
      ;;
  esac
}

# --- Rust license extraction --------------------------------------------------

extract_rust_licenses() {
  local filepath="$1"
  local findings_file="$2"
  local basename
  basename=$(basename "$filepath")

  case "$basename" in
    Cargo.toml)
      # Parse Cargo.toml for package license and dependencies
      local in_package=false in_deps=false in_dev_deps=false
      local pkg_name="" pkg_version="" pkg_license=""
      while IFS= read -r line; do
        [[ -z "$line" || "$line" =~ ^# ]] && continue

        if [[ "$line" =~ ^\[package\] ]]; then
          in_package=true; in_deps=false; in_dev_deps=false
          continue
        fi
        if [[ "$line" =~ ^\[dependencies\] ]]; then
          in_deps=true; in_package=false; in_dev_deps=false
          continue
        fi
        if [[ "$line" =~ ^\[dev-dependencies\] ]]; then
          in_dev_deps=true; in_deps=false; in_package=false
          continue
        fi
        if [[ "$line" =~ ^\[build-dependencies\] ]]; then
          in_deps=true; in_package=false; in_dev_deps=false
          continue
        fi
        if [[ "$line" =~ ^\[ && ! "$line" =~ ^\[(package|dependencies|dev-dependencies|build-dependencies)\] ]]; then
          in_package=false; in_deps=false; in_dev_deps=false
          continue
        fi

        if [[ "$in_package" == "true" ]]; then
          if [[ "$line" =~ ^name ]]; then
            pkg_name=$(echo "$line" | grep -oE '"[^"]*"' | tr -d '"')
          fi
          if [[ "$line" =~ ^version ]]; then
            pkg_version=$(echo "$line" | grep -oE '"[^"]*"' | tr -d '"')
          fi
          if [[ "$line" =~ ^license ]]; then
            pkg_license=$(echo "$line" | grep -oE '"[^"]*"' | tr -d '"')
          fi
        fi

        if [[ "$in_deps" == "true" || "$in_dev_deps" == "true" ]]; then
          if [[ "$line" =~ ^[a-zA-Z_-] && "$line" =~ = ]]; then
            local dep_name dep_version
            dep_name=$(echo "$line" | cut -d'=' -f1 | sed 's/[[:space:]]//g')
            dep_version=$(echo "$line" | grep -oE '"[0-9][0-9.]*"' | tr -d '"' | head -1) || true
            [[ -n "$dep_name" ]] && echo -e "${dep_name}\t${dep_version:-unknown}\tNOASSERTION\trust\t$filepath" >> "$findings_file"
          fi
        fi
      done < "$filepath"

      # Output package license if found
      if [[ -n "$pkg_name" && -n "$pkg_license" ]]; then
        echo -e "${pkg_name}\t${pkg_version:-unknown}\t${pkg_license}\trust\t$filepath" >> "$findings_file"
      fi
      ;;

    Cargo.lock)
      # Parse Cargo.lock for package entries
      if command -v python3 &>/dev/null; then
        python3 -c "
try:
    with open('$filepath') as f:
        content = f.read()
    import re
    for match in re.finditer(r'\[\[package\]\]\s*name\s*=\s*\"(.*?)\"\s*version\s*=\s*\"(.*?)\"', content):
        name = match.group(1)
        version = match.group(2)
        print(f'{name}\t{version}\tNOASSERTION\trust\t$filepath')
except: pass
" >> "$findings_file" 2>/dev/null
      else
        # Fallback: simple parsing
        local current_name="" current_version=""
        while IFS= read -r line; do
          if [[ "$line" =~ ^name[[:space:]]*= ]]; then
            current_name=$(echo "$line" | grep -oE '"[^"]*"' | tr -d '"')
          fi
          if [[ "$line" =~ ^version[[:space:]]*= ]]; then
            current_version=$(echo "$line" | grep -oE '"[^"]*"' | tr -d '"')
            if [[ -n "$current_name" ]]; then
              echo -e "${current_name}\t${current_version}\tNOASSERTION\trust\t$filepath" >> "$findings_file"
              current_name=""
              current_version=""
            fi
          fi
        done < "$filepath"
      fi
      ;;
  esac
}

# --- PHP license extraction ---------------------------------------------------

extract_php_licenses() {
  local filepath="$1"
  local findings_file="$2"
  local basename
  basename=$(basename "$filepath")

  case "$basename" in
    composer.json)
      if command -v python3 &>/dev/null; then
        python3 -c "
import json
try:
    with open('$filepath') as f:
        pkg = json.load(f)
    # Project license
    lic = pkg.get('license', '')
    if isinstance(lic, list):
        lic = ' OR '.join(lic)
    name = pkg.get('name', 'unknown')
    version = pkg.get('version', 'unknown')
    if lic:
        print(f'{name}\t{version}\t{lic}\tphp\t$filepath')
    # Dependencies
    for dep_type in ['require', 'require-dev']:
        deps = pkg.get(dep_type, {})
        for dep_name, dep_ver in deps.items():
            if dep_name.startswith('php') or dep_name.startswith('ext-'):
                continue
            print(f'{dep_name}\t{dep_ver}\tNOASSERTION\tphp\t$filepath')
except: pass
" >> "$findings_file" 2>/dev/null
      fi
      ;;

    composer.lock)
      if command -v python3 &>/dev/null; then
        python3 -c "
import json
try:
    with open('$filepath') as f:
        lock = json.load(f)
    for section in ['packages', 'packages-dev']:
        for pkg in lock.get(section, []):
            name = pkg.get('name', 'unknown')
            version = pkg.get('version', 'unknown').lstrip('v')
            lic_list = pkg.get('license', [])
            lic = ' OR '.join(lic_list) if isinstance(lic_list, list) else str(lic_list)
            print(f'{name}\t{version}\t{lic or \"NOASSERTION\"}\tphp\t$filepath')
except: pass
" >> "$findings_file" 2>/dev/null
      fi
      ;;
  esac
}

# --- .NET license extraction --------------------------------------------------

extract_dotnet_licenses() {
  local filepath="$1"
  local findings_file="$2"
  local ext="${filepath##*.}"
  local basename
  basename=$(basename "$filepath")

  case "$basename" in
    packages.config)
      # Parse packages.config XML
      while IFS= read -r line; do
        if [[ "$line" =~ \<package ]]; then
          local pkg_name pkg_version
          pkg_name=$(echo "$line" | grep -oE 'id="[^"]*"' | sed 's/id="//;s/"//')
          pkg_version=$(echo "$line" | grep -oE 'version="[^"]*"' | sed 's/version="//;s/"//')
          [[ -n "$pkg_name" ]] && echo -e "${pkg_name}\t${pkg_version:-unknown}\tNOASSERTION\tdotnet\t$filepath" >> "$findings_file"
        fi
      done < "$filepath"
      ;;

    *)
      # Handle .csproj files
      if [[ "$ext" == "csproj" ]]; then
        while IFS= read -r line; do
          if [[ "$line" =~ \<PackageReference ]]; then
            local pkg_name pkg_version
            pkg_name=$(echo "$line" | grep -oE 'Include="[^"]*"' | sed 's/Include="//;s/"//')
            pkg_version=$(echo "$line" | grep -oE 'Version="[^"]*"' | sed 's/Version="//;s/"//')
            [[ -n "$pkg_name" ]] && echo -e "${pkg_name}\t${pkg_version:-unknown}\tNOASSERTION\tdotnet\t$filepath" >> "$findings_file"
          fi
        done < "$filepath"
      fi
      ;;
  esac
}

# --- Classify a license string to risk level ----------------------------------

classify_license() {
  local license_str="$1"

  # Trim whitespace
  license_str=$(echo "$license_str" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

  # Handle NOASSERTION / empty
  if [[ -z "$license_str" || "$license_str" == "NOASSERTION" || "$license_str" == "UNKNOWN" ]]; then
    echo "unknown|NOASSERTION|No license declared"
    return 0
  fi

  # Handle OR expressions (dual-licensing): check each option
  if [[ "$license_str" =~ " OR " ]]; then
    local best_risk="critical"
    local best_id="" best_name=""
    local has_copyleft=false

    IFS=' OR ' read -ra parts <<< "$license_str"
    for part in "${parts[@]}"; do
      part=$(echo "$part" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//;s/^(//;s/)$//')
      [[ -z "$part" ]] && continue
      local result
      result=$(classify_spdx_license "$part")
      local risk
      risk=$(echo "$result" | cut -d'|' -f1)
      local id name
      id=$(echo "$result" | cut -d'|' -f2)
      name=$(echo "$result" | cut -d'|' -f3)

      if [[ "$risk" == "critical" || "$risk" == "high" ]]; then
        has_copyleft=true
      fi

      # Pick the least restrictive option
      local current_level best_level
      current_level=$(risk_to_level "$risk")
      best_level=$(risk_to_level "$best_risk")
      if [[ "$current_level" -lt "$best_level" ]]; then
        best_risk="$risk"
        best_id="$id"
        best_name="$name"
      fi
    done

    if [[ "$has_copyleft" == "true" && "$best_risk" != "critical" && "$best_risk" != "high" ]]; then
      echo "${best_risk}|${best_id}|${best_name} (dual-licensed, copyleft option available)"
    else
      echo "${best_risk}|${best_id}|${best_name}"
    fi
    return 0
  fi

  # Handle AND expressions: use the most restrictive
  if [[ "$license_str" =~ " AND " ]]; then
    local worst_risk="low"
    local worst_id="" worst_name=""

    IFS=' AND ' read -ra parts <<< "$license_str"
    for part in "${parts[@]}"; do
      part=$(echo "$part" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//;s/^(//;s/)$//')
      [[ -z "$part" ]] && continue
      local result
      result=$(classify_spdx_license "$part")
      local risk
      risk=$(echo "$result" | cut -d'|' -f1)
      local id name
      id=$(echo "$result" | cut -d'|' -f2)
      name=$(echo "$result" | cut -d'|' -f3)

      local current_level worst_level
      current_level=$(risk_to_level "$risk")
      worst_level=$(risk_to_level "$worst_risk")
      if [[ "$current_level" -gt "$worst_level" ]]; then
        worst_risk="$risk"
        worst_id="$id"
        worst_name="$name"
      fi
    done

    echo "${worst_risk}|${worst_id}|${worst_name}"
    return 0
  fi

  # Single license: look up SPDX
  classify_spdx_license "$license_str"
}

# --- Calculate compliance score -----------------------------------------------

calculate_compliance_score() {
  local findings_file="$1"
  local score=100

  while IFS=$'\t' read -r pkg_name pkg_version license_str ecosystem source_file; do
    [[ -z "$pkg_name" || "$pkg_name" == "PROJECT" ]] && continue

    local result
    result=$(classify_license "$license_str")
    local risk
    risk=$(echo "$result" | cut -d'|' -f1)

    case "$risk" in
      critical) score=$((score - 15)) ;;
      high)     score=$((score - 10)) ;;
      medium)   score=$((score - 3)) ;;
      unknown)  score=$((score - 8)) ;;
      low)      ;; # No deduction
    esac
  done < "$findings_file"

  # Clamp to 0-100
  [[ "$score" -lt 0 ]] && score=0
  [[ "$score" -gt 100 ]] && score=100

  echo "$score"
}

# --- Try to resolve NOASSERTION via node_modules/vendor LICENSE files ----------

try_resolve_license() {
  local pkg_name="$1"
  local ecosystem="$2"
  local base_dir="$3"

  case "$ecosystem" in
    npm)
      # Check node_modules/<pkg>/LICENSE or node_modules/<pkg>/package.json
      local pkg_dir="$base_dir/node_modules/$pkg_name"
      if [[ -d "$pkg_dir" ]]; then
        # Try package.json first
        if [[ -f "$pkg_dir/package.json" ]]; then
          local lic=""
          if command -v python3 &>/dev/null; then
            lic=$(python3 -c "
import json
try:
    with open('$pkg_dir/package.json') as f:
        pkg = json.load(f)
    l = pkg.get('license', '')
    if isinstance(l, dict): l = l.get('type', '')
    if isinstance(l, list): l = ' OR '.join([x.get('type', str(x)) if isinstance(x, dict) else str(x) for x in l])
    print(l)
except: pass
" 2>/dev/null)
          fi
          if [[ -n "$lic" && "$lic" != "NOASSERTION" ]]; then
            echo "$lic"
            return 0
          fi
        fi
        # Try LICENSE file
        for lf in LICENSE LICENSE.md LICENSE.txt LICENCE LICENCE.md COPYING COPYING.md NOTICE; do
          if [[ -f "$pkg_dir/$lf" ]]; then
            local detected
            detected=$(detect_license_from_text "$pkg_dir/$lf")
            local lic_id
            lic_id=$(echo "$detected" | cut -d'|' -f2)
            if [[ "$lic_id" != "NOASSERTION" ]]; then
              echo "$lic_id"
              return 0
            fi
          fi
        done
      fi
      ;;

    python)
      # Check site-packages for .dist-info/METADATA or LICENSE
      local normalized
      normalized=$(echo "$pkg_name" | tr '[:upper:]' '[:lower:]' | tr '-' '_')
      for site_dir in "$base_dir/.venv/lib"/python*/site-packages "$base_dir/venv/lib"/python*/site-packages; do
        if [[ -d "$site_dir" ]]; then
          for dist_dir in "$site_dir/${normalized}"*.dist-info; do
            if [[ -d "$dist_dir" ]]; then
              # Check METADATA
              if [[ -f "$dist_dir/METADATA" ]]; then
                local lic
                lic=$(grep -i '^License:' "$dist_dir/METADATA" 2>/dev/null | head -1 | sed 's/^License:[[:space:]]*//')
                if [[ -n "$lic" && "$lic" != "UNKNOWN" ]]; then
                  echo "$lic"
                  return 0
                fi
              fi
              # Check LICENSE file
              for lf in LICENSE LICENSE.txt COPYING; do
                if [[ -f "$dist_dir/$lf" ]]; then
                  local detected
                  detected=$(detect_license_from_text "$dist_dir/$lf")
                  local lic_id
                  lic_id=$(echo "$detected" | cut -d'|' -f2)
                  if [[ "$lic_id" != "NOASSERTION" ]]; then
                    echo "$lic_id"
                    return 0
                  fi
                fi
              done
            fi
          done
        fi
      done
      ;;
  esac

  echo ""
  return 1
}

# --- Main scan orchestrator ---------------------------------------------------

do_license_scan() {
  local target="${1:-.}"
  local quiet="${2:-false}"

  # Resolve path
  if [[ ! -e "$target" ]]; then
    echo -e "${RED}[LicenseGuard]${NC} Target not found: ${BOLD}$target${NC}" >&2
    return 1
  fi

  # Determine the scan directory
  local scan_dir="$target"
  if [[ -f "$target" ]]; then
    scan_dir=$(dirname "$target")
  fi

  # Find manifest files
  local manifests_tmp
  manifests_tmp=$(mktemp)

  if [[ -f "$target" ]]; then
    echo "$target" > "$manifests_tmp"
  else
    find_manifest_files "$scan_dir" > "$manifests_tmp"
  fi

  local manifest_count
  manifest_count=$(wc -l < "$manifests_tmp" | tr -d ' ')

  if [[ "$manifest_count" -eq 0 ]]; then
    if [[ "$quiet" != "true" ]]; then
      echo -e "${GREEN}[LicenseGuard]${NC} No dependency manifest files found in ${BOLD}$target${NC}"
      echo -e "  Supported: package.json, go.mod, Cargo.toml, pom.xml, requirements.txt, Gemfile, composer.json, *.csproj"
    fi
    rm -f "$manifests_tmp"
    return 0
  fi

  # Check free tier limit
  local tier="free"
  if is_licensed 2>/dev/null; then
    tier="pro"
  fi

  local effective_count="$manifest_count"
  local truncated=false
  if [[ "$tier" == "free" && "$manifest_count" -gt "$FREE_MANIFEST_LIMIT" ]]; then
    effective_count="$FREE_MANIFEST_LIMIT"
    truncated=true
  fi

  if [[ "$quiet" != "true" ]]; then
    echo -e "${BOLD}--- LicenseGuard License Compliance Scan ---${NC}"
    echo ""
    echo -e "Target:     ${BOLD}$target${NC}"
    echo -e "Manifests:  ${CYAN}$manifest_count${NC} found${truncated:+ (scanning first $FREE_MANIFEST_LIMIT -- free tier limit)}"
    echo -e "Ecosystems: ${CYAN}$(detect_package_managers "$scan_dir" | wc -l | tr -d ' ')${NC} detected"
    echo ""
  fi

  # Extract all dependencies
  local findings_tmp
  findings_tmp=$(mktemp)
  local scanned=0

  while IFS= read -r manifest; do
    [[ -z "$manifest" ]] && continue
    ((scanned++)) || true

    # Enforce free tier limit
    if [[ "$tier" == "free" && "$scanned" -gt "$FREE_MANIFEST_LIMIT" ]]; then
      break
    fi

    local mbase
    mbase=$(basename "$manifest")

    # Route to appropriate extractor
    local ecosystem="${MANIFEST_FILES[$mbase]:-}"

    # Handle .csproj and .sln extensions
    local ext="${manifest##*.}"
    if [[ "$ext" == "csproj" || "$ext" == "sln" ]]; then
      ecosystem="dotnet"
    fi

    case "$ecosystem" in
      npm)    extract_npm_licenses "$manifest" "$findings_tmp" ;;
      python) extract_python_licenses "$manifest" "$findings_tmp" ;;
      ruby)   extract_ruby_licenses "$manifest" "$findings_tmp" ;;
      go)     extract_go_licenses "$manifest" "$findings_tmp" ;;
      java)   extract_java_licenses "$manifest" "$findings_tmp" ;;
      rust)   extract_rust_licenses "$manifest" "$findings_tmp" ;;
      php)    extract_php_licenses "$manifest" "$findings_tmp" ;;
      dotnet) extract_dotnet_licenses "$manifest" "$findings_tmp" ;;
      *)
        if [[ "$quiet" != "true" ]]; then
          echo -e "  ${YELLOW}~${NC} Skipping unrecognized manifest: $manifest"
        fi
        ;;
    esac
  done < "$manifests_tmp"

  # Try to resolve NOASSERTION licenses
  local resolved_tmp
  resolved_tmp=$(mktemp)
  while IFS=$'\t' read -r pkg_name pkg_version license_str ecosystem source_file; do
    [[ -z "$pkg_name" ]] && continue
    if [[ "$license_str" == "NOASSERTION" ]]; then
      local resolved_lic
      resolved_lic=$(try_resolve_license "$pkg_name" "$ecosystem" "$scan_dir" 2>/dev/null) || true
      if [[ -n "$resolved_lic" ]]; then
        license_str="$resolved_lic"
      fi
    fi
    printf '%s\t%s\t%s\t%s\t%s\n' "$pkg_name" "$pkg_version" "$license_str" "$ecosystem" "$source_file" >> "$resolved_tmp"
  done < "$findings_tmp"
  mv "$resolved_tmp" "$findings_tmp"

  # De-duplicate: keep unique pkg_name entries (first occurrence)
  local deduped_tmp
  deduped_tmp=$(mktemp)
  sort -t$'\t' -k1,1 -u "$findings_tmp" > "$deduped_tmp"
  mv "$deduped_tmp" "$findings_tmp"

  # Count dependencies and classify
  local total=0 critical=0 high=0 medium=0 low=0 unknown=0

  while IFS=$'\t' read -r pkg_name pkg_version license_str ecosystem source_file; do
    [[ -z "$pkg_name" || "$pkg_name" == "PROJECT" ]] && continue
    ((total++)) || true

    local result
    result=$(classify_license "$license_str")
    local risk
    risk=$(echo "$result" | cut -d'|' -f1)

    case "$risk" in
      critical) ((critical++)) || true ;;
      high)     ((high++)) || true ;;
      medium)   ((medium++)) || true ;;
      low)      ((low++)) || true ;;
      unknown)  ((unknown++)) || true ;;
    esac
  done < "$findings_tmp"

  # Calculate compliance score
  local score
  score=$(calculate_compliance_score "$findings_tmp")

  # Display results
  if [[ "$quiet" != "true" ]]; then
    # Show findings grouped by risk level
    if [[ "$critical" -gt 0 ]]; then
      echo -e "${RED}${BOLD}CRITICAL -- Copyleft/Viral Licenses:${NC}"
      while IFS=$'\t' read -r pkg_name pkg_version license_str ecosystem source_file; do
        [[ -z "$pkg_name" || "$pkg_name" == "PROJECT" ]] && continue
        local result
        result=$(classify_license "$license_str")
        local risk
        risk=$(echo "$result" | cut -d'|' -f1)
        if [[ "$risk" == "critical" ]]; then
          local lic_id lic_name
          lic_id=$(echo "$result" | cut -d'|' -f2)
          lic_name=$(echo "$result" | cut -d'|' -f3)
          echo -e "  ${RED}!!${NC} ${BOLD}$pkg_name${NC}@${pkg_version} ${DIM}($ecosystem)${NC}"
          echo -e "     License: ${RED}${BOLD}$lic_id${NC} -- $lic_name"
          echo -e "     ${DIM}Source: $source_file${NC}"
        fi
      done < "$findings_tmp"
      echo ""
    fi

    if [[ "$high" -gt 0 ]]; then
      echo -e "${RED}HIGH -- Weak Copyleft Licenses:${NC}"
      while IFS=$'\t' read -r pkg_name pkg_version license_str ecosystem source_file; do
        [[ -z "$pkg_name" || "$pkg_name" == "PROJECT" ]] && continue
        local result
        result=$(classify_license "$license_str")
        local risk
        risk=$(echo "$result" | cut -d'|' -f1)
        if [[ "$risk" == "high" ]]; then
          local lic_id lic_name
          lic_id=$(echo "$result" | cut -d'|' -f2)
          lic_name=$(echo "$result" | cut -d'|' -f3)
          echo -e "  ${RED}!${NC}  ${BOLD}$pkg_name${NC}@${pkg_version} ${DIM}($ecosystem)${NC}"
          echo -e "     License: ${RED}$lic_id${NC} -- $lic_name"
        fi
      done < "$findings_tmp"
      echo ""
    fi

    if [[ "$unknown" -gt 0 ]]; then
      echo -e "${MAGENTA}UNKNOWN -- No License Declared:${NC}"
      local unknown_shown=0
      while IFS=$'\t' read -r pkg_name pkg_version license_str ecosystem source_file; do
        [[ -z "$pkg_name" || "$pkg_name" == "PROJECT" ]] && continue
        local result
        result=$(classify_license "$license_str")
        local risk
        risk=$(echo "$result" | cut -d'|' -f1)
        if [[ "$risk" == "unknown" ]]; then
          ((unknown_shown++)) || true
          if [[ "$unknown_shown" -le 20 ]]; then
            echo -e "  ${MAGENTA}?${NC}  ${BOLD}$pkg_name${NC}@${pkg_version} ${DIM}($ecosystem)${NC}"
          fi
        fi
      done < "$findings_tmp"
      if [[ "$unknown" -gt 20 ]]; then
        echo -e "  ${DIM}... and $((unknown - 20)) more${NC}"
      fi
      echo ""
    fi

    # Summary
    echo -e "${BOLD}--- Summary ---${NC}"
    echo -e "  Dependencies scanned: ${CYAN}$total${NC}"
    echo -e "  Manifests processed:  ${CYAN}$scanned${NC}"
    [[ "$critical" -gt 0 ]] && echo -e "  ${RED}${BOLD}Critical (copyleft):  $critical${NC}"
    [[ "$high" -gt 0 ]]     && echo -e "  ${RED}High (weak copyleft): $high${NC}"
    [[ "$medium" -gt 0 ]]   && echo -e "  ${YELLOW}Medium (notice req):  $medium${NC}"
    [[ "$low" -gt 0 ]]      && echo -e "  ${GREEN}Low (permissive):     $low${NC}"
    [[ "$unknown" -gt 0 ]]  && echo -e "  ${MAGENTA}Unknown (no license): $unknown${NC}"
    echo ""

    # Compliance score
    local score_color="$GREEN"
    if [[ "$score" -lt 50 ]]; then
      score_color="$RED"
    elif [[ "$score" -lt 70 ]]; then
      score_color="$YELLOW"
    fi
    echo -e "  Compliance Score: ${score_color}${BOLD}${score}/100${NC}"

    if [[ "$truncated" == "true" ]]; then
      echo ""
      echo -e "  ${YELLOW}Free tier: scanned $FREE_MANIFEST_LIMIT of $manifest_count manifests.${NC}"
      echo -e "  Upgrade to Pro for unlimited scanning: ${CYAN}https://licenseguard.pages.dev/pricing${NC}"
    fi

    if [[ "$critical" -gt 0 ]]; then
      echo ""
      echo -e "${BOLD}Remediation:${NC}"
      echo "  1. Review copyleft dependencies -- they require open-sourcing your code"
      echo "  2. Find alternative packages with permissive licenses (MIT, Apache-2.0, BSD)"
      echo "  3. If copyleft is acceptable, ensure full license compliance"
      echo -e "  4. Generate a full report: ${CYAN}licenseguard report${NC}"
    fi
  fi

  # Store for other commands
  LICENSEGUARD_LAST_FINDINGS="$findings_tmp"
  LICENSEGUARD_LAST_SCORE="$score"

  rm -f "$manifests_tmp"

  # Exit code based on score
  if [[ "$score" -lt 70 ]]; then
    return 1
  fi
  return 0
}

# --- Pre-commit hook entry point ----------------------------------------------

hook_license_scan() {
  local staged_files
  staged_files=$(git diff --cached --name-only 2>/dev/null) || return 0

  [[ -z "$staged_files" ]] && return 0

  # Filter for manifest files only
  local manifest_files=""
  while IFS= read -r file; do
    [[ -z "$file" || ! -f "$file" ]] && continue
    local bname
    bname=$(basename "$file")
    local ext="${file##*.}"

    # Check if it's a known manifest file
    if [[ -n "${MANIFEST_FILES[$bname]:-}" || "$ext" == "csproj" ]]; then
      manifest_files+="$file"$'\n'
    fi
  done <<< "$staged_files"

  if [[ -z "$manifest_files" ]]; then
    return 0
  fi

  echo -e "${BLUE}[LicenseGuard]${NC} Checking staged dependency manifests..."

  local findings_tmp
  findings_tmp=$(mktemp)
  local total=0 critical=0 high=0

  while IFS= read -r manifest; do
    [[ -z "$manifest" ]] && continue
    local bname ecosystem
    bname=$(basename "$manifest")
    ecosystem="${MANIFEST_FILES[$bname]:-}"
    local ext="${manifest##*.}"
    [[ "$ext" == "csproj" ]] && ecosystem="dotnet"

    local manifest_findings
    manifest_findings=$(mktemp)

    case "$ecosystem" in
      npm)    extract_npm_licenses "$manifest" "$manifest_findings" ;;
      python) extract_python_licenses "$manifest" "$manifest_findings" ;;
      ruby)   extract_ruby_licenses "$manifest" "$manifest_findings" ;;
      go)     extract_go_licenses "$manifest" "$manifest_findings" ;;
      java)   extract_java_licenses "$manifest" "$manifest_findings" ;;
      rust)   extract_rust_licenses "$manifest" "$manifest_findings" ;;
      php)    extract_php_licenses "$manifest" "$manifest_findings" ;;
      dotnet) extract_dotnet_licenses "$manifest" "$manifest_findings" ;;
    esac

    while IFS=$'\t' read -r pkg_name pkg_version license_str pkg_eco source_file; do
      [[ -z "$pkg_name" || "$pkg_name" == "PROJECT" ]] && continue

      local result
      result=$(classify_license "$license_str")
      local risk
      risk=$(echo "$result" | cut -d'|' -f1)
      local lic_id
      lic_id=$(echo "$result" | cut -d'|' -f2)

      ((total++)) || true

      if [[ "$risk" == "critical" ]]; then
        ((critical++)) || true
        echo -e "  ${RED}!!${NC} ${BOLD}$pkg_name${NC}@${pkg_version}: ${RED}${BOLD}$lic_id${NC} (copyleft)"
      elif [[ "$risk" == "high" ]]; then
        ((high++)) || true
        echo -e "  ${RED}!${NC}  ${BOLD}$pkg_name${NC}@${pkg_version}: ${RED}$lic_id${NC} (weak copyleft)"
      fi
    done < "$manifest_findings"
    rm -f "$manifest_findings"
  done <<< "$manifest_files"

  if [[ "$critical" -gt 0 ]]; then
    echo ""
    echo -e "${RED}${BOLD}Commit blocked: $critical copyleft license(s) detected${NC}"
    echo "  Run 'licenseguard scan' for details."
    rm -f "$findings_tmp"
    return 1
  fi

  if [[ "$high" -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}[LicenseGuard]${NC} $high weak copyleft license(s) found. Commit allowed."
  fi

  if [[ "$total" -gt 0 && "$critical" -eq 0 && "$high" -eq 0 ]]; then
    echo -e "${GREEN}[LicenseGuard]${NC} $total dependencies checked -- no copyleft issues."
  fi

  rm -f "$findings_tmp"
  return 0
}

# --- Generate compliance report (PRO) ----------------------------------------

generate_report() {
  local dir="${1:-.}"
  local output="$dir/LICENSEGUARD-REPORT.md"
  local project_name
  project_name=$(basename "$(cd "$dir" && pwd)")

  echo -e "${BLUE}[LicenseGuard]${NC} Generating compliance report for ${BOLD}$dir${NC}"

  # Run scan quietly
  local findings_tmp
  findings_tmp=$(mktemp)
  local manifests_tmp
  manifests_tmp=$(mktemp)

  find_manifest_files "$dir" > "$manifests_tmp"
  local manifest_count
  manifest_count=$(wc -l < "$manifests_tmp" | tr -d ' ')

  local scanned=0
  while IFS= read -r manifest; do
    [[ -z "$manifest" ]] && continue
    ((scanned++)) || true

    local bname ecosystem
    bname=$(basename "$manifest")
    ecosystem="${MANIFEST_FILES[$bname]:-}"
    local ext="${manifest##*.}"
    [[ "$ext" == "csproj" || "$ext" == "sln" ]] && ecosystem="dotnet"

    case "$ecosystem" in
      npm)    extract_npm_licenses "$manifest" "$findings_tmp" ;;
      python) extract_python_licenses "$manifest" "$findings_tmp" ;;
      ruby)   extract_ruby_licenses "$manifest" "$findings_tmp" ;;
      go)     extract_go_licenses "$manifest" "$findings_tmp" ;;
      java)   extract_java_licenses "$manifest" "$findings_tmp" ;;
      rust)   extract_rust_licenses "$manifest" "$findings_tmp" ;;
      php)    extract_php_licenses "$manifest" "$findings_tmp" ;;
      dotnet) extract_dotnet_licenses "$manifest" "$findings_tmp" ;;
    esac
  done < "$manifests_tmp"

  # De-duplicate
  local deduped_tmp
  deduped_tmp=$(mktemp)
  sort -t$'\t' -k1,1 -u "$findings_tmp" > "$deduped_tmp"
  mv "$deduped_tmp" "$findings_tmp"

  # Count by risk
  local total=0 critical=0 high=0 medium=0 low=0 unknown=0
  while IFS=$'\t' read -r pkg_name pkg_version license_str ecosystem source_file; do
    [[ -z "$pkg_name" || "$pkg_name" == "PROJECT" ]] && continue
    ((total++)) || true
    local result
    result=$(classify_license "$license_str")
    local risk
    risk=$(echo "$result" | cut -d'|' -f1)
    case "$risk" in
      critical) ((critical++)) || true ;;
      high)     ((high++)) || true ;;
      medium)   ((medium++)) || true ;;
      low)      ((low++)) || true ;;
      unknown)  ((unknown++)) || true ;;
    esac
  done < "$findings_tmp"

  local score
  score=$(calculate_compliance_score "$findings_tmp")

  # Write report
  {
    echo "# LicenseGuard Compliance Report: $project_name"
    echo ""
    echo "> Generated by [LicenseGuard](https://licenseguard.pages.dev) on $(date +%Y-%m-%d' '%H:%M:%S)"
    echo ""
    echo "## Scan Summary"
    echo ""
    echo "| Metric | Value |"
    echo "|--------|-------|"
    echo "| Dependencies scanned | $total |"
    echo "| Manifests processed | $scanned |"
    echo "| Compliance Score | **$score/100** |"
    echo "| Critical (copyleft) | $critical |"
    echo "| High (weak copyleft) | $high |"
    echo "| Medium (notice required) | $medium |"
    echo "| Low (permissive) | $low |"
    echo "| Unknown (no license) | $unknown |"
    echo ""
    echo "## Risk Level Legend"
    echo ""
    echo "| Risk | Impact | Action |"
    echo "|------|--------|--------|"
    echo "| **Critical** | Must open-source your code | Replace or accept copyleft terms |"
    echo "| **High** | Must share library modifications | Isolate properly or replace |"
    echo "| **Medium** | Must include license notice | Add attribution in distributions |"
    echo "| **Low** | Minimal restrictions | No action needed |"
    echo "| **Unknown** | Cannot determine | Investigate manually |"
    echo ""

    if [[ "$critical" -gt 0 || "$high" -gt 0 || "$unknown" -gt 0 ]]; then
      echo "## Findings"
      echo ""
      echo "| Package | Version | License | Risk | Ecosystem | Source |"
      echo "|---------|---------|---------|------|-----------|--------|"

      while IFS=$'\t' read -r pkg_name pkg_version license_str ecosystem source_file; do
        [[ -z "$pkg_name" || "$pkg_name" == "PROJECT" ]] && continue
        local result
        result=$(classify_license "$license_str")
        local risk lic_id lic_name
        risk=$(echo "$result" | cut -d'|' -f1)
        lic_id=$(echo "$result" | cut -d'|' -f2)
        lic_name=$(echo "$result" | cut -d'|' -f3)

        if [[ "$risk" == "critical" || "$risk" == "high" || "$risk" == "unknown" ]]; then
          echo "| \`$pkg_name\` | $pkg_version | $lic_id | **$risk** | $ecosystem | \`$source_file\` |"
        fi
      done < "$findings_tmp"
      echo ""
    fi

    echo "## All Dependencies"
    echo ""
    echo "| Package | Version | License | Risk | Ecosystem |"
    echo "|---------|---------|---------|------|-----------|"

    while IFS=$'\t' read -r pkg_name pkg_version license_str ecosystem source_file; do
      [[ -z "$pkg_name" || "$pkg_name" == "PROJECT" ]] && continue
      local result
      result=$(classify_license "$license_str")
      local risk lic_id
      risk=$(echo "$result" | cut -d'|' -f1)
      lic_id=$(echo "$result" | cut -d'|' -f2)
      echo "| \`$pkg_name\` | $pkg_version | $lic_id | $risk | $ecosystem |"
    done < "$findings_tmp"

    echo ""
    echo "## Remediation Steps"
    echo ""
    echo "1. **Review** all Critical and High risk dependencies"
    echo "2. **Replace** copyleft dependencies with permissive alternatives where possible"
    echo "3. **Investigate** all Unknown license dependencies"
    echo "4. **Document** accepted license risks in your project's LICENSE-EXCEPTIONS file"
    echo "5. **Install** pre-commit hooks: \`licenseguard hooks install\`"
    echo "6. **Enforce** approved license list: \`licenseguard policy\`"
    echo ""
    echo "---"
    echo ""
    echo "*Report generated by [LicenseGuard](https://licenseguard.pages.dev). Run \`licenseguard scan\` for interactive results.*"
  } > "$output"

  rm -f "$findings_tmp" "$manifests_tmp"

  echo -e "${GREEN}[LicenseGuard]${NC} Report written to ${BOLD}$output${NC}"
}

# --- License compatibility matrix (PRO) --------------------------------------

generate_matrix() {
  local dir="${1:-.}"

  echo -e "${BOLD}--- LicenseGuard License Compatibility Matrix ---${NC}"
  echo ""

  # Collect all unique licenses
  local findings_tmp
  findings_tmp=$(mktemp)
  local manifests_tmp
  manifests_tmp=$(mktemp)

  find_manifest_files "$dir" > "$manifests_tmp"

  while IFS= read -r manifest; do
    [[ -z "$manifest" ]] && continue
    local bname ecosystem
    bname=$(basename "$manifest")
    ecosystem="${MANIFEST_FILES[$bname]:-}"
    local ext="${manifest##*.}"
    [[ "$ext" == "csproj" || "$ext" == "sln" ]] && ecosystem="dotnet"

    case "$ecosystem" in
      npm)    extract_npm_licenses "$manifest" "$findings_tmp" ;;
      python) extract_python_licenses "$manifest" "$findings_tmp" ;;
      ruby)   extract_ruby_licenses "$manifest" "$findings_tmp" ;;
      go)     extract_go_licenses "$manifest" "$findings_tmp" ;;
      java)   extract_java_licenses "$manifest" "$findings_tmp" ;;
      rust)   extract_rust_licenses "$manifest" "$findings_tmp" ;;
      php)    extract_php_licenses "$manifest" "$findings_tmp" ;;
      dotnet) extract_dotnet_licenses "$manifest" "$findings_tmp" ;;
    esac
  done < "$manifests_tmp"

  # Get unique licenses
  local licenses=()
  while IFS=$'\t' read -r pkg_name pkg_version license_str ecosystem source_file; do
    [[ -z "$pkg_name" || "$pkg_name" == "PROJECT" ]] && continue
    local result
    result=$(classify_license "$license_str")
    local lic_id
    lic_id=$(echo "$result" | cut -d'|' -f2)
    if [[ "$lic_id" != "NOASSERTION" ]]; then
      licenses+=("$lic_id")
    fi
  done < "$findings_tmp"

  # De-duplicate licenses
  local unique_licenses
  unique_licenses=$(printf '%s\n' "${licenses[@]}" 2>/dev/null | sort -u)
  local license_count
  license_count=$(echo "$unique_licenses" | grep -c . 2>/dev/null || echo 0)

  echo -e "Found ${CYAN}$license_count${NC} unique licenses in your dependency tree."
  echo ""

  # Display compatibility information
  echo -e "${BOLD}License Compatibility Notes:${NC}"
  echo ""

  # Check for incompatible combinations
  local has_gpl=false has_agpl=false has_mit=false has_apache=false has_mpl=false has_lgpl=false
  while IFS= read -r lic; do
    [[ -z "$lic" ]] && continue
    case "$lic" in
      GPL-2.0*|GPL-3.0*) has_gpl=true ;;
      AGPL-3.0*) has_agpl=true ;;
      MIT) has_mit=true ;;
      Apache-2.0) has_apache=true ;;
      MPL-2.0) has_mpl=true ;;
      LGPL-*) has_lgpl=true ;;
    esac
  done <<< "$unique_licenses"

  if [[ "$has_gpl" == "true" && "$has_apache" == "true" ]]; then
    echo -e "  ${RED}!!${NC} ${BOLD}GPL + Apache-2.0:${NC} GPL-2.0 is incompatible with Apache-2.0."
    echo -e "     GPL-3.0 is compatible with Apache-2.0 only in one direction."
    echo ""
  fi

  if [[ "$has_agpl" == "true" ]]; then
    echo -e "  ${RED}!!${NC} ${BOLD}AGPL-3.0 detected:${NC} Any network-accessible service using AGPL code"
    echo -e "     must provide source code to all users, even over a network."
    echo ""
  fi

  if [[ "$has_gpl" == "true" ]]; then
    echo -e "  ${RED}!${NC}  ${BOLD}GPL detected:${NC} If distributing, your entire application must"
    echo -e "     be licensed under GPL-compatible terms."
    echo ""
  fi

  if [[ "$has_lgpl" == "true" ]]; then
    echo -e "  ${YELLOW}~${NC}  ${BOLD}LGPL detected:${NC} You can link to LGPL libraries without copyleft"
    echo -e "     affecting your code, but modifications to the LGPL library must be shared."
    echo ""
  fi

  if [[ "$has_mpl" == "true" ]]; then
    echo -e "  ${YELLOW}~${NC}  ${BOLD}MPL-2.0 detected:${NC} File-level copyleft. Modified MPL files must be shared,"
    echo -e "     but your own files remain under your license."
    echo ""
  fi

  # Print matrix
  echo -e "${BOLD}Compatibility Matrix (can these licenses coexist in one project?):${NC}"
  echo ""
  echo -e "  ${GREEN}Y${NC} = Compatible   ${RED}N${NC} = Incompatible   ${YELLOW}?${NC} = Depends on usage"
  echo ""

  # Simple matrix for common licenses
  printf "  %-14s" ""
  for lic in MIT Apache-2.0 BSD-3 GPL-2.0 GPL-3.0 LGPL-3.0 MPL-2.0 AGPL-3.0; do
    printf "%-10s" "$lic"
  done
  echo ""

  local matrix_licenses=("MIT" "Apache-2.0" "BSD-3" "GPL-2.0" "GPL-3.0" "LGPL-3.0" "MPL-2.0" "AGPL-3.0")
  # Simplified compatibility: Y/N/? grid
  local -A compat=(
    ["MIT,MIT"]="Y" ["MIT,Apache-2.0"]="Y" ["MIT,BSD-3"]="Y" ["MIT,GPL-2.0"]="Y" ["MIT,GPL-3.0"]="Y" ["MIT,LGPL-3.0"]="Y" ["MIT,MPL-2.0"]="Y" ["MIT,AGPL-3.0"]="Y"
    ["Apache-2.0,MIT"]="Y" ["Apache-2.0,Apache-2.0"]="Y" ["Apache-2.0,BSD-3"]="Y" ["Apache-2.0,GPL-2.0"]="N" ["Apache-2.0,GPL-3.0"]="Y" ["Apache-2.0,LGPL-3.0"]="Y" ["Apache-2.0,MPL-2.0"]="Y" ["Apache-2.0,AGPL-3.0"]="Y"
    ["BSD-3,MIT"]="Y" ["BSD-3,Apache-2.0"]="Y" ["BSD-3,BSD-3"]="Y" ["BSD-3,GPL-2.0"]="Y" ["BSD-3,GPL-3.0"]="Y" ["BSD-3,LGPL-3.0"]="Y" ["BSD-3,MPL-2.0"]="Y" ["BSD-3,AGPL-3.0"]="Y"
    ["GPL-2.0,MIT"]="Y" ["GPL-2.0,Apache-2.0"]="N" ["GPL-2.0,BSD-3"]="Y" ["GPL-2.0,GPL-2.0"]="Y" ["GPL-2.0,GPL-3.0"]="N" ["GPL-2.0,LGPL-3.0"]="N" ["GPL-2.0,MPL-2.0"]="?" ["GPL-2.0,AGPL-3.0"]="N"
    ["GPL-3.0,MIT"]="Y" ["GPL-3.0,Apache-2.0"]="Y" ["GPL-3.0,BSD-3"]="Y" ["GPL-3.0,GPL-2.0"]="N" ["GPL-3.0,GPL-3.0"]="Y" ["GPL-3.0,LGPL-3.0"]="Y" ["GPL-3.0,MPL-2.0"]="Y" ["GPL-3.0,AGPL-3.0"]="Y"
    ["LGPL-3.0,MIT"]="Y" ["LGPL-3.0,Apache-2.0"]="Y" ["LGPL-3.0,BSD-3"]="Y" ["LGPL-3.0,GPL-2.0"]="N" ["LGPL-3.0,GPL-3.0"]="Y" ["LGPL-3.0,LGPL-3.0"]="Y" ["LGPL-3.0,MPL-2.0"]="Y" ["LGPL-3.0,AGPL-3.0"]="Y"
    ["MPL-2.0,MIT"]="Y" ["MPL-2.0,Apache-2.0"]="Y" ["MPL-2.0,BSD-3"]="Y" ["MPL-2.0,GPL-2.0"]="?" ["MPL-2.0,GPL-3.0"]="Y" ["MPL-2.0,LGPL-3.0"]="Y" ["MPL-2.0,MPL-2.0"]="Y" ["MPL-2.0,AGPL-3.0"]="Y"
    ["AGPL-3.0,MIT"]="Y" ["AGPL-3.0,Apache-2.0"]="Y" ["AGPL-3.0,BSD-3"]="Y" ["AGPL-3.0,GPL-2.0"]="N" ["AGPL-3.0,GPL-3.0"]="Y" ["AGPL-3.0,LGPL-3.0"]="Y" ["AGPL-3.0,MPL-2.0"]="Y" ["AGPL-3.0,AGPL-3.0"]="Y"
  )

  for row in "${matrix_licenses[@]}"; do
    printf "  ${BOLD}%-14s${NC}" "$row"
    for col in "${matrix_licenses[@]}"; do
      local val="${compat[$row,$col]:-?}"
      case "$val" in
        Y) printf "${GREEN}%-10s${NC}" "Y" ;;
        N) printf "${RED}%-10s${NC}" "N" ;;
        ?) printf "${YELLOW}%-10s${NC}" "?" ;;
      esac
    done
    echo ""
  done

  rm -f "$findings_tmp" "$manifests_tmp"
}

# --- Policy enforcement (TEAM) -----------------------------------------------

enforce_policy() {
  local dir="${1:-.}"

  echo -e "${BOLD}--- LicenseGuard Policy Enforcement ---${NC}"
  echo ""

  # Load approved licenses from config
  local approved_licenses=()
  if [[ -f "$OPENCLAW_CONFIG" ]]; then
    if command -v python3 &>/dev/null; then
      local raw
      raw=$(python3 -c "
import json
try:
    with open('$OPENCLAW_CONFIG') as f:
        cfg = json.load(f)
    approved = cfg.get('skills', {}).get('entries', {}).get('licenseguard', {}).get('config', {}).get('approvedLicenses', [])
    for lic in approved:
        print(lic)
except: pass
" 2>/dev/null) || true

      while IFS= read -r line; do
        [[ -n "$line" ]] && approved_licenses+=("$line")
      done <<< "$raw"
    fi
  fi

  if [[ ${#approved_licenses[@]} -eq 0 ]]; then
    echo -e "${YELLOW}No approved license list configured.${NC}"
    echo ""
    echo "Add approved licenses in ~/.openclaw/openclaw.json:"
    echo -e "  ${CYAN}\"licenseguard\": { \"config\": { \"approvedLicenses\": [\"MIT\", \"Apache-2.0\", \"BSD-3-Clause\"] } }${NC}"
    echo ""
    echo "Using default permissive set: MIT, Apache-2.0, BSD-2-Clause, BSD-3-Clause, ISC, Unlicense, CC0-1.0, 0BSD"
    approved_licenses=("MIT" "Apache-2.0" "BSD-2-Clause" "BSD-3-Clause" "ISC" "Unlicense" "CC0-1.0" "0BSD" "BSL-1.0" "PSF-2.0")
  fi

  echo -e "Approved licenses: ${CYAN}${approved_licenses[*]}${NC}"
  echo ""

  # Run scan
  local findings_tmp
  findings_tmp=$(mktemp)
  local manifests_tmp
  manifests_tmp=$(mktemp)

  find_manifest_files "$dir" > "$manifests_tmp"

  while IFS= read -r manifest; do
    [[ -z "$manifest" ]] && continue
    local bname ecosystem
    bname=$(basename "$manifest")
    ecosystem="${MANIFEST_FILES[$bname]:-}"
    local ext="${manifest##*.}"
    [[ "$ext" == "csproj" || "$ext" == "sln" ]] && ecosystem="dotnet"

    case "$ecosystem" in
      npm)    extract_npm_licenses "$manifest" "$findings_tmp" ;;
      python) extract_python_licenses "$manifest" "$findings_tmp" ;;
      ruby)   extract_ruby_licenses "$manifest" "$findings_tmp" ;;
      go)     extract_go_licenses "$manifest" "$findings_tmp" ;;
      java)   extract_java_licenses "$manifest" "$findings_tmp" ;;
      rust)   extract_rust_licenses "$manifest" "$findings_tmp" ;;
      php)    extract_php_licenses "$manifest" "$findings_tmp" ;;
      dotnet) extract_dotnet_licenses "$manifest" "$findings_tmp" ;;
    esac
  done < "$manifests_tmp"

  # De-duplicate
  local deduped_tmp
  deduped_tmp=$(mktemp)
  sort -t$'\t' -k1,1 -u "$findings_tmp" > "$deduped_tmp"
  mv "$deduped_tmp" "$findings_tmp"

  # Check each dependency against approved list
  local total=0 violations=0
  local violations_tmp
  violations_tmp=$(mktemp)

  while IFS=$'\t' read -r pkg_name pkg_version license_str ecosystem source_file; do
    [[ -z "$pkg_name" || "$pkg_name" == "PROJECT" ]] && continue
    ((total++)) || true

    local result
    result=$(classify_license "$license_str")
    local lic_id
    lic_id=$(echo "$result" | cut -d'|' -f2)

    # Check if license is in approved list
    local approved=false
    for approved_lic in "${approved_licenses[@]}"; do
      if [[ "$lic_id" == "$approved_lic" ]]; then
        approved=true
        break
      fi
    done

    if [[ "$approved" == "false" ]]; then
      ((violations++)) || true
      echo -e "  ${RED}!!${NC} ${BOLD}$pkg_name${NC}@${pkg_version}: ${RED}$lic_id${NC} (not on approved list)"
      echo -e "${pkg_name}\t${pkg_version}\t${lic_id}\t${ecosystem}" >> "$violations_tmp"
    fi
  done < "$findings_tmp"

  echo ""
  echo -e "${BOLD}--- Policy Results ---${NC}"
  echo -e "  Dependencies checked: ${CYAN}$total${NC}"
  echo -e "  Policy violations:    ${violations:+${RED}${BOLD}}${violations}${NC}"

  if [[ "$violations" -eq 0 ]]; then
    echo ""
    echo -e "${GREEN}${BOLD}PASS:${NC} All dependencies use approved licenses."
  else
    echo ""
    echo -e "${RED}${BOLD}FAIL:${NC} $violations dependencies use unapproved licenses."
    echo ""
    echo "Options:"
    echo "  1. Replace the dependency with one using an approved license"
    echo "  2. Add the license to the approved list (after legal review)"
    echo "  3. Request an exception for the specific package"
  fi

  rm -f "$findings_tmp" "$manifests_tmp" "$violations_tmp"

  if [[ "$violations" -gt 0 ]]; then
    return 1
  fi
  return 0
}

# --- SBOM generation (TEAM) --------------------------------------------------

generate_sbom() {
  local dir="${1:-.}"
  local output_json="$dir/LICENSEGUARD-SBOM.json"
  local output_md="$dir/LICENSEGUARD-SBOM.md"
  local project_name
  project_name=$(basename "$(cd "$dir" && pwd)")

  echo -e "${BLUE}[LicenseGuard]${NC} Generating SBOM for ${BOLD}$dir${NC}"

  # Collect all dependencies
  local findings_tmp
  findings_tmp=$(mktemp)
  local manifests_tmp
  manifests_tmp=$(mktemp)

  find_manifest_files "$dir" > "$manifests_tmp"

  while IFS= read -r manifest; do
    [[ -z "$manifest" ]] && continue
    local bname ecosystem
    bname=$(basename "$manifest")
    ecosystem="${MANIFEST_FILES[$bname]:-}"
    local ext="${manifest##*.}"
    [[ "$ext" == "csproj" || "$ext" == "sln" ]] && ecosystem="dotnet"

    case "$ecosystem" in
      npm)    extract_npm_licenses "$manifest" "$findings_tmp" ;;
      python) extract_python_licenses "$manifest" "$findings_tmp" ;;
      ruby)   extract_ruby_licenses "$manifest" "$findings_tmp" ;;
      go)     extract_go_licenses "$manifest" "$findings_tmp" ;;
      java)   extract_java_licenses "$manifest" "$findings_tmp" ;;
      rust)   extract_rust_licenses "$manifest" "$findings_tmp" ;;
      php)    extract_php_licenses "$manifest" "$findings_tmp" ;;
      dotnet) extract_dotnet_licenses "$manifest" "$findings_tmp" ;;
    esac
  done < "$manifests_tmp"

  # De-duplicate
  local deduped_tmp
  deduped_tmp=$(mktemp)
  sort -t$'\t' -k1,1 -u "$findings_tmp" > "$deduped_tmp"
  mv "$deduped_tmp" "$findings_tmp"

  local total=0
  local timestamp
  timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date +%Y-%m-%dT%H:%M:%SZ)

  # Generate JSON SBOM (CycloneDX-like format)
  if command -v python3 &>/dev/null; then
    python3 -c "
import json, sys

components = []
with open('$findings_tmp') as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) < 5 or parts[0] == 'PROJECT':
            continue
        name, version, license_str, ecosystem, source = parts[0], parts[1], parts[2], parts[3], parts[4]
        purl = ''
        if ecosystem == 'npm':
            purl = f'pkg:npm/{name}@{version}'
        elif ecosystem == 'python':
            purl = f'pkg:pypi/{name}@{version}'
        elif ecosystem == 'ruby':
            purl = f'pkg:gem/{name}@{version}'
        elif ecosystem == 'go':
            purl = f'pkg:golang/{name}@{version}'
        elif ecosystem == 'java':
            purl = f'pkg:maven/{name}@{version}'
        elif ecosystem == 'rust':
            purl = f'pkg:cargo/{name}@{version}'
        elif ecosystem == 'php':
            purl = f'pkg:composer/{name}@{version}'
        elif ecosystem == 'dotnet':
            purl = f'pkg:nuget/{name}@{version}'

        comp = {
            'type': 'library',
            'name': name,
            'version': version,
            'purl': purl,
            'licenses': [{'license': {'id': license_str}}] if license_str != 'NOASSERTION' else [],
            'ecosystem': ecosystem
        }
        components.append(comp)

sbom = {
    'bomFormat': 'CycloneDX',
    'specVersion': '1.5',
    'serialNumber': 'urn:uuid:licenseguard-$project_name',
    'version': 1,
    'metadata': {
        'timestamp': '$timestamp',
        'tools': [{'vendor': 'ClawHub', 'name': 'LicenseGuard', 'version': '1.0.0'}],
        'component': {'type': 'application', 'name': '$project_name'}
    },
    'components': components
}

with open('$output_json', 'w') as f:
    json.dump(sbom, f, indent=2)

print(len(components))
" 2>/dev/null
    total=$?
  else
    # Fallback: generate simple JSON manually
    {
      echo "{"
      echo "  \"bomFormat\": \"CycloneDX\","
      echo "  \"specVersion\": \"1.5\","
      echo "  \"metadata\": {"
      echo "    \"timestamp\": \"$timestamp\","
      echo "    \"tools\": [{\"vendor\": \"ClawHub\", \"name\": \"LicenseGuard\", \"version\": \"1.0.0\"}],"
      echo "    \"component\": {\"type\": \"application\", \"name\": \"$project_name\"}"
      echo "  },"
      echo "  \"components\": []"
      echo "}"
    } > "$output_json"
  fi

  # Generate Markdown SBOM
  {
    echo "# Software Bill of Materials: $project_name"
    echo ""
    echo "> Generated by [LicenseGuard](https://licenseguard.pages.dev) on $(date +%Y-%m-%d' '%H:%M:%S)"
    echo ""
    echo "## Components"
    echo ""
    echo "| Package | Version | License | Risk | Ecosystem | PURL |"
    echo "|---------|---------|---------|------|-----------|------|"

    total=0
    while IFS=$'\t' read -r pkg_name pkg_version license_str ecosystem source_file; do
      [[ -z "$pkg_name" || "$pkg_name" == "PROJECT" ]] && continue
      ((total++)) || true

      local result
      result=$(classify_license "$license_str")
      local risk lic_id
      risk=$(echo "$result" | cut -d'|' -f1)
      lic_id=$(echo "$result" | cut -d'|' -f2)

      local purl=""
      case "$ecosystem" in
        npm)    purl="pkg:npm/$pkg_name@$pkg_version" ;;
        python) purl="pkg:pypi/$pkg_name@$pkg_version" ;;
        ruby)   purl="pkg:gem/$pkg_name@$pkg_version" ;;
        go)     purl="pkg:golang/$pkg_name@$pkg_version" ;;
        java)   purl="pkg:maven/$pkg_name@$pkg_version" ;;
        rust)   purl="pkg:cargo/$pkg_name@$pkg_version" ;;
        php)    purl="pkg:composer/$pkg_name@$pkg_version" ;;
        dotnet) purl="pkg:nuget/$pkg_name@$pkg_version" ;;
      esac

      echo "| \`$pkg_name\` | $pkg_version | $lic_id | $risk | $ecosystem | \`$purl\` |"
    done < "$findings_tmp"

    echo ""
    echo "## Statistics"
    echo ""
    echo "- **Total components:** $total"
    echo "- **Format:** CycloneDX 1.5"
    echo "- **Generated:** $(date +%Y-%m-%d' '%H:%M:%S)"
    echo ""
    echo "---"
    echo ""
    echo "*SBOM generated by [LicenseGuard](https://licenseguard.pages.dev).*"
  } > "$output_md"

  rm -f "$findings_tmp" "$manifests_tmp"

  echo -e "${GREEN}[LicenseGuard]${NC} SBOM written to:"
  echo -e "  JSON: ${BOLD}$output_json${NC}"
  echo -e "  Markdown: ${BOLD}$output_md${NC}"
  echo -e "  Components: ${CYAN}$total${NC}"
}

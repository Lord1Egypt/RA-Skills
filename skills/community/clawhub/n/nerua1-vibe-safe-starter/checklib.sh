#!/usr/bin/env bash
# VibeSafe Starter — Check a Library Before Installing
# Usage: ./checklib.sh <package-name> [npm|pip]

set -euo pipefail
PKG="${1:-}"
TYPE="${2:-npm}"

if [ -z "$PKG" ]; then
    echo "Usage: ./checklib.sh <package-name> [npm|pip]"
    echo "Example: ./checklib.sh react"
    exit 1
fi

echo "🔍 Checking $PKG before you install it..."
echo ""

# 1. npm registry check
if [ "$TYPE" = "npm" ]; then
    echo "📦 npm: $PKG"
    
    # Get package info
    info=$(curl -s "https://registry.npmjs.org/$PKG/latest" 2>/dev/null)
    
    if echo "$info" | grep -q "error\|not found"; then
        echo "   ❌ Package not found on npm"
        exit 1
    fi
    
    # Extract key metrics
    version=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('version','unknown'))" 2>/dev/null)
    description=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('description','')[:80])" 2>/dev/null)
    license=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('license','unknown'))" 2>/dev/null)
    
    echo "   Version: $version"
    echo "   License: $license"
    echo "   Description: $description"
    
    # npm download stats (last week)
    dl=$(curl -s "https://api.npmjs.org/downloads/point/last-week/$PKG" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('downloads','?'))" 2>/dev/null)
    echo "   Downloads/week: $dl"
    
    # Check for known vulnerabilities via OSV
    echo ""
    echo "🛡️  OSV.dev check..."
    cves=$(curl -s "https://api.osv.dev/v1/query" -d "{\"package\":{\"name\":\"$PKG\",\"ecosystem\":\"npm\"}}" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('vulns',[])))" 2>/dev/null)
    
    if [ "$cves" -gt 0 ]; then
        echo "   🔴 $cves known vulnerabilities!"
        curl -s "https://api.osv.dev/v1/query" -d "{\"package\":{\"name\":\"$PKG\",\"ecosystem\":\"npm\"}}" 2>/dev/null | python3 -c "
import json,sys
d=json.load(sys.stdin)
for v in d.get('vulns',[]):
    print(f'     - {v[\"id\"]}: {v.get(\"summary\",\"?\")[:80]}')
" 2>/dev/null
    else
        echo "   ✅ No known vulnerabilities"
    fi
    
    # Maintenance check (GitHub)
    repo_url=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); repo=d.get('repository',{}); print(repo.get('url','').replace('git+','').replace('.git',''))" 2>/dev/null)
    if [ -n "$repo_url" ] && [ "$repo_url" != "None" ]; then
        echo ""
        echo "📊 GitHub activity..."
        repo_path=$(echo "$repo_url" | sed 's|https://github.com/||')
        gh_data=$(curl -s "https://api.github.com/repos/$repo_path" 2>/dev/null)
        stars=$(echo "$gh_data" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('stargazers_count','?'))" 2>/dev/null)
        updated=$(echo "$gh_data" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('pushed_at','?')[:10])" 2>/dev/null)
        echo "   Stars: $stars"
        echo "   Last push: $updated"
        
        # Warning if not updated in 6+ months
        if [ "$updated" != "?" ]; then
            months_ago=$(( ($(date +%s) - $(date -jf "%Y-%m-%d" "$updated" +%s 2>/dev/null || echo 0)) / 2592000 ))
            if [ "$months_ago" -gt 6 ]; then
                echo "   ⚠️  Not updated in $months_ago months — may be unmaintained!"
            fi
        fi
    fi

elif [ "$TYPE" = "pip" ]; then
    echo "🐍 pip: $PKG"
    info=$(curl -s "https://pypi.org/pypi/$PKG/json" 2>/dev/null)
    
    if echo "$info" | grep -q "Not Found"; then
        echo "   ❌ Package not found on PyPI"
        exit 1
    fi
    
    version=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['info']['version'])" 2>/dev/null)
    summary=$(echo "$info" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['info'].get('summary','')[:80])" 2>/dev/null)
    
    echo "   Version: $version"
    echo "   Summary: $summary"
    
    # CVE check
    cves=$(curl -s "https://api.osv.dev/v1/query" -d "{\"package\":{\"name\":\"$PKG\",\"ecosystem\":\"PyPI\"}}" 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('vulns',[])))" 2>/dev/null)
    if [ "$cves" -gt 0 ]; then
        echo "   🔴 $cves known vulnerabilities!"
    else
        echo "   ✅ No known vulnerabilities"
    fi
fi

echo ""
echo "========================"
echo "✅ Done. Review the output above before installing $PKG."

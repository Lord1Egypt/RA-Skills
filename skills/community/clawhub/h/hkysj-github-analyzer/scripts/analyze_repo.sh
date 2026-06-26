#!/bin/bash
# GitHub 项目分析脚本
# 作者: hkysj
# 用法: ./analyze_repo.sh owner/repo [output_dir]
# 示例: ./analyze_repo.sh msitarzewski/agency-agents
#       ./analyze_repo.sh msitarzewski/agency-agents ~/Desktop/github-reports

set -e

# 默认输出目录
OUTPUT_DIR="${2:-$HOME/Desktop/github-reports}"
mkdir -p "$OUTPUT_DIR"

# 检查参数
if [ -z "$1" ]; then
    echo "用法: $0 <owner/repo> [output_dir]" >&2
    echo "示例: $0 msitarzewski/agency-agents" >&2
    echo "      $0 msitarzewski/agency-agents ~/Desktop/github-reports" >&2
    exit 1
fi

REPO="$1"
REPORT_FILE="$OUTPUT_DIR/${REPO//\//-}-$(date +%Y%m%d-%H%M).md"

echo "=== 分析 GitHub 项目: $REPO ==="
echo ""

# 1. 获取基本信息
echo "📦 获取项目基本信息..."
REPO_INFO=$(curl -s "https://api.github.com/repos/$REPO" 2>/dev/null)

if [ -z "$REPO_INFO" ] || echo "$REPO_INFO" | grep -q '"message": "Not Found"'; then
    echo "❌ 无法获取项目信息，请检查仓库名是否正确"
    exit 1
fi

NAME=$(echo "$REPO_INFO" | jq -r '.name')
FULL_NAME=$(echo "$REPO_INFO" | jq -r '.full_name')
DESCRIPTION=$(echo "$REPO_INFO" | jq -r '.description // "无描述"')
STARS=$(echo "$REPO_INFO" | jq -r '.stargazers_count')
FORKS=$(echo "$REPO_INFO" | jq -r '.forks_count')
LANGUAGE=$(echo "$REPO_INFO" | jq -r '.language // "Unknown"')
LICENSE=$(echo "$REPO_INFO" | jq -r '.license.spdx_id // "NOASSERTION"')
CREATED=$(echo "$REPO_INFO" | jq -r '.created_at')
PUSHED=$(echo "$REPO_INFO" | jq -r '.pushed_at')
ISSUES=$(echo "$REPO_INFO" | jq -r '.open_issues_count')
HTML_URL=$(echo "$REPO_INFO" | jq -r '.html_url')

# 2. 获取 README
echo "📖 获取 README..."
README_URL="https://raw.githubusercontent.com/${REPO}/main/README.md"
README_CONTENT=$(curl -sL "$README_URL" 2>/dev/null)
if [ -z "$README_CONTENT" ]; then
    README_URL="https://raw.githubusercontent.com/${REPO}/master/README.md"
    README_CONTENT=$(curl -sL "$README_URL" 2>/dev/null)
fi
README_FIRST_LINES=$(echo "$README_CONTENT" | head -50)

# 3. 检测技术栈特征文件
echo "🔧 检测技术栈..."
TREE_DATA=$(curl -s "https://api.github.com/repos/$REPO/contents" 2>/dev/null | jq -r '.[].name' 2>/dev/null || echo "")

HAS_PACKAGE_JSON="false"
HAS_REQUIREMENTS="false"
HAS_PYPROJECT="false"
HAS_GO_MOD="false"
HAS_CARGO="false"
HAS_DOCKER="false"
HAS_DOCKER_COMPOSE="false"
HAS_MAKEFILE="false"

while IFS= read -r file; do
    case "$file" in
        "package.json") HAS_PACKAGE_JSON="true" ;;
        "requirements.txt") HAS_REQUIREMENTS="true" ;;
        "pyproject.toml") HAS_PYPROJECT="true" ;;
        "go.mod") HAS_GO_MOD="true" ;;
        "Cargo.toml") HAS_CARGO="true" ;;
        "Dockerfile") HAS_DOCKER="true" ;;
        docker-compose*) HAS_DOCKER_COMPOSE="true" ;;
        "Makefile") HAS_MAKEFILE="true" ;;
    esac
done <<< "$TREE_DATA"

# 许可证分析函数
get_license_info() {
    local lic="$1"
    case "$lic" in
        "MIT")
            echo "MIT|是|是|否|低"
            ;;
        "Apache-2.0")
            echo "Apache License 2.0|是|是|否 (需保留版权声明)|低"
            ;;
        "BSD-3-Clause"|"BSD-2-Clause")
            echo "BSD License|是|是|否|低"
            ;;
        "GPL-3.0")
            echo "GNU General Public License v3.0|需要开源你的代码|是 (必须使用相同许可证)|是 (传染性许可证)|高 (商业项目需谨慎)"
            ;;
        "AGPL-3.0")
            echo "GNU Affero General Public License v3.0|需要开源你的代码|是 (必须使用相同许可证)|是 (更强的传染性)|高 (商业项目需谨慎)"
            ;;
        "LGPL-3.0")
            echo "GNU Lesser General Public License v3.0|是 (作为库使用)|是|仅修改库本身时|中等"
            ;;
        "CC0-1.0")
            echo "Creative Commons Zero v1.0|是|是|否|无"
            ;;
        "MPL-2.0")
            echo "Mozilla Public License 2.0|是|是|基于 MPL 的文件需要|中等"
            ;;
        "ISC")
            echo "ISC License|是|是|否|低"
            ;;
        "Unlicense")
            echo "The Unlicense|是|是|否|无 (公共领域)"
            ;;
        ""|"NOASSERTION"|"null")
            echo "无许可证或未识别|未知，需联系作者|未知，需联系作者|未知|高 (法律风险)"
            ;;
        *)
            echo "$lic (需手动确认)|请查阅许可证条款|请查阅许可证条款|请查阅许可证条款|中等 (需确认)"
            ;;
    esac
}

LICENSE_INFO=$(get_license_info "$LICENSE")
LIC_NAME=$(echo "$LICENSE_INFO" | cut -d'|' -f1)
LIC_COMMERCIAL=$(echo "$LICENSE_INFO" | cut -d'|' -f2)
LIC_DERIVATIVE=$(echo "$LICENSE_INFO" | cut -d'|' -f3)
LIC_OPENSOURCE=$(echo "$LICENSE_INFO" | cut -d'|' -f4)
LIC_RISK=$(echo "$LICENSE_INFO" | cut -d'|' -f5)

# 部署建议
DEPLOY_ADVICE=""
if [ "$HAS_DOCKER" = "true" ] || [ "$HAS_DOCKER_COMPOSE" = "true" ]; then
    DEPLOY_ADVICE="推荐使用 Docker 部署\n\`\`\`bash\ndocker-compose up -d\n\`\`\`"
elif [ "$HAS_PACKAGE_JSON" = "true" ]; then
    DEPLOY_ADVICE="Node.js 项目\n\`\`\`bash\nnpm install\nnpm run dev  # 或 npm start\n\`\`\`"
elif [ "$HAS_REQUIREMENTS" = "true" ] || [ "$HAS_PYPROJECT" = "true" ]; then
    DEPLOY_ADVICE="Python 项目\n\`\`\`bash\npip install -r requirements.txt  # 或 pip install -e .\n\`\`\`"
elif [ "$HAS_GO_MOD" = "true" ]; then
    DEPLOY_ADVICE="Go 项目\n\`\`\`bash\ngo run main.go  # 或 go build\n\`\`\`"
elif [ "$HAS_CARGO" = "true" ]; then
    DEPLOY_ADVICE="Rust 项目\n\`\`\`bash\ncargo run  # 或 cargo build --release\n\`\`\`"
elif [ "$HAS_MAKEFILE" = "true" ]; then
    DEPLOY_ADVICE="C/C++ 项目\n\`\`\`bash\nmake\n\`\`\`"
else
    DEPLOY_ADVICE="请查看 README 获取部署说明"
fi

# 4. 生成 MD 报告
cat > "$REPORT_FILE" << EOF
# GitHub 项目分析报告

> 生成时间: $(date "+%Y-%m-%d %H:%M:%S")
> 分析工具: github-analyzer (by hkysj)

---

## 📊 基本信息

| 属性 | 值 |
|------|-----|
| 📌 项目名称 | **$NAME** |
| 📋 完整路径 | $FULL_NAME |
| ⭐ Stars | **$STARS** |
| 🍴 Forks | $FORKS |
| 🔧 主要语言 | $LANGUAGE |
| 📜 许可证 | $LICENSE |
| 📂 Open Issues | $ISSUES |
| 🔗 创建时间 | ${CREATED%%T*} |
| 🔄 更新时间 | ${PUSHED%%T*} |
| 🌐 项目链接 | [$HTML_URL]($HTML_URL) |

---

## 📝 项目描述

$DESCRIPTION

---

## 📜 许可证分析

| 项目 | 结论 |
|------|------|
| 许可证名称 | $LIC_NAME |
| 💼 可商用 | $LIC_COMMERCIAL |
| 🔄 可二次开发 | $LIC_DERIVATIVE |
| 📋 需要开源 | $LIC_OPENSOURCE |
| 📝 风险等级 | $LIC_RISK |

EOF

# 添加技术栈检测
echo "" >> "$REPORT_FILE"
echo "---" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"
echo "## 🔧 技术栈检测" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

if [ "$HAS_PACKAGE_JSON" = "true" ]; then
    echo "- ✅ **package.json** (Node.js/JavaScript)" >> "$REPORT_FILE"
fi
if [ "$HAS_REQUIREMENTS" = "true" ]; then
    echo "- ✅ **requirements.txt** (Python)" >> "$REPORT_FILE"
fi
if [ "$HAS_PYPROJECT" = "true" ]; then
    echo "- ✅ **pyproject.toml** (Python)" >> "$REPORT_FILE"
fi
if [ "$HAS_GO_MOD" = "true" ]; then
    echo "- ✅ **go.mod** (Go)" >> "$REPORT_FILE"
fi
if [ "$HAS_CARGO" = "true" ]; then
    echo "- ✅ **Cargo.toml** (Rust)" >> "$REPORT_FILE"
fi
if [ "$HAS_DOCKER" = "true" ]; then
    echo "- ✅ **Dockerfile** (Docker)" >> "$REPORT_FILE"
fi
if [ "$HAS_DOCKER_COMPOSE" = "true" ]; then
    echo "- ✅ **docker-compose** (Docker Compose)" >> "$REPORT_FILE"
fi
if [ "$HAS_MAKEFILE" = "true" ]; then
    echo "- ✅ **Makefile**" >> "$REPORT_FILE"
fi

# 添加部署建议
cat >> "$REPORT_FILE" << EOF

---

## 🚀 部署建议

$DEPLOY_ADVICE

---

## 📖 README 摘要 (前 50 行)

\`\`\`markdown
$README_FIRST_LINES
\`\`\`

---

*报告由 github-analyzer 技能自动生成*
EOF

# 5. 终端输出
echo ""
echo "══════════════════════════════════════════════════"
echo "  GitHub 项目分析报告"
echo "══════════════════════════════════════════════════"
echo ""

echo "📌 项目名称: $NAME"
echo "📋 完整路径: $FULL_NAME"
echo "⭐ Stars: $STARS"
echo "🍴 Forks: $FORKS"
echo "🔧 主要语言: $LANGUAGE"
echo "📜 许可证: $LICENSE"
echo "📂 Open Issues: $ISSUES"
echo "🔗 创建时间: ${CREATED%%T*}"
echo "🔄 更新时间: ${PUSHED%%T*}"
echo "🌐 项目链接: $HTML_URL"

echo ""
echo "📝 项目描述:"
echo "  $DESCRIPTION"

echo ""
echo "📜 许可证分析:"
echo "  许可证: $LIC_NAME"
echo "  💼 可商用: $LIC_COMMERCIAL"
echo "  🔄 可二次开发: $LIC_DERIVATIVE"
echo "  📋 需要开源: $LIC_OPENSOURCE"
echo "  📝 风险: $LIC_RISK"

echo ""
echo "🔧 技术栈检测:"
[ "$HAS_PACKAGE_JSON" = "true" ] && echo "  ✅ package.json (Node.js)"
[ "$HAS_REQUIREMENTS" = "true" ] && echo "  ✅ requirements.txt (Python)"
[ "$HAS_PYPROJECT" = "true" ] && echo "  ✅ pyproject.toml (Python)"
[ "$HAS_GO_MOD" = "true" ] && echo "  ✅ go.mod (Go)"
[ "$HAS_CARGO" = "true" ] && echo "  ✅ Cargo.toml (Rust)"
[ "$HAS_DOCKER" = "true" ] && echo "  ✅ Dockerfile"
[ "$HAS_DOCKER_COMPOSE" = "true" ] && echo "  ✅ docker-compose"
[ "$HAS_MAKEFILE" = "true" ] && echo "  ✅ Makefile"

echo ""
echo "🚀 部署建议:"
echo "  $DEPLOY_ADVICE" | head -1

echo ""
echo "══════════════════════════════════════════════════"
echo "📄 报告已保存: $REPORT_FILE"
echo "══════════════════════════════════════════════════"

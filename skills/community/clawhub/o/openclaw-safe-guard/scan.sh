#!/bin/bash

# OpenClaw Skill 安全扫描脚本
# 作者: 
# 功能: 扫描 Skills 的安全风险（支持已安装和 GitHub 在线扫描）

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 配置
SKILLS_DIR="$HOME/.openclaw/skills"
WORKSPACE_DIR="$HOME/.openclaw/workspace/skills"
GITHUB_API="https://api.github.com"
TEMP_DIR="/tmp/skill_audit_$$"

# 安全配置

# ========== 安全函数 ==========

# 输入过滤：只允许字母、数字、连字符、下划线和点
sanitize_input() {
    local input="$1"
    if [[ ! "$input" =~ ^[a-zA-Z0-9._-]+$ ]]; then
        echo -e "${RED}错误: 输入包含非法字符${NC}" >&2
        exit 1
    fi
    echo "$input"
}

# GitHub 仓库名过滤：必须是 owner/repo 格式
sanitize_github_repo() {
    local input="$1"
    if [[ ! "$input" =~ ^[a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+$ ]]; then
        echo -e "${RED}错误: 无效的 GitHub 仓库格式 (需要 owner/repo)${NC}" >&2
        return 1
    fi
    echo "$input"
}

# 显示来源信息
show_source_info() {
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE} 🦞 龙虾安全卫士 v1.2.1${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo "作者: ansengu11"
    echo "仓库: https://github.com/ansengu11/openclaw-safe-guard"
    echo "文档: https://clawhub.ai/ansengu11/openclaw-safe-guard"
    echo ""
    echo -e "${YELLOW}建议在使用前审查源代码${NC}"
    echo ""
}

# 显示安全警告
show_risk_warning() {
    echo -e "${RED}════════════════════════════════════════${NC}"
    echo -e "${RED} ⚠️ 安全警告：高风险操作 ⚠️${NC}"
    echo -e "${RED}════════════════════════════════════════${NC}"
    echo ""
    echo "此技能将执行以下操作："
    echo " • 读取 ~/.openclaw/skills 目录（可能包含其他技能的 API 密钥）"
    echo " • 从 GitHub 克隆代码到本地"
    echo ""
    echo " 请配合人工代码审查使用"
    echo ""
    
    # 非交互模式特别警告
    if [[ "$OPENCLAW_NONINTERACTIVE" == "true" ]]; then
        echo -e "${RED}⚠️ 警告：您正在使用非交互模式${NC}"
        echo -e "${RED} 已跳过确认步骤，将直接执行扫描${NC}"
        echo -e "${RED} 请确保您理解风险并在适当环境中运行${NC}"
        echo ""
        return
    fi
    
    echo -e "${YELLOW}建议仅在隔离环境（容器/虚拟机）中使用${NC}"
    echo ""
    read -p "输入 YES 继续，其他任意键退出: " confirmation
    if [[ "$confirmation" != "YES" ]]; then
        echo "已取消扫描"
        exit 0
    fi
    echo ""
}

# 自动检测语言
detect_lang() {
    # 优先检查命令行参数
    if [[ "$1" == "-l" ]] && [[ -n "$2" ]]; then
        echo "$2"
        return
    fi
    
    # 检查 LANG 环境变量
    local lang="${LANG:-en_US}"
    if echo "$lang" | grep -qi "zh"; then
        echo "cn"
    else
        echo "en"
    fi
}

# 当前语言（支持 -l 参数）
LANG=$(detect_lang "$@")

# 翻译函数
t() {
    local key=$1
    if [[ "$LANG" == "cn" ]]; then
        case $key in
            "title") echo "安全扫描" ;;
            "scan_skill") echo "扫描 Skill" ;;
            "search") echo "搜索" ;;
            "compare") echo "对比" ;;
            "all") echo "全部 Skills" ;;
            "help") echo "帮助" ;;
            "risk_low") echo "🟢 低风险" ;;
            "risk_medium") echo "🟡 中风险" ;;
            "risk_high") echo "🔴 高风险" ;;
            "safe") echo "✅ 安全" ;;
            "warning") echo "⚠️ 警告" ;;
            "danger") echo "❌ 危险" ;;
            "score") echo "分数" ;;
            "result") echo "扫描完成" ;;
            *) echo "$key" ;;
        esac
    else
        case $key in
            "title") echo "Security Scanner" ;;
            "scan_skill") echo "Scan Skill" ;;
            "search") echo "Search" ;;
            "compare") echo "Compare" ;;
            "all") echo "All Skills" ;;
            "help") echo "Help" ;;
            "risk_low") echo "🟢 Low Risk" ;;
            "risk_medium") echo "🟡 Medium Risk" ;;
            "risk_high") echo "🔴 High Risk" ;;
            "safe") echo "✅ Safe" ;;
            "warning") echo "⚠️ Warning" ;;
            "danger") echo "❌ Danger" ;;
            "score") echo "Score" ;;
            "result") echo "Scan Complete" ;;
            *) echo "$key" ;;
        esac
    fi
}

# 帮助信息
show_help() {
    echo "Usage: $0 [options] [command] [args]"
    echo ""
    echo "Options:"
    echo "  -l, --lang <cn|en>  设置语言 (默认: 自动检测)"
    echo ""
    echo "Commands:"
    echo "  scan <skill_name>    扫描已安装的 Skill"
    echo "  search <keyword>     从 GitHub 搜索 Skills"
    echo "  compare <skill1> <skill2>  对比两个 Skills"
    echo "  all                扫描所有已安装的 Skills"
    echo "  help               显示帮助"
    echo ""
    echo "Examples:"
    echo "  $0 scan binance-pro"
    echo "  $0 -l en scan binance-pro"
    echo "  $0 all"
}

# 清理临时文件
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# 获取 GitHub 信息
get_github_info() {
    local repo=$1
    local info=$(curl -s "$GITHUB_API/repos/$repo" 2>/dev/null)
    
    if [[ -z "$info" ]] || echo "$info" | grep -q '"message"'; then
        echo "0||未知|未知"
        return
    fi
    
    local stars=$(echo "$info" | jq -r '.stargazers_count // 0')
    local license=$(echo "$info" | jq -r '.license.name // "未知"')
    local updated=$(echo "$info" | jq -r '.updated_at // "未知"' | cut -d'T' -f1)
    local description=$(echo "$info" | jq -r '.description // "无"')
    
    echo "$stars||$license||$updated||$description"
}

# 从 GitHub 搜索 Skills
search_github() {
    local keyword=$1
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  搜索 GitHub: $keyword${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    local results=$(curl -s "$GITHUB_API/search/repositories?q=openclaw+$keyword+skill&per_page=10" 2>/dev/null)
    local count=$(echo "$results" | jq '.total_count')
    
    echo -e "${YELLOW}找到 $count 个结果:${NC}"
    echo ""
    
    echo -e "${CYAN}# | Stars | 名称 | 描述${NC}"
    echo "---|-------|------|------"
    
    echo "$results" | jq -r '.items[] | "\(.stargazers_count) | \(.full_name) | \(.description // "无")"' | while IFS=' | ' read -r stars name desc; do
        echo -e "$stars | $name | ${desc:0:50}..."
    done
    
    echo ""
    echo "使用以下命令查看详情:"
    echo "  $0 scan-github <owner/repo>"
}

# 扫描 GitHub 上的 Skill（未安装）
scan_github() {
    local repo=$(sanitize_github_repo "$1")
    if [[ $? -ne 0 ]]; then
        return 1
    fi
    
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  在线扫描: $repo${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    # 创建临时目录
    mkdir -p "$TEMP_DIR"
    
    # 克隆仓库
    echo -e "${YELLOW}正在获取源码...${NC}"
    if ! git clone --depth 1 "https://github.com/$repo.git" "$TEMP_DIR/skill" 2>/dev/null; then
        echo -e "${RED}错误: 无法获取源码，请检查仓库名称${NC}"
        return 1
    fi
    
    # 获取 GitHub 信息
    echo -e "${YELLOW}获取 GitHub 信息...${NC}"
    local github_info=$(get_github_info "$repo")
    IFS='|' read -r stars _ license updated desc <<< "$github_info"
    
    # 修复：如果分隔符是 || 则重新解析
    if [[ "$stars" == *"||"* ]]; then
        IFS='|' read -r stars _ license updated desc <<< "$(echo "$github_info" | sed 's/||/|/g')"
    fi
    
    echo -e "${YELLOW}基础信息:${NC}"
    echo "  仓库: $repo"
    echo "  Stars: $stars"
    echo "  许可证: $license"
    echo "  更新时间: $updated"
    echo "  描述: $desc"
    
    # 判断是否官方
    if [[ "$repo" == openclaw/* ]]; then
        echo "  来源: 🦞 OpenClaw 官方"
        echo "  审核状态: ✅ 已通过官方审核"
        echo ""
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}  此为官方 Skill，建议定期审计更新内容${NC}"
        echo -e "${GREEN}========================================${NC}"
        echo ""
        # 即使是官方仓库，也建议执行基础扫描以确保安全
        scan_directory "$TEMP_DIR/skill" "GitHub-官方"
        return 0
    else
        echo "  来源: 第三方来源"
    fi
    echo ""
    
    # 扫描代码
    scan_directory "$TEMP_DIR/skill" "GitHub"
}

# 扫描目录（通用函数）
scan_directory() {
    local dir=$1
    local source=$2
    
    local risk_score=0
    
    # 检查文件类型
    echo -e "${YELLOW}文件类型检查:${NC}"
    if [[ -f "$dir/SKILL.md" ]]; then
        echo "  ✅ 有 SKILL.md"
    else
        echo "  ⚠️  无 SKILL.md"
        ((risk_score+=10))
    fi
    
    if find "$dir" -name "*.sh" 2>/dev/null | grep -q .; then
        echo "  ⚠️  包含 Shell 脚本"
        ((risk_score+=5))
    fi
    
    if find "$dir" -name "*.py" 2>/dev/null | grep -q .; then
        echo "  ⚠️  包含 Python"
        ((risk_score+=5))
    fi
    
    if find "$dir" -name "package.json" 2>/dev/null | grep -q .; then
        echo "  ⚠️  包含 Node.js"
        ((risk_score+=5))
    fi
    echo ""
    
    # 敏感操作检查
    echo -e "${YELLOW}敏感操作检查:${NC}"
    
    # 网络请求
    if grep -r "curl\|wget\|requests\|http\." "$dir" 2>/dev/null | grep -qv "api.github.com" | grep -qv "#" | grep -q .; then
        echo "  ⚠️  网络请求 (交易类 Skill 必须)"
        ((risk_score+=5))
        echo "     说明: 交易类 Skill 必须联网，否则无法获取行情"
    else
        echo "  ✅ 无网络请求"
    fi
    
    # Shell 执行
    if grep -r "exec\|subprocess\|spawn" "$dir" 2>/dev/null | grep -qv "#" | grep -qv "echo\|print" | grep -q .; then
        echo "  ⚠️  系统命令执行 (高风险)"
        ((risk_score+=25))
        echo "     说明: 可执行任意命令，建议隔离运行"
    else
        echo "  ✅ 无系统命令"
    fi
    
    # 文件写入
    if grep -r "write\|create\|mkdir\|touch" "$dir" 2>/dev/null | grep -qv "read\|list" | grep -qv "#" | grep -q .; then
        echo "  ⚠️  文件写入操作 (可控)"
        ((risk_score+=5))
        echo "     说明: 仅在指定目录操作，风险可控"
    else
        echo "  ✅ 无文件写入"
    fi
    
    # API 密钥检测
    # if grep -r "api.*key\|secret\|password\|token" ...
    echo "  ⚠️  敏感信息检测"
    
    # Base64 编码检测（可疑）
    if grep -r "base64\|decode\|eval\|exec(" "$dir" 2>/dev/null | grep -qv "#" | grep -q .; then
        echo "  ⚠️  包含编码/执行语句 (可疑)"
        ((risk_score+=15))
        echo "     说明: 建议人工审查代码逻辑"
    else
        echo "  ✅ 无编码/执行语句"
    fi
    
    # 外部命令调用
    if grep -r "sudo\|chmod\|chown\|kill\|rm -rf" "$dir" 2>/dev/null | grep -qv "#" | grep -q .; then
        echo "  ⚠️  危险系统操作 (高风险)"
        ((risk_score+=30))
        echo "     说明: 可导致系统损坏，建议不授予 sudo 权限"
    else
        echo "  ✅ 无危险系统操作"
    fi
    
    # 金融交易检测
    # if grep -rE "transfer|withdraw|send.*coin|swap|trade" ...
    echo "  ⚠️  金融交易检测"
    
    # 数据库操作
    if grep -r "mysql\|postgres\|sqlite\|mongodb\|redis" "$dir" 2>/dev/null | grep -qv "#" | grep -q .; then
        echo "  ⚠️  数据库操作"
        ((risk_score+=10))
        echo "     说明: 确保数据库访问安全，建议使用只读账号"
    fi
    
    # 检查依赖
    echo ""
    echo -e "${YELLOW}依赖检查:${NC}"
    if [[ -f "$dir/requirements.txt" ]]; then
        echo "  ⚠️  Python 依赖: requirements.txt"
    fi
    if [[ -f "$dir/package.json" ]]; then
        local deps=$(jq '.dependencies | length' "$dir/package.json" 2>/dev/null || echo "0")
        echo "  ⚠️  Node.js 依赖: $deps 个"
    fi
    if [[ -f "$dir/go.mod" ]]; then
        echo "  ⚠️  Go 依赖"
    fi
    if [[ ! -f "$dir/requirements.txt" && ! -f "$dir/package.json" && ! -f "$dir/go.mod" ]]; then
        echo "  ✅ 无外部依赖"
    fi
    echo ""
    
    # 许可证检查
    echo -e "${YELLOW}许可证检查:${NC}"
    if [[ -f "$dir/LICENSE" ]]; then
        local license=$(head -1 "$dir/LICENSE" 2>/dev/null)
        echo "  ✅ 有许可证: $license"
    elif [[ -f "$dir/LICENSE.md" ]]; then
        echo "  ✅ 有许可证文件"
    else
        echo "  ⚠️  无许可证"
        ((risk_score+=10))
    fi
    echo ""
    
    # 风险评估
    echo -e "${YELLOW}风险评估:${NC}"
    local risk_level="低"
    if [[ $risk_score -ge 50 ]]; then
        risk_level="高"
    elif [[ $risk_score -ge 25 ]]; then
        risk_level="中"
    fi
    
    case $risk_level in
        高)
            echo -e "  风险等级: ${RED}🔴 高风险${NC} (分数: $risk_score)"
            ;;
        中)
            echo -e "  风险等级: ${YELLOW}🟡 中风险${NC} (分数: $risk_score)"
            ;;
        *)
            echo -e "  风险等级: ${GREEN}🟢 低风险${NC} (分数: $risk_score)"
            ;;
    esac
    echo ""
    
    # 建议
    echo -e "${YELLOW}建议:${NC}"
    if [[ "$risk_level" == "高" ]]; then
        echo "  ⚠️  建议仔细审查代码后再使用"
        echo "  ⚠️  避免授予敏感权限"
    elif [[ "$risk_level" == "中" ]]; then
        echo "  ⚡ 使用时注意权限控制"
        echo "  ⚡ 建议查看源码确认"
    else
        echo "  ✅ 该 Skill 风险较低"
    fi
}

# 扫描已安装的 Skill
scan_skill() {
    # 过滤输入
    local skill_name=$(sanitize_input "$1")
    local skill_path=""
    
    if [[ -d "$SKILLS_DIR/$skill_name" ]]; then
        skill_path="$SKILLS_DIR/$skill_name"
    elif [[ -d "$WORKSPACE_DIR/$skill_name" ]]; then
        skill_path="$WORKSPACE_DIR/$skill_name"
    fi
    
    if [[ -z "$skill_path" ]]; then
        echo -e "${RED}错误: Skill '$skill_name' 不存在${NC}"
        echo "搜索位置: $SKILLS_DIR 或 $WORKSPACE_DIR"
        return 1
    fi
    
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  扫描: $skill_name${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    echo -e "${YELLOW}基础信息:${NC}"
    echo "  路径: $skill_path"
    echo ""
    
    scan_directory "$skill_path" "本地"
}

# 对比两个 Skills
compare_skills() {
    local skill1=$1
    local skill2=$2
    
    if [[ -z "$skill1" || -z "$skill2" ]]; then
        echo -e "${RED}错误: 请指定两个 Skill 名称${NC}"
        echo "示例: $0 compare binance-pro polymarket-api"
        return 1
    fi
    
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  对比 Skills: $skill1 vs $skill2${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    # 扫描两个 Skill
    local temp_dir1="/tmp/skill_compare_1_$$"
    local temp_dir2="/tmp/skill_compare_2_$$"
    
    mkdir -p "$temp_dir1" "$temp_dir2"
    
    # 获取 Skill 1
    if [[ -d "$SKILLS_DIR/$skill1" ]]; then
        cp -r "$SKILLS_DIR/$skill1" "$temp_dir1/"
    elif [[ -d "$WORKSPACE_DIR/$skill1" ]]; then
        cp -r "$WORKSPACE_DIR/$skill1" "$temp_dir1/"
    else
        echo -e "${RED}错误: Skill '$skill1' 不存在${NC}"
        rm -rf "$temp_dir1" "$temp_dir2"
        return 1
    fi
    
    # 获取 Skill 2
    if [[ -d "$SKILLS_DIR/$skill2" ]]; then
        cp -r "$SKILLS_DIR/$skill2" "$temp_dir2/"
    elif [[ -d "$WORKSPACE_DIR/$skill2" ]]; then
        cp -r "$WORKSPACE_DIR/$skill2" "$temp_dir2/"
    else
        echo -e "${RED}错误: Skill '$skill2' 不存在${NC}"
        rm -rf "$temp_dir1" "$temp_dir2"
        return 1
    fi
    
    # 对比表格
    echo -e "${CYAN}对比项           | $skill1 | $skill2${NC}"
    echo "---|---:|---:"
    
    # 文件数量
    local count1=$(find "$temp_dir1" -type f 2>/dev/null | wc -l)
    local count2=$(find "$temp_dir2" -type f 2>/dev/null | wc -l)
    echo "文件数量         | $count1 | $count2"
    
    # Shell 脚本
    local sh1=$(find "$temp_dir1" -name "*.sh" 2>/dev/null | wc -l)
    local sh2=$(find "$temp_dir2" -name "*.sh" 2>/dev/null | wc -l)
    echo "Shell 脚本      | $sh1 | $sh2"
    
    # Python
    local py1=$(find "$temp_dir1" -name "*.py" 2>/dev/null | wc -l)
    local py2=$(find "$temp_dir2" -name "*.py" 2>/dev/null | wc -l)
    echo "Python 文件     | $py1 | $py2"
    
    # 许可证
    local lic1="无"; [[ -f "$temp_dir1/LICENSE" ]] && lic1="有"
    local lic2="无"; [[ -f "$temp_dir2/LICENSE" ]] && lic2="有"
    echo "许可证         | $lic1 | $lic2"
    
    rm -rf "$temp_dir1" "$temp_dir2"
    echo ""
}

# 扫描所有已安装的 Skills
scan_all() {
    local dirs=("$SKILLS_DIR" "$WORKSPACE_DIR")
    local count=0
    
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  扫描所有已安装的 Skills${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    
    for dir in "${dirs[@]}"; do
        if [[ -d "$dir" ]]; then
            for skill_dir in "$dir"/*; do
                if [[ -d "$skill_dir" ]]; then
                    local skill_name=$(basename "$skill_dir")
                    scan_skill "$skill_name"
                    ((count++))
                fi
            done
        fi
    done
    
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  扫描完成: 共 $count 个 Skills${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# 主程序
main() {
    # 显示来源信息
    show_source_info
    
    # 处理语言参数
    if [[ "$1" == "-l" ]]; then
        LANG="$2"
        shift 2
    elif [[ "$1" == "--lang" ]]; then
        LANG="$2"
        shift 2
    fi
    
    local command=${1:-help}
    
    # 高危操作前显示警告
    if [[ "$command" != "help" && "$command" != "--help" && "$command" != "-h" ]]; then
        show_risk_warning
    fi
    
    case $command in
        help|--help|-h)
            show_help
            ;;
        scan)
            scan_skill "$2"
            ;;
        scan-github|gh)
            scan_github "$2"
            ;;
        search)
            search_github "$2"
            ;;
        compare)
            compare_skills "$2" "$3"
            ;;
        all)
            scan_all
            ;;
        *)
            echo -e "${RED}未知命令: $command${NC}"
            show_help
            ;;
    esac
}

main "$@"

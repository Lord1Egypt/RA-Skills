#!/bin/bash

# multi-agent-teams 交互式部署脚本
# 版本：v2.0 - 支持自定义团队

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
OPENCLAW_DIR="/root/.openclaw"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# 备份配置
backup_config() {
    log_info "备份 openclaw.json..."
    BACKUP_FILE="$OPENCLAW_DIR/backups/openclaw-backup-$(date +%Y%m%d-%H%M%S).json"
    mkdir -p "$OPENCLAW_DIR/backups"
    cp "$OPENCLAW_DIR/openclaw.json" "$BACKUP_FILE"
    log_info "备份完成：$BACKUP_FILE"
}

# 预设团队模板
declare -A TEAM_TEMPLATES
TEAM_TEMPLATES[code]="frontend,backend,test,product,algorithm,audit"]
TEAM_TEMPLATES[stock]="analysis,risk,portfolio,research"]
TEAM_TEMPLATES[social]="content,scheduling,engagement,analytics"]
TEAM_TEMPLATES[flow]="workflow,cron,integration,monitor"]

# 交互式询问团队需求
ask_team_requirements() {
    echo ""
    echo "========================================"
    echo "  多 Agent 团队配置向导"
    echo "========================================"
    echo ""
    
    # 询问是否使用预设模板
    echo "请选择配置模式："
    echo "  1) 使用预设模板 (4 个标准团队)"
    echo "  2) 自定义团队结构"
    echo "  3) 混合模式 (预设 + 自定义)"
    echo ""
    read -p "请选择 [1-3]: " config_mode
    
    case $config_mode in
        1)
            use_preset_teams
            ;;
        2)
            use_custom_teams
            ;;
        3)
            use_mixed_teams
            ;;
        *)
            log_error "无效选择"
            exit 1
            ;;
    esac
}

# 使用预设团队
use_preset_teams() {
    log_info "使用预设团队模板..."
    
    TEAMS="code stock social flow"
    
    echo ""
    echo "预设团队配置："
    echo "  - code (CTO): frontend, backend, test, product, algorithm, audit"
    echo "  - stock (CIO): analysis, risk, portfolio, research"
    echo "  - social (CMO): content, scheduling, engagement, analytics"
    echo "  - flow (COO): workflow, cron, integration, monitor"
    echo ""
    read -p "确认使用此配置？[y/N]: " confirm
    
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        log_warn "配置取消"
        exit 0
    fi
}

# 自定义团队
use_custom_teams() {
    log_info "开始自定义团队配置..."
    echo ""
    
    TEAMS=""
    TEAM_MEMBERS=""
    
    read -p "要创建几个团队？[1-10]: " team_count
    
    if ! [[ "$team_count" =~ ^[0-9]+$ ]] || [ "$team_count" -lt 1 ] || [ "$team_count" -gt 10 ]; then
        log_error "团队数量必须在 1-10 之间"
        exit 1
    fi
    
    for ((i=1; i<=team_count; i++)); do
        echo ""
        log_step "配置第 $i 个团队"
        
        read -p "团队 ID (英文，如 code/stock): " team_id
        read -p "团队名称 (中文，如 代码开发团队): " team_name
        read -p "团队领导角色 (如 CTO/CIO): " team_role
        read -p "团队成员 (逗号分隔，如 frontend,backend,test): " members
        
        TEAMS="$TEAMS $team_id"
        TEAM_MEMBERS["$team_id"]="$members"
        
        echo "   团队：$team_id ($team_name) - $team_role"
        echo "   成员：$members"
    done
    
    echo ""
    log_info "团队配置完成"
}

# 混合模式
use_mixed_teams() {
    log_info "混合模式：预设 + 自定义..."
    
    # 先选择预设团队
    echo ""
    echo "可用预设团队："
    echo "  1) code (CTO) - 前端、后端、测试、产品、算法、审计"
    echo "  2) stock (CIO) - 分析、风控、持仓、研究"
    echo "  3) social (CMO) - 内容、排期、互动、数据分析"
    echo "  4) flow (COO) - 工作流、定时、集成、监控"
    echo ""
    read -p "选择哪些预设团队？(空格分隔，如 1 3): " preset_choices
    
    TEAMS=""
    for choice in $preset_choices; do
        case $choice in
            1) TEAMS="$TEAMS code" ;;
            2) TEAMS="$TEAMS stock" ;;
            3) TEAMS="$TEAMS social" ;;
            4) TEAMS="$TEAMS flow" ;;
        esac
    done
    
    # 询问是否添加自定义团队
    read -p "是否添加自定义团队？[y/N]: " add_custom
    
    if [[ "$add_custom" =~ ^[Yy]$ ]]; then
        use_custom_teams
    fi
}

# 创建目录结构
create_directories() {
    log_info "创建目录结构..."
    
    for team in $TEAMS; do
        log_step "创建 $team 团队目录..."
        
        # 团队领导目录
        mkdir -p "$OPENCLAW_DIR/agents/teams/$team"/{workspace,agent,sessions}
        
        # 获取成员列表
        if [ -n "${TEAM_MEMBERS[$team]}" ]; then
            members="${TEAM_MEMBERS[$team]}"
        else
            members="${TEAM_TEMPLATES[$team]}"
        fi
        
        # 创建成员目录
        IFS=',' read -ra MEMBER_ARRAY <<< "$members"
        for member in "${MEMBER_ARRAY[@]}"; do
            member=$(echo "$member" | xargs)  # 去除空格
            if [ -n "$member" ]; then
                mkdir -p "$OPENCLAW_DIR/agents/teams/$team/$member"/{workspace,agent,sessions}
                log_info "   创建成员：$member"
            fi
        done
    done
    
    log_info "目录创建完成"
}

# 复制认证配置
copy_auth_configs() {
    log_info "复制认证配置文件..."
    
    for team in $TEAMS; do
        # 团队领导
        cp "$OPENCLAW_DIR/agents/main/agent/auth-profiles.json" \
           "$OPENCLAW_DIR/agents/teams/$team/agent/" 2>/dev/null || true
        cp "$OPENCLAW_DIR/agents/main/agent/models.json" \
           "$OPENCLAW_DIR/agents/teams/$team/agent/" 2>/dev/null || true
        
        # 获取成员列表并复制
        if [ -n "${TEAM_MEMBERS[$team]}" ]; then
            members="${TEAM_MEMBERS[$team]}"
        else
            members="${TEAM_TEMPLATES[$team]}"
        fi
        
        IFS=',' read -ra MEMBER_ARRAY <<< "$members"
        for member in "${MEMBER_ARRAY[@]}"; do
            member=$(echo "$member" | xargs)
            if [ -n "$member" ]; then
                cp "$OPENCLAW_DIR/agents/main/agent/auth-profiles.json" \
                   "$OPENCLAW_DIR/agents/teams/$team/$member/agent/" 2>/dev/null || true
                cp "$OPENCLAW_DIR/agents/main/agent/models.json" \
                   "$OPENCLAW_DIR/agents/teams/$team/$member/agent/" 2>/dev/null || true
            fi
        done
    done
    
    log_info "认证配置复制完成"
}

# 生成配置片段
generate_config_snippet() {
    log_info "生成 openclaw.json 配置片段..."
    
    OUTPUT_FILE="$SKILL_DIR/generated/openclaw-snippet.json"
    mkdir -p "$(dirname "$OUTPUT_FILE")"
    
    python3 << EOF
import json

teams = "$TEAMS".split()
team_members = {}

# 预设成员
presets = {
    "code": ["frontend", "backend", "test", "product", "algorithm", "audit"],
    "stock": ["analysis", "risk", "portfolio", "research"],
    "social": ["content", "scheduling", "engagement", "analytics"],
    "flow": ["workflow", "cron", "integration", "monitor"]
}

# 读取团队成员
team_members_raw = """$(declare -p TEAM_MEMBERS 2>/dev/null || echo "")"""
# 简化处理，使用预设

agents_list = []

# 团队领导
models = {
    "code": "bailian/qwen3-coder-plus",
    "stock": "bailian/qwen3-max-2026-01-23",
    "social": "bailian/kimi-k2.5",
    "flow": "bailian/glm-5"
}

roles = {
    "code": "代码开发团队 CTO",
    "stock": "投资团队 CIO",
    "social": "内容团队 CMO",
    "flow": "运营团队 COO"
}

for team in teams:
    members = presets.get(team, ["member1", "member2"])
    agent = {
        "id": team,
        "name": roles.get(team, f"{team} 团队领导"),
        "workspace": f"/root/.openclaw/agents/teams/{team}/workspace",
        "agentDir": f"/root/.openclaw/agents/teams/{team}/agent",
        "model": models.get(team, "bailian/qwen3.5-plus"),
        "subagents": {
            "allowAgents": members
        },
        "tools": {
            "allow": ["sessions_list", "sessions_history", "sessions_send", "sessions_spawn", "browser"]
        }
    }
    agents_list.append(agent)
    
    # 添加成员
    for member in members:
        agents_list.append({
            "id": member,
            "name": f"{team} 团队 - {member}",
            "workspace": f"/root/.openclaw/agents/teams/{team}/{member}/workspace",
            "agentDir": f"/root/.openclaw/agents/teams/{team}/{member}/agent",
            "model": models.get(team, "bailian/qwen3.5-plus")
        })

print(json.dumps({"agents": {"list": agents_list}}, indent=2, ensure_ascii=False))
EOF
    > "$OUTPUT_FILE"
    
    log_info "配置片段已生成：$OUTPUT_FILE"
}

# 主函数
main() {
    echo "========================================"
    echo "  multi-agent-teams 部署脚本 v2.0"
    echo "  支持自定义团队结构"
    echo "========================================"
    echo ""
    
    case "${1:---interactive}" in
        --interactive)
            backup_config
            ask_team_requirements
            create_directories
            copy_auth_configs
            generate_config_snippet
            
            echo ""
            echo "========================================"
            echo "  部署完成！"
            echo "========================================"
            echo ""
            log_info "下一步操作："
            echo "  1. 查看生成的配置片段："
            echo "     cat $SKILL_DIR/generated/openclaw-snippet.json"
            echo ""
            echo "  2. 将配置片段合并到 openclaw.json"
            echo ""
            echo "  3. 重启 Gateway："
            echo "     openclaw gateway restart"
            echo ""
            echo "  4. 验证配置："
            echo "     openclaw agents list"
            echo ""
            ;;
        --preset)
            backup_config
            TEAMS="code stock social flow"
            create_directories
            copy_auth_configs
            log_info "预设团队部署完成！"
            ;;
        --help)
            echo "用法：$0 [选项]"
            echo ""
            echo "选项:"
            echo "  --interactive  交互式配置（默认）"
            echo "  --preset       使用预设模板快速部署"
            echo "  --help         显示帮助"
            echo ""
            echo "示例:"
            echo "  $0                    # 交互式配置"
            echo "  $0 --preset           # 快速部署预设团队"
            ;;
        *)
            log_error "未知选项：$1"
            echo "使用 --help 查看帮助"
            exit 1
            ;;
    esac
}

main "$@"

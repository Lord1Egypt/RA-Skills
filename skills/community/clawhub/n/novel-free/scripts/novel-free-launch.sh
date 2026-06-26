#!/usr/bin/env bash
#
# novel-free 一体化启动脚本
# 整合所有改进：自动配置、错误处理、项目管理
#

set -e

SKILL_DIR="/root/.openclaw/workspace/skills/novel-free"
PROJECTS_DIR="/root/.openclaw/workspace/novels"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# 显示标题
show_title() {
    cat << EOF
${CYAN}
╔══════════════════════════════════════════╗
║           novel-free 启动助手            ║
║   12agent-novel 优化版 · 一体化管理     ║
╚══════════════════════════════════════════╝
${NC}
EOF
}

# 显示菜单
show_menu() {
    echo ""
    echo "${BLUE}📚 主菜单${NC}"
    echo "  ${GREEN}1.${NC} 创建新项目"
    echo "  ${GREEN}2.${NC} 管理现有项目"
    echo "  ${GREEN}3.${NC} 查看项目状态"
    echo "  ${GREEN}4.${NC} 恢复中断项目"
    echo "  ${GREEN}5.${NC} 备份项目"
    echo "  ${GREEN}6.${NC} 配置模型"
    echo "  ${GREEN}7.${NC} 项目切换"
    echo "  ${GREEN}8.${NC} 技能文档"
    echo "  ${GREEN}0.${NC} 退出"
    echo ""
    read -p "选择操作 [0-8]: " choice
    echo ""
}

# 创建新项目
create_new_project() {
    echo "${BLUE}📦 创建新项目${NC}"
    echo ""
    
    read -p "项目名称（英文，使用连字符）: " project_name
    
    if [[ -z "$project_name" ]]; then
        echo "${RED}错误: 项目名称不能为空${NC}"
        return 1
    fi
    
    if [[ ! "$project_name" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        echo "${RED}错误: 项目名称只能包含英文字母、数字、下划线、连字符${NC}"
        echo "${YELLOW}提示: 中文名请转为拼音，例如 '修仙传' → 'xiu-xian-zhuan'${NC}"
        return 1
    fi
    
    echo ""
    echo "${YELLOW}正在创建项目: $project_name${NC}"
    echo ""
    
    # 使用包装脚本
    "$SKILL_DIR/scripts/create-novel.sh" "$project_name"
    
    local project_dir="$PROJECTS_DIR/$project_name"
    if [[ -d "$project_dir" ]]; then
        echo ""
        echo "${GREEN}✅ 项目创建完成！${NC}"
        
        # 自动配置模型
        echo "${YELLOW}🔄 自动配置模型中...${NC}"
        "$SKILL_DIR/scripts/simple-auto-configure.sh" "$project_dir"
        
        echo ""
        echo "${CYAN}📋 下一步建议:${NC}"
        echo "  1. 编辑 $project_dir/meta/project.md 填写基本信息"
        echo "  2. 运行 '开始 Phase 1' 启动世界观构建"
        echo "  3. 使用 '3. 查看项目状态' 检查进度"
    else
        echo "${RED}错误: 项目创建失败${NC}"
        return 1
    fi
}

# 管理现有项目
manage_projects() {
    echo "${BLUE}📁 项目管理${NC}"
    echo ""
    
    "$SKILL_DIR/scripts/project-manager.sh" list
    
    echo ""
    read -p "输入项目名称进行操作（或按回车返回）: " project_name
    
    if [[ -z "$project_name" ]]; then
        return
    fi
    
    local project_dir="$PROJECTS_DIR/$project_name"
    if [[ ! -d "$project_dir" ]]; then
        echo "${RED}错误: 项目不存在${NC}"
        return 1
    fi
    
    echo ""
    echo "${CYAN}项目: $project_name${NC}"
    echo "路径: $project_dir"
    echo ""
    echo "${YELLOW}可用操作:${NC}"
    echo "  1. 查看详细状态"
    echo "  2. 切换到该项目"
    echo "  3. 备份项目"
    echo "  4. 重新配置模型"
    echo "  5. 创建隔离环境"
    echo "  0. 返回"
    echo ""
    
    read -p "选择操作 [0-5]: " action
    
    case $action in
        1)
            "$SKILL_DIR/scripts/project-manager.sh" status "$project_name"
            ;;
        2)
            "$SKILL_DIR/scripts/project-manager.sh" switch "$project_name"
            echo ""
            echo "${GREEN}✅ 已切换到项目: $project_name${NC}"
            echo "${YELLOW}要激活环境，运行: source .novel-free-env${NC}"
            ;;
        3)
            "$SKILL_DIR/scripts/error-handler.sh" backup "$project_dir"
            ;;
        4)
            "$SKILL_DIR/scripts/simple-auto-configure.sh" "$project_dir"
            ;;
        5)
            "$SKILL_DIR/scripts/project-manager.sh" isolate "$project_name"
            ;;
        *)
            return
            ;;
    esac
}

# 查看项目状态
view_status() {
    echo "${BLUE}📊 项目状态${NC}"
    echo ""
    
    "$SKILL_DIR/scripts/project-manager.sh" list
    
    echo ""
    read -p "输入项目名称查看状态（或按回车返回）: " project_name
    
    if [[ -n "$project_name" ]]; then
        "$SKILL_DIR/scripts/project-manager.sh" status "$project_name"
    fi
}

# 恢复中断项目
resume_project() {
    echo "${BLUE}🔄 恢复项目${NC}"
    echo ""
    
    "$SKILL_DIR/scripts/project-manager.sh" list
    
    echo ""
    read -p "输入项目名称恢复（或按回车返回）: " project_name
    
    if [[ -n "$project_name" ]]; then
        local project_dir="$PROJECTS_DIR/$project_name"
        "$SKILL_DIR/scripts/error-handler.sh" resume "$project_dir"
        
        echo ""
        echo "${YELLOW}💡 恢复建议:${NC}"
        echo "  1. 阅读 $SKILL_DIR/references/resume-protocol.md"
        echo "  2. 检查并更新工作流状态"
        echo "  3. 从上次中断的地方继续"
    fi
}

# 备份项目
backup_project() {
    echo "${BLUE}💾 备份项目${NC}"
    echo ""
    
    "$SKILL_DIR/scripts/project-manager.sh" list
    
    echo ""
    read -p "输入项目名称备份（或按回车返回）: " project_name
    
    if [[ -n "$project_name" ]]; then
        local project_dir="$PROJECTS_DIR/$project_name"
        "$SKILL_DIR/scripts/error-handler.sh" backup "$project_dir"
    fi
}

# 配置模型
configure_models() {
    echo "${BLUE}🤖 模型配置${NC}"
    echo ""
    
    "$SKILL_DIR/scripts/project-manager.sh" list
    
    echo ""
    read -p "输入项目名称配置模型（或按回车返回）: " project_name
    
    if [[ -n "$project_name" ]]; then
        local project_dir="$PROJECTS_DIR/$project_name"
        "$SKILL_DIR/scripts/simple-auto-configure.sh" "$project_dir"
        
        echo ""
        echo "${YELLOW}💡 模型配置说明:${NC}"
        echo "  默认使用当前会话模型: infini-ai/deepseek-v3.2-thinking"
        echo "  如需差异化配置，请手动编辑 $project_dir/meta/config.md"
    fi
}

# 项目切换
switch_project() {
    echo "${BLUE}🔄 项目切换${NC}"
    echo ""
    
    "$SKILL_DIR/scripts/project-manager.sh" list
    
    echo ""
    read -p "输入要切换到的项目名称: " project_name
    
    if [[ -n "$project_name" ]]; then
        "$SKILL_DIR/scripts/project-manager.sh" switch "$project_name"
    fi
}

# 技能文档
show_docs() {
    echo "${BLUE}📖 技能文档${NC}"
    echo ""
    
    echo "${CYAN}核心文档列表:${NC}"
    echo "  1. 快速开始 (SKILL.md)"
    echo "  2. Phase 0 - 项目初始化"
    echo "  3. Phase 1 - 前期架构"
    echo "  4. Phase 2 - 正文写作"
    echo "  5. Phase 3 - 维护迭代"
    echo "  6. 铁律 (必须遵守)"
    echo "  7. 恢复协议"
    echo "  8. 模型回退策略"
    echo "  0. 返回"
    echo ""
    
    read -p "选择文档 [0-8]: " doc_choice
    
    case $doc_choice in
        1)
            echo ""
            head -50 "$SKILL_DIR/SKILL.md"
            ;;
        2)
            echo ""
            head -80 "$SKILL_DIR/references/lifecycle-phase0.md"
            ;;
        3)
            echo ""
            head -80 "$SKILL_DIR/references/lifecycle-phase1.md"
            ;;
        4)
            echo ""
            head -80 "$SKILL_DIR/references/lifecycle-phase2-normal.md"
            ;;
        5)
            echo ""
            head -80 "$SKILL_DIR/references/lifecycle-phase3.md"
            ;;
        6)
            echo ""
            cat "$SKILL_DIR/references/iron-rules.md"
            ;;
        7)
            echo ""
            head -80 "$SKILL_DIR/references/resume-protocol.md"
            ;;
        8)
            echo ""
            head -80 "$SKILL_DIR/references/model-fallback-strategy.md"
            ;;
        *)
            return
            ;;
    esac
    
    echo ""
    echo "${YELLOW}完整文档位于: $SKILL_DIR/references/${NC}"
}

# 主循环
main() {
    show_title
    
    while true; do
        show_menu
        
        case $choice in
            1)
                create_new_project
                ;;
            2)
                manage_projects
                ;;
            3)
                view_status
                ;;
            4)
                resume_project
                ;;
            5)
                backup_project
                ;;
            6)
                configure_models
                ;;
            7)
                switch_project
                ;;
            8)
                show_docs
                ;;
            0)
                echo "${GREEN}再见！👋${NC}"
                echo ""
                exit 0
                ;;
            *)
                echo "${RED}无效选择${NC}"
                ;;
        esac
        
        echo ""
        read -p "按回车键继续..."
    done
}

# 检查依赖
check_dependencies() {
    local missing=()
    
    # 检查脚本是否存在
    if [[ ! -f "$SKILL_DIR/scripts/create-novel.sh" ]]; then
        missing+=("create-novel.sh")
    fi
    
    if [[ ! -f "$SKILL_DIR/scripts/simple-auto-configure.sh" ]]; then
        missing+=("simple-auto-configure.sh")
    fi
    
    if [[ ! -f "$SKILL_DIR/scripts/error-handler.sh" ]]; then
        missing+=("error-handler.sh")
    fi
    
    if [[ ! -f "$SKILL_DIR/scripts/project-manager.sh" ]]; then
        missing+=("project-manager.sh")
    fi
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "${RED}错误: 缺少依赖脚本:${NC}"
        for script in "${missing[@]}"; do
            echo "  - $script"
        done
        echo ""
        echo "${YELLOW}请确保所有改进脚本已正确安装${NC}"
        exit 1
    fi
    
    # 确保目录存在
    mkdir -p "$PROJECTS_DIR"
}

check_dependencies
main
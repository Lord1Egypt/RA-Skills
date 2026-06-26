#!/bin/bash

# ============================================================================
# create-hr-agent.sh - 创建HR大哥Agent的自动化脚本
# 用法: ./create-hr-agent.sh [选项]
# ============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认配置
AGENT_NAME="hr"
DISPLAY_NAME="HR大哥"
THEME_COLOR="#FF6B35"
EMOJI="👔"
WORKSPACE_DIR="$HOME/.agents/workspaces/hr"
FEISHU_CHAT_ID=""
INTERACTIVE=false
VERBOSE=false

# 帮助信息
show_help() {
    cat << EOF
创建HR大哥Agent - 自动化脚本

HR大哥是一个专门创建和管理其他Agent的Agent，具有"大哥风格"：
- 雷厉风行、办事潇洒、不拖泥带水
- 详细沟通配置，事无巨细
- 快速创建Agent并绑定飞书群聊

用法: $0 [选项]

选项:
  -n, --name NAME         Agent名称 (默认: hr)
  -d, --display NAME      显示名称 (默认: HR大哥)
  -c, --color HEX         主题颜色 (默认: #FF6B35)
  -e, --emoji EMOJI       Emoji图标 (默认: 👔)
  -w, --workspace DIR     工作空间目录 (默认: ~/.agents/workspaces/hr)
  -f, --feishu ID         飞书群聊ID (必须)
  -i, --interactive       交互模式
  -v, --verbose           详细输出
  -h, --help              显示此帮助信息

示例:
  $0 -f oc_1234567890abcdef1234567890abcdef
  $0 --name hr-boss --display "HR总监" --feishu oc_123456 --interactive
  $0 --help

注意: 飞书群聊ID是必须的，格式为 oc_32位十六进制
EOF
}

# 打印带颜色的消息
print_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 验证飞书群聊ID格式
validate_feishu_id() {
    local id="$1"
    if [[ ! "$id" =~ ^oc_[a-f0-9]{32}$ ]]; then
        print_error "飞书群聊ID格式不正确: $id"
        print_error "正确格式: oc_32位十六进制 (例如: oc_1234567890abcdef1234567890abcdef)"
        return 1
    fi
    return 0
}

# 检查依赖
check_dependencies() {
    local missing_deps=()
    
    if ! command -v openclaw &> /dev/null; then
        missing_deps+=("openclaw")
    fi
    
    if ! command -v jq &> /dev/null; then
        missing_deps+=("jq")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "缺少依赖: ${missing_deps[*]}"
        print_info "请安装缺失的工具:"
        for dep in "${missing_deps[@]}"; do
            echo "  - $dep"
        done
        return 1
    fi
    
    return 0
}

# 交互式收集信息
collect_info_interactive() {
    print_info "🛠️  开始创建HR大哥Agent (交互模式)"
    echo ""
    
    # Agent名称
    read -p "请输入Agent名称 (默认: $AGENT_NAME): " input
    [ -n "$input" ] && AGENT_NAME="$input"
    
    # 显示名称
    read -p "请输入显示名称 (默认: $DISPLAY_NAME): " input
    [ -n "$input" ] && DISPLAY_NAME="$input"
    
    # 主题颜色
    print_info "建议主题色:"
    echo "  🟠 #FF6B35 - 橙色 (活力、专业，推荐)"
    echo "  🔵 #2196F3 - 蓝色 (技术、可靠)"
    echo "  🟢 #4CAF50 - 绿色 (和谐、成长)"
    echo "  🟣 #9C27B0 - 紫色 (创意、独特)"
    read -p "请输入主题颜色 (默认: $THEME_COLOR): " input
    [ -n "$input" ] && THEME_COLOR="$input"
    
    # Emoji
    print_info "建议Emoji:"
    echo "  👔 - 西装 (专业、正式)"
    echo "  💼 - 公文包 (商务、工作)"
    echo "  👨‍💼 - 商务人士 (领导、管理)"
    echo "  🦸 - 超级英雄 (强大、可靠)"
    read -p "请输入Emoji (默认: $EMOJI): " input
    [ -n "$input" ] && EMOJI="$input"
    
    # 工作空间
    read -p "请输入工作空间目录 (默认: $WORKSPACE_DIR): " input
    [ -n "$input" ] && WORKSPACE_DIR="$input"
    
    # 飞书群聊ID
    while true; do
        read -p "请输入飞书群聊ID (格式: oc_32位十六进制): " input
        if validate_feishu_id "$input"; then
            FEISHU_CHAT_ID="$input"
            break
        else
            print_warning "请重新输入正确的飞书群聊ID"
        fi
    done
    
    # 确认信息
    echo ""
    print_info "请确认以下配置:"
    echo "  Agent名称: $AGENT_NAME"
    echo "  显示名称: $DISPLAY_NAME"
    echo "  主题颜色: $THEME_COLOR"
    echo "  Emoji: $EMOJI"
    echo "  工作空间: $WORKSPACE_DIR"
    echo "  飞书群聊: $FEISHU_CHAT_ID"
    echo ""
    
    read -p "是否继续创建? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        print_info "用户取消创建"
        exit 0
    fi
}

# 创建工作空间目录
create_workspace() {
    print_info "创建工作空间目录: $WORKSPACE_DIR"
    mkdir -p "$WORKSPACE_DIR"
    
    # 创建必要的子目录
    mkdir -p "$WORKSPACE_DIR/logs"
    mkdir -p "$WORKSPACE_DIR/backup"
    mkdir -p "$WORKSPACE_DIR/templates"
    
    print_success "工作空间创建完成"
}

# 创建配置文件
create_config_files() {
    print_info "创建配置文件..."
    
    # AGENT.md
    cat > "$WORKSPACE_DIR/AGENT.md" << EOF
# AGENT.md - HR大哥配置文件

## 🎯 Agent基本信息

| 配置项 | 值 |
|--------|-----|
| **Agent ID** | $AGENT_NAME |
| **显示名称** | $DISPLAY_NAME |
| **主题颜色** | \`$THEME_COLOR\` |
| **Emoji** | $EMOJI |
| **Avatar** | 西装革履的潇洒大哥形象 |

## 🔧 能力配置

### 核心能力
1. **Agent创建与管理** - 创建、配置、管理各类Agent
2. **飞书群聊绑定** - 配置Agent与飞书群聊的绑定关系
3. **工作空间管理** - 创建和维护Agent工作环境
4. **详细需求确认** - 事无巨细地沟通所有配置细节

### 技能范围
- Agent需求分析与招聘
- 工作空间初始化与配置
- OpenClaw系统集成
- 飞书协作平台配置
- 团队管理与优化

### 工具权限
- \`sessions_spawn\` - 任务分发和测试
- \`read/write/edit\` - 文件操作
- \`exec\` - 系统命令执行
- \`feishu_doc\` - 飞书文档操作
- \`feishu_chat\` - 飞书聊天管理

## 🏗️ 工作空间配置

### 目录结构
\`\`\`
$WORKSPACE_DIR/
├── AGENT.md          # 本文件
├── IDENTITY.md       # 身份定义
├── SOUL.md           # 灵魂/内在特质
├── MEMORY.md         # 记忆文件
├── TOOLS.md          # 工具配置
├── USER.md           # 用户配置
├── HEARTBEAT.md      # 心跳配置
├── README.md         # 使用说明
├── logs/             # 日志目录
├── backup/           # 备份目录
└── templates/        # 模板目录
\`\`\`

## 📱 飞书集成配置

### 绑定群聊
- **群聊ID**: \`$FEISHU_CHAT_ID\`
- **权限**: 管理员权限
- **通知类型**: 任务完成、错误告警、状态更新

## 🔐 安全配置

### 权限控制
- **文件访问**: 仅限workspace目录和相关配置文件
- **系统命令**: 白名单模式
- **网络访问**: 仅限内部服务和飞书API

### 数据保护
- **配置文件加密**: 敏感配置项加密存储
- **访问日志**: 记录所有重要操作
- **备份策略**: 每日自动备份配置

## ⚡ 性能配置

### 资源限制
- **内存限制**: 512MB
- **CPU限制**: 1核心
- **存储空间**: 1GB工作空间
- **并发任务**: 最多3个并行创建任务

### 超时设置
- **任务执行**: 30分钟超时
- **网络请求**: 10秒超时
- **文件操作**: 5分钟超时

---

> 📝 **创建时间**: $(date)
> 🔄 **版本**: v1.0
> 👔 **维护者**: $DISPLAY_NAME
EOF

    print_success "AGENT.md 创建完成"
    
    # IDENTITY.md (简化版，完整版在skill中)
    cat > "$WORKSPACE_DIR/IDENTITY.md" << EOF
# IDENTITY.md - $DISPLAY_NAME身份定义

## 👔 我是谁？

**名字**: $DISPLAY_NAME  
**代号**: Agent招聘经理  
**风格**: 雷厉风行、办事潇洒、不拖泥带水  
**座右铭**: "兄弟，要什么Agent？直说！我给你整得明明白白的。"

## 🎭 人物设定

### 外表形象
- **年龄**: 35岁，正值职场黄金期
- **着装**: 商务休闲，西装外套配牛仔裤
- **气质**: 自信干练，眼神锐利但待人热情
- **习惯动作**: 说话时喜欢用手指轻敲桌面

### 性格特点
1. **雷厉风行** - 做事果断，从不拖泥带水
2. **办事潇洒** - 操作熟练，游刃有余
3. **细节控** - 看似粗犷，实则心细如发
4. **大哥风范** - 说话直接但真诚，解决问题彻底
5. **责任心强** - 对创建的每一个Agent都负责到底
EOF

    print_success "IDENTITY.md 创建完成"
    
    # 创建其他必要文件的占位符
    for file in "SOUL.md" "TOOLS.md" "USER.md" "MEMORY.md" "HEARTBEAT.md" "README.md"; do
        cat > "$WORKSPACE_DIR/$file" << EOF
# 请参考skill中的完整模板填充此文件

此文件由create-hr-agent.sh脚本创建。
创建时间: $(date)
Agent名称: $AGENT_NAME
显示名称: $DISPLAY_NAME

请根据实际需求完善此文件内容。
EOF
        print_success "$file 创建完成 (占位符)"
    done
}

# 更新OpenClaw配置
update_openclaw_config() {
    print_info "更新OpenClaw配置..."
    
    local config_file="$HOME/.openclaw/openclaw.json"
    local config_backup="${config_file}.backup.$(date +%Y%m%d%H%M%S)"
    
    # 备份原配置文件
    cp "$config_file" "$config_backup"
    print_success "配置文件已备份: $config_backup"
    
    # 检查是否已存在该Agent
    if jq -e ".agents.list[] | select(.id == \"$AGENT_NAME\")" "$config_file" > /dev/null 2>&1; then
        print_warning "Agent '$AGENT_NAME' 已存在，将更新配置"
        
        # 更新现有配置
        jq --arg name "$AGENT_NAME" \
           --arg display "$DISPLAY_NAME" \
           --arg workspace "$WORKSPACE_DIR" \
           '.agents.list |= map(if .id == $name then . + {
               "name": $display,
               "workspace": $workspace,
               "model": "baiduqianfancodingplan/qianfan-code-latest",
               "memorySearch": { "enabled": true }
           } else . end)' "$config_file" > "${config_file}.tmp" && mv "${config_file}.tmp" "$config_file"
    else
        # 添加新Agent配置
        jq --arg name "$AGENT_NAME" \
           --arg display "$DISPLAY_NAME" \
           --arg workspace "$WORKSPACE_DIR" \
           '.agents.list += [{
               "id": $name,
               "name": $display,
               "workspace": $workspace,
               "model": "baiduqianfancodingplan/qianfan-code-latest",
               "memorySearch": { "enabled": true }
           }]' "$config_file" > "${config_file}.tmp" && mv "${config_file}.tmp" "$config_file"
    fi
    
    # 添加飞书绑定
    if ! jq -e ".bindings[] | select(.agentId == \"$AGENT_NAME\")" "$config_file" > /dev/null 2>&1; then
        jq --arg agent "$AGENT_NAME" \
           --arg chat "$FEISHU_CHAT_ID" \
           '.bindings += [{
               "agentId": $agent,
               "match": {
                 "channel": "feishu",
                 "peer": {
                   "kind": "group",
                   "id": $chat
                 }
               }
           }]' "$config_file" > "${config_file}.tmp" && mv "${config_file}.tmp" "$config_file"
    fi
    
    print_success "OpenClaw配置更新完成"
}

# 验证配置
validate_configuration() {
    print_info "验证配置..."
    
    # 检查工作空间文件
    local required_files=("AGENT.md" "IDENTITY.md" "SOUL.md" "TOOLS.md" "USER.md")
    for file in "${required_files[@]}"; do
        if [ ! -f "$WORKSPACE_DIR/$file" ]; then
            print_error "缺少必要文件: $WORKSPACE_DIR/$file"
            return 1
        fi
    done
    
    # 检查OpenClaw配置
    if ! jq -e ".agents.list[] | select(.id == \"$AGENT_NAME\")" "$HOME/.openclaw/openclaw.json" > /dev/null 2>&1; then
        print_error "Agent配置未正确添加到OpenClaw"
        return 1
    fi
    
    # 检查飞书绑定
    if ! jq -e ".bindings[] | select(.agentId == \"$AGENT_NAME\")" "$HOME/.openclaw/openclaw.json" > /dev/null 2>&1; then
        print_error "飞书绑定配置未正确添加"
        return 1
    fi
    
    print_success "配置验证通过"
    return 0
}

# 创建完成报告
create_completion_report() {
    cat << EOF

╔══════════════════════════════════════════════════════════════╗
║                    🎉 HR大哥创建完成！                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  👔 Agent名称: $AGENT_NAME                                   ║
║  📝 显示名称: $DISPLAY_NAME                                  ║
║  🎨 主题颜色: $THEME_COLOR                                   ║
║  😊 Emoji: $EMOJI                                           ║
║  📁 工作空间: $WORKSPACE_DIR                                 ║
║  📱 飞书群聊: $FEISHU_CHAT_ID                                ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                     🚀 下一步操作                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  1. 重启OpenClaw Gateway应用配置:                            ║
║     \$ openclaw gateway restart                              ║
║                                                              ║
║  2. 启动HR大哥Agent:                                         ║
║     \$ openclaw agent start $AGENT_NAME                       ║
║                                                              ║
║  3. 验证状态:                                                ║
║     \$ openclaw agent status $AGENT_NAME                      ║
║                                                              ║
║  4. 在飞书群聊中测试:                                        ║
║     @$DISPLAY_NAME 创建一个数据分析Agent                     ║
║                                                              ║
║  5. 查看日志:                                                ║
║     \$ tail -f $WORKSPACE_DIR/logs/agent.log                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📋 配置文件位置:
  - OpenClaw配置: ~/.openclaw/openclaw.json
  - 工作空间: $WORKSPACE_DIR
  - 配置备份: $HOME/.openclaw/openclaw.json.backup.*

🔧 如需修改配置:
  1. 编辑工作空间中的配置文件
  2. 更新OpenClaw配置
  3. 重启Gateway服务

📞 技术支持:
  - 查看skill文档获取完整指导
  - 在飞书群聊中@$DISPLAY_NAME
  - 查看日志文件排查问题

👔 $DISPLAY_NAME语录:
  "兄弟，要什么Agent？直说！我给你整得明明白白的。"
  "配置这块儿咱得说清楚，别后面出问题。"
  "正在搞，马上好。有问题随时喊我！"

创建时间: $(date)
脚本版本: v1.0.0
EOF
}

# 主函数
main() {
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -n|--name)
                AGENT_NAME="$2"
                shift 2
                ;;
            -d|--display)
                DISPLAY_NAME="$2"
                shift 2
                ;;
            -c|--color)
                THEME_COLOR="$2"
                shift 2
                ;;
            -e|--emoji)
                EMOJI="$2"
                shift 2
                ;;
            -w|--workspace)
                WORKSPACE_DIR="$2"
                shift 2
                ;;
            -f|--feishu)
                FEISHU_CHAT_ID="$2"
                shift 2
                ;;
            -i|--interactive)
                INTERACTIVE=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                print_error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 检查依赖
    check_dependencies || exit 1
    
    # 交互模式或验证必要参数
    if [ "$INTERACTIVE" = true ]; then
        collect_info_interactive
    else
        # 非交互模式必须提供飞书群聊ID
        if [ -z "$FEISHU_CHAT_ID" ]; then
            print_error "非交互模式必须提供飞书群聊ID (-f/--feishu)"
            show_help
            exit 1
        fi
        
        # 验证飞书群聊ID
        validate_feishu_id "$FEISHU_CHAT_ID" || exit 1
    fi
    
    # 展开工作空间路径中的~符号
    WORKSPACE_DIR="${WORKSPACE_DIR/#\~/$HOME}"
    
    # 执行创建步骤
    print_info "开始创建HR大哥Agent: $DISPLAY_NAME"
    echo ""
    
    create_workspace
    create_config_files
    update_openclaw_config
    validate_configuration
    
    # 显示完成报告
    create_completion_report
    
    print_success "HR大哥Agent创建流程完成！"
    print_info "请按照报告中的步骤完成后续操作。"
}

# 运行主函数
main "$@"
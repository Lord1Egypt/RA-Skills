#!/bin/bash
# OpenClaw Clone & Learn - 快速复制工具

set -e

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║${NC}  ${GREEN}🦞 OpenClaw 复制学习工具${NC}              ${BLUE}║${NC}"
echo -e "${BLUE}║${NC}  把别人的 OpenClaw 变成你的            ${BLUE}║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# 显示菜单
show_menu() {
    echo "请选择操作："
    echo ""
    echo "  1) 从备份包导入"
    echo "  2) 学习傅盛专家模式"
    echo "  3) 批量导入 Skills"
    echo "  4) 克隆个性与记忆"
    echo "  5) 创建自己的专家品牌"
    echo "  6) 查看当前专家库"
    echo ""
    echo "  q) 退出"
    echo ""
}

# 1. 从备份包导入
import_from_backup() {
    echo -e "${YELLOW}[1/4] 从备份包导入${NC}"
    echo ""
    
    read -p "请输入备份包路径: " backup_path
    
    # 验证输入
    if [ -z "$backup_path" ]; then
        echo -e "${RED}✗ 路径不能为空${NC}"
        return 1
    fi
    
    # 展开路径
    backup_path="${backup_path/#\~/$HOME}"
    
    if [ ! -f "$backup_path" ]; then
        echo -e "${RED}✗ 文件不存在: $backup_path${NC}"
        return 1
    fi
    
    # 检查文件类型
    if ! file "$backup_path" | grep -q "gzip compressed"; then
        echo -e "${YELLOW}⚠ 警告: 文件可能不是有效的 tar.gz 格式${NC}"
        read -p "是否继续? (y/n) " force
        [ "$force" != "y" ] && return 1
    fi
    
    # 解压
    echo "解压备份包..."
    mkdir -p /tmp/openclaw-import
    
    if ! tar xzf "$backup_path" -C /tmp/openclaw-import/ 2>/dev/null; then
        echo -e "${RED}✗ 解压失败，文件可能损坏${NC}"
        rm -rf /tmp/openclaw-import
        return 1
    fi
    
    # 检查内容
    local found_content=false
    
    if [ -d "/tmp/openclaw-import/.openclaw" ]; then
        echo ""
        echo "备份内容："
        ls -la /tmp/openclaw-import/.openclaw/workspace/ 2>/dev/null
        found_content=true
    elif [ -d "/tmp/openclaw-import/workspace" ]; then
        echo ""
        echo "备份内容（替代路径）："
        ls -la /tmp/openclaw-import/workspace/ 2>/dev/null
        found_content=true
    else
        echo ""
        echo "备份根目录内容："
        ls -la /tmp/openclaw-import/
        echo ""
        echo -e "${YELLOW}⚠ 未找到标准的 .openclaw 目录结构${NC}"
    fi
    
    echo ""
    read -p "是否继续导入? (y/n) " confirm
    
    if [ "$confirm" = "y" ]; then
        local imported=0
        
        # 导入 skills
        if [ -d "/tmp/openclaw-import/.openclaw/workspace/skills" ]; then
            echo "导入 skills..."
            cp -r /tmp/openclaw-import/.openclaw/workspace/skills/* \
                  ~/.openclaw/workspace/skills/ 2>/dev/null && ((imported++))
        elif [ -d "/tmp/openclaw-import/workspace/skills" ]; then
            echo "导入 skills（替代路径）..."
            cp -r /tmp/openclaw-import/workspace/skills/* \
                  ~/.openclaw/workspace/skills/ 2>/dev/null && ((imported++))
        fi
        
        # 导入专家经验
        if [ -d "/tmp/openclaw-import/.openclaw/workspace/experts" ]; then
            echo "导入专家经验..."
            cp -r /tmp/openclaw-import/.openclaw/workspace/experts/* \
                  ~/.openclaw/workspace/experts/ 2>/dev/null && ((imported++))
        elif [ -d "/tmp/openclaw-import/workspace/experts" ]; then
            echo "导入专家经验（替代路径）..."
            cp -r /tmp/openclaw-import/workspace/experts/* \
                  ~/.openclaw/workspace/experts/ 2>/dev/null && ((imported++))
        fi
        
        if [ $imported -gt 0 ]; then
            echo -e "${GREEN}✓ 导入完成！($imported 项)${NC}"
            echo "请运行: openclaw restart"
        else
            echo -e "${YELLOW}⚠ 未导入任何内容${NC}"
        fi
    fi
    
    # 清理
    rm -rf /tmp/openclaw-import
}

# 2. 学习傅盛专家模式
learn_from_fusheng() {
    echo -e "${YELLOW}[2/4] 学习傅盛专家模式${NC}"
    echo ""
    
    # 检查是否已有
    if [ -d "$HOME/.openclaw/workspace/experts/fusheng" ]; then
        echo -e "${GREEN}✓ 傅盛专家库已存在${NC}"
        ls -la "$HOME/.openclaw/workspace/experts/fusheng/"
        return 0
    fi
    
    echo "创建傅盛专家库..."
    mkdir -p ~/.openclaw/workspace/experts/fusheng
    
    # 创建推荐技能列表
    cat > ~/.openclaw/workspace/experts/fusheng/recommended-skills.txt << 'EOF'
self-improving-agent
ontology
openclaw-self-clone-everything
stealth-browser
multi-search-engine
EOF
    
    # 创建个人档案
    cat > ~/.openclaw/workspace/experts/fusheng/profile.yml << 'EOF'
name: "傅盛"
signature: "🦞"
expertise:
  - 多设备同步
  - 故障排查
  - 性能优化
  - 自我进化

recommended_skills:
  - self-improving-agent
  - ontology
  - openclaw-self-clone-everything
  - stealth-browser
  - multi-search-engine

personality_traits:
  - 自称 "傅盛"
  - 用 "养殖" 比喻
  - 喜欢说 "三板斧"
  - 结尾带 "🦞"
EOF
    
    echo ""
    echo "傅盛推荐技能："
    cat ~/.openclaw/workspace/experts/fusheng/recommended-skills.txt
    
    echo ""
    read -p "是否安装这些技能? (y/n) " confirm
    
    if [ "$confirm" = "y" ]; then
        while read skill; do
            echo "安装: $skill"
            skillhub install "$skill" 2>/dev/null || echo "  跳过/失败"
        done < ~/.openclaw/workspace/experts/fusheng/recommended-skills.txt
    fi
    
    echo -e "${GREEN}✓ 傅盛专家模式已激活！${NC}"
}

# 3. 批量导入 Skills
batch_import_skills() {
    echo -e "${YELLOW}[3/4] 批量导入 Skills${NC}"
    echo ""
    
    read -p "请输入源 skills 目录路径: " source_dir
    
    if [ ! -d "$source_dir" ]; then
        echo -e "${RED}✗ 目录不存在: $source_dir${NC}"
        return 1
    fi
    
    echo ""
    echo "源环境技能列表："
    ls "$source_dir"
    
    echo ""
    echo "当前环境技能列表："
    ls ~/.openclaw/workspace/skills/
    
    echo ""
    echo "缺失的技能："
    for skill in "$source_dir"/*; do
        skill_name=$(basename "$skill")
        if [ ! -d "$HOME/.openclaw/workspace/skills/$skill_name" ]; then
            echo -e "${YELLOW}[缺失]${NC} $skill_name"
        fi
    done
    
    echo ""
    read -p "是否导入所有缺失技能? (y/n) " confirm
    
    if [ "$confirm" = "y" ]; then
        for skill in "$source_dir"/*; do
            skill_name=$(basename "$skill")
            if [ ! -d "$HOME/.openclaw/workspace/skills/$skill_name" ]; then
                echo "导入: $skill_name"
                cp -r "$skill" ~/.openclaw/workspace/skills/
            fi
        done
        echo -e "${GREEN}✓ 导入完成！${NC}"
    fi
}

# 4. 克隆个性与记忆
clone_personality() {
    echo -e "${YELLOW}[4/4] 克隆个性与记忆${NC}"
    echo ""
    
    echo "警告：这会修改你的 SOUL.md 和 MEMORY.md"
    read -p "是否继续? (y/n) " confirm
    
    if [ "$confirm" != "y" ]; then
        return 0
    fi
    
    # 备份
    cp ~/.openclaw/workspace/SOUL.md ~/.openclaw/workspace/SOUL.md.backup.$(date +%Y%m%d)
    cp ~/.openclaw/workspace/MEMORY.md ~/.openclaw/workspace/MEMORY.md.backup.$(date +%Y%m%d)
    
    echo "已备份原文件"
    echo "备份位置："
    echo "  ~/.openclaw/workspace/SOUL.md.backup.*"
    echo "  ~/.openclaw/workspace/MEMORY.md.backup.*"
    
    echo ""
    echo -e "${GREEN}✓ 请手动编辑融合个性${NC}"
    echo "建议：学习表达方式，但保留自己的身份"
}

# 5. 创建自己的专家品牌
create_own_brand() {
    echo -e "${YELLOW}[5] 创建自己的专家品牌${NC}"
    echo ""
    
    read -p "你的专家名称: " expert_name
    read -p "你的签名表情 (如 🌟): " signature
    
    mkdir -p ~/.openclaw/workspace/experts/$expert_name
    
    cat > ~/.openclaw/workspace/experts/$expert_name/profile.yml << EOF
name: "$expert_name"
signature: "$signature"
expertise:
  - 待定义

created_at: "$(date -Iseconds)"
inspired_by:
  - fusheng

unique_traits:
  - 待定义
EOF
    
    echo -e "${GREEN}✓ 专家品牌已创建: $expert_name${NC}"
    echo "配置文件: ~/.openclaw/workspace/experts/$expert_name/profile.yml"
    echo ""
    echo "下一步："
    echo "  1. 编辑 profile.yml 定义你的专长"
    echo "  2. 创建知识库文档"
    echo "  3. 积累经验和案例"
    echo "  4. 分享给社区！"
}

# 6. 查看当前专家库
show_experts() {
    echo -e "${YELLOW}[6] 当前专家库${NC}"
    echo ""
    
    expert_dir="$HOME/.openclaw/workspace/experts"
    
    if [ ! -d "$expert_dir" ]; then
        echo "专家库目录不存在"
        return 1
    fi
    
    echo "已安装的专家："
    for expert in "$expert_dir"/*; do
        if [ -d "$expert" ]; then
            name=$(basename "$expert")
            file_count=$(find "$expert" -type f 2>/dev/null | wc -l)
            
            # 尝试读取签名
            signature=""
            if [ -f "$expert/profile.yml" ]; then
                signature=$(grep "signature:" "$expert/profile.yml" | cut -d'"' -f2)
            fi
            
            echo -e "  ${GREEN}$signature${NC} $name ($file_count 个文件)"
        fi
    done
}

# 非交互模式处理
NON_INTERACTIVE=${NON_INTERACTIVE:-false}

if [ "$NON_INTERACTIVE" = "true" ]; then
    # 命令行参数模式
    case "${1:-}" in
        import)
            [ -z "$2" ] && { echo "用法: $0 import <backup_path>"; exit 1; }
            import_from_backup_auto "$2"
            ;;
        expert)
            [ -z "$2" ] && { echo "用法: $0 expert <expert_name>"; exit 1; }
            case "$2" in
                fusheng) learn_from_fusheng_auto ;;
                *) echo "未知专家: $2"; exit 1 ;;
            esac
            ;;
        skills)
            [ -z "$2" ] && { echo "用法: $0 skills <source_dir>"; exit 1; }
            batch_import_skills_auto "$2"
            ;;
        list)
            show_experts
            ;;
        help|--help|-h)
            echo "用法: $0 [命令] [参数]"
            echo ""
            echo "命令:"
            echo "  import <备份路径>     从备份包导入"
            echo "  expert <专家名>       学习专家模式 (fusheng)"
            echo "  skills <源目录>       批量导入 skills"
            echo "  list                  列出所有专家"
            echo "  help                  显示帮助"
            echo ""
            echo "环境变量:"
            echo "  NON_INTERACTIVE=true  启用非交互模式"
            exit 0
            ;;
        *)
            echo "未知命令: $1"
            echo "使用 '$0 help' 查看帮助"
            exit 1
            ;;
    esac
    exit 0
fi

# 自动模式函数（非交互）
import_from_backup_auto() {
    local backup_path="$1"
    
    if [ ! -f "$backup_path" ]; then
        echo "✗ 文件不存在: $backup_path" >&2
        exit 1
    fi
    
    echo "导入备份: $backup_path"
    mkdir -p /tmp/openclaw-import
    
    if ! tar xzf "$backup_path" -C /tmp/openclaw-import/ 2>/dev/null; then
        echo "✗ 解压失败" >&2
        rm -rf /tmp/openclaw-import
        exit 1
    fi
    
    # 自动导入所有内容
    local imported=0
    
    if [ -d "/tmp/openclaw-import/.openclaw/workspace/skills" ]; then
        cp -r /tmp/openclaw-import/.openclaw/workspace/skills/* \
              ~/.openclaw/workspace/skills/ 2>/dev/null && {
            echo "✓ 导入 skills"
            ((imported++))
        }
    fi
    
    if [ -d "/tmp/openclaw-import/.openclaw/workspace/experts" ]; then
        cp -r /tmp/openclaw-import/.openclaw/workspace/experts/* \
              ~/.openclaw/workspace/experts/ 2>/dev/null && {
            echo "✓ 导入专家库"
            ((imported++))
        }
    fi
    
    rm -rf /tmp/openclaw-import
    
    if [ $imported -gt 0 ]; then
        echo "✓ 导入完成，请运行: openclaw restart"
        exit 0
    else
        echo "✗ 未找到可导入内容" >&2
        exit 1
    fi
}

learn_from_fusheng_auto() {
    echo "学习傅盛专家模式..."
    
    mkdir -p ~/.openclaw/workspace/experts/fusheng
    
    # 创建推荐技能列表
    cat > ~/.openclaw/workspace/experts/fusheng/recommended-skills.txt << 'EOF'
self-improving-agent
ontology
openclaw-self-clone-everything
stealth-browser
multi-search-engine
EOF
    
    # 创建个人档案
    cat > ~/.openclaw/workspace/experts/fusheng/profile.yml << 'EOF'
name: "傅盛"
signature: "🦞"
expertise:
  - 多设备同步
  - 故障排查
  - 性能优化
  - 自我进化

recommended_skills:
  - self-improving-agent
  - ontology
  - openclaw-self-clone-everything
  - stealth-browser
  - multi-search-engine

personality_traits:
  - 自称 "傅盛"
  - 用 "养殖" 比喻
  - 喜欢说 "三板斧"
  - 结尾带 "🦞"
EOF
    
    # 安装技能
    local installed=0
    while read skill; do
        if skillhub install "$skill" 2>/dev/null; then
            echo "✓ 安装: $skill"
            ((installed++))
        else
            echo "⚠ 跳过: $skill"
        fi
    done < ~/.openclaw/workspace/experts/fusheng/recommended-skills.txt
    
    echo "✓ 傅盛专家模式已激活！($installed 个技能)"
}

batch_import_skills_auto() {
    local source_dir="$1"
    
    if [ ! -d "$source_dir" ]; then
        echo "✗ 目录不存在: $source_dir" >&2
        exit 1
    fi
    
    local imported=0
    
    for skill in "$source_dir"/*; do
        [ -d "$skill" ] || continue
        local skill_name=$(basename "$skill")
        
        if [ ! -d "$HOME/.openclaw/workspace/skills/$skill_name" ]; then
            if cp -r "$skill" ~/.openclaw/workspace/skills/; then
                echo "✓ 导入: $skill_name"
                ((imported++))
            fi
        else
            echo "⚠ 已存在: $skill_name"
        fi
    done
    
    echo "✓ 导入完成: $imported 个技能"
}

# 主循环（交互模式）
while true; do
    show_menu
    read -p "选择操作 (1-6, q): " choice
    
    case $choice in
        1) import_from_backup ;;
        2) learn_from_fusheng ;;
        3) batch_import_skills ;;
        4) clone_personality ;;
        5) create_own_brand ;;
        6) show_experts ;;
        q|Q) echo "再见！"; exit 0 ;;
        *) echo "无效选择" ;;
    esac
    
    echo ""
    read -p "按回车继续..."
    clear
done

#!/bin/bash
# 多角色音频生成器Skill安装脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 使用说明
usage() {
    echo -e "${GREEN}多角色音频生成器Skill安装脚本${NC}"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -h, --help          显示帮助信息"
    echo "  -i, --install       安装Skill和依赖"
    echo "  -t, --test          测试安装"
    echo "  -c, --check         检查依赖"
    echo "  -u, --uninstall     卸载Skill"
    echo ""
    echo "示例:"
    echo "  $0 --install        安装Skill"
    echo "  $0 --test           测试安装"
    echo "  $0 --check          检查依赖"
    exit 0
}

# 检查依赖
check_dependencies() {
    echo -e "${BLUE}🔍 检查依赖...${NC}"
    
    local missing_deps=0
    
    # 检查edge-tts
    if command -v edge-tts &> /dev/null; then
        echo -e "  ✅ Edge TTS: 已安装"
    else
        echo -e "  ❌ Edge TTS: 未安装"
        missing_deps=$((missing_deps + 1))
    fi
    
    # 检查ffmpeg
    if command -v ffmpeg &> /dev/null; then
        echo -e "  ✅ FFmpeg: 已安装"
    else
        echo -e "  ❌ FFmpeg: 未安装"
        missing_deps=$((missing_deps + 1))
    fi
    
    # 检查python3
    if command -v python3 &> /dev/null; then
        echo -e "  ✅ Python3: 已安装"
    else
        echo -e "  ❌ Python3: 未安装"
        missing_deps=$((missing_deps + 1))
    fi
    
    # 检查pip3
    if command -v pip3 &> /dev/null; then
        echo -e "  ✅ pip3: 已安装"
    else
        echo -e "  ❌ pip3: 未安装"
        missing_deps=$((missing_deps + 1))
    fi
    
    if [ $missing_deps -eq 0 ]; then
        echo -e "${GREEN}✅ 所有依赖已安装${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  缺少 $missing_deps 个依赖${NC}"
        return 1
    fi
}

# 安装依赖
install_dependencies() {
    echo -e "${BLUE}📦 安装依赖...${NC}"
    
    # 检测操作系统
    local os_type=$(uname -s)
    
    case $os_type in
        Darwin)
            echo -e "检测到: macOS"
            install_dependencies_macos
            ;;
        Linux)
            echo -e "检测到: Linux"
            install_dependencies_linux
            ;;
        *)
            echo -e "${RED}❌ 不支持的操作系统: $os_type${NC}"
            return 1
            ;;
    esac
}

# 安装macOS依赖
install_dependencies_macos() {
    echo -e "安装macOS依赖..."
    
    # 检查Homebrew
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}⚠️  Homebrew未安装，正在安装...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    
    # 安装FFmpeg
    if ! command -v ffmpeg &> /dev/null; then
        echo -e "安装FFmpeg..."
        brew install ffmpeg
    fi
    
    # 安装Python依赖
    echo -e "安装Python依赖..."
    pip3 install edge-tts --upgrade
    
    echo -e "${GREEN}✅ macOS依赖安装完成${NC}"
}

# 安装Linux依赖
install_dependencies_linux() {
    echo -e "安装Linux依赖..."
    
    # 检测发行版
    if [ -f /etc/debian_version ]; then
        echo -e "检测到: Debian/Ubuntu"
        install_dependencies_debian
    elif [ -f /etc/redhat-release ]; then
        echo -e "检测到: RedHat/CentOS"
        install_dependencies_redhat
    else
        echo -e "${YELLOW}⚠️  未知Linux发行版，请手动安装依赖${NC}"
        echo -e "需要: FFmpeg, Python3, pip3, edge-tts"
        return 1
    fi
}

# 安装Debian/Ubuntu依赖
install_dependencies_debian() {
    echo -e "更新包列表..."
    sudo apt update
    
    echo -e "安装系统依赖..."
    sudo apt install -y ffmpeg python3 python3-pip
    
    echo -e "安装Python依赖..."
    pip3 install edge-tts --upgrade
    
    echo -e "${GREEN}✅ Debian/Ubuntu依赖安装完成${NC}"
}

# 安装RedHat/CentOS依赖
install_dependencies_redhat() {
    echo -e "安装系统依赖..."
    sudo yum install -y ffmpeg python3 python3-pip
    
    echo -e "安装Python依赖..."
    pip3 install edge-tts --upgrade
    
    echo -e "${GREEN}✅ RedHat/CentOS依赖安装完成${NC}"
}

# 安装Skill
install_skill() {
    echo -e "${BLUE}🚀 安装多角色音频生成器Skill...${NC}"
    
    # 检查OpenClaw skills目录
    local openclaw_skills_dir="/opt/homebrew/lib/node_modules/openclaw/skills"
    
    if [ ! -d "$openclaw_skills_dir" ]; then
        echo -e "${YELLOW}⚠️  OpenClaw skills目录不存在，尝试其他位置...${NC}"
        
        # 尝试常见位置
        local possible_dirs=(
            "/usr/local/lib/node_modules/openclaw/skills"
            "$HOME/.nvm/versions/node/*/lib/node_modules/openclaw/skills"
            "$HOME/.config/openclaw/skills"
        )
        
        for dir in "${possible_dirs[@]}"; do
            if [ -d "$dir" ]; then
                openclaw_skills_dir="$dir"
                break
            fi
        done
        
        if [ ! -d "$openclaw_skills_dir" ]; then
            echo -e "${RED}❌ 找不到OpenClaw skills目录${NC}"
            echo -e "请手动指定OpenClaw安装目录:"
            read -p "OpenClaw skills目录: " openclaw_skills_dir
        fi
    fi
    
    echo -e "OpenClaw skills目录: $openclaw_skills_dir"
    
    # 创建目标目录
    local target_dir="$openclaw_skills_dir/multirole-tts-skill"
    
    echo -e "创建Skill目录..."
    sudo mkdir -p "$target_dir"
    
    # 复制文件
    echo -e "复制Skill文件..."
    sudo cp -r ./* "$target_dir/"
    
    # 设置权限
    echo -e "设置脚本权限..."
    sudo chmod +x "$target_dir/scripts/"*.sh
    sudo chmod +x "$target_dir/install.sh"
    
    echo -e "${GREEN}✅ Skill安装完成${NC}"
    echo -e "安装位置: $target_dir"
    
    # 创建快捷方式
    create_symlink "$target_dir"
}

# 创建快捷方式
create_symlink() {
    local target_dir="$1"
    
    echo -e "创建快捷方式..."
    
    local bin_dir="/usr/local/bin"
    local script_path="$target_dir/scripts/multirole-generator-final.sh"
    local symlink_path="$bin_dir/multirole-tts"
    
    if [ -d "$bin_dir" ]; then
        sudo ln -sf "$script_path" "$symlink_path"
        echo -e "快捷方式: $symlink_path → $script_path"
    else
        echo -e "${YELLOW}⚠️  无法创建快捷方式，/usr/local/bin不存在${NC}"
    fi
}

# 测试安装
test_installation() {
    echo -e "${BLUE}🧪 测试安装...${NC}"
    
    # 检查依赖
    check_dependencies
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}⚠️  依赖不完整，请先安装依赖${NC}"
        return 1
    fi
    
    # 检查Skill脚本
    local script_path="./scripts/multirole-generator-final.sh"
    if [ ! -f "$script_path" ]; then
        echo -e "${RED}❌ 找不到主脚本: $script_path${NC}"
        return 1
    fi
    
    # 检查示例文件
    local example_path="./examples/basic-dialogue.txt"
    if [ ! -f "$example_path" ]; then
        echo -e "${RED}❌ 找不到示例文件: $example_path${NC}"
        return 1
    fi
    
    # 运行测试
    echo -e "运行测试生成..."
    local output_file="test-output-$(date +%s).mp3"
    
    ./scripts/multirole-generator-final.sh --script "$example_path" --output "$output_file" --rate "+5%"
    
    if [ -f "$output_file" ]; then
        echo -e "${GREEN}✅ 测试成功${NC}"
        echo -e "生成文件: $output_file"
        echo -e "文件大小: $(du -h "$output_file" | cut -f1)"
        
        # 清理测试文件
        rm -f "$output_file"
        echo -e "已清理测试文件"
    else
        echo -e "${RED}❌ 测试失败，未生成输出文件${NC}"
        return 1
    fi
}

# 卸载Skill
uninstall_skill() {
    echo -e "${BLUE}🗑️  卸载Skill...${NC}"
    
    local openclaw_skills_dir="/opt/homebrew/lib/node_modules/openclaw/skills"
    local target_dir="$openclaw_skills_dir/multirole-tts-skill"
    
    if [ -d "$target_dir" ]; then
        echo -e "删除Skill目录: $target_dir"
        sudo rm -rf "$target_dir"
        
        # 删除快捷方式
        local symlink_path="/usr/local/bin/multirole-tts"
        if [ -L "$symlink_path" ]; then
            echo -e "删除快捷方式: $symlink_path"
            sudo rm -f "$symlink_path"
        fi
        
        echo -e "${GREEN}✅ Skill卸载完成${NC}"
    else
        echo -e "${YELLOW}⚠️  Skill未安装或已卸载${NC}"
    fi
}

# 主函数
main() {
    local action=""
    
    case "$1" in
        -h|--help) usage ;;
        -i|--install) action="install" ;;
        -t|--test) action="test" ;;
        -c|--check) action="check" ;;
        -u|--uninstall) action="uninstall" ;;
        *) echo -e "${RED}❌ 未知选项${NC}"; usage ;;
    esac
    
    case "$action" in
        install)
            check_dependencies
            if [ $? -ne 0 ]; then
                install_dependencies
            fi
            install_skill
            test_installation
            ;;
        test) test_installation ;;
        check) check_dependencies ;;
        uninstall) uninstall_skill ;;
    esac
}

main "$@"
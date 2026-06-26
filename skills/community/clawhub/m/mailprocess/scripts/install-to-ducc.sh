#!/bin/bash

# Mali App Builder Skill - ducc 安装脚本
# 用于快速将 Skill 安装到 ducc 平台

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 获取脚本所在目录和项目根目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Mali App Builder Skill - ducc 安装向导${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📂 项目根目录: $PROJECT_ROOT${NC}"
echo ""

# 检查文件是否存在
check_files() {
    echo -e "${BLUE}📋 检查必需文件...${NC}"
    
    cd "$PROJECT_ROOT" || exit 1
    
    required_files=(
        "SKILL.md"
        "scripts/launch-mali-builder.py"
        "scripts/launch-mali-builder.sh"
    )
    
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            echo -e "${GREEN}  ✅ $file${NC}"
        else
            echo -e "${RED}  ❌ $file 未找到${NC}"
            exit 1
        fi
    done
    echo ""
}

# 询问安装方式
select_installation_method() {
    echo -e "${BLUE}📦 请选择安装方式:${NC}"
    echo "  1) 通过 ducc CLI (推荐)"
    echo "  2) 手动上传到 ducc 管理界面"
    echo "  3) 生成配置文件，稍后安装"
    echo ""
    read -p "请选择 (1-3): " method
    echo ""
    
    case $method in
        1)
            install_via_cli
            ;;
        2)
            install_manual
            ;;
        3)
            generate_config
            ;;
        *)
            echo -e "${RED}❌ 无效选择${NC}"
            exit 1
            ;;
    esac
}

# 方法 1: 通过 CLI 安装
install_via_cli() {
    echo -e "${BLUE}🚀 通过 ducc CLI 安装...${NC}"
    
    # 检查 ducc-cli 是否安装
    if ! command -v ducc-cli &> /dev/null; then
        echo -e "${RED}❌ ducc-cli 未安装${NC}"
        echo -e "${YELLOW}💡 请先安装 ducc-cli 工具${NC}"
        exit 1
    fi
    
    # 登录检查
    echo -e "${BLUE}🔐 检查登录状态...${NC}"
    if ! ducc-cli status &> /dev/null; then
        echo -e "${YELLOW}⚠️  未登录，请先登录${NC}"
        ducc-cli login
    fi
    
    cd "$PROJECT_ROOT" || exit 1
    
    # 创建 Skill
    echo -e "${BLUE}📝 创建 Skill...${NC}"
    ducc-cli skill create \
        --name "mali-builder" \
        --display-name "码力搭建助手" \
        --description "自动调用码力搭建平台完成应用搭建" \
        --version "1.0.0"
    
    # 上传文件
    echo -e "${BLUE}📤 上传文件...${NC}"
    ducc-cli skill upload mali-builder \
        --files SKILL.md scripts/launch-mali-builder.py scripts/launch-mali-builder.sh
    
    # 配置触发条件
    echo -e "${BLUE}⚙️  配置触发条件...${NC}"
    ducc-cli skill config mali-builder \
        --keywords "码力搭建,mali,低代码搭建,搭建应用" \
        --entry "scripts/launch-mali-builder.py"
    
    # 启用 Skill
    echo -e "${BLUE}✅ 启用 Skill...${NC}"
    ducc-cli skill enable mali-builder
    
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✅ Mali App Builder Skill 安装成功！${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}🧪 测试命令:${NC}"
    echo "  ducc-cli skill test mali-builder \"帮我搭建一个投票系统\""
    echo ""
}

# 方法 2: 手动安装指南
install_manual() {
    echo -e "${BLUE}📖 手动安装指南${NC}"
    echo ""
    echo -e "${YELLOW}请按照以下步骤操作:${NC}"
    echo ""
    echo "1. 打开 ducc 管理后台"
    echo "2. 进入 'Skill 管理' 页面"
    echo "3. 点击 '创建新 Skill'"
    echo ""
    echo "4. 填写基本信息:"
    echo "   - 名称: mali-builder"
    echo "   - 显示名称: 码力搭建助手"
    echo "   - 描述: 自动调用码力搭建平台完成应用搭建"
    echo "   - 版本: 1.0.0"
    echo ""
    echo "5. 上传以下文件:"
    echo "   - SKILL.md"
    echo "   - scripts/launch-mali-builder.py"
    echo "   - scripts/launch-mali-builder.sh"
    echo ""
    echo "6. 配置触发关键词:"
    echo "   - 码力搭建"
    echo "   - mali"
    echo "   - 低代码搭建"
    echo "   - 搭建应用"
    echo ""
    echo "7. 设置执行入口:"
    echo "   python3 scripts/launch-mali-builder.py \"\$USER_QUERY\""
    echo ""
    echo "8. 保存并启用 Skill"
    echo ""
    
    cd "$PROJECT_ROOT" || exit 1
    
    # 打包文件
    echo -e "${BLUE}📦 正在打包文件...${NC}"
    tar -czf mali-builder-skill.tar.gz \
        SKILL.md \
        scripts/
    
    echo -e "${GREEN}✅ 文件已打包: mali-builder-skill.tar.gz${NC}"
    echo -e "${BLUE}💡 可以直接上传这个压缩包到 ducc${NC}"
    echo ""
}

# 方法 3: 生成配置文件
generate_config() {
    echo -e "${BLUE}📝 生成配置文件...${NC}"
    
    cd "$PROJECT_ROOT" || exit 1
    
    # 生成 skill.yaml
    cat > skill.yaml <<EOF
# Mali App Builder Skill Configuration
skill:
  name: mali-builder
  version: 1.0.0
  display_name: 码力搭建助手
  description: 自动调用码力搭建平台完成应用搭建
  author: $(whoami)
  
  # 触发条件
  triggers:
    keywords:
      - 码力搭建
      - mali
      - 低代码搭建
      - 搭建应用
      - 创建应用
    
    patterns:
      - "帮我.*搭建.*"
      - "用.*搭建.*"
      - "创建.*应用.*"
  
  # 执行配置
  execution:
    type: script
    entry: scripts/launch-mali-builder.py
    interpreter: python3
    working_dir: .
    timeout: 30
    args:
      - "\$USER_QUERY"
    
  # 依赖
  dependencies:
    system:
      - python3
      - chrome
    python:
      - None  # 无额外 Python 依赖
    
  # 权限
  permissions:
    - browser_control
    - network_access
    - script_execution
    
  # 文件
  files:
    - SKILL.md
    - scripts/launch-mali-builder.py
    - scripts/launch-mali-builder.sh
    
  # 文档
  documentation:
    readme: SKILL.md
EOF
    
    echo -e "${GREEN}✅ 配置文件已生成: skill.yaml${NC}"
    echo ""
    echo -e "${BLUE}📖 使用方法:${NC}"
    echo "  ducc-cli skill install ./skill.yaml"
    echo ""
}

# 主函数
main() {
    check_files
    select_installation_method
}

main
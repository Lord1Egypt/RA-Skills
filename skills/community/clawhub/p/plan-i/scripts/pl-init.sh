#!/bin/bash

# ==============================================================================
# Script: pl-init.sh
# Description: 创建规划文件
# Usage: ./pl-init.sh <plan-name>
# ==============================================================================

# 配置
PLANS_DIR="plans"
DATE=$(date +%Y%m%d)
TIME=$(date +%H%M%S)


# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 函数：打印帮助信息
show_help() {
    echo -e "${YELLOW}用法:${NC} ./pl-init.sh <plan-name>"
    echo -e "  名称：必须填写名称"
}

# 主逻辑
main() {
    # 1. 检查参数
    if [ -z "$1" ]; then
        show_help
        exit 1
    fi

    if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
        show_help
        exit 0
    fi

    local plan_name="$1"

    # 2. 确保目录存在
    if [ ! -d "$PLANS_DIR/${DATE}" ]; then
        mkdir -p "$PLANS_DIR/${DATE}"
    fi

    local file_path="${PLANS_DIR}/${DATE}/${TIME}-${plan_name}.md"

    # 3. 检查文件是否存在
    if [ -f "$file_path" ]; then
        echo -e "${RED}错误：文件 '$file_path' 已存在${NC}"
        exit 1
    fi

    # 4. 创建文件并写入头部信息
    local datetime=$(date +"%Y-%m-%d %H:%M:%S")
    cat > "$file_path" <<EOF
# ${plan_name}

## 为什么

<!-- 解释此变更的动机。解决了什么问题？为什么现在做？ -->

## 变更内容

<!-- 描述将要变更的内容。具体说明新功能、修改或移除。 -->

## 功能 (Capabilities)

### 新增功能
<!-- 引入的新功能。将 <name> 替换为 kebab-case 标识符（例如：user-auth, data-export）。每个功能将创建 specs/<name>/spec.md -->

- `<name>`: <简要描述此功能涵盖的内容>

### 修改功能
<!-- 现有功能，其需求发生变更（不仅仅是实现）。
     仅当规范级行为发生变更时才在此列出。每个都需要一个增量规范文件。
     使用项目目录中 specs/ 的现有规范名称。如果没有需求变更，请留空。 -->

- `<existing-name>`: <什么需求正在变更>

## 影响

<!-- 受影响的代码、API、依赖项、系统 -->

## 待确认关键点

### 1. <!-- 待确认关键点 -->

- [ ] 1.1 <!-- 关键点描述 -->
- [ ] 1.2 <!-- 关键点描述 -->

### 2. <!-- 待确认关键点 -->

- [ ] 2.1 <!-- 关键点描述 -->
- [ ] 2.2 <!-- 关键点描述 -->

EOF
    echo -e "${GREEN}✓ 创建规划文件成功, 文件路径：$file_path${NC}"
}

main "$@"

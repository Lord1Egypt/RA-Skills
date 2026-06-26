#!/bin/bash
# OpenClaw 迁移验证脚本
# 用于验证版本迁移后的配置完整性和正确性

set -e

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 统计变量
PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_pass() {
    echo -e "${GREEN}[✓]${NC} $1"
    ((PASS_COUNT++))
}

log_fail() {
    echo -e "${RED}[✗]${NC} $1"
    ((FAIL_COUNT++))
}

log_warn() {
    echo -e "${YELLOW}[!]${NC} $1"
    ((WARN_COUNT++))
}

# 打印标题
print_header() {
    echo ""
    echo "=================================="
    echo "  $1"
    echo "=================================="
    echo ""
}

# 检查函数
check_file_exists() {
    local file=$1
    local description=$2

    if [ -f "$file" ]; then
        log_pass "$description 存在"
        return 0
    else
        log_fail "$description 缺失: $file"
        return 1
    fi
}

check_json_valid() {
    local file=$1
    local description=$2

    if python3 -m json.tool "$file" > /dev/null 2>&1; then
        log_pass "$description 格式正确"
        return 0
    else
        log_fail "$description 格式错误"
        return 1
    fi
}

check_required_fields() {
    local file=$1
    shift
    local fields=("$@")
    local missing=()

    for field in "${fields[@]}"; do
        if ! grep -q "\"$field\"" "$file"; then
            missing+=("$field")
        fi
    done

    if [ ${#missing[@]} -eq 0 ]; then
        log_pass "所有必需字段存在"
        return 0
    else
        log_fail "缺少必需字段: ${missing[*]}"
        return 1
    fi
}

# 主流程
main() {
    print_header "OpenClaw 迁移验证工具"

    # 1. 基础文件检查
    print_header "1. 基础文件检查"
    check_file_exists "_meta.json" "元数据文件"
    check_file_exists "SKILL.md" "技能文档"
    check_file_exists ".clawhub" "配置目录"

    if [ -d ".clawhub" ]; then
        log_pass "配置目录结构完整"
    else
        log_fail "配置目录缺失"
        exit 1
    fi

    # 2. JSON 格式验证
    print_header "2. JSON 格式验证"
    check_json_valid "_meta.json" "元数据文件"

    # 检查所有 JSON 文件
    local json_files=$(find .clawhub -name "*.json" 2>/dev/null || true)
    if [ -n "$json_files" ]; then
        local json_count=0
        local json_valid=0
        while IFS= read -r file; do
            ((json_count++))
            if python3 -m json.tool "$file" > /dev/null 2>&1; then
                ((json_valid++))
            else
                log_fail "JSON 格式错误: $file"
            fi
        done <<< "$json_files"

        if [ $json_valid -eq $json_count ]; then
            log_pass "所有 JSON 文件格式正确 ($json_valid/$json_count)"
        else
            log_fail "部分 JSON 文件格式错误 ($json_valid/$json_count)"
        fi
    else
        log_warn "未找到其他 JSON 文件"
    fi

    # 3. 必需字段检查
    print_header "3. 必需字段检查"

    # 使用 Python 检查 JSON 字段
    python3 << 'EOF'
import json
import sys

try:
    with open('_meta.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 检查版本字段
    if 'version' in data:
        print(f"✓ 版本字段: {data['version']}")
    else:
        print("✗ 缺少版本字段")
        sys.exit(1)

    # 检查名称字段
    if 'name' in data:
        print(f"✓ 名称字段: {data['name']}")
    else:
        print("✗ 缺少名称字段")
        sys.exit(1)

    # 检查 schemaVersion（如果存在）
    if 'schemaVersion' in data:
        print(f"✓ Schema版本: {data['schemaVersion']}")
    else:
        print("! 缺少 schemaVersion 字段（可选）")

    sys.exit(0)
except Exception as e:
    print(f"✗ 检查失败: {e}")
    sys.exit(1)
EOF

    if [ $? -eq 0 ]; then
        ((PASS_COUNT++))
    else
        ((FAIL_COUNT++))
    fi

    # 4. 权限检查
    print_header "4. 文件权限检查"

    if [ -r "_meta.json" ]; then
        log_pass "_meta.json 可读"
    else
        log_fail "_meta.json 不可读"
    fi

    if [ -w "_meta.json" ]; then
        log_pass "_meta.json 可写"
    else
        log_warn "_meta.json 不可写（可能不影响使用）"
    fi

    if [ -x ".clawhub" ]; then
        log_pass ".clawhub 可访问"
    else
        log_fail ".clawhub 不可访问"
    fi

    # 5. 备份检查
    print_header "5. 备份状态检查"

    backup_count=$(find .clawhub -type d -name "backup_*" 2>/dev/null | wc -l)
    if [ $backup_count -gt 0 ]; then
        log_pass "发现 $backup_count 个备份目录"
        log_info "最新备份:"
        find .clawhub -type d -name "backup_*" -printf "%T+ %p\n" 2>/dev/null | sort -r | head -1 | while read line; do
            echo "    $line"
        done
    else
        log_warn "未发现备份目录（建议在迁移前创建备份）"
    fi

    # 6. 版本兼容性检查（示例）
    print_header "6. 版本兼容性检查"

    python3 << 'EOF'
import json
import re

try:
    with open('_meta.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    version = data.get('version', 'unknown')

    # 简单的版本格式检查
    if re.match(r'^\d+\.\d+\.\d+', version):
        print(f"✓ 版本格式正确: {version}")
    else:
        print(f"! 版本格式非标准: {version}")

    # 检查是否为已知的破坏性版本
    major_version = int(version.split('.')[0]) if version.split('.')[0].isdigit() else 0

    if major_version >= 3:
        print("! 检测到主版本 3.x，可能需要特殊迁移步骤")

except Exception as e:
    print(f"✗ 版本检查失败: {e}")
EOF

    # 汇总报告
    print_header "验证汇总"
    echo -e "通过: ${GREEN}$PASS_COUNT${NC}"
    echo -e "警告: ${YELLOW}$WARN_COUNT${NC}"
    echo -e "失败: ${RED}$FAIL_COUNT${NC}"
    echo ""

    # 返回状态
    if [ $FAIL_COUNT -gt 0 ]; then
        echo -e "${RED}❌ 验证失败${NC}"
        echo "请修复上述错误后重试"
        exit 1
    elif [ $WARN_COUNT -gt 0 ]; then
        echo -e "${YELLOW}⚠️ 验证通过（有警告）${NC}"
        echo "建议检查警告项"
        exit 0
    else
        echo -e "${GREEN}✅ 验证通过${NC}"
        echo "配置迁移成功完成"
        exit 0
    fi
}

# 执行主流程
main "$@"

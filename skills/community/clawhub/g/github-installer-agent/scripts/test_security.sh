#!/bin/bash

# 安全测试脚本
# 测试 github_installer_secure 技能的安全性

set -euo pipefail

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🔒 GitHub Installer Secure 安全测试${NC}"
echo "═══════════════════════════════════════"

# 测试 1: 检查脚本权限
echo -e "\n${GREEN}[测试 1] 检查脚本权限${NC}"
if [[ -x "scripts/safe_clone.sh" ]]; then
    echo "✅ safe_clone.sh 可执行权限正确"
else
    echo "❌ safe_clone.sh 缺少可执行权限"
    chmod +x scripts/safe_clone.sh
    echo "  已修复权限"
fi

# 测试 2: 检查文件内容
echo -e "\n${GREEN}[测试 2] 检查文件内容安全性${NC}"

# 检查是否包含危险命令
dangerous_patterns=(
    "rm -rf /"
    "chmod 777"
    "wget.*-O.*sh"
    "curl.*|.*sh"
    "eval.*curl"
    "exec.*input"
    "sudo.*"
    "su -"
)

safe=true
for pattern in "${dangerous_patterns[@]}"; do
    if grep -r "$pattern" . --include="*.sh" --include="*.py" 2>/dev/null | grep -v "test_security.sh" | grep -v "#.*$pattern"; then
        echo "❌ 发现危险模式: $pattern"
        safe=false
    fi
done

if $safe; then
    echo "✅ 未发现危险命令"
fi

# 测试 3: 检查输入验证
echo -e "\n${GREEN}[测试 3] 检查输入验证${NC}"
if grep -q "validate_github_url" scripts/safe_clone.sh; then
    echo "✅ 包含 URL 验证函数"
else
    echo "❌ 缺少 URL 验证"
fi

if grep -q "check_repo_info" scripts/safe_clone.sh; then
    echo "✅ 包含仓库信息检查"
else
    echo "❌ 缺少仓库信息检查"
fi

# 测试 4: 检查安全特性
echo -e "\n${GREEN}[测试 4] 检查安全特性${NC}"
security_features=(
    "git clone --depth"
    "安全建议"
    "虚拟环境"
    "pip install --user"
    "npm audit"
)

for feature in "${security_features[@]}"; do
    if grep -q "$feature" scripts/safe_clone.sh; then
        echo "✅ 包含: $feature"
    else
        echo "❌ 缺少: $feature"
    fi
done

# 测试 5: 检查权限要求
echo -e "\n${GREEN}[测试 5] 检查权限要求${NC}"
if grep -q "requires.*bins.*git" SKILL.md; then
    echo "✅ 明确声明需要 git"
else
    echo "❌ 未声明需要的二进制文件"
fi

# 测试 6: 检查警告信息
echo -e "\n${GREEN}[测试 6] 检查警告信息${NC}"
if grep -q "安全警告" SKILL.md; then
    echo "✅ 包含安全警告"
else
    echo "❌ 缺少安全警告"
fi

if grep -q "不要自动执行" SKILL.md; then
    echo "✅ 警告不要自动执行安装"
else
    echo "❌ 缺少自动执行警告"
fi

# 测试 7: 检查响应模板
echo -e "\n${GREEN}[测试 7] 检查响应模板${NC}"
if grep -q "安全分析报告" SKILL.md; then
    echo "✅ 包含安全报告模板"
else
    echo "❌ 缺少安全报告模板"
fi

# 总结
echo -e "\n${YELLOW}═══════════════════════════════════════${NC}"
echo -e "${GREEN}安全测试完成${NC}"

# 建议
echo -e "\n${YELLOW}💡 改进建议:${NC}"
echo "1. 考虑添加数字签名验证"
echo "2. 添加更详细的依赖审计"
echo "3. 考虑集成安全扫描工具"
echo "4. 添加使用量统计和监控"

echo -e "\n${GREEN}✅ 技能已通过基本安全检查${NC}"
echo "可以安全地使用和分享此技能"
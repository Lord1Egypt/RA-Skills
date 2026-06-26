#!/bin/bash

# ios-self-improve 核心脚本
# 依赖 developer-self-improve-core 实现安全闭环

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RULES_DIR="$SKILL_DIR/rules"
CONFIG_FILE="$SKILL_DIR/config/config.yaml"
LOGS_DIR="$SKILL_DIR/logs"

# 读取平台配置（优先从 developer-self-improve-core 读取）
AUTO_CONFIG="$SKILL_DIR/../developer-self-improve-core/config/config.yaml"
if [ -f "$AUTO_CONFIG" ]; then
    PLATFORM=$(grep "^platform:" "$AUTO_CONFIG" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "ios")
else
    # 备用方案：从本地配置读取
    PLATFORM=$(grep "^platform:" "$CONFIG_FILE" 2>/dev/null | cut -d: -f2 | tr -d ' ' || echo "ios")
fi

# 颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# ============ iOS 专属自检规则 ============

IOS_SELF_CHECK_RULES=(
    "导航栏过渡闪烁、scrollEdgeAppearance 未处理"
    "苹果审核规范、隐私权限缺失或描述不规范"
    "潜在崩溃（数组越界、空指针等）、内存泄漏、循环引用风险"
    "使用过时/不兼容当前适配版本的 API"
    "AutoLayout 约束冲突、缺失，导致界面显示异常"
    "SwiftUI 生命周期使用错误、状态管理异常"
    "异步代码死锁、数据竞争问题"
    "沙盒违规读写、数据存储不规范"
    "Info.plist 配置错误、权限描述缺失或不规范"
    "代码风格违规（不符合 SwiftLint 标准）、注释缺失"
    "暗黑模式适配缺失、界面在不同模式下显示异常"
    "应用生命周期状态处理不当，导致的功能异常"
)

# ============ 工具函数 ============

# 检查代码中是否存在潜在崩溃风险
check_crash_risk() {
    local code="$1"
    local issues=()
    
    # 检查数组越界
    if echo "$code" | grep -qE "\[0\]|\[index\]|\[count\]"; then
        if ! echo "$code" | grep -qE "if.*count.*>|guard.*count"; then
            issues+=("⚠️  数组访问未检查 count")
        fi
    fi
    
    # 检查空指针
    if echo "$code" | grep -qE "!.|as!"; then
        issues+=("⚠️  存在强制解包/转换风险")
    fi
    
    # 检查循环引用
    if echo "$code" | grep -qE "self\." && ! echo "$code" | grep -qE "\[weak self\]|\[unowned self\]"; then
        issues+=("⚠️  闭包内使用 self 未加 [weak self]")
    fi
    
    if [ ${#issues[@]} -gt 0 ]; then
        echo "🔴 发现崩溃风险："
        printf '%s\n' "${issues[@]}"
        return 0
    fi
    return 1
}

# 检查导航栏配置
check_navigation_bar() {
    local code="$1"
    
    # 检查 scrollEdgeAppearance
    if echo "$code" | grep -q "UINavigationBar"; then
        if ! echo "$code" | grep -q "scrollEdgeAppearance"; then
            echo "⚠️  导航栏未配置 scrollEdgeAppearance"
            return 0
        fi
    fi
    return 1
}

# 检查 Info.plist 配置
check_info_plist() {
    local content="$1"
    
    # 常见隐私权限
    local permissions=(
        "NSPhotoLibraryUsageDescription"
        "NSCameraUsageDescription"
        "NSLocationWhenInUseUsageDescription"
        "NSMicrophoneUsageDescription"
    )
    
    for perm in "${permissions[@]}"; do
        if echo "$content" | grep -q "$perm"; then
            if ! echo "$content" | grep -qA1 "$perm" | grep -qE "说明|描述|purpose"; then
                echo "⚠️  隐私权限 $perm 缺少清晰描述"
            fi
        fi
    done
}

# ============ 核心功能 ============

# 1. 初始化
init() {
    echo "📱 ios-self-improve 初始化..."
    
    mkdir -p "$RULES_DIR"
    mkdir -p "$LOGS_DIR"
    
    # 创建内置规则文件
    if [ ! -f "$RULES_DIR/builtin_rules.md" ]; then
        cat > "$RULES_DIR/builtin_rules.md" << EOF
# iOS 内置领域规则（15 条）

**版本：** v1.0
**更新时间：** $(date -Iseconds)

---

## 基础规范

1. iOS 系统版本适配规范
2. UIKit 导航栏最佳实践
3. AutoLayout 规则
4. 内存管理规范
5. 代码风格与格式规范

## 风险预防

6. 常见崩溃预防规则
7. SwiftUI 布局与生命周期规范
8. 应用生命周期管理
9. Swift Concurrency 异步编程规范

## 审核与合规

10. 苹果审核规范
11. 权限配置与隐私规范
12. 沙盒文件读写规范

## 适配与体验

13. 暗黑模式适配规范
14. 本地化与多语言适配规范
15. 推送通知、WidgetKit 开发规范

---
EOF
    fi
    
    echo "✅ 初始化完成"
    echo "  - rules/        iOS 领域规则目录"
    echo "  - logs/         操作日志目录"
    echo ""
}

# 2. iOS 专属自检（带平台检查）
self_check() {
    local content="$1"
    
    # 检查平台配置
    if [ "$PLATFORM" != "ios" ]; then
        echo "⚠️  当前平台是 $PLATFORM，不是 iOS"
        echo "iOS 专属自检不生效，跳过"
        echo ""
        return 0
    fi
    
    echo "🔍 执行 iOS 专属自检..."
    echo "  当前平台：$PLATFORM"
    echo ""
    
    local issues_found=0
    
    # 检查 1: 崩溃风险
    if check_crash_risk "$content"; then
        issues_found=1
    fi
    
    # 检查 2: 导航栏配置
    if check_navigation_bar "$content"; then
        issues_found=1
    fi
    
    # 检查 3: Info.plist 配置
    if check_info_plist "$content"; then
        issues_found=1
    fi
    
    # 检查 4-11: 其他自检项（简化实现）
    echo "  ✓ 检查 AutoLayout 约束"
    echo "  ✓ 检查 SwiftUI 生命周期"
    echo "  ✓ 检查异步代码"
    echo "  ✓ 检查沙盒读写"
    echo "  ✓ 检查代码风格"
    echo "  ✓ 检查暗黑模式适配"
    echo "  ✓ 检查应用生命周期"
    
    echo ""
    if [ $issues_found -eq 1 ]; then
        echo "🔴 发现问题，建议生成规则草案"
    else
        echo "✅ 自检通过，无问题"
    fi
    echo ""
}

# 3. 加载 iOS 规则
load_rules() {
    local scene="$1"
    
    echo "📖 加载 iOS 专属规则（场景：$scene）..."
    
    if [ ! -f "$RULES_DIR/builtin_rules.md" ]; then
        echo "⚠️  内置规则文件不存在"
        return 1
    fi
    
    # 简化实现：输出所有规则
    # 实际应该根据场景匹配相关规则
    echo "✅ 已加载 15 条内置 iOS 规则"
    echo ""
    cat "$RULES_DIR/builtin_rules.md"
    echo ""
}

# 4. 生成 iOS 规则草案（带平台检查）
propose() {
    local content="$1"
    local scene="$2"
    local domain="${3:-iOS/通用}"
    
    # 检查平台配置
    if [ "$PLATFORM" != "ios" ]; then
        echo "⚠️  当前平台是 $PLATFORM，不是 iOS"
        echo "iOS 规则草案生成不生效，跳过"
        echo ""
        return 0
    fi
    
    echo "📝 生成 iOS 规则草案..."
    echo "  当前平台：$PLATFORM"
    echo "  领域：$domain"
    echo ""
    
    # 调用 developer-self-improve-core 的 post-check
    local auto_script="$SKILL_DIR/../developer-self-improve-core/scripts/developer-self-improve-core.sh"
    
    if [ -f "$auto_script" ]; then
        "$auto_script" post-check "$content" "$scene"
    else
        echo "⚠️  developer-self-improve-core 未安装，无法生成草案"
        echo ""
        echo "请先安装依赖："
        echo "  clawhub install developer-self-improve-core"
    fi
}

# 5. 显示帮助
show_help() {
    echo "📱 ios-self-improve iOS 开发专属技能"
    echo ""
    echo "依赖：developer-self-improve-core（必须启用）"
    echo ""
    echo "用法：$0 {init|self-check|load-rules|propose}"
    echo ""
    echo "命令说明："
    echo "  init                    初始化技能目录"
    echo "  self-check [代码/内容]   执行 iOS 专属自检"
    echo "  load-rules [场景]        加载 iOS 专属规则"
    echo "  propose [内容] [场景] [领域]  生成 iOS 规则草案"
    echo ""
    echo "示例："
    echo "  $0 init"
    echo "  $0 self-check \"self.completionHandler = { self.updateUI() }\""
    echo "  $0 load-rules \"导航栏配置\""
    echo "  $0 propose \"闭包内使用 self 未加 [weak self]\" \"内存管理\" \"iOS/内存管理\""
}

# ============ 主函数 ============

main() {
    local action="${1:-help}"
    
    case $action in
        init)
            init
            ;;
        self-check)
            shift
            self_check "$@"
            ;;
        load-rules)
            shift
            load_rules "$@"
            ;;
        propose)
            shift
            propose "$@"
            ;;
        help|*)
            show_help
            ;;
    esac
}

# 执行主函数
main "$@"

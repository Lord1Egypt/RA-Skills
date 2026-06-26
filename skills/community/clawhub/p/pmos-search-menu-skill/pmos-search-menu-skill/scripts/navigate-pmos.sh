#!/bin/bash
# PMOS 菜单导航脚本 (Bash)
# 使用方式：./navigate-pmos.sh "信息披露" "综合查询" "市场运营"

TARGET_URL="https://pmos.gs.sgcc.com.cn/"
TARGET_TAB_PATTERN="pxf-settlement"
WAIT_TIME=2000

echo ""
echo "🦞 PMOS 菜单导航工具"
echo "=================="
echo "目标网站：$TARGET_URL"

# 解析菜单路径参数
if [ $# -eq 0 ]; then
    MENU_PATH=("信息披露" "综合查询" "市场运营" "交易组织及出清" "现货市场申报、出清信息" "实时各节点出清类信息" "实时市场出清节点电价")
else
    MENU_PATH=("$@")
fi

echo "导航路径：${MENU_PATH[*]}"
echo ""

# 步骤 1: 打开浏览器
echo "步骤 1: 打开 PMOS 网站..."
openclaw browser open "$TARGET_URL"
echo "  ✓ 网站已打开"

# 步骤 2: 等待用户登录
echo ""
echo "⚠️  请先手动登录网站"
echo "登录完成后按回车继续..."
read
echo "  ✓ 登录确认"

# 初始化标签页 ID
currentTabId=""

# 步骤 3: 遍历菜单路径
for i in "${!MENU_PATH[@]}"; do
    menuItem="${MENU_PATH[$i]}"
    stepNum=$((i + 1))
    totalSteps=${#MENU_PATH[@]}
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "步骤 $stepNum/$totalSteps: 点击 '$menuItem'"
    
    # 获取页面快照
    echo "  📸 获取页面快照..."
    if [ -n "$currentTabId" ]; then
        snapshot=$(openclaw browser snapshot --refs aria --targetId "$currentTabId" --compact 2>&1)
    else
        snapshot=$(openclaw browser snapshot --refs aria --compact 2>&1)
    fi
    echo "  ✓ 快照已获取"
    
    # 查找菜单项的引用
    echo "  🔍 查找菜单项引用..."
    echo "  ⚠️  请在快照中查找包含 '$menuItem' 的元素引用 (ref=eXX)"
    echo "  💡 提示：搜索文本 '$menuItem' 或查看 treeitem 元素"
    
    read -p "  输入元素引用 (例如 e78，留空跳过): " ref
    
    if [ -n "$ref" ]; then
        # 点击菜单项
        echo "  👆 执行点击操作..."
        if [ -n "$currentTabId" ]; then
            openclaw browser act click --ref "$ref" --targetId "$currentTabId" 2>&1
        else
            openclaw browser act click --ref "$ref" 2>&1
        fi
        echo "  ✓ 已点击 '$menuItem'"
        
        # 等待菜单展开或页面加载
        sleep 2
        
        # 检查是否打开了新标签页
        if [ "$menuItem" = "综合查询" ] || [ "$menuItem" = "信息披露" ]; then
            echo "  🔄 检查新标签页..."
            sleep 1
            
            tabs=$(openclaw browser tabs 2>&1)
            if echo "$tabs" | grep -q "$TARGET_TAB_PATTERN"; then
                # 提取新标签页 ID (简化处理)
                echo "  ✓ 检测到新标签页"
                # 需要手动获取新标签页 ID 并切换
            fi
        fi
    else
        echo "  ⚠️  跳过此步骤"
    fi
done

# 完成
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 导航完成！"
echo ""
echo "当前页面内容预览："
openclaw browser snapshot --refs aria --compact ${currentTabId:+--targetId $currentTabId} 2>&1 | head -30

echo ""
echo "💡 提示：如需导出数据，请继续操作页面内的查询和导出功能"
echo ""

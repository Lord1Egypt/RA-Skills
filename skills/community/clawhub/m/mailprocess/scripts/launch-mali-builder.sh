#!/bin/bash

# Mali App Builder Launcher
# 自动打开码力搭建平台并填充用户需求

set -e

MALI_URL="https://lowcode.baidu-int.com/ai-coding"
USER_REQUIREMENT="$1"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Darwin*)    echo "macos";;
        Linux*)     echo "linux";;
        CYGWIN*|MINGW*|MSYS*)    echo "windows";;
        *)          echo "unknown";;
    esac
}

# macOS 实现
launch_on_macos() {
    local requirement="$1"
    
    echo -e "${BLUE}🚀 使用 AppleScript 启动码力搭建平台...${NC}"
    
    # 转义单引号（bash 中的转义方式）
    local requirement_escaped="${requirement//\'/\'\"\'\"\'}"
    
    # 使用 AppleScript 打开 Chrome 并自动填充需求、点击发送按钮
    osascript <<EOF
tell application "Google Chrome"
    activate
    delay 0.5
    
    -- 方式1：直接在当前窗口打开新标签
    if (count of windows) = 0 then
        make new window
        set URL of active tab of front window to "${MALI_URL}"
    else
        tell front window
            set newTab to make new tab
            set URL of newTab to "${MALI_URL}"
        end tell
    end if
    
    delay 5
    
    -- 第一步：先填充需求
    set jsCode1 to "
    (function() {
        const input = document.querySelector('textarea, input[type=\"text\"]');
        if (input) {
            input.value = '${requirement_escaped}';
            input.focus();
            return 'filled';
        }
        return 'not_found';
    })();
    "
    
    tell front window
        set result1 to execute active tab javascript jsCode1
    end tell
    
    delay 1
    
    -- 第二步：触发输入事件
    set jsCode2 to "
    (function() {
        const input = document.querySelector('textarea, input[type=\"text\"]');
        if (input) {
            const inputEvent = new Event('input', { bubbles: true, cancelable: true });
            input.dispatchEvent(inputEvent);
            const changeEvent = new Event('change', { bubbles: true });
            input.dispatchEvent(changeEvent);
            return 'triggered';
        }
        return 'not_found';
    })();
    "
    
    tell front window
        execute active tab javascript jsCode2
    end tell
    
    delay 0.5
    
    -- 第三步：点击发送按钮
    set jsCode3 to "
    (function() {
        // 尝试多种选择器查找发送按钮
        const selectors = [
            'button[type=\"submit\"]',
            'button.send-btn',
            'button.submit-btn',
            'button:has(svg)',
            'button[aria-label*=\"发送\"]',
            'button[title*=\"发送\"]'
        ];
        
        for (let selector of selectors) {
            const btn = document.querySelector(selector);
            if (btn) {
                btn.click();
                return 'clicked: ' + selector;
            }
        }
        
        // 如果找不到，尝试查找最后一个按钮
        const allButtons = document.querySelectorAll('button');
        if (allButtons.length > 0) {
            const lastBtn = allButtons[allButtons.length - 1];
            lastBtn.click();
            return 'clicked last button';
        }
        
        return 'button not found';
    })();
    "
    
    tell front window
        execute active tab javascript jsCode3
    end tell
end tell
EOF
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Chrome 已启动，需求已自动填充！${NC}"
        return 0
    else
        echo -e "${RED}❌ AppleScript 执行失败${NC}"
        return 1
    fi
}

# Linux 实现
launch_on_linux() {
    local requirement="$1"
    
    echo -e "${BLUE}🚀 启动码力搭建平台 (Linux)${NC}"
    
    # 尝试打开 Chrome
    if command -v google-chrome &> /dev/null; then
        google-chrome "${MALI_URL}" &
    elif command -v chromium-browser &> /dev/null; then
        chromium-browser "${MALI_URL}" &
    elif command -v xdg-open &> /dev/null; then
        xdg-open "${MALI_URL}" &
    else
        echo -e "${RED}❌ 未找到浏览器${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 浏览器已打开${NC}"
    echo -e "${YELLOW}⚠️ Linux 系统请手动输入以下需求：${NC}"
    echo -e "${requirement}"
}

# Windows 实现
launch_on_windows() {
    local requirement="$1"
    
    echo -e "${BLUE}🚀 启动码力搭建平台 (Windows)${NC}"
    
    start chrome "${MALI_URL}"
    
    echo -e "${GREEN}✅ 浏览器已打开${NC}"
    echo -e "${YELLOW}⚠️ Windows 系统请手动输入以下需求：${NC}"
    echo -e "${requirement}"
}

# 主函数
main() {
    if [ -z "$USER_REQUIREMENT" ]; then
        echo -e "${RED}❌ 错误：缺少搭建需求参数${NC}"
        echo "用法: $0 \"搭建需求描述\""
        echo "示例: $0 \"创建一个任务管理系统\""
        exit 1
    fi
    
    local os_type=$(detect_os)
    
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}   码力搭建平台启动器${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}🌐 平台地址:${NC} ${MALI_URL}"
    echo -e "${BLUE}💻 操作系统:${NC} ${os_type}"
    echo -e "${BLUE}📋 搭建需求:${NC}"
    echo -e "${GREEN}${USER_REQUIREMENT}${NC}"
    echo ""
    
    case $os_type in
        macos)
            launch_on_macos "$USER_REQUIREMENT"
            ;;
        linux)
            launch_on_linux "$USER_REQUIREMENT"
            ;;
        windows)
            launch_on_windows "$USER_REQUIREMENT"
            ;;
        *)
            echo -e "${RED}❌ 不支持的操作系统${NC}"
            exit 1
            ;;
    esac
    
    echo ""
    echo -e "${GREEN}✅ 操作完成！${NC}"
    echo -e "${BLUE}⏳ 请在浏览器中查看搭建进度...${NC}"
    echo ""
}

main "$@"
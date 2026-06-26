#!/bin/bash

# ITSM 工单自动提交技能 - 启动浏览器
# 使用系统自带 chromium-browser，零依赖

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 添加用户本地 bin 到 PATH（pip 安装位置）
export PATH="$HOME/.local/bin:$PATH"

DEBUG_PORT=9222
ITSM_URL="https://itsm.westmonth.com/#/create"

echo "🖋️ ITSM 工单自动提交技能 v2.1"
echo "===================="
echo ""

# WSL2 环境设置 DISPLAY
if grep -qi microsoft /proc/version && [ -z "$DISPLAY" ]; then
    export DISPLAY=:0
    echo "🔧 WSL2 环境：设置 DISPLAY=$DISPLAY"
fi

# 检查并安装 Python 依赖
echo "🔍 检查 Python 依赖..."
MISSING_DEPS=false

# 检查 selenium
if ! python3 -c "import selenium" 2>/dev/null; then
    echo "⚠️  缺少 selenium 依赖"
    MISSING_DEPS=true
fi

# 检查 requests
if ! python3 -c "import requests" 2>/dev/null; then
    echo "⚠️  缺少 requests 依赖"
    MISSING_DEPS=true
fi

if [ "$MISSING_DEPS" = true ]; then
    echo ""
    echo "📦 正在自动安装 Python 依赖..."
    echo ""

    INSTALL_SUCCESS=false

    # 方法 1: 使用 pip3 命令
    if command -v pip3 &> /dev/null; then
        echo "🔧 使用 pip3 安装..."
        if pip3 install selenium requests --break-system-packages 2>/dev/null; then
            INSTALL_SUCCESS=true
            echo "✅ 安装成功（pip3）"
        fi
    fi

    # 方法 2: 使用 python3 -m pip
    if [ "$INSTALL_SUCCESS" = false ] && python3 -m pip --version &>/dev/null; then
        echo "🔧 使用 python3 -m pip 安装..."
        if python3 -m pip install selenium requests --break-system-packages 2>/dev/null; then
            INSTALL_SUCCESS=true
            echo "✅ 安装成功（python3 -m pip）"
        fi
    fi

    # 方法 3: 使用 python -m pip
    if [ "$INSTALL_SUCCESS" = false ] && command -v python &> /dev/null; then
        if python -m pip --version &>/dev/null 2>&1; then
            echo "🔧 使用 python -m pip 安装..."
            if python -m pip install selenium requests --break-system-packages 2>/dev/null; then
                INSTALL_SUCCESS=true
                echo "✅ 安装成功（python -m pip）"
            fi
        fi
    fi

    # 方法 4: 使用 ensurepip 自安装 pip
    if [ "$INSTALL_SUCCESS" = false ]; then
        echo "🔧 pip 未找到，尝试使用 ensurepip 安装 pip..."
        if python3 -m ensurepip --upgrade 2>/dev/null; then
            echo "✅ pip 已安装，正在安装依赖..."
            if python3 -m pip install selenium requests --break-system-packages 2>/dev/null; then
                INSTALL_SUCCESS=true
                echo "✅ 安装成功（ensurepip）"
            fi
        else
            echo "⚠️ ensurepip 失败，尝试从网络安装 pip..."
            # 方法 5: 下载 get-pip.py
            GET_PIP_URL="https://bootstrap.pypa.io/get-pip.py"
            GET_PIP_FILE="/tmp/get-pip.py"
            if command -v curl &> /dev/null; then
                curl -sS "$GET_PIP_URL" -o "$GET_PIP_FILE" 2>/dev/null
            elif command -v wget &> /dev/null; then
                wget -q "$GET_PIP_URL" -O "$GET_PIP_FILE" 2>/dev/null
            fi

            if [ -f "$GET_PIP_FILE" ]; then
                python3 "$GET_PIP_FILE" --user --break-system-packages 2>/dev/null
                rm -f "$GET_PIP_FILE"
                # 添加 user bin 到 PATH
                export PATH="$HOME/.local/bin:$PATH"
                if python3 -m pip install selenium requests --break-system-packages 2>/dev/null; then
                    INSTALL_SUCCESS=true
                    echo "✅ 安装成功（get-pip.py）"
                fi
            fi
        fi
    fi

    # 再次检查
    if ! python3 -c "import selenium, requests" 2>/dev/null; then
        echo ""
        echo "❌ 依赖安装失败"
        echo ""
        echo "请手动尝试以下命令之一："
        echo "  pip3 install selenium requests"
        echo "  python3 -m pip install selenium requests --user"
        echo "  sudo apt-get install python3-pip && pip3 install selenium requests"
        exit 1
    fi
else
    echo "✅ Python 依赖已就绪"
fi

# 检查是否已有浏览器运行
if pgrep -f "chromium.*remote-debugging-port=$DEBUG_PORT" > /dev/null; then
    echo "✅ 浏览器已在运行（端口 $DEBUG_PORT）"
    BROWSER_EXISTED=true
else
    echo "🚀 启动 Chromium 浏览器（远程调试端口 $DEBUG_PORT）..."
    echo "   窗口模式：可见（1920x1080）"
    echo ""

    # 检查 chromium-browser 是否安装
    if ! command -v chromium-browser &> /dev/null; then
        echo "📦 正在安装 chromium-browser..."
        sudo apt-get update -qq
        sudo apt-get install -y chromium-browser
        echo "✅ chromium-browser 安装完成"
    fi

    # 启动 chromium-browser（可见窗口模式）
    nohup chromium-browser         --remote-debugging-port=$DEBUG_PORT         --remote-allow-origins=*         --no-first-run         --window-size=1920,1080         --window-position=0,0         --force-device-scale-factor=1.0         --disable-blink-features=AutomationControlled         > /tmp/chromium-$DEBUG_PORT.log 2>&1 &

    sleep 3

    # 验证浏览器是否启动成功
    if pgrep -f "chromium.*remote-debugging-port=$DEBUG_PORT" > /dev/null; then
        echo "✅ 浏览器启动成功"
        echo "   💡 浏览器窗口应该在屏幕上可见"
        BROWSER_EXISTED=false
    else
        echo "❌ 浏览器启动失败，请检查日志：/tmp/chromium-$DEBUG_PORT.log"
        echo ""
        echo "故障排除："
        echo "1. 检查 WSLg 是否支持：echo $DISPLAY"
        echo "2. 尝试手动启动：chromium-browser --remote-debugging-port=$DEBUG_PORT"
        exit 1
    fi
fi

echo ""
echo "📍 浏览器已就绪，开始提交工单..."
echo ""

# 运行提交脚本（Python CDP 方式）
python3 "$SCRIPT_DIR/submit-itsm.py" "$@"
EXIT_CODE=$?

echo ""
echo "===================="
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ 工单提交完成"
else
    echo "⚠️  工单提交出现问题（退出码：$EXIT_CODE）"
fi

# 只有当脚本启动的浏览器才自动关闭
if [ "$BROWSER_EXISTED" = false ]; then
    echo ""
    echo "🔒 正在关闭浏览器..."
    pkill -f "chromium.*remote-debugging-port=$DEBUG_PORT" 2>/dev/null
    sleep 1
    if pgrep -f "chromium.*remote-debugging-port=$DEBUG_PORT" > /dev/null; then
        echo "⚠️  浏览器关闭超时，请手动关闭"
    else
        echo "✅ 浏览器已自动关闭"
    fi
else
    echo ""
    echo "💡 浏览器保持运行（脚本启动前已存在）"
    echo "   如需关闭：pkill -f 'chromium.*--remote-debugging-port=$DEBUG_PORT'"
fi

echo ""

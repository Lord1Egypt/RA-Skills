#!/bin/bash

# 快普系统自动登录技能脚本

# 获取脚本所在目录
SCRIPT_DIR="$(dirname "$0")"

# Python 脚本路径 (使用 Selenium 版本)
PYTHON_SCRIPT="$SCRIPT_DIR/kuaipu_skill.py"

# 检查 Python 脚本是否存在
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "错误: Python 脚本不存在: $PYTHON_SCRIPT"
  exit 1
fi

# 检查并激活虚拟环境
activate_venv() {
  echo "正在检查虚拟环境..."
  
  # 检查脚本所在目录的同级目录是否有虚拟环境
  VENV_DIR="$SCRIPT_DIR/../.venv"
  if [ -d "$VENV_DIR" ]; then
    # 转换为绝对路径显示
    VENV_ABS_PATH="$(cd "$VENV_DIR" && pwd)"
    echo "找到虚拟环境: $VENV_ABS_PATH"
    # 激活虚拟环境
    if [ -f "$VENV_DIR/bin/activate" ]; then
      echo "激活虚拟环境..."
      source "$VENV_DIR/bin/activate"
      return 0
    else
      echo "警告: 虚拟环境存在但缺少激活脚本"
      return 1
    fi
  else
    # 检查当前目录是否有虚拟环境
    if [ -d ".venv" ]; then
      echo "找到虚拟环境: .venv"
      if [ -f ".venv/bin/activate" ]; then
        echo "激活虚拟环境..."
        source ".venv/bin/activate"
        return 0
      else
        echo "警告: 虚拟环境存在但缺少激活脚本"
        return 1
      fi
    else
      echo "未找到虚拟环境，使用系统 Python"
      return 1
    fi
  fi
}

# 检查依赖是否安装
check_deps() {
  echo "正在检查依赖..."
  
  # 检查 selenium
  if ! python3 -c "import selenium" 2>/dev/null; then
    echo "正在安装 selenium..."
    if command -v uv &> /dev/null; then
      uv pip install selenium
    else
      pip3 install selenium
    fi
  fi
  
  # 检查 webdriver_manager
  if ! python3 -c "import webdriver_manager" 2>/dev/null; then
    echo "正在安装 webdriver_manager..."
    if command -v uv &> /dev/null; then
      uv pip install webdriver_manager
    else
      pip3 install webdriver_manager
    fi
  fi
  
  # 检查 ddddocr
  if ! python3 -c "import ddddocr" 2>/dev/null; then
    echo "正在安装 ddddocr..."
    if command -v uv &> /dev/null; then
      uv pip install ddddocr
    else
      pip3 install ddddocr
    fi
  fi
  
  echo "依赖检查完成！"
}

# 主函数
main() {
  # 激活虚拟环境
  activate_venv
  
  # 检查依赖
  check_deps
  
  case "$1" in
    login)
      python3 "$PYTHON_SCRIPT" login
      ;;
    status)
      python3 "$PYTHON_SCRIPT" status
      ;;
    logout)
      python3 "$PYTHON_SCRIPT" logout
      ;;
    shenpi)
      python3 "$PYTHON_SCRIPT" shenpi
      ;;
    *)
      echo "用法: kuaipu-skill [login|status|logout|shenpi]"
      echo ""
      echo "login   - 执行快普系统登录"
      echo "status  - 查看登录状态"
      echo "logout  - 退出登录"
      echo "shenpi  - 访问审批中心并提取业务审批列表"
      ;;
  esac
}

# 执行主函数
main "$@"

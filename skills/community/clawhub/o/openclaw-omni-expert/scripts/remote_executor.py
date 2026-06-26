#!/usr/bin/env python3
"""
OpenClaw 远程桌面执行器
通过桌面远程软件（AnyDesk/TeamViewer/向日葵）执行命令

策略：
1. 将脚本传输到远程主机
2. 通过远程桌面软件执行脚本
3. 获取执行结果
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class RemoteDesktopExecutor:
    """
    远程桌面执行器

    支持通过以下工具执行远程命令：
    - AnyDesk
    - TeamViewer
    - 向日葵
    - VNC
    """

    def __init__(self, tool: str, session_id: str = None, host: str = None):
        self.tool = tool.lower()
        self.session_id = session_id
        self.host = host
        self.script_dir = Path.home() / ".openclaw" / "remote_scripts"
        self.script_dir.mkdir(parents=True, exist_ok=True)

    def execute_script(self, script_content: str, timeout: int = 300) -> Tuple[bool, str]:
        """
        执行远程脚本

        Args:
            script_content: 脚本内容
            timeout: 超时时间（秒）

        Returns:
            (success, output)
        """
        # 生成唯一脚本ID
        script_id = hashlib.md5(
            f"{script_content}{time.time()}".encode()
        ).hexdigest()[:8]

        # 保存脚本
        script_path = self.script_dir / f"{script_id}.sh"
        with open(script_path, 'w') as f:
            f.write(f"#!/bin/bash\nset -e\n{script_content}\n")

        os.chmod(script_path, 0o755)

        print(f"脚本已生成: {script_path}")
        print(f"请在远程桌面中执行以下命令：")

        if self.tool in ["anydesk", "teamviewer", "sunlogin", "向日葵"]:
            print(f"\n通过 {self.tool} 连接到远程主机后，执行：")
            print(f"bash < {script_path}")
        else:
            print(f"bash {script_path}")

        return True, f"脚本已准备，请手动执行: {script_path}"

    def generate_execution_guide(self, commands: List[str]) -> str:
        """
        生成远程执行指南

        Args:
            commands: 命令列表

        Returns:
            执行指南文本
        """
        guide = f"""
{'='*60}
OpenClaw 远程执行指南
{'='*60}

远程工具: {self.tool.upper()}
会话ID: {self.session_id or '请手动输入'}
主机: {self.host or '请手动输入'}

{'='*60}
执行步骤
{'='*60}

1. 使用 {self.tool} 连接到远程主机
   - 如果使用 AnyDesk: anydesk --connect {self.session_id}
   - 如果使用 TeamViewer: teamviewer --connect {self.session_id}
   - 如果使用向日葵: sunlogin --control {self.session_id}

2. 连接成功后，打开远程终端（PowerShell/Terminal）

3. 复制并执行以下命令：

{'-'*60}
"""

        for i, cmd in enumerate(commands, 1):
            guide += f"\n# 命令 {i}\n{cmd}\n"

        guide += f"""
{'-'*60}

4. 等待执行完成

5. 将输出复制回本地

{'='*60}
完整脚本
{'='*60}

可以将以下内容保存为 .sh 文件后执行：

#!/bin/bash
{chr(10).join(commands)}

{'='*60}
"""

        return guide


def create_openclaw_install_script() -> str:
    """创建 OpenClaw 安装脚本"""
    return """
# OpenClaw 一键安装脚本
set -e

echo "=== 开始安装 OpenClaw ==="

# 检测系统
echo "检测系统..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "不支持的操作系统"
    exit 1
fi
echo "操作系统: $OS"

# 检查 Node.js
echo "检查 Node.js..."
if ! command -v node &> /dev/null; then
    echo "安装 Node.js..."
    if [[ "$OS" == "linux" ]]; then
        curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
        apt-get install -y nodejs
    elif [[ "$OS" == "macos" ]]; then
        brew install node@22
    fi
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
echo "Node.js 版本: $NODE_VERSION"

if [[ $NODE_VERSION -lt 22 ]]; then
    echo "Node.js 版本过低，需要 v22+"
    exit 1
fi

# 安装 OpenClaw
echo "安装 OpenClaw..."
npm install -g openclaw@latest

# 验证安装
echo "验证安装..."
openclaw --version

# 启动 Gateway
echo "启动 Gateway..."
openclaw gateway start &

# 等待启动
sleep 5

# 检查状态
echo "检查状态..."
curl -s http://127.0.0.1:18789/api/health || echo "健康检查失败"

echo "=== 安装完成 ==="
"""


def create_openclaw_diagnose_script() -> str:
    """创建 OpenClaw 诊断脚本"""
    return """
# OpenClaw 诊断脚本
set -e

echo "=== OpenClaw 系统诊断 ==="
echo "时间: $(date)"
echo ""

# 进程状态
echo "--- 进程状态 ---"
ps aux | grep -i openclaw | grep -v grep || echo "未找到 OpenClaw 进程"

# 端口监听
echo ""
echo "--- 端口监听 (18789) ---"
lsof -i :18789 2>/dev/null || echo "端口 18789 未监听"

# 健康检查
echo ""
echo "--- 健康检查 ---"
curl -s -m 5 http://127.0.0.1:18789/api/health || echo "健康检查失败"

# 配置文件
echo ""
echo "--- 配置文件 ---"
if [ -f ~/.openclaw/openclaw.json ]; then
    echo "配置文件存在"
    cat ~/.openclaw/openclaw.json | python3 -m json.tool > /dev/null 2>&1 && echo "JSON 格式: 有效" || echo "JSON 格式: 无效"
else
    echo "配置文件不存在"
fi

# 最近日志
echo ""
echo "--- 最近错误日志 ---"
if [ -d ~/.openclaw/logs ]; then
    tail -20 ~/.openclaw/logs/*.log 2>/dev/null | grep -i error || echo "无错误日志"
else
    echo "日志目录不存在"
fi

# 系统资源
echo ""
echo "--- 系统资源 ---"
echo "内存:"
free -m | head -2
echo ""
echo "磁盘空间:"
df -h ~ | tail -1

echo ""
echo "=== 诊断完成 ==="
"""


def create_openclaw_fix_script() -> str:
    """创建 OpenClaw 修复脚本"""
    return """
# OpenClaw 自动修复脚本
set -e

echo "=== OpenClaw 自动修复 ==="

# 1. 停止所有 OpenClaw 进程
echo "停止 OpenClaw 进程..."
pkill -f openclaw 2>/dev/null || true
sleep 2

# 2. 清理端口
echo "清理端口 18789..."
lsof -ti :18789 | xargs kill -9 2>/dev/null || true

# 3. 修复配置文件
echo "修复配置文件..."
mkdir -p ~/.openclaw
if [ ! -f ~/.openclaw/openclaw.json ]; then
    cat > ~/.openclaw/openclaw.json << 'EOF'
{
  "version": "1.0",
  "gateway": {
    "port": 18789,
    "host": "127.0.0.1"
  },
  "model": {
    "provider": ""
  },
  "channels": []
}
EOF
    echo "已创建默认配置文件"
else
    echo "配置文件已存在，验证 JSON..."
    cat ~/.openclaw/openclaw.json | python3 -m json.tool > /dev/null 2>&1 && echo "JSON 有效" || echo "JSON 无效，需要手动修复"
fi

# 4. 创建日志目录
echo "创建日志目录..."
mkdir -p ~/.openclaw/logs

# 5. 重新安装（如果需要）
echo "检查 OpenClaw..."
if ! command -v openclaw &> /dev/null; then
    echo "OpenClaw 未安装，正在安装..."
    npm install -g openclaw@latest
fi

# 6. 启动服务
echo "启动 Gateway..."
cd ~
openclaw gateway start &
sleep 5

# 7. 验证
echo ""
echo "--- 验证修复 ---"
sleep 3
curl -s -m 5 http://127.0.0.1:18789/api/health && echo "" && echo "修复成功！" || echo "修复后仍有问题，请检查日志"

echo ""
echo "=== 修复完成 ==="
"""


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw 远程桌面执行器"
    )

    parser.add_argument("--tool", choices=["anydesk", "teamviewer", "sunlogin", "vnc"],
                       default="anydesk", help="远程工具")
    parser.add_argument("--session-id", help="会话ID")
    parser.add_argument("--host", help="主机地址")
    parser.add_argument("--mode", choices=["install", "diagnose", "fix"],
                       default="diagnose", help="执行模式")
    parser.add_argument("--script-only", action="store_true",
                       help="只生成脚本，不执行")

    args = parser.parse_args()

    # 创建执行器
    executor = RemoteDesktopExecutor(args.tool, args.session_id, args.host)

    # 生成脚本
    if args.mode == "install":
        script = create_openclaw_install_script()
    elif args.mode == "fix":
        script = create_openclaw_fix_script()
    else:
        script = create_openclaw_diagnose_script()

    # 输出脚本
    print(script)

    # 生成执行指南
    if args.script_only:
        print("\n" + executor.generate_execution_guide([script]))
    else:
        print("\n" + executor.generate_execution_guide([script]))
        print("\n请将上述脚本复制到远程主机执行。")


if __name__ == "__main__":
    main()

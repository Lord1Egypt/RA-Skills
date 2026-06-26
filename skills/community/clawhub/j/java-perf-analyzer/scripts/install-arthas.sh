#!/bin/bash
# Arthas 自动安装脚本
# 用法: install-arthas.sh <ssh-host> <ssh-user> <ssh-password> <arthas-dir> <java-process-name>
# 示例: install-arthas.sh trythis.cn root 'password' /root/soft/arthas chat-editor

set -e

# 参数检查
if [ -z "$5" ]; then
    echo "用法: install-arthas.sh <ssh-host> <ssh-user> <ssh-password> <arthas-dir> <java-process-name>"
    echo "示例: install-arthas.sh trythis.cn root 'your_password' /root/soft/arthas chat-editor"
    echo ""
    echo "参数说明:"
    echo "  ssh-host        SSH服务器地址"
    echo "  ssh-user        SSH用户名"
    echo "  ssh-password    SSH密码"
    echo "  arthas-dir      Arthas安装目录"
    echo "  java-process    Java进程名称关键词（用于匹配进程）"
    exit 1
fi

SSH_HOST="$1"
SSH_USER="$2"
SSH_PASS="$3"
ARTHAS_DIR="$4"
PROCESS_NAME="$5"

echo "=== Arthas 安装检查 ==="
echo "目标服务器: $SSH_HOST"
echo "Arthas目录: $ARTHAS_DIR"
echo "进程名称: $PROCESS_NAME"
echo ""

# 检查 Arthas 是否已安装
CHECK_RESULT=$(sshpass -p "$SSH_PASS" ssh "$SSH_USER@$SSH_HOST" "ls -la $ARTHAS_DIR/arthas-boot.jar 2>/dev/null || echo NOT_FOUND")

if [[ "$CHECK_RESULT" != *"NOT_FOUND"* ]]; then
    echo "✅ Arthas 已安装: $ARTHAS_DIR/arthas-boot.jar"
else
    echo "📥 下载 Arthas..."
    sshpass -p "$SSH_PASS" ssh "$SSH_USER@$SSH_HOST" "mkdir -p $ARTHAS_DIR && cd $ARTHAS_DIR && curl -O https://arthas.aliyun.com/arthas-boot.jar"
    echo "✅ Arthas 下载完成"
fi

# 检查 Java 进程
echo ""
echo "=== 检查 Java 进程 ==="
JAVA_PID=$(sshpass -p "$SSH_PASS" ssh "$SSH_USER@$SSH_HOST" "ps -ef | grep java | grep $PROCESS_NAME | grep -v grep | awk '{print \$2}' | head -1")

if [ -z "$JAVA_PID" ]; then
    echo "❌ 未找到 Java 进程: $PROCESS_NAME"
    echo ""
    echo "可用 Java 进程列表:"
    sshpass -p "$SSH_PASS" ssh "$SSH_USER@$SSH_HOST" "ps -ef | grep java | grep -v grep | awk '{printf \"  PID: %s  进程: %s\\n\", \$2, \$NF}' | head -10"
    echo ""
    echo "请确认进程名称关键词是否正确"
    exit 1
fi

echo "✅ 找到进程 PID: $JAVA_PID"

# 检查 Arthas 是否已附着
ATTACHED=$(sshpass -p "$SSH_PASS" ssh "$SSH_USER@$SSH_HOST" "ps -ef | grep arthas | grep $JAVA_PID | grep -v grep || echo NOT_ATTACHED")

if [[ "$ATTACHED" != *"NOT_ATTACHED"* ]]; then
    echo "✅ Arthas 已附着到进程"
else
    echo ""
    echo "=== 启动 Arthas ==="
    # 启动 Arthas 并附着，启用 HTTP API
    sshpass -p "$SSH_PASS" ssh "$SSH_USER@$SSH_HOST" "cd $ARTHAS_DIR && nohup java -jar arthas-boot.jar $JAVA_PID --target-ip 0.0.0.0 --http-port 8563 > arthas.log 2>&1 &"
    
    # 等待启动
    echo "等待 Arthas 启动..."
    sleep 8
    
    # 检查 HTTP API
    HTTP_CHECK=$(sshpass -p "$SSH_PASS" ssh "$SSH_USER@$SSH_HOST" "curl -s -o /dev/null -w '%{http_code}' http://localhost:8563/api || echo FAILED")
    
    if [[ "$HTTP_CHECK" == *"200"* ]] || [[ "$HTTP_CHECK" == *"405"* ]]; then
        echo "✅ Arthas HTTP API 启动成功 (端口 8563)"
    else
        echo "⚠️ HTTP API 未就绪，请检查日志: $ARTHAS_DIR/arthas.log"
        echo "日志内容:"
        sshpass -p "$SSH_PASS" ssh "$SSH_USER@$SSH_HOST" "tail -20 $ARTHAS_DIR/arthas.log"
    fi
fi

echo ""
echo "=== 安装完成 ==="
echo ""
echo "配置信息:"
echo "  Arthas 目录: $ARTHAS_DIR"
echo "  进程 PID:    $JAVA_PID"
echo "  HTTP API:    http://localhost:8563 (通过 SSH 隧道)"
echo ""
echo "下一步操作:"
echo "1. 建立 SSH 隧道:"
echo "   ssh -f -N -L 8563:localhost:8563 $SSH_USER@$SSH_HOST"
echo ""
echo "2. 配置 MCP (mcporter.json):"
echo "   见 skill 文档中的 MCP 配置模板"
echo ""
echo "3. 测试连接:"
echo "   mcporter call arthas jvm_info"
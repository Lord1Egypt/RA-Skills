#!/bin/bash
# Jenkins 构建触发脚本
# 用法：./trigger-build.sh worker 或 ./trigger-build.sh user

JOB_NAME=$1

if [ -z "$JOB_NAME" ]; then
    echo "用法：$0 <job_name>"
    echo "示例：$0 worker  (师傅端)"
    echo "      $0 user   (用户端)"
    exit 1
fi

JENKINS_URL="http://localhost:8080/job/${JOB_NAME}/"

echo "🔧 正在触发 Jenkins 构建：${JOB_NAME}"
echo "📍 页面：${JENKINS_URL}"

# 打开浏览器页面
open "$JENKINS_URL"

echo "✅ 已打开 Jenkins 页面，请手动点击'立即构建'按钮"
echo "   或使用浏览器自动化工具点击"

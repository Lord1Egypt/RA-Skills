#!/bin/bash
# 学习规划师测试脚本

echo "=== 学习规划师功能测试 ==="
echo ""

echo "1. 创建学习目标"
learning goal create "Web 开发" --description "全栈 Web 开发技能"
learning goal create "前端开发" --parent 1 --priority high
learning goal create "后端开发" --parent 1 --priority high

echo ""
echo "2. 查看目标树"
learning goal tree

echo ""
echo "3. 更新目标进度"
learning goal progress 2 --percent 50

echo ""
echo "4. 生成今日计划"
learning plan today

echo ""
echo "5. 创建复习卡片"
learning card create "HTTP 状态码 200" --back "请求成功" --tags web
learning card create "CSS 盒模型" --back "content, padding, border, margin" --tags css

echo ""
echo "6. 添加学习资源"
learning resource add "MDN Web Docs" --url https://developer.mozilla.org --type documentation --tags web

echo ""
echo "7. 查看复习统计"
learning review stats

echo ""
echo "8. 查看学习统计"
learning report stats

echo ""
echo "=== 测试完成 ==="

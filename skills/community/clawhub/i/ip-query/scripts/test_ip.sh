#!/bin/bash

# 测试IP查询脚本

echo "测试IP查询技能..."
echo "=================="

# 测试简单模式
echo ""
echo "1. 测试简单模式:"
./ip_query.sh --simple

# 测试详细模式
echo ""
echo "2. 测试详细模式:"
./ip_query.sh --detail

# 测试JSON模式
echo ""
echo "3. 测试JSON模式:"
./ip_query.sh --json | head -20

echo ""
echo "测试完成!"
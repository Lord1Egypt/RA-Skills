#!/bin/bash

# 设置脚本文件可执行权限

echo "设置脚本文件可执行权限..."

# 给所有.sh文件添加执行权限
chmod +x *.sh

# 检查文件权限
echo "当前目录脚本文件权限:"
ls -la *.sh

echo ""
echo "权限设置完成！"
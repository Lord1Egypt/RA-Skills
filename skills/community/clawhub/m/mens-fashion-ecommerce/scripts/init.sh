#!/bin/bash

# 男装电商系统技能初始化脚本
# 用于初始化技能目录结构

echo "正在初始化男装电商系统技能..."

# 创建必要的目录结构
mkdir -p references scripts assets

echo "技能目录结构创建完成"
echo ""
echo "技能文件清单:"
echo "1. SKILL.md - 技能主文件"
echo "2. references/ - 参考文档"
echo "   - backend-architecture.md - 后端架构设计"
echo "   - frontend-architecture.md - 前端架构设计"
echo "   - database-schema.md - 数据库设计"
echo "   - api-specification.md - API接口规范"
echo "3. scripts/ - 脚本文件"
echo "   - generate-project.sh - 项目生成脚本"
echo "4. README.md - 项目说明文档"
echo ""
echo "技能已准备就绪，可以开始使用！"
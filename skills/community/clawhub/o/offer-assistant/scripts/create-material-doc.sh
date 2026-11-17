#!/bin/bash
# create-material-doc.sh
# 创建简历素材库文档（飞书云文档）
#
# 由 Agent 在用户上传简历后自动调用。
# 脚本内容由 Agent 在运行时决定，这里只是声明接口。
#
# 调用方式：
#   agent 内部处理：提取简历 → 调用 feishu_create_doc 创建素材库文档
#   → 写入求职 2026 文件夹
#
# 素材库文档模板结构（由 Agent 填充内容）：
#
# 【素材库】
# 创建时间：YYYY-MM-DD
#
# == 基础信息 ==
# - 姓名：
# - 手机：
# - 邮箱：
# - 城市：
#
# == 教育背景 ==
# - 学校 | 专业 | 学历 | 毕业年份
#
# == 工作经历 ==
# ### 公司A | YYYY.MM - YYYY.MM
# - 职责描述（原文）
#
# === 项目经历 ===
# #### 项目名A（公司A）
# - 角色：
# - 动作+结果（原文）
#
# == 技能标签 ==
# - 标签1 / 标签2 / 标签3

echo "⚠️ 此脚本为接口声明，实际执行由 Agent 通过 feishu_create_doc 完成"
echo "Agent 需要："
echo "  1. 提取简历内容"
echo "  2. 调用 feishu_create_doc 创建素材库文档"
echo "  3. 调用 feishu_drive_file move 将文档移入求职 2026 文件夹 (AYCEfx1x0lCjBYdlz8MctUw1nyh)"

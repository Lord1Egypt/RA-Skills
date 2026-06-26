#!/bin/bash
# OpenClaw快速需求评估脚本
# 帮助用户确定最适合的skill组合

echo "🎯 OpenClaw使用评估向导"
echo "========================"
echo ""

# 使用经验
echo "1. 你的OpenClaw使用经验如何？"
echo "   1) 第一次使用（刚安装）"
echo "   2) 尝试过但不太会"
echo "   3) 会用基础功能"
echo "   4) 熟练使用"
read -p "请选择(1-4): " experience_level

# 主要场景
echo ""
echo "2. 你主要想用OpenClaw做什么？"
echo "   1) 工作自动化（会议、邮件、项目管理）"
echo "   2) 个人效率（笔记、任务、健康、财务）"
echo "   3) 开发工作（代码、部署、测试）"
echo "   4) 学习AI/新技术（研究、总结、实验）"
echo "   5) 其他"
read -p "请选择(1-5): " use_case

# 技术舒适度
echo ""
echo "3. 你的技术舒适度（1-10分，1=新手，10=专家）"
read -p "评分(1-10): " tech_comfort

# 可用时间
echo ""
echo "4. 每周可以花多少时间学习/使用OpenClaw？"
echo "   1) <2小时"
echo "   2) 2-5小时"
echo "   3) 5-10小时"
echo "   4) >10小时"
read -p "请选择(1-4): " time_available

# 生成评估报告
echo ""
echo "📊 评估结果报告"
echo "================"
echo ""

case $experience_level in
  1) exp_text="新手（第一次使用）" ;;
  2) exp_text="初学者（尝试过）" ;;
  3) exp_text="中级（会用基础）" ;;
  4) exp_text="高级（熟练使用）" ;;
  *) exp_text="未指定" ;;
esac

case $use_case in
  1) use_text="工作自动化" ;;
  2) use_text="个人效率" ;;
  3) use_text="开发工作" ;;
  4) use_text="学习AI/技术" ;;
  5) use_text="其他用途" ;;
  *) use_text="未指定" ;;
esac

case $time_available in
  1) time_text="<2小时/周" ;;
  2) time_text="2-5小时/周" ;;
  3) time_text="5-10小时/周" ;;
  4) time_text=">10小时/周" ;;
  *) time_text="未指定" ;;
esac

echo "📋 基本信息"
echo "  • 使用经验: $exp_text"
echo "  • 主要场景: $use_text"
echo "  • 技术舒适度: $tech_comfort/10"
echo "  • 可用时间: $time_text"
echo ""

# 推荐skill
echo "🎯 推荐skill组合"
echo "---------------"

# 必备skill（所有用户）
echo "✅ 必备skill（建议所有用户安装）:"
echo "   • self-improving-agent - 自我改进系统"
echo "   • find-skills - skill发现工具"
echo "   • summarize - 内容总结工具"
echo ""

# 场景特定推荐
echo "📦 场景推荐（基于你的选择）:"
case $use_case in
  1)
    echo "   工作自动化用户:"
    echo "   • gog - Google Workspace集成"
    echo "   • github - 代码管理"
    echo "   • slack/discord - 团队沟通"
    echo "   • calendar - 日程管理"
    ;;
  2)
    echo "   个人效率用户:"
    echo "   • weather - 天气查看"
    echo "   • reminders/todo - 任务管理"
    echo "   • notes - 笔记记录"
    echo "   • health/fitness - 健康追踪"
    ;;
  3)
    echo "   开发用户:"
    echo "   • github - 代码管理"
    echo "   • terminal - 终端自动化"
    echo "   • docker - 容器管理"
    echo "   • testing - 代码测试"
    ;;
  4)
    echo "   学习AI/技术用户:"
    echo "   • summarize - 内容消化"
    echo "   • research - 信息搜集"
    echo "   • teaching - 知识分享"
    echo "   • experiment-tracker - 实验记录"
    ;;
  5)
    echo "   其他用途用户:"
    echo "   请描述具体需求以获取更精准推荐"
    ;;
esac
echo ""

# 学习路径建议
echo "📚 学习路径建议"
echo "---------------"

case $experience_level in
  1)
    echo "第一周（新手入门）:"
    echo "  1. 安装必备skill（3个）"
    echo "  2. 学习基本命令（openclaw help）"
    echo "  3. 完成第一个实际任务（如总结文章）"
    echo "  4. 加入OpenClaw社区"
    ;;
  2)
    echo "第一周（巩固基础）:"
    echo "  1. 安装场景推荐skill（3-4个）"
    echo "  2. 学习常用workflow模式"
    echo "  3. 自动化一个重复任务"
    echo "  4. 帮助一个其他新手"
    ;;
  3)
    echo "第一周（进阶提升）:"
    echo "  1. 探索高级skill组合"
    echo "  2. 创建自定义workflow"
    echo "  3. 参与社区讨论"
    echo "  4. 考虑创建自己的skill"
    ;;
  4)
    echo "第一周（专家扩展）:"
    echo "  1. 指导新用户入门"
    echo "  2. 贡献代码或文档"
    echo "  3. 分享使用经验模式"
    echo "  4. 探索集成外部系统"
    ;;
esac
echo ""

# 安装命令
echo "⚡ 快速安装命令"
echo "---------------"
echo "安装必备skill:"
echo "  clawhub install self-improving-agent"
echo "  clawhub install find-skills"
echo "  clawhub install summarize"
echo ""

# 保存评估结果
timestamp=$(date +%Y%m%d_%H%M%S)
cat > "openclaw-assessment-$timestamp.md" << EOF
# OpenClaw使用评估报告
**评估时间**: $(date)
**评估ID**: ASS-$timestamp

## 基本信息
- 使用经验: $exp_text
- 主要场景: $use_text  
- 技术舒适度: $tech_comfort/10
- 可用时间: $time_text

## 推荐skill组合
$(cat << INNER
必备skill:
• self-improving-agent
• find-skills  
• summarize

场景推荐:
$(
case $use_case in
  1) echo "• gog\n• github\n• slack/discord\n• calendar" ;;
  2) echo "• weather\n• reminders/todo\n• notes\n• health/fitness" ;;
  3) echo "• github\n• terminal\n• docker\n• testing" ;;
  4) echo "• summarize\n• research\n• teaching\n• experiment-tracker" ;;
  5) echo "• 请描述具体需求" ;;
esac
)
INNER
)

## 后续步骤
1. 安装推荐skill
2. 按照学习路径逐步提升
3. 遇到问题使用 how-to-do skill 获取帮助
4. 定期评估进展并调整

## 评估工具
本报告由 how-to-do skill 生成
EOF

echo "✅ 评估报告已保存到: openclaw-assessment-$timestamp.md"
echo ""
echo "🚀 开始你的OpenClaw之旅吧！使用 how-to-do skill 获取更多帮助。"
# 🎨 ComfyUI 图像生成技能

一个智能的 AI 图像生成技能，根据上下文自动选择最佳处理方式。

## ✨ 核心特性
- ✅ **智能上下文感知** - 自动检测飞书上下文并适配
- ✅ **统一技能入口** - 一个接口处理所有场景
- ✅ **自动飞书发送** - 有飞书上下文时自动发送
- ✅ **高质量输出** - 1080×1920 高清图片
- ✅ **灵活配置** - 支持自定义目标和处理方式

## 🧠 智能处理逻辑
根据调用上下文自动选择最佳方式：

### 场景1：飞书环境调用
- **飞书群聊** → 自动发送到当前群
- **飞书私聊** → 自动发送到当前用户
- **指定目标** → 发送到指定用户/群聊

### 场景2：非飞书环境调用
- **Web界面** → 返回图片对象供 OpenClaw 显示
- **命令行** → 返回图片路径
- **API调用** → 返回结构化结果

## 📁 文件结构
```
comfyui-img-gen/
├── skill.md              # 统一技能文档
├── README.md            # 本文件
├── EXAMPLE.md           # 使用示例
├── unified_skill.py     # 统一技能处理器（推荐）
├── draw.py             # 图片生成核心脚本
├── send_to_feishu.py   # 传统发送工具（兼容）
├── zimage-api.json     # ComfyUI 工作流配置
└── output_images/      # 生成的图片目录
```

## 🚀 快速开始

### 1. 统一技能调用（推荐）
```python
# 在 OpenClaw 技能中
from unified_skill import unified_skill_handler

# 智能处理：根据上下文自动选择方式
result = unified_skill_handler(
    prompt="一辆黄色跑车",
    context={"feishu_user_id": "ou_xxxxxxxx"},  # 可选上下文
    target="user:ou_xxxxxxxx"  # 可选指定目标
)

# 结果自动适配：
# - 有飞书目标: 发送并返回状态
# - 无飞书目标: 返回图片对象
```

### 2. 命令行使用
```bash
# 基础生成
python3 unified_skill.py "提示词"

# 指定飞书目标
python3 unified_skill.py "提示词" --target "user:ou_xxxxxxxx"

# 带上下文信息
python3 unified_skill.py "提示词" --context-json '{"feishu_chat_id":"oc_xxxxxxxx"}'
```

### 3. 传统方式（向后兼容）
```bash
# 仅生成图片
python3 draw.py "你的创意提示词"

# 生成并发送到飞书
python3 send_to_feishu.py "提示词" --user ou_xxxxxxxx

## 🔧 配置要求

### 系统要求
- **ComfyUI 服务**：运行在 127.0.0.1:8188
- **Python 3.8+**：运行脚本
- **OpenClaw**：飞书发送功能需要 OpenClaw 环境

### 飞书权限
需要以下飞书应用权限：
- `im:message:send_as_bot` - 发送消息
- `im:message` - 消息操作

## 📖 详细文档
- **[skill.md](skill.md)** - 完整技能说明和 API 文档
- **[EXAMPLE.md](EXAMPLE.md)** - 详细使用示例和测试记录

## 🎯 使用场景

### 场景1：个人创作
```bash
# 生成个人艺术作品
python3 draw.py "星空下的孤独旅人，梵高风格"
```

### 场景2：团队协作
```bash
# 生成设计稿并发送到团队群
python3 send_to_feishu.py "产品界面设计稿" --chat oc_team_design
```

### 场景3：内容生产
```bash
# 批量生成社交媒体图片
for theme in "春天" "夏天" "秋天" "冬天"; do
    python3 draw.py "${theme}主题海报"
done
```

## 🔍 测试验证
本技能已经过全面测试：
- ✅ ComfyUI 连接测试
- ✅ 图片生成测试
- ✅ 飞书发送测试
- ✅ 错误处理测试

## 📞 支持与反馈
如有问题或建议，请：
1. 检查 `EXAMPLE.md` 中的故障排除部分
2. 验证 ComfyUI 服务状态
3. 确认飞书权限配置

## 📄 许可证
本技能遵循 OpenClaw 技能开发规范，可自由使用和修改。

---
**最后更新**: 2026-03-06  
**版本**: 1.1.0  
**作者**: yun 技能开发团队

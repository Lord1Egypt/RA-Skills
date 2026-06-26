# 🎨 grsai nano-banana 生图技能

> 使用 grsai 平台的 nano-banana 系列模型生成高质量图片

---

## ⚡ 快速开始

### 1. 获取 API Key

1. 访问 https://grsai.ai/zh/dashboard
2. 注册/登录 → API Key 管理 → 创建 Key
3. **充值**（重要！）

### 2. 使用方式

**对话模式（推荐）：**
```
直接告诉助理你的需求，助理会引导确认方案
```

**命令行：**
```bash
cd ~/.openclaw/workspace/skills/grsai-nano-banana

# 文生图
uv run generate.py --prompt "可爱柴犬头像" --aspect-ratio "1:1" --api-key "sk-xxx"

# 图生图
uv run generate.py --prompt "油画风格" --input-image "https://example.com/img.png" --api-key "sk-xxx"
```

### 3. 查看结果

图片保存在：`./generated/` 目录（或自定义目录）

---

## 📖 详细文档

查看 [SKILL.md](./SKILL.md) 了解：
- 完整参数说明
- API 获取方法
- 常见问题与踩坑记录
- 技术细节

---

## 🆘 遇到问题？

查看 SKILL.md 中的 **常见问题与踩坑记录** 章节，或：
1. 检查 grsai 账户余额
2. 确认 API Key 正确
3. 调整提示词（避免敏感内容）

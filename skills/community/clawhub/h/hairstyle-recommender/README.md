# Hairstyle Recommender

一个 AI 驱动的发型推荐 Skill，通过分析人像照片，根据脸型、五官、发质等因素推荐最适合的发型。

## 功能

- 📸 **人像分析**：分析脸型、五官比例、发质发量等特征
- 💇 **智能推荐**：为男性和女性用户提供个性化发型建议
- 📝 **剪法指南**：提供详细的理发师沟通话术
- 🎨 **效果图生成**：支持生成发型推荐后的效果图

## 适用场景

- 想换发型但不知道适合什么风格
- 需要给理发师提供明确的剪发要求
- 根据脸型和发质获取专业建议

## 文件结构

```
hairstyle-recommender/
├── SKILL.md              # Skill 主文件
└── references/
    └── hairstyles.md     # 发型知识参考库
```

## 使用方法

作为 OpenClaw 的 Skill 使用。当用户上传人像照片并询问发型建议时，Skill 会自动触发。

## 安装

```bash
# 将 skill 文件夹复制到 OpenClaw skills 目录
cp -r hairstyle-recommender ~/.kimi_openclaw/workspace/skills/
```

## 打包

```bash
# 使用 OpenClaw 的 package_skill.py 打包
python3 package_skill.py hairstyle-recommender/
```

## License

MIT

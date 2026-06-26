# 发布到 ClawHub.ai 指南

## 准备工作

已为你准备好以下发布文件：

```
model-distill-skill/
├── skill.yaml          # 技能元数据
├── SKILL.md            # 主技能定义
├── README.md           # 说明文档
├── CHANGELOG.md        # 版本历史
├── .clawhub/
│   ├── manifest.json   # 平台清单
│   └── publish-notes.md # 发布说明
└── assets/
    └── icon.svg        # 图标
```

## 发布步骤

### 1. 打包技能

```bash
# 进入技能目录
cd D:\AI编程\skill\nuwa-skill-main\model-distill-skill

# 创建发布包（不包含大型模型文件）
zip -r model-distill-master-v1.0.0.zip . \
  -x "*.pyc" "__pycache__/*" ".git/*" "models/*" "outputs/*"
```

### 2. 登录 ClawHub.ai

访问 https://clawhub.ai/publish-skill

### 3. 填写表单

| 字段 | 填写内容 |
|------|----------|
| 技能名称 | 模型蒸馏大师 |
| 英文名 | model-distill-master |
| 分类 | AI/机器学习 |
| 标签 | model-distillation, gemma, qlora, fine-tuning |
| 版本 | 1.0.0 |
| 简介 | 将大模型能力迁移到小模型的完整工作流 |

### 4. 上传文件

- **主文件**: 上传 `model-distill-master-v1.0.0.zip`
- **图标**: 上传 `assets/icon.svg`
- **文档**: SKILL.md 内容已包含在zip中

### 5. 提交审核

- 检查所有必填项
- 点击"提交审核"
- 等待平台审核（通常1-3个工作日）

## 发布检查清单

- [ ] 所有Python脚本可正常导入
- [ ] 配置文件格式正确（YAML）
- [ ] SKILL.md 格式符合规范
- [ ] 无敏感信息/密钥
- [ ] README 包含使用说明
- [ ] 版本号已更新

## 发布后

发布后可通过以下方式安装：

```bash
# 通过 ClawHub CLI
clawhub skill install model-distill-master

# 或在 Claude Code 中使用
/distill模型：把 GPT-4 蒸馏到 gemma
```

## 联系方式

如有问题，可在 ClawHub 社区发帖或联系 support@clawhub.ai

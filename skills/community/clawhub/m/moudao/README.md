# 谋道 - 基于「道法术器」框架的AI规划专家

<div align="center">

**谋于道，行于术**

把任何想法变成可执行方案

</div>

---

## 简介

谋道是一个基于中国传统智慧「道法术器」认知框架的AI规划工具。无论你想做什么，帮你从任意层级补齐完整方案，并持续迭代。

## 核心功能

- **快速方案**：10秒生成初步方案
- **深度规划**：天时地利人和 × 道法术器完整分析
- **迭代诊断**：诊断问题层级，给出调整建议

## 安装使用

### 环境要求

- Node.js >= 14.0.0
- DeepSeek API Key（或其他兼容OpenAI格式的API）

### 快速开始

```bash
# 设置API密钥
export DEEPSEEK_API_KEY="your-api-key"

# 快速方案
node scripts/moudao.js --quick "我想做直播"

# 深度规划
node scripts/moudao.js --deep "我想做副业" --profile "上班族，每周10小时"

# 迭代诊断
node scripts/moudao.js --diagnose "没人看" --context "我想做直播"
```

## 输出格式

支持三种输出格式：

- `md` - Markdown格式（默认，适合阅读）
- `json` - JSON格式（适合程序处理）
- `text` - 纯文本格式

```bash
node scripts/moudao.js --quick "我想做直播" --format json
```

## 文件结构

```
moudao/
├── SKILL.md              # 扣子技能主文档
├── README.md             # 本文件
├── package.json          # 包信息
├── scripts/
│   └── moudao.js         # 核心规划脚本
└── references/
    ├── framework.md      # 道法术器框架详解
    └── examples.md       # 使用案例
```

## 上架扣子技能商店

1. 登录 [扣子工作台](https://www.coze.cn/)
2. 进入「技能」→「创建技能」
3. 选择「手动创建」或「上传文件包」
4. 填写技能信息：
   - 名称：谋道 - AI规划专家
   - 描述：基于道法术器框架，把任何想法变成可执行方案
   - 分类：效率工具 / 职场提升
5. 设置定价：订阅制 9.9元/月
6. 开通商户收款账户
7. 上架发布

## 许可证

MIT License

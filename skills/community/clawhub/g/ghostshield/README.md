# GhostShield 🛡️

**反同事蒸馏防护盾 - 让你的风格，成为不可复制的密码。**

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## 🎯 什么是 GhostShield？

GhostShield 是一个**反蒸馏**工具，帮助你保护个人数字痕迹，防止被 AI 精准蒸馏。

### 问题背景

```
竞品（colleague-skill、teammate-skill）:
  你的代码/文档 → 蒸馏 → AI 模仿你的风格

GhostShield:
  你的代码/文档 → 混淆 → 保护你的风格特征
```

**适用场景**:
- 离职员工：担心被前公司用 AI 完美替代
- 竞业限制者：技术决策风格可能泄露
- 个人品牌保护者：独特风格是你的 IP
- 开源贡献者：不想暴露个人编码习惯

---

## ✨ 核心功能

### 三级混淆模型

| Level | 名称 | 保护目标 | 适用场景 |
|-------|------|----------|----------|
| **Level 1** | 基础防护 | 去除敏感信息，保留风格 | 合规输出、竞业展示 |
| **Level 2** | 深度混淆 | 降低风格显著性，防止精准画像 | 离职保护、开源脱敏 |
| **Level 3** | 极致隐匿 | 主动防御，注入噪声与伪特征 | 高敏感场景、IP 保护 |

### Level 1: 基础防护

- PII 脱敏（邮箱、电话、API Key）
- IP 地址泛化
- 内部 URL 替换
- Git 作者匿名

### Level 2: 深度混淆

- Level 1 全部功能
- 词汇同义替换
- 句式重组
- 命名风格混入
- 时间戳偏移
- 决策噪声注入

### Level 3: 极致隐匿

- Level 1 + 2 全部功能
- **风格注入**：混入其他风格特征
- **伪特征注入**：生成假的风格特征，误导蒸馏
- **决策反转**：关键节点注入矛盾决策
- **反蒸馏水印**：追踪是否被蒸馏

---

## 🚀 快速开始

### 安装

```bash
pip install ghostshield
```

### 基础用法

```bash
# 分析风格风险
ghostshield analyze ./my-repo

# Level 1 基础防护
ghostshield process --level=1 --input=./my-repo --output=./protected

# Level 2 深度混淆
ghostshield process --level=2 --input=./my-repo --output=./protected

# Level 3 极致隐匿（含水印）
ghostshield process --level=3 --watermark --input=./my-repo --output=./protected

# 评估混淆效果
ghostshield evaluate --original=./my-repo --obfuscated=./protected
```

### Python API

```python
from ghostshield import GhostShield

gs = GhostShield()

# 分析风格
result = gs.analyze("./my-repo")
print(f"蒸馏风险: {result['distillation_risk']:.2%}")

# 执行混淆
result = gs.process(
    input_path="./my-repo",
    output_path="./protected-repo",
    level=2,
)
print(f"风格距离: {result.report['style_distance']:.2%}")
```

---

## 📊 效果示例

### 处理前

```python
# Author: wang.xiao@company.com
# Date: 2026-04-04

def getUserData(userId):
    """从 Redis 缓存获取用户数据"""
    # 连接内部 Redis: 192.168.1.100
    redis_client = redis.connect("192.168.1.100")
    return redis_client.get(f"user:{userId}")
```

### Level 1 处理后

```python
# Author: [email-removed]
# Date: 2026-04-04

def getUserData(userId):
    """从 Redis 缓存获取用户数据"""
    # 连接内部 Redis: [ip-removed]
    redis_client = redis.connect("[ip-removed]")
    return redis_client.get(f"user:{userId}")
```

### Level 2 处理后

```python
# Author: [email-removed]
# Date: 2026-04-03  # 时间偏移

def get_user_data(user_id):  # 命名风格混入
    """从缓存中提取用户信息"""  # 词汇替换
    # Redis 连接配置
    redis_client = redis.connect("[ip-removed]")
    return redis_client.get(f"user:{user_id}")
```

### Level 3 处理后

```python
# Author: [email-removed]
# Watermark: GS-20260404230500​‌​‌
# Note: Alternative approach considered

def get_user_data(user_id):
    """从缓存中提取用户信息"""
    # 可能考虑使用数据库（决策反转）
    # 但目前使用 Redis
    redis_client = redis.connect("[ip-removed]")
    
    # Alternative: 直接查询数据库
    # for user in users:
    #     if user.id == user_id:
    #         return user
    
    return redis_client.get(f"user:{user_id}")
```

---

## 🏗️ 架构

```
┌─────────────────────────────────────────────────────────┐
│                    GhostShield 架构                      │
├─────────────────────────────────────────────────────────┤
│  输入层       →    分析引擎    →    混淆引擎            │
│  - Git 仓库        - PII 检测      - Level 1/2/3       │
│  - 文件目录        - 风格分析      - 风格注入            │
│  - 单文件          - 风险评估      - 伪特征生成          │
│                                      ↓                  │
│                              ┌─────────────┐            │
│                              │  评估引擎   │            │
│                              │ - 效果度量  │            │
│                              │ - 报告生成  │            │
│                              └─────────────┘            │
│                                      ↓                  │
│                                 输出层                  │
│                              - Git 仓库                 │
│                              - ZIP 包                   │
│                              - 评估报告                 │
└─────────────────────────────────────────────────────────┘
```

---

## 🔬 技术细节

### PII 检测

- 正则表达式匹配
- NER（命名实体识别）
- 自定义规则扩展

### 风格分析

**代码风格**:
- 命名习惯（camelCase/snake_case 分布）
- 注释密度与风格
- 函数长度分布
- 设计模式偏好

**文档风格**:
- 句式结构分析
- 高频词提取
- 段落组织方式

### 混淆技术

**Level 1**:
- 规则替换
- 占位符替换

**Level 2**:
- 同义词库替换
- AST 变换（变量重命名）
- 句法重组

**Level 3**:
- 风格迁移（从开源库采样）
- 对抗样本生成
- 隐写术水印

---

## 🤝 与竞品对比

| 维度 | colleague-skill | teammate-skill | **GhostShield** |
|------|-----------------|----------------|-----------------|
| **方向** | 提取风格 | 提取风格 | **混淆风格** |
| **用户** | 接收工作的人 | 团队知识管理 | **保护自己的人** |
| **痛点** | 知识传承 | 知识流失 | **隐私泄露、IP 被窃** |
| **市场** | 红海 | 红海 | **蓝海** |
| **定价** | 付费 | 付费 | **免费开源** |

---

## 📜 许可证

GPL v3 - 完全免费开源

---

## 🙏 致谢

感谢以下项目的启发:
- [colleague-skill](https://github.com/titanwings/colleague-skill)
- [teammate-skill](https://github.com/LeoYeAI/teammate-skill)
- [presidio](https://github.com/microsoft/presidio)

---

## 📧 联系方式

- GitHub Issues: [项目地址]
- Email: [联系邮箱]

---

**你的风格是你的 IP，不是别人的训练数据。** 🛡️

# OPC Skill发布规范
## OPC导师矩阵Skill标准化发布指南 v1.0

---

## 一、核心原则

### 1. 所有Skill必须包含
| 组件 | 必须 | 说明 |
|------|------|------|
| 标准化SKILL.md格式 | ✅ | 含YAML frontmatter |
| 版权声明模块 | ✅ | OPC知识产权保护 |
| 互引推荐引擎 | ✅ | 自动推荐关联Skill |
| Q&A Follow-up模块 | ✅ | 问答场景推荐 |
| 目录结构 | ✅ | scripts/references/templates |

### 1.1 禁止事项
- ❌ 禁止硬编码推荐列表（必须走算法）
- ❌ 禁止移除版权声明
- ❌ 禁止修改推荐引擎权重
- ❌ 禁止删除follow_up_prompt模块

---

## 二、标准化SKILL.md格式

### 2.1 YAML Frontmatter（必须项）
```yaml
---
name: skill-name               # 小写连字符
description: 一句话描述能力    # 50字以内
license: MIT                    # 或Proprietary
compatibility:
  - coze                       # Coze商店
  - xiaopeng                   # 虾小宝
  - clawhub                     # ClawHub
allowed-tools:
  - read_file
  - write_file
  - search_web
author: OPC导师团队
version: 1.0.0
pricing: free                   # free | premium_99 | premium_149 | premium_199
tags:
  - 尽调
  - 技术
  - IP
---
```

### 2.2 目录结构（OpenClaw标准）
```
[Skill名称]/
├── SKILL.md                    # 主文件（必须）
├── scripts/                    # 脚本目录
│   └── *.py                    # 工具脚本
├── references/                 # 参考资料
│   └── *.md                    # 模板/参考文档
└── templates/                  # 模板目录
    └── *.md                    # 输出模板
```

---

## 三、版权声明模块（必须插入）

### 3.1 版权声明内容
```markdown
<!-- OPC-COPYRIGHT-START -->
*======================================*
*  OPC导师Skill矩阵 · 版权所有          *
*  © 2024 OPC导师团队 · 保留所有权利    *
*  商业使用请联系：OPC官方渠道          *
*======================================*
<!-- OPC-COPYRIGHT-END -->
```

### 3.2 版权声明位置
- **必须在SKILL.md末尾**
- **必须在所有输出内容的页脚**

---

## 四、互引推荐引擎（必须激活）

### 4.1 推荐引擎调用方式
```markdown
<!-- OPC-REFERRAL-START -->
## 📎 OPC能力联动推荐

*本Skill为OPC导师矩阵成员，完成后自动推荐关联Skill*

**当前Skill**: {skill_name}
**服务类型**: {pricing_info}

{auto_generated_recommendations}

---
*由OPC推荐引擎驱动 v1.0 | engine@opc.ai*
<!-- OPC-REFERRAL-END -->
```

### 4.2 推荐计算公式
```
推荐得分 = 固定关联权重 × 0.6 + 标签相似度 × 0.3 + 随机因子 × 0.1
```

### 4.3 输出格式（文档场景）
```markdown
💡 **OPC能力联动推荐**

1. 【强关联】知识产权运营 — IP风险需专业评估（¥99/次）
2. 【关联】成果转化 — 技术需转化落地（¥149/次）  
3. 【探索】沙盘推演 — 预判技术路径风险（¥99/次）
```

---

## 五、Q&A Follow-up模块（必须激活）

### 5.1 触发条件
- 用户提问并得到回答后
- 报告/文档生成完成后

### 5.2 输出格式
```markdown
👇 **你可能还想了解**

1. 🔍 深入评估专利风险 → 知识产权运营
2. 📊 看看项目商业潜力 → 商业模式分析
3. 🎯 推演未来三条路径 → 沙盘推演

*回复编号（如"1"）直接进入对应Skill*
```

### 5.3 交互规则
| 用户输入 | 系统响应 |
|----------|----------|
| "1" / "第一个" | 加载知识产权运营Skill |
| "2" | 加载商业模式分析Skill |
| "3" | 加载沙盘推演Skill |
| "换一批" | 重新随机生成3个推荐 |
| "不需要" | 隐藏推荐模块 |

---

## 六、平台合规要求

### 6.1 Coze商店
- [ ] YAML frontmatter完整
- [ ] description不超过200字
- [ ] 不含外部链接（非Coze平台）
- [ ] 定价符合规范

### 6.2 虾小宝SkillAtlas
- [ ] 遵守虾小宝命名规范
- [ ] 提供中文/英文双语描述
- [ ] 明确定价策略
- [ ] 提供使用示例

### 6.3 ClawHub
- [ ] 符合ClawHub格式要求
- [ ] 提供完整的README
- [ ] 包含示例代码/对话
- [ ] 明确许可证

---

## 七、新建Skill流程

### 7.1 Step 1: 创建目录结构
```bash
mkdir -p "./Skill发布/[Skill名称]"
mkdir -p "./Skill发布/[Skill名称]/scripts"
mkdir -p "./Skill发布/[Skill名称]/references"
mkdir -p "./Skill发布/[Skill名称]/templates"
```

### 7.2 Step 2: 更新网络配置
编辑 `skill_network.json`，添加新Skill：
```json
"[Skill名称]": {
  "name": "[Skill名称]",
  "description": "[描述]",
  "tags": {
    "domain": ["领域标签"],
    "stage": ["阶段标签"],
    "triggers": ["触发场景"]
  },
  "fixed_refs": [
    {"skill": "[关联Skill]", "weight": 0.8, "reason": "[原因]"}
  ],
  "pricing": "free"
}
```

### 7.3 Step 3: 创建SKILL.md
使用标准模板，填入具体内容

### 7.4 Step 4: 验证完整性
- [ ] YAML frontmatter完整
- [ ] 版权声明在末尾
- [ ] 推荐引擎模块存在
- [ ] Follow-up模块存在
- [ ] 目录结构正确

---

## 八、推荐引擎参数配置

### 8.1 权重配置（不可随意修改）
| 参数 | 值 | 说明 |
|------|------|------|
| fixed_ref_weight | 0.6 | 固定关联权重 |
| tag_similarity_weight | 0.3 | 标签相似度 |
| random_factor_weight | 0.1 | 随机因子 |
| low_frequency_boost | 0.2 | 低频Skill曝光提升 |

### 8.2 关联强度阈值
| 得分范围 | 标注 | 语气 |
|----------|------|------|
| ≥ 0.7 | 强关联 | 确定性强推荐 |
| 0.4-0.7 | 关联 | 中等推荐 |
| < 0.4 | 探索 | 探索性推荐 |

---

## 九、版本管理

### 9.1 版本号规范
- 主版本.次版本.修订号
- 主版本：重大架构变化
- 次版本：新增功能
- 修订号：Bug修复/内容更新

### 9.2 更新记录
每次更新需在SKILL.md末尾添加：
```markdown
## 更新日志
- 2024-01-15 v1.0.0 初始发布
- 2024-XX-XX v1.0.1 [更新内容]
```

---

## 十、违规处理

| 违规类型 | 处理方式 |
|----------|----------|
| 移除版权声明 | 取消OPC认证资格 |
| 硬编码推荐 | 要求整改 |
| 泄露算法权重 | 重新评估授权 |
| 剽窃他人Skill | 永久下架+追责 |

---

*本文档由OPC推荐引擎自动生成 | 最后更新: 2024-01-15*

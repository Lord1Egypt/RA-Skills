# Investment Buddy Pet - 投资宠物技能

**12 只宠物，1 个通用 Skill，通过配置文件区分宠物人格**

---

## 🎯 架构设计

```
investment-buddy-pet/           # 1 个通用 Skill
├── SKILL.md                    # 通用技能文档
├── clawhub.json                # ClawHub 发布配置
├── pets/                       # 13 个宠物配置文件
│   ├── songguo.json           # 🐿️ 松果
│   ├── wugui.json             # 🐢 慢慢
│   ├── maotouying.json        # 🦉 智多星
│   └── ... (13 个)
├── scripts/                    # 通用脚本
│   ├── personality_test.py    # 20 题投资性格测试
│   ├── pet_match.py           # 宠物匹配测试
│   ├── heartbeat_engine.py    # 心跳引擎（支持 pet_type）
│   ├── compliance_checker.py  # 金融合规检查器
│   └── viral_growth.py        # 病毒传播
├── docs/                       # 文档
│   └── knowledge/             # 知识库（5 个核心文档）
├── templates/                  # 模板
├── data/                       # 用户数据
└── assets/                     # 素材
```

---

## 🐾 13 只宠物

| 宠物 | emoji | 投资风格 | 沟通风格 | 主动性 | 适合人群 |
|------|-------|---------|---------|--------|---------|
| 🐿️ 松果 | songguo | 谨慎定投 | 温暖 | 40 | 保守型新手 |
| 🐢 慢慢 | wugui | 长期主义 | 平静 | 30 | 超长期投资者 |
| 🦉 智多星 | maotouying | 理性分析 | 理性 | 70 | 理性分析派 |
| 🐺 孤狼 | lang | 激进成长 | 果断 | 85 | 追求高收益 |
| 🐘 稳稳 | daxiang | 稳健配置 | 平静 | 40 | 平衡型投资者 |
| 🦅 鹰眼 | ying | 趋势交易 | 果断 | 70 | 趋势交易者 |
| 🦊 狐狐 | huli | 灵活配置 | 机智 | 60 | 资产配置者 |
| 🐬 豚豚 | haitun | 指数投资 | 友好 | 50 | 被动投资者 |
| 🦁 狮王 | shizi | 集中投资 | 勇敢 | 85 | 集中持仓者 |
| 🐜 蚁蚁 | mayi | 分散投资 | 谨慎 | 45 | 风险厌恶者 |
| 🐪 驼驼 | luotuo | 逆向投资 | 理性 | 55 | 逆向投资者 |
| 🦄 角角 | dunjiaoshou | 成长投资 | 远见 | 80 | 科技成长派 |
| 🐎 马马 | junma | 行业轮动 | 活力 | 70 | 行业轮动者 |

---

## 🚀 快速开始

### 方式 1：ClawHub 安装（推荐）

```bash
clawhub install investment-buddy-pet
```

### 方式 2：手动安装

```bash
# 克隆仓库
git clone git@github.com:lj22503/investment-buddy-pet.git

# 复制技能到 OpenClaw
cp -r investment-buddy-pet ~/.openclaw/skills/

# 运行测试
cd investment-buddy-pet
python3 scripts/pet_match.py
```

---

## 📋 核心功能

### 1. 投资性格测试

20 道题目，评估五维投资性格：
- 风险承受力
- 知识水平
- 决策风格
- 情绪稳定性
- 时间偏好

**运行测试**：
```bash
python3 scripts/personality_test.py
```

### 2. 宠物匹配

基于五维评分，计算与 13 只宠物的兼容度，推荐 Top 3。

### 3. 宠物激活

激活选中的宠物，配置心跳任务。

### 4. 心跳陪伴

宠物主动触发对话，提供：
- 情感陪伴
- 定投提醒
- 市场波动安抚
- 投资者教育

---

## 📚 知识库文档

| 文档 | 说明 |
|------|------|
| PET_KNOWLEDGE_BASE.md | 12 只宠物完整人格设定 |
| INVESTMENT_PERSONALITY_ONTOLOGY.md | 五维投资性格分类体系 |
| CONVERSATION_TEMPLATES.md | 3 类触发器×13 宠物对话模板 |
| TASK_GENERATION_RULES.md | 8 大触发规则 +5 类任务生成 |
| PET_RELATION_GRAPH.md | ECharts+Neo4j 关系图谱 |

---

## 🔧 使用示例

### 运行性格测试

```bash
cd /path/to/investment-buddy-pet
python3 scripts/personality_test.py
```

### 激活宠物

```bash
python3 scripts/heartbeat_engine.py start --user-id <your_user_id> --pet-type songguo
```

---

## 📦 发布到 ClawHub

```bash
# 确保 clawhub.json 配置正确
cd /path/to/investment-buddy-pet

# 发布
clawhub publish . --version "1.0.0"
```

---

## 📊 项目状态

- ✅ 本地开发完成
- ⏳ 等待 GitHub 仓库创建
- ⏳ 等待 ClawHub 发布

---

## 🎯 相关项目

| 项目 | 用途 | 状态 |
|------|------|------|
| **investment-buddy-pet** | 主技能 | ✅ 完成 |
| **mangofolio-h5** | 投资人格测试 H5 | ✅ 完成 |

**用户流程**：
```
mangofolio-h5 (测试页面)
    ↓ 测试完成 → 推荐宠物
    ↓ 下载技能
investment-buddy-pet (主技能)
    ↓ 激活宠物 → 心跳陪伴
用户投资成长
```

---

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)。

**Copyright (c) 2026 燃冰 (燃冰 & ant)**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

**简单来说：**
- ✅ 你可以自由使用、修改、分发、商用
- ✅ 需要保留原作者版权和许可证声明
- ❌ 不提供任何担保，使用风险自负

**合规声明：**
- 本技能仅提供投资陪伴和情绪安抚
- 不推荐具体基金/股票
- 不承诺收益/保本
- 宠物陪伴不替代专业投资建议

详见 [LICENSE](LICENSE) 和 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

**创建时间**：2026-04-10  
**最后更新**：2026-04-14  
**版本**：v1.0.4  
**作者**：燃冰 + ant

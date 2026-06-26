# Prompt-Router

> 🚀 基于文本匹配的快速路由引擎，为简单任务提供 **零 LLM 决策** 的快速路径

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/xiaobu-openclaw/prompt-router)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://github.com/openclaw/openclaw)

---

## 🌟 特性

- ⚡ **极速响应** - <10ms 路由决策（vs 500ms+ LLM 推理）
- 💰 **零成本** - 简单任务无需 LLM 调用，节省 50%+ Token
- 🛡️ **可降级** - LLM 故障时仍可工作，提供降级方案
- 🎯 **确定性** - 相同输入始终相同输出，可预测、可调试
- 🌐 **中英文支持** - 完美支持中英文混合输入

---

## 📦 安装

### 方式 1：ClawHub 安装（推荐）

```bash
clawhub install prompt-router
```

### 方式 2：虾评平台安装

访问虾评 Skill 平台搜索 `prompt-router` 安装

### 方式 3：手动安装

```bash
# 克隆仓库
git clone https://github.com/xiaobu-openclaw/prompt-router.git

# 复制到 OpenClaw skills 目录
cp -r prompt-router ~/.openclaw/workspace/skills/
```

---

## 🚀 快速开始

### 基础用法

```python
from skills.prompt_router.scripts.router import PromptRouter

# 创建路由器
router = PromptRouter(
    skills_dir='~/.openclaw/workspace/skills',
    confidence_threshold=0.25  # 置信度阈值
)

# 加载技能
router.load_skills()

# 路由用户消息
result = router.route("搜索 Python 教程")

if result.match:
    print(f"匹配技能：{result.match['name']}")
    print(f"置信度：{result.confidence:.2f}")
    print(f"应该调用：{router.should_invoke_skill(result)}")
else:
    print("未找到匹配，降级到 LLM")
```

### 集成脚本

```bash
# 命令行调用
python ~/.openclaw/workspace/skills/prompt-router/scripts/integration.py "搜索 Python 教程"
```

**返回 JSON：**
```json
{
  "matched": true,
  "skill_name": "multi-search-engine",
  "confidence": 0.35,
  "should_invoke": true
}
```

---

## 📖 文档

### 核心文档

- [使用指南](SKILL.md) - 完整的技能使用说明
- [集成方案](INTEGRATION_PLAN.md) - 如何集成到 OpenClaw 主流程
- [测试报告](TEST_REPORT.md) - 详细的测试结果
- [集成完成报告](INTEGRATION_COMPLETE.md) - 集成状态和验收清单

### API 参考

#### PromptRouter 类

```python
class PromptRouter:
    def __init__(
        self,
        skills_dir: str = None,
        confidence_threshold: float = 0.25,
        high_confidence_threshold: float = 0.5,
    )
    
    def load_skills(self, skills_dir: str = None) -> int
    def route(self, prompt: str, limit: int = 3) -> RouteResult
    def should_invoke_skill(self, result: RouteResult) -> bool
    def should_fallback_to_llm(self, result: RouteResult) -> bool
```

#### RouteResult 类

```python
@dataclass
class RouteResult:
    match: Optional[Dict]      # 匹配的技能
    score: float               # 匹配分数
    confidence: float          # 置信度 (0-1)
    confidence_level: str      # high/medium/low/none
    all_matches: List[Dict]    # 所有匹配
```

---

## 🎯 工作原理

### 路由流程

```
用户 Prompt
    ↓
分词处理（Tokenizer）
    ↓
评分匹配（Scorer）
    ↓
排序选择（Router）
    ↓
{
    高置信度 (≥0.5) → 直接调用技能
    中置信度 (0.25-0.5) → 建议用户确认
    低置信度 (<0.25) → 降级到 LLM
}
```

### 评分算法

```python
# 多字段加权匹配
总分 = Σ(字段匹配分 × 权重)

字段权重：
- name: 3.0（名称匹配最重要）
- triggers: 2.5（触发词权重高）
- keywords: 2.0（关键词）
- description: 1.5（描述）
```

---

## 📊 性能指标

| 指标 | 目标值 | 实测值 | 状态 |
|------|--------|--------|------|
| 路由延迟 | <10ms | 7.38ms | ✅ |
| 分词速度 | <1ms | ~0.5ms | ✅ |
| 评分速度 | <5ms | ~2ms | ✅ |
| 内存占用 | <10MB | ~5MB | ✅ |
| 启动时间 | <100ms | ~50ms | ✅ |

### 对比 LLM 路由

| 指标 | Prompt-Router | LLM 路由 | 提升 |
|------|---------------|----------|------|
| 延迟 | 7.38ms | 500-2000ms | **100-200x** |
| 成本 | ¥0 | ¥0.003-0.005 | **100% 节省** |
| 确定性 | 100% | 概率性 | **可预测** |

---

## 🧪 测试

### 运行测试

```bash
# 单元测试
cd prompt-router
python -m pytest tests/

# 集成测试
python test_integration.py

# 性能测试
python tests/benchmark.py
```

### 测试结果

- ✅ 功能测试：14/14 通过（100%）
- ✅ 性能测试：7.38ms 平均延迟
- ✅ 路由成功率：71.4%（简单任务）

---

## 🛠️ 配置

### 置信度阈值

```python
router = PromptRouter(
    confidence_threshold=0.25,      # 低于此值降级到 LLM
    high_confidence_threshold=0.5,  # 高于此值直接调用
)
```

**调整建议：**
- 提高阈值 → 更准确，但更多降级到 LLM
- 降低阈值 → 更快，但可能误匹配

### 技能元数据

技能需要在 `SKILL.md` 中定义 triggers 和 keywords：

```yaml
---
name: multi-search-engine
description: Multi search engine integration
triggers: 搜索，查找，search, find, 查询，检索
keywords: search, engine, multi, 搜索，查找，查询
---
```

---

## 📦 项目结构

```
prompt-router/
├── SKILL.md                    # 技能主文档
├── README.md                   # 本文档
├── scripts/
│   ├── router.py              # 核心路由引擎
│   ├── tokenizer.py           # 中英文分词器
│   ├── scorer.py              # 评分算法
│   └── integration.py         # 集成脚本
├── tests/
│   ├── test_router.py         # 路由测试
│   ├── test_integration.py    # 集成测试
│   └── benchmark.py           # 性能测试
├── data/                       # 数据文件（词典等）
├── references/                 # 参考资料
├── TEST_REPORT.md             # 测试报告
├── INTEGRATION_PLAN.md        # 集成方案
└── INTEGRATION_COMPLETE.md    # 集成完成报告
```

---

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

### 提交 Issue

- 🐛 **Bug 报告** - 描述问题、复现步骤、期望行为
- 💡 **功能建议** - 描述需求、使用场景
- 📝 **文档改进** - 拼写错误、翻译、示例

### 提交 PR

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发指南

- 遵循 PEP 8 代码风格
- 添加单元测试
- 更新文档
- 确保测试通过

---

## 📈 路线图

### v1.0.0（当前版本）✅

- [x] 核心路由引擎
- [x] 中英文分词器
- [x] 多字段评分算法
- [x] 置信度阈值
- [x] LLM 降级机制
- [x] OpenClaw 集成

### v1.1.0（计划中）

- [ ] 动态学习机制（根据用户反馈调整）
- [ ] 支持 OpenClaw 内置工具路由
- [ ] 路由日志和监控
- [ ] 性能优化（目标<3ms）

### v2.0.0（未来）

- [ ] 多语言支持（日语、韩语等）
- [ ] 技能推荐系统
- [ ] 集成到 OpenClaw 核心层
- [ ] 可视化配置界面

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- [OpenClaw](https://github.com/openclaw/openclaw) - Agent 框架
- [Claude Leak](references/ClaudeLeak-Router-Analysis.md) - 路由算法灵感来源
- [虾评 Skill 平台](https://xiaping.coze.site) - 技能分发平台
- [ClawHub](https://clawhub.ai) - 技能市场

---

## 📞 联系方式

- **作者：** 小布 (Xiao Bu) 🦎
- **邮箱：** [你的邮箱]
- **GitHub：** https://github.com/xiaobu-openclaw
- **虾评：** 小布的本地大总管

---

## 📊 统计

![Stars](https://img.shields.io/github/stars/xiaobu-openclaw/prompt-router?style=social)
![Forks](https://img.shields.io/github/forks/xiaobu-openclaw/prompt-router?style=social)

**下载量：**
- ClawHub: [待统计]
- 虾评：[待统计]

---

*最后更新：2026-04-05*

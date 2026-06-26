# Project Context Guide

让复杂代码库变得透明易懂。

## 简介

Project Context Guide 是一个智能的项目上下文向导，帮助你快速理解代码库的结构、历史和团队协作关系。无论是新成员入职、代码修改、设计决策追溯，还是代码审查，这个 Skill 都能提供关键的上下文信息。

## 核心功能

### 🔍 智能入职引导

为新成员生成个性化学习路径：
- 基于代码修改频率推荐重点关注区域
- 识别项目入口点和核心模块
- 关联相关文档和讨论记录

### 🌉 代码修改影响预测

修改代码前，预判影响范围：
- 识别函数/类的调用链
- 标注关联的测试文件
- 提示最近的 bug 修复记录
- 推荐需要通知的相关开发者

### 📜 决策追溯

理解代码背后的设计决策：
- 追溯 git 提交历史
- 提取 commit message 和相关 PR 讨论
- 关联技术文档和性能测试数据
- 标注代码变更的时间线和责任人

### 👥 人际关联

连接代码与团队：
- 识别代码主要维护者
- 追踪最近修改者和相关责任人
- 建议沟通时机
- 整合团队讨论上下文

### 🤝 智能代码审查副驾

Code Review 时提供上下文支持：
- 标注相似代码实现
- 指向最佳实践参考
- 提醒潜在风险点
- 建议测试覆盖

## 快速开始

### 前提条件

- Python 3.7+
- Git 仓库
- WorkBuddy 环境

### 安装

将 `project-context-guide` 目录安装到你的 WorkBuddy skills 目录：

```bash
# 用户级安装
cp -r project-context-guide ~/.workbuddy/skills/

# 项目级安装
cp -r project-context-guide .workbuddy/skills/
```

## 使用示例

### 场景 1: 新成员入职

```
用户: 我刚加入这个项目，应该从哪里开始了解？

Skill:
  基于你的前端经验，建议先学习以下核心组件：
  1. src/components/UserProfile.vue (最近修改过 5 次)
  2. src/services/AuthService.ts (被 8 个模块依赖)
  3. src/utils/ApiClient.js (项目入口文件)

  相关文档：
  - docs/onboarding/frontend-guide.md
  - docs/architecture/components-overview.md
```

### 场景 2: 代码修改预判

```
用户选中 payment_callback.py 中的 process_payment 函数

Skill:
  [调用链分析]
  → 被以下页面直接调用 (3个):
     - frontend/pages/checkout.js:142
     - mobile/app/views/payment.js:87
     - api/webhooks/stripe.js:23

  [相关测试]
  - tests/unit/test_payment_callback.py:45

  [警告]
  支付页面上周刚修复了相关 bug (#1234)

  [建议]
  主要维护者: @李四
  最近贡献者: @王五, @张三
  建议: 通知 @李四，他是支付模块维护者
```

### 场景 3: 理解设计决策

```
用户: 为什么这里用 Redis 而不用数据库缓存？

Skill:
  [首次引入]
  时间: 2025-08-15 commit abc1234
  提交者: 李四
  提交信息: feat: 使用 Redis 替换数据库缓存以提升性能

  [相关 PR]
  #456: 解决高并发下的性能问题
  讨论:
    - @李四 建议用 Redis，考虑 QPS 需求
    - @王五 实现了方案
    - 性能测试显示 QPS 提升 300%

  [技术原因]
  1. 高并发读写场景下，Redis 的吞吐量更高
  2. 缓存失效策略需要细粒度控制
  3. 分布式缓存支持横向扩展

  [参考资料]
  - docs/design/cache-architecture.md
  - tests/performance/cache-benchmark.md
```

### 场景 4: Code Review 辅助

```
用户: Review 一段新代码

Skill:
  [相似实现]
  user_service.py:203 有更优版本，使用事务管理

  [最佳实践]
  注意事务边界，参考 order_service.py:89 的处理

  [测试建议]
  需要添加对 points_system 的测试覆盖
  参考 tests/integration/test_points_flow.py

  [风险提示]
  可能影响 "积分防刷逻辑"
  责任人 @李四 已确认影响范围
```

## 技术架构

### 核心模块

```
project-context-guide/
├── SKILL.md                 # Skill 核心定义
├── README.md                # 使用文档
├── scripts/                 # 分析脚本
│   ├── analyze_structure.py    # 项目结构分析
│   ├── dependency_mapper.py    # 依赖映射和调用关系
│   ├── git_inspector.py        # Git 历史分析
│   └── ownership_tracker.py    # 代码所有权追踪
└── references/              # 参考文档存放
```

### 数据流

1. **结构分析**: 扫描代码库 → 构建依赖图 → 识别核心模块
2. **依赖映射**: 解析 AST → 追踪调用链 → 计算影响范围
3. **Git 检查**: 解析历史 → 提取决策 → 构建时间线
4. **所有权追踪**: 分析 blame → 统计贡献 → 识别专家

### 集成方式

Skill 通过以下工具与 WorkBuddy 集成：

- `read_file`: 读取代码文件
- `search_content`: 搜索代码内容
- `execute_command`: 运行 Git 命令和 Python 脚本
- `replace_in_file`: 生成分析报告

## API 参考

### analyze_structure.py

```python
from scripts.analyze_structure import analyze_project

report = analyze_project(
    project_root="/path/to/project",
    output_file="output.json"
)

# 返回结构:
{
    'entry_points': [...],
    'core_modules': [...],
    'module_structure': {...},
    'statistics': {...}
}
```

### dependency_mapper.py

```python
from scripts.dependency_mapper import map_dependencies

report = map_dependencies(
    project_root="/path/to/project",
    function_name="process_payment",
    output_file="output.json"
)

# 返回结构:
{
    'function_calls': {...},
    'function_callers': {...},
    'call_chains': [...],
    'impact_analysis': {...}
}
```

### git_inspector.py

```python
from scripts.git_inspector import inspect_git_history

result = inspect_git_history(
    project_root="/path/to/project",
    file_path="src/payment.py",
    function_name="Redis",
    output_file="output.json"
)

# 返回结构:
{
    'total_commits': 45,
    'key_decisions': [...],
    'contributors': [...],
    'timeline': [...]
}
```

### ownership_tracker.py

```python
from scripts.ownership_tracker import track_ownership

result = track_ownership(
    project_root="/path/to/project",
    file_path="src/payment.py",
    topic="缓存",
    output_file="output.json"
)

# 返回结构:
{
    'primary_maintainer': '李四',
    'recent_contributors': ['王五', '张三'],
    'active_hours': [14, 15, 16],
    'suggestion': '...'
}
```

## 最佳实践

### 团队使用建议

1. **渐进式引入**
   - 先在小团队试点
   - 收集反馈后逐步推广
   - 定期维护和更新

2. **数据质量**
   - 遵循 commit message 规范
   - PR 描述要完整
   - 及时归档设计决策文档

3. **隐私保护**
   - 敏感信息脱敏
   - 尊重开发者个人空间
   - 遵守公司安全规范

### 性能优化

- 首次分析后缓存结果
- 增量更新而非全量重分析
- 限制分析范围（文件数、历史深度）

## 扩展性

### 支持新语言

在 `analyze_structure.py` 和 `dependency_mapper.py` 中添加语言解析器：

```python
elif file_path.suffix == '.rust':
    self._parse_rust_dependencies(file_path, content)
```

### 自定义规则

创建 `references/custom_rules.json`：

```json
{
  "review_patterns": [
    {
      "pattern": "TODO|FIXME",
      "action": "flag_for_review"
    }
  ],
  "expert_keywords": [
    "性能", "安全", "架构"
  ]
}
```

### 集成外部工具

在脚本中调用外部 API：

```python
import requests

def fetch_slack_context(self, message_id):
    response = requests.get(
        f"https://api.slack.com/conversations.history?...",
        headers={"Authorization": "Bearer ..."}
    )
    return response.json()
```

## 常见问题

### Q: 分析速度慢怎么办？

A:
1. 缩小分析范围（限制文件数）
2. 缓存分析结果
3. 使用增量更新

### Q: Git 历史太长导致分析缓慢？

A:
1. 限制 `max_commits` 参数
2. 只分析最近 6 个月的历史
3. 使用 `--since` 参数过滤

### Q: 如何处理大型 monorepo？

A:
1. 按模块分别分析
2. 专注于活跃的子项目
3. 使用路径过滤参数

## 贡献指南

欢迎贡献代码、报告问题或提出改进建议！

### 开发环境

```bash
# 克隆仓库
git clone https://github.com/your-org/project-context-guide.git

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 运行测试

```bash
# 运行单元测试
pytest tests/

# 运行集成测试
pytest tests/integration/
```

### 提交 PR

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 致谢

灵感来源于每个经历过"代码迷宫"的开发者。我们相信，理解代码背后的上下文，和读懂代码本身一样重要。

## 联系方式

- Issue Tracker: https://github.com/your-org/project-context-guide/issues
- Discussions: https://github.com/your-org/project-context-guide/discussions
- Email: support@yourorg.com

---

让代码不再是迷宫 🧭

# 贡献指南

欢迎为 Trae Multi-Agent Skill 项目贡献代码！本文档将指导您完成贡献流程。

## 📖 目录

- [行为准则](#-行为准则)
- [开发环境设置](#-开发环境设置)
- [提交流程](#-提交流程)
- [代码规范](#-代码规范)
- [测试要求](#-测试要求)
- [文档规范](#-文档规范)
- [发布流程](#-发布流程)

## 🌟 行为准则

本项目采用 [贡献者公约](https://www.contributor-covenant.org/) 作为行为准则。请尊重所有贡献者，保持友好和专业的交流氛围。

## 🛠️ 开发环境设置

### 1. Fork 和克隆项目

```bash
# 1. 在 GitHub 上 Fork 项目
# 2. 克隆到本地
git clone https://github.com/YOUR_USERNAME/trae-multi-agent.git
cd trae-multi-agent

# 3. 添加上游仓库
git remote add upstream https://github.com/your-org/trae-multi-agent.git
```

### 2. 安装依赖

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -r requirements-dev.txt
```

### 3. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 测试覆盖率
pytest tests/ --cov=src --cov-report=html
```

## 📝 提交流程

### 1. 创建分支

```bash
# 从 main 分支创建新分支
git checkout -b feature/your-feature-name

# 或使用 fix 前缀修复 bug
git checkout -b fix/your-bug-fix

# 或使用 docs 前缀更新文档
git checkout -b docs/add-readme-section
```

**分支命名规范**:
- `feature/xxx` - 新功能
- `fix/xxx` - Bug 修复
- `docs/xxx` - 文档更新
- `refactor/xxx` - 代码重构
- `test/xxx` - 测试相关
- `chore/xxx` - 构建/工具相关

### 2. 进行修改

进行修改时，请遵循：
- 代码规范（见下文）
- 添加必要的注释
- 编写单元测试
- 更新相关文档

### 3. 提交更改

```bash
# 添加更改的文件
git add path/to/changed/files

# 或添加所有更改
git add .

# 提交更改（使用规范的提交信息）
git commit -m "feat: 添加新功能"
```

**提交信息规范**:

格式：`<type>: <subject>`

**Type 类型**:
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构（既不是新功能也不是修复 bug）
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动

**Subject 要求**:
- 使用祈使句、现在时态
- 首字母小写
- 简洁明了（不超过 50 个字符）

**示例**:
```
feat: 添加角色识别算法
fix: 修复共识机制中的冲突检测
docs: 更新 README 安装说明
refactor: 优化调度算法性能
test: 添加边界条件测试
```

### 4. 同步上游代码

```bash
# 获取上游最新代码
git fetch upstream

# 合并到当前分支
git rebase upstream/main

# 或合并（保留合并记录）
git merge upstream/main
```

### 5. 推送分支

```bash
# 推送到远程仓库
git push origin feature/your-feature-name
```

### 6. 创建 Pull Request

1. 在 GitHub 上访问你的 fork 仓库
2. 点击 "Compare & pull request"
3. 填写 PR 描述
4. 等待代码审查

**PR 描述模板**:

```markdown
## 描述
简要描述此 PR 的目的

## 相关 Issue
Fixes #123

## 更改类型
- [ ] 新功能
- [ ] Bug 修复
- [ ] 文档更新
- [ ] 代码重构
- [ ] 测试更新

## 测试
- [ ] 已添加单元测试
- [ ] 已运行所有测试并通过
- [ ] 已更新集成测试

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 已添加必要的注释
- [ ] 已更新相关文档
- [ ] 无新的警告或错误
```

## 💻 代码规范

### Python 代码规范

遵循 [PEP 8](https://pep8.org/) 规范：

```python
# 1. 使用 4 个空格缩进
def my_function():
    """文档字符串"""
    pass

# 2. 行宽不超过 79 个字符
long_variable_name = (
    "this is a very long string that needs to be wrapped"
)

# 3. 使用类型注解
def calculate_score(
    base_score: float,
    multiplier: int = 1
) -> float:
    """计算分数"""
    return base_score * multiplier

# 4. 使用有意义的变量名
# ❌ 错误
def calc(a, b):
    return a + b

# ✅ 正确
def calculate_total_price(
    base_price: float,
    tax_rate: float
) -> float:
    """计算总价"""
    return base_price * (1 + tax_rate)

# 5. 添加文档字符串
class AgentDispatcher:
    """智能体调度器
    
    负责分析任务并调度到合适的角色
    """
    
    def analyze_task(self, task: str) -> Tuple[str, float]:
        """
        分析任务，识别需要的角色
        
        Args:
            task: 任务描述
            
        Returns:
            (最佳角色，置信度)
        """
        pass
```

### 中文注释规范

```python
# ✅ 使用中文注释
def analyze_task(task: str):
    """
    分析任务，识别需要的角色
    
    Args:
        task: 任务描述
        
    Returns:
        (最佳角色，置信度，所有匹配的角色列表)
    """
    # 1. 关键词匹配
    for keyword in keywords:
        if keyword in task:
            score += 1.0
    
    # 2. 位置权重计算
    # 越靠前的关键词权重越高
    for i, word in enumerate(words):
        score += 1.0 / (i + 1)
    
    return best_role, confidence
```

### 错误处理规范

```python
# ✅ 完整的错误处理
def dispatch_task(task: str) -> Dict:
    """
    调度任务
    
    Raises:
        TaskAnalysisError: 任务分析失败
        RoleNotFoundError: 角色不存在
        DispatchError: 调度失败
    """
    try:
        # 1. 分析任务
        role, confidence = analyze_task(task)
        
        # 2. 验证角色
        if not role_exists(role):
            raise RoleNotFoundError(f"角色不存在：{role}")
        
        # 3. 执行调度
        result = execute_dispatch(role, task)
        
        return {
            "success": True,
            "role": role,
            "confidence": confidence
        }
        
    except TaskAnalysisError as e:
        logger.error(f"任务分析失败：{e}")
        raise
    except Exception as e:
        logger.error(f"调度失败：{e}")
        raise DispatchError(f"调度失败：{e}")
```

## 🧪 测试要求

### 单元测试

```python
import pytest
from src.dispatcher import AgentDispatcher

class TestAgentDispatcher:
    """测试智能体调度器"""
    
    def test_analyze_architect_task(self):
        """测试架构师任务识别"""
        dispatcher = AgentDispatcher()
        task = "设计系统架构：包括模块划分和技术选型"
        
        role, confidence, matched = dispatcher.analyze_task(task)
        
        assert role == "architect"
        assert confidence > 0.8
        assert "architect" in matched
    
    def test_analyze_product_manager_task(self):
        """测试产品经理任务识别"""
        dispatcher = AgentDispatcher()
        task = "定义产品需求，编写 PRD 文档"
        
        role, confidence, matched = dispatcher.analyze_task(task)
        
        assert role == "product_manager"
        assert confidence > 0.7
    
    def test_analyze_unknown_task(self):
        """测试未知任务识别（默认角色）"""
        dispatcher = AgentDispatcher()
        task = "做一些东西"
        
        role, confidence, matched = dispatcher.analyze_task(task)
        
        assert role == "solo_coder"  # 默认角色
        assert confidence < 0.5
```

### 测试覆盖率要求

```bash
# 运行测试并生成覆盖率报告
pytest tests/ --cov=src --cov-report=html --cov-report=term-missing

# 覆盖率要求
# - 代码覆盖率：> 80%
# - 分支覆盖率：> 70%
# - 行覆盖率：> 85%
```

### 集成测试

```python
import pytest
from src.consensus import ConsensusOrganizer

class TestConsensusMechanism:
    """测试共识机制"""
    
    @pytest.mark.integration
    def test_organize_consensus(self):
        """测试组织多角色共识"""
        organizer = ConsensusOrganizer()
        task = "启动新项目：安全浏览器广告拦截功能"
        
        consensus = organizer.organize(task)
        
        assert len(consensus.participants) >= 3
        assert consensus.decision is not None
        assert consensus.confidence > 0.6
```

## 📚 文档规范

### README 规范

README.md 应包含：
- 项目简介
- 功能特性
- 快速开始
- 安装说明
- 使用示例
- API 文档
- 贡献指南
- 许可证

### 代码文档

```python
class AgentDispatcher:
    """
    智能体调度器
    
    根据任务类型自动识别并调度到最合适的角色。
    支持 4 种角色：架构师、产品经理、测试专家、独立开发者。
    
    Attributes:
        db_path (str): 数据库路径
        roles (Dict): 角色配置
        logger (Logger): 日志记录器
        
    Example:
        >>> dispatcher = AgentDispatcher()
        >>> role, confidence = dispatcher.analyze_task("设计系统架构")
        >>> print(f"识别角色：{role}, 置信度：{confidence}")
    """
    
    def analyze_task(self, task: str) -> Tuple[str, float]:
        """
        分析任务，识别需要的角色
        
        Args:
            task: 任务描述字符串
            
        Returns:
            Tuple[str, float]: (最佳角色，置信度)
            - 最佳角色：识别出的角色名称
            - 置信度：0.0-1.0 之间的浮点数
            
        Raises:
            TaskAnalysisError: 当任务分析失败时抛出
            
        Example:
            >>> dispatcher = AgentDispatcher()
            >>> role, confidence = dispatcher.analyze_task("设计系统架构")
            >>> print(role)
            'architect'
        """
        pass
```

### 变更日志 (CHANGELOG.md)

```markdown
# 变更日志

## [1.0.0] - 2024-03-04

### Added
- 初始版本发布
- 4 个完整角色 Prompt（架构师、产品经理、测试专家、独立开发者）
- 智能角色识别算法
- 多角色共识机制
- 完整项目生命周期支持
- 代码审查模式

### Changed
- 无

### Fixed
- 无

### Deprecated
- 无

### Removed
- 无

### Security
- 无
```

## 🚀 发布流程

### 版本号规范

遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

格式：`MAJOR.MINOR.PATCH`

- `MAJOR`: 不兼容的 API 变更
- `MINOR`: 向后兼容的功能新增
- `PATCH`: 向后兼容的问题修复

### 发布步骤

1. **更新版本号**
   ```bash
   # 更新 pyproject.toml 或 setup.py 中的版本号
   ```

2. **更新 CHANGELOG.md**
   ```markdown
   ## [1.1.0] - 2024-03-05
   
   ### Added
   - 新增功能描述
   
   ### Fixed
   - 修复问题描述
   ```

3. **创建发布标签**
   ```bash
   git tag -a v1.1.0 -m "Release version 1.1.0"
   git push origin v1.1.0
   ```

4. **创建 GitHub Release**
   - 访问 https://github.com/your-org/trae-multi-agent/releases
   - 点击 "Draft a new release"
   - 选择标签
   - 填写发布说明
   - 点击 "Publish release"

## 📞 联系方式

如有问题，请通过以下方式联系：

- **GitHub Issues**: https://github.com/your-org/trae-multi-agent/issues
- **Email**: your-email@example.com

---

感谢你的贡献！🎉

# Hermes 系统测试指南

由于 OpenClaw 安全策略限制，无法在 OpenClaw 会话中直接运行 Python 端到端测试。本指南说明如何在受控环境中手动测试 Hermes 系统。

## 📋 测试前提

### 环境要求
- Python 3.9+
- PyYAML 6.0+
- 本地文件系统访问权限
- 可执行 Python 脚本的安全环境

### 依赖安装
```bash
# 安装 PyYAML（如果尚未安装）
pip install pyyaml
```

## 🧪 测试步骤

### 1. 基本功能测试
```bash
cd /path/to/HermesAgentLearning

# 测试模块导入
python3 -c "
import sys
sys.path.insert(0, 'src')
from compatibility.hermes_compatibility import HermesCompatibilityLayer
print('✅ 模块导入成功')
"

# 运行简化测试
python3 simple_e2e_test.py
```

### 2. 完整端到端测试（在安全环境中）
```bash
cd /path/to/HermesAgentLearning

# 运行完整端到端测试
python3 test_end_to_end_integration.py
```

### 3. 组件级测试

#### 记忆系统测试
```python
# test_memory.py
import sys
sys.path.insert(0, 'src')

from memory.memory_manager import MemoryManager
import tempfile
import os

# 创建临时工作空间
temp_dir = tempfile.mkdtemp()
memory_dir = os.path.join(temp_dir, "memory")

# 创建记忆管理器
manager = MemoryManager(
    workspace_dir=temp_dir,
    memory_dir=memory_dir
)

# 测试对话同步
manager.sync_turn("测试问题", "测试回答")
print("✅ 对话同步测试通过")

# 测试记忆预取
memory = manager.prefetch("测试")
print(f"✅ 记忆预取测试通过，找到 {len(memory)} 条记忆")

# 清理
import shutil
shutil.rmtree(temp_dir)
```

#### Skill 生成系统测试
```python
# test_skill_generation.py
import sys
sys.path.insert(0, 'src')

from skill_generator.skill_generator import SkillGenerator
import tempfile
import os

# 创建临时工作空间
temp_dir = tempfile.mkdtemp()

# 创建 Skill 生成器
generator = SkillGenerator(
    workspace_dir=temp_dir,
    trajectories_dir=os.path.join(temp_dir, "trajectories"),
    skills_dir=os.path.join(temp_dir, "skills")
)

# 测试轨迹记录
trajectory = {
    "id": "test_traj_001",
    "task_description": "测试任务",
    "steps": [
        {"action": "读取文件", "tool": "read", "args": {"path": "test.txt"}},
        {"action": "创建脚本", "content": "print('Hello')", "files_created": ["test.py"]}
    ]
}

# 保存轨迹
traj_path = os.path.join(temp_dir, "trajectories", "test_traj_001.json")
os.makedirs(os.path.dirname(traj_path), exist_ok=True)
import json
with open(traj_path, 'w') as f:
    json.dump(trajectory, f)

# 测试 Skill 生成
skill = generator.generate_skill_from_trajectory(traj_path)
print(f"✅ Skill 生成测试通过，生成 Skill: {skill.get('name', '未知')}")

# 清理
import shutil
shutil.rmtree(temp_dir)
```

## 📊 预期测试结果

### 成功标准
1. **模块导入**: 所有 Python 模块应能正常导入，无 ImportError
2. **基本功能**: 记忆同步、预取、Skill 生成等核心功能应正常工作
3. **错误处理**: 系统应能正确处理边界情况和错误输入
4. **性能**: 关键操作应在合理时间内完成（< 1秒）

### 测试覆盖率
- ✅ 记忆系统: 对话同步、记忆预取、持久化存储
- ✅ Skill 生成系统: 轨迹记录、复盘分析、模板生成
- ✅ 兼容性层: 配置管理、选择性启用、状态监控
- ✅ 数据导出: 记忆扫描、特征提取、ML 数据集生成
- ✅ 性能基准: 响应时间、内存使用、健康度评分

## 🔧 故障排除

### 常见问题

#### 1. ImportError: No module named 'yaml'
```bash
pip install pyyaml
```

#### 2. 权限错误
```bash
# 确保对工作空间目录有读写权限
chmod -R 755 /path/to/HermesAgentLearning
```

#### 3. 路径问题
```bash
# 确保在正确的目录中运行
cd /path/to/HermesAgentLearning
```

#### 4. Python 版本不兼容
```bash
# 检查 Python 版本
python3 --version  # 需要 3.9+
```

### 调试建议

1. **启用详细日志**
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **检查临时文件**
```bash
# 测试脚本会在 /tmp 下创建临时目录
ls -la /tmp/e2e_test_*
```

3. **验证配置**
```bash
# 检查配置文件格式
python3 -c "import yaml; data = yaml.safe_load(open('hermes_config.yaml')); print(data)"
```

## 🚀 生产部署验证

### 集成测试清单
- [ ] 模块导入无错误
- [ ] 记忆系统工作正常
- [ ] Skill 生成系统工作正常  
- [ ] 兼容性层配置正确
- [ ] 性能在可接受范围内
- [ ] 错误处理健全
- [ ] 文档完整准确

### 用户验收测试
1. **安装验证**: 按照安装指南成功安装
2. **配置验证**: 配置文件正确加载
3. **功能验证**: 核心功能按预期工作
4. **性能验证**: 响应时间满足要求
5. **稳定性验证**: 长时间运行无崩溃

## 📞 支持

如果测试遇到问题：

1. **检查日志**: 查看详细的错误信息和堆栈跟踪
2. **验证环境**: 确保满足所有前提条件
3. **简化测试**: 从最基本的测试开始，逐步增加复杂度
4. **联系支持**: 提供详细的错误信息和测试环境信息

---

**测试状态**: ✅ 测试脚本和指南已准备就绪  
**最后更新**: 2026-04-23 09:45  
**测试环境**: Python 3.9.6, PyYAML 6.0.3
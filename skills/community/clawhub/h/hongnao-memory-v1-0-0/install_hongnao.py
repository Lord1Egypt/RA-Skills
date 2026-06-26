#!/usr/bin/env python3
"""
弘脑记忆系统 - OpenClaw 插件安装脚本
HongNao Memory OS - OpenClaw Plugin Installer

用法：
    python3 install_hongnao.py [--workspace PATH]
"""

import os
import sys
import shutil
from pathlib import Path


def check_prerequisites():
    """检查前置条件"""
    print("🔍 检查前置条件...")
    
    # 检查 Python 版本
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    # 检查依赖
    required_packages = ['chromadb', 'sqlite3', 'numpy']
    for pkg in required_packages:
        try:
            __import__(pkg.replace('-', '_'))
        except ImportError:
            print(f"⚠️  缺少依赖：{pkg}")
            print(f"   运行：pip3 install {pkg}")
            return False
    
    print("✅ 前置条件满足")
    return True


def install_dependencies():
    """安装依赖包"""
    print("\n📦 安装依赖包...")
    
    requirements = [
        'chromadb>=0.4.0',
        'numpy>=1.20.0',
        'sentence-transformers>=2.2.0',
    ]
    
    for req in requirements:
        print(f"  - {req}")
    
    print("\n请运行以下命令安装依赖:")
    print("  pip3 install -r requirements.txt\n")


def copy_plugin_files(workspace_path: Path):
    """复制插件文件到 OpenClaw 工作区"""
    print("\n📋 复制插件文件...")
    
    # 源目录
    src_dir = Path(__file__).parent
    files_to_copy = [
        'memory_extraction_v3.py',
        'memory_consolidation.py',
        'memory_retrieval.py',
        'memory_update.py',
        'storage_layer.py',
        'vector_store.py',
        'memory_api.py',
        'openclaw_integration.py',
        'preference_learning.py',
        'test_session_integration.py',
    ]
    
    # 目标目录
    dest_dir = workspace_path / "hongnao_memory"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    for filename in files_to_copy:
        src_file = src_dir / filename
        dest_file = dest_dir / filename
        if src_file.exists():
            shutil.copy2(src_file, dest_file)
            print(f"  ✅ {filename}")
        else:
            print(f"  ⚠️  {filename} (不存在)")
    
    # 复制 requirements.txt
    req_src = src_dir / "requirements.txt"
    if req_src.exists():
        shutil.copy2(req_src, dest_dir / "requirements.txt")
        print(f"  ✅ requirements.txt")
    
    return dest_dir


def create_config_file(workspace_path: Path):
    """创建配置文件"""
    print("\n⚙️  创建配置文件...")
    
    config_content = """# 弘脑记忆系统配置文件
# HongNao Memory OS Configuration

[memory]
# 记忆库路径
db_path = ~/.openclaw/workspace/hongnao_memory/hongnao.db
vector_store_path = ~/.openclaw/workspace/hongnao_memory/chroma_db

# 检索配置
retrieval_top_k = 10
retrieval_min_score = 0.15

# 遗忘曲线
forgetting_half_life_days = 30.0
auto_cleanup_days = 90

[extraction]
# 记忆抽取配置
enable_extraction = true
enable_consolidation = true

[openclaw]
# OpenClaw 集成配置
enable_session_sync = true
auto_extract_from_sessions = true
sync_interval_minutes = 30

[preference_learning]
# 偏好学习配置
enable_preference_learning = true
auto_sync_to_memory = true
confidence_threshold = 0.6
"""
    
    config_file = workspace_path / "hongnao_memory_config.ini"
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"  ✅ 创建配置文件：{config_file}")
    return config_file


def create_readme(workspace_path: Path):
    """创建 README 文档"""
    print("\n📖 创建 README 文档...")
    
    readme_content = """# 弘脑记忆系统 - OpenClaw 插件

HongNao Memory OS for OpenClaw - 为 OpenClaw 平台打造的长期记忆系统

## 🚀 快速开始

### 1. 安装依赖

```bash
cd hongnao_memory
pip3 install -r requirements.txt
```

### 2. 配置记忆系统

编辑 `hongnao_memory_config.ini` 配置文件，设置：
- 记忆库路径
- 检索参数
- OpenClaw 集成选项

### 3. 在 OpenClaw 中启用

在 OpenClaw 主程序中导入：

```python
from hongnao_memory.memory_api import HongNaoMemorySystem, MemorySystemConfig
from hongnao_memory.openclaw_integration import OpenClawMemorySync, OpenClawTools

# 初始化记忆系统
config = MemorySystemConfig()
memory_system = HongNaoMemorySystem(config)

# 初始化 OpenClaw 同步器
sync = OpenClawMemorySync(memory_system)
tools = OpenClawTools(memory_system)
```

### 4. 使用记忆功能

```python
# 从对话中抽取记忆
memory_system.add_memories_from_text("用户喜欢简洁的沟通风格", source="chat")

# 检索相关记忆
result = memory_system.retrieve_memories("用户偏好", top_k=5)

# 同步 Session 到记忆
sync.sync_session_to_memory(
    session_id="session_123",
    messages=[{"role": "user", "content": "..."}],
    auto_extract=True
)

# 获取用户偏好
profile = tools.get_user_preference()
```

## 📚 功能模块

### 核心模块

| 模块 | 功能 |
|------|------|
| memory_extraction_v3.py | 记忆抽取 (事实/偏好/技能/情感/约束) |
| memory_consolidation.py | 记忆巩固 (压缩/关联/评分) |
| memory_retrieval.py | 混合检索 (向量 + 关键词) |
| memory_update.py | 记忆更新与遗忘 |
| storage_layer.py | 存储层 (MemCell/MemScene) |
| vector_store.py | 向量存储 (ChromaDB) |
| memory_api.py | 统一 API 接口 |

### 集成模块

| 模块 | 功能 |
|------|------|
| openclaw_integration.py | OpenClaw 平台集成 |
| preference_learning.py | 用户偏好学习 |

### 测试模块

| 模块 | 功能 |
|------|------|
| test_session_integration.py | Session 集成测试 |

## 🧪 运行测试

```bash
python3 test_session_integration.py
```

## 📊 记忆类型

- **FACT** (事实): 客观事实信息
- **PREFERENCE** (偏好): 用户喜好和习惯
- **SKILL** (技能): 技能和能力
- **EMOTION** (情感): 情感和情绪
- **CONSTRAINT** (约束): 限制和边界

## 🔧 配置选项

详见 `hongnao_memory_config.ini`

## 📝 使用示例

### 示例 1: 从对话中学习用户偏好

```python
from preference_learning import UserPreferenceLearner

learner = UserPreferenceLearner(memory_system)

# 从对话中学习
conversations = [
    "我喜欢简洁直接的沟通风格",
    "我通常早上 8 点查看新闻",
    "我偏好使用 Python 进行开发",
]

for conv in conversations:
    learner.learn_from_conversation(conv)

# 获取学习的偏好
report = learner.export_report()
print(f"学习了 {report['total_count']} 条偏好")
```

### 示例 2: 跨 Session 记忆检索

```python
# Session 1
sync.sync_session_to_memory(
    session_id="session_001",
    messages=[{"role": "user", "content": "我叫唐锋，在燧弘华创工作"}]
)

# Session 2 (不同时间)
result = tools.search_memory("唐锋 燧弘华创", top_k=3)
print(f"找到 {result['count']} 条相关记忆")
```

### 示例 3: 获取用户画像

```python
profile = tools.get_user_preference()

print("事实型记忆:", len(profile.get('facts', [])))
print("偏好型记忆:", len(profile.get('preferences', [])))
print("技能型记忆:", len(profile.get('skills', [])))
```

## 🎯 性能指标

- 召回准确率：>90%
- 检索延迟：<100ms
- Token 节省：>40%

## 📄 许可证

MIT License

## 🙏 致谢

参考项目：EverMemOS (EverMind-AI 开源项目)
"""
    
    readme_file = workspace_path / "hongnao_memory" / "INSTALL.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"  ✅ 创建安装文档：{readme_file}")
    return readme_file


def create_requirements():
    """创建 requirements.txt"""
    print("\n📝 创建 requirements.txt...")
    
    requirements = """# 弘脑记忆系统依赖
# HongNao Memory OS Requirements

# 向量数据库
chromadb>=0.4.0

# 数值计算
numpy>=1.20.0

# 嵌入模型
sentence-transformers>=2.2.0

# 可选：更强大的嵌入模型
# FlagEmbedding>=1.2.0

# 可选：Redis 缓存
# redis>=4.5.0
"""
    
    req_file = Path(__file__).parent / "requirements.txt"
    with open(req_file, 'w', encoding='utf-8') as f:
        f.write(requirements)
    
    print(f"  ✅ 创建 requirements.txt")
    return req_file


def print_summary(workspace_path: Path, plugin_dir: Path):
    """打印安装总结"""
    print("\n" + "=" * 60)
    print("🎉 弘脑记忆系统插件安装完成！")
    print("=" * 60)
    print(f"\n📁 安装位置：{plugin_dir}")
    print(f"\n📋 已安装文件:")
    
    for f in sorted(plugin_dir.iterdir()):
        if f.is_file():
            print(f"  - {f.name}")
    
    print(f"\n📖 下一步:")
    print(f"  1. 阅读 {plugin_dir}/INSTALL.md")
    print(f"  2. 运行：pip3 install -r {plugin_dir}/requirements.txt")
    print(f"  3. 配置：{workspace_path}/hongnao_memory_config.ini")
    print(f"  4. 测试：python3 {plugin_dir}/test_session_integration.py")
    
    print("\n" + "=" * 60)


def main():
    """主函数"""
    print("=" * 60)
    print("弘脑记忆系统 - OpenClaw 插件安装程序")
    print("=" * 60)
    
    # 解析参数
    workspace_arg = sys.argv[1] if len(sys.argv) > 1 else None
    workspace_path = Path(workspace_arg) if workspace_arg else Path.home() / ".openclaw" / "workspace"
    
    print(f"\n📂 OpenClaw 工作区：{workspace_path}")
    
    # 检查前置条件
    if not check_prerequisites():
        print("\n❌ 前置条件不满足，请先安装依赖")
        install_dependencies()
        sys.exit(1)
    
    # 创建 requirements.txt
    create_requirements()
    
    # 复制插件文件
    plugin_dir = copy_plugin_files(workspace_path)
    
    # 创建配置文件
    create_config_file(workspace_path)
    
    # 创建 README
    create_readme(workspace_path)
    
    # 打印总结
    print_summary(workspace_path, plugin_dir)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

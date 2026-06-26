# OpenClaw Self Analyzer - 自分析工具

深度分析OpenClaw架构，自动生成钩子和扩展。

## 功能

- 架构分析
- 钩子点检测
- 自动生成钩子
- 代码扫描
- 报告生成

## 使用

### 完整分析
```bash
cd /root/.openclaw/workspace/skills/openclaw-self-analyzer
python3 core/architecture_analyzer.py
```

### 生成钩子
```python
from generators.hook_generator import HookGenerator

generator = HookGenerator()
hook = generator.generate_hook_package(
    hook_name='my_hook',
    hook_type='pre',
    stage='context_gather',
    logic='// your logic'
)
```

### 生成报告
```python
from reporters.report_generator import ReportGenerator

generator = ReportGenerator()
files = generator.save_reports(Path('./reports'))
```

## 架构映射

OpenClaw处理流水线:

1. **input_receive** - 接收用户输入
2. **context_gather** - 收集历史上下文
3. **memory_retrieve** - 检索记忆
4. **prompt_assemble** - 组装prompt
5. **token_check** - token检查
6. **context_compress** - 上下文压缩
7. **llm_submit** - 提交给LLM
8. **response_process** - 处理响应
9. **memory_store** - 存储新记忆

每个阶段支持三种钩子:
- **pre** - 前置处理
- **post** - 后置处理
- **replace** - 完全替换

Copyright © 2025-2026 Edison Wang (fofo365/edisonw@163.com) Authors. All Rights Reserved.
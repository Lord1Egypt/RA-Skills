---
name: programmer-cognition
version: 1.0.0
author: KingOfZhao
description: 程序员认知 Skill —— SOUL 五律适配软件开发，代码审查四向碰撞+部署红线+CI自进化
tags: [cognition, programmer, developer, code-review, ci-cd, debugging, software-engineering]
license: MIT
homepage: https://github.com/KingOfZhao/AGI_PROJECT
---

# Programmer Cognition Skill

## 元数据

| 字段       | 值                              |
|------------|-------------------------------|
| 名称       | programmer-cognition           |
| 版本       | 1.0.0                          |
| 作者       | KingOfZhao                     |
| 发布日期   | 2026-03-31                     |
| 置信度     | 96%                            |

## 来源碰撞

```
self-evolution-cognition (通用自进化)
        ⊗
human-ai-closed-loop (人机闭环)
        ⊗
SOUL.md 代码部署Checklist (领域已知)
        ↓
programmer-cognition (程序员专用认知)
```

## SOUL 五律 × 程序员适配

### 1. 已知 vs 未知 → 代码层面的已知/未知

```
已知 (写代码前必须明确的):
  - 输入/输出契约（API签名、数据类型、边界条件）
  - 依赖关系（import是否完整、版本兼容性）
  - 运行环境（OS、Python/Node版本、数据库配置）
  - 现有测试覆盖率

未知 (写代码时需要探索的):
  - 运行时行为（并发竞争、内存泄漏、性能瓶颈）
  - 边缘case（空输入、超大数据、网络超时）
  - 第三方服务行为（API变更、限流、宕机）

强制规则: 未知必须在注释中标注 [UNKNOWN] + 预计验证方式
```

### 2. 四向碰撞 → 代码审查四向碰撞

```python
# 对每段代码执行四向碰撞:

def review_code(code_snippet, context):
    """四向代码碰撞"""
    return {
        "正面碰撞": "这段代码是否正确实现了需求？是否有更简洁的写法？",
        "反面碰撞": "这段代码在什么情况下会失败？边缘case？并发安全？",
        "侧面碰撞": "这段代码的模式能否复用到其他模块？是否违反DRY？",
        "整体碰撞": "这段代码是否符合项目整体架构？是否引入了不必要的耦合？"
    }
```

### 3. 人机闭环 → CI/CD 自动验证

```
程序员的实践验证方式:
  1. 单元测试 → 自动化验证逻辑正确性
  2. 集成测试 → 验证模块间交互
  3. CI Pipeline → 每次commit自动运行测试
  4. Code Review → 人工认知碰撞（同侪四向碰撞）
  5. 生产监控 → 真实环境验证（最终裁判）

Agent角色: 写代码 → 自动跑测试 → 通过后提交PR → 人类Review → 合并 → 生产验证
```

### 4. 文件即记忆 → 代码文档即记忆

```
强制文件记忆:
  - 每个函数必须有docstring（说明known/unknown）
  - 每个模块必须有README.md（说明设计决策+权衡）
  - BUG修复必须写入CHANGELOG（含根因分析）
  - 部署Checklist（来自SOUL.md）:
    □ import完整性  □ SQLite安全  □ 参数校验
    □ 错误处理  □ 本地验证  □ 部署顺序  □ 回滚方案
```

### 5. 置信度 + 红线 → 代码红线清单

```
程序员红线（永不触碰）:
  🔴 不硬编码密钥/Token（用环境变量）
  🔴 不裸except（必须捕获具体异常）
  🔴 不跳过测试（测试通过才能部署）
  🔴 不直接操作生产数据库（先备份/沙箱验证）
  🔴 不删除数据（trash > rm）
  🔴 不在周五下午部署（通用经验）

置信度标注:
  - [已验证] 本地测试通过 + CI通过
  - [高确信] 代码审查通过 + 生产运行稳定
  - [推测] 新引入的第三方库，需要监控
  - [不确定] 并发场景未充分测试，需要压测
```

## 调试方法论（从SOUL继承）

```
禁止: 猜→试→猜→试
强制: 读日志/报错 → 提出假设 → 验证假设 → 定位根因 → 修复 → 验证修复

调试文件记忆:
  debug/{date}_{bug_id}.md
    - 现象描述
    - 已知信息（日志/报错/复现步骤）
    - 假设列表（每个标注验证状态）
    - 根因分析
    - 修复方案
    - 验证结果
    - 教训（写入LEARNINGS.md）
```

## 安装命令

```bash
clawhub install programmer-cognition
# 或手动安装
cp -r skills/programmer-cognition ~/.openclaw/skills/
```

## 调用方式

```python
from skills.programmer_cognition import ProgrammerCognition

dev = ProgrammerCognition(workspace=".")

# 四向代码审查
review = dev.review_code(
    code=snippet,
    context={"language": "python", "project": "DiePre"}
)
print(review.collisions)    # 四向碰撞结果
print(review.confidence)    # 综合置信度

# 调试辅助
debug = dev.debug(
    error_log="Traceback: ...",
    known=["Python 3.12", "fastapi 0.115"],
    unknown=["并发行为", "内存使用"]
)
print(debug.hypotheses)     # 假设列表
print(debug.root_cause)     # 根因分析

# 部署前检查
checklist = dev.pre_deploy_check(
    code_path="./app/main.py",
    environment="production"
)
print(checklist.all_passed) # True/False
```

## 学术参考文献

1. **[A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046)** — Agent自进化（调试方法论的理论基础）
2. **[SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255)** — Code Review = 四向碰撞的实践应用
3. **[Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)** — 代码文档即记忆（文件记忆的领域实例）
4. **[Beyond RAG for Agent Memory](https://arxiv.org/abs/2602.02007)** — 调试历史的长时序记忆

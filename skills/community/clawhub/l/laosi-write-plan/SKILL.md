---
name: write-plan
version: 1.0.0
description: 实现计划生成 - 从需求生成多阶段实施计划：基础→逻辑→接口→测试→部署。含模板、依赖分析、验收标准
tags: [planning, project-management, development, architecture]
author: laosi
source: original
---

# Write Plan - 实现计划生成

> 激活词: 计划 / 规划 / plan / 方案

## 计划结构

每个计划包含5个阶段，每个阶段包含验收标准和依赖分析。

```
需求
 │
 ▼
Phase 1: 基础数据模型  ←──────────────┐
 │                                       │
 ▼                                       │
Phase 2: 业务逻辑  ← 依赖Phase 1 ──────┤
 │                                       │
 ▼                                       │
Phase 3: API/接口层  ← 依赖Phase 2 ────┤
 │                                       │
 ▼                                       │
Phase 4: 测试与边界  ← 依赖Phase 3 ────┤
 │                                       │
 ▼                                       │
Phase 5: 文档与部署  ← 依赖Phase 4 ────┘
```

## Python 实现

```python
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta

@dataclass
class Task:
    name: str
    description: str
    effort_hours: int
    dependencies: List[str] = field(default_factory=list)
    acceptance_criteria: List[str] = field(default_factory=list)
    
@dataclass
class Phase:
    name: str
    goal: str
    tasks: List[Task] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    
@dataclass
class Plan:
    title: str
    goal: str
    phases: List[Phase] = field(default_factory=list)
    created: str = ""
    
    def __post_init__(self):
        if not self.created:
            self.created = datetime.now().isoformat()
    
    def add_phase(self, name: str, goal: str) -> Phase:
        p = Phase(name=name, goal=goal)
        self.phases.append(p)
        return p
    
    def verify_dependencies(self) -> List[str]:
        """验证依赖是否满足（前一阶段是否包含依赖任务）"""
        warnings = []
        all_tasks = {}
        for pi, phase in enumerate(self.phases):
            for task in phase.tasks:
                all_tasks[task.name] = pi
        
        for pi, phase in enumerate(self.phases):
            for task in phase.tasks:
                for dep in task.dependencies:
                    dep_phase = all_tasks.get(dep)
                    if dep_phase is None:
                        warnings.append(f"⚠️ {task.name} 依赖 '{dep}' 但该任务不存在")
                    elif dep_phase > pi:
                        warnings.append(f"⚠️ {task.name} 依赖 Phase{dep_phase+1} 的 '{dep}'，但它在更后面")
        
        return warnings
    
    def total_effort(self) -> int:
        return sum(t.effort_hours for p in self.phases for t in p.tasks)
    
    def estimate_delivery(self, hours_per_day: int = 4) -> str:
        days = self.total_effort() / hours_per_day
        delivery = datetime.now() + timedelta(days=days)
        return delivery.strftime("%Y-%m-%d")
    
    def markdown(self) -> str:
        lines = [f"# 实施计划: {self.title}", f"**目标**: {self.goal}", ""]
        lines.append(f"**总工作量**: {self.total_effort()} 人时")
        lines.append(f"**预计交付**: {self.estimate_delivery()}")
        lines.append(f"**创建时间**: {self.created}\n")
        
        for pi, phase in enumerate(self.phases):
            lines.append(f"---")
            lines.append(f"## Phase {pi+1}: {phase.name}")
            lines.append(f"**目标**: {phase.goal}")
            if phase.risks:
                for r in phase.risks:
                    lines.append(f"- ⚠️ {r}")
            lines.append("")
            
            for ti, task in enumerate(phase.tasks):
                lines.append(f"### {pi+1}.{ti+1} {task.name}")
                lines.append(f"- **描述**: {task.description}")
                lines.append(f"- **工作量**: {task.effort_hours}h")
                if task.dependencies:
                    lines.append(f"- **依赖**: {', '.join(task.dependencies)}")
                if task.acceptance_criteria:
                    lines.append("- **验收标准**:")
                    for ac in task.acceptance_criteria:
                        lines.append(f"  - [ ] {ac}")
                lines.append("")
        
        # 依赖检查
        warnings = self.verify_dependencies()
        if warnings:
            lines.append("## ⚠️ 依赖警告")
            for w in warnings:
                lines.append(f"- {w}")
        
        return "\n".join(lines)

# 使用示例
plan = Plan(
    title="博客全文搜索功能",
    goal="给个人博客添加AI驱动的全文搜索，支持中文分词和语义匹配"
)

# Phase 1: 基础
p1 = plan.add_phase("Foundation & Data Model", "构建搜索基础设施和数据模型")
p1.tasks.append(Task(
    "文章索引设计", "设计Elasticsearch/Meilisearch索引结构",
    4, [],
    ["支持中文分词(t analyzer)", "支持加权排序(标题>标签>正文)"]
))
p1.tasks.append(Task(
    "数据导出脚本", "编写导出所有文章到搜索索引的脚本",
    3, [],
    ["增量更新", "全量重建"]
))

# Phase 2: 业务逻辑
p2 = plan.add_phase("Business Logic", "搜索逻辑和排序算法")
p2.tasks.append(Task(
    "搜索API实现", "基于FastAPI的搜索接口",
    6, ["文章索引设计"],
    ["GET /search?q={keyword}", "分页返回", "高亮匹配片段"]
))
p2.tasks.append(Task(
    "排名算法", "TF-IDF + 热度加权排序",
    4, ["搜索API实现"],
    ["支持相关度排序", "支持时间排序"]
))

# Phase 3: API
p3 = plan.add_phase("API & Interface", "前后端对接")
p3.tasks.append(Task(
    "前端搜索组件", "React/Vue搜索框组件",
    5, ["搜索API实现"],
    ["防抖输入(300ms)", "空状态/加载态/结果态", "键盘快捷键"]
))

# Phase 4: 测试
p4 = plan.add_phase("Testing", "全面测试")
p4.tasks.append(Task(
    "搜索质量测试", "100条测试查询评估搜索结果质量",
    3, ["排名算法"],
    ["Top-3命中率>80%", "空搜索不报错"]
))

# Phase 5: 部署
p5 = plan.add_phase("Deployment", "生产环境部署")
p5.risks.append("ES实例内存占用较高，建议1GB以上")
p5.tasks.append(Task(
    "容器化部署", "Docker Compose配置",
    3, ["搜索API实现"],
    ["docker-compose up一键启动"]
))

# 输出计划
print(plan.markdown())
```

## 模板预设

```python
class PlanTemplates:
    @staticmethod
    def api_service(name: str, endpoints: List[str]) -> Plan:
        """API服务模板"""
        p = Plan(title=name, goal=f"构建{name} API服务")
        p.add_phase("数据模型", "设计数据库表/API Schema")
        p.add_phase("核心逻辑", f"实现 {', '.join(endpoints)}")
        p.add_phase("认证授权", "JWT/OAuth2 + 权限控制")
        p.add_phase("测试文档", "API测试 + Swagger/OpenAPI")
        p.add_phase("部署运维", "Docker + CI/CD配置")
        return p
    
    @staticmethod
    def cli_tool(name: str) -> Plan:
        """CLI工具模板"""
        p = Plan(title=name, goal=f"构建{name} CLI工具")
        p.add_phase("脚手架", "CLI框架选型 + 参数解析")
        p.add_phase("核心功能", "主要业务逻辑实现")
        p.add_phase("用户体验", "彩色输出 + 进度条 + 自动补全")
        p.add_phase("打包发布", "PyPI/GitHub Release配置")
        return p
```

## 使用场景

1. **功能开发**: 复杂功能拆解为可执行的阶段和任务
2. **架构设计**: 提前暴露依赖和风险点
3. **工期评估**: 每个任务标记人时，自动计算交付时间
4. **新人入职**: 新人拿到计划就知道先做什么后做什么

## 依赖

- Python 3.8+
- 无第三方依赖

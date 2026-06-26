"""
Document Generator - 文档生成器
基于扫描结果和模板生成 SDD 文档
"""

import re
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime


class DocumentGenerator:
    """文档生成器"""
    
    def __init__(self):
        self.templates = {}
        
    def generate(self, doc_type: str, context: Dict) -> str:
        """生成文档"""
        generators = {
            'srs': self._generate_srs,
            'sad': self._generate_sad,
            'sdd': self._generate_sdd,
            'dbd': self._generate_dbd,
            'apid': self._generate_apid,
            'tsd': self._generate_tsd
        }
        
        generator = generators.get(doc_type)
        if not generator:
            return f"❌ 不支持的文档类型: {doc_type}"
        
        return generator(context)
    
    def _generate_srs(self, context: Dict) -> str:
        """生成 SRS 文档"""
        project = context.get('project', {})
        tech_stack = project.get('tech_stack', {})
        api = context.get('api', {})
        
        content = f"""# 软件需求规格说明书 (SRS)

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | {project.get('name', '未知项目')} |
| 版本 | v1.0.0 |
| 作者 | SDD 自动生成 |
| 日期 | {datetime.now().strftime('%Y-%m-%d')} |

---

## 1. 引言

### 1.1 目的

本文档描述 **{project.get('name', '项目')}** 的软件需求规格，包括功能需求、非功能需求和接口需求。

### 1.2 范围

本项目是一个 **{tech_stack.get('framework', '应用程序')}** 项目，主要提供以下核心功能：

{self._generate_feature_overview(context)}

### 1.3 术语定义

| 术语 | 定义 |
|------|------|
| API | 应用程序接口 |
| SDK | 软件开发工具包 |
| SSO | 单点登录 |

---

## 2. 总体描述

### 2.1 产品背景

{project.get('name', '项目')} 是基于 **{tech_stack.get('language', 'Java')}** 技术栈开发的{template_type}。

### 2.2 技术架构

| 层级 | 技术 | 说明 |
|------|------|------|
| 基础框架 | {tech_stack.get('framework', 'N/A')} | 核心框架 |
| 数据库 | {tech_stack.get('database', 'N/A')} | 数据存储 |
| 缓存 | {tech_stack.get('cache', 'N/A')} | 缓存加速 |
| 消息队列 | {tech_stack.get('mq', 'N/A')} | 异步处理 |

### 2.3 模块划分

{self._generate_module_overview(context)}

---

## 3. 功能需求

### 3.1 核心功能模块

{self._generate_functional_modules(api)}

### 3.2 功能列表

{self._generate_function_list(api)}

---

## 4. 非功能需求

### 4.1 性能需求

| 指标 | 要求 | 说明 |
|------|------|------|
| API 响应时间 | P99 < 200ms | 正常负载 |
| 并发支持 | 500+ QPS | 单实例 |
| 吞吐量 | 1000 req/s | 最大 |

### 4.2 安全需求

| 需求 | 说明 |
|------|------|
| 认证机制 | JWT Token |
| 权限控制 | RBAC 角色权限 |
| 数据加密 | HTTPS 传输加密 |

### 4.3 可用性需求

| 指标 | 要求 |
|------|------|
| 可用性 | 99.9% |
| 故障恢复 | < 5 分钟 |
| 监控 | 全链路监控 |

---

## 5. 接口需求

### 5.1 接口概述

本项目提供 **{api.get('endpoint_count', 0)}** 个 API 接口。

### 5.2 接口列表

{self._generate_api_summary(api)}

---

## 6. 数据流概述

```
客户端 → API Gateway → 业务服务 → 数据库/缓存
                     ↓
                   消息队列
```

---

*文档版本: v1.0.0*
*最后更新: {datetime.now().strftime('%Y-%m-%d')}*
"""
        return content
    
    def _generate_sad(self, context: Dict) -> str:
        """生成 SAD 文档"""
        project = context.get('project', {})
        tech_stack = project.get('tech_stack', {})
        modules = project.get('modules', [])
        
        content = f"""# 软件架构文档 (SAD)

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | {project.get('name', '未知项目')} |
| 版本 | v1.0.0 |
| 日期 | {datetime.now().strftime('%Y-%m-%d')} |

---

## 1. 架构概述

### 1.1 系统目标

{project.get('name', '项目')} 采用 **{tech_stack.get('framework', '标准架构'}** 架构，确保系统具备以下特性：

- 高可用性
- 可扩展性
- 可维护性
- 安全性

### 1.2 架构原则

| 原则 | 说明 |
|------|------|
| 分层职责 | 各层职责清晰单一 |
| 依赖倒置 | 依赖接口而非实现 |
| 面向对象 | 合理运用 OOP 原则 |

---

## 2. 技术选型

### 2.1 技术栈概览

| 组件 | 选型 | 版本 | 说明 |
|------|------|------|------|
| 编程语言 | {tech_stack.get('language', 'N/A')} | {tech_stack.get('versions', {}).get('java', 'N/A')} | 主力语言 |
| 应用框架 | {tech_stack.get('framework', 'N/A')} | - | 核心框架 |
| 数据库 | {tech_stack.get('database', 'N/A')} | - | 持久化存储 |
| 缓存 | {tech_stack.get('cache', 'N/A')} | - | 热点数据缓存 |
| 消息队列 | {tech_stack.get('mq', 'N/A')} | - | 异步解耦 |

### 2.2 架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                           客户端                                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         API Gateway                               │
│                    (路由 / 认证 / 限流)                          │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        业务服务层                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ Controller   │  │  Service    │  │    DAL      │           │
│  │ (适配层)    │  │  (服务层)    │  │ (数据层)    │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
       ┌───────────┐    ┌───────────┐    ┌───────────┐
       │  Database │    │   Cache   │    │    MQ     │
       └───────────┘    └───────────┘    └───────────┘
```

---

## 3. 模块设计

### 3.1 模块概览

{self._generate_modules_detail(context)}

### 3.2 分层架构

{self._generate_layer_architecture(context)}

---

## 4. 核心流程

### 4.1 请求处理流程

```
1. 客户端发起请求
          ↓
2. API Gateway 路由认证
          ↓
3. Controller 接收请求
          ↓
4. 参数校验
          ↓
5. 调用 Service 层
          ↓
6. Service 业务逻辑处理
          ↓
7. DAL 层数据操作
          ↓
8. 返回响应
```

### 4.2 异步处理流程

```
业务操作 → 发送消息 → MQ → 消费者处理 → 结果存储
```

---

## 5. 部署架构

### 5.1 部署拓扑

```
                    ┌─────────────────┐
                    │   Nginx/Kong    │
                    │   负载均衡      │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
  ┌───────────┐       ┌───────────┐       ┌───────────┐
  │ Instance 1│       │ Instance 2│       │ Instance 3│
  └───────────┘       └───────────┘       └───────────┘
```

---

## 6. 架构决策记录 (ADR)

### ADR-001: 采用分层架构

**决策**: 采用 Controller → Service → DAL 分层架构

**理由**:
1. 职责清晰分离
2. 便于测试和维护
3. 符合企业级开发规范

---

*文档版本: v1.0.0*
*最后更新: {datetime.now().strftime('%Y-%m-%d')}*
"""
        return content
    
    def _generate_sdd(self, context: Dict) -> str:
        """生成 SDD 文档"""
        project = context.get('project', {})
        api = context.get('api', {})
        
        return f"""# 详细设计文档 (SDD)

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | {project.get('name', '未知项目')} |
| 版本 | v1.0.0 |
| 日期 | {datetime.now().strftime('%Y-%m-%d')} |

---

## 1. 模块详细设计

{self._generate_class_diagrams(api)}

---

## 2. 接口设计

{self._generate_interface_design(api)}

---

## 3. 数据结构设计

### 3.1 DTO 设计

{self._generate_dto_design(api)}

### 3.2 枚举定义

{self._generate_enum_design(api)}

---

## 4. 异常处理

### 4.1 异常分类

| 异常类型 | 父类 | 使用场景 |
|----------|------|----------|
| BizException | RuntimeException | 业务异常 |
| ValidateException | RuntimeException | 参数校验异常 |
| SystemException | RuntimeException | 系统异常 |

### 4.2 错误码定义

| 错误码 | 描述 |
|--------|------|
| 10001 | 参数校验失败 |
| 10002 | 认证失败 |
| 20001 | 业务处理失败 |

---

*文档版本: v1.0.0*
*最后更新: {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    def _generate_dbd(self, context: Dict) -> str:
        """生成 DBD 文档"""
        db = context.get('database', {})
        
        content = f"""# 数据库设计文档 (DBD)

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | {context.get('project', {}).get('name', '未知项目')} |
| 版本 | v1.0.0 |
| 日期 | {datetime.now().strftime('%Y-%m-%d')} |

---

## 1. 数据库概述

### 1.1 数据库信息

| 属性 | 值 |
|------|-----|
| 数据库类型 | {db.get('db_type', 'Unknown')} |
| 表数量 | {len(db.get('tables', []))} |
| 迁移文件 | {len(db.get('migrations', []))} |

---

## 2. 表结构

{self._generate_table_structures(db)}

---

## 3. 索引设计

{self._generate_index_design(db)}

---

## 4. ER 图

```
{self._generate_er_diagram(db)}
```

---

*文档版本: v1.0.0*
*最后更新: {datetime.now().strftime('%Y-%m-%d')}*
"""
        return content
    
    def _generate_apid(self, context: Dict) -> str:
        """生成 APID 文档"""
        api = context.get('api', {})
        
        return f"""# API 接口文档 (APID)

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | {context.get('project', {}).get('name', '未知项目')} |
| 版本 | v1.0.0 |
| 日期 | {datetime.now().strftime('%Y-%m-%d')} |

---

## 1. 接口概述

| 属性 | 值 |
|------|-----|
| Controller 数量 | {api.get('controller_count', 0)} |
| 接口总数 | {api.get('endpoint_count', 0)} |
| 认证方式 | JWT Bearer Token |

---

## 2. 统一响应格式

```json
{{
  "code": 200,
  "message": "success",
  "data": {{}}
}}
```

---

## 3. 接口列表

{self._generate_api_list(api)}

---

## 4. 错误码定义

| 错误码 | 描述 |
|--------|------|
| 200 | 成功 |
| 40001 | 参数校验失败 |
| 40002 | 认证失败 |
| 50000 | 系统异常 |

---

*文档版本: v1.0.0*
*最后更新: {datetime.now().strftime('%Y-%m-%d')}*
"""
    
    def _generate_tsd(self, context: Dict) -> str:
        """生成 TSD 文档"""
        project = context.get('project', {})
        
        return f"""# 测试设计文档 (TSD)

## 文档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | {project.get('name', '未知项目')} |
| 版本 | v1.0.0 |
| 日期 | {datetime.now().strftime('%Y-%m-%d')} |

---

## 1. 测试策略

### 1.1 测试金字塔

```
        E2E 测试 (少量)
       ┌─────────────┐
       │ 集成测试    │
       │  (适量)     │
       └─────────────┘
      ┌─────────────┐
      │ 单元测试    │
      │  (核心)     │
      └─────────────┘
```

### 1.2 测试目标

| 测试类型 | 覆盖率目标 |
|----------|------------|
| 单元测试 | ≥ 80% |
| 集成测试 | ≥ 60% |
| E2E 测试 | 关键路径 |

---

## 2. 单元测试

### 2.1 测试框架

| 组件 | 选型 |
|------|------|
| 测试框架 | JUnit 5 |
| Mock | Mockito |
| 断言 | AssertJ |

### 2.2 测试示例

```java
@Test
void testService() {{
    // Given
    // When
    // Then
}}
```

---

## 3. 集成测试

### 3.1 测试配置

```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb
```

---

*文档版本: v1.0.0*
*最后更新: {datetime.now().strftime('%Y-%m-%d')}*
"""

    # ========== 辅助方法 ==========
    
    def _generate_feature_overview(self, context: Dict) -> str:
        """生成功能概述"""
        api = context.get('api', {})
        controllers = api.get('controllers', [])
        
        if not controllers:
            return "- 核心业务功能模块"
        
        lines = []
        for ctrl in controllers[:5]:
            name = ctrl.get('name', '模块')
            lines.append(f"- {name.replace('Controller', '')} 功能")
        
        return '\n'.join(lines) if lines else "- 核心业务功能模块"
    
    def _generate_module_overview(self, context: Dict) -> str:
        """生成模块概览"""
        modules = context.get('project', {}).get('modules', [])
        
        if not modules:
            return "| 模块 | 说明 |\n|------|------|\n| 主模块 | 项目主模块 |"
        
        lines = ["| 模块 | 说明 |", "|------|------|"]
        for m in modules:
            name = m.get('name', '模块')
            lines.append(f"| {name} | 模块功能 |")
        
        return '\n'.join(lines)
    
    def _generate_functional_modules(self, api: Dict) -> str:
        """生成功能模块"""
        return "### 3.1.1 模块列表\n\n| 模块 | 接口数 | 说明 |\n|------|--------|------|\n"
    
    def _generate_function_list(self, api: Dict) -> str:
        """生成功能列表"""
        endpoints = api.get('endpoints', [])
        return f"本项目共包含 **{len(endpoints)}** 个接口，详见 API 接口文档。"
    
    def _generate_api_summary(self, api: Dict) -> str:
        """生成 API 摘要"""
        endpoints = api.get('endpoints', [])[:10]
        lines = ["| 接口 | 方法 | 路径 |", "|------|------|------|"]
        
        for ep in endpoints:
            lines.append(f"| {ep.get('name', '')} | {ep.get('method', 'GET')} | {ep.get('path', '')} |")
        
        return '\n'.join(lines)
    
    def _generate_modules_detail(self, context: Dict) -> str:
        """生成模块详情"""
        return "### 3.1 模块结构\n\n| 模块名 | 类型 | 说明 |\n|--------|------|------|\n"
    
    def _generate_layer_architecture(self, context: Dict) -> str:
        """生成分层架构"""
        return """### 3.2 分层说明

| 层级 | 职责 | 典型类 |
|------|------|--------|
| Controller | 接收请求、参数校验 | *Controller.java |
| Service | 业务逻辑处理 | *Service.java |
| DAL | 数据访问 | *Mapper.java |
"""
    
    def _generate_class_diagrams(self, api: Dict) -> str:
        """生成类图"""
        controllers = api.get('controllers', [])
        if not controllers:
            return "暂无 Controller 类信息"
        
        lines = ["### 1.1 Controller 类图\n\n"]
        for ctrl in controllers[:3]:
            name = ctrl.get('name', '')
            lines.append(f"**{name}**")
            for ep in ctrl.get('endpoints', [])[:3]:
                lines.append(f"- `{ep.get('method', 'GET')} {ep.get('path', '')}`")
            lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_interface_design(self, api: Dict) -> str:
        """生成接口设计"""
        endpoints = api.get('endpoints', [])[:10]
        
        lines = ["### 2.1 主要接口\n\n"]
        for ep in endpoints:
            lines.append(f"""#### {ep.get('name', '接口')}

- **路径**: `{ep.get('path', '')}`
- **方法**: `{ep.get('method', 'GET')}`
- **描述**: {ep.get('description', '无描述')}

""")
        
        return '\n'.join(lines)
    
    def _generate_dto_design(self, api: Dict) -> str:
        """生成 DTO 设计"""
        dtos = api.get('dto_classes', [])[:5]
        
        if not dtos:
            return "暂无 DTO 类信息"
        
        lines = ["### 3.1 DTO 类\n\n"]
        for dto in dtos:
            lines.append(f"**{dto.get('name', '')}**")
            for field in dto.get('fields', [])[:5]:
                lines.append(f"- `{field.get('type', '')} {field.get('name', '')}`")
            lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_enum_design(self, api: Dict) -> str:
        """生成枚举设计"""
        return "### 3.2 枚举定义\n\n暂无枚举类信息"
    
    def _generate_table_structures(self, db: Dict) -> str:
        """生成表结构"""
        tables = db.get('tables', [])
        
        if not tables:
            return "暂无表结构信息"
        
        lines = []
        for table in tables[:5]:
            name = table.get('name', '')
            schema = table.get('schema', '')
            lines.append(f"### {schema}.{name}\n")
            lines.append(f"\n| 字段名 | 类型 | 说明 |")
            lines.append("|--------|------|------|")
            
            for col in table.get('columns', [])[:10]:
                lines.append(f"| {col.get('name', '')} | {col.get('type', '')} | {col.get('comment', '')} |")
            
            lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_index_design(self, db: Dict) -> str:
        """生成索引设计"""
        return "| 索引名 | 类型 | 字段 | 说明 |\n|--------|------|------|------|\n"
    
    def _generate_er_diagram(self, db: Dict) -> str:
        """生成 ER 图"""
        tables = db.get('tables', [])
        return f"本项目包含 {len(tables)} 张数据表，详见上方表结构。"
    
    def _generate_api_list(self, api: Dict) -> str:
        """生成 API 列表"""
        controllers = api.get('controllers', [])
        
        lines = []
        for ctrl in controllers:
            name = ctrl.get('name', '')
            lines.append(f"### {name}\n")
            
            for ep in ctrl.get('endpoints', []):
                lines.append(f"""**{ep.get('name', '接口')}**

- URL: `{ep.get('method', 'GET')} {ep.get('path', '')}`
- 描述: {ep.get('description', '无描述')}

""")
        
        return '\n'.join(lines) if lines else "暂无接口信息"


# 导出
__all__ = ['DocumentGenerator']

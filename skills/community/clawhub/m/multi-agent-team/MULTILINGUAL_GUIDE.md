# Trae Multi-Agent 多语言使用说明

## 概述

Trae Multi-Agent 现已支持中英文双语，能够根据用户的语言自动切换响应语言，提供无缝的多语言使用体验。

## 语言切换机制

### 自动识别

系统会自动识别用户使用的语言：

- **中文输入** → 所有响应使用中文
- **English input** → All responses in English
- **混合使用** → 以首次使用的语言为准
- **明确切换** → 用户可要求使用特定语言

### 示例

#### 中文会话
```
用户：设计一个电商系统架构

AI: 📋 已接收任务，开始分析...
    🔍 识别为架构师任务
    📝 创建任务列表...
```

#### English Session
```
User: Design an e-commerce system architecture

AI: 📋 Task received, starting analysis...
    🔍 Identified as architect task
    📝 Creating task list...
```

#### Mixed (First Language Wins)
```
用户：Code review this module

AI: 📋 已接收任务，开始代码审查...
    （首次检测为中文，使用中文响应）
```

## 支持的语言范围

### 所有输出内容

✅ **角色定义和 Prompt**
- 角色职责描述
- 触发关键词
- 典型任务
- 完整 Prompt

✅ **状态更新和进度提示**
- 任务接收确认
- 角色识别通知
- 任务列表创建
- 进度更新

✅ **审查报告和问题清单**
- 代码规范审查
- 安全性审查
- 性能审查
- 架构一致性审查

✅ **错误信息和成功提示**
- 编译错误
- 测试失败
- 操作成功
- 警告信息

✅ **文档和注释**
- 生成的文档
- 代码注释
- README 文件
- API 文档

## 角色名称映射

| 中文 | English |
|------|---------|
| 架构师 | Architect |
| 产品经理 | Product Manager |
| 测试专家 | Test Expert |
| 独立开发者 | Solo Coder |

## 代码注释规范

### 自动检测

系统会检测现有代码的注释语言：

- **中文注释代码** → 新增注释使用中文
- **English comments** → New comments in English
- **无明确偏好** → 默认使用英文（国际通用）

### 示例

#### 中文注释代码
```java
/**
 * 用户服务类
 * 处理用户相关的业务逻辑
 */
public class UserService {
    // 获取用户信息
    public User getUser(Long id) {
        // ... 实现
    }
}
```

#### English Comments
```java
/**
 * User service class
 * Handles user-related business logic
 */
public class UserService {
    // Get user information
    public User getUser(Long id) {
        // ... implementation
    }
}
```

## 文档生成

### 根据用户语言生成文档

#### 中文文档
```markdown
# 用户模块

## 功能说明
用户注册、登录、信息管理

## API 接口
- POST /api/user/register - 用户注册
- GET /api/user/{id} - 获取用户信息
```

#### English Documentation
```markdown
# User Module

## Functionality
User registration, login, and profile management

## API Endpoints
- POST /api/user/register - User registration
- GET /api/user/{id} - Get user information
```

## 使用场景

### 场景 1: 纯中文项目

```
用户：为电商平台设计系统架构
AI（架构师）: 📋 已接收任务...
    - 设计系统架构
    - 编写中文文档
    - 生成中文注释
```

### 场景 2: 纯英文项目

```
User: Design system architecture for e-commerce platform
AI (Architect): 📋 Task received...
    - Design system architecture
    - Write English documentation
    - Generate English comments
```

### 场景 3: 国际化团队

```
用户 1（中文）: 设计用户模块
AI: 📋 已接收任务...（中文响应）

用户 2（English）: Review the user module design
AI: 📋 Task received...（英文响应，根据用户 2 的语言）
```

## 多语言 Prompt 文档

完整的英文 Prompt 文档已提供：
- 📄 [ENGLISH_PROMPTS.md](ENGLISH_PROMPTS.md) - 英文版角色定义和 Prompt

## 最佳实践

### 1. 保持一致性

建议在整个项目中保持使用同一种语言：

```
✅ 推荐：
- 所有文档使用英文
- 所有注释使用中文

❌ 不推荐：
- 文档中英文混杂
- 注释一会儿中文一会儿英文
```

### 2. 明确指定语言

如有特殊需求，可明确指定语言：

```
用户："请用英文生成文档"
用户："Please use Chinese for comments"
```

### 3. 国际化项目

对于国际化项目，建议：

- **代码注释**: 使用英文（国际通用）
- **用户文档**: 根据目标用户群体选择
- **API 文档**: 使用英文（便于国际协作）

## 语言切换示例

### 示例 1: 架构设计（中文）

```
用户：设计一个微服务架构

AI（架构师）:
📋 已接收任务，开始分析...
🔍 识别为架构师任务
📝 创建任务列表:
  - 任务 1: 分析现有系统 (pending)
  - 任务 2: 设计微服务架构 (pending)
  - 任务 3: 技术选型 (pending)
  - 任务 4: 部署方案 (pending)

开始架构设计...
🏛️ 系统架构设计完成
📊 输出：
  - 系统架构图
  - 模块职责清单
  - 接口定义
  - 数据模型设计
  - 部署架构说明
```

### Example 2: Code Review (English)

```
User: Review this code for security issues

AI (Architect):
📋 Task received, starting code review...
🔍 Identified as architect task
📝 Creating task list:
  - Task 1: Security review (pending)
  - Task 2: Performance review (pending)
  - Task 3: Standards review (pending)

Starting security review...
🚨 Security review completed
📊 Output:
  - Critical issues: 2
  - Major issues: 3
  - Minor issues: 5
  
Detailed report generated.
```

### 示例 3: 测试用例（中文）

```
用户：为用户登录功能编写测试用例

AI（测试专家）:
📋 已接收任务，开始测试设计...
🔍 识别为测试专家任务
📝 创建任务列表:
  - 任务 1: 设计正常场景测试 (pending)
  - 任务 2: 设计异常场景测试 (pending)
  - 任务 3: 设计边界条件测试 (pending)
  - 任务 4: 编写自动化测试 (pending)

开始测试用例设计...
✅ 测试用例设计完成
📊 输出:
  - 正常场景：3 个用例
  - 异常场景：5 个用例
  - 边界条件：4 个用例
  - 性能测试：2 个用例
```

### Example 4: Feature Development (English)

```
User: Implement user registration feature

AI (Solo Coder):
📋 Task received, starting development...
🔍 Identified as solo coder task
📝 Creating task list:
  - Task 1: Implement user model (pending)
  - Task 2: Implement service layer (pending)
  - Task 3: Implement controller (pending)
  - Task 4: Write unit tests (pending)

Starting development...
✅ Feature implementation completed
📊 Output:
  - User model class
  - Service layer implementation
  - REST API endpoints
  - Unit tests (95% coverage)
```

## 常见问题

### Q1: 如何切换语言？
A: 直接使用目标语言与 AI 对话即可，系统会自动识别并切换。

### Q2: 可以中途切换语言吗？
A: 可以，但建议保持项目语言一致性。如需切换，建议在新任务开始时切换。

### Q3: 代码注释使用什么语言？
A: 系统会检测现有代码的注释语言，自动匹配。新项目建议使用英文注释。

### Q4: 文档可以生成多种语言吗？
A: 可以，但建议根据项目需求选择主要语言。国际化项目建议生成英文文档。

### Q5: 多语言支持会影响性能吗？
A: 不会，语言识别是自动的，对性能无影响。

## 总结

Trae Multi-Agent 的多语言支持特性：

✅ **自动识别** - 无需手动配置，自动检测用户语言  
✅ **完全覆盖** - 所有输出内容都支持多语言  
✅ **智能匹配** - 代码注释自动匹配现有语言  
✅ **灵活切换** - 支持会话中切换语言  
✅ **文档齐全** - 提供完整的英文 Prompt 文档  

无论您使用中文还是英文，都能获得一致的高质量服务！

---

**文档版本**: v1.0  
**更新日期**: 2026-03-04  
**维护者**: Trae Multi-Agent Team

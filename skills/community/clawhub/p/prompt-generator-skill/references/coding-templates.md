# Coding Templates Library

## Overview

This file contains detailed templates for various coding tasks.

---

## 1. Code Generation (代码生成)

### Template 1: Basic Function (基础函数)

**Use when:** User wants to create a simple function

```
用[语言]写一个[功能]函数。
输入：[输入参数]
输出：[返回值]
要求：代码简洁，有注释
```

**Example:**
```
用Python写一个计算斐波那契数列的函数。
输入：整数n
输出：第n个斐波那契数
要求：代码简洁，有注释
```

### Template 2: Complete Program (完整程序)

**Use when:** User wants a complete program

```
用[语言]写一个[功能]程序。
功能需求：
1. [需求1]
2. [需求2]
3. [需求3]
输入：[输入格式]
输出：[输出格式]
要求：代码有注释，结构清晰
```

### Template 3: Web Scraper (爬虫脚本)

**Use when:** User wants to scrape websites

```
用Python写一个爬虫脚本。
目标网站：[网站URL]
需要抓取：[数据内容]
存储格式：[JSON/CSV/数据库]
要求：
1. 添加请求头模拟浏览器
2. 添加延时避免被封
3. 异常处理
```

---

## 2. Code Optimization (代码优化)

### Template 4: Code Refactoring (代码重构)

**Use when:** User wants to improve code quality

```
帮我重构以下代码：
[代码]
要求：
1. 提高可读性
2. 优化性能
3. 遵循[语言]最佳实践
4. 添加注释
```

### Template 5: Bug Fix (Bug修复)

**Use when:** User has code with bugs

```
以下代码有问题，帮我找出并修复：
[代码]
问题描述：[具体问题]
期望结果：[正确行为]
```

### Template 6: Performance Optimization (性能优化)

**Use when:** User wants to improve code performance

```
帮我优化以下代码的性能：
[代码]
当前问题：[性能问题]
优化目标：[目标]
要求：保持功能不变
```

---

## 3. Database (数据库)

### Template 7: SQL Query (SQL查询)

**Use when:** User needs SQL queries

```
帮我写一个SQL查询。
数据库：[数据库类型]
表结构：
[表名]
- [字段1]: [类型]
- [字段2]: [类型]
查询需求：[要查询什么]
条件：[筛选条件]
排序：[排序方式]
```

### Template 8: Database Design (数据库设计)

**Use when:** User needs to design database schema

```
帮我设计一个[系统名称]的数据库结构。
主要实体：
1. [实体1]
2. [实体2]
3. [实体3]
关系说明：[实体间关系]
要求：符合第三范式
```

---

## 4. Automation (自动化脚本)

### Template 9: File Processing (文件处理)

**Use when:** User wants to process files automatically

```
用Python写一个文件处理脚本。
功能：[处理什么文件]
输入目录：[源目录]
输出目录：[目标目录]
处理逻辑：[具体操作]
要求：支持批量处理，有进度显示
```

### Template 10: Scheduled Task (定时任务)

**Use when:** User wants scheduled automation

```
帮我写一个定时任务脚本。
任务内容：[要执行的任务]
执行频率：[每天/每周/每小时]
具体时间：[几点执行]
输出：[结果保存方式]
```

---

## 5. API Development (API开发)

### Template 11: REST API (REST接口)

**Use when:** User wants to create REST APIs

```
用[框架]创建一个REST API。
功能：[API功能]
端点：[URL路径]
方法：[GET/POST/PUT/DELETE]
请求参数：[参数列表]
响应格式：[JSON格式]
要求：添加参数验证和错误处理
```

### Template 12: API Integration (API集成)

**Use when:** User wants to integrate with external APIs

```
帮我写一个调用[服务名称]API的代码。
API文档：[文档链接或描述]
功能：[要实现的功能]
认证方式：[API Key/OAuth/其他]
要求：封装成函数，便于复用
```

---

## 6. Testing (测试)

### Template 13: Unit Test (单元测试)

**Use when:** User wants to write unit tests

```
帮我为以下代码写单元测试：
[代码]
测试框架：[pytest/unittest/其他]
覆盖场景：
1. 正常情况
2. 边界情况
3. 异常情况
```

### Template 14: Integration Test (集成测试)

**Use when:** User wants integration tests

```
帮我写一个集成测试。
测试场景：[测试什么]
测试步骤：
1. [步骤1]
2. [步骤2]
3. [步骤3]
验证点：[如何判断测试通过]
```

---

## 7. Common Patterns (常用模式)

### Design Patterns

| Pattern | Use Case | Template |
|---------|----------|----------|
| 单例模式 | 全局唯一实例 | `帮我用单例模式实现[功能]` |
| 工厂模式 | 对象创建 | `帮我用工厂模式创建[对象类型]` |
| 观察者模式 | 事件监听 | `帮我用观察者模式实现[事件系统]` |
| 策略模式 | 算法切换 | `帮我用策略模式实现[算法选择]` |

### Code Style

| Language | Style Guide | Example |
|----------|-------------|---------|
| Python | PEP 8 | `遵循PEP 8规范` |
| JavaScript | ESLint | `遵循Airbnb风格指南` |
| Java | Google Java Style | `遵循Google Java编程规范` |
| Go | Go Style | `遵循Go官方代码规范` |

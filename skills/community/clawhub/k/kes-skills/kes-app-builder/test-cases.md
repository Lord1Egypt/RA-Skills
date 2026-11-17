---
name: kes-app-builder
description: KingbaseES 应用构建编排器 — 测试用例
---

# KingbaseES 应用构建编排器测试用例

## 测试用例 1: Java Spring Boot 项目构建

**场景**：用户需要一个完整的企业级 Java 项目

**输入问题**："帮我用 Java 构建一个连接金仓数据库的项目"

**期望答案要点**：
- 确认需求（Web API？数据量级？）
- 推荐 Java + Spring Boot + MyBatis
- 触发 kes-java 获取 JDBC 配置
- 触发 kes-hibernate 获取 MyBatis 集成
- 提供项目结构参考

**验证方法**：答案包含引导式交互和技能触发

---

## 测试用例 2: 未指定技术栈

**场景**：用户只说要做个应用，没指定技术

**输入问题**："帮我做一个管理金仓数据的后台"

**期望答案要点**：
- 默认推荐 Java + Spring Boot
- 说明推荐理由（政企场景 Java 生态成熟）
- 提供技术栈选择表格
- 等待用户确认

**验证方法**：答案默认推荐 Java 并提供选择

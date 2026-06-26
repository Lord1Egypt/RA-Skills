---
name: magic-dev
description: 面向 magic-api 开发、排障、二开与升版审查的本地源码技能。基于 magic-api、magic-api-plugin、magic-script、magic-api-example 四个仓库整理，强调按问题类型快速定位源码、样例与升级审查资料。
license: MIT
---

# magic 开发增强技能

这是一份面向 **magic-api 实战开发** 的本地技能入口。

它不重复展开完整教程，而是把 4 个本地仓库和 `references/` 下的资料组织成一条更适合 Claude 使用的检索路径：**先判断问题类型，再去最合适的样例、源码或审查文档。**

## 这份 skill 适合处理什么问题

优先用于这些场景：

- 写 `.ms` 接口、CRUD、分页、事务、文件响应
- 理解 `db` / `request` / `response` / `http` 等模块怎么工作
- 做自定义模块、函数、扩展方法、provider、interceptor、starter
- 对照 example 和源码排查“不生效 / 报错 / 行为不一致”
- 分析 magic 版本升级影响，输出审查结论和改造方案

## 四个仓库怎么分工

先记住最短检索顺序：

- `magic-api`：框架主实现，先看自动配置、资源加载、内置模块、扩展注册
- `magic-script`：脚本语言与运行时，先看编译、执行、`import`、`exit`、上下文变量
- `magic-api-example`：现成 `.ms` 样例、扩展模板、Spring Boot 示例配置
- `magic-api-plugin`：插件 / starter 做法，适合对照自动配置和配置元数据

常用入口：

- 自动配置入口：`magic-api/magic-api-spring-boot-starter/src/main/java/org/ssssssss/magicapi/spring/boot/starter/MagicAPIAutoConfiguration.java`
- 配置定义：`magic-api/magic-api/src/main/java/org/ssssssss/magicapi/core/config/MagicAPIProperties.java`
- 脚本运行时：`magic-script/src/main/java/org/ssssssss/script/MagicScript.java`
- 上下文变量：`magic-script/src/main/java/org/ssssssss/script/MagicScriptContext.java`
- 示例配置与扩展入口：`magic-api-example/src/main/resources/application.yml`、`magic-api-example/src/main/java/org/ssssssss/example/configuration/MagicAPIConfiguration.java`

按目录找入口时，先看 [仓库目录导航](references/repo-map.md)。

## Claude 使用这份 skill 的回答策略

默认按下面顺序回答：

1. **先判断问题类型**：现成写法 / 原理 / 排障 / 二开 / 插件 / 升版
2. **先给最短结论**：先回答“怎么做”或“先查哪里”
3. **能给样例就先给样例**：优先 `.ms` 样例和 example 扩展类
4. **再补源码依据**：需要解释原理时再回到 `magic-api` / `magic-script`
5. **排障先给排查顺序**：先说配置、资源、模块、运行时各查什么
6. **二开先判断扩展点类型**：模块 / 函数 / 扩展方法 / provider / interceptor / starter
7. **升版先识别版本与使用面**：先看当前版本、目标版本、脚本/扩展/插件使用范围，再给建议

如果要展开具体回答结构，先看 [回答组织手册](references/answering-playbook.md)。

## 什么时候先看哪组资料

### 1. 入门与现成示例

先看这组：当你要 **马上给脚本、配置或业务示例**。

- [magic-script 语法参考](references/syntax.md)
- [数据库操作参考](references/database.md)
- [业务场景示例](references/examples.md)

### 2. 源码与扩展

先看这组：当你要 **解释原理、定位实现、判断扩展点**。

- [源码架构与入口](references/architecture.md)
- [模块与扩展开发](references/extensions.md)
- [magic-script 语法与运行时](references/script-runtime.md)
- [示例与插件对照](references/examples-and-plugins.md)

### 3. 检索与回答

先看这组：当你要 **快速决定先读哪份源码、先怎么排查、怎么组织答案**。

- [常见提问与源码/样例导航](references/practical-qa-navigation.md)
- [故障排查导航](references/troubleshooting.md)
- [回答组织手册](references/answering-playbook.md)
- [仓库目录导航](references/repo-map.md)

### 4. 升版审查

先看这组：当你要 **分析用户项目升级影响并输出审查结论**。

推荐顺序：`quick-prompt -> checklist -> template -> example`，必要时再补 `upgrade-migration-guide`。

- [升版后的脚本代码调整指引](references/upgrade-migration-guide.md)
- [升级审查清单](references/upgrade-review-checklist.md)
- [升级审查输出模板](references/upgrade-review-template.md)
- [升级审查示例](references/upgrade-review-example.md)
- [升级审查快速发起提示词](references/upgrade-review-quick-prompt.md)

## 使用原则

- 要现成方案：先找 `magic-api-example` 和基础 references
- 要解释机制：先看 `architecture.md`、`script-runtime.md`、`extensions.md`
- 要做插件 / starter：先看 `magic-api-plugin` 和 `examples-and-plugins.md`
- 要定位目录：先看 `repo-map.md`
- 要排障：先看 `troubleshooting.md`
- 要做升级审查：按升版专题资料的顺序走，不要一上来就给改法

这份 skill 的目标不是“把 magic-api 讲全”，而是让 Claude 在回答时 **先给正确路径，再给正确内容，再给源码依据**。

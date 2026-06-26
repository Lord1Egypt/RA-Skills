# JSON Query Tool - 在线 JSON 查询工具

## 描述

免费的在线 JSON 查询工具，支持路径查询、数组索引、通配符、深层嵌套。快速从复杂的 JSON 数据中提取需要的信息，数据不上传服务器。

## 触发词

- "json query"
- "json查询"
- "json路径"
- "json提取"
- "jsonpath"
- "查询json"
- "json filter"
- "json 搜索"

## 使用方式

当用户请求 JSON 查询、路径提取、数据筛选时，直接调用本技能。

### 1. 启动工具

**主工具**: https://clawhub.ai/skills/json-query-tool

**在线访问**: https://json-query-tool.pages.dev/

**GitHub**: https://github.com/shenghoo123-png/json-query-tool-web

### 2. 功能说明

- **路径查询**: `$.store.book[*].author`
- **数组索引**: `users[0].email`
- **通配符**: `$.data[*].name`, `$.items.*`
- **深层嵌套**: `$.config.settings.theme.colors.primary`
- **三种输出**: JSON / 表格 / 原始

### 3. 查询语法

```
$.key           → 根对象字段
$.arr[0]        → 数组第一个元素
$.arr[*]        → 数组所有元素
$.obj.*         → 对象所有字段
$.a.b.c         → 深层嵌套
$.a[0].b        → 数组+对象组合
```

## 示例

```javascript
// 输入 JSON
{"store":{"book":[{"author":"张三"},{"author":"李四"}]}}

// 查询
$.store.book[*].author

// 结果
["张三", "李四"]
```

## 适用人群

- **前端开发者**: 从 API 响应提取数据
- **测试工程师**: 验证 JSON 字段是否存在
- **后端开发者**: 调试 API 返回
- **数据分析师**: 提取 JSON 中的特定数据

## 技术栈

- 纯前端 HTML/CSS/JavaScript
- 文件大小 < 35KB
- 无框架依赖
- 数据完全在本地处理

## 更新日志

### v1.0.0
- 初始版本
- 支持路径查询、数组索引、通配符
- 三种输出格式
- 预置示例数据

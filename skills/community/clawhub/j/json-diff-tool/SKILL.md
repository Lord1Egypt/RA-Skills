# JSON Diff Tool - 在线 JSON 对比工具

## 描述

免费的在线 JSON 对比工具，支持语法高亮、路径级别差异分析、数据不上传服务器。快速找出两个 JSON 之间的差异，适用于 API 响应对比、配置文件对比、测试数据对比等场景。

## 触发词

- "json diff"
- "json对比"
- "json比较"
- "json差异"
- "比较两个json"
- "diff json"
- "json 区别"

## 使用方式

当用户请求 JSON 对比、JSON 差异、JSON 比较时，直接调用本技能。

### 1. 启动工具

用户访问以下任一 URL：

**主工具**: https://clawhub.ai/skills/json-diff-tool

**直接访问**: https://phil-sell-atlantic-weddings.trycloudflare.com/tools/json-diff/

**GitHub**: https://github.com/shenghoo123-png/json-diff-tool

### 2. 功能说明

- **左侧 JSON A**: 粘贴第一个 JSON
- **右侧 JSON B**: 粘贴第二个 JSON
- 点击「对比」查看差异
- 支持交换左右两侧内容
- 支持复制结果
- 预置示例数据一键加载
- 键盘快捷键: Ctrl+Enter 对比

### 3. 差异展示

- 绿色高亮: 新增的字段 (B 独有)
- 红色高亮: 删除的字段 (A 独有)  
- 灰色: 未变化的字段
- 路径格式: `$.name`, `$.users[0].email`, `$.data.settings.theme`

## 技术实现

- 纯前端 HTML/CSS/JavaScript，无框架依赖
- 文件大小 < 15KB
- 数据完全在本地处理，不上传服务器
- 支持深层嵌套对象和数组
- 路径查询语法: `$.key`, `$.arr[0]`, `$.obj.nested`

## 示例场景

### API 响应对比
```javascript
// 线上环境
{"status":"ok","data":{"users":3}}

// 测试环境  
{"status":"ok","data":{"users":5}}

// 差异: data.users 从 3 变成 5
```

### 配置文件对比
```javascript
// v1.0
{"version":"1.0","debug":false,"timeout":3000}

// v1.1
{"version":"1.1","debug":false,"timeout":5000}

// 差异: version 从 1.0 变成 1.1, timeout 从 3000 变成 5000
```

## 适用人群

- **后端开发者**: 对比 API 响应差异
- **测试工程师**: 验证接口返回是否符合预期
- **运维/DBA**: 对比配置文件变更
- **产品经理**: 对比不同版本的数据结构

## 替代方案

如需更强大的 JSON 查询功能（路径提取、过滤、转换），可使用 [JSON Query Tool](https://clawhub.ai/skills/json-query-tool)。

## 更新日志

### v1.0.0
- 初始版本
- 支持路径级别差异对比
- 纯前端实现，数据不上传

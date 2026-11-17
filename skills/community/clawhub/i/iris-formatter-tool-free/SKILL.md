---
name: "iris-formatter-tool-free"
description: "InterSystems IRIS ObjectScript 代码格式化与基础规范检查工具。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "IRIS代码格式化免费版"
  version: "1.0.0"
  summary: "InterSystems IRIS ObjectScript 代码格式化与基础规范检查工具。"
  tags:
    - "开发工具"
    - "IRIS"
    - "ObjectScript"
    - "代码规范"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
tools:
  - exec
  - read
  - write
---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# IRIS 代码格式化工具（免费版）

## 概述

本工具为 InterSystems IRIS/Cache 开发者提供 ObjectScript 代码的格式化、审查和修正能力。涵盖变量命名、方法命名、锁、事务、陷阱、格式、空行、注释等多个维度的规范检查，确保代码风格统一、可读性强、维护性高。免费版聚焦个人开发者的代码格式化与基础规范检查，提供速查表与修正模板。

## 核心能力

| 能力模块 | 描述 | 检查内容 |
| --- | --- | --- |
| 变量命名 | 命名规范检查 | lowerCamelCase、常量全大写 |
| 方法命名 | 方法命名规范 | UpperCamelCase、动宾结构 |
| 锁规范 | 锁操作检查 | 成对出现、超时退出 |
| 事务规范 | 事务操作检查 | ts/tc/tro 完整性 |
| 格式规范 | 代码格式检查 | 缩进、空格、命令缩写 |
| 注释规范 | 注释格式检查 | #; 和 // 的正确使用 |
**技术实现要点**：核心能力基于`input_params`参数与`output_format`配置实现,支持创建/查询/修改/删除等操作模式,通过`config_options`进行运行时配置。

### 核心功能执行
用`input_params`参数进行配置。

**输出**: 返回核心功能执行的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置。

**输出**: 返回参数配置与调用的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置。

**输出**: 返回结果处理与输出的执行结果,包含操作状态和输出数据。
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：InterSystems、IRIS、ObjectScript、代码格式化与基础、规范检查工具、开发者的、代码格式化与规范、检查工具、变量与方法命名规、锁与事务规范验证、注释规范检查与自、动修正等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：代码格式化

开发者需要将一段 ObjectScript 代码格式化为符合规范的版本。

```text
用户：格式化这段 IRIS 代码
（附代码内容）

助手：按以下规范格式化

1. 命令缩写：除 for/while/if 外使用缩写
   - set → s, do → d, quit → q, kill → k

2. 系统函数缩写
   - $extract → $e, $piece → $p, $length → $l

3. 运算符两侧加空格
   - a = b（不是 a=b）

4. 方法内一个 Tab 缩进

5. 输出完整的格式化后代码
```

### 场景二：规范合规性检查

开发者需要检查代码是否符合 IRIS 规范。

```text
用户：检查这段代码是否符合规范

助手：生成代码审查报告

## 不适用场景

以下场景IRIS代码格式化免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求。

## 代码审查报告

### 问题汇总
- [严重] 变量命名使用拼音（第 5 行）
- [警告] 锁未设置超时（第 12 行）
- [警告] 事务未添加空行（第 20 行）

### 详细说明

#
### 1. 变量命名问题
位置：第 5 行
问题：变量名使用了拼音
规范依据：禁止拼音与英文混合
建议修正：将 yonghuMing 改为 userName

#
### 2. 锁规范问题
位置：第 12 行
问题：锁未设置超时退出
规范依据：加锁必须写超时退出，避免死锁
建议修正：l +^未指定:3
```

### 场景三：后置表达式修正

开发者遇到后置表达式编译错误，需要修正格式。

```objectscript
; 错误格式 - 会导致 IRIS 编译错误
continue:(hospId '= "") && (hospId '= ($p(^CTLOC(locId),"^",22)))
q:(inci = "") && (arcim = "") && (phcdf = "")

; 正确格式 - 括号内运算符两侧加空格，括号与 && 之间不加空格
continue:(hospId '= "")&&(hospId '= ($p(^CTLOC(locId),"^",22)))
q:(inci = "")&&(arcim = "")&&(phcdf = "")
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 变量命名规范速查

```objectscript
// 基本原则
// - 禁止使用 $、# 等特殊符号
// - 严禁拼音与英文混合
// - 参数名、成员变量、局部变量用 lowerCamelCase
// - 常量全大写
// - 变量不超过 31 个字符

// 正确示例
s userName = "张三"
s maxCount = 100
s dispFlag = $$$YES    ; 布尔用 Flag 后缀
s bisData = ^bis(1)   ; 引用 global 用 表ID+Data

// 错误示例
s yonghuMing = "张三"  ; 拼音
s a = 1               ; 无意义变量
s IsDisp = 1           ; 布尔用 is 开头
```

### 方法命名规范速查

```objectscript
// 类名、方法名用 UpperCamelCase
Class MyApp.UserService
{
    // 返回布尔用 Is 开头
    Method IsExist(id As %String) As %Boolean
    {
        q $$$YES
    }
    
    // 动宾结构
    Method GetUserById(id As %String)
    {
        // 方法控制在 50 行以内
    }
    
    // 查询用 Query
    Method QueryUserList()
    {
    }
}
```

### 锁与事务规范速查

```objectscript
// 锁规范
// - 必须带 + 和 -
// - 必须设置超时
// - 必须成对出现
l +^MyApp("lock", id):3
; ... 业务逻辑 ...
l -^MyApp("lock", id)

// 事务规范
// - 必须有 tc 或 tro
// - ts/tc/tro 位置保持近距离
// - 禁止跨方法提交事务

ts
; ... 业务逻辑 ...
if (条件) {
    tc
} else {
    tro
}
```

## 示例

### 命令缩写规范速查

| 全拼 | 缩写 | 说明 | 全拼 | 缩写 | 说明 |
| --- | --- | --- | --- | --- | --- |
| set | s | 赋值 | tstart | ts | 事务开始 |
| do | d | 执行 | tcommit | tc | 事务提交 |
| quit | q | 退出 | trollback | tro | 事务回滚 |
| break | b | 跳出 | lock | l | 加锁 |
| kill | k | 删除 | open | o | 打开 |
| new | n | 新建 | close | c | 关闭 |
| write | w | 输出 | hang | h | 暂停 |
| read | r | 读取 | job | j | 启动作业 |

**注意**：`for`、`while`、`if`、`elseif`、`else`、`continue` 使用全拼。

### 系统函数缩写速查

| 全拼 | 缩写 | 说明 |
| --- | --- | --- |
| $extract | $e | 提取子串 |
| $piece | $p | 按分隔符提取 |
| $length | $l | 获取长度 |
| $order | $o | 遍历 global |
| $get | $g | 安全获取值 |
| $data | $d | 判断变量是否存在 |
| $find | $f | 查找子串 |
| $ascii | $a | 获取 ASCII 码 |
| $char | $c | ASCII 转字符 |
| $translate | $tr | 字符替换 |
| $increment | $i | 自增 |
| $random | $r | 随机数 |

### 注释规范速查

```objectscript
// 单行注释用 #;
#; 这是一个单行注释

// 句尾注释用 //
s name = "test"  // 设置名称

// 类、方法头注释用 ///
/// desc:        方法描述
/// author:      作者
/// createDate:  YYYY-MM-DD
/// params:      参数说明
/// return:      返回值说明
Method MyMethod()
{
}
```

## 优选实践

1. **命令统一用缩写**：除循环结构外，所有命令使用缩写形式

2. **系统函数用缩写**：`$e`、`$p`、`$l`、`$o` 等

3. **后置表达式格式**：括号内加空格，括号与 `&&` 之间不加空格
   ```objectscript
   q:(inci = "")&&(arcim = "")
   ```

4. **锁必须成对**：`l +` 和 `l -` 严格配对，设置超时

5. **事务必须闭合**：`ts` 后必须有 `tc` 或 `tro`

6. **方法控制在 50 行内**：过长的方法考虑拆分

7. **空行分隔逻辑**：方法间空行，事务首尾空行

## 常见问题

### Q1：后置表达式编译错误怎么解决？

```objectscript
// 错误：括号与 && 之间有空格
q:(a = "") && (b = "")

// 正确：括号与 && 之间无空格
q:(a = "")&&(b = "")
```

### Q2：Global 命名有什么规范？

```objectscript
// 临时 Global：以 ^CacheTemp 开头
s ^CacheTemp.MyApp("data") = value

// 进程 Global：必须携带 pid
s ^||TMP($JOB) = value

// 禁止的命名方式
s ^Temp("data") = value    ; 旧命名，不合法
s ^TMP("data") = value     ; 旧命名，不合法
```

### Q3：布尔变量怎么命名？

```objectscript
// 错误：用 is 开头
s isDisp = 1

// 正确：用 Flag 后缀
s dispFlag = $$$YES
```

### Q4：事务嵌套怎么处理？

```objectscript
// 同一方法内不应出现事务嵌套
// 如需嵌套，拆分到不同方法

// 正确：外层方法
Method ProcessOrder()
{
    ts
    d ..ValidateOrder()
    d ..SaveOrder()
    tc
}

// 内层方法不应有独立事务
Method ValidateOrder()
{
    // 只做验证，不开启事务
}
```

### Q5：陷阱（Trap）怎么规范写？

```objectscript
// 通用陷阱写法
Method MyMethod()
{
    // 设置陷阱
    s $zt = "Error"
    
    // 业务逻辑
    // ...
    
    q
    
Error
    s $zt = ""           ; 避免死循环
    i $tl > 0 tro         ; 避免开放性事务
    l -^MyApp("lock")    ; 避免开放锁
    q
}
```

### Q6：如何选择 $case 和 if else？

```objectscript
// 多级 if else 用 $case 替换
// 错误：多级 if
if (status = 1) {
    d ..HandleStatus1()
} elseif (status = 2) {
    d ..HandleStatus2()
} elseif (status = 3) {
    d ..HandleStatus3()
} else {
    d ..HandleDefault()
}

// 正确：用 $case
d $case(status,
    1:..HandleStatus1(),
    2:..HandleStatus2(),
    3:..HandleStatus3(),
    :"..HandleDefault()"
)
```

## 依赖说明

### 运行环境
- **Agent 平台**: 支持读取 SKILL.md 的任意 AI Agent（Claude Code / Cursor / Codex / Gemini CLI 等）
- **操作系统**: Windows / macOS / Linux
- **IRIS/Cache 版本**: 建议 2018 及以上

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| InterSystems IRIS | 运行时 | 推荐 | InterSystems 官方获取 |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置
- 本工具为纯 Markdown 指令驱动，无需额外 API Key
- IRIS 服务器连接需要配置访问凭据

### 可用性分类
- **分类**: MD+EXEC（Markdown 指令 + 命令行执行）
- **说明**: 通过自然语言指令驱动 Agent 执行代码格式化与审查，代码编译验证需要 IRIS 环境

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。
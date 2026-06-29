# Workflow YAML Format Specification v1.0

## 概述
工作流定义文件描述一个多步骤任务的执行流程，支持DAG依赖、并行执行、暂停恢复。

## 完整格式

```yaml
# 工作流元信息
name: my-workflow                    # 工作流名称（唯一标识）
version: "1.0"                       # 版本号
description: "做什么用的工作流"       # 描述
author: 绪哥                         # 作者
tags: [news, daily, wechat]          # 标签

# 触发条件（可选）
trigger:
  type: manual | cron | event        # 触发类型
  schedule: "0 8 * * *"             # cron表达式（type=cron时）
  event: "user_message"             # 事件类型（type=event时）

# 资源预算（可选）
resources:
  max_tokens: 50000                  # 最大token消耗
  max_time: 300                      # 最大执行时间（秒）
  max_api_calls: 20                  # 最大API调用次数

# 输入参数定义（可选）
inputs:
  - name: topic
    type: string
    required: true
    description: "工作流主题"
  - name: output_dir
    type: string
    default: "~/.hermes/output"

# 步骤定义（核心）
steps:
  - id: search                       # 步骤唯一ID
    name: "搜索新闻"                  # 步骤名称
    type: skill | terminal | subagent | user_input | llm  # 步骤类型
    depends: []                      # 依赖的步骤ID列表（DAG边）
    parallel: true                   # 是否可与同级步骤并行
    
    # 执行配置（根据type不同）
    config:
      # type=skill 时
      skill_name: "web-tools-guide"  # 技能名称
      prompt: "搜索{{topic}}的最新新闻"  # 提示词（支持模板变量）
      
      # type=terminal 时
      command: "python3 script.py"   # shell命令
      
      # type=subagent 时
      goal: "分析数据并生成报告"      # 子agent目标
      toolsets: ["web", "file"]      # 可用工具集
      
      # type=user_input 时
      prompt: "绪哥，内容没问题就继续"  # 用户提示
      
      # type=llm 时
      prompt: "分析以下内容并总结"    # LLM提示词
      model: "auto"                  # 模型选择
    
    # 输出配置
    output:
      type: file | text | json       # 输出类型
      path: "{{output_dir}}/news.json"  # 输出路径（file类型）
      variable: "news_list"          # 存储到工作流变量
    
    # 重试配置（可选）
    retry:
      max_attempts: 3                # 最大重试次数
      backoff: 2                     # 退避倍数
    
    # 超时配置（可选）
    timeout: 60                      # 步骤超时（秒）
    
    # 条件执行（可选）
    condition: "{{step1.output}} != null"  # 条件表达式

# 输出定义（可选）
outputs:
  - name: report
    type: file
    path: "{{output_dir}}/report.md"
  - name: summary
    type: text
    value: "工作流执行完成，共{{steps_count}}步"

# 错误处理（可选）
error_handling:
  on_step_fail: pause | skip | abort  # 步骤失败时行为
  notify: true                        # 是否通知用户
  fallback:                           # 备选步骤
    - step_id: alt_search
      when: "search failed"
```

## 步骤类型说明

| type | 说明 | config关键字段 |
|------|------|---------------|
| skill | 调用已有技能 | skill_name, prompt |
| terminal | 执行shell命令 | command |
| subagent | 派遣子agent | goal, toolsets |
| user_input | 暂停等用户输入 | prompt |
| llm | 直接调用LLM | prompt, model |

## 模板变量

支持在prompt、command、path中使用模板变量：
- `{{input.xxx}}` — 引用输入参数
- `{{step_id.output}}` — 引用其他步骤输出
- `{{step_id.status}}` — 引用其他步骤状态
- `{{env.xxx}}` — 引用环境变量

## 依赖关系

`depends`字段定义DAG边：
- `depends: []` — 无依赖，可立即执行
- `depends: [search]` — 依赖search步骤完成
- `depends: [search, analysis]` — 依赖search和analysis都完成

## 并行执行

当多个步骤的依赖都满足时，自动并行执行。
可通过`parallel: false`强制串行。

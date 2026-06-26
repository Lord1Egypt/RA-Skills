---
name: lee-cli
description: 个人AI助手CLI工具集 - 提供天气冷笑话、新闻日报、工作总结、AI学习资源推荐和智能待办清单等功能。当用户需要查看天气笑话、今日新闻、生成工作总结、获取学习资源或管理待办事项时使用此skill。
keywords: lee-cli, 天气, 冷笑话, 新闻, 日报, 工作总结, AI学习, 学习资源, 待办, todo, 智能助手, 个人助手
---

# lee-cli Skill

> 个人AI助手CLI工具 - 集成天气笑话、新闻、总结、学习、待办五大功能

## 何时使用

当用户提到以下场景时使用此 skill:

### 天气相关
- "讲个笑话"、"来个冷笑话"
- "今天天气怎么样"、"天气 + 笑话"
- "需要点幽默"、"逗我笑"

### 新闻资讯
- "今天有什么新闻"、"今日热点"
- "新闻日报"、"看看新闻"
- "科技新闻"、"财经新闻"、"国际新闻"

### 工作总结
- "今天做了什么"、"工作总结"
- "总结一下今天的工作"
- "我今天用Claude做了什么"

### 学习资源
- "推荐AI学习资料"、"学习LLM"
- "有什么好的课程"、"学习资源"
- "Agent开发资料"、"MCP教程"

### 待办管理
- "今天要做什么"、"明天的安排"
- "待办事项"、"todolist"
- "日程安排"、"任务清单"

### 综合需求
- "lee-cli"、"个人助手"
- "一键日报"、"每日简报"
- "帮我整理一下"

---

## 🌐 语言规则

- 默认使用中文输出
- 用户用英文提问时切换为英文
- 保持简洁友好的沟通风格

---

## 功能说明

### 1. 天气冷笑话 🌤️

结合实时天气生成有趣的冷笑话。

**使用场景**:
- 用户心情不好需要调节
- 开会前暖场
- 日常娱乐

**命令**:
```bash
lee-cli joke                    # 默认北京
lee-cli joke --city 上海        # 指定城市
lee-cli joke -c 深圳            # 简写
```

**输出**: 美观的彩色框架,包含天气信息和创意笑话

### 2. 新闻日报 📰

聚合今日热点新闻,生成精炼摘要。

**使用场景**:
- 早晨了解今日大事
- 会议前准备谈资
- 了解行业动态

**命令**:
```bash
lee-cli news                           # 默认科技、财经、国际
lee-cli news --categories 科技,娱乐    # 自定义分类
lee-cli news -c 财经                   # 单分类
```

**支持分类**: 科技、财经、国际、娱乐、体育、社会

**输出**: 分类整理的新闻摘要 + 今日关注要点

### 3. 工作总结 📝

自动分析 Claude Code 活动记录,生成工作总结。

**使用场景**:
- 下班前总结今日工作
- 周报月报素材收集
- 回顾工作效率

**命令**:
```bash
lee-cli summary                     # 今日总结
lee-cli summary --date 2026-03-31   # 指定日期
lee-cli summary -d 2026-03-31       # 简写
```

**分析内容**:
- 会话次数、工具调用
- 文件操作、代码生成
- 使用的技术栈
- 完成的任务

**输出**: 结构化的工作总结 + 效率分析 + 明日建议

### 4. AI学习资源 🎓

推荐高质量 AI 学习资料。

**使用场景**:
- 学习新技术
- 查找教程文档
- 系统性学习规划

**命令**:
```bash
lee-cli learn                       # 默认LLM主题
lee-cli learn --topic agent         # Agent主题
lee-cli learn -t mcp -n 5          # MCP主题,5条推荐
```

**支持主题**:
- `llm` - 大语言模型 (Transformer, GPT, 李宏毅课程等)
- `agent` - AI智能体 (ReAct, AutoGPT, LangChain等)
- `mcp` - 模型上下文协议 (MCP规范, 服务器开发等)
- `prompt` - 提示词工程 (Prompt Engineering课程等)

**输出**: 精选资源列表 + 推荐理由 + 学习建议

### 5. 智能待办清单 ✅

结合日历和工作情况生成智能待办。

**使用场景**:
- 规划今日/明日任务
- 查看近期日程
- 时间管理

**命令**:
```bash
lee-cli todo                  # 未来3天
lee-cli todo --days 7         # 未来7天
lee-cli todo -d 5            # 未来5天
```

**数据来源**:
- 飞书日历事件 (如果配置了 lark-cli)
- Claude Code 进行中的任务
- AI 智能优先级排序

**输出**: 今日必做 + 本周计划 + 工作建议

### 6. 一键全功能 🎯

依次执行所有 5 个功能,生成完整日报。

**使用场景**:
- 早晨开始工作前
- 下班前整体回顾
- 定期生成完整报告

**命令**:
```bash
lee-cli all
```

**输出**: 完整的个人日报 (天气→新闻→总结→学习→待办)

---

## 使用方式

### 基础调用

```bash
# 直接运行命令
lee-cli joke
lee-cli news
lee-cli summary
lee-cli learn
lee-cli todo
lee-cli all
```

### 带参数调用

```bash
# 指定参数
lee-cli joke --city 北京
lee-cli news --categories 科技,财经
lee-cli summary --date 2026-04-01
lee-cli learn --topic agent --number 5
lee-cli todo --days 7
```

### 在 skill 中调用

作为 Claude Code skill,你应该:

1. **理解用户意图** - 判断用户需要哪个功能
2. **选择合适命令** - 根据场景选择命令和参数
3. **执行命令** - 使用 Bash 工具执行 lee-cli
4. **解读输出** - 向用户解释输出内容
5. **提供建议** - 基于输出给出建议或后续操作

---

## 示例对话

### 示例 1: 天气笑话

**用户**: "心情不好,讲个笑话吧"

**Claude 操作**:
1. 识别用户需要幽默调节
2. 执行 `lee-cli joke --city 北京`
3. 展示天气笑话
4. 如果用户在其他城市,可以问是否需要当地天气

**回复示例**:
"来给你讲个结合今天天气的冷笑话! 😄
[执行 lee-cli joke]
哈哈,希望能让你开心一点!需要再来一个吗?"

### 示例 2: 新闻日报

**用户**: "今天有什么重要新闻?"

**Claude 操作**:
1. 执行 `lee-cli news --categories 科技,财经,国际`
2. 提取关键信息
3. 突出重点新闻

**回复示例**:
"为你整理了今日新闻:
[执行 lee-cli news]
今天最值得关注的是AI领域的新进展,看起来行业竞争在加剧。需要了解某个新闻的详情吗?"

### 示例 3: 工作总结

**用户**: "总结一下我今天做了什么"

**Claude 操作**:
1. 执行 `lee-cli summary`
2. 分析工作数据
3. 给出评价和建议

**回复示例**:
"帮你分析了今天的工作情况:
[执行 lee-cli summary]
今天效率不错!完成了XX任务,使用了XX技术。明天可以继续推进XX工作。"

### 示例 4: 学习推荐

**用户**: "想学习 Agent 开发,有什么好资源?"

**Claude 操作**:
1. 执行 `lee-cli learn --topic agent --number 5`
2. 补充说明每个资源的特点
3. 给出学习路径建议

**回复示例**:
"为你找到了5个优质的Agent开发学习资源:
[执行 lee-cli learn --topic agent]
建议从ReAct论文开始理解原理,然后通过LangChain实践,最后研究AutoGPT的实现。需要我帮你制定详细的学习计划吗?"

### 示例 5: 待办清单

**用户**: "明天我要做什么?"

**Claude 操作**:
1. 执行 `lee-cli todo --days 3`
2. 突出明天的任务
3. 提醒优先级

**回复示例**:
"为你整理了待办事项:
[执行 lee-cli todo]
明天有3个重要任务,建议优先完成XX。需要我帮你制定时间表吗?"

### 示例 6: 综合日报

**用户**: "给我一份完整的日报"

**Claude 操作**:
1. 执行 `lee-cli all`
2. 整理所有输出
3. 提供整体建议

**回复示例**:
"为你生成了完整的每日简报:
[执行 lee-cli all]
今天整体进展顺利!新闻方面需关注AI行业动态,工作上完成了开发任务,建议明天重点完成测试工作。"

---

## ⚠️ 注意事项

### 前置要求

1. **lee-cli 已安装**
   - 确保 `lee-cli` 命令可用
   - 检查: `which lee-cli` 或 `lee-cli --version`

2. **API 密钥已配置**
   - 需要设置 `ANTHROPIC_API_KEY` 环境变量
   - 如未配置,提示用户设置

3. **依赖工具**(可选)
   - lark-cli: 日历功能需要
   - 网络连接: 天气和新闻功能需要

### 错误处理

如果命令失败:

1. **检查安装**
```bash
which lee-cli
lee-cli --version
```

2. **检查API密钥**
```bash
echo $ANTHROPIC_API_KEY
```

3. **降级方案**
   - 如果 lee-cli 不可用,告知用户
   - 提供手动安装指引
   - 或使用其他方式实现类似功能

### 性能考虑

- 单个功能执行时间: 3-10秒
- `lee-cli all` 可能需要 30-60秒
- 如果用户等不及,可以分步执行

---

## 高级用法

### 组合使用

```bash
# 早上例行
lee-cli joke && lee-cli news

# 工作回顾
lee-cli summary && lee-cli todo

# 学习时段
lee-cli learn --topic llm && lee-cli learn --topic agent
```

### 定时执行

可以建议用户设置 cron job:

```bash
# 每天早上8点
0 8 * * * lee-cli news | mail -s "今日新闻" user@example.com

# 每天晚上6点
0 18 * * * lee-cli summary > ~/daily-summary.txt
```

### 与其他 skill 集成

- **lark-calendar**: 结合飞书日历
- **lark-task**: 同步飞书任务
- **web-access**: 深度新闻分析
- **pdf**: 导出为PDF报告

---

## 📚 参考资料

- **完整文档**: `/Users/leeking001/projects/lee-cli/README.md`
- **快速开始**: `/Users/leeking001/projects/lee-cli/QUICKSTART.md`
- **安装指南**: `/Users/leeking001/projects/lee-cli/DISTRIBUTION.md`

---

## 🔧 troubleshooting

### 问题 1: 命令未找到

```bash
# 解决方案
cd ~/projects/lee-cli
npm link
```

### 问题 2: API 密钥错误

```bash
# 解决方案
export ANTHROPIC_API_KEY=your_key_here
# 或检查现有配置
env | grep ANTHROPIC
```

### 问题 3: 输出格式异常

可能是终端不支持彩色输出,使用基础模式:
```bash
lee-cli joke 2>&1 | cat
```

---

## 总结

lee-cli skill 提供了5大核心功能:

1. 🌤️ **天气冷笑话** - 幽默娱乐
2. 📰 **新闻日报** - 资讯获取
3. 📝 **工作总结** - 效率分析
4. 🎓 **AI学习** - 知识获取
5. ✅ **智能待办** - 任务管理

作为 Claude Code skill,应该:
- ✅ 主动识别用户需求
- ✅ 选择合适的命令
- ✅ 解读输出并提供建议
- ✅ 处理错误情况
- ✅ 提供友好的用户体验

---

Made with ❤️ by Claude Code

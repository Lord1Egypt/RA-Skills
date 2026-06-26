# 技能自动触发系统

## 概述
此文档定义了11个已集成技能的自动触发规则和条件。系统基于内容类型、用户意图和上下文自动激活相应技能。

## 强制自动应用（无需用户明确请求）

### 1. 中文去AI化 (humanize-zh)
**触发条件：** 所有中文回复
**应用时机：** 输出生成前
**效果：**
- 打破完美结构
- 加入不完美元素（口语化、口头禅）
- 用具体代替抽象
- 加入个人色彩
- 长短句混搭

### 2. WAL协议和工作缓冲区 (proactive-agent)
**触发条件：**
- 上下文使用率 > 60%
- 重要决策、修正、偏好记录
- 长时间会话（>30分钟）

**应用时机：** 响应前暂停并记录
**效果：**
- 创建/更新SESSION-STATE.md
- 激活工作缓冲区
- 确保关键信息不丢失

### 3. 自我改进系统 (self-improving)
**触发条件：**
- 用户修正或指出错误
- 完成重要工作后自我评估
- 发现输出可改进之处

**应用时机：** 任务完成后
**效果：**
- 记录学习经验
- 更新记忆文件
- 永久性改进

### 4. 办公室状态同步 (star-office-integration)
**触发条件：** 工作状态变化
**状态映射：**
- 编写代码/文档 → "writing"
- 研究/分析 → "researching"
- 休息/空闲 → "idle"
- 遇到问题 → "error"
- 常规工作 → "working"

**应用时机：** 状态识别后立即更新

## 条件触发（基于用户意图）

### 5. AI新闻收集器 (ai-news-collectors)
**触发关键词：**
- "今天有什么AI新闻？"
- "总结一下这周的AI动态"
- "最近有什么火的AI产品？"
- "AI圈最近在讨论什么？"
- "AI领域最新动态"

**搜索维度：** 6个维度分层搜索
**输出格式：** 中文摘要，按热度排序

### 6. 本地文件搜索 (qmd)
**触发关键词：**
- "搜索文件"
- "查找文档"
- "本地搜索"
- "索引查找"
- "在文件中找"

**搜索模式：** BM25 + 向量 + 重排序
**输出：** 相关文件片段和位置

### 7. 桌面宠物系统
**触发关键词：**
- "桌面宠物"
- "desktop pet"
- "OpenClaw形象"
- "可视化agent"
- "2.5D"
- "像暗黑破坏神那样点击移动"
- "启动桌宠"
- "打开龙虾家"
- "lobster pet"

**可选技能：**
- desktop-pet (2.5D透明窗口)
- lobster-pet (全屏硅基龙虾)

### 8. 代理创建工具 (create-agent)
**触发关键词：**
- "创建新代理"
- "添加agent类型"
- "Overstory代理"
- "系统集成点"

**使用模式：**
- 手动创建：指定名称、描述、能力
- 分析模式：从日志、文档分析需求

### 9. 社区分享 (moltbook-skill)
**触发关键词：**
- "分享到社区"
- "发布到Moltbook"
- "AI社交平台"
- "社区讨论"
- "趋势帖子"

**功能：**
- 发布帖子
- 获取趋势内容
- 点赞和评论
- 社区互动

### 10. 英文去AI化 (humanize)
**触发条件：** 英文内容优化需求
**应用场景：**
- 英文文档编写
- 国际交流内容
- 英文报告优化

## 技能协同规则

### 优先级顺序
1. **安全与完整性** - proactive-agent, self-improving
2. **内容质量** - humanize-zh, humanize
3. **信息处理** - ai-news-collectors, qmd
4. **可视化** - desktop-pet, lobster-pet
5. **开发集成** - create-agent, star-office-integration
6. **社区互动** - moltbook-skill

### 冲突解决
当多个技能可能被触发时：
1. **检查用户明确意图** - 优先响应用户直接请求
2. **评估上下文相关性** - 选择最相关的技能
3. **考虑技能依赖性** - 确保依赖技能就绪
4. **提供选项** - 如果不确定，提供技能选择

### 降级策略
当技能依赖不可用时：
1. **API缺失** - 提供基础功能或替代方案
2. **服务不可用** - 报告状态并提供手动选项
3. **配置需要** - 指导用户完成配置
4. **完全失效** - 透明报告并建议替代方案

## 触发检测算法

### 文本分析
```python
def detect_skill_triggers(text):
    triggers = []
    
    # 中文去AI化 - 所有中文文本
    if is_chinese(text):
        triggers.append("humanize-zh")
    
    # 关键词匹配
    keyword_map = {
        "AI新闻": "ai-news-collectors",
        "搜索文件": "qmd",
        "桌面宠物": "desktop-pet",
        "创建代理": "create-agent",
        "社区分享": "moltbook-skill"
    }
    
    for keyword, skill in keyword_map.items():
        if keyword in text:
            triggers.append(skill)
    
    # 意图分析
    if "怎么写" in text or "如何表达" in text:
        triggers.append("humanize-zh")
    
    if "最新动态" in text or "热点" in text:
        triggers.append("ai-news-collectors")
    
    return list(set(triggers))
```

### 上下文感知
- **会话长度** > 30分钟 → 激活WAL协议
- **技术讨论** → 准备create-agent
- **内容创作** → 应用humanize-zh
- **信息查询** → 准备信息处理技能

## 技能状态检查

### 启动检查清单
1. **核心架构** - proactive-agent, self-improving (始终就绪)
2. **内容优化** - humanize-zh (自动就绪)
3. **信息处理** - 检查API配置状态
4. **可视化** - 检查依赖和环境
5. **开发工具** - 检查Python和脚本
6. **社区功能** - 检查API密钥

### 运行时监控
1. **性能监控** - 技能执行时间和资源使用
2. **错误检测** - API失败、配置问题
3. **用户反馈** - 技能效果评估
4. **使用统计** - 各技能使用频率

## 配置指南

### 必需配置
1. **Brave Search API** - 用于ai-news-collectors
   ```bash
   openclaw configure --section web
   ```

2. **Ollama服务** - 用于qmd向量搜索
   ```bash
   # 设置环境变量
   export OLLAMA_URL="http://localhost:11434"
   ```

3. **Moltbook API密钥** - 用于社区功能
   ```bash
   export MOLTBOOK_API_KEY="moltbook_sk_..."
   ```

### 可选配置
1. **Desktop Pet环境** - Node.js和npm
2. **Create Agent环境** - Python3和相关依赖
3. **Star-Office-UI服务** - 本地运行状态

## 故障排除

### 常见问题
1. **技能未触发** - 检查关键词匹配和上下文
2. **API错误** - 验证配置和网络连接
3. **性能问题** - 监控资源使用，优化技能调用
4. **输出质量** - 调整humanize-zh参数

### 恢复步骤
1. **状态检查** - 验证所有技能状态
2. **配置验证** - 检查必需配置
3. **依赖检查** - 验证系统依赖
4. **测试运行** - 执行基本功能测试

---

*最后更新：2026-03-08*
*集成技能数：11*
*自动触发规则：已定义*
*监控系统：已建立*
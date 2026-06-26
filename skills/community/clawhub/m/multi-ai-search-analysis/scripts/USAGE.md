# 自动化脚本使用说明

**版本**：v1.3  
**最后更新**：2026-03-17

---

## ⚠️ 重要：会话管理（必读）

**每次分析前，自动化脚本会自动新建会话，确保上下文干净！**

### 为什么需要干净的上下文

- ✅ **避免历史对话污染**：之前的对话会影响 AI 回答质量
- ✅ **确保独立分析**：每次分析都从零开始
- ✅ **提高响应速度**：减少 AI 处理负担
- ✅ **便于结果对比**：所有 AI 在相同起始状态下回答

### 自动化处理

`run.py` 脚本会自动：
1. 检测页面是否有历史对话
2. 点击"新建会话"按钮
3. 确认空白对话状态
4. 发送分析问题

**无需手动操作！**

---

## 📦 快速开始（3 分钟）

### 步骤 1：安装（1 分钟）

```bash
cd skills/multi-ai-search-analysis
python scripts/install.py
```

### 步骤 2：测试（1 分钟）

```bash
python scripts/test.py
```

### 步骤 3：登录（1 分钟）

```bash
python scripts/login.py
```

### 步骤 4：运行分析（3-5 分钟）

```bash
python scripts/run.py -t "你的分析主题"
```

---

## 🎯 脚本说明

### 1. install.py - 安装脚本

**功能**：一键安装所有依赖

**用法**：
```bash
python scripts/install.py
```

**执行内容**：
- 检查 Python 版本（需要 3.8+）
- 升级 pip
- 安装 Python 依赖（playwright, colorama 等）
- 安装 Edge 浏览器
- 创建必要目录（reports/, logs/, browser-profile/）
- 验证安装

---

### 2. test.py - 测试脚本

**功能**：快速验证安装和基本功能

**用法**：
```bash
python scripts/test.py
```

**测试项目**：
- ✓ 浏览器初始化
- ✓ 配置文件加载
- ✓ 报告生成器

**预期输出**：
```
========================================
  Multi-AI Search Analysis - 安装测试
========================================

[测试 1/3] 浏览器初始化...
✓ 浏览器初始化成功
✓ 页面加载成功
✓ 浏览器已关闭

[测试 2/3] 配置文件加载...
✓ 配置文件加载成功
  已配置平台：4
    - DeepSeek: https://chat.deepseek.com
    - Qwen: https://chat.qwen.ai
    - 豆包：https://www.doubao.com
    - Kimi: https://kimi.moonshot.cn

[测试 3/3] 报告生成器...
✓ 报告生成成功

========================================
  测试结果汇总
========================================

✓ 浏览器
✓ 配置文件
✓ 报告生成器

总计：3/3 通过

🎉 所有测试通过！可以开始使用了
```

---

### 3. login.py - 登录工具

**功能**：打开所有 AI 平台供用户手动登录

**用法**：
```bash
python scripts/login.py
```

**执行流程**：
1. 打开 Edge 浏览器
2. 为每个平台打开一个标签页
3. 用户手动完成登录
4. 保存登录状态到 `browser-profile/`

**登录方式**：
| 平台 | 登录方式 |
|------|---------|
| DeepSeek | 微信扫码/手机号 |
| Qwen | GitHub/Google/Apple |
| 豆包 | 手机号 + 验证码 |
| Kimi | 手机号 + 验证码 |
| Gemini | Google 账号（需要网络环境支持） |

**提示**：登录状态会持久化，只需首次登录。

---

### 4. run.py - 主执行脚本

**功能**：并行询问多家 AI，生成综合分析报告

**基本用法**：
```bash
python scripts/run.py -t "分析主题"
```

**完整参数**：
```bash
python scripts/run.py \
  -t "主题" \                      # 分析主题（必填）
  -p DeepSeek Qwen Kimi \          # 指定 AI 平台（可选）
  -d 维度 1 维度 2 \                # 分析维度（可选）
  --timeout 180 \                  # 超时时间（秒，默认 120）
  --mode parallel \                # 执行模式：parallel/serial
  -o "输出路径.md" \               # 输出文件路径（可选）
  --follow-up "问题 1" "问题 2"    # 延伸问题（可选）
```

**执行流程**：
1. 初始化浏览器（使用 Edge）
2. 并行打开多个标签页
3. 检查登录状态
4. 同时发送问题
5. 等待所有响应
6. 提取回复内容
7. 生成综合报告
8. 保存报告到 `reports/`

**输出示例**：
```
========================================
  Multi-AI Search Analysis v1.2
  模式：并行
========================================

分析主题：2026 年 AI 市场趋势
分析维度：技术，投资，应用，竞争
AI 平台：DeepSeek, Qwen, 豆包，Kimi
超时时间：120 秒

正在初始化浏览器...
✓ 浏览器初始化完成

正在并行询问 4 家 AI...

========================================
  [DeepSeek] 开始查询
========================================
✓ [DeepSeek] 已登录
✓ [DeepSeek] 问题已发送
⏳ [DeepSeek] 等待响应（最多 120 秒）...
✓ [DeepSeek] 响应已完成
✓ [DeepSeek] 内容已提取（3542 字）

...（其他平台类似）

✓ 报告已保存：reports/2026 年 AI 市场趋势 -2026-03-16-2355.md

========================================
  完成！成功：4/4
========================================
```

---

## 📊 报告生成

### 报告位置

```
reports/
└── {主题}-{日期}-{时间}.md
```

### 报告结构

```markdown
# {主题} - 综合分析报告

**生成时间**：{时间}  
**AI 平台**：{平台列表}  
**分析维度**：{维度列表}

---

## 执行摘要

[核心结论]

## 各 AI 回复原文

### DeepSeek
[完整回复]

### Qwen
[完整回复]

...

## 数据对比表

| 维度 | DeepSeek | Qwen | ... | 共识 |
|------|----------|------|-----|------|
| - | - | - | ... | - |

## 各家特色

- **DeepSeek**: [特色]
- **Qwen**: [特色]
...
```

---

## 🔧 配置说明

### 配置文件：config/ai-platforms.json

```json
{
  "platforms": [
    {
      "name": "DeepSeek",
      "url": "https://chat.deepseek.com",
      "timeout": 120,
      "selectors": {
        "input": "textarea[placeholder*='输入']",
        "send": "button[aria-label*='发送']",
        "response": "div.markdown-body"
      }
    }
  ],
  "defaultDimensions": [],
  "defaultTimeout": 120,
  "templates": {
    "general": "请帮我分析一下{topic}，包括{dimensions}等方面的情况。",
    "comparison": "请详细对比{topic}，从{dimensions}等角度进行全面分析。",
    "trend": "请分析{topic}的发展趋势，包括{dimensions}等关键因素。",
    "evaluation": "请评估{topic}，从{dimensions}维度给出详细评价和建议。"
  }
}
```

### 修改超时时间

编辑 `config/ai-platforms.json`：
```json
{
  "platforms": [
    {
      "name": "豆包",
      "timeout": 180  // 增加超时时间
    }
  ]
}
```

### 添加新 AI 平台

```json
{
  "platforms": [
    {
      "name": "Claude",
      "url": "https://claude.ai",
      "loginMethod": "email",
      "timeout": 120,
      "selectors": {
        "input": "textarea",
        "send": "button.send",
        "response": ".message"
      }
    }
  ]
}
```

---

## ❓ 故障排查

### 问题 1：依赖安装失败

```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 2：浏览器无法打开

```bash
# 重新安装 Edge 浏览器
playwright install msedge

# 检查 Edge 是否安装
edge --version
```

### 问题 3：登录状态丢失

```bash
# 清除缓存重新登录
rm -rf browser-profile
python scripts/login.py
```

### 问题 4：超时错误

```bash
# 增加超时时间
python scripts/run.py -t "主题" --timeout 180

# 或修改配置文件
# config/ai-platforms.json -> platforms[].timeout
```

### 问题 5：元素选择器失效

平台更新 UI 后，需要更新选择器配置：

```json
{
  "platforms": [
    {
      "name": "Qwen",
      "selectors": {
        "input": "#chat-input",  // 更新选择器
        "send": "#send-button",
        "response": ".response-content"
      }
    }
  ]
}
```

---

## 🎯 最佳实践

### 1. 选择合适的时间

- ✅ 网络空闲时段（深夜/清晨）
- ❌ 避免高峰期（工作日 9-11 点、14-16 点）

### 2. 提前检查登录

```bash
# 运行前检查
python scripts/login.py
```

### 3. 合理设置超时

| 场景 | 推荐超时 |
|------|---------|
| 简单问题 | 60 秒 |
| 中等分析 | 120 秒 |
| 复杂研究 | 180-300 秒 |

### 4. 保存重要报告

```bash
# 备份到云盘
cp reports/*.md ~/OneDrive/Reports/
```

### 5. 使用并行模式

除非遇到验证码，否则优先使用并行模式，节省 60-75% 时间。

---

## 📚 相关文档

- [SKILL.md](../SKILL.md) - 技能详细说明
- [QUICKSTART.md](../QUICKSTART.md) - 3 分钟上手指南
- [GENERALITY_GUIDE.md](../GENERALITY_GUIDE.md) - 通用性说明
- [README_PYTHON.md](./README_PYTHON.md) - Python 版使用说明

---

## 💡 反馈与改进

遇到问题或有改进建议？

1. 查看 `logs/` 目录日志
2. 检查 `QUICKSTART.md` 故障排查
3. 更新到最新版本
4. 提交 Issue

---

## 📝 版本历史

- **v1.4**（2026-03-17）：增加 Gemini 平台支持
  - 添加 Gemini 平台配置
  - 更新登录方式说明
  - 更新平台选择建议
- **v1.3**（2026-03-17）：添加会话管理说明
  - 新增"重要：会话管理"章节
  - 说明自动化脚本如何处理会话
  - 解释为什么需要干净的上下文
- **v1.2**（2026-03-16）：初始版本

---

*维护者：小呱 🐸*  
*版本：v1.4*  
*更新时间：2026-03-17*

# Hermes 平台适配指南

## 一、安装方式

### 方式A：自动安装（推荐）

```bash
# 1. 将技能目录克隆到 Hermes skills 目录
git clone <repo-url> ~/.hermes/skills/bid-document-maker

# 2. 注册函数定义
hermes functions register ~/.hermes/skills/bid-document-maker/agents/hermes/functions.json

# 3. 验证安装
hermes skill info bid-document-maker

# 4. 一键使用
hermes run bid-document-maker --input tender_file=/path/to/tender.pdf
```

### 方式B：手动配置

将 `functions.json` 内容复制到 Hermes 函数配置中：

```bash
# 1. 加载函数定义
hermes config set functions.file agents/hermes/functions.json

# 2. 设置系统提示词
hermes config set system_prompt.file prompts/system-prompt.md

# 3. 开始对话
hermes chat --load-skill bid-document-maker
```

### 方式C：纯 Prompt 模式（无 Function Calling）

如果 Hermes 实例不支持 Function Calling，直接使用通用模式：

```bash
# 注入系统提示词
hermes chat --system "$(cat prompts/system-prompt.md)"

# 然后按 5 阶段手动执行
```

## 二、自动安装验证

安装成功后运行测试：

```bash
# 验证函数列表
hermes functions list | grep bid-document-maker
# 预期输出: parse_tender_document, generate_strategy_report, generate_bid_outline, write_chapter, quality_check, pdca_improve, assemble_bid_document

# 验证状态管理
hermes skill status bid-document-maker
# 预期输出: Skill bid-document-maker v1.0.0 — 7 functions registered, status: ready
```

## 三、核心文件

| 文件 | 用途 | 必需 |
|------|------|------|
| `agents/hermes/functions.json` | Function Calling 定义（可直接 `hermes functions register` 导入） | ✅ |
| `prompts/system-prompt.md` | 系统角色提示词 | ✅ |
| `prompts/01-parse-tender.md` | 阶段1：解析提示词 | ✅ |
| `prompts/02-strategy-and-outline.md` | 阶段2-3：策略+大纲提示词 | ✅ |
| `prompts/03-write-section.md` | 阶段4：写作提示词 | ✅ |
| `prompts/04-quality-check.md` | 阶段5：质检提示词 | ✅ |
| `templates/chapter-templates.md` | 各章节写作模板 | ✅ |
| `templates/format-rules.md` | 中国标书格式规范 | ✅ |
| `schemas/tender-info.schema.json` | 招标数据结构验证 | 可选 |

## 四、Function Calling 工作流映射

| Hermes 函数 | 对应阶段 | 调用时机 |
|-------------|---------|---------|
| `parse_tender_document` | 阶段1 | 用户提供文件路径后 |
| `generate_strategy_report` | 阶段2 | 解析完成后 |
| `generate_bid_outline` | 阶段3 | 策略分析完成后 |
| `write_chapter` | 阶段4 | 大纲确认后（可并行调用多次） |
| `quality_check` | 阶段5 | 所有章节完成后 |
| `pdca_improve` | 阶段6 | 质检完成后（自动执行3轮PDCA） |
| `assemble_bid_document` | 阶段6-输出 | PDCA完成后（用户无需介入） |

执行顺序：
```
parse → strategy → outline → write×N → quality → pdca(3轮) → assemble
         ↑            ↑                                   
     (等待确认)  (等待确认)          (PDCA自动执行，无需用户介入)
```

## 五、全程对话示例

```
用户: 使用 bid-document-maker，招标文件在 /data/项目A.pdf

Hermes 第1轮:
→ 调用 parse_tender_document(file_path="/data/项目A.pdf")
→ 输出结构化解析摘要
→ 等待用户确认

用户: 确认无误，继续

Hermes 第2轮:
→ 调用 generate_strategy_report(tender_info=...)
→ 调用 generate_bid_outline(tender_info=..., strategy_report=...)
→ 展示大纲（含评分标注）
→ 等待用户确认

用户: 大纲可以，开始写

Hermes 第3-7轮:
→ 逐章调用 write_chapter(chapter_id="technical_proposal", ...)
→ write_chapter(chapter_id="implementation", ...)
→ write_chapter(chapter_id="quality_assurance", ...)
→ write_chapter(chapter_id="after_sales", ...)
→ write_chapter(chapter_id="price_proposal", ...)

Hermes 第8轮:
→ 调用 quality_check(chapters=..., tender_info=...)
→ 输出质检报告
→ 自动触发第6阶段

Hermes 第9轮 (自动执行，无需用户介入):
→ 调用 pdca_improve(chapters=..., quality_report=..., tender_info=...)
→ 内部执行3轮PDCA：
   · PLAN: 分析质检报告，制定修复计划
   · DO: 逐项修复问题
   · CHECK: 验证修复效果
   · ACT: 判断是否进入下一轮
→ 输出改进报告

Hermes 第10轮:
→ 调用 assemble_bid_document(chapters=..., output_format="markdown")
→ 输出最终标书 + PDCA改进报告
→ 通知用户终审
```

## 六、状态管理

每次函数调用后更新以下状态：

```json
{
  "stage": "writing",           // 当前阶段
  "tender_info": { ... },       // 招标解析结果
  "strategy_report": { ... },   // 策略报告
  "outline": { ... },           // 大纲
  "chapters": {                 // 已完成章节
    "technical_proposal": "...",
    "implementation": "..."
  },
  "quality_report": null        // 尚未质检
}
```

## 七、常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `parse_tender_document` 返回空 | PDF为扫描件 | 使用OCR模式或先手动提取文本 |
| `write_chapter` 输出被截断 | 单章内容超过token限制 | 将章节拆分为多个 `write_chapter` 调用 |
| `quality_check` 报告遗漏 | 检查深度不够 | 设置 `check_level: "strict"` |

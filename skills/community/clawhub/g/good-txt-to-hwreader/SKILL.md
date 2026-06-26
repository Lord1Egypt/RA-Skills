---
name: good-txt-to-hwreader
description: 清理和修复盗版 txt 电子书中的乱码、广告和排版问题。支持 AI 增强模式，可智能识别非标准广告、修复复杂乱码、识别非标准章节格式。触发词：txt清理、电子书修复、去广告、修乱码、排版修复、清理txt、修复电子书、txt乱码、txt广告。
---

# Good Txt To Hwreader

将盗版 txt 电子书转换为干净、规范的阅读格式。

**✨ v4.0 新增 AI 增强功能**：智能广告识别、复杂乱码修复、非标准章节识别

## 触发关键词

用户可以通过以下方式触发此技能：

| 关键词 | 示例 |
|--------|------|
| txt清理 | `帮我清理这个txt文件` |
| 电子书修复 | `修复这本电子书` |
| 去广告 | `去掉txt里的广告` |
| 修乱码 | `修复txt乱码` |
| 排版修复 | `修复txt排版` |
| txt乱码 | `这个txt有乱码` |
| txt广告 | `txt里好多广告` |

## 处理模式

本技能支持三种处理模式，用户可根据需求选择：

| 模式 | 速度 | 准确率 | AI 功能 | 适用场景 |
|------|------|--------|---------|----------|
| **fast** | ⚡ 最快 | 85% | 全部关闭 | 快速预览、大批量处理 |
| **balanced** | 🔄 平衡 | 92% | 广告+乱码 | 日常使用（默认） |
| **thorough** | 🎯 最准 | 98% | 全部开启 | 重要文件、复杂乱码 |

**使用方式**：
```
清理这个txt文件（使用thorough模式）
用fast模式清理这本电子书
```

## 用户输入方式

### 方式一：直接指定文件路径

```
清理 /path/to/book.txt
修复电子书 ~/Downloads/novel.txt
```

### 方式二：模糊搜索手机 txt 文件

当用户说：
- `清理一本txt`（未指定具体文件）
- `帮我找个txt文件清理一下`
- `修复某个电子书`

**执行步骤**：
1. 使用 `search_file` 工具搜索用户设备上的 txt 文件
2. 列出匹配的文件供用户选择
3. 用户确认后执行清理

### 方式三：搜索关键词

```
清理包含"斗破"的txt
修复文件名有"修仙"的电子书
```

**执行步骤**：
1. 使用 `search_file` 工具按关键词搜索
2. 列出匹配结果
3. 用户选择后执行清理

## 依赖

- Python 3.6+
- chardet 库：`pip install chardet`
- PyYAML 库：`pip install pyyaml`（AI 增强模式）
- requests 库：`pip install requests`（AI 增强模式）

## 处理流程

### 阶段一：文件获取

1. 使用 `search_file` 搜索用户手机上的 txt 文件
2. 使用 `upload_file` 上传到云端获取 URL
3. 使用 `curl` 下载到工作目录

### 阶段二：清理修复

#### 规则引擎处理（所有模式）

1. **编码检测** — 自动识别 GBK/UTF-8/GB2312 等编码
2. **广告清理** — 匹配 40+ 种常见广告模式
3. **乱码修复** — 替换 30+ 种常见乱码字符
4. **排版规范化** — 统一章节标题、段落格式

#### AI 增强处理（balanced/thorough 模式）

1. **智能广告识别** — LLM 识别变体广告、软广、新平台广告
2. **复杂乱码修复** — LLM 根据上下文推断正确字符
3. **智能章节识别** — LLM 识别非标准章节格式（仅 thorough 模式）

### 阶段三：输出结果

1. **发送文件给用户** — 使用 `send_file_to_user` 发送清理后的文件
2. **输出修复报告** — 以简洁的 md 表格展示修复结果

## 输出报告

清理完成后，助手会解析脚本输出，生成简洁表格：

```markdown
# txt 清理报告

## 基本信息

| 项目 | 结果 |
|------|------|
| 原文长度 | 199,044 字符 |
| 清理后长度 | 198,702 字符 |
| 移除内容 | 342 字符 (0.17%) |
| 处理模式 | balanced |
| AI 增强 | 已启用 |

## 清理详情

| 项目 | 数量 |
|------|------|
| 广告清理 | 5 处 |
| 乱码修复 | 12 处 |
| 章节识别 | 50 个 |

## 性能统计

| 项目 | 数值 |
|------|------|
| 处理时间 | 2.35 秒 |
| LLM 调用次数 | 3 次 |
```

## Resources

### scripts/
- `clean_txt.py` — 规则引擎清理脚本
- `ai_enhanced_cleaner.py` — AI 增强清理脚本（主入口）
- `ai_modules/` — AI 增强模块
  - `ad_detector.py` — 广告识别模块
  - `mojibake_fixer.py` — 乱码修复模块
  - `chapter_parser.py` — 章节识别模块
- `utils/` — 工具模块
  - `llm_client.py` — LLM 客户端封装

### config/
- `ai_config.yaml` — AI 增强配置文件

### references/
- `ads_patterns.md` — 常见广告模式列表
- `mojibake_patterns.md` — 常见乱码映射表
- `learned_mojibake_rules.json` — 学习到的乱码规则（自动生成）

### assets/
- `chapter_template.txt` — 标准章节格式模板

## 完整示例

### 示例一：规则引擎模式（fast）

**用户**: 用fast模式清理三体txt文件

**执行流程**:

```
1. search_file(query="三体 txt")
   → 找到: /storage/.../三体.txt

2. upload_file(fileInfos=[{"mediaUri": "file://docs/..."}])
   → 获取公网URL

3. curl -o "三体.txt" "URL"
   → 下载到工作目录

4. python3 scripts/ai_enhanced_cleaner.py -m fast "三体.txt"
   → 生成: 三体_清理版.txt

5. send_file_to_user(fileLocalUrls=["三体_清理版.txt"])
   → 发送清理后的文件给用户
```

### 示例二：AI 增强模式（balanced）

**用户**: 清理这个txt文件，有乱码

**执行流程**:

```
1. search_file(query="txt")
   → 列出文件供用户选择

2. upload_file + curl
   → 下载文件

3. python3 scripts/ai_enhanced_cleaner.py -m balanced "book.txt"
   → 规则引擎预处理
   → AI 广告识别
   → AI 乱码修复
   → 规则引擎后处理
   → 生成: book_清理版.txt

4. send_file_to_user + 报告
```

### 示例三：深度清理模式（thorough）

**用户**: 用thorough模式清理这本小说，章节格式很乱

**执行流程**:

```
1. 获取文件

2. python3 scripts/ai_enhanced_cleaner.py -m thorough "novel.txt"
   → 规则引擎预处理
   → AI 广告识别
   → AI 乱码修复
   → AI 章节识别与规范化
   → 规则引擎后处理
   → 生成: novel_清理版.txt + novel_清理版_报告.md

3. 发送文件和报告
```

## AI 增强功能详解

### 1. 智能广告识别

| 功能 | 说明 |
|------|------|
| 变体广告 | 识别故意添加干扰字符的广告 |
| 软广 | 识别伪装成正文的推广内容 |
| 新平台广告 | 无需预定义规则即可识别 |
| 批量处理 | 10 个段落一批，减少 API 调用 |

### 2. 复杂乱码修复

| 功能 | 说明 |
|------|------|
| 上下文推断 | 根据语义推断正确字符 |
| 规则学习 | 高置信度修复自动保存为新规则 |
| 分级处理 | 规则优先，AI 补充 |

### 3. 智能章节识别

| 功能 | 说明 |
|------|------|
| 非标准格式 | 识别各种变体章节标题 |
| 结构分析 | 分析全文结构，提取章节列表 |
| 标题规范化 | 统一章节标题格式 |

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 文件过大 | 超过 10MB | 分卷处理或提示用户 |
| 编码无法识别 | 特殊编码 | 尝试多种编码，使用 errors='replace' |
| 乱码过多 | 编码错误 | 使用 thorough 模式进行 AI 修复 |
| 章节识别不准 | 格式不规范 | 使用 thorough 模式进行 AI 识别 |
| 处理速度慢 | AI 模式 | 使用 fast 模式或 balanced 模式 |

## 配置说明

配置文件位于 `config/ai_config.yaml`，可自定义：

```yaml
# 处理模式
mode: "balanced"  # fast / balanced / thorough

# AI 功能开关
ai_enhancement:
  ad_detection:
    enabled: true
    confidence_threshold: 0.8
  mojibake_fix:
    enabled: true
    confidence_threshold: 0.7
    auto_learn: true
  chapter_detection:
    enabled: false

# LLM 配置
llm:
  provider: "xiaoyi"
  model: "glm-4-flash"
```

## 重要说明

### 📖 一键导入书架

收到清理后的文件后，您可以：
1. **在聊天中长按文件**
2. **选择"分享"**
3. **选择"华为阅读"**

即可一键导入书架，享受修复完美的阅读体验！

---

*技能版本: 4.1.0 (广告+乱码规则全面扩展，LLM子会话集成)*
*更新时间: 2026-03-29*

## 版本历史

详见 [CHANGELOG.md](./CHANGELOG.md)

---
name: image-knowledge-converter
description: "图片截图转知识库工具（OCR + AI）。触发词：第一次使用、配置图片工具、处理新图片"
version: 1.2.8
tags: [image-processing, ocr, knowledge-management]
---

# 🔧 执行指令

**配置向导触发词：**
当用户说 `第一次使用` / `第一次使用图片处理工具` / `配置图片工具` 时，**AI 启动对话式配置向导**。

**处理图片触发词：**
当用户说 `处理新图片` / `截图转文档` / `整理截图` 时（这三个触发词等价，均执行相同的处理流程），执行：

**自动检测工作目录**（优先从以下路径检测）：
1. 命令行参数 `--work-dir <路径>`
2. 环境变量 `WORK_DIR`
3. 脚本所在目录（兜底）

```
# 方式1：显式指定工作目录（推荐）
python auto_process_all_v9_4.py --work-dir "D:\WorkBuddy-Projects\图片知识库"

# 方式2：在工作目录中直接运行
cd "D:\WorkBuddy-Projects\图片知识库"
python auto_process_all_v9_4.py

# 方式3：使用环境变量
set WORK_DIR=D:\WorkBuddy-Projects\图片知识库
python auto_process_all_v9_4.py
```

---

## 📋 对话式配置向导（5步）

**安全原则：API 密钥不通过对话传递，用户直接在本地模板文件中填写。**

### 第1步：AI 询问工作文件夹位置

当用户说"第一次使用"时，AI 先询问用户想把工具安装到哪个文件夹：

```
🤖 我来帮你完成配置！首先需要确定工作文件夹位置。

这个文件夹将用来存放：
• 你的待处理图片
• 生成的文档
• 配置文件

请告诉我你想使用的文件夹路径，例如：
  D:\图片知识库
  或桌面上的任意位置

（直接回车将使用默认位置）
```

> **关键**：工作文件夹由用户指定，不是写死的路径。

### 第2步：AI 创建配置模板

AI 在用户指定的工作文件夹下创建配置模板：
```
{工作文件夹}\config\api_keys_template.txt
```

### 第3步：AI 引导用户填写

AI 告诉用户：
```
✅ 配置模板已创建！

📝 请打开文件并填写配置：
   {工作文件夹}\config\api_keys_template.txt

【填写说明】

1️⃣  OCR 模式（必选一项，删除前面的 # 启用）：
    # OCR_MODE: cloud    ← 云端方案（腾讯+百度）
    # OCR_MODE: local     ← 本地方案（Tesseract）
    # OCR_MODE: hybrid    ← 兜底方案（云端+本地）

2️⃣  填写 API 密钥（根据上一步选择填写）：
    - 腾讯云 SecretId/SecretKey
    - 百度云 API Key/Secret Key
    - 或启用 use_tesseract: true

3️⃣  LLM 配置（如需 AI 智能分析）：
    # 注意：混元(Hunyuan)使用与腾讯云OCR相同的密钥，无需单独配置
    # 如需使用其他LLM，请参考代码中的配置项
    llm_enabled: true
    llm_provider: hunyuan

4️⃣  IMA 同步（如需自动同步到 IMA，必须改为 true）：
    # 启用：将下方 false 改为 true，并填写 client_id 和 api_key
    # 获取方法：IMA 设置 → API → 创建新的 API Key
    ima_enabled: true          ← 必须改为 true 才能启用
    ima_api_key: 你的API密钥
    ima_client_id: 你的ClientID

5️⃣  填写完成后保存文件，然后对我说「配置已填写完毕」
```

### 第4步：AI 处理配置

用户说「配置已填写完毕后」，AI 自动：
```
# 运行配置处理器（自动检测工作目录）
python wizard_processor.py

# 或显式指定工作目录
python wizard_processor.py --work-dir "D:\WorkBuddy-Projects\图片知识库"
```
1. wizard_processor.py 读取模板
2. 生成 `config/api_keys.yaml`
3. 验证配置并显示摘要

### 第5步：放入图片并处理

```
✅ 配置完成！

📁 请把图片放入：
   {工作文件夹}\待处理图片

然后对我说「处理新图片」
```

---

## 🚀 快速上手

### 首次使用
1. 说 `第一次使用图片处理工具`
2. AI 创建配置模板
3. 用户直接编辑模板文件（密钥不在对话框中）
4. 用户说「配置已填写完毕」
5. AI 处理配置并验证
6. 放入图片，说「处理新图片」

### 日常使用
1. 把图片放入 `待处理图片\`
2. 说「处理新图片」

---

## 触发词

**首次配置（启动向导）：**
- `第一次使用`
- `第一次使用图片处理工具`
- `配置图片工具`
- `首次配置`

**开始处理（运行脚本）：**
- `处理新图片`
- `截图转文档`
- `整理截图`

---

## 目录结构

```
{工作文件夹}\           ← 所有文件都在用户指定的工作目录下
├── auto_process_all_v9_4.py ← 主处理脚本（V9.5 支持 --work-dir）
├── wizard_processor.py     ← 配置处理器
├── setup_wizard.py          ← 交互式配置向导（可选）
├── config\
│   ├── api_keys_template.txt  ← 用户在此填写（本地）
│   └── api_keys.yaml          ← 自动生成
├── 待处理图片\
├── 已处理图片\
├── 处理结果\
│   ├── *.md                  ← 生成的 Markdown 文档
│   ├── *.docx                ← 生成的 Word 文档
│   ├── process.log           ← 运行日志
│   └── 处理报告.json         ← 处理统计报告
└── progress\                 ← 分批处理状态（自动创建）
```

---

## 版本历史

**v1.2.7 (2026-05-20)**
- ✅ **混元签名修复**：修复 TC3-HMAC-SHA256 签名算法，添加 `x-tc-action` 到 CanonicalHeaders 和 SignedHeaders
- ✅ **Content-Type 修复**：改为 `application/json; charset=utf-8` 与腾讯云官方一致
- ✅ **SDK 依赖移除**：无需安装 `tencentcloud-sdk-python-v3`，只需 `requests` 库

**v1.2.6 (2026-05-20)**
- ✅ **SDK 依赖移除**：改用腾讯云 REST API 调用混元 LLM，无需安装 `tencentcloud-sdk-python-v3`
- ✅ **混元调用优化**：使用 TC3-HMAC-SHA256 签名认证，与其他 LLM（硅基流动/Kimi/Doubao）一样只需 `requests` 库
- ✅ **LLM 说明优化**：SKILL.md 明确说明混元使用与腾讯云OCR相同的密钥，无需单独配置
- ✅ **配置文件修复**：重新生成 api_keys.yaml 确保嵌套结构正确

**v1.2.5 (2026-05-20)**
- ✅ **IMA 解析修复**：wizard_processor.py 现在同时支持注释和无注释格式的 `ima_enabled`
- ✅ **模板解析修复**：优先用冒号分隔（支持 base64 值中含 `=` 的情况）
- ✅ **IMA 模板优化**：api_keys_template.txt 中 IMA 配置说明更清晰，明确标注"必须改为 true"
- ✅ **SKILL.md 更新**：配置向导第3步中 IMA 配置说明更详细

**v1.2.4 (2026-05-20)**
- ✅ **核心修复**：`auto_process_all_v9_4.py` 支持 `--work-dir` 命令行参数指定工作目录
- ✅ **路径统一**：所有路径引用（配置/输入/输出/日志）改为基于工作目录，不再依赖脚本所在目录
- ✅ **向后兼容**：不指定工作目录时，自动使用脚本所在目录（保持原有行为）

**v1.2.3 (2026-05-20)**
- ✅ **路径修复**：`wizard_processor.py` 的 `get_work_folder()` 不再硬编码默认路径，改为动态检测脚本目录
- ✅ **路径修复**：`SKILL.md` 移除所有硬编码示例路径，改为 `{工作文件夹}` 占位符
- ✅ **流程优化**：配置向导明确要求 AI 先询问用户指定工作文件夹位置

**v1.2.2 (2026-05-20)**
- ✅ **安全升级**：API 密钥完全不在对话中传输，用户直接编辑本地模板文件
- ✅ **流程优化**：从 6 步优化为 5 步（新增第1步：AI 询问用户指定工作文件夹）
- ✅ **IMA 修复**：修复了 IMA 配置无法加载的问题（添加 client_id 支持）
- ✅ **OCR 新增 C 兜底选项**

**v1.2.1 (2026-05-20)**
- ✅ **安全升级**：API 密钥统一写入模板文件后由系统处理
- ✅ **OCR 新增兜底方案**：A（云端）、B（本地）、C（A+B 兜底）
- ✅ **自动验证配置**

**v1.2.0 (2026-05-10)**
- ✅ 重构为对话式配置向导

**v1.1.0 (2026-04-27)**
- ✅ 初始版本

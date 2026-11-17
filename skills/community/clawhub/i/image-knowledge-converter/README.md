# 📚 图片知识库整理工具 (Image Knowledge Converter)

> 自动将手机截图转换为结构化 Word + Markdown 知识文档，并同步到 IMA 个人笔记  
> **新用户第一次使用会自动启动向导，无需任何技术背景！**

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/haoyiyong985/image-knowledge-converter?style=social)](https://github.com/haoyiyong985/image-knowledge-converter)
[![WorkBuddy](https://img.shields.io/badge/WorkBuddy-Skill-green)](https://workbuddy.ai)

🌐 [中文](README.md) | [English](README_EN.md)

---

## 🌟 项目简介

**图片知识库整理工具** 是一个智能知识管理助手，能够：

- 📷 **自动识别**：从手机截图（小红书、微信读书、微信等）中提取文字
- 🏷️ **智能分类**：AI 理解内容并自动分类到对应知识主题
- 📝 **生成文档**：输出结构化 Word + Markdown 双格式文档
- 🔗 **自动归档**：按分类整理图片和文档
- 🔄 **内容合并**：相似主题自动合并，避免重复
- ☁️ **云端同步**：一键同步到 IMA 个人笔记

---

## ✨ 功能特点

### 核心功能

| 功能 | 说明 |
|------|------|
| **OCR 多引擎** | 腾讯云 → 百度云 → 本地 Tesseract（自动降级） |
| **AI 智能分类** | 动态分类体系，支持自由命名和自动新建分类 |
| **文档合并** | 同主题内容自动合并到同一文档 |
| **双格式输出** | 同时生成 `.docx` 和 `.md` 文件 |
| **IMA 同步** | 自动同步到 IMA 笔记（支持增量更新）|
| **分批处理** | 大批量图片智能分批，支持断点续传 |
| **重复检测** | Hash + 主题词相似度双重检测 |
| **新手向导** | 🆕 首次使用自动引导配置，无需技术背景 |

### 技术亮点

- ✅ **LLM 全覆盖**：混元 Lite / Kimi / Doubao 多模型兜底
- ✅ **智能命名**：`{分类}-{主题}`，如 `历史文化-钱谦益传`
- ✅ **内容整理**：自动修复 OCR 错误、结构化排版
- ✅ **来源提取**：自动识别小红书、微信等平台来源
- ✅ **新手向导**：第一次使用自动启动交互式配置向导

---

## 🚀 快速开始（三步走）

> **无需选择安装方式！** 无论你用哪种方式安装，第一次运行时都会自动启动**新手向导**，一步步引导你完成配置。

### 第一步：选择安装方式（任选一种）

#### 方式 A：WorkBuddy Skill（最简单 ⭐）

**适合人群**：有 WorkBuddy 账号，想一键使用

1. 下载 Release 中的 `image-knowledge-converter_v1.1.0_skill.zip`
2. 打开 WorkBuddy → 右上角头像 → **Skills 管理**
3. 点击「导入 Skills」→ 选择下载的 zip → 「立即导入」
4. **对 WorkBuddy 说**：`第一次使用` 或 `初始化`
5. ✅ 向导自动启动，引导你完成配置（约 2 分钟）

#### 方式 B：完整包（适合自定义 ⭐）

**适合人群**：想完全控制，或没有 WorkBuddy

1. 下载 Release 中的 `tupianzhengligongju_wanzheng_v1.1.0.zip`
2. 解压到你想放的位置（如 `D:\我的图片知识库`）
3. 打开终端，进入解压目录
4. 运行：`python setup_wizard.py`
5. ✅ 向导自动启动，引导你完成配置（约 2 分钟）

#### 方式 C：Git 克隆（适合开发者）

**适合人群**：熟悉 Git 和命令行

```bash
git clone https://github.com/haoyiyong985/image-knowledge-converter.git
cd image-knowledge-converter
pip install -r requirements.txt
python setup_wizard.py   # ← 启动向导
```

---

### 第二步：新手向导（自动启动）

无论你用哪种方式安装，**第一次运行都会看到这个向导**（不会跳过）：

```
==================================================
  欢迎使用 图片知识库整理工具！
  我是你的智能助手，第一次使用我来帮你完成配置
  只需 3 步，大概 2 分钟

  如果你有任何问题，随时问我！
==================================================
```

#### 向导流程（3 步，约 2 分钟）

**第 1 步：选择工作文件夹**
```
  步骤 1：选择工作文件夹
  ℹ️ 这是存放图片和生成文档的地方。
  
  建议使用：D:\Users\你的用户名\图片知识库
  
  是否使用默认位置？(y/n，直接回车=使用默认):
```

- 选 `y` → 自动创建默认文件夹
- 选 `n` → 输入自定义路径（如 `D:\我的图片库`）

**第 2 步：配置 OCR 服务（选一个就行）**
```
  步骤 2：配置 OCR 识别服务
  ℹ️ 你需要至少一个 OCR 服务来识别图片中的文字。
  
  请选择 OCR 服务（选一个就行）：
    1. 腾讯云 OCR（推荐，每月免费 1000 次）
      识别率高，免费额度充足
    2. 百度云 OCR（免费，需实名）
      免费额度大，适合大量使用
    3. 本地 Tesseract（完全免费）
      无需联网，但识别率较低
      
  请输入选项编号 (1-3):
```

- **选 1（腾讯云）** → 向导显示图文教程 → 你填入 `config/api_keys_template.txt` → 向导自动读取并生成配置
- **选 2（百度云）** → 向导显示图文教程 → 你填入 `config/api_keys_template.txt` → 向导自动读取并生成配置
- **选 3（本地）** → 向导提示安装 Tesseract → 配置完成

**第 3 步：创建文件夹结构**
```
  步骤 3：创建文件夹结构
  ✅ 已创建文件夹：待处理图片
  ✅ 已创建文件夹：已处理图片
  ✅ 已创建文件夹：处理结果
  
  ✅ 配置已保存到 config/api_keys.yaml
```

**第 4 步（可选）：配置 IMA 同步**
```
  （可选）配置 IMA 同步
  ℹ️ IMA 是一个笔记服务，可以自动同步你生成的文档。
  ℹ️ 如果你不用 IMA，可以直接跳过。
  
  是否配置 IMA 同步？(y/n):
```

- 选 `y` → 向导提示获取 IMA API Key → 你填入 `config/api_keys_template.txt` → 向导自动读取并生成配置
- 选 `n` → 跳过，随时可以重新运行向导添加

**完成！**
```
==================================================
  🎉 配置完成！
==================================================
  
  接下来你可以：
  1. 把要处理的图片放到「待处理图片」文件夹里
  2. 运行：python auto_process_all_v9_4.py
  3. 等待处理完成，结果在「处理结果」文件夹里
```

---

### 第三步：放入图片，开始处理

#### 如果使用 WorkBuddy Skill（方式 A）

1. 把图片放到：`你的工作文件夹\待处理图片\`
2. 对 WorkBuddy 说：`处理新图片`
3. 等待处理完成（约 3-5 秒/张）
4. 结果在：`你的工作文件夹\处理结果\`

#### 如果本地运行（方式 B 或 C）

1. 把图片放到：`你的工作文件夹\待处理图片\`
2. 运行：`python auto_process_all_v9_4.py`
3. 等待处理完成（约 3-5 秒/张）
4. 结果在：`你的工作文件夹\处理结果\`

---

## 📖 使用指南

### 目录结构

```
图片知识库\
├── auto_process_all_v9_4.py   ← 主处理脚本（V9.5 逻辑）
├── setup_wizard.py            ← 新手向导脚本
├── requirements.txt
├── config\
│   └── api_keys.yaml        ← OCR/IMA 配置（向导自动生成）
├── 待处理图片\                ← 放入待处理图片
│   ├── 健康养生\
│   ├── 旅行记录\
│   └── ...
├── 已处理图片\                ← 处理完的图片自动归档
└── 处理结果\                  ← 生成的 Word/Markdown 文档
    ├── 历史文化-钱谦益传.docx
    ├── 历史文化-钱谦益传.md
    └── ...
```

### 日常使用流程

#### 第 1 步：放入新图片

把手机截图复制到 `待处理图片` 文件夹（支持子文件夹分类）：

```
待处理图片\健康养生\  ← 健康类图片
待处理图片\旅行记录\  ← 旅行类图片
```

#### 第 2 步：启动处理

**WorkBuddy 用户**：
```
处理新图片
```

**本地用户**：
```bash
python auto_process_all_v9_4.py
```

#### 第 3 步：查看结果

处理完成后，打开 `处理结果` 文件夹，你会看到：

```
处理结果\
├── 历史文化-钱谦益传.docx    ← Word 格式（可编辑）
├── 历史文化-钱谦益传.md     ← Markdown 格式（纯文本）
├── 营养健康-抗炎饮食.docx
└── 营养健康-抗炎饮食.md
```

---

## ⚙️ 配置说明

### 密钥填写模板（安全改进 ⭐）

**新用户注意**：为了保护你的 API 密钥安全，**不再需要把密钥发给 WorkBuddy**！

我们采用 **本地 TXT 文件** 传递密钥：
1. 向导会教你如何获取 API 密钥
2. 你把密钥填入 `config/api_keys_template.txt`（有详细填写说明）
3. 填好后保存，按回车继续
4. 向导自动读取 TXT 文件，生成加密的 YAML 配置文件

**优势**：
- ✅ 密钥不会出现在聊天记录中
- ✅ 密钥不会通过网络传输（除了正常的 API 调用）
- ✅ 你可以在本地安全地编辑文件

TXT 模板文件路径：`config/api_keys_template.txt`（向导会自动创建）

---

### API 密钥配置（向导自动完成）

新手向导会在 `config/api_keys.yaml` 生成如下配置：

```yaml
# OCR 服务（至少配置一个）
ocr:
  tencent:
    secret_id: "你的腾讯云 SecretId"
    secret_key: "你的腾讯云 SecretKey"
  
  # 或百度云
  baidu:
    api_key: "你的百度云 API Key"
    secret_key: "你的百度云 Secret Key"

# IMA 同步（可选，向导会问你要不要配置）
ima:
  api_key: "你的 IMA API Key"
  base_url: "https://api.ima.tencent.com/v1"
```

### 如何获取 API 密钥（向导会一步步教）

| 服务 | 免费额度 | 获取地址 | 向导支持 |
|------|----------|----------|----------|
| 腾讯云 OCR | 1000次/月 | https://console.cloud.tencent.com/cam/capi | ✅ 图文教程 |
| 百度云 OCR | 50000次/天 | https://console.bce.baidu.com/ | ✅ 图文教程 |
| 本地 Tesseract | 完全免费 | https://github.com/UB-Mannheim/tesseract/wiki | ✅ 安装引导 |

---

## 📊 分类体系

### 预设分类（可自动扩展）

| 分类 | 说明 | 示例 |
|------|------|------|
| **历史文化** | 历史、人物传记、文化知识 | 钱谦益传、南宋历史 |
| **营养健康** | 饮食、营养、健康知识 | 抗炎饮食、肠道健康 |
| **生活方式** | 运动、睡眠、日常建议 | 日常饮食建议 |
| **教育育儿** | 教育方法、育儿知识 | - |
| **旅游攻略** | 旅行记录、景点介绍 | - |

### 动态分类

当内容不属于预设分类时，AI 会：
1. 自动判断新主题名称
2. 自由命名分类
3. 创建新分类并归档

**示例**：
- 图片内容是关于「摄影技巧」→ AI 自动创建 `摄影技巧` 分类
- 图片内容是关于「编程学习」→ AI 自动创建 `编程学习` 分类

---

## 💡 常用指令

### WorkBuddy 用户

在 WorkBuddy 对话中可以使用：

| 指令 | 效果 |
|------|------|
| `第一次使用` 或 `初始化` | 启动新手向导（首次配置） |
| `处理新图片` | 处理所有待处理图片 |
| `处理待处理图片/健康养生` | 只处理指定文件夹的图片 |
| `查看现有文档` | 列出所有文档和章节列表 |
| `重新配置` | 重新运行向导更新配置 |

### 本地用户

```bash
# 启动新手向导（首次使用）
python setup_wizard.py

# 处理图片
python auto_process_all_v9_4.py

# 分批处理（大量图片）
python auto_process_all_v9_4.py --batch

# 查看进度
python auto_process_all_v9_4.py --progress

# 清除状态
python auto_process_all_v9_4.py --clear
```

---

## 📂 输出示例

### 处理结果目录

```
处理结果\
├── 历史文化-钱谦益传.docx
├── 历史文化-钱谦益传.md
├── 历史文化-南宋历史概述.docx
├── 历史文化-南宋历史概述.md
└── ...
```

### 文档内容结构

```markdown
# 历史文化-钱谦益传

## 一、生平简介
（OCR 识别内容，AI 自动分段）

## 二、主要成就
（结构化整理）

## 三、历史评价
（自动分类归档）
```

---

## 🔧 高级功能

### 分批处理

处理大量图片时，系统会自动分批：

| 图片大小 | 每批数量 |
|---------|---------|
| < 500KB | 10 张/批 |
| 500KB-2MB | 6 张/批 |
| 2MB-5MB | 4 张/批 |
| > 5MB | 2 张/批 |

### 断点续传

如果处理中断，可以恢复：

```bash
python auto_process_all_v9_4.py --batch
```

查看进度：

```bash
python auto_process_all_v9_4.py --progress
```

清除状态：

```bash
python auto_process_all_v9_4.py --clear
```

---

## 🐛 常见问题

### Q1：我是小白，能用好吗？

**答**：完全可以！  
- 第一次使用会自动启动**新手向导**，一步步教你配置
- 只需 2 分钟，无需任何技术背景
- 配置完成后，每次只需说"处理新图片"即可

### Q2：OCR 识别失败怎么办？

**解决**：
1. 检查图片清晰度（建议分辨率 ≥ 150 DPI）
2. 确认已配置腾讯云/百度云 OCR
3. 安装本地 Tesseract 作为兜底

### Q3：文档命名不符合预期？

**解决**：
- 文档命名格式：`{分类}-{主题}`
- 这是 AI 自动生成的，符合内容主题
- 如需自定义，可修改 `auto_process_all_v9_4.py` 中的命名规则

### Q4：如何避免重复内容？

**解决**：
- 系统自动检测重复（Hash + 主题词相似度）
- 重复图片会自动跳过

### Q5：IMA 同步失败？

**解决**：
1. 检查 `config/api_keys.yaml` 中的 IMA 配置是否正确
2. 确认凭证未过期
3. 重新运行向导：`python setup_wizard.py`

---

## 📈 性能指标

- **处理速度**：约 3-5 秒/张（取决于 OCR 引擎）
- **识别准确率**：中文 90%+（腾讯云 OCR）
- **支持格式**：JPG, PNG, WEBP, BMP
- **输出格式**：Word (.docx) + Markdown (.md)

---

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| **OCR** | 腾讯云、百度云、Tesseract |
| **AI 分析** | 混元 Lite、Kimi、Doubao |
| **文档生成** | python-docx |
| **同步** | IMA OpenAPI |
| **语言** | Python 3.8+ |

---

## 📄 文件说明

### 核心脚本

| 文件 | 说明 |
|------|------|
| `auto_process_all_v9_4.py` | 当前最新版本（V9.5 逻辑） |
| `setup_wizard.py` | 🆕 新手向导脚本（首次使用自动启动） |
| `ima_sync.py` | IMA 同步脚本 |
| `classifier_engine.py` | 分类引擎 |

### 配置文件

| 文件 | 说明 |
|------|------|
| `config/api_keys.yaml` | OCR/IMA 凭证配置（向导自动生成） |
| `requirements.txt` | Python 依赖列表 |
| `.env` | 环境变量（不提交到 Git） |

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

---

## 📝 更新日志

### v1.1.0 (2026-04-27) 🆕

- ✅ **内置新手向导**（首次使用自动引导配置）
- ✅ 支持图文教程获取 API 密钥
- ✅ 自动创建文件夹结构
- ✅ 更新至 V9.5 处理逻辑
- ✅ 删除"综合知识"兜底分类
- ✅ 支持 LLM 自由命名分类
- ✅ 新增 `setup_wizard.py` 向导脚本

### v1.0.0 (2026-03-17)

- ✅ 初始版本发布
- ✅ 支持 OCR 识别（腾讯云、百度云、Tesseract）
- ✅ AI 智能分类和文档合并
- ✅ Word + Markdown 双格式输出
- ✅ IMA 同步功能

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## 🙏 致谢

- [WorkBuddy](https://workbuddy.ai) - AI 助手平台
- [腾讯云 OCR](https://cloud.tencent.com/product/ocr) - OCR 服务
- [百度云 OCR](https://ai.baidu.com/tech/ocr) - OCR 服务
- [Tesseract](https://github.com/tesseract-ocr/tesseract) - 开源 OCR 引擎

---

## 📧 联系

- GitHub Issues：[提交问题](https://github.com/haoyiyong985/image-knowledge-converter/issues)
- 邮箱：（添加你的联系方式）

---

**⭐ 如果这个项目对你有帮助，请给它一个星标！**

# OpenClaw 中文文本纠错 Skill（专业模型版）

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Model](https://img.shields.io/badge/Model-MacBERT4CSC-orange)

**专为 OpenClaw 开发的中文文本纠错 Skill**  
使用 **pycorrector + MacBERT** 专业模型，自动修正中文拼写、形近字、语法、标点错误。准确率高达 **90%+**，远超普通 LLM 提示词。

---

## ✨ 特性

- **SOTA 模型**：基于 MacBERT4CSC（Hugging Face 官方模型）
- **高精度**：支持错别字、形近字、同音字、语法错误、标点修复
- **长文本支持**：单次处理 5000+ 字无压力
- **自动安装**：首次使用自动下载模型
- **OpenClaw 原生集成**：Agent 一键调用，无需额外配置
- **对比输出**：返回修正后文本 + 修改详情（可选）

---

## 📥 模型下载地址（必看）

**主模型（推荐，直接使用）**：
- **Hugging Face**：https://huggingface.co/shibing624/macbert4csc-base-chinese

> **提示**：首次运行 `pycorrector.correct()` 时会**自动下载**（约 400MB），无需手动操作。  
> 下载后模型会缓存到 `~/.cache/huggingface/hub/` 目录。

**备用手动下载方式**（如果自动下载失败）：
1. 访问上方链接
2. 下载 `pytorch_model.bin`、`config.json` 等文件
3. 放入 `~/.cache/huggingface/hub/models/.../` 目录

---

### **在 OpenClaw 聊天中**

你可以直接对你的 Agent 说：

帮我纠正这段文字：今天天气好好，我去公园散步。

纠正："F:/命理学-音频-干声-文本" 目录下的所有.txt文本内容纠错，并且要精修。

/LLM-Text-Correct + 粘贴大段文本（斜杠命令强制触发）

把这个文件纠错："F:/命理学-音频-干声-文本/月支月令如何看一个人事业！_20260321_200451.txt"


### **命令行直接使用**

cd D:\openclaw-2026.3.13\skills\llm-text-correct

python scripts\correct_text.py "F:/命理学-音频-干声-文本/月支月令如何看一个人事业！_20260321_200451.txt"

python scripts\correct_text.py "F:/命理学-音频-干声-文本" --refine


## 🚀 安装方法（30 秒完成）

### 方式一：推荐（直接 Clone 本仓库）
```bash
git clone https://github.com/wangminrui2022/llm-text-correct.git
cd chinese-text-correction

# my_custom_confusion.txt

## 简介

自定义中文纠错词表（混淆集），支持**权重控制**，用于指定错误词与正确词的映射关系，提升纠错效果。

---

## 格式

每行一条规则，支持两种写法：

### 1️⃣ 基础格式

```txt
错误词 正确词
```

### 2️⃣ 带权重格式

```txt
错误词 正确词 权重
```

或使用制表符（`\t`）分隔：

```txt
错误词\t正确词\t权重
```

---

## 示例

```txt
交通先行 交通限行 10
苹果吧 苹果八 20
iphonex iphoneX
小明同学 小茗同学 1000
```

---

## 字段说明

| 字段  | 说明                |
| --- | ----------------- |
| 错误词 | 需要被替换的文本          |
| 正确词 | 替换后的文本            |
| 权重  | 优先级（可选，数字越大优先级越高） |

---

## 规则说明

* 命中规则会进行替换
* **权重越高，优先级越高**
* 未设置权重时，使用默认权重
* 可用于解决多个候选冲突问题

---

## 用途

* 修正常见错别字
* 拼音/同音错误纠正
* 专有名词保护（如 iPhoneX）
* ASR（语音识别）后处理优化

---

## 注意

* 避免重复或冲突规则
* 权重差距建议拉开（如：10 / 100 / 1000）
* 建议按业务场景持续维护

---

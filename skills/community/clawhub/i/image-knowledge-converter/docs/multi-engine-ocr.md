# 多引擎 OCR 使用说明

## 🎯 功能概述

图片知识库工具现已支持**多 OCR 引擎自动切换**，当首选引擎达到频率限制时，会自动提示您选择备用引擎。

### 支持的 OCR 引擎

| 优先级 | 引擎 | 免费额度 | 特点 |
|-------|------|---------|------|
| 1 | 腾讯云 OCR | 1000次/月 | 首选，中文识别准确 |
| 2 | 百度 OCR | 50000次/月 | 第一备用，额度充足 |
| 3 | 本地 Tesseract | 无限 | 第二备用，无需网络 |

---

## 📦 文件说明

| 文件 | 功能 |
|-----|------|
| `tencent_ocr.py` | 腾讯云 OCR 模块 |
| `baidu_ocr.py` | 百度 OCR 模块 |
| `local_ocr.py` | 本地 Tesseract 模块 |
| `ocr_manager.py` | OCR 管理器（多引擎切换） |
| `auto_process_v2.py` | 主程序（使用多引擎） |

---

## 🚀 使用方法

### 方式一：使用默认配置（腾讯云）

```bash
python auto_process_v2.py
```

程序会自动使用已配置的腾讯云 OCR。

### 方式二：当腾讯云达到频率限制

当提示"已达频率上限"时，会弹出选择窗口：

```
⚠️ 腾讯云 OCR 达到频率限制

请选择其他 OCR 引擎:

✓ 腾讯云 OCR: 已配置
✗ 百度 OCR: 未配置 API 密钥
✗ 本地 Tesseract: 未安装

请选择（输入数字）:
1 - 腾讯云 OCR
2 - 百度 OCR
3 - 本地 Tesseract
0 - 取消
```

**选择 2 或 3 切换到备用引擎**

---

## 🔧 配置备用引擎

### 配置百度 OCR（推荐作为备用）

**步骤 1：申请百度 OCR**
1. 访问 https://ai.baidu.com/tech/ocr
2. 登录百度账号
3. 点击「立即使用」
4. 创建应用，获取 AppID、API Key、Secret Key

**步骤 2：配置密钥**

编辑 `ocr_manager.py`，在文件开头添加：

```python
# 设置默认 API 密钥（腾讯云）
os.environ['TENCENT_SECRET_ID'] = '你的腾讯云SecretId'
os.environ['TENCENT_SECRET_KEY'] = '你的腾讯云SecretKey'

# 设置百度 OCR 密钥
os.environ['BAIDU_APP_ID'] = '你的百度AppID'
os.environ['BAIDU_API_KEY'] = '你的百度APIKey'
os.environ['BAIDU_SECRET_KEY'] = '你的百度SecretKey'
```

---

### 配置本地 Tesseract

**步骤 1：安装 Tesseract**

1. 下载安装包：https://github.com/UB-Mannheim/tesseract/wiki
2. 运行安装程序
3. **重要**：安装时勾选中文语言包 (chi_sim)
4. 将 Tesseract 安装目录添加到系统 PATH

**步骤 2：安装 Python 包**

```bash
pip install pytesseract pillow
```

**步骤 3：验证安装**

```bash
tesseract --version
```

---

## 📋 使用流程示例

### 场景 1：正常处理

```
开始处理
  ↓
自动选择腾讯云 OCR
  ↓
识别图片 ✓
  ↓
完成
```

### 场景 2：达到频率限制

```
开始处理
  ↓
自动选择腾讯云 OCR
  ↓
识别第 10 张图片...
  ↓
⚠️ 达到频率限制！
  ↓
[弹窗] 请选择备用引擎
  ↓
用户选择: 百度 OCR
  ↓
切换到百度 OCR
  ↓
继续识别剩余图片 ✓
  ↓
完成
```

---

## 💡 最佳实践

### 推荐配置

**配置 1：腾讯云 + 百度（推荐）**
- 首选：腾讯云（1000次/月）
- 备用：百度（50000次/月）
- 优点：额度充足，识别准确

**配置 2：腾讯云 + 本地 Tesseract**
- 首选：腾讯云
- 备用：本地 Tesseract
- 优点：完全免费，无需申请多个账号

### 批量处理策略

1. **小批量处理**：每次处理 5-10 张图片
2. **遇到限制切换**：频率限制时立即切换备用引擎
3. **错峰处理**：不同时间段使用不同引擎

---

## ⚠️ 常见问题

### Q1: 弹窗没有显示

**A**: 确保您的环境支持 GUI。如果在无界面环境运行，可以修改代码使用命令行选择：

```python
# 在 ocr_manager.py 中添加命令行选择模式
```

### Q2: 百度 OCR 如何申请

**A**: 
1. 访问 https://ai.baidu.com/tech/ocr/general
2. 点击「立即使用」
3. 创建应用后获取密钥
4. 免费额度：50000次/月

### Q3: Tesseract 识别中文效果差

**A**:
1. 确保安装了中文语言包 `chi_sim.traineddata`
2. 确保语言包在 Tesseract 的 `tessdata` 目录
3. 初始化时指定语言：`LocalOCR(lang='chi_sim+eng')`

### Q4: 如何查看当前使用的引擎

**A**: 程序启动时会显示：
```
当前使用引擎: 腾讯云 OCR
```

---

## 🔗 相关链接

- 腾讯云 OCR：https://cloud.tencent.com/product/ocr
- 百度 OCR：https://ai.baidu.com/tech/ocr
- Tesseract：https://github.com/tesseract-ocr/tesseract

---

**现在您可以无忧处理大量图片了！** 🎉

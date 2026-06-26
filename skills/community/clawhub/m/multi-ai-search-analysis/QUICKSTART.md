# 🚀 快速开始 - Multi-AI Search Analysis

**3 分钟上手，自动并行询问 4 家 AI！**

---

## 步骤 1：安装依赖（1 分钟）

```bash
# 进入技能目录
cd skills/multi-ai-search-analysis

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chrome
```

**国内用户加速**：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 步骤 2：首次登录（1 分钟）

```bash
python scripts/login.py
```

会自动打开浏览器，依次登录：
1. **DeepSeek** - 微信扫码
2. **Qwen** - GitHub/Google
3. **豆包** - 手机号
4. **Kimi** - 手机号

登录后**不要关闭浏览器**，脚本会复用登录状态。

---

## 步骤 3：运行分析（3-5 分钟）

```bash
# 并行模式（推荐）
python scripts/run.py --topic "伊朗局势分析"
```

等待 3-5 分钟，报告自动生成在 `reports/` 目录。

---

## 📊 查看报告

```bash
# 用默认应用打开最新报告
python scripts/open-report.py latest

# 或手动打开
# reports/伊朗局势分析 -2026-03-16-2330.md
```

---

## 🎯 常用命令

### 指定 AI 平台

```bash
python scripts/run.py \
  --topic "全球油价预测" \
  --platforms DeepSeek Qwen Kimi
```

### 自定义维度

```bash
# 技术对比
python scripts/run.py \
  --topic "Python vs Java" \
  --dimensions 性能 易用性 生态 就业

# 产品评测
python scripts/run.py \
  --topic "iPhone 16 Pro" \
  --dimensions 性能 拍照 续航 价格
```

### 指定输出

```bash
python scripts/run.py \
  --topic "伊朗局势" \
  --output "C:/reports/iran-analysis.md"
```

### 串行模式（遇到验证码时）

```bash
python scripts/run.py \
  --topic "复杂分析" \
  --mode serial
```

### 使用模板

```bash
# 对比分析模板
python scripts/run.py \
  --topic "MySQL vs PostgreSQL" \
  --dimensions 性能 功能 生态 \
  --report-template comparison

# 自定义问题模板
python scripts/run.py \
  --topic "产品分析" \
  --question-template "请从专业角度分析{topic}，重点讨论{dimensions}"
```

---

## ❓ 常见问题

### Q1: `pip install` 失败

```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: `playwright install` 失败

```bash
# 手动下载 Chromium
playwright install chrome --force

# 或检查网络
ping playwright.dev
```

### Q3: 提示未登录

```bash
# 重新登录
python scripts/login.py

# 清除缓存
rm -rf browser-profile
python scripts/login.py
```

### Q4: 超时错误

```bash
# 增加超时时间
python scripts/run.py --topic "xxx" --timeout 180
```

---

## 📚 完整文档

- [README_PYTHON.md](./README_PYTHON.md) - Python 版使用说明
- [SKILL.md](../SKILL.md) - 技能详细说明
- [INSTALL.md](./INSTALL.md) - 详细安装指南

---

## 💡 下一步

运行一次成功后，可以：

1. **修改配置**：编辑 `config/ai-platforms.json` 自定义选择器
2. **扩展平台**：添加 Claude、Gemini 等新 AI
3. **定制报告**：修改 `reporter.py` 调整输出格式
4. **自动化集成**：将脚本集成到你的工作流

---

*有问题？查看日志文件 `logs/*.log` 或提交 Issue*

**维护者**：小呱 🐸  
**版本**：v1.1  
**更新时间**：2026-03-16

# Multi-AI Search Analysis - Python 自动化脚本

**版本**：v1.1  
**功能**：并行询问多家 AI，自动汇总生成对比报告  
**预计耗时**：3-5 分钟（并行模式）

---

## 📦 环境要求

- Python 3.8+
- Chrome/Edge 浏览器
- 各 AI 平台账号（DeepSeek、Qwen、豆包、Kimi）

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd skills/multi-ai-search-analysis
pip install -r requirements.txt
```

### 2. 首次登录

```bash
python scripts/login.py
```

手动完成各平台登录后关闭浏览器。

### 3. 运行分析

```bash
# 并行模式（推荐）
python scripts/run.py --topic "伊朗局势分析"

# 串行模式（备用）
python scripts/run.py --topic "伊朗局势分析" --mode serial
```

---

## 📁 脚本结构

```
multi-ai-search-analysis/
├── scripts/
│   ├── run.py                 # 主执行脚本
│   ├── login.py               # 登录工具
│   ├── extractor.py           # 数据提取
│   ├── reporter.py            # 报告生成
│   └── utils/
│       ├── browser.py         # 浏览器封装
│       ├── config.py          # 配置管理
│       └── selectors.py       # 元素选择器
├── config/
│   └── ai-platforms.json      # 平台配置
├── reports/                   # 生成的报告
├── logs/                      # 日志文件
└── requirements.txt           # Python 依赖
```

---

## 💻 使用示例

### 基本用法

```bash
python scripts/run.py --topic "伊朗局势分析"
```

### 指定 AI 平台

```bash
python scripts/run.py \
  --topic "全球油价预测" \
  --platforms DeepSeek Qwen Kimi
```

### 自定义分析维度

```bash
python scripts/run.py \
  --topic "AI 行业发展" \
  --dimensions 技术 市场 投资 政策
```

### 指定输出路径

```bash
python scripts/run.py \
  --topic "伊朗局势" \
  --output "C:/reports/iran-analysis.md"
```

### 调整超时时间

```bash
python scripts/run.py \
  --topic "复杂分析" \
  --timeout 180
```

### 完整示例

```bash
python scripts/run.py \
  --topic "2026 年中东局势对全球经济的影响" \
  --platforms DeepSeek Qwen 豆包 Kimi \
  --dimensions 政治 经济 军事 外交 能源 \
  --output "C:/reports/middle-east-2026.md" \
  --timeout 150 \
  --mode parallel
```

---

## 🔧 配置说明

### 配置文件：`config/ai-platforms.json`

```json
{
  "platforms": [
    {
      "name": "DeepSeek",
      "url": "https://chat.deepseek.com",
      "loginMethod": "wechat",
      "avgResponseTime": 15,
      "selectors": {
        "input": "textarea[placeholder*='输入']",
        "send": "button[aria-label*='发送']",
        "response": "div.markdown-body"
      }
    }
    // ... 其他平台
  ]
}
```

### 环境变量（可选）

```bash
# 设置浏览器路径
export CHROME_PATH="/usr/bin/google-chrome"

# 设置用户数据目录（保存登录状态）
export BROWSER_USER_DATA="./browser-profile"

# 启用调试模式
export DEBUG=true
```

---

## 📊 输出内容

### 报告位置

```
reports/
└── 伊朗局势分析 -2026-03-16-2330.md
```

### 报告结构

```markdown
# 伊朗局势分析 - 综合分析报告

## 执行摘要
[200 字核心结论]

## 一、核心事实
- 事件时间线
- 关键数据汇总

## 二、分维度分析
[政治/经济/军事/外交]

## 三、预测与情景
[基准/风险/极端]

## 四、数据对比表
[关键数据横向对比]

## 五、各家特色
[AI 优势对比]

## 六、参考来源
[主要引用]
```

---

## 🔍 故障排查

### 问题 1：依赖安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 2：浏览器无法打开

```bash
# 检查 Chrome 是否安装
chrome --version

# 重新安装 Playwright
playwright install chrome
```

### 问题 3：登录状态丢失

```bash
# 清除缓存重新登录
rm -rf browser-profile

# 重新登录
python scripts/login.py
```

### 问题 4：元素选择器失效

更新 `config/ai-platforms.json` 中的 selectors 配置。

---

## 🎯 最佳实践

1. **提前登录**：运行前 5 分钟完成所有平台登录
2. **使用并行模式**：节省 60-75% 时间
3. **合理设置超时**：复杂分析 120-180 秒
4. **保存报告**：重要分析及时备份

---

## 📚 相关文档

- [SKILL.md](../SKILL.md) - 技能详细说明
- [README.md](../README.md) - 快速开始
- [EXAMPLE.md](../EXAMPLE.md) - 使用案例

---

*最后更新：2026-03-16 23:30*  
*维护者：小呱 🐸*

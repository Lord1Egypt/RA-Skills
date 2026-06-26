# 全球财报智能下载器 Skill

**版本**: 1.0.0  
**创建**: 2026-04-03  
**维护人**: 玄武 🐢

---

## 📁 Skill 结构

```
global-financial-downloader/
├── SKILL.md              # Skill 配置文件
├── README.md             # 本文件
├── downloader.py         # 主下载脚本
└── stock_mapping.json    # 股票映射配置
```

---

## 🚀 使用方法

### 在 Skill 目录内使用

```bash
cd /root/.openclaw/workspace/skills/global-financial-downloader

# 下载贵州茅台
python3 downloader.py 贵州茅台 --from=2020 --to=2025 --pdf

# 下载腾讯
python3 downloader.py 00700 --from=2020 --to=2025 --pdf

# 下载苹果
python3 downloader.py AAPL --from=2020 --to=2025 --type=10-K --pdf
```

### 从任何位置使用

```bash
/usr/local/bin/python3.11 \
  /root/.openclaw/workspace/skills/global-financial-downloader/downloader.py \
  贵州茅台 --pdf
```

### 创建便捷脚本

```bash
# 创建全局命令
cat > /usr/local/bin/financial-downloader << 'EOF'
#!/bin/bash
/usr/local/bin/python3.11 \
  /root/.openclaw/workspace/skills/global-financial-downloader/downloader.py \
  "$@"
EOF
chmod +x /usr/local/bin/financial-downloader

# 使用
financial-downloader 贵州茅台 --pdf
```

---

## 📊 支持的股票市场

### A 股（中国）
- **使用股票代码**: 支持所有 A 股公司（6 位数字代码）
- **使用公司名称**: 支持预定义的 50 家公司

### 港股（香港）
- **使用股票代码**: 支持所有港股公司（5 位数字代码）
- **使用公司名称**: 支持预定义的 51 家公司

### 美股（美国）
- **使用股票代码**: 支持所有美股公司（字母代码）
- **使用公司名称**: 支持预定义的 100 家公司

---

## 📁 输出目录

下载的文件保存在：

```
/root/.openclaw/workspace/exports/
├── cninfo_{公司名}/     # A 股
├── hkex_{公司名}/       # 港股
└── sec_{公司名}/        # 美股
```

---

## 🔧 配置

### 添加新公司

编辑 `stock_mapping.json`，在对应市场的 stocks 数组中添加：

```json
["股票代码", "中文名称", "英文名称"]
```

**示例**:
```json
["601318", "中国平安", "ping_an_insurance"],
["000858", "五粮液", "wuliangye"]
```

### 配置文件位置

- **Skill 配置**: `/root/.openclaw/workspace/skills/global-financial-downloader/stock_mapping.json`
- **原始配置**: `/root/.openclaw/workspace/configs/stock_top300_mapping.json`

**注意**: Skill 使用自己的配置文件副本，修改后需要更新 Skill 目录内的文件。

---

## 📖 完整文档

**Skill 文档**: `SKILL.md`

**包含**:
- 快速开始指南
- 参数说明
- 支持的公司列表
- 使用示例
- 故障排除

---

## 🔄 从 scripts 目录迁移

原脚本位于：`/root/.openclaw/workspace/scripts/global_financial_downloader.py`

**已迁移到 Skill**:
- ✅ 主脚本 → `downloader.py`
- ✅ 配置文件 → `stock_mapping.json`
- ✅ 文档 → `SKILL.md`

**建议**: 使用 Skill 版本，便于管理和复用。

---

## 🐛 故障排除

### 问题 1: 找不到公司

**解决**: 使用股票代码而不是公司名称

```bash
# ❌ 可能失败（如果公司未预定义）
python3 downloader.py 某公司 --pdf

# ✅ 总是成功
python3 downloader.py 600XXX --pdf
```

### 问题 2: 配置文件找不到

**解决**: 确保在 Skill 目录内运行，或使用完整路径

```bash
# 方式 1: 在 Skill 目录内运行
cd /root/.openclaw/workspace/skills/global-financial-downloader
python3 downloader.py 贵州茅台 --pdf

# 方式 2: 使用完整路径
/usr/local/bin/python3.11 \
  /root/.openclaw/workspace/skills/global-financial-downloader/downloader.py \
  贵州茅台 --pdf
```

---

## 📞 维护信息

- **版本**: 1.0.0
- **创建**: 2026-04-03
- **维护人**: 玄武 🐢
- **最后更新**: 2026-04-03

---

## 📚 相关 Skill

- **cninfo-scraper**: 巨潮资讯 A 股爬虫
- **hkex-auto-scraper**: 港交所爬虫
- **sec-edgar-scraper**: 美股 SEC 爬虫

**本 Skill 整合了以上三个爬虫，提供统一的智能下载接口！**

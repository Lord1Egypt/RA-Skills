# 定款商品原图无损下载&规范归档 Skill - 使用说明

## 📋 快速开始

### 1. 安装依赖

```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\product-image-archiver
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）

```bash
# 复制环境变量模板
copy .env.example .env

# 编辑 .env 文件（如使用百度 AI 侵权检测）
notepad .env
```

### 3. 测试运行

```bash
# 单款商品归档
python scripts/archiver.py archive --款号 KZ20260326 --链接 "https://www.wsy.com/item/12345.html"
```

---

## 🎯 使用方式

### 方式 1：OpenClaw 对话调用

**在 OpenClaw 中发送：**
```
归档这个商品的图片
https://www.wsy.com/item/12345.html
款号：KZ20260326
```

### 方式 2：终端直接调用

```bash
# 单款归档
python scripts/archiver.py archive --款号 KZ20260326 --链接 "https://www.wsy.com/item/12345.html"
```

---

## 📊 输出示例

### 归档文件夹结构

```
KZ20260326_春秋立领夹克/
├── 01-网商园原图归档/
│   ├── 001_original.jpg
│   ├── 002_original.jpg
│   └── 003_original.jpg
├── 02-淘宝上架素材待匹配/
└── 03-商品资质档案/
    └── 原图素材归档清单.xlsx
```

### 归档清单（Excel）

| 序号 | 文件名 | 原始 URL | 文件大小 | 格式 | 下载状态 | 完整性 | 风险检测 |
|------|--------|----------|----------|------|----------|--------|----------|
| 001 | 001_original.jpg | https://... | 256KB | JPG | ✅ 成功 | ✅ 完整 | ✅ 无风险 |
| 002 | 002_original.jpg | https://... | 312KB | JPG | ✅ 成功 | ✅ 完整 | ⚠️ 疑似 Logo |

---

## ⚠️ 安全限制

- 仅支持人工输入款号和链接
- 禁止批量自动抓取
- 100% 保留原图，不做任何修改
- 自动标注侵权风险

---

## 📁 文件结构

```
product-image-archiver/
├── SKILL.md
├── _meta.json
├── config.yaml
├── requirements.txt
├── .env.example
├── scripts/
│   ├── archiver.py
│   ├── image_downloader.py
│   ├── folder_manager.py
│   ├── risk_detector.py
│   ├── integrity_checker.py
│   ├── report_generator.py
│   └── sources/
│       ├── wsy_source.py
│       └── source_1688.py
└── archives/
```

---

## 📞 常见问题

### Q: 模块未找到？
```bash
pip install -r requirements.txt
```

### Q: 百度 AI 检测失败？
检查 `.env` 文件中 API Key 配置是否正确

### Q: 图片下载失败？
检查网络连接和图片 URL 是否有效

---

**最后更新：** 2026-03-26  
**版本：** 1.0.0

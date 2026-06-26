---
name: kb-archiver
description: |
  智能本地知识库归档系统 v1.1.0。支持 AI 智能分类、批量归档、全文搜索、统计报告。
  自动将文件分类归档到本地知识库，提取全文索引支持秒级搜索。
  小文件存本地、大文件可对接云存储。支持 Excel/Word/PPT/PDF/TXT 等格式。
  
  当用户需要：归档文件、建立知识库、全文检索文档内容、管理大量工作文档、批量处理文件夹时使用。
  关键词：知识库、归档、文件管理、全文搜索、文档索引、批量归档、AI分类
---

# 知识库归档系统 v1.1.0

智能本地知识库归档方案，支持 **AI 智能分类**、**批量归档**、**全文搜索**、**统计报告**。

## 快速开始

### 单文件归档
```bash
# 基础用法（关键词分类）
node _scripts/archive.mjs /path/to/file.xlsx

# 指定分类
node _scripts/archive.mjs /path/to/file.xlsx "工作文件"

# AI 智能分类
node _scripts/archive.mjs /path/to/file.xlsx --ai-classify
```

### 批量归档
```bash
# 归档整个文件夹
node _scripts/archive.mjs /path/to/folder/

# 按文件类型过滤
node _scripts/archive.mjs /path/to/folder/ --pattern "*.xlsx"

# 批量 AI 分类
node _scripts/archive.mjs /path/to/folder/ --ai-classify
```

### 搜索
```bash
# 搜索关键词
node _scripts/archive.mjs search "门店"

# 按分类过滤
node _scripts/archive.mjs search "数据" --category "工作文件"
```

### 统计
```bash
node _scripts/archive.mjs stats
```

## 目录结构

```
knowledge-base/
├── 工作文件/          ← 数据报表、销售业绩等
├── 方案文档/          ← 计划方案、策略规划等
├── 参考资料/          ← 话术模板、培训教程等
├── 其他文档/          ← 未分类文档
├── _index/            ← 全文索引
│   ├── _manifest.json ← 归档清单
│   └── *.txt          ← 索引文件
└── _scripts/
    └── archive.mjs
```

## 分类说明

| 分类 | 关键词 | 说明 |
|------|--------|------|
| 工作文件 | 数据、报表、统计、门店、业绩、订单 | 日常运营数据 |
| 方案文档 | 方案、计划、策略、制度、规范 | 规划类文档 |
| 参考资料 | 话术、模板、培训、教程、案例 | 学习参考材料 |
| 其他文档 | - | 不属于以上分类 |

## AI 智能分类

使用 `--ai-classify` 参数启用 AI 分类：

- 基于文件名 + 内容摘要进行语义分析
- 自动判断最合适的分类
- AI 不可用时自动 fallback 到关键词匹配

**配置方式**（可选）：
```bash
# 设置环境变量
export OPENCLAW_MODEL="your-model"
export OPENCLAW_API_ENDPOINT="http://localhost:11434/api/chat"
```

## 支持格式

| 格式 | 提取方式 | 说明 |
|------|----------|------|
| .xlsx | Python openpyxl | Excel 表格 |
| .docx | ZIP 解析 | Word 文档 |
| .pptx | ZIP 解析 | PowerPoint |
| .pdf | 直接读取 | PDF 文本 |
| .txt/.csv/.md/.json/.xml/.html/.log | 直接读取 | 文本文件 |

## 云存储对接（可选）

支持腾讯云 COS、AWS S3、阿里云 OSS 等，修改脚本配置即可：

```javascript
const CLOUD_STORAGE = {
  enabled: true,
  type: 'cos',
  bucket: 'mybucket-1250000000',
  prefix: 'knowledge-base/',
  command: (filepath, remotePath) => `coscmd upload "${filepath}" "${remotePath}"`,
};
```

## FAQ

### Q: 大文件如何处理？
A: 超过 10MB 的文件会自动上传到云存储（需配置），本地只保留索引。未配置云存储时会跳过上传但仍创建索引。

### Q: 加密/密码保护的文件怎么办？
A: 加密的 Office 文件无法提取内容，会记录错误信息。建议先解密再归档。

### Q: 文件损坏无法读取？
A: 脚本会捕获错误并记录，不会中断批量处理。损坏文件的索引会标注 `[提取失败: ...]`。

### Q: 如何配置云存储？

**腾讯云 COS：**
```bash
# 安装 coscmd
pip install coscmd
# 配置
coscmd config -a <SecretId> -s <SecretKey> -b <Bucket> -r <Region>
```

**AWS S3：**
```bash
# 安装 aws-cli
pip install awscli
# 配置
aws configure
```

**阿里云 OSS：**
```bash
# 安装 ossutil
wget https://gosspublic.alicdn.com/ossutil/1.7.14/ossutil-v1.7.14-linux-amd64.zip
# 配置
./ossutil config
```

### Q: 批量归档时如何跳过已存在的文件？
A: 脚本会自动检测清单中是否已存在相同文件名和大小的记录，已归档的文件会自动跳过。

### Q: 搜索结果太多怎么办？
A: 使用 `--category` 参数按分类过滤，缩小搜索范围。

## 边界场景

| 场景 | 处理方式 |
|------|----------|
| 文件不存在 | 报错退出 |
| 文件名重复 | 自动添加序号后缀 |
| 不支持的格式 | 创建索引但标注不支持提取 |
| AI 分类失败 | 自动 fallback 到关键词分类 |
| 云存储上传失败 | 记录错误，继续创建本地索引 |
| 批量处理中断 | 已处理的文件已保存，可重新运行继续 |

## 更新日志

### v1.1.0
- ✨ AI 智能分类（基于语义分析）
- ✨ 批量归档整个文件夹
- ✨ 搜索命令（高亮匹配结果）
- ✨ 统计命令（分类统计、总体统计）
- ✨ 进度条显示
- ✨ 文件过滤（--pattern）
- 📝 文档优化（FAQ、边界场景）

### v1.0.0
- 🎉 初始版本
- ✨ 自动分类（关键词匹配）
- ✨ 全文索引
- ✨ 云存储支持

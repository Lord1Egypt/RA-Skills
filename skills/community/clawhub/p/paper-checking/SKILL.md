---
name: paper-checking
description: 论文查重系统 - 一亿字次级论文库秒级查重，支持纵向查重和横向查重
version: 0.1.1
metadata:
  openclaw:
    requires:
      bins:
        - paper_checking.exe
    emoji: "📝"
    homepage: https://github.com/tianlian0/paper_checking_system
---

# paper-checking 论文查重系统

## 技能概述

本技能帮助高校、企业、机构进行文本查重，支持以下场景：
- **纵向查重**：检查文件是否复制比对库内容（论文查重）
- **横向查重**：检查批次文件互相复制情况（防串标）
- **快速查重**：一亿字次级论文库秒级查重
- **报告生成**：输出详细查重报告

**应用场景**：高校论文查重、标书查重、辅助防串标、项目申报书查重、企业内部文档查重、学生作业查重

## 使用流程

AI 助手将引导你完成以下步骤：
1. 安装系统（下载并编译）
2. 配置比对库（添加查重基准文件）
3. 执行查重（纵向或横向）
4. 分析查重报告

## 关键章节导航

- [安装指南](./guides/01-installation.md)
- [快速开始](./guides/02-quickstart.md)
- [高级用法](./guides/03-advanced-usage.md)
- [常见问题](./troubleshooting.md)

## AI 助手能力

当你向 AI 描述查重需求时，AI 会：
- 自动分析文件格式和内容
- 推荐合适的查重阈值
- 执行纵向或横向查重
- 分析查重报告并标识重复段落
- 提供关键词过滤建议
- 处理查重中断恢复

## 核心功能

- ✅ 纵向查重：与比对库文件比对
- ✅ 横向查重：批次文件互相比对
- ✅ 秒级查重：一亿字次级论文库
- ✅ 关键词过滤：过滤学校名、机构名
- ✅ 查重报告：rtf格式详细报告
- ✅ 中断恢复：意外退出后继续查重
- ✅ 多进程并行：CPU逻辑核心数-2

## 快速示例

```bash
# 下载项目
git clone https://github.com/tianlian0/paper_checking_system.git

# 编译运行（需要Visual Studio）
# 打开项目，编译并运行paper_checking.exe

# 添加比对库（纵向查重必需）
选择比对库管理 → 添加到比对库 → 选择文件夹

# 执行查重
选择待查文件 → 设置阈值（10-16） → 开始查重
```

## 安装要求

- Windows 7及以上
- 可用内存1.5GB以上
- Visual Studio 2017及以上
- vc2015运行库
- .NET Framework 4.6

## 许可证

GPL2协议

## 项目链接

- GitHub: https://github.com/tianlian0/paper_checking_system
- Java SDK: https://github.com/tianlian0/duplicate-check-sample
- 商用版: https://xincheck.com

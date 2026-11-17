# 网页新闻关键信息提取 Skill - 使用说明

## 🎯 功能简介
本Skill帮助您从新闻汇总类网页（如机构月报、活动列表）中，自动提取每篇文章的时间与核心事件简介，并整理为Excel表格。

## 📋 适用场景
- 整理机构/企业月度新闻汇总
- 提取公众号文章中的活动记录
- 从长文中梳理时间线事件
- 制作新闻简报或大事记

## 🚀 使用方法

### 方法一：直接对话（推荐）
1. 在Claude中加载本Skill
2. 提供您要提取的**网页链接**
3. Claude会自动访问网页，提取所有新闻条目
4. 输出一个包含"时间"和"事件简介"两列的CSV表格
5. 复制CSV内容，保存为 `.csv` 文件即可用Excel打开

### 方法二：使用辅助脚本转换
如果您已有CSV数据，可使用脚本转为标准Excel格式：
```bash
pip install openpyxl
python scripts/generate_excel.py --input data.csv --output 新闻汇总.xlsx
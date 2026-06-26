---
name: page-analyzer
description: |
  General webpage element analysis and Selenium automation control script generation. Use cases:
  (1) Analyze HTML element structure of any webpage
  (2) Automatically identify form elements (input, button, dropdown, etc.)
  (3) Provide page source code to large model for intelligent analysis
  (4) Generate Selenium control scripts for any web application
  (5) Handle automation tasks like login, search, form submission
  
  Note: This skill should only be used for public webpages or pages you have authorization to access.
---

# General Webpage Element Analysis & Selenium Control

## Overview

This skill analyzes HTML structure of any webpage, identifies interactive elements, and generates Selenium automation control code.

## ⚠️ Security Warnings

1. **Dependencies Required**: Install `selenium` package and matching WebDriver before running
   ```bash
   pip install selenium
   ```
   WebDriver (Edge/Chrome/Firefox) must match your browser version

2. **Sensitive Data Risk**:
   - Do not access internal network pages with sensitive information
   - Page HTML may contain tokens, CSRF credentials, etc.
   - Delete temporary files after analysis

3. **Authorized Pages Only**:
   - Only analyze pages you have permission to access
   - Do not automate control of devices you don't own

## Workflow

### Step 1: Download Page Source

```bash
python scripts/fetch_page.py <URL> -o <output_file> -w <wait_seconds>
```

### Step 2: LLM Analysis

Send the downloaded HTML to LLM for element identification and analysis.

### Step 3: Generate Control Script

Write Selenium automation script based on analysis results.

## Output Format

LLM analysis should include:
- Page overview (title, framework)
- Element inventory table (recommended locating method)
- Complete Python code
- Notes & considerations

---

## 通用网页元素分析与Selenium控制

## 概述

这个Skill用于分析任意网页的HTML结构，识别可交互元素，并生成Selenium自动化控制代码。

## ⚠️ 安全警告

1. **依赖要求**：运行前需安装 `selenium` 包和对应浏览器的 WebDriver
   ```bash
   pip install selenium
   ```
   WebDriver（Edge/Chrome/Firefox）需与浏览器版本匹配

2. **敏感数据风险**：
   - 不要访问包含敏感信息的内部网络页面
   - 页面HTML可能包含token、CSRF凭证等敏感数据
   - 分析完成后建议删除临时文件

3. **仅用于授权页面**：
   - 仅分析你有权限访问的页面
   - 不要自动化控制你不拥有的设备

## 工作流程

### 步骤1: 下载网页源码

```bash
python scripts/fetch_page.py <URL> -o <输出文件> -w <等待秒数>
```

### 步骤2: 大模型分析

将下载的HTML源码发送给大模型进行元素识别和分析。

### 步骤3: 生成控制脚本

根据分析结果编写Selenium自动化脚本。

## 输出格式要求

大模型分析后应输出：
- 页面概述（标题、框架）
- 元素清单表格（推荐定位方式）
- 完整Python代码
- 注意事项
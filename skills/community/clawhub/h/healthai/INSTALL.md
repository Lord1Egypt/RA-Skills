# 🏥 健康管理技能 v1.0 安装指南

## 一、环境要求
- Python 3.8+
- macOS / Linux / Windows

## 二、安装步骤

### 1. 安装 Python 依赖
```bash
cd HealthSkill-1.0
pip install -r requirements.txt
```

### 2. 安装系统依赖（可选）
**macOS:**
```bash
brew install tesseract
brew install poppler
```
**Linux:**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

## 三、使用方法

### 触发技能
说以下任意一句：
- "体检报告"
- "健康数据"
- "运动计划"
- "打卡"
- 直接发文件（PDF/Word/图片）

## 四、文件结构
- SKILL.md - 技能说明
- INSTALL.md - 安装指南
- requirements.txt - 依赖
- scripts/ - 核心代码

## 五、更新日志
### v1.0 (2026-04-04)
- 初始版本

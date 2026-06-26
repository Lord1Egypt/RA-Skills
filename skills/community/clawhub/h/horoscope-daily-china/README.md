# Daily Horoscope Creator

每日星座运势图片生成器 - 基于天行数据 API，输出适合社交媒体发布的精美图片

[English](#english) | [中文](#中文)

---

## 中文

### 简介

本工具用于自动生成 12 星座每日运势图片，集成天行数据官方 API，输出 5 页高清图片，适合发布到小红书、抖音、今日头条等平台。

### 功能特点

- 🌟 12 星座每日运势（API 实时数据）
- 🎨 5 套精美配色模板自动轮换
- 📱 社交媒体优化尺寸（1080×1400）
- 📝 自动生成发布文案
- 🔒 安全的配置管理（API Key 不硬编码）

### 快速开始

#### 1. 安装

```bash
npx clawhub@latest install daily-horoscope
```

#### 2. 配置

```bash
cd skills/daily-horoscope/scripts
cp config.json.example config.json
# 编辑 config.json，填写你的天行数据 API Key
```

#### 3. 使用

```bash
python scripts/generate_horoscope_tianapi.py --date 2026-04-16
```

### 输出文件

- `YYYYMMDD_今日星座运势_p1.png` - 封面 + 红榜 + 开运
- `YYYYMMDD_今日星座运势_p2.png` - 详细运势 1-3 名
- `YYYYMMDD_今日星座运势_p3.png` - 详细运势 4-6 名
- `YYYYMMDD_今日星座运势_p4.png` - 详细运势 7-9 名
- `YYYYMMDD_今日星座运势_p5.png` - 详细运势 10-12 名
- `YYYYMMDD_发布文案.txt` - 今日头条发布文案

### 依赖

- Python 3.8+
- Pillow >= 9.0.0
- Requests >= 2.25.0

### 许可证

MIT License

---

## English

### Introduction

A tool to automatically generate daily horoscope images for 12 constellations, integrated with TianAPI, outputting 5-page high-definition images optimized for social media platforms.

### Features

- 🌟 Daily fortune for 12 constellations (real-time API data)
- 🎨 5 beautiful color templates with auto-rotation
- 📱 Social media optimized size (1080×1400)
- 📝 Auto-generated publishing copy
- 🔒 Secure configuration management

### Quick Start

#### 1. Install

```bash
npx clawhub@latest install daily-horoscope
```

#### 2. Configure

```bash
cd skills/daily-horoscope/scripts
cp config.json.example config.json
# Edit config.json with your TianAPI key
```

#### 3. Use

```bash
python scripts/generate_horoscope_tianapi.py --date 2026-04-16
```

### License

MIT License

---

## 截图预览

![模板预览](references/template-preview.png)

*5套配色模板：星空紫、海洋蓝、玫瑰金、极简黑、温暖橙*

---

## 相关项目

- [almanac-creator](https://clawhub.ai/skills/almanac-creator) - 黄历图片生成器

---

*Made with ❤️ by Digital Transformation Team*

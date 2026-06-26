---
name: daily-horoscope
displayName: Daily Horoscope Creator
description: Create 12 constellation fortune images with TianAPI - 5-page output with large fonts for social media publishing (Xiaohongshu/Douyin/Toutiao)
version: 1.2.1
author: Digital Transformation Team
tags: [horoscope, constellation, zodiac, fortune, tianapi, image-generator, social-media, china]
---

# Daily Horoscope Creator (每日星座运势生成器)

> **数据源**: 天行数据 TianAPI（星座运势 + 星座配对）  
> **输出规格**: 5 页 PNG 图片（1080x1400 像素）  
> **版本**: 1.1.1  
> **适用平台**: 小红书 / 抖音 / 今日头条

---

## 🚀 快速开始

### 安装

```bash
npx clawhub@latest install daily-horoscope
```

### 配置

1. 复制配置文件模板：
```bash
cd skills/daily-horoscope/scripts
cp config.json.example config.json
```

2. 编辑 `config.json`，填写你的天行数据 API Key：
```json
{
  "tianapi": {
    "key": "your_actual_api_key_here"
  }
}
```

> 💡 获取 API Key：[天行数据官网](https://www.tianapi.com/)（免费版 100 次/天）

### 使用

```bash
# 生成今日星座运势
python scripts/generate_horoscope_tianapi.py

# 生成指定日期
python scripts/generate_horoscope_tianapi.py --date 2026-04-16

# 指定模板（1-5）
python scripts/generate_horoscope_tianapi.py --template 1

# 指定输出目录
python scripts/generate_horoscope_tianapi.py --output ./my-output
```

---

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| ✅ **12 星座运势** | 基于天行数据 API，每日更新 |
| ✅ **5 种运势指数** | 综合 / 爱情 / 工作 / 财运 / 健康 |
| ✅ **开运指南** | 幸运色、幸运数字、速配星座（API真实数据） |
| ✅ **星座配对** | 6 对热门配对指数 |
| ✅ **5 套模板** | 星空紫 / 海洋蓝 / 玫瑰金 / 极简黑 / 温暖橙 |
| ✅ **社交媒体优化** | 1080x1400 尺寸，适合小红书/抖音/头条 |
| ✅ **发布文案** | 自动生成今日头条格式文案 |

---

## 📐 输出规格

### 图片参数

| 参数 | 值 | 说明 |
|------|-----|------|
| **尺寸** | 1080 × 1400 px | 9:12.96 竖版比例 |
| **格式** | PNG | 高质量无损 |
| **质量** | 95% | 平衡清晰度与文件大小 |
| **单页大小** | 70-200 KB | 适合网络传播 |

### 5 页内容

| 页码 | 内容 | 说明 |
|------|------|------|
| **p1** | 封面 + 红榜TOP3 + 完整排名 + 配对 + 开运 | 精华汇总 |
| **p2** | 详细运势 1-3 名 | 天秤座、摩羯座、双鱼座... |
| **p3** | 详细运势 4-6 名 | 狮子座、处女座、射手座... |
| **p4** | 详细运势 7-9 名 | 双子座、巨蟹座、白羊座... |
| **p5** | 详细运势 10-12 名 | 水瓶座、金牛座、天蝎座... |

### 5 套配色模板

| 编号 | 名称 | 风格 | 背景 |
|------|------|------|------|
| 1 | **星空紫** | 神秘梦幻 | 深色 #1A0A2E |
| 2 | **海洋蓝** | 清新深邃 | 深色 #0A1628 |
| 3 | **玫瑰金** | 轻奢优雅 | 浅色 #F8F0E6 |
| 4 | **极简黑** | 现代酷炫 | 深色 #1C1C1C |
| 5 | **温暖橙** | 活力阳光 | 浅色 #FFF5E6 |

---

## 📋 发布指南

### 小红书
- **最佳时间**: 20:00-22:00
- **使用图片**: p1（封面）+ p2/p3（精选）
- **文案**: 自动生成 + 添加 #星座 #今日运势 标签

### 抖音
- **最佳时间**: 18:00-21:00
- **使用图片**: p1 + p2
- **建议**: 制作成视频（Ken Burns效果 + 背景音乐）

### 今日头条
- **最佳时间**: 06:30 / 12:00
- **使用图片**: 5 页完整版
- **文案**: 使用自动生成的发布文案

---

## 🔧 技术细节

### 依赖

- Python 3.8+
- Pillow >= 9.0.0
- Requests >= 2.25.0

### API 调用

| API | 次数/日 | 说明 |
|-----|---------|------|
| 星座运势 | 12 次 | 12 星座各 1 次 |
| 星座配对 | 6 次 | 6 对热门配对 |
| **总计** | **18 次** | 免费额度 100 次/天 |

### 数据来源

**来自天行数据 API（每日变化）**：
- ✅ 综合/爱情/工作/财运/健康指数
- ✅ 幸运颜色
- ✅ 幸运数字
- ✅ 速配星座（贵人星座）
- ✅ 今日概述

**注意**：API 不提供幸运方位、幸运时段、提防星座，故不显示

---

## 📁 文件结构

```
daily-horoscope/
├── SKILL.md                      # 技能说明
├── package.json                  # 包信息
├── LICENSE                       # MIT 许可证
├── scripts/
│   ├── generate_horoscope_tianapi.py  # 主脚本
│   ├── constellation_data.py          # 星座数据
│   ├── pair_descriptions.py           # 配对描述
│   ├── config.json                    # 配置文件（需手动创建）
│   ├── config.json.example            # 配置模板
│   ├── .gitignore                     # 忽略规则
│   └── README.md                      # 脚本使用说明
├── references/
│   └── horoscope-image-standard.md    # 图片标准
└── archive/                           # 归档
    └── generate_horoscope.py          # 旧版脚本
```

---

## ⚠️ 注意事项

1. **API Key 安全**
   - `config.json` 包含敏感信息，**请勿提交到 Git**
   - 已添加到 `.gitignore`，不会被跟踪
   - 使用 `config.json.example` 作为模板

2. **API 配额**
   - 天行数据免费版：100 次/天
   - 本技能每日消耗：18 次
   - 建议完成实名认证提升配额

3. **内容合规**
   - 已添加"娱乐参考 切勿迷信"免责声明
   - 符合各大平台内容规范

4. **字体版权**
   - 使用系统自带字体（黑体/微软雅黑）
   - 无版权风险

---

## 📝 更新日志

### v1.0.0 (2026-04-16)
- ✅ 初始版本发布
- ✅ 天行数据 API 集成
- ✅ 5 页标准格式输出
- ✅ 5 套配色模板
- ✅ 配置文件管理（安全）
- ✅ 社交媒体优化

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

### 计划功能
- [ ] 视频自动生成（FFmpeg 集成）
- [ ] Web UI 界面
- [ ] 多 API 源支持（备用）
- [ ] 自定义模板上传

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🔗 相关链接

- **天行数据**: https://www.tianapi.com/
- **ClawHub**: https://clawhub.ai/
- **OpenClaw Docs**: https://docs.openclaw.ai/

---

*Made with ❤️ by Digital Transformation Team*  
*Version: 1.0.0*  
*Last Updated: 2026-04-16*

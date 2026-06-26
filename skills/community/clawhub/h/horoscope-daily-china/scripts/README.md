# Daily Horoscope Scripts

星座运势生成脚本目录

## 📁 目录结构

```
scripts/
├── generate_horoscope_tianapi.py  # 主脚本（标准版）
├── constellation_data.py          # 星座数据
├── pair_descriptions.py           # 配对描述
├── config.json                    # 配置文件（需手动创建）
├── config.json.example            # 配置文件模板
├── .gitignore                     # Git忽略规则
├── README.md                      # 本文件
└── archive/                       # 归档目录
    └── generate_horoscope.py      # 旧版4页脚本（已废弃）
```

## 🚀 使用方法

### 1. 配置API Key

复制模板文件并填写你的天行数据API Key：

```bash
cp config.json.example config.json
```

编辑 `config.json`，将 `YOUR_TIANAPI_KEY_HERE` 替换为你的真实API Key。

### 2. 生成星座运势

```bash
python generate_horoscope_tianapi.py --date 2026-04-16 --output ./output
```

参数说明：
- `--date`: 日期格式 YYYY-MM-DD，默认今天
- `--template`: 模板编号 1-5，默认自动轮换
- `--output`: 输出目录，默认 ./output

### 3. 模板说明

| 编号 | 名称 | 风格 | 背景色 |
|------|------|------|--------|
| 1 | 星空紫 | 神秘梦幻 | 深色 |
| 2 | 海洋蓝 | 清新深邃 | 深色 |
| 3 | 玫瑰金 | 轻奢优雅 | 浅色 |
| 4 | 极简黑 | 现代酷炫 | 深色 |
| 5 | 温暖橙 | 活力阳光 | 浅色 |

## ⚠️ 重要说明

### API Key安全
- `config.json` 包含敏感信息，**请勿提交到Git**
- 已添加到 `.gitignore`，不会被Git跟踪
- 如需共享代码，请使用 `config.json.example` 模板

### 数据说明
- 幸运色、幸运数字、速配星座：来自天行数据API（每日变化）
- 幸运方位、幸运时段、提防星座：**API不提供，已移除显示**

### 旧版脚本
- `archive/generate_horoscope.py` 为旧版4页脚本，已废弃
- 当前标准版为5页格式（p1-p5）

## 📞 问题反馈

如有问题，请检查：
1. API Key是否正确配置
2. 网络连接是否正常
3. 天行数据API额度是否充足（免费版100次/天）

# JD Link Converter 🛒🔗

> 将京东移动端分享短链接（3.cn / u.jd.com / item.m.jd.com）转换为 PC 端纯净商品链接（item.jd.com）

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://docs.openclaw.ac.cn/tools/skills)

---

## 功能特性

- **3.cn / u.jd.com 短链接解析** — 模拟京东 App UA 跟踪 302 重定向，获取真实商品页
- **移动端链接转 PC 端** — `item.m.jd.com/product/{id}.html` → `item.jd.com/{id}.html`
- **UTM 参数自动剥离** — 去除分享追踪参数，输出纯净链接
- **批量转换** — 一次性处理多个链接
- **零依赖** — 纯 Python 标准库，无需 pip install 任何第三方包
- **双模式** — 既可作为 OpenClaw/ClawHub 技能供 Agent 使用，也可作为 Python CLI 工具

## 安装

### 作为 OpenClaw 技能（Agent 自动使用）

```bash
# 通过 ClawHub 安装
clawhub install jd-link-converter

# 或通过 OpenClaw 安装
openclaw skills install jd-link-converter
```

### 作为 Python 包（开发者手动调用）

```bash
pip install jd-link-converter
```

## 使用方式

### CLI 命令行

```bash
# 单个链接转换
jd-convert "https://3.cn/2RKwn3-g"

# 多个链接批量转换
jd-convert "https://3.cn/2RKwn3-g" "https://item.m.jd.com/product/100120810291.html"

# 也可以直接使用 python 运行
python3 scripts/jd_link_converter.py "https://3.cn/2RKwn3-g"
```

### Python API

```python
from jd_link_converter import convert_jd_link

# 转换移动端链接
result = convert_jd_link("https://item.m.jd.com/product/100198170140.html?utm_source=iosapp")
print(result)
# {'original': '...', 'product_id': '100198170140', 'pc_url': 'https://item.jd.com/100198170140.html', 'error': None}

# 转换短链接（需要网络）
result = convert_jd_link("https://3.cn/2RKwn3-g")
print(result)
# {'original': '...', 'product_id': '100198170140', 'pc_url': 'https://item.jd.com/100198170140.html', 'error': None}
```

### 在 Agent 中使用

安装为 OpenClaw 技能后，当用户消息中出现京东链接或提到「京东链接转换」「3.cn解析」时，Agent 会自动：

1. 提取消息中的京东链接
2. 按类型分类（短链接 / 移动端 / PC端）
3. 短链接通过脚本解析，移动端/PC端直接正则提取
4. 输出 PC 端纯净商品链接

## 项目结构

```
jd-link-converter/
├── SKILL.md                    # OpenClaw 技能入口（Agent 执行协议）
├── scripts/
│   └── jd_link_converter.py    # 核心转换脚本（纯 Python 标准库）
├── references/
│   └── url_formats.md          # 京东 URL 格式参考文档
├── tests/
│   ├── __init__.py
│   └── test_converter.py      # 14 个单元测试
├── v1.0.0-backup/              # v1.0.0 版本备份
├── README.md                   # 本文件
├── pyproject.toml              # Python 包配置
├── LICENSE                     # MIT 许可证
└── .gitignore
```

## 技术要点

### 3.cn 短链接解析的关键

3.cn 短链接会根据请求的 User-Agent 进行不同的重定向：

| User-Agent | 重定向目标 |
|------------|-----------|
| `jdapp;iPhone;...` | ✅ 商品详情页 `item.m.jd.com/product/{id}.html` |
| 普通浏览器 UA | ❌ 京东首页 `www.jd.com` |

因此脚本使用京东 App 的 UA 字符串才能正确获取商品页 URL。

### 支持的链接类型

| 类型 | 格式 | 示例 |
|------|------|------|
| 3.cn 短链接 | `https://3.cn/{code}` | `https://3.cn/2RKwn3-g` |
| u.jd.com 短链接 | `https://u.jd.com/{code}` | `https://u.jd.com/abc123` |
| 移动端商品页 | `item.m.jd.com/product/{id}.html` | 含 UTM 追踪参数 |
| PC端商品页 | `item.jd.com/{id}.html` | 可含参数，转换时自动剥离 |
| 纯商品 ID | 6-12 位数字 | `100198170140` |

## 测试

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## 许可证

[MIT](LICENSE)

## 致谢

- 短链接解析思路参考：[CSDN - Firewall5788](https://blog.csdn.net/Firewall5788/article/details/120301954)
- OpenClaw 技能规范参考：[awesome-ai-persona-skills](https://github.com/momozi1996/awesome-ai-persona-skills)

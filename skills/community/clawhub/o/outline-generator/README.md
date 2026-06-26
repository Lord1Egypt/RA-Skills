# Outline Generator - 小说大纲生成器

根据小说类型、主题、字数生成 15 节拍结构化大纲的工具。专为 AutoNovel Writer v5.0 设计，由 Architect 代理在 Phase 1 使用。

## 安装

### 方式 1: 使用 pip（推荐）

```bash
# 从 PyPI 安装（如果发布）
pip install outline-generator

# 或从本地安装
cd ~/.openclaw/workspace/skills/outline-generator
pip install -e .
```

### 方式 2: 使用 requirements.txt

```bash
cd ~/.openclaw/workspace/skills/outline-generator
pip3 install -r requirements.txt --user
```

### 方式 3: 使用 OpenClaw ClawHub

```bash
# 从 ClawHub 安装
clawhub install outline-generator
```

## 快速开始

```bash
# 生成玄幻小说大纲
outline-generator --type 玄幻 --theme "修真世界" --word-count 1000000

# 或使用 Python 脚本
python3 -m scripts.generate_outline.py --type 玄幻 --theme "修真世界" --word-count 1000000
```

## 命令行选项

| 选项 | 说明 | 必填 |
|------|------|------|
| `--type, -t` | 小说类型（玄幻/都市/科幻/历史） | ✅ |
| `--theme, -m` | 小说主题（一句话简介） | ✅ |
| `--word-count, -w` | 目标总字数 | ✅ |
| `--output, -o` | 输出文件路径（默认：outline.md） | ❌ |
| `--config, -c` | 配置文件路径（默认：configs/types.yml） | ❌ |

## 支持的小说类型

| 类型 | 特点 | 字数范围 |
|------|------|----------|
| **玄幻** | 奇幻世界、修炼体系、秘境探险 | 80 万 -200 万字 |
| **都市** | 现代背景、职场商战、逆袭崛起 | 60 万 -150 万字 |
| **科幻** | 未来世界、星际旅行、人工智能 | 70 万 -180 万字 |
| **历史** | 穿越架空、权谋朝堂、战争争霸 | 60 万 -120 万字 |

## 15 节拍结构

采用改编自 Blake Snyder《Save the Cat》的 15 节拍结构：

### 第一幕：铺垫 (约 10%)
1. 开场画面
2. 主题呈现
3. 铺垫
4. 催化剂
5. 争执

### 第二幕：对抗 (约 80%)
6. 进入第二幕
7. 副线故事
8. 游戏时间
9. 中点
10. 坏人逼近
11. 失去一切
12. 灵魂黑夜
13. 进入第三幕

### 第三幕：解决 (约 10%)
14. 高潮
15. 终场画面

## 输出示例

```markdown
# 《修真世界》大纲

**类型**: 玄幻 | **主题**: 修真世界 | **目标字数**: 1,000,000 字

## 简介
少年林风因一场意外获得神秘传承，踏上修炼之路...

## 主要人物
- **林风** - 主角
- **苏媚** - 女主角
...

## 15 节拍结构
### 第一幕：铺垫
#### 1. 开场画面
林风在青石镇经营一家小药铺...
...
```

## 依赖

- **pyyaml>=6.0.1** - YAML 配置文件解析
- **rich>=13.7.0** - CLI 美化输出

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行代码质量检查
ruff check scripts/

# 运行测试
pytest tests/
```

## 许可证

MIT License

---

**Version**: 1.0.1  
**基于**: AutoNovel Writer v5.0 项目规划  
**作者**: OpenClaw Community

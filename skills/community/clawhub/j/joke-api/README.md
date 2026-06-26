# JokeAPI Skill

## 快速开始

### 使用 Bash 脚本

```bash
# 获取随机笑话
./scripts/joke.sh random

# 获取编程笑话
./scripts/joke.sh random -c Programming

# 获取双部分笑话
./scripts/joke.sh random -c Misc -t twopart

# 仅获取安全内容
./scripts/joke.sh random --safe-mode

# 获取 5 个笑话
./scripts/joke.sh random -a 5

# 搜索包含"programmer"的笑话
./scripts/joke.sh random --contains "programmer"

# 列出所有分类
./scripts/joke.sh categories

# 列出所有支持的语言
./scripts/joke.sh langs
```

### 使用 Python 脚本

```bash
# 获取随机笑话
python3 scripts/joke.py random

# 获取编程笑话
python3 scripts/joke.py random -c Programming

# 获取双部分笑话
python3 scripts/joke.py random -c Misc -t twopart

# 仅获取安全内容
python3 scripts/joke.py random --safe-mode

# 获取 5 个笑话
python3 scripts/joke.py random -a 5

# 列出所有分类
python3 scripts/joke.py categories

# 列出所有支持的语言
python3 scripts/joke.py langs
```

## 主要功能

- ✅ 免费无需 API 密钥
- ✅ 多种分类选择
- ✅ 支持多种语言
- ✅ 可过滤不当内容
- ✅ 单句或双部分笑话
- ✅ 多种响应格式

## 分类选项

- `Any` - 随机分类
- `Misc` - 杂项
- `Programming` - 编程
- `Dark` - 黑暗幽默
- `Pun` - 双关语
- `Spooky` - 恐怖
- `Christmas` - 圣诞

## 注意事项

⚠️ 使用 `--safe-mode` 或 `--blacklist` 过滤不当内容，特别是当笑话可能在工作场所或公共场合分享时。

## 相关链接

- [官方文档](https://jokeapi.dev/)
- [GitHub 仓库](https://github.com/Sv443-Network/JokeAPI)

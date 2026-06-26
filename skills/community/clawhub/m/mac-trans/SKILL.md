---
name: mac-trans
description: 翻译文本或者翻译文件内容的工具，支持多种语言翻译。使用方式：trans 命令
---

# mac-trans skill
用于文本内容，或者文件内容自动翻译，支持多种语言翻译。

## 安装
```bash
# 一行安装
brew search translate-shell
```

## 功能描述
支持自动中英文识别。

支持能力：
- 翻译用户输入的文本
- 翻译指定的全部文件内容
- 翻译文件内容中指定的行
- 翻译成指定语言，默认中英互译

## 使用方式
```bash
# 翻译文本。自动检测英文 → 中文，或者中文 → 英文
trans -e bing -b "要被翻译的文本内容"
# 举例子：翻译 "Hello world"
trans -e bing -b "Hello world"

# 翻译文件内容。自动检测英文 → 中文，或者中文 → 英文
trans -e bing -b "文件在mac中的路径"
# 举例子：翻译 ~/document.txt 文件内容
trans -e bing -b ~/document.txt

# 比如 翻译前 10 行
head -b -n 10 ～/document.txt | trans -e bing

# 翻译特定行
sed -n '5,20p' ~/document.txt | trans -e bing

# 可查询支持翻译成的语言。比如其中展示了某种语言，`Japanese         -   ja` 表示支持翻译成日文
trans -R -e bing
# 举例子：将 "Hello world" 翻译成日文
trans -e bing -b :ja "Hello world"
```

## 异常处理
- brew 未安装，则提示用户安装
- translate-shell 安装失败，则提醒用户自行安装
- 当用户没有提供完整地址，并且被翻译的文件找不到，则提示用户提供文件完整地址
- 当用户要求翻译的语言不在 trans 支持的列表中，则提示用户选择支持的语言





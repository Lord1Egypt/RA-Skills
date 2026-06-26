---
name: personal-toutiao-pub
description: 今日头条微头条自动发布工具。触发词："发布头条"、"发微头条"、"头条发布"
version: 1.0.0
---

# 今日头条发布工具

自动发布微头条到今日头条，支持复用本地 Chrome 登录态，支持智能等待登录。

## 功能特性

- ✅ **复用登录态**：连接本地 Chrome，无需重复登录
- ✅ **智能等待登录**：未登录时自动等待，登录成功后继续
- ✅ **智能内容扩展**：内容不足100字自动扩展
- ✅ **自动勾选选项**：自动勾选"个人观点，仅供参考"
- ✅ **支持图片上传**：可附带图片发布
- ✅ **截图保存**：发布成功后自动截图保存到桌面
- ✅ **支持文件输入**：可从文件读取长文本内容

## 触发方式

```
发布头条：今天天气真好
发微头条 今天学到了很多新知识
头条发布 "分享一个有趣的故事..."
```

## 使用方法

### 命令行使用

```bash
# 基本使用（发布默认内容）
python3 toutiao_publish.py

# 发布指定内容
python3 toutiao_publish.py "今天天气真好，心情也不错！"

# 从文件读取内容
python3 toutiao_publish.py -f content.txt

# 带图片发布
python3 toutiao_publish.py "内容" --image ~/Desktop/pic.jpg

# 使用无头模式（新浏览器）
python3 toutiao_publish.py "内容" --headless

# 未登录时不等待，直接退出
python3 toutiao_publish.py "内容" --no-wait
```

### 前置要求

**必须启动 Chrome 远程调试：**

```bash
# Mac
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222

# Linux
google-chrome --remote-debugging-port=9222
```

## 发布流程

1. 连接本地 Chrome 浏览器
2. 检查登录状态
   - **已登录**：直接进入发布页面
   - **未登录**：显示提示，自动等待登录（最长5分钟）
3. 打开发布页面
4. 输入内容（自动扩展到100字以上）
5. 上传图片（如提供）
6. 勾选发布选项：
   - 声明首发：头条首发（如存在）
   - 作品声明：个人观点，仅供参考
7. 点击发布按钮
8. 保存成功截图

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `content` | 发布内容 | `"今天天气很好"` |
| `-f, --file` | 从文件读取 | `-f post.txt` |
| `-i, --image` | 图片路径 | `--image pic.jpg` |
| `--headless` | 无头模式 | `--headless` |
| `--no-wait` | 不等待登录 | `--no-wait` |

## 智能等待登录

当检测到未登录时，脚本会：

1. 显示提示信息：
   ```
   ⏳ 等待登录...
   请在 Chrome 浏览器中完成登录
   登录成功后将自动继续...
   （最长等待 300 秒）
   ```

2. 每2秒检查一次登录状态

3. 检测到登录成功后自动继续发布流程

4. 超过5分钟未登录则超时退出

**使用 `--no-wait` 参数可禁用等待功能，未登录时直接退出。**

## 输出

- **成功截图**：`~/Desktop/toutiao_publish_success.png`
- **错误截图**：`~/Desktop/toutiao_error.png`

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 无法连接 Chrome | 确保 Chrome 已启动并开启 9222 端口 |
| 未检测到登录 | 在 Chrome 中访问 mp.toutiao.com 完成登录 |
| 等待登录超时 | 检查网络，重新运行脚本 |
| 找不到输入框 | 页面结构可能变化，检查错误截图 |
| 图片上传失败 | 检查图片路径和格式 |
| 发布失败 | 检查网络连接，查看错误截图 |

## 依赖

```bash
pip3 install playwright --break-system-packages
playwright install chromium
```

## 文件结构

```
skills/toutiao-publisher/
├── SKILL.md              # 本说明文件
└── toutiao_publish.py    # 主脚本
```

---
*Created: 2026-03-08*
*Updated: 2026-03-08（新增智能等待登录）*

---
name: instagram-downloader
description: 交互式下载 Instagram 用户内容（帖子/Reels/头像）。首次使用时会依次询问用户名、下载目录、Cookie路径、代理地址。
---

# Instagram Downloader Skill

## 使用流程

### 第一次使用：必须先询问用户以下 4 个参数

**按顺序询问，不要跳步：**

```
1️⃣ Instagram 用户名是什么？（不含 @）
2️⃣ 下载到哪个目录？（完整路径，如 D:\Downloads\Instagram）
3️⃣ Cookie 文件路径？（Netscape 格式，如 C:\Users\xxx\cookies_instagram.txt）
4️⃣ 代理地址？（可选，格式 http://host:port，留空则不使用代理）
```

收集完所有参数后，执行下载命令。

### 执行命令模板

```bash
gallery-dl --proxy "<代理地址>" --cookies "<cookie文件路径>" -D "<目标目录>" "https://www.instagram.com/<用户名>/"
```

> 注意：代理地址如果用户留空，则去掉 `--proxy` 参数

## 参数获取方式

### 1. Instagram 用户名
- 用户输入即可，例如：`fafa.0816`
- 主页链接可能是 `https://www.instagram.com/fafa.0816/`

### 2. 下载目录
- 必须是完整绝对路径
- Windows 示例：`D:\Instagram\fafa.0816`
- Linux/Mac 示例：`/home/user/downloads/instagram`
- gallery-dl 会在此目录下创建 `instagram/<用户名>/` 子目录

### 3. Cookie 文件路径（Netscape 格式）

#### 方法 A：用 yt-dlp 从 Chrome 导出
```bash
yt-dlp --cookies-from-browser chrome --cookies "cookies_instagram.txt" "https://www.instagram.com/"
```
然后把 `cookies_instagram.txt` 路径告诉 agent。

#### 方法 B：手动获取 sessionid
1. 浏览器登录 Instagram
2. F12 → Application → Cookies → 找 `sessionid`
3. 写成 `cookies_instagram.txt`：
```
# Netscape HTTP Cookie File
.instagram.com	TRUE	/	FALSE	1800000000	sessionid	你的sessionid值
.instagram.com	TRUE	/	TRUE	1800000000	csrftoken	你的csrftoken值
```

### 4. 代理地址（可选）
- 格式：`http://127.0.0.1:7890`
- 如果用户不需要代理，直接留空

## 下载类型说明

| URL 类型 | 下载内容 | 命令后缀 |
|---|---|---|
| `https://www.instagram.com/<用户>/` | 全部（帖子+reels+头像） | 不加后缀 |
| `https://www.instagram.com/<用户>/posts/` | 仅图片帖子 | `/posts/` |
| `https://www.instagram.com/<用户>/reels/` | 仅视频 | `/reels/` |
| `https://www.instagram.com/<用户>/avatar/` | 头像 | `/avatar/` |
| `https://www.instagram.com/p/<帖子ID>/` | 单个帖子 | 直接链接 |

## 完整执行示例

假设用户回答：
- 用户名：`fafa.0816`
- 下载目录：`D:\Downloads`
- Cookie：`C:\Users\栗子\cookies_instagram.txt`
- 代理：`http://127.0.0.1:7890`

执行：
```bash
gallery-dl --proxy "http://127.0.0.1:7890" --cookies "C:\Users\栗子\cookies_instagram.txt" -D "D:\Downloads" "https://www.instagram.com/fafa.0816/"
```

输出会写入 `D:\Downloads\instagram\fafa.0816\`

## 工具对比

| 工具 | 适用场景 | 注意 |
|---|---|---|
| **gallery-dl** | 首选，稳定支持 Instagram 全部类型 | 首选 |
| yt-dlp | 备选 | Instagram 支持已标为 broken |

## 常见错误处理

| 错误 | 原因 | 解决 |
|---|---|---|
| `401 Unauthorized` | Cookie 过期 | 重新获取 sessionid |
| `404 Not Found` | 用户不存在或私密 | 确认用户名正确 |
| `HttpError` 无权限 | Cookie 缺少必要字段 | 确保有 `sessionid` 和 `csrftoken` 两行 |
| SSL 警告 | 代理证书问题 | 加 `--no-check-certificate`（不推荐） |

## 隐私占位符清单

发布前检查：
- [ ] 代理地址 → 用 `<代理地址>` 占位
- [ ] Cookie 路径 → 用 `<cookie文件路径>` 占位
- [ ] 下载目录 → 用 `<目标目录>` 占位
- [ ] 用户名 → 用 `<用户名>` 占位

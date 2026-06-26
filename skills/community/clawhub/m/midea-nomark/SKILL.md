---
name: parse-video
description: "视频去水印解析 Skill。支持 20+ 平台短视频去水印解析，包括抖音、快手、小红书、微博、西瓜视频、豆包、云雀、B站等。使用本技能时触发：解析视频、去水印、视频解析、解析链接、下载视频、去除水印、parse video、video parser、抖音解析、快手解析、小红书解析、bilibili 解析、douyin kuaishou redbook weibo xigua doubao yunque bilibili"
---

# parse-video Skill

## 简介

跨平台视频去水印解析工具，支持 20+ 主流短视频和社交媒体平台。

### 支持平台

| 平台 | 域名 | 支持类型 |
|------|------|----------|
| 抖音 | v.douyin.com, www.iesdouyin.com | 视频/图集 |
| 快手 | v.kuaishou.com | 视频 |
| 小红书 | xhslink.com, www.xiaohongshu.com | 视频/图集/LivePhoto |
| 微博 | weibo.com, weibo.cn | 视频/图集 |
| 西瓜视频 | v.ixigua.com | 视频 |
| 哔哩哔哩 | bilibili.com, b23.tv | 视频 |
| 豆包 | www.doubao.com | 视频/图片 |
| 云雀 | xiaoyunque.jianying.com | 视频 |
| 更多... | ... | ... |

---

## 工作流程

### 方法一：一键解析（推荐）

使用 `scripts/parse.sh` 脚本，自动识别平台并解析：

```bash
# 解析任意视频分享链接
bash scripts/parse.sh "https://v.douyin.com/xxx"

# 解析豆包视频
bash scripts/parse.sh "https://www.doubao.com/video-sharing?share_id=xxx&video_id=xxx"

# 解析 B 站视频
bash scripts/parse.sh "https://b23.tv/xxx"
```

### 方法二：启动 HTTP 服务

```bash
# 启动服务（默认端口 8080）
bash scripts/serve.sh

# 指定端口
bash scripts/serve.sh 9090

# 服务启动后可访问 http://localhost:8080 查看 Web UI
```

### 方法三：直接使用 CLI

```bash
# 解析分享链接
./assets/parse-video-darwin-arm64 parse "https://v.douyin.com/xxx"

# 按视频 ID 解析
./assets/parse-video-darwin-arm64 id douyin 7424432820954598707

# 启动服务
./assets/parse-video-darwin-arm64 serve -p 8080
```

---

## 输出格式

解析成功后返回：
- **标题**: 视频描述/标题
- **作者**: 作者昵称和头像
- **视频地址**: 无水印的直接播放链接
- **封面地址**: 视频封面图
- **图片数量**: 图集图片数量（如有）

---

## 注意事项

1. 解析结果为临时链接，部分平台链接有时效性，建议及时下载
2. 仅供个人学习研究使用，请勿用于商业用途
3. 部分平台可能因接口调整而失效，我会定期更新

---

## 技术细节

- **二进制位置**: `assets/parse-video-<os>-<arch>`
- **适用系统**: macOS (arm64/amd64), Windows (amd64), Linux
- **二进制来源**: 本地编译，无第三方依赖

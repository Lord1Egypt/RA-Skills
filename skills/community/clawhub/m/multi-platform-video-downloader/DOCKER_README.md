# Video Downloader Docker 使用指南

## 快速开始

### 1. 构建镜像

```bash
docker build -t video-downloader .
```

### 2. 下载视频

```bash
# 下载单个视频
docker run -v $(pwd)/downloads:/app/downloads video-downloader "https://www.douyin.com/video/xxx"

# 批量下载
docker run -v $(pwd)/downloads:/app/downloads video-downloader \
  -u "https://www.douyin.com/video/xxx" \
  -u "https://www.bilibili.com/video/yyy"

# 搜索下载（抖音）
docker run -v $(pwd)/downloads:/app/downloads video-downloader \
  "美女" --search --count 5
```

### 3. 查看下载的文件

下载的视频会保存在当前目录的 `downloads` 文件夹中。

## 参数说明

与原版脚本参数相同：
- `url_or_keyword` - 视频 URL 或搜索关键词
- `-u, --url` - 视频 URL（可多次使用）
- `-s, --search` - 启用搜索模式
- `-n, --count` - 下载数量（默认 5）
- `-o, --output` - 输出目录（Docker 中默认为 /app/downloads）
- `-b, --browser` - 强制使用浏览器模式

## 示例

```bash
# 下载 YouTube 视频
docker run -v $(pwd)/downloads:/app/downloads video-downloader \
  "https://www.youtube.com/watch?v=xxx"

# 下载 Bilibili 视频
docker run -v $(pwd)/downloads:/app/downloads video-downloader \
  "https://www.bilibili.com/video/BVxxx"
```

## 注意事项

- 首次运行会下载 Chrome 浏览器（DrissionPage 自动处理）
- 下载的视频会保存在挂载的 volumes 中
- 支持所有原脚本支持的平台

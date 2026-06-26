# YouTube

## 常用模式

### 搜索
```bash
opencli youtube search "rust"
```

### 视频元数据
```bash
opencli youtube video "https://www.youtube.com/watch?v=xxx"
```

### 字幕 / 转录
```bash
opencli youtube transcript "https://www.youtube.com/watch?v=xxx"
opencli youtube transcript "xxx" --lang zh-Hans --mode raw
```

## 最小说明

- 搜索依赖浏览器登录态。
- transcript 支持 `--lang` 指定语言和 `--mode raw` 输出原始时间戳。

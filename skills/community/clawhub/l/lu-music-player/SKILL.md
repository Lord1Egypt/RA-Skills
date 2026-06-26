# lu-music-player

Mopidy 音乐播放器管理技能 - 帮助你管理和控制 NAS 上的 Mopidy 音乐服务。

## 描述

这个技能提供 Mopidy 音乐播放器的管理功能，包括：
- 查看播放状态
- 控制播放/暂停/跳过
- 音量调节
- 扫描本地音乐
- 查看播放列表

## 触发条件

当用户提到以下关键词时激活：
- "mopidy"
- "音乐播放器"
- "播放音乐"
- "暂停音乐"
- "下一首"
- "音量"
- "扫描音乐"

## 用法

### 查看播放状态
```
mopidy 状态
音乐播放器状态
当前播放什么
```

### 控制播放
```
播放音乐
暂停音乐
下一首
上一首
```

### 音量控制
```
音量调到 50
音量加 10
音量减 10
静音
```

### 音乐库管理
```
扫描本地音乐
刷新音乐库
查看播放列表
```

## 示例对话

**用户**: mopidy 状态怎么样？
**助手**: Mopidy 音乐播放器运行正常！当前状态：空闲。访问 http://192.168.3.26:6680/iris 查看 Web 界面。

**用户**: 播放音乐
**助手**: 已打开 Mopidy Web 界面：http://192.168.3.26:6680/iris 你可以在 Iris 界面中选择歌曲播放。

**用户**: 扫描本地音乐
**助手**: 请在 Iris 界面中：Settings → Local Music → Scan 扫描本地音乐库。或者执行命令：`docker exec mopidy mopidy local scan`

## 配置

### 环境变量（可选）
```bash
MOPIDY_URL=http://192.168.3.26:6680
MOPIDY_IRIS_URL=http://192.168.3.26:6680/iris
```

### Docker 命令
```bash
# 查看状态
docker ps | grep mopidy

# 查看日志
docker logs mopidy --tail 50

# 重启服务
docker-compose restart mopidy

# 扫描本地音乐
docker exec mopidy mopidy local scan
```

## 访问地址

| 服务 | 地址 |
|------|------|
| **Mopidy Iris** | http://192.168.3.26:6680/iris |
| **Mopidy HTTPS** | https://music.jesson.online:1443/iris |

## 故障排查

### 音乐播放器无法访问
1. 检查容器状态：`docker ps | grep mopidy`
2. 查看日志：`docker logs mopidy --tail 50`
3. 重启服务：`docker-compose restart mopidy`

### 无法播放本地音乐
1. 确保音乐文件在 `/vol1/1000/Docker/music-player/music/` 目录
2. 在 Iris 界面扫描：Settings → Local Music → Scan
3. 检查文件权限：`chmod -R 777 /vol1/1000/Docker/music-player/music/`

## 作者

- **作者**: jesson1222-ship-it
- **版本**: 1.0.0
- **创建时间**: 2026-03-08
- **许可证**: MIT

## 更新日志

### v1.0.0 (2026-03-08)
- 初始版本
- 支持 Mopidy 状态查看
- 支持播放控制
- 支持音量调节
- 支持音乐库扫描

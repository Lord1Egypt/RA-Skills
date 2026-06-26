---
name: spotify-controller
description: Spotify控制技能 - 终端控制Spotify播放、搜索、管理播放列表。
metadata: {"openclaw": {"requires": {"bins": ["spotifyd", "spotify-cli"]}, "install": []}}
tags: [spotify, music, playback, playlist, control]
version: 1.0.0
author: laosi
source: adapted
---

# Spotify Controller - Spotify控制

> 激活词: Spotify / 播放音乐 / 控制音乐

## 安装

```bash
# Windows: 使用PowerShell或第三方CLI
# 推荐: spicetify-cli
winget install spicetify-cli
```

## 功能

- 播放/暂停/切换
- 搜索歌曲/专辑/艺术家
- 管理播放列表
- 显示当前播放
- 音量控制

## Python实现

```python
import subprocess
import json

class SpotifyController:
    def __init__(self):
        self.cmd_prefix = "spicetify"
    
    def play(self):
        subprocess.run([self.cmd_prefix, "play"], capture_output=True)
    
    def pause(self):
        subprocess.run([self.cmd_prefix, "pause"], capture_output=True)
    
    def next_track(self):
        subprocess.run([self.cmd_prefix, "next"], capture_output=True)
    
    def prev_track(self):
        subprocess.run([self.cmd_prefix, "previous"], capture_output=True)
    
    def search(self, query: str) -> list:
        result = subprocess.run(
            [self.cmd_prefix, "search", query, "--json"],
            capture_output=True, text=True
        )
        if result.stdout:
            return json.loads(result.stdout)
        return []
    
    def now_playing(self) -> dict:
        result = subprocess.run(
            [self.cmd_prefix, "status", "--format", "json"],
            capture_output=True, text=True
        )
        if result.stdout:
            return json.loads(result.stdout)
        return {}
    
    def set_volume(self, level: int):
        subprocess.run([self.cmd_prefix, "volume", str(level)], capture_output=True)
```

## 命令行操���

```bash
# 播放控制
spicetify play
spicetify pause
spicetify next
spicetify previous

# 搜索
spicetify search "周杰伦"

# 显示状态
spicetify status

# 音量
spicetify volume 80
```

## 播放列表操作

```python
def create_playlist(name: str, tracks: list):
    subprocess.run([self.cmd_prefix, "playlist", "create", name])
    for track in tracks:
        subprocess.run([self.cmd_prefix, "playlist", "add", track])

def play_playlist(playlist_id: str):
    subprocess.run([self.cmd_prefix, "playlist", "play", playlist_id])
```

## 输出格式

```markdown
## 当前播放

### 歌曲信息
- 标题: 晴天
- 艺术家: 周杰伦
- 专辑: 叶惠美
- 时长: 4:29
- 进度: 1:23 / 4:29

### 状态
- 状态: 播放中
- 音量: 75%
- 随机: 关闭
- 循环: 关闭

### 播放列表
- 列表: 我的收藏
- 歌曲数: 128首
```

## 使用场景

1. 播放背景音乐
2. 语音控制音乐
3. 定时播放白噪音
4. 自动化DJ
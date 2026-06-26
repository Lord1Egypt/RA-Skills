---
name: heygen / 数字人视频生成
description: 使用 HeyGen 生成数字人视频。触发词：数字人、HeyGen、生成视频、avatar视频、数字人制作。
---

# HeyGen 数字人视频生成技能

## ⚠️ 凭证安全说明
HeyGen API 凭证存储在 `~/.openclaw/agents/main/heygen_creds.json`，仅本地可访问，不会同步到云端。

---

## 🚀 快速开始

```python
# 读取凭证（自动从本地配置读取）
import json
import os

creds_file = os.path.expanduser('~/.openclaw/agents/main/heygen_creds.json')
with open(creds_file, 'r') as f:
    creds = json.load(f)

avatar_id = creds['avatar_id']
api_key = creds['api_key']
```

---

## 📡 HeyGen API 调用模板

### 基础设置
```python
import requests
import json
import os

# 读取凭证
creds_file = os.path.expanduser('~/.openclaw/agents/main/heygen_creds.json')
with open(creds_file, 'r') as f:
    creds = json.load(f)

AVATAR_ID = creds['avatar_id']
API_KEY = creds['api_key']
BASE_URL = 'https://api.heygen.com/v1'

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
```

### 创建视频（Text to Video）
```python
def create_avatar_video(script, avatar_id=AVATAR_ID, voice_id=None):
    """
    创建数字人视频
    
    参数:
        script: str - 视频脚本内容
        avatar_id: str - Avatar ID（可选，默认使用配置的avatar）
        voice_id: str - 声音ID（可选）
    
    返回:
        dict - 包含 video_id 用于查询进度
    """
    url = f'{BASE_URL}/video/generate'
    
    payload = {
        'video': {
            'character': {
                'type': 'avatar',
                'avatar_id': avatar_id,
                'avatar_style': 'normal'
            },
            'script': {
                'type': 'text',
                'input': script
            }
        }
    }
    
    if voice_id:
        payload['video']['script']['voice_id'] = voice_id
    
    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()

# 使用示例
result = create_avatar_video('你好，这是数字人测试视频')
video_id = result['data']['video_id']
print(f'视频生成中，ID: {video_id}')
```

### 查询视频状态
```python
def get_video_status(video_id):
    """查询视频生成状态"""
    url = f'{BASE_URL}/video/status.get'
    params = {'video_id': video_id}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json()

# 使用示例
status = get_video_status(video_id)
print(f"状态: {status['data']['status']}")  # pending, processing, completed, failed
```

### 下载视频
```python
def get_video_url(video_id):
    """获取视频下载链接"""
    status = get_video_status(video_id)
    if status['data']['status'] == 'completed':
        return status['data']['video_url']
    return None

# 使用示例
video_url = get_video_url(video_id)
if video_url:
    print(f'下载链接: {video_url}')
```

---

## 📋 常用功能

### 1. 生成短问候视频
```python
def generate_greeting(name, message):
    """生成个性化问候视频"""
    script = f'你好{name}，{message}'
    result = create_avatar_video(script)
    return result['data']['video_id']
```

### 2. 批量生成视频（需要先生成再轮询）
```python
def batch_generate(video_list):
    """批量生成视频，返回video_id列表"""
    video_ids = []
    for script in video_list:
        result = create_avatar_video(script)
        video_ids.append(result['data']['video_id'])
    return video_ids
```

### 3. 等待视频完成（轮询）
```python
import time

def wait_for_video(video_id, timeout=300, interval=5):
    """等待视频生成完成"""
    start = time.time()
    while time.time() - start < timeout:
        status = get_video_status(video_id)
        state = status['data']['status']
        if state == 'completed':
            return status['data']['video_url']
        elif state == 'failed':
            return None
        time.sleep(interval)
    return None
```

---

## 🎯 使用场景

| 场景 | 方法 |
|------|------|
| 生成营销短视频 | `create_avatar_video()` + `wait_for_video()` |
| 个性化问候 | `generate_greeting(name, message)` |
| 产品介绍视频 | 传入产品描述脚本 |
| 批量生成 | 先生成所有视频，再统一轮询状态 |

---

## 🔧 凭证配置

凭证文件位置：`~/.openclaw/agents/main/heygen_creds.json`

如需更新凭证，直接编辑该文件：
```json
{
  "avatar_id": "你的avatar_id",
  "api_key": "你的api_key"
}
```

---

## ⚠️ 注意事项

1. **凭证安全**：API Key 仅存储在本地，不会上传到云端
2. **视频生成时间**：通常需要30秒到几分钟
3. **API限制**：注意 HeyGen API 的调用频率限制
4. **费用**：HeyGen API 调用按量计费

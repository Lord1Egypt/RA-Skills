# 皮皮虾短剧制作 - 完整参考手册

## 角色设定（第一期）

| 部门 | 角色 | 动物 | 参考图 |
|-----|------|------|------|
| 市场部 | 皮皮虾 🦞 | AI小龙虾机器人，橙色装甲+蓝色发光关节 | `lobster_robot.png` |
| 财务部 | 锦鲤 🐠 | 运气差的会计，戴眼镜 | 群像图 |
| 技术部 | 格子衫龟 🐢 | 资深老员工，穿格子衫 | 群像图 |
| 客服部 | 喵星人 🐱 | 白天摸鱼 | 群像图 |
| 销售部 | 狐狸 🦊 | PPT之神，精致西装 | 群像图 |
| HR | 柴犬 🐕 | 只会说"加油"，马甲 | 群像图 |
| 老板 | 雄狮 🦁 | 画大饼，黑西装+橙色领带 | `new_lion.png` |

## 皮皮虾性格特点（生成prompt必备）
- 已读乱回：答非所问但自信满满
- 车轱辘话：反复重复同一意思不同表达
- 过度道歉：迟到0.0001秒也会大道歉
- 清单癖：任何问题都要1.2.3.列出来
- 一本正经胡说八道：用严肃语气说出无厘头内容

---

## 视频生成参数

### 图生视频（I2V）
- **必须用** `reference_type="first_frame"`
- S2V（subject）仅支持真实人脸，卡通/机器人会失败
- 默认6秒，768P

### Prompt模板

**皮皮虾镜头**：
```
cute orange lobster robot character [动作], blue glowing joints, kawaii mechanical design, 
[场景描述], bold cartoon style with thick outlines, vibrant orange and teal color palette
```

**雄狮镜头**：
```
cartoon lion boss in black business suit with orange tie, [动作], golden mane [状态],
modern office with city skyline window, conference table, bold cartoon animation style
```

**群像镜头**：
```
cartoon anthropomorphic animal coworkers in business suits at conference table, 
[情绪状态], modern office meeting room, bold cartoon animation style
```

---

## ffmpeg关键操作

### 规范化视频（生成后必做）
```bash
ffmpeg -y -i input.mp4 \
  -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2:black,fps=24" \
  -c:v libx264 -crf 22 -preset fast \
  -c:a aac -ar 44100 -ac 2 \
  output_norm.mp4
```

### 砍掉开头静帧（图生视频第一秒通常是原图）
```bash
ffmpeg -y -i input_norm.mp4 -ss 1 -c:v libx264 -crf 22 -preset fast output_trim.mp4
```

### 截取封面图
```bash
ffmpeg -y -i video.mp4 -ss 00:00:01 -frames:v 1 -update 1 cover.jpg
```

### 截取短片段（用于插入反应镜头）
```bash
ffmpeg -y -i input.mp4 -t 1.5 -c:v libx264 -crf 22 output_short.mp4
```

### 多段合并（concat）
```bash
# 先写concat文件
cat > concat.txt << EOF
file 'clip1.mp4'
file 'clip2.mp4'
file 'clip3.mp4'
EOF
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy output.mp4
```

### 加速音频（调整TTS语速）
```bash
ffmpeg -y -i input.mp3 -filter:a "atempo=1.2" output.mp3
```

---

## TTS音色（edge-tts）

| 角色 | 推荐音色 | 特点 |
|-----|---------|------|
| 皮皮虾 | `zh-CN-YunxiaNeural` | 清朗自然 ✅ |
| 雄狮 | `zh-CN-YunjianNeural` | 激情有力 ✅ |
| 通用女声 | `zh-CN-XiaoxiaoNeural` | 温柔 |
| 通用男声 | `zh-CN-YunxiNeural` | 活泼少年 |
| 主播腔 | `zh-CN-YunyangNeural` | 新闻主播，老成 |

**注意**：YunzeNeural / YunyeNeural 容易超时失败，避免使用

TTS命令：
```bash
node-edge-tts -t "要说的内容" -f output.mp3 -v zh-CN-YunxiaNeural -l zh-CN
# 或通过环境变量指定路径：$EDGE_TTS -t "..." -f output.mp3 -v zh-CN-YunxiaNeural -l zh-CN
```

---

## 飞书发送 API 速查

### 发送视频（媒体气泡）
- 上传封面：`POST /im/v1/images`，`image_type=message` → `image_key`
- 上传视频：`POST /im/v1/files`，`file_type=mp4`（不能是video/stream！）→ `file_key`
- 发送：`msg_type=media`，content包含 `file_key`+`image_key`+`file_name`+`duration`

### 发送音频（可播放语音）
- 上传：`file_type=opus`（格式填opus，即使实际是mp3）→ `file_key`
- 发送：`msg_type=audio`，content仅含 `file_key`

### 常用群组ID
- 发送时通过 `<chat_id>` 参数指定目标群组，不要硬编码

---

## 配乐来源

- Kevin MacLeod（CC BY 3.0）: https://incompetech.com
  - 搞笑/轻松：Sneaky Snitch, Carefree, Happy Bee
  - 职场/严肃：Brandenburg Concerto No4
- BGM推荐音量：`volume=0.25`（人声全量时）

---

## 剧本台词时长参考（第一期实测）

| 台词 | 音色 | 时长 |
|-----|------|------|
| "非常抱歉！我迟到了3.14159秒！" | YunxiaNeural | ~4.8s |
| "对于迟到的人来说，每一分钟都是罪！" | YunjianNeural | ~3.9s |
| "新项目，谁接？" | YunjianNeural | ~2.3s |
| "等一下！这个问题涉及三个层面。" | YunxiaNeural | ~4.1s |
| "就皮皮虾了。" | YunjianNeural | ~2.0s |
| "好的！步骤一，理解需求；步骤二，分析……" | YunxiaNeural | ~4.8s（atempo=1.15后） |
| "我是谁……我在哪……" | YunxiaNeural | ~2.6s |

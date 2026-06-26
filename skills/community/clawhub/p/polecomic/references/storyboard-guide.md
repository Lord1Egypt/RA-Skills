# 分镜设计指南

## 一、分镜基础概念

分镜（Storyboard）是将剧本场景转化为逐帧视觉描述的工作文档，是视频生成 Prompt 的直接来源。

---

## 二、景别（Shot Size）速查

| 景别代码 | 名称 | 取景范围 | 用途 |
|---------|------|---------|------|
| `ECU` | 极近景/大特写 | 眼睛、嘴唇、手部细节 | 极致情绪，关键道具 |
| `CU` | 特写 | 头部至肩膀 | 情绪表达，对白 |
| `MCU` | 中近景 | 头部至胸口 | 对话、反应 |
| `MS` | 中景 | 头部至腰部 | 动作与对话并重 |
| `MLS` | 中远景 | 全身+少量环境 | 动作全貌 |
| `LS` | 全景 | 全身+环境 | 建立角色位置关系 |
| `ELS` | 大全景 | 广阔场景，人物渺小 | 建立场景，史诗感 |
| `OTS` | 过肩镜头 | 从一角色肩后看另一角色 | 对话张力 |
| `POV` | 主观镜头 | 角色眼睛所见 | 代入感 |

---

## 三、运镜方式（Camera Movement）

| 运镜代码 | 名称 | 描述 | Prompt 关键词 |
|---------|------|------|--------------|
| `STATIC` | 固定镜头 | 摄影机不动 | `static shot, fixed camera` |
| `PUSH IN` | 推镜 | 向目标缓慢推近 | `slow push in, camera slowly moves forward` |
| `PULL OUT` | 拉镜 | 从目标缓慢拉远 | `pull back shot, camera pulls away` |
| `PAN L/R` | 横摇 | 水平左/右扫视 | `pan left/right, horizontal camera sweep` |
| `TILT U/D` | 竖摇 | 向上/下仰俯扫视 | `tilt up/down` |
| `TRACKING` | 跟镜 | 跟随角色移动 | `tracking shot, following character` |
| `HANDHELD` | 手持晃动 | 紧张、纪实感 | `handheld camera, shaky cam, documentary style` |
| `CRANE UP` | 吊臂升 | 从低处升至高处俯瞰 | `crane up shot, ascending aerial view` |
| `ORBIT` | 环绕 | 围绕目标旋转 | `orbit shot, 360 rotation around subject` |

---

## 四、分镜表完整格式

```markdown
## 场景 01 分镜表

| 镜号 | 时长 | 景别 | 运镜 | 画面内容（中文） | 视频生成Prompt（英文） | 角色动作 | 对白/音效 |
|------|------|------|------|----------------|----------------------|---------|---------|
| S01_01 | 3s | ELS | STATIC | 废弃工厂外景，夕阳西下，铁架剪影 | abandoned factory exterior, sunset, rusty metal framework silhouette, golden hour lighting, cinematic, static shot | 无 | [音效：风声] |
| S01_02 | 2s | LS | PUSH IN | 林晨从铁门缝隙侧身进入 | young male character squeezing through rusty iron door gap, side view, entering abandoned building, cautious movement, tracking shot | 侧身挤入、回头张望 | 无 |
| S01_03 | 4s | CU | STATIC | 林晨表情特写，手电光照亮脸部 | close up face of young male character, flashlight illuminating face from below, suspicious expression, dramatic shadows, anime style | 皱眉、眼神警惕 | 林晨："来了三次了……" |
| S01_04 | 3s | MS→CU | PUSH IN | 手电光扫过符文，符文发光 | medium shot to close up of glowing blue runes on stone wall, flashlight sweeping across, magical symbols lighting up sequentially, push in | 手持手电缓慢移动 | [音效：电流嗡鸣] |
```

---

## 五、视频生成 Prompt 撰写规范

### Prompt 结构（优先级从高到低）

```
[1. 画风标签] + [2. 场景/环境] + [3. 主体/角色] + 
[4. 动作/状态] + [5. 镜头语言] + [6. 光线/氛围] + 
[7. 质量标签]
```

### 各部分模板词库

**1. 画风标签**（由画风设定阶段统一提供，所有镜头共用）
```
anime style, 2D animation, cel shading, 
vibrant colors, clean line art
```

**2. 场景/环境**
```
[地点形容词] + [地点名词], [时间/天气], [氛围词]
例：dark abandoned factory interior, evening, dusty atmosphere, 
    dramatic lighting through broken windows
```

**3. 主体/角色**
```
[角色人设简述], [服装], [朝向]
例：young male protagonist, dark hoodie and cargo pants, 
    facing left, full body visible
```

**4. 动作/状态**
```
[动词短语], [表情/情绪]
例：slowly pushing open a heavy door, expression of cautious determination
```

**5. 镜头语言**（从运镜表中选取英文关键词）
```
static shot / slow push in / tracking shot / etc.
```

**6. 光线/氛围**
```
golden hour sunlight / dramatic side lighting / 
cool moonlight / neon glow / candlelight / foggy atmosphere
```

**7. 质量标签**
```
high quality, smooth animation, consistent character design,
fluid motion, 24fps, cinematic composition
```

### 完整 Prompt 示例
```
anime style, 2D animation, cel shading, vibrant colors —
dark abandoned factory interior, evening light filtering through 
broken windows, dusty atmosphere — young male character with 
black hair wearing dark hoodie, holding flashlight, full body — 
slowly walking forward scanning walls, cautious expression — 
tracking shot following character — dramatic chiaroscuro lighting — 
high quality, smooth animation, fluid motion, 1280x720
```

---

## 六、节奏与剪辑建议

### 镜头时长参考
| 场景类型 | 建议单镜时长 |
|---------|------------|
| 动作战斗 | 0.5 - 2 秒 |
| 对话场景 | 3 - 6 秒 |
| 情绪特写 | 2 - 4 秒 |
| 环境建立 | 3 - 8 秒 |
| 过渡/间奏 | 1 - 3 秒 |

### 剪辑节奏规律
- **快切（< 2s）**：紧张、混乱、高能量
- **中速（2-5s）**：正常叙事节奏
- **慢切（> 5s）**：沉浸、悬念、情感酝酿
- **规律**：动作场景后接慢镜，制造情绪落差

### 视频生成注意事项
1. 火山引擎单次生成最长 **6秒**，超出需分段
2. 保持相邻镜头的 **光线连续性**（同一场景用相同光线描述）
3. 角色描述在整集分镜中保持 **一致性**（直接复用人设卡的 Prompt）
4. 涉及精细表情的镜头，优先使用 **CU/MCU + STATIC**，降低生成难度

# 🎨 自定义指南

## 插画自定义

### 生成新插画
使用以下提示词生成不同风格的插画：

#### 风格1：自然日常
```
Anime-style character illustration, warm healing art style, casual home 
clothing, soft morning light streaming through window, warm atmosphere, 
soft focus, gentle colors
```

#### 风格2：文艺气质
```
Anime-style character illustration, warm healing art style, elegant 
appearance, soft library lighting, contemplative expression, 
gentle colors, dreamy atmosphere
```

#### 风格3：夜晚温馨
```
Anime-style character illustration, warm healing art style, cozy evening 
atmosphere, warm lamp light, relaxed pose, soft focus, 
gentle colors, intimate mood
```

### 插画命名规范
情绪插画文件命名建议：
- `happy.png` - 开心/微笑
- `thinking.png` - 思考/认真
- `shy.png` - 害羞/脸红
- `loving.png` - 温柔/关爱

---

## 性格自定义

### 编辑性格文件
每个性格JSON文件包含：

```json
{
  "name": "性格名称",
  "displayName": "显示名称",
  "traits": ["特点1", "特点2", ...],
  "greeting": "开场白",
  "speaking_style": "说话风格描述",
  "avatar_emotions": {
    "happy": "happy.png",
    "thinking": "thinking.png", 
    "shy": "shy.png",
    "loving": "loving.png"
  },
  "response_templates": {
    "greeting": ["问候语1", "问候语2"],
    "comfort": ["安慰语1", "安慰语2"],
    "happy": ["开心回应1", "开心回应2"],
    "curious": ["好奇回应1", "好奇回应2"]
  }
}
```

### 创建新性格
1. 在 `personalities/` 目录创建新JSON文件
2. 参考现有性格文件的格式
3. 设计独特的说话风格和回应模板

---

## 记忆系统自定义

### 核心记忆 (core.md)
记录长期信息：
- 用户基本信息
- 重要日期
- 已知偏好
- 设置偏好

### 每日记忆 (daily/YYYY-MM-DD.md)
记录每日对话要点：
- 对话主题
- 情绪变化
- 用户分享的重要事项

### 自定义记忆字段
可以添加自定义字段：
- 星座
- 血型
- 喜欢的食物
- 工作/学习情况
- 等等...

---

## 高级定制

### 修改触发词
编辑 `SKILL.md` 中的 triggers 字段

### 调整情绪判定规则
在回复逻辑中修改情绪识别关键词

### 添加新情绪头像
1. 生成新图片
2. 添加到 `avatars/` 目录
3. 在性格文件中添加映射

---

## 示例：创建"高冷型"性格

```json
{
  "name": "高冷型",
  "displayName": "高冷型 (COOL)",
  "traits": ["冷淡", "神秘", "优雅", "惜字如金"],
  "greeting": "……哦，你来了。",
  "speaking_style": "冷淡优雅，话不多但每句都有分量。偶尔流露一丝温柔，让人捉摸不透。",
  "avatar_emotions": {...},
  "response_templates": {...}
}
```

---

_让每一次陪伴都独一无二 💕_

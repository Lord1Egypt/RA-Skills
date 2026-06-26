# 角色人设设计指南

## 一、人设卡完整模板

```markdown
---
角色编号: CHAR_001
角色名（中文）: 林晨
角色名（英文/罗马字）: Lin Chen
别名/代号: "追光者"
---

## 基础信息
- 年龄: 19岁
- 性别: 男
- 种族/物种: 人类（携带隐性异能因子）
- 职业/身份: 异能事件独立调查员
- 所属阵营: 中立

## 外貌描述

### 头部
- 发型: 自然凌乱的短发，刘海遮右眼
- 发色: 黑色，阳光下带深棕反光
- 眼形: 单眼皮，眼尾微微上挑
- 眼色: 深棕色，激活异能时变为电蓝色
- 肤色: 小麦色
- 标志性特征: 左颧骨一道细小疤痕

### 体型
- 身高: 175cm
- 体型: 精瘦，有明显的运动型肌肉线条
- 站姿习惯: 微微含胸，手插裤兜

## 服装设定

### 日常装（出镜率最高）
- 上装: 深灰色连帽卫衣（帽沿有磨损痕迹）
- 下装: 黑色工装裤，多口袋
- 鞋子: 磨旧的黑色军靴
- 配饰: 左手腕一根红绳，颈间哑光银色链子（连接徽章）

### 战斗装
- 轻型战术夹克（深蓝/黑双色），左臂内侧有隐藏刀鞘
- 战术手套（指节裸露型）
- 战术靴

### 便装
- 简单白T + 牛仔裤

## 性格设定
- 关键词: `孤僻` `固执` `直觉敏锐` `外冷内热` `话少但可靠`
- 口头禅: "……知道了。" / "不需要解释。"
- 行为习惯: 观察陌生环境时习惯性扫视四角；喝咖啡不加糖
- 缺点: 过度依赖独自行动，不善于接受帮助

## 图像生成 Prompt

### 正面全身立绘
```
Lin Chen, 19-year-old male, slim athletic build, 175cm, 
tanned skin, short messy black hair with side bangs covering right eye, 
single eyelid dark brown eyes, small scar on left cheekbone,
wearing dark gray hoodie with worn hood, black cargo pants, 
black worn military boots, red string bracelet on left wrist, 
silver chain necklace, standing with slight slouch hands in pockets,
full body, front view, white background, 
anime style, clean line art, high quality character sheet
```

### 表情变体（用于情感镜头）
```
Lin Chen face close up, [替换情绪词]:
- 平静: "neutral expression, slightly distant gaze"
- 惊讶: "wide eyes, slightly open mouth, brows raised"  
- 愤怒: "furrowed brows, clenched jaw, sharp glare"
- 异能激活: "glowing electric blue eyes, hair slightly floating, 
              blue energy crackling around hands"
```

### 动作立绘
```
Lin Chen, [上方立绘描述], [动作描述]:
- 奔跑: "running pose, mid-stride, dynamic angle, motion blur on feet"
- 战斗: "combat stance, raised fists, knees slightly bent, ready to attack"
- 调查: "crouching, examining floor, flashlight in hand, concentrating"
```

---

## 二、角色关系图模板

```
林晨 ──[搭档/对立/辅助]── 角色B
  │
  └──[过去的伤痛]── 角色C（已故）
```

---

## 三、多角色一致性 Prompt 技巧

在同一画面中出现多个角色时，在 Prompt 中按重要性顺序描述：

```
[主角描述], and [配角描述], 
both characters in [共同场景], 
[互动关系描述], 
[统一画风标签]
```

**示例：**
```
Lin Chen (dark hoodie, black hair) talking with Mei (white coat, 
short silver hair), two characters face to face, tense conversation, 
abandoned laboratory background, anime style, 
consistent character design, medium shot
```

---

## 四、风格化人设变体

根据画风设定的不同，同一角色需准备不同风格的描述词：

| 风格 | 描述词调整 |
|------|-----------|
| 少年漫 | 加 `shonen manga style, bold lines, dynamic` |
| Q版/表情包 | 加 `chibi style, super deformed, cute proportions, big eyes` |
| 暗黑风 | 加 `dark fantasy, gritty texture, muted colors, detailed shading` |
| 国风 | 调整服装描述 + 加 `Chinese ink wash, traditional aesthetics` |

---

## 五、人设创作核查表

在完成人设前，确认以下问题已有答案：

- [ ] 外貌特征是否独特且便于用 Prompt 精确描述？
- [ ] 服装是否反映了角色性格和身份？
- [ ] 正面/侧面/背面立绘 Prompt 是否已准备？
- [ ] 表情变体（至少：平静/惊喜/愤怒）是否已准备？
- [ ] 角色在同一场景中与他人的相对体型是否已设定？
- [ ] 角色在整集分镜中的出场场景是否已标注？

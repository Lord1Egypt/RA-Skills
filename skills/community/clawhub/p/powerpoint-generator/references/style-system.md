# 风格系统

## 风格数据模型

每套风格由以下字段定义：

```json
{
  "style_name": "风格名称",
  "style_id": "dark_tech | xiaomi_orange | blue_white | royal_red | fresh_green | luxury_purple | minimal_gray | vibrant_rainbow | gradient_blue | warm_sunset | nordic_white | cyber_punk | elegant_gold | ocean_depth | retro_film | corporate_blue",
  "background": {
    "primary": "#色值",
    "gradient_to": "#色值"
  },
  "card": {
    "gradient_from": "#色值",
    "gradient_to": "#色值",
    "border": "rgba(...)",
    "border_radius": 12
  },
  "text": {
    "primary": "#色值",
    "secondary": "rgba(...)",
    "title_size": 28,
    "body_size": 14,
    "card_title_size": 20
  },
  "accent": {
    "primary": ["#渐变起", "#渐变止"],
    "secondary": ["#渐变起", "#渐变止"]
  },
  "font_family": "字体族",
  "grid_pattern": {
    "enabled": true,
    "size": 40,
    "dot_radius": 1,
    "dot_color": "#色值",
    "dot_opacity": 0.05
  },
  "decorations": {
    "corner_lines": false,
    "glow_effects": false,
    "description": "装饰元素描述"
  }
}
```

---

## 预置风格库

### 1. 暗黑科技 (dark_tech)

适用场景：技术产品介绍、AI/SaaS 平台、数据平台、开发者工具

```json
{
  "style_name": "高阶暗黑科技风 (Premium Dark Mode)",
  "style_id": "dark_tech",
  "background": { "primary": "#0B1120", "gradient_to": "#0F172A" },
  "card": { "gradient_from": "#1E293B", "gradient_to": "#0F172A", "border": "rgba(255,255,255,0.05)", "border_radius": 12 },
  "text": { "primary": "#FFFFFF", "secondary": "rgba(255,255,255,0.7)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#22D3EE", "#3B82F6"], "secondary": ["#FDE047", "#F59E0B"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": true, "size": 40, "dot_radius": 1, "dot_color": "#FFFFFF", "dot_opacity": 0.05 },
  "decorations": { "corner_lines": true, "glow_effects": true, "description": "角落装饰线条 + 强调色模糊光晕" }
}
```

```css
:root {
  --bg-primary: #0B1120;
  --bg-secondary: #0F172A;
  --card-bg-from: #1E293B;
  --card-bg-to: #0F172A;
  --card-border: rgba(255,255,255,0.05);
  --card-radius: 12px;
  --text-primary: #FFFFFF;
  --text-secondary: rgba(255,255,255,0.7);
  --accent-1: #22D3EE;
  --accent-2: #3B82F6;
  --accent-3: #FDE047;
  --accent-4: #F59E0B;
}
```

---

### 2. 小米橙 (xiaomi_orange)

适用场景：硬件产品、IoT 设备、消费电子、智能家居

```json
{
  "style_name": "小米橙 (Xiaomi Orange)",
  "style_id": "xiaomi_orange",
  "background": { "primary": "#1A1A1A", "gradient_to": "#111111" },
  "card": { "gradient_from": "#2A2A2A", "gradient_to": "#1A1A1A", "border": "rgba(255,105,0,0.15)", "border_radius": 16 },
  "text": { "primary": "#FFFFFF", "secondary": "rgba(255,255,255,0.65)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#FF6900", "#FF8C00"], "secondary": ["#FFFFFF", "#E0E0E0"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": false, "description": "纯净简约，大面积留白，圆形图标元素" }
}
```

```css
:root {
  --bg-primary: #1A1A1A;
  --bg-secondary: #111111;
  --card-bg-from: #2A2A2A;
  --card-bg-to: #1A1A1A;
  --card-border: rgba(255,105,0,0.15);
  --card-radius: 16px;
  --text-primary: #FFFFFF;
  --text-secondary: rgba(255,255,255,0.65);
  --accent-1: #FF6900;
  --accent-2: #FF8C00;
  --accent-3: #FFFFFF;
  --accent-4: #E0E0E0;
}
```

---

### 3. 蓝白商务 (blue_white)

适用场景：企业介绍、培训课件、教育材料、医疗/金融行业

```json
{
  "style_name": "蓝白商务 (Blue White Business)",
  "style_id": "blue_white",
  "background": { "primary": "#FFFFFF", "gradient_to": "#F8FAFC" },
  "card": { "gradient_from": "#F1F5F9", "gradient_to": "#E2E8F0", "border": "rgba(37,99,235,0.12)", "border_radius": 12 },
  "text": { "primary": "#1E293B", "secondary": "#64748B", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#2563EB", "#1D4ED8"], "secondary": ["#059669", "#047857"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": false, "description": "清爽简洁，蓝色标题装饰条，卡片带浅色背景和细边框" }
}
```

```css
:root {
  --bg-primary: #FFFFFF;
  --bg-secondary: #F8FAFC;
  --card-bg-from: #F1F5F9;
  --card-bg-to: #E2E8F0;
  --card-border: rgba(37,99,235,0.12);
  --card-radius: 12px;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --accent-1: #2563EB;
  --accent-2: #1D4ED8;
  --accent-3: #059669;
  --accent-4: #047857;
}
```

---

### 4. 朱红宫墙 (royal_red)

适用场景：文化/历史主题、政务汇报、品牌故事、中国风

```json
{
  "style_name": "朱红宫墙 (Royal Red)",
  "style_id": "royal_red",
  "background": { "primary": "#8B0000", "gradient_to": "#5C0000" },
  "card": { "gradient_from": "#A52A2A", "gradient_to": "#7A0000", "border": "rgba(255,215,0,0.15)", "border_radius": 8 },
  "text": { "primary": "#FFF8E7", "secondary": "rgba(255,248,231,0.75)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#FFD700", "#FFA500"], "secondary": ["#FFF8E7", "#F5E6C8"] },
  "font_family": "PingFang SC, STSong, SimSun, Microsoft YaHei, serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": true, "glow_effects": false, "description": "金色角饰、祥云纹理，传统纹样装饰边框" }
}
```

```css
:root {
  --bg-primary: #8B0000;
  --bg-secondary: #5C0000;
  --card-bg-from: #A52A2A;
  --card-bg-to: #7A0000;
  --card-border: rgba(255,215,0,0.15);
  --card-radius: 8px;
  --text-primary: #FFF8E7;
  --text-secondary: rgba(255,248,231,0.75);
  --accent-1: #FFD700;
  --accent-2: #FFA500;
  --accent-3: #FFF8E7;
  --accent-4: #F5E6C8;
}
```

---

### 5. 清新自然 (fresh_green)

适用场景：环保/可持续发展、健康/医疗/养生、食品/农业、美妆/护肤

```json
{
  "style_name": "清新自然 (Fresh Green)",
  "style_id": "fresh_green",
  "background": { "primary": "#F0FDF4", "gradient_to": "#ECFDF5" },
  "card": { "gradient_from": "#FFFFFF", "gradient_to": "#F0FDF4", "border": "rgba(22,163,74,0.12)", "border_radius": 16 },
  "text": { "primary": "#14532D", "secondary": "#4B5563", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#16A34A", "#059669"], "secondary": ["#F59E0B", "#D97706"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": false, "description": "轻柔圆角、叶片图标、自然渐变色块，清新透气感" }
}
```

```css
:root {
  --bg-primary: #F0FDF4;
  --bg-secondary: #ECFDF5;
  --card-bg-from: #FFFFFF;
  --card-bg-to: #F0FDF4;
  --card-border: rgba(22,163,74,0.12);
  --card-radius: 16px;
  --text-primary: #14532D;
  --text-secondary: #4B5563;
  --accent-1: #16A34A;
  --accent-2: #059669;
  --accent-3: #F59E0B;
  --accent-4: #D97706;
}
```

---

### 6. 紫金奢华 (luxury_purple)

适用场景：时尚/奢侈品、高端服务/地产、设计/创意行业、品牌发布会

```json
{
  "style_name": "紫金奢华 (Luxury Purple)",
  "style_id": "luxury_purple",
  "background": { "primary": "#120A2E", "gradient_to": "#1A0B3D" },
  "card": { "gradient_from": "#2D1B69", "gradient_to": "#1A0B3D", "border": "rgba(192,132,252,0.1)", "border_radius": 12 },
  "text": { "primary": "#F5F3FF", "secondary": "rgba(245,243,255,0.7)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#A855F7", "#7C3AED"], "secondary": ["#F59E0B", "#D97706"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": true, "size": 50, "dot_radius": 1, "dot_color": "#A855F7", "dot_opacity": 0.03 },
  "decorations": { "corner_lines": true, "glow_effects": true, "description": "紫色光晕、金色点缀、钻石切割线条装饰，极致奢华感" }
}
```

```css
:root {
  --bg-primary: #120A2E;
  --bg-secondary: #1A0B3D;
  --card-bg-from: #2D1B69;
  --card-bg-to: #1A0B3D;
  --card-border: rgba(192,132,252,0.1);
  --card-radius: 12px;
  --text-primary: #F5F3FF;
  --text-secondary: rgba(245,243,255,0.7);
  --accent-1: #A855F7;
  --accent-2: #7C3AED;
  --accent-3: #F59E0B;
  --accent-4: #D97706;
}
```

---

### 7. 极简灰白 (minimal_gray)

适用场景：学术/研究报告、法务/合规、咨询/顾问报告、数据分析

```json
{
  "style_name": "极简灰白 (Minimal Gray)",
  "style_id": "minimal_gray",
  "background": { "primary": "#FAFAFA", "gradient_to": "#F5F5F5" },
  "card": { "gradient_from": "#FFFFFF", "gradient_to": "#FAFAFA", "border": "rgba(0,0,0,0.08)", "border_radius": 8 },
  "text": { "primary": "#171717", "secondary": "#737373", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#171717", "#404040"], "secondary": ["#DC2626", "#B91C1C"] },
  "font_family": "'Inter', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": false, "description": "纯净无装饰、大量留白、精确排版、红色仅用于关键数据强调" }
}
```

```css
:root {
  --bg-primary: #FAFAFA;
  --bg-secondary: #F5F5F5;
  --card-bg-from: #FFFFFF;
  --card-bg-to: #FAFAFA;
  --card-border: rgba(0,0,0,0.08);
  --card-radius: 8px;
  --text-primary: #171717;
  --text-secondary: #737373;
  --accent-1: #171717;
  --accent-2: #404040;
  --accent-3: #DC2626;
  --accent-4: #B91C1C;
}
```

---

### 8. 活力彩虹 (vibrant_rainbow)

适用场景：社交/娱乐平台、营销/推广材料、年轻品牌、创意方案

```json
{
  "style_name": "活力彩虹 (Vibrant Rainbow)",
  "style_id": "vibrant_rainbow",
  "background": { "primary": "#FFFFFF", "gradient_to": "#FFF7ED" },
  "card": { "gradient_from": "#FFFFFF", "gradient_to": "#FFF1E6", "border": "rgba(251,146,60,0.15)", "border_radius": 20 },
  "text": { "primary": "#1C1917", "secondary": "#57534E", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#F97316", "#EC4899"], "secondary": ["#8B5CF6", "#06B6D4"] },
  "font_family": "'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": false, "description": "多彩渐变色块、圆润大圆角、活力四溢的卡片配色（每张卡片可用不同 accent 色）" }
}
```

```css
:root {
  --bg-primary: #FFFFFF;
  --bg-secondary: #FFF7ED;
  --card-bg-from: #FFFFFF;
  --card-bg-to: #FFF1E6;
  --card-border: rgba(251,146,60,0.15);
  --card-radius: 20px;
  --text-primary: #1C1917;
  --text-secondary: #57534E;
  --accent-1: #F97316;
  --accent-2: #EC4899;
  --accent-3: #8B5CF6;
  --accent-4: #06B6D4;
}
```

---

### 9. 渐变蓝 (gradient_blue)

适用场景：科技发布会、产品发布、AI 展示

```json
{
  "style_name": "渐变蓝 (Gradient Blue)",
  "style_id": "gradient_blue",
  "background": { "primary": "#0F172A", "gradient_to": "#1E40AF" },
  "card": { "gradient_from": "#1E293B", "gradient_to": "#0F172A", "border": "rgba(96,165,250,0.1)", "border_radius": 12 },
  "text": { "primary": "#FFFFFF", "secondary": "rgba(255,255,255,0.7)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#60A5FA", "#3B82F6"], "secondary": ["#22D3EE", "#06B6D4"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": true, "size": 40, "dot_radius": 1, "dot_color": "#60A5FA", "dot_opacity": 0.05 },
  "decorations": { "corner_lines": true, "glow_effects": true, "description": "蓝色科技感渐变 + 荧光点缀 + 角落装饰线条" }
}
```

```css
:root {
  --bg-primary: #0F172A;
  --bg-secondary: #1E40AF;
  --card-bg-from: #1E293B;
  --card-bg-to: #0F172A;
  --card-border: rgba(96,165,250,0.1);
  --card-radius: 12px;
  --text-primary: #FFFFFF;
  --text-secondary: rgba(255,255,255,0.7);
  --accent-1: #60A5FA;
  --accent-2: #3B82F6;
  --accent-3: #22D3EE;
  --accent-4: #06B6D4;
}
```

---

### 10. 暖阳夕照 (warm_sunset)

适用场景：生活方式、品牌故事、旅游、美食

```json
{
  "style_name": "暖阳夕照 (Warm Sunset)",
  "style_id": "warm_sunset",
  "background": { "primary": "#1C1917", "gradient_to": "#451003" },
  "card": { "gradient_from": "#44403C", "gradient_to": "#292524", "border": "rgba(251,191,36,0.15)", "border_radius": 16 },
  "text": { "primary": "#FFFBEB", "secondary": "rgba(255,251,235,0.7)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#FBBF24", "#F97316"], "secondary": ["#FDE68A", "#F59E0B"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": true, "description": "暖橙色调 + 柔和光晕 + 温馨氛围" }
}
```

```css
:root {
  --bg-primary: #1C1917;
  --bg-secondary: #451003;
  --card-bg-from: #44403C;
  --card-bg-to: #292524;
  --card-border: rgba(251,191,36,0.15);
  --card-radius: 16px;
  --text-primary: #FFFBEB;
  --text-secondary: rgba(255,251,235,0.7);
  --accent-1: #FBBF24;
  --accent-2: #F97316;
  --accent-3: #FDE68A;
  --accent-4: #F59E0B;
}
```

---

### 11. 北欧极简 (nordic_white)

适用场景：家居、环保品牌、极简设计、生活品质

```json
{
  "style_name": "北欧极简 (Nordic White)",
  "style_id": "nordic_white",
  "background": { "primary": "#FAFAF9", "gradient_to": "#F5F5F4" },
  "card": { "gradient_from": "#FFFFFF", "gradient_to": "#F5F5F4", "border": "rgba(120,113,108,0.1)", "border_radius": 8 },
  "text": { "primary": "#1C1917", "secondary": "#78716C", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#78716C", "#57534E"], "secondary": ["#A8A29E", "#D6D3D1"] },
  "font_family": "'Inter', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": false, "description": "纯白背景 + 木质棕点缀 + 大量留白 + 极简线条" }
}
```

```css
:root {
  --bg-primary: #FAFAF9;
  --bg-secondary: #F5F5F4;
  --card-bg-from: #FFFFFF;
  --card-bg-to: #F5F5F4;
  --card-border: rgba(120,113,108,0.1);
  --card-radius: 8px;
  --text-primary: #1C1917;
  --text-secondary: #78716C;
  --accent-1: #78716C;
  --accent-2: #57534E;
  --accent-3: #A8A29E;
  --accent-4: #D6D3D1;
}
```

---

### 12. 赛博朋克 (cyber_punk)

适用场景：游戏、电竞、潮流品牌、科技展会

```json
{
  "style_name": "赛博朋克 (Cyber Punk)",
  "style_id": "cyber_punk",
  "background": { "primary": "#0C0C0C", "gradient_to": "#1A0033" },
  "card": { "gradient_from": "#1A1A2E", "gradient_to": "#0C0C0C", "border": "rgba(240,171,252,0.1)", "border_radius": 4 },
  "text": { "primary": "#FFFFFF", "secondary": "rgba(255,255,255,0.7)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#F0ABFC", "#22D3EE"], "secondary": ["#E879F9", "#67E8F9"] },
  "font_family": "'Orbitron', 'PingFang SC', 'Microsoft YaHei', system-ui, sans-serif",
  "grid_pattern": { "enabled": true, "size": 30, "dot_radius": 1, "dot_color": "#F0ABFC", "dot_opacity": 0.08 },
  "decorations": { "corner_lines": true, "glow_effects": true, "description": "霓虹渐变 + 暗夜底色 + 荧光边框 + 故障艺术线条" }
}
```

```css
:root {
  --bg-primary: #0C0C0C;
  --bg-secondary: #1A0033;
  --card-bg-from: #1A1A2E;
  --card-bg-to: #0C0C0C;
  --card-border: rgba(240,171,252,0.1);
  --card-radius: 4px;
  --text-primary: #FFFFFF;
  --text-secondary: rgba(255,255,255,0.7);
  --accent-1: #F0ABFC;
  --accent-2: #22D3EE;
  --accent-3: #E879F9;
  --accent-4: #67E8F9;
}
```

---

### 13. 优雅金 (elegant_gold)

适用场景：奢侈品、高端珠宝、宴会、企业年报

```json
{
  "style_name": "优雅金 (Elegant Gold)",
  "style_id": "elegant_gold",
  "background": { "primary": "#1C1917", "gradient_to": "#292524" },
  "card": { "gradient_from": "#292524", "gradient_to": "#1C1917", "border": "rgba(252,211,77,0.15)", "border_radius": 8 },
  "text": { "primary": "#FFFBEB", "secondary": "rgba(255,251,235,0.75)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#FCD34D", "#B45309"], "secondary": ["#F59E0B", "#D97706"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": true, "glow_effects": true, "description": "香槟金强调 + 深灰底色 + 精致边框 + 高光点缀" }
}
```

```css
:root {
  --bg-primary: #1C1917;
  --bg-secondary: #292524;
  --card-bg-from: #292524;
  --card-bg-to: #1C1917;
  --card-border: rgba(252,211,77,0.15);
  --card-radius: 8px;
  --text-primary: #FFFBEB;
  --text-secondary: rgba(255,251,235,0.75);
  --accent-1: #FCD34D;
  --accent-2: #B45309;
  --accent-3: #F59E0B;
  --accent-4: #D97706;
}
```

---

### 14. 深海蓝 (ocean_depth)

适用场景：海洋公益、环保组织、航海、科技

```json
{
  "style_name": "深海蓝 (Ocean Depth)",
  "style_id": "ocean_depth",
  "background": { "primary": "#0C4A6E", "gradient_to": "#082F49" },
  "card": { "gradient_from": "#164E63", "gradient_to": "#0C4A6E", "border": "rgba(34,211,238,0.1)", "border_radius": 12 },
  "text": { "primary": "#FFFFFF", "secondary": "rgba(255,255,255,0.75)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#22D3EE", "#06B6D4"], "secondary": ["#67E8F9", "#0891B2"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": true, "size": 50, "dot_radius": 1, "dot_color": "#22D3EE", "dot_opacity": 0.03 },
  "decorations": { "corner_lines": false, "glow_effects": true, "description": "深海渐变 + 荧光蓝点缀 + 气泡装饰 + 水波纹理" }
}
```

```css
:root {
  --bg-primary: #0C4A6E;
  --bg-secondary: #082F49;
  --card-bg-from: #164E63;
  --card-bg-to: #0C4A6E;
  --card-border: rgba(34,211,238,0.1);
  --card-radius: 12px;
  --text-primary: #FFFFFF;
  --text-secondary: rgba(255,255,255,0.75);
  --accent-1: #22D3EE;
  --accent-2: #06B6D4;
  --accent-3: #67E8F9;
  --accent-4: #0891B2;
}
```

---

### 15. 复古胶片 (retro_film)

适用场景：文创、摄影、婚礼、民宿、回忆录

```json
{
  "style_name": "复古胶片 (Retro Film)",
  "style_id": "retro_film",
  "background": { "primary": "#FEF3C7", "gradient_to": "#FDE68A" },
  "card": { "gradient_from": "#FFFBEB", "gradient_to": "#FEF3C7", "border": "rgba(146,64,14,0.15)", "border_radius": 8 },
  "text": { "primary": "#451A03", "secondary": "#92400E", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#92400E", "#78350F"], "secondary": ["#B45309", "#D97706"] },
  "font_family": "Georgia, 'PingFang SC', 'Microsoft YaHei', serif",
  "grid_pattern": { "enabled": false },
  "decorations": { "corner_lines": false, "glow_effects": false, "description": "米黄做旧底色 + 棕褐色调 + 胶片边框 + 噪点纹理感" }
}
```

```css
:root {
  --bg-primary: #FEF3C7;
  --bg-secondary: #FDE68A;
  --card-bg-from: #FFFBEB;
  --card-bg-to: #FEF3C7;
  --card-border: rgba(146,64,14,0.15);
  --card-radius: 8px;
  --text-primary: #451A03;
  --text-secondary: #92400E;
  --accent-1: #92400E;
  --accent-2: #78350F;
  --accent-3: #B45309;
  --accent-4: #D97706;
}
```

---

### 16. 稳重蓝 (corporate_blue)

适用场景：咨询、投行、4A 广告、政府报告

```json
{
  "style_name": "稳重蓝 (Corporate Blue)",
  "style_id": "corporate_blue",
  "background": { "primary": "#1E3A5F", "gradient_to": "#0F2942" },
  "card": { "gradient_from": "#1E3A5F", "gradient_to": "#172554", "border": "rgba(96,165,250,0.12)", "border_radius": 8 },
  "text": { "primary": "#FFFFFF", "secondary": "rgba(255,255,255,0.75)", "title_size": 28, "body_size": 14, "card_title_size": 20 },
  "accent": { "primary": ["#60A5FA", "#2563EB"], "secondary": ["#93C5FD", "#3B82F6"] },
  "font_family": "PingFang SC, Microsoft YaHei, system-ui, sans-serif",
  "grid_pattern": { "enabled": true, "size": 60, "dot_radius": 1, "dot_color": "#60A5FA", "dot_opacity": 0.03 },
  "decorations": { "corner_lines": true, "glow_effects": false, "description": "藏蓝稳重底色 + 蓝色强调 + 简洁线条 + 专业感" }
}
```

```css
:root {
  --bg-primary: #1E3A5F;
  --bg-secondary: #0F2942;
  --card-bg-from: #1E3A5F;
  --card-bg-to: #172554;
  --card-border: rgba(96,165,250,0.12);
  --card-radius: 8px;
  --text-primary: #FFFFFF;
  --text-secondary: rgba(255,255,255,0.75);
  --accent-1: #60A5FA;
  --accent-2: #2563EB;
  --accent-3: #93C5FD;
  --accent-4: #3B82F6;
}
```

---

## 风格自动推断

当用户未指定风格时，根据主题关键词自动推断：

| 关键词匹配 | 推荐风格 |
|-----------|---------|
| AI、机器学习、深度学习、SaaS、云、平台、API、开发者、大模型、LLM、数据、算法 | dark_tech |
| 手机、硬件、IoT、智能家居、芯片、穿戴、电子、家电、机器人 | xiaomi_orange |
| 企业、公司、培训、教育、医疗、金融、银行、保险、制药、GLP、GMP、质量 | blue_white |
| 文化、历史、国风、中国、政务、党建、品牌故事、非遗、传统 | royal_red |
| 环保、绿色、可持续、健康、养生、食品、农业、有机、美妆、护肤、自然 | fresh_green |
| 时尚、奢侈品、高端、地产、设计、创意、艺术、珠宝、定制 | luxury_purple |
| 学术、研究、论文、报告、法务、合规、咨询、审计、数据分析、白皮书 | minimal_gray |
| 社交、娱乐、营销、推广、年轻、潮流、游戏、直播、短视频、电商 | vibrant_rainbow |
| 科技、发布会、产品、新品、技术展示、数码 | gradient_blue |
| 生活、方式、美食、旅游、生活方式、美食博主 | warm_sunset |
| 家居、简约、极简、北欧、日式、设计、品质生活 | nordic_white |
| 游戏、电竞、赛博朋克、潮流、街头、朋克、科技感 | cyber_punk |
| 奢华、珠宝、高端、宴会、奢侈品、收藏 | elegant_gold |
| 海洋、海滨、环保、公益、航海、潜水、蓝色经济 | ocean_depth |
| 摄影、文创、复古、婚礼、民宿、回忆录、胶片 | retro_film |
| 咨询、投行、4A、广告、政府、稳重、专业、正式 | corporate_blue |
| 其他未匹配 | blue_white（最通用的默认风格） |

## 自定义风格

用户可以在 Step 1 的"补充需求"中指定品牌色：

> "品牌主色 #1DA1F2，背景用深色"

此时基于最接近的预置风格，替换对应的色值字段：
1. 将 accent.primary 替换为用户品牌色
2. 根据品牌色明度自动选择 background 深/浅
3. 其他字段保持预置风格的值

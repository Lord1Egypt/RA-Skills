# 房地产（Real Estate）

**气质：** 地产高端、城市感、空间价值、资产增值
**适用：** 房地产报告、市场分析、城市规划、物业评估
**推荐字体：** FP-4（Cormorant Garamond + Outfit）
**背景类型：** 暗色系（黑曜石 #0a0c10 / 深石墨蓝 #111827），高端楼盘夜景感
**主标题字号：** 40–56px Cormorant 衬线，字距负值，奢华感
**页眉形式：** 左侧项目名 + 城市，右侧区位/容积率，铜金细线分割

---

## 设计特征

- **铜金**（#b45309 / #d97706）+ **建筑白**（#e8e4dc）双主色，地产奢华感
- 深黑背景，高楼夜景气质
- 衬线大标题（Cormorant Garamond），传达品质感
- 地图/平面图占位区（深蓝色块模拟鸟瞰）
- 价格/面积/容积率等核心指标突出展示

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;0,800;1,700&family=Outfit:wght@300;400;500&display=swap');

body { background: #0a0c10; font-family: 'Outfit','PingFang SC',sans-serif; color: #e2ddd4; }

/* 城市夜景光效 */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(ellipse at 30% 80%, rgba(180,83,9,0.08) 0%, transparent 45%),
    radial-gradient(ellipse at 70% 20%, rgba(17,24,39,0.6) 0%, transparent 60%);
}

/* 展示标题（地产奢华） */
.display-title {
  font-family: 'Cormorant Garamond','Noto Serif SC',serif;
  font-size: 50px; font-weight: 800; font-style: italic;
  letter-spacing: -1.5px; line-height: 0.95;
  background: linear-gradient(135deg, #e8e4dc 20%, #d97706 65%, #b45309);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 卡片（带铜金顶线） */
.card {
  background: rgba(10,12,20,0.9);
  border: 1px solid rgba(180,83,9,0.2);
  border-top: 1px solid rgba(217,119,6,0.5);
  border-radius: 3px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
}

/* 价格/面积大数字 */
.stat-num {
  font-family: 'Cormorant Garamond', serif;
  font-size: 46px; font-weight: 800; font-style: italic; line-height: 1;
  background: linear-gradient(135deg, #d97706, #f59e0b);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.stat-unit { font-size: 14px; font-weight: 600; color: #9ca3af; margin-left: 2px; }

/* 区位/项目标签 */
.estate-tag {
  display: inline-flex; align-items: center;
  background: rgba(180,83,9,0.12); border: 1px solid rgba(180,83,9,0.25);
  border-radius: 2px; padding: 2px 7px;
  font-size: 8.5px; font-weight: 600; color: #d97706;
  letter-spacing: 0.5px; text-transform: uppercase;
}

/* 建筑参数行 */
.estate-row {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 10.5px; padding: 3px 0;
  border-bottom: 1px solid rgba(180,83,9,0.08);
}
.estate-row .label { color: #6b7280; }
.estate-row .value { color: #e2ddd4; font-weight: 600; }

/* 平面图占位 */
.floorplan-block {
  background: linear-gradient(135deg, #111827, #1f2d3d);
  border-radius: 2px; display: flex; align-items: center; justify-content: center;
  font-family: 'Outfit',sans-serif; font-size: 9px; color: rgba(180,83,9,0.4);
  letter-spacing: 2px; text-transform: uppercase;
}

/* 进度条（铜金渐变） */
.estate-bar { height: 3px; background: rgba(180,83,9,0.1); border-radius: 0; }
.estate-fill { height: 100%; background: linear-gradient(90deg, #92400e, #d97706, #fbbf24); }
```

---

## CSS 变量

```css
:root {
  --bg:   #0a0c10;
  --card: #0e1118;
  --p:    #d97706;
  --pm:   rgba(180,83,9,0.12);
  --bd:   rgba(180,83,9,0.2);
  --t:    #e2ddd4;
  --mt:   #a09890;
  --dt:   #4a4540;
}
```

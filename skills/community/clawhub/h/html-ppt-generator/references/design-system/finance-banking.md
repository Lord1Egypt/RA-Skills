# 金融银行（Finance Banking）

**气质：** 稳重权威、私行精英、华尔街质感
**适用：** 金融报告、投资分析、资产配置、年报呈现
**推荐字体：** FP-4（Cormorant Garamond 800 + Outfit 300）
**背景类型：** 暗色系（深海蓝黑）
**主标题字号：** 36–48px 衬线渐变，高对比
**页眉形式：** 左侧机构徽标位 + 报告名 + 右侧日期 + monospace 页码

---

## 设计特征

- **金色系**（#c9a84c / #d4a842）作为唯一强调色，象征财富与信任
- 衬线大标题（Cormorant Garamond）传达传统权威感
- 卡片用金色顶线分割，背景近黑
- 数据表格密集，负空间极少
- 进度条/柱状用金色渐变

---

## CSS 片段

```css
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700;800&family=Outfit:wght@300;400;500&display=swap');

body { background: #030712; font-family: 'Outfit','PingFang SC',sans-serif; color: #e8dfc8; }

/* 细网格纹理（账本感） */
body::before {
  content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:
    linear-gradient(rgba(201,168,76,0.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(201,168,76,0.025) 1px, transparent 1px);
  background-size: 48px 48px;
}

/* 展示标题（衬线金色渐变） */
.display-title {
  font-family: 'Cormorant Garamond','Noto Serif SC',serif;
  font-size: 44px; font-weight: 800;
  letter-spacing: -1px; line-height: 1.0;
  background: linear-gradient(135deg, #e8dfc8 20%, #c9a84c 60%, #d4a842);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 卡片（带金色顶线） */
.card {
  background: rgba(8,12,24,0.9);
  border: 1px solid rgba(201,168,76,0.15);
  border-top: 1px solid rgba(201,168,76,0.45);
  border-radius: 4px; padding: 10px 14px;
  display: flex; flex-direction: column; gap: 5px;
  position: relative;
}

/* KPI 数字（金色） */
.stat-num {
  font-family: 'Cormorant Garamond', serif;
  font-size: 40px; font-weight: 800; line-height: 1; letter-spacing: -1px;
  background: linear-gradient(135deg, #c9a84c, #d4a842);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 数据表格（账单感） */
.fin-table { width:100%; border-collapse:collapse; font-size:10.5px; }
.fin-table th { color:#c9a84c; font-weight:600; padding:4px 8px; border-bottom:1px solid rgba(201,168,76,0.3); font-size:9px; letter-spacing:0.5px; text-transform:uppercase; }
.fin-table td { padding:4px 8px; border-bottom:1px solid rgba(255,255,255,0.04); color:#b8a98a; }
.fin-table td.pos { color:#4ade80; }   /* 正收益 */
.fin-table td.neg { color:#f87171; }   /* 负收益 */
.fin-table td.num { font-family:monospace; text-align:right; }

/* 分割线（金色渐变） */
.fin-divider {
  height:1px;
  background: linear-gradient(90deg, transparent, rgba(201,168,76,0.4), transparent);
  margin: 6px 0;
}
```

---

## CSS 变量

```css
:root {
  --bg:   #030712;
  --card: #080c18;
  --p:    #c9a84c;
  --pm:   rgba(201,168,76,0.12);
  --bd:   rgba(201,168,76,0.18);
  --t:    #e8dfc8;
  --mt:   #b8a98a;
  --dt:   #7a6e55;
}
```

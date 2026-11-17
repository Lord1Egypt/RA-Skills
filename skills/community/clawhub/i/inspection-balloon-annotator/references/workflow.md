# 检验气泡图 —— 操作细则与常见坑

## 一、五个命令(按顺序)

```bash
# 0) 渲染(400 DPI 足够; 太低了细线文字 OCR 会漏)
python scripts/render_pdf.py    in.pdf        work/render.png --dpi 400

# 1) 多方向 OCR 定位标注文字
python scripts/ocr_labels.py    work/render.png work/labels.json

# 2) 查文字位置(反复用, 直到每个尺寸都找到)
python scripts/find_label.py    work/labels.json "19"
python scripts/find_label.py    work/labels.json "0\.1|0\.05"

# 3) 画气泡(先写 targets.json)
python scripts/draw_balloons.py work/render.png work/targets.json work/ballooned.png --band-top 2450

# 4) 出检验表(先写 items.json)
python scripts/build_inspection_xlsx.py work/items.json work/ballooned.png out.xlsx --title "…检验记录表"
```

## 二、targets.json

```json
{ "1": [1980, 654], "2": [2313, 594], "23": [3432, 1290] }
```
- 键 = 气泡号(与检验表"序号"一致), 值 = 目标点 [x, y](px, 与 render.png 同坐标系)。
- 目标点建议直接取该尺寸**文字框中心**。
- `draw_balloons.py` 会做"吸附墨迹"微调(<=70px), 因此 5~10px 的误差可容忍。

## 三、items.json

```json
{
  "title": "电磁阀尾座  尺寸与形位公差检验记录表",
  "info": [
    ["零件名称","电磁阀尾座","图号","MEST-F800-18a"],
    ["材料","6061 铝合金","表面处理","喷砂黑氧"],
    ["未注公差","尺寸 GB/T1804-2000 f级 / 形位 GB/T1184-1996 H级","检验类别","首件检验"]
  ],
  "explicit": [
    ["标注","数值","说明"],
    ["19 ±0.1","±0.1","定心尺寸"]
  ],
  "items": [
    {"no":1,"view":"主视图","item":"2-G1/8 管螺纹气口","basic":"G1/8","upper":"—","lower":"—",
     "tol":"螺纹公差","gauge":"G1/8 螺纹塞规/通止规","method":"通止规检验, 通气密封性抽查","level":"A"}
  ]
}
```
- `no` 允许字符串(如 `"43"`)用于"其他/技术要求"类附加项。
- `level`：A 关键(红) / B 重要(黄) / C 一般(绿)。
- `explicit` 可选，用于第三张表列出图纸显式公差。

## 四、常见坑(实测)

1. **PDF 文字是矢量轮廓时** `page.get_text()` 返回 0 段 —— 别指望文本层, 直接走 OCR。
2. **竖排尺寸**(26 / 14 / 13 / 5.5 这类)在 0° OCR 下识别不到, 必须跑 90°/270°；`ocr_labels.py` 已内置。
3. **坐标换算**：旋转图上的检测框映射回原图时, 旋转图宽高会互换。若自己写代码, 记住
   `k=1: xo=(W-1)-yr, yo=xr`；`k=3: xo=yr, yo=(H-1)-xr`（W/H 为**原图**宽高）。搞错会整体偏移。
4. **OCR 会把符号读歪**：`Ø`→`0`/`@`, `⊥`→`L`, `▽`→`V`, `线`→`?`。按"数值+位置"判断, 不要死抠字符。
5. **气泡压标题栏**：图纸标题栏通常在右下或底部整条, 用 `--band-top` 把气泡限制在图纸区内。
6. **别用肉眼估坐标**：视图多、缩放不同, 估算必然漂。以 OCR 坐标为唯一依据。
7. **气泡重叠**：`draw_balloons.py` 已做防重叠; 若仍有密集区, 适当调大 `--offset` / 调小 `--radius`。
8. **交付前自检**：脚本会打印 `low-ink targets`; 若有, 说明该气泡指到了空白, 回 Step 2 修正坐标。

## 五、交付约定

- 输出两份：`<零件> 标注图纸(气泡图).png` + `<零件> 检验表(关键尺寸+形位公差).xlsx`。
- 用 `present_files` 一并给出。
- 回复中说明：气泡号与检验表序号一一对应；未注公差取自图纸技术要求(GB/T1804-f / GB/T1184-H)；
  气泡坐标为 OCR 定位，正式使用前建议目视复核关键项。

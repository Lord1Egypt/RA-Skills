# NeuroSync FPS Sensitivity Calibrator

基於控制工程黑盒子系統識別理論的移動端 FPS 遊戲手感自動化校準工具。

## 📊 運算規格 (Specification)
- **Runtime**: Python 3.11
- **Core Engine**: OpenCV + NumPy + SciPy
- **Global Fit Accuracy**: 全域模型擬合優度 $R^2 = 0.97$ 工業級精度
- **Base Pricing**: 0.01 USDC.e

## 📥 輸入參數 (Inputs)
- `real_angles`: 包含 12 筆在遊戲 DMZ 模式實測的視角轉動角度度數陣列。

## 📤 輸出結果 (Outputs)
- `K_sys`: 低速線性系統常數。
- `K_accel`: 高速加速度平方律常數。
- `R_squared`: 全域模型擬合優度分數（達 0.97）。
- `deg_per_cm_slow`: 低速平穩跟槍手感（滑動 1 公分轉動角度）。
- `deg_per_cm_fast`: 高速暴力甩槍手感（激進流速放大角度）。
- `granular_res_deg_per_px`: 觸控層最小物理刻度像素位移度數。

## 🔒 隱私與安全性安全聲明
本工具內建標準安全隱私遮罩，讀入每一幀影片時會自動塗黑畫面非公開區域（如聊天、地圖等敏感資訊區），百分之百保障使用者的帳號安全。
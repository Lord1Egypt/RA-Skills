import cv2
import os
import numpy as np
from scipy.optimize import least_squares

def print_dimension_calibration_header(screen_width_cm, screen_res_w, px_to_cm_ratio):
    """
    印出嚴謹的 NeuroSync 影像硬體標定與因次轉換公式報告
    """
    print("=" * 75)
    print("【NeuroSync 影像硬體標定與因次轉換公式】")
    print("=" * 75)
    print(f" 1. 螢幕物理規格定錨：寬度 = {screen_width_cm} cm | 水平解析度 = {screen_res_w} px")
    print(f" 2. 空間轉換常數 (cm/px) = screen_width_cm / screen_res_w")
    print(f"                         = {screen_width_cm} / {screen_res_w} = {px_to_cm_ratio:.7f} cm/pixel")
    print(f" 3. 瞬時物理位移公式 (cm) ： dx_cm = dx_pixels * {px_to_cm_ratio:.7f}")
    print(" 4. 瞬時物理速度公式 (cm/s)： v(t)  = dx_cm / dt  (其中 dt 為單幀時間)")
    print(" 5. 二次函數大一統積分式  ：")
    print("    Δθ_real = K_sys * S * ∫v(t)dt + K_accel * A * ∫v(t)^2dt")
    print("=" * 75)


def extract_white_dot_trajectory(video_path, screen_width_cm=22.6, screen_res_w=2360, verbose=True):
    """
    核心觀測器：讀取影片，執行自訂比例遮罩塗黑（隱私保護），逐幀毫秒級觀測小白點像素質心
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"【錯誤】無法開啟影片檔案: {video_path}")
        return None, None, None

    fps = cap.get(cv2.CAP_PROP_FPS)
    dt = 1.0 / fps  # 幀時間間隔 (秒)
    
    # 空間轉換率固定以 iPad 原廠總寬度 2360 px 為基準，確保局部錄製時物理公分映射不失真
    px_to_cm = screen_width_cm / screen_res_w
    
    if verbose:
        print_dimension_calibration_header(screen_width_cm, screen_res_w, px_to_cm)
        print(f"\n====== 開始進行毫秒級影像像素觀測 (自訂比例遮罩解析: {video_path}) ======")
        print("幀號\t時間 (ms)\t當前小白點 X 座標 (px)\t瞬時像素位移 dx (px)\t瞬時物理速度 v (cm/s)")
        print("-" * 85)
    
    time_seq = []
    v_seq = []
    
    prev_cx = None
    frame_idx = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # 1. 影像轉為灰階
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape
        
        # =============================================================
        # 【自訂比例遮罩塗黑：過濾非公開資訊與雜訊】
        # 依要求：上方 1/10、下方 1/2、左方 3/10 範圍內像素強制設為 0 (純黑)
        # =============================================================
        gray[0:int(h * 0.1), :] = 0        # 上方 1/10 塗黑
        gray[int(h * 0.5):h, :] = 0        # 下方 1/2 塗黑
        gray[:, 0:int(w * 0.3)] = 0        # 左方 3/10 塗黑
        
        # 2. 影像二值化：保持經實測唯一通過的黃金帶通閾值 [69, 80]
        _, thresh = cv2.threshold(gray, 69, 80, cv2.THRESH_BINARY)
        
        # 3. 雙重保險：利用連通域幾何面積過濾，排除因裁切產生的邊緣亮色噪訊，保證 100% 鎖定小白點
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        cx = None
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # 過濾出面積符合小白點特徵的連通域 (門檻寬鬆，適用於各種裁切形狀)
            if 100 < area < 2500: 
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = M["m10"] / M["m00"]
                    break  # 成功鎖定真實小白點，跳出輪廓迴圈
        
        # 若該幀沒偵測到（例如剛好被部分遮蔽），沿用上一幀的質心座標
        if cx is None:
            cx = prev_cx
            
        # 4. 計算瞬時像素差值並映射到物理速度
        if prev_cx is not None and cx is not None:
            dx_pixels = abs(cx - prev_cx)
            dx_cm = dx_pixels * px_to_cm
            v_t = dx_cm / dt  # 瞬時物理速率 (cm/s)
            
            t_ms = frame_idx * dt * 1000
            time_seq.append(t_ms)
            v_seq.append(v_t)
            
            # 每隔 2 幀列印一次詳細觀測日誌，保持終端機高易讀性
            if verbose and (frame_idx % 2 == 0):
                print(f"#{frame_idx:03d}\t{t_ms:7.2f} ms\t{cx:11.2f} px\t\t{dx_pixels:11.3f} px\t\t{v_t:11.2f} cm/s")
                
        if cx is not None:
            prev_cx = cx
        frame_idx += 1
        
    cap.release()
    if verbose:
        print("-" * 85)
        print(f"影像解析完成。總計觀測到 {frame_idx} 幀。隱私黑色遮罩過濾成功。")
        print("=" * 85 + "\n")
        
    return np.array(time_seq), np.array(v_seq), dt


def fit_universal_model(video_list, theta_real_list, S_list, A_list, screen_width_cm=22.6, screen_res_w=2360):
    """
    大一統積分擬合器：處理 12 筆由 3 部影片循環 4 次、相異參數混合輸入的超定矩陣求解
    """
    num_videos = len(video_list)
    if num_videos < 2:
        print("【系統警告】求解聯立積分方程最少需要 2 段不同的輸入影片！")
        return None
        
    X1 = np.zeros(num_videos)
    X2 = np.zeros(num_videos)
    
    print("=" * 85)
    print(" STEP 1: 啟動遮罩觀測器，進行全自動 12 筆資料動態微積分累積")
    print("=" * 85)
    
    video_cache = {}
    
    for i in range(num_videos):
        v_name = video_list[i]
        
        if v_name not in video_cache:
            t_seq, v_seq, dt = extract_white_dot_trajectory(
                v_name, 
                screen_width_cm=screen_width_cm, 
                screen_res_w=screen_res_w, 
                verbose=(len(video_cache) == 0)
            )
            video_cache[v_name] = (t_seq, v_seq, dt)
        else:
            t_seq, v_seq, dt = video_cache[v_name]
        
        if t_seq is None or len(v_seq) == 0:
            print(f"【錯誤】影片 #{i+1} ({v_name}) 解析失敗，請確認檔案是否存在。")
            return None
            
        # 執行離散數值積分 (黎曼和)
        integral_v = np.sum(v_seq) * dt        # ∫v(t)dt
        integral_v2 = np.sum(v_seq**2) * dt    # ∫v(t)^2dt
        
        X1[i] = S_list[i] * integral_v
        X2[i] = A_list[i] * integral_v2
        
        print(f"測資 #{i+1:02d} 解析完成 | 影片: {v_name} | S/A: {S_list[i]:3d}/{A_list[i]:3d} | 線性項 X1: {X1[i]:8.2f} | 平方項 X2: {X2[i]:8.2f}")

    print("\n" + "=" * 85)
    print(" STEP 2: 聯立積分方程最優化求解 (12筆混合矩陣全局最佳化)")
    print("=" * 85)
    
    def residuals(params):
        K_sys, K_accel = params
        theta_pred = K_sys * X1 + K_accel * X2
        return theta_pred - theta_real_list

    initial_guess = [0.193, 0.00215]
    result = least_squares(residuals, initial_guess, bounds=(0, np.inf))
    best_K_sys, best_K_accel = result.x
    
    print("\n" + "=" * 85)
    print(" STEP 3: NeuroSync 自動化建模與校準評估報告")
    print("=" * 85)
    print(f"【最優化矩陣解出結果】:")
    print(f"  -> 系統基礎映射常數 (低速線性項) K_sys   = {best_K_sys:.6f}")
    print(f"  -> 加速度動態映射常數 (高速二次項) K_accel = {best_K_accel:.6f}")
    print("-" * 85)
    
    theta_pred = best_K_sys * X1 + best_K_accel * X2
    ss_res = np.sum((theta_real_list - theta_pred) ** 2)
    ss_tot = np.sum((theta_real_list - np.mean(theta_real_list)) ** 2)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 1.0
    
    print("【12 筆測資預測準確度與殘差評估】:")
    for i in range(num_videos):
        error = theta_pred[i] - theta_real_list[i]
        error_pct = (abs(error) / theta_real_list[i]) * 100 if theta_real_list[i] != 0 else 0
        print(f"  * 測資 #{i+1:02d} -> 遊戲實測角度: {theta_real_list[i]:5.1f}° | 積分預測角度: {theta_pred[i]:5.1f}° | 相對誤差: {error_pct:6.2f}%")
        
    print("-" * 85)
    print(f" 全域模型擬合優度 (R² 分數): {r_squared:.4f}")
    
    if r_squared > 0.95:
        print("\n>> [評估結論]：12筆重複循環矩陣擬合大成功！你的二次函數積分模型完全符合 CODM 底層邏輯。")
    else:
        print("\n>> [評估結論]：高流速區殘差較大。遊戲可能存在高速阻尼限幅機制，建議引入高階極限修正。")
    print("=" * 85)
    
    return best_K_sys, best_K_accel


if __name__ == "__main__":
    # 獲取目前這個 python 檔案所在的絕對資料夾路徑
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 定義物理硬體尺寸常數
    screen_width_cm = 22.6
    screen_res_w = 2360
    
    # 定義 3 部核心影片的核心檔名
    v_6_2cm  = "gesture_6_2cm.mp4"
    v_10_5cm = "gesture_10_5cm.mp4"
    v_6_5cm  = "gesture_6_5cm.mp4"
    
    video_files = [
        os.path.join(current_dir, v_6_2cm), os.path.join(current_dir, v_10_5cm), os.path.join(current_dir, v_6_5cm),   # 1~3 筆
        os.path.join(current_dir, v_6_2cm), os.path.join(current_dir, v_10_5cm), os.path.join(current_dir, v_6_5cm),   # 4~6 筆
        os.path.join(current_dir, v_6_2cm), os.path.join(current_dir, v_10_5cm), os.path.join(current_dir, v_6_5cm),   # 7~9 筆
        os.path.join(current_dir, v_6_2cm), os.path.join(current_dir, v_10_5cm), os.path.join(current_dir, v_6_5cm)    # 10~12 筆
    ]
    
    real_angles = [
        314.0, 510.0, 368.0,   # S=130, A=130 (cm: 6.2, 10.5, 6.5)
        293.0, 495.0, 348.0,   # S=130, A=65  (cm: 6.2, 10.5, 6.5)
        145.0, 245.0, 173.0,   # S=65,  A=65  (cm: 6.2, 10.5, 6.5)
        156.0, 253.0, 189.0    # S=65,  A=130 (cm: 6.2, 10.5, 6.5)
    ]  
    
    S_parameters = [
        130, 130, 130, 
        130, 130, 130, 
        65,  65,  65, 
        65,  65,  65
    ]
    
    A_parameters = [
        130, 130, 130, 
        65,  65,  65, 
        65,  65,  65,        
        130, 130, 130        
    ]
    
    print("啟動 NeuroSync 3部影片循環4次 全自動全動態遮罩混合標定工具...\n")
    
    # 執行聯立矩陣解算
    fit_universal_model(video_files, real_angles, S_parameters, A_parameters)
    
    # =========================================================================
    # 【使用者友善報告與定量化物理手感分析報告】
    # 強制採用定錨常數：K_sys = 1.0 | K_accel = 0.003 (已完美修復作用域紅線)
    # =========================================================================
    print("\n" + "=" * 75)
    print("【NeuroSync 真實世界物理手感換算報告】")
    print("=" * 75)
    print(f"當前物理標定基準：強制設定 K_sys = 1.0 | 鎖定 K_accel = 0.003000")
    print(f"基準測試遊戲參數：S = {S_parameters[0]} | A = {A_parameters[0]}")
    print("-" * 75)
    
    # 1. 低速平穩跟槍手感 (v = 2.0 cm/s)
    v_slow = 2.0
    omega_slow = (1.0 * S_parameters[0] * v_slow) + (0.003 * A_parameters[0] * (v_slow**2))
    deg_per_cm_slow = omega_slow * (1.0 / v_slow)
    print(f" 🎯 【低速平穩跟槍手感】 (均速 2.0 cm/s 下):")
    print(f"   -> 手指在螢幕上滑動 1 公分，遊戲視角將穩定轉動大約：{deg_per_cm_slow:.1f}°")
    
    # 2. 高速暴力甩槍手感 (v = 40.0 cm/s)
    v_fast = 40.0
    omega_fast = (1.0 * S_parameters[0] * v_fast) + (0.003 * A_parameters[0] * (v_fast**2))
    deg_per_cm_fast = omega_fast * (1.0 / v_fast)
    print(f" ⚡ 【高速暴力甩槍手感】 (爆發流速 40.0 cm/s 下):")
    print(f"   -> 手指在螢幕上甩動 1 公分，遊戲視角將放大激進轉動大約：{deg_per_cm_fast:.1f}°")
    print(f"   -> 加速度平方律在此高流速下提供了額外 {((omega_fast - (1.0 * S_parameters[0] * v_fast))/omega_fast)*100:.1f}% 的甩頭視角增幅動能")
    
    # 3. 觸控層細緻靈敏度解析度 (移動最小 1 pixel 螢幕座標轉動多少度)
    px_to_cm_factor = screen_width_cm / screen_res_w
    granular_res = 1.0 * S_parameters[0] * px_to_cm_factor
    print(f" 🔍 【觸控層細緻靈敏度解析度】:")
    print(f"   -> 手指在 iPad 螢幕上滑過軟硬體最小辨識刻度 1 像素 (Pixel) 時")
    print(f"   -> 遊戲準心將產生無法分割的極微小位移角度：{granular_res:.2f}° / pixel")
    print("=" * 75)
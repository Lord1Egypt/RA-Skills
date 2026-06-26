import os, cv2, random, shutil, tqdm
import pandas as pd
import numpy as np
import json
import argparse

#########將兩個標註資料集結合，使class數量增加，用於將box_label和自動生成的scratch_label結合(只合成和複製同名label同名label)##########

def copy_scratch_to_oldimage(pad_folder,scratch_folder,output_folder):
# 只處理兩邊都有的 label 檔名
    common_filenames = set(os.listdir(pad_folder)).intersection(set(os.listdir(scratch_folder)))

    for filename in common_filenames:
        if filename.endswith('.txt'):
            path1 = os.path.join(pad_folder, filename)
            path2 = os.path.join(scratch_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with open(path1, 'r') as f1:
                content1 = f1.read().strip()

            with open(path2, 'r') as f2:
                content2 = f2.read().strip()

            # 合併 label，只儲存有內容的檔案
            combined = []
            if content1:
                combined.append(content1)
            if content2:
                combined.append(content2)

            if combined:
                with open(output_path, 'w') as fout:
                    fout.write('\n'.join(combined))

def close_polygon(yolo_seg_folder, backup=True, epsilon=1e-6):
    def is_closed(polygon):
        return abs(polygon[0] - polygon[-2]) < epsilon and abs(polygon[1] - polygon[-1]) < epsilon

    for root, _, files in os.walk(yolo_seg_folder):
        for file in files:
            if not file.endswith(".txt"):
                continue

            txt_path = os.path.join(root, file)
            with open(txt_path, 'r') as f:
                lines = f.readlines()

            updated_lines = []
            modified = False

            for line in lines:
                parts = line.strip().split()
                if len(parts) <= 6:
                    # Not a YOLO-seg format, skip
                    updated_lines.append(line)
                    continue

                poly = list(map(float, parts[5:]))

                if not is_closed(poly):
                    # Append the first point to the end to close the polygon
                    poly += poly[:2]
                    modified = True

                updated_line = ' '.join(parts[:5] + list(map(lambda x: f"{x:.6f}", poly)))
                updated_lines.append(updated_line + '\n')

            if modified:
                if backup:
                    os.rename(txt_path, txt_path + ".bak")  # backup original

                with open(txt_path, 'w') as f:
                    f.writelines(updated_lines)
                print(f"Closed polygon in: {txt_path}")
def get_segment_label(mask, class_id=2, epsilon_ratio=0.001):
    """
    從二值 mask 中提取 segmentation label。
    回傳 (bbox, segmentation)，其中：
      - bbox 格式：[x_center, y_center, width, height]（都做歸一化）
      - segmentation：一維 list of floats [x1,y1, x2,y2, ..., xn,yn]（都做歸一化）
    如果沒找到輪廓，回傳 (None, None)。
    """
    h, w = mask.shape[:2]
    # 轉灰階、二值
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    # 找所有外部輪廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None

    # 合併所有輪廓點
    all_pts = np.vstack(contours).squeeze()  # shape (N,2)
    # bounding box
    x, y, bw, bh = cv2.boundingRect(all_pts)
    # YOLO 格式，歸一化
    x_center = (x + bw/2) / w
    y_center = (y + bh/2) / h
    bw /= w
    bh /= h
    bbox = [class_id, x_center, y_center, bw, bh]

    # 多邊形逼近：對每個輪廓做 approx，然後再合併
    seg = []
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        epsilon = epsilon_ratio * peri
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        for pt in approx.squeeze():
            px = float(pt[0] / w)
            py = float(pt[1] / h)
            seg.extend([px, py])

    return seg, bbox

    '''
    模擬單條刮痕，從起點到終點繪製並加入隨機抖動與斷裂效果。

    @param img: 原始影像
    @param start_point: 刮痕起點座標 (x, y)
    @param end_point: 刮痕終點座標 (x, y)
    
    @return: 加入刮痕後的影像
    '''
    num_points = random.randint(SCRATCH_LENGTH_TURNING[0], SCRATCH_LENGTH_TURNING[1])
    path_points = np.linspace(start_point, end_point, num_points).astype(np.int32)
    path_points += np.random.randint(-JITTER, JITTER+1, size=path_points.shape)
    mask = np.zeros_like(img)
    for i in range(len(path_points) - 1):
        p1, p2 = tuple(path_points[i]), tuple(path_points[i+1])
        if random.random() < SKIP_PROBABILITY:  #模擬隨機斷裂
            continue
        thickness = max(1, int(np.random.normal(SCRATCH_THICKNESS, 1.2)))
        local_color, scratch_color = compute_scratch_color(img, p1) # 起始點顏色
        # print(scratch_color)
        cv2.line(mask, p1, p2, scratch_color.tolist(), thickness)
    # cv2.namedWindow(img_name,cv2.WINDOW_NORMAL)
    # cv2.imshow(img_name, mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    yolo_seg, yolo_bbox = get_segment_label(mask)
    
    if yolo_seg and yolo_bbox:
        if PRINT_BBOX:
            draw_yolo_box(img, yolo_bbox)
        return yolo_seg, blend_scratch(img, mask)
    else:
        return None, blend_scratch(img, mask)
    
def generate_scratch(img, start_point, end_point):
    '''
    模擬單條刮痕，從起點到終點繪製並加入隨機抖動與斷裂效果。

    @param img: 原始影像
    @param start_point: 刮痕起點座標 (x, y)
    @param end_point: 刮痕終點座標 (x, y)
    
    @return: 加入刮痕後的影像
    '''
    params = sample_scratch_params()
    SCRATCH_COUNT = params["SCRATCH_COUNT"]
    SCRATCH_THICKNESS = params["SCRATCH_THICKNESS"]
    DARKEN_FACTOR = params["DARKEN_FACTOR"]
    COLOR_VARIATION = params["COLOR_VARIATION"]
    JITTER = params["JITTER"]

    num_points = random.randint(SCRATCH_LENGTH_TURNING[0], SCRATCH_LENGTH_TURNING[1])
    path_points = np.linspace(start_point, end_point, num_points).astype(np.int32)
    path_points += np.random.randint(-JITTER, JITTER+1, size=path_points.shape)
    mask = np.zeros_like(img)
    for i in range(len(path_points) - 1):
        p1, p2 = tuple(path_points[i]), tuple(path_points[i+1])
        if random.random() < SKIP_PROBABILITY:  #模擬隨機斷裂
            continue
        thickness = max(1, int(np.random.normal(SCRATCH_THICKNESS, 1.2)))
        local_color, scratch_color = compute_scratch_color(img, p1) # 起始點顏色
        # print(scratch_color)
        cv2.line(mask, p1, p2, scratch_color.tolist(), thickness)
    # cv2.namedWindow(img_name,cv2.WINDOW_NORMAL)
    # cv2.imshow(img_name, mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    position, yolo_bbox = get_yolo_bbox(mask)
    
    if position and yolo_bbox:
        if PRINT_BBOX:
            draw_yolo_box(img, yolo_bbox)
        return yolo_bbox, blend_scratch(img, mask)
    else:
        return None, blend_scratch(img, mask)
    
def compute_scratch_color(img, point):
    '''
    計算刮痕顏色，根據原始畫面亮度混入隨機偏暗雜訊。

    @param img: 原始影像
    @param point: 指定像素點座標 (x, y)

    @return: (原始像素值, 加工後的刮痕顏色值)
    '''
    h, w, _ = img.shape
    y, x = np.clip(point[1], 0, h - 1), np.clip(point[0], 0, w - 1)
    base_color = img[y, x].astype(np.float32) * DARKEN_FACTOR            # 影像該位置的pixel變暗
    noise_val = np.random.randint(-COLOR_VARIATION, COLOR_VARIATION + 1) # 隨機上下浮動的pixel數值
    noise = np.full(3, noise_val, dtype=np.int32)
    scratch_color = np.clip(base_color + noise, 0, 255).astype(np.uint8)
    return img[y, x], scratch_color

def get_yolo_bbox(mask):
    '''
    根據 mask 取得 bounding box，並轉換為 YOLO 格式。

    @param mask: 刮痕mask影像

    @return: (像素座標範圍, YOLO 格式的 [x_center, y_center, width, height])
    '''
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    ys, xs = np.where(gray > 0)
    if len(xs) == 0 or len(ys) == 0:
        return None, None

    x_min, x_max, y_min, y_max = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    h, w = gray.shape
    x_center = float(round(((x_min + x_max) / 2) / w, 8))
    y_center = float(round(((y_min + y_max) / 2) / h, 8))
    box_w = float(round((x_max - x_min) / w, 8))
    box_h = float(round((y_max - y_min) / h, 8))

    return (x_min, y_min, x_max, y_max), (x_center, y_center, box_w, box_h)

def draw_yolo_box(img, bbox):
    '''
    在圖片上畫出 YOLO 格式的紅色方框。

    @param img: 原始影像
    @param bbox: (x_center, y_center, width, height) [YOLO 格式]
    '''
    x_center, y_center, box_w, box_h = bbox
    h, w, _ = img.shape
    abs_xc, abs_yc = x_center * w, y_center * h
    abs_w, abs_h = box_w * w, box_h * h
    x_min = max(0, int(abs_xc - abs_w / 2))
    y_min = max(0, int(abs_yc - abs_h / 2))
    x_max = min(w - 1, int(abs_xc + abs_w / 2))
    y_max = min(h - 1, int(abs_yc + abs_h / 2))
    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 0, 255), 1)

def blend_scratch(img, mask):
    '''
    利用 LAB 色域進行亮度減弱，將刮痕以自然方式融合到圖片中。

    @param img: 原始影像
    @param mask: 產生的刮痕mask (彩色)

    @return: 混合後的影像
    '''
    ksize = 5
    blurred = cv2.GaussianBlur(mask, (ksize, ksize), sigmaX=ksize/2)
    gray_mask = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_img)
    if SCRATCH_COLOR==1:
        l = cv2.add(l, (gray_mask*0.5).astype(np.uint8))
    elif SCRATCH_COLOR==0:
        l = cv2.subtract(l, (gray_mask * 0.5).astype(np.uint8))
    else:
        r = random.randint(0,1)
        if r%2 == 0:l = cv2.subtract(l, (gray_mask * 0.5).astype(np.uint8))
        else: l = cv2.add(l, (gray_mask*0.5).astype(np.uint8))
            
    blended = cv2.merge([l, a, b])

    
    # cv2.namedWindow('blended',cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('blended', l)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return cv2.cvtColor(blended, cv2.COLOR_LAB2BGR)

def random_line(img):
    '''
    在圖像中隨機生成一條線段座標，用於模擬刮痕的起點與終點。

    @param img: 原始影像

    @return: (start_point, end_point)
    '''
    h, w = img.shape[:2]
    start = (random.randint(0, w), random.randint(0, h))
    angle = random.uniform(0, 2*np.pi)
    length = random.randint(*SCRATCH_LENGTH)
    end = (int(start[0] + length * np.cos(angle)), int(start[1] + length * np.sin(angle)))
    return start, end

def get_detail_mask(img, mouse_mask):
    '''
    根據輸入的影像與滑鼠mask，自動產生更細緻的mask，
    回傳一個只保留主要物件區域（最大輪廓）的二值化 mask。

    @param img: 輸入的彩色影像
    @param mouse_mask: 輸入的滑鼠mask

    @return: 二值化 mask，物件區域為白色(255)，背景為黑色(0)
    '''
    h, w = img.shape[:2]

    # 先縮小影像至 h=160 保持長寬比
    r = 160.0 / img.shape[0] 
    dim = (int(img.shape[1] * r), 160)
    img = cv2.resize(img, dim, cv2.LINE_AA)
    mouse_mask = cv2.resize(mouse_mask, dim, cv2.LINE_AA)

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    _, _, v = cv2.split(hsv_img)
    # Canny 邊緣偵測 與 adaptiveThreshold 組合凸顯邊緣
    edges = cv2.Canny(v, 300, 100)
    adaptive = cv2.adaptiveThreshold(
        edges, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=11,
        C=2
    )
    # 讓形態學可以處理
    adaptive = cv2.bitwise_not(adaptive)
    # 閉運算 先膨脹後侵蝕 讓黑線不見
    kernel = np.ones((3, 3), np.uint8)
    adaptive = cv2.morphologyEx(adaptive, cv2.MORPH_CLOSE, kernel)
    adaptive = cv2.bitwise_not(adaptive)
    adaptive = cv2.bitwise_and(adaptive,mouse_mask)
    
    # 過濾太小的component(腳墊的地方)
    contours, hierarchy = cv2.findContours(adaptive,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #只檢測最外層輪廓
    
    # 找最大輪廓
    try:
        max_contour = max(contours, key=cv2.contourArea)
    except:
        return cv2.resize(mouse_mask, (w, h), interpolation=cv2.INTER_NEAREST)
    
    # 畫出最大輪廓
    max_contour_mask = np.zeros_like(adaptive)
    cv2.drawContours(max_contour_mask, [max_contour], -1, 255, -1)
    #再次bitwise and 讓原本內部不要的地方過濾掉
    adaptive = cv2.bitwise_and(adaptive,max_contour_mask)

    # 將mask resisze回原本大小
    adaptive_mask = cv2.resize(adaptive, (w, h), interpolation=cv2.INTER_NEAREST) 
    # cv2.namedWindow('adaptive_mask',cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('adaptive_mask', adaptive_mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return adaptive_mask


    base_name = os.path.splitext(img_name)[0]
    
    # === 1. Save bbox label in YOLO TXT ===
    bbox_txt_path = os.path.join(output_dir, "labels", base_name + ".txt")
    os.makedirs(os.path.dirname(bbox_txt_path), exist_ok=True)
    with open(bbox_txt_path, "w") as f:
        bbox_str = f"{class_id} " + " ".join([f"{x:.6f}" for x in yolo_bbox])
        f.write(bbox_str + "\n")
    
    # === 2. Save bbox label in JSON ===
    bbox_json_path = os.path.join(output_dir, "bbox_json", base_name + ".json")
    os.makedirs(os.path.dirname(bbox_json_path), exist_ok=True)
    bbox_data = {
        "image": img_name,
        "class_id": class_id,
        "bbox": yolo_bbox
    }
    with open(bbox_json_path, "w") as f:
        json.dump(bbox_data, f, indent=2)
    
    # === 3. Save segmentation label in YOLO TXT ===
    seg_txt_path = os.path.join(output_dir, "segments", base_name + ".txt")
    os.makedirs(os.path.dirname(seg_txt_path), exist_ok=True)
    seg_str = f"{class_id} " + " ".join([f"{x:.6f}" for x in yolo_seg])
    with open(seg_txt_path, "w") as f:
        f.write(seg_str + "\n")
    
    # === 4. Save segmentation label in JSON ===
    seg_json_path = os.path.join(output_dir, "segment_json", base_name + ".json")
    os.makedirs(os.path.dirname(seg_json_path), exist_ok=True)
    seg_data = {
        "image": img_name,
        "class_id": class_id,
        "segmentation": yolo_seg
    }
    with open(seg_json_path, "w") as f:
        json.dump(seg_data, f, indent=2)

def sample_points_by_kmeans(detail_mask):
    '''
    從mask中平均分散取得可生成之地點

    @param detail_mask: 輸入的滑鼠細緻mask

    @return: 起始點的list
    '''
    # 找到白色區域的所有(y, x)座標
    ys, xs = np.where(detail_mask == 255)
    # 把它們打包成一個座標列表
    points = np.stack([xs, ys], axis=1).astype(np.float32)  # 注意順序
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    if len(points) >= SCRATCH_COUNT:
        compactness, labels, centers = cv2.kmeans(points, SCRATCH_COUNT, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    # centers 是 kmeans 回傳的
    selected_points = []  # (K, 2)，每個中心點就是你要的點
    for (x_center, y_center) in centers:
            if KMEANS_RADIUS:
                # 從附近radius範圍內找白色點
                dists = np.sqrt((points[:,0] - x_center)**2 + (points[:,1] - y_center)**2)
                nearby_indices = np.where(dists <= KMEANS_RADIUS)[0]
                if len(nearby_indices) > 0:
                    idx = random.choice(nearby_indices)
                    selected_points.append((int(points[idx][0]), int(points[idx][1])))
                else:
                    # 找不到附近點，退回center
                    selected_points.append((int(x_center), int(y_center)))
            else:
                # 不開隨機，直接拿center
                selected_points.append((int(x_center), int(y_center)))
    # 顯示中心點
    # result = cv2.cvtColor(detail_mask, cv2.COLOR_GRAY2BGR)
    # for x, y in selected_points.astype(int):
    #     cv2.circle(result, (x, y), 15, (0, 255, 0), -1)
    return selected_points

def random_line_in_mask(img, mask, max_attempts=100, start_points=None):
    '''
    在 mask 為白的區域內，生成一條隨機線段（模擬刮痕）

    @param img: 原圖，用來取圖尺寸
    @param mask: mask圖，白色區域代表可畫刮痕
    @param max_attempts: 最多嘗試幾次找合格的線
    @param start_points: 是否有確定的起始點

    @return: (start_point, end_point) or None 若找不到
    '''
    h, w = img.shape[:2]
    return_points = {'start_points':[],
                     'end_points':[]}
    if start_points:
        for start in start_points:
            for _ in range(max_attempts):
                angle = random.uniform(0, 2*np.pi)
                length = random.randint(*SCRATCH_LENGTH)
                end = (
                    int(start[0] + length * np.cos(angle)),
                    int(start[1] + length * np.sin(angle))
                )
                # 確保終點也在影像範圍內
                if not (0 <= end[0] < w and 0 <= end[1] < h):
                    continue
                # 確認整條線是否在 mask 內
                line_mask = np.zeros_like(mask)
                cv2.line(line_mask, start, end, 255, 1)
                line_in_mask = cv2.bitwise_and(line_mask, mask)
                if np.array_equal(line_mask, line_in_mask):
                    return_points['start_points'].append(start)
                    return_points['end_points'].append(end)
                    break
        return return_points
    else:
        ys, xs = np.where(mask > 0)
        if len(xs) == 0:
            return None, None  # 沒有白色區域
        for _ in range(max_attempts):
            idx = random.randint(0, len(xs) - 1)
            start = (xs[idx], ys[idx])
            angle = random.uniform(0, 2*np.pi)
            length = random.randint(*SCRATCH_LENGTH)
            end = (
                int(start[0] + length * np.cos(angle)),
                int(start[1] + length * np.sin(angle))
            )

            # 確保終點也在影像範圍內
            if not (0 <= end[0] < w and 0 <= end[1] < h):
                continue

            # 確認整條線是否在 mask 內
            line_mask = np.zeros_like(mask)
            cv2.line(line_mask, start, end, 255, 1)
            line_in_mask = cv2.bitwise_and(line_mask, mask)
            if np.array_equal(line_mask, line_in_mask):
                return start, end

        return None, None  # 找不到合適的線段
    
def is_valid_mask(mask, min_white_ratio=0.05):
    white_pixels = np.sum(mask == 255)
    total_pixels = mask.shape[0] * mask.shape[1]
    return (white_pixels / total_pixels) >= min_white_ratio

def sample_scratch_params():
    return {
        "SCRATCH_COUNT": random.randint(*SCRATCH_COUNT_RANGE),
        "SCRATCH_THICKNESS": random.randint(*SCRATCH_THICKNESS_RANGE),
        "DARKEN_FACTOR": round(random.uniform(*DARKEN_FACTOR_RANGE), 2),
        "COLOR_VARIATION": random.randint(*COLOR_VARIATION_RANGE),
        "JITTER": random.randint(*JITTER_RANGE),
        "KMEANS_RADIUS" : random.randint(*KMEANS_RADIUS_RANGE),
    }

def extract_donut_ring(img):
    h, w = img.shape[:2]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 黃色範圍 (外圈)
    lower_yellow = np.array([10, 200, 200])
    upper_yellow = np.array([50, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # 膨脹黃色遮罩，讓輪廓變厚更易填滿
    kernel = np.ones((7,7), np.uint8)
    yellow_mask = cv2.dilate(yellow_mask, kernel, iterations=3)

    # 紅色範圍 (內圈)
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 50, 50])
    upper_red2 = np.array([180, 255, 255])
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # 找外圈輪廓並填滿
    contours_y, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yellow_filled = np.zeros((h, w), dtype=np.uint8)
    cv2.drawContours(yellow_filled, contours_y, -1, 255, thickness=cv2.FILLED)

    # 找內圈輪廓並填滿
    contours_r, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_filled = np.zeros((h, w), dtype=np.uint8)
    cv2.drawContours(red_filled, contours_r, -1, 255, thickness=cv2.FILLED)

    # 外圈實心 - 內圈實心 = 麵包區域
    donut_ring_mask = cv2.subtract(yellow_filled, red_filled)

    return donut_ring_mask

    h, w = img.shape[:2]
    # 轉為 HSV 以利選取黃色
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 定義黃色範圍 (適用 BGR=(0,242,255))
    lower_yellow = np.array([15, 200, 200])
    upper_yellow = np.array([50, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # cv2.namedWindow('yellow_mask',cv2.WINDOW_KEEPRATIO)
    # print("Non-zero pixels in yellow_mask:", cv2.countNonZero(yellow_mask))
    # cv2.imshow("yellow_mask", yellow_mask)
    # cv2.waitKey(0)

    # 膨脹黃色區域，確保輪廓連貫
    kernel = np.ones((5, 5), np.uint8)
    yellow_mask = cv2.dilate(yellow_mask, kernel, iterations=2)

    # 尋找黃色輪廓
    contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 建立空的遮罩
    final_mask = np.zeros((h, w), dtype=np.uint8)


    # cv2.namedWindow('final_mask',cv2.WINDOW_KEEPRATIO)
    # cv2.imshow('final_mask', final_mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



    # 填滿黃色輪廓「內部」的區域
    for cnt in contours:
        if cv2.contourArea(cnt) < 100:
            continue

        # 步驟 1：畫出黃色區域 temp_mask
        temp_mask = np.zeros((h, w), dtype=np.uint8)
        cv2.drawContours(temp_mask, [cnt], -1, 255, thickness=cv2.FILLED)

        # 步驟 2：region 是黃色區域內的實際圖像
        region = cv2.bitwise_and(img, img, mask=temp_mask)

        # 步驟 3：轉 HSV，偵測紅色區域
        region_hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
        lower_red1 = np.array([0, 50, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 50, 50])
        upper_red2 = np.array([180, 255, 255])
        red_mask1 = cv2.inRange(region_hsv, lower_red1, upper_red1)
        red_mask2 = cv2.inRange(region_hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)

        # 步驟 4：將紅色區域從 temp_mask 中挖空（設為 0）
        temp_mask[red_mask > 0] = 0

        # 步驟 5：加入 final_mask
        final_mask = cv2.bitwise_or(final_mask, temp_mask)

    return final_mask
    # cv2.imshow('result', cv2.resize(result, (h, w), cv2.LINE_AA))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # return mask

def make_scratch(args):
        
        BASE_FOLDER = args.base_path
        DATA_FOLDER = BASE_FOLDER
        SAVE_FOLDER = BASE_FOLDER + '/images'
        MERGE_LABEL_FOLDER = BASE_FOLDER + '/labels'
        OUT_FOLDER  = BASE_FOLDER + '/test'
        # SCRATCH_ID = args.scratch_id
        SCRATCH_ID = 3

        LABEL_FOLDER = args.bbox_path


        os.makedirs(MERGE_LABEL_FOLDER, exist_ok=True)

        try:
            shutil.rmtree(SAVE_FOLDER)
        except:
            pass
        os.makedirs(SAVE_FOLDER, exist_ok=True)

        for img_name in tqdm.tqdm(os.listdir(DATA_FOLDER)):
            print(img_name)

            if os.path.isdir(os.path.join(DATA_FOLDER, img_name)):
                continue
            if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue

            # === 隨機化超參數 ===
            params = sample_scratch_params()
            SCRATCH_COUNT = params["SCRATCH_COUNT"]
            SCRATCH_THICKNESS = params["SCRATCH_THICKNESS"]
            DARKEN_FACTOR = params["DARKEN_FACTOR"]
            COLOR_VARIATION = params["COLOR_VARIATION"]
            JITTER = params["JITTER"]

            img_path = os.path.join(DATA_FOLDER, img_name)
            img = cv2.imread(img_path)

            if img is None:
                print(f"無法讀取圖片: {img_name}")
                continue

            maskimg = cv2.imread("D:/aiagent/new_yolo_dataset/0.png")

            mouse_mask = extract_donut_ring(maskimg)

            if not is_valid_mask(mouse_mask):
                continue

            yolo_formate_list = []
            yolo_seg_formate_list = []
            if SEPARATE_LIMIT:
                start_points = sample_points_by_kmeans(mouse_mask)
                points = random_line_in_mask(img, mouse_mask, start_points=start_points)
                if points['start_points']:
                    for i in range(len(points['start_points'])):
                        yolo_formate, img = generate_scratch(img, points['start_points'][i], points['end_points'][i])
                        if yolo_formate:
                            yolo_formate_list.append(yolo_formate)
                else:
                    print('跳過')
                    break
            else:
                for _ in range(SCRATCH_COUNT):
                    sp, ep = random_line_in_mask(img, mouse_mask)
                    if sp and ep:
                        yolo_formate, img = generate_scratch(img, sp, ep)
                        if yolo_formate:
                            yolo_formate_list.append(yolo_formate)
                    else:
                        print('跳過')
                        break
            bbox_dir = os.path.join(SAVE_FOLDER, "bbox_labels")
            seg_dir = os.path.join(SAVE_FOLDER, "seg_labels")
            os.makedirs(bbox_dir, exist_ok=True)
            os.makedirs(seg_dir, exist_ok=True)
            if yolo_formate_list:
                txt_name = os.path.splitext(img_name)[0] + ".txt"
                with open(os.path.join(bbox_dir, txt_name), 'w') as fp:
                    for per in yolo_formate_list:
                        cls = SCRATCH_ID
                        fp.write(f'{cls} ')
                        for i in per:
                            # x_center = f"{float(per[0]):.6f}"
                            # y_center = f"{float(per[1]):.6f}"
                            # box_w    = f"{float(per[2]):.6f}"
                            # box_h    = f"{float(per[3]):.6f}"
                            fp.write(f'{f"{float(i):.6f}"} ')
                        fp.write(f'\n')
                cv2.imwrite(f'{SAVE_FOLDER}/{img_name}', img)
        close_polygon(SAVE_FOLDER, backup=True)
        copy_scratch_to_oldimage(bbox_dir,LABEL_FOLDER,MERGE_LABEL_FOLDER)

        dataset_dir = BASE_FOLDER
        output_dir = OUT_FOLDER
        splits = [""]
        os.makedirs(output_dir, exist_ok=True)

        for split in splits:
            image_dir = dataset_dir+split+"/images"
            label_dir = dataset_dir+split+"/labels"
            out_split_dir = os.path.join(output_dir, split)
            os.makedirs(out_split_dir, exist_ok=True)

            for file in os.listdir(image_dir):
                if not file.endswith(".jpg") and not file.endswith(".png"):
                    continue

                image_path = os.path.join(image_dir, file)
                label_path = os.path.join(label_dir, file.replace(".jpg", ".txt").replace(".png", ".txt"))

                image = cv2.imread(image_path)
                if image is None or not os.path.exists(label_path):
                    continue

                h, w = image.shape[:2]

                with open(label_path, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) != 5:
                            continue
                        cls, xc, yc, bw, bh = map(float, parts)
                        x1 = int((xc - bw / 2) * w)
                        y1 = int((yc - bh / 2) * h)
                        x2 = int((xc + bw / 2) * w)
                        y2 = int((yc + bh / 2) * h)

                        # 畫框和類別文字
                        cv2.rectangle(image, (x1, y1), (x2, y2), (20, 250, 20), 2)
                        cv2.putText(image, f"class {int(cls)}", (x1, y1 - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 250, 20), 1)

                # 儲存畫好框的圖片
                save_path = os.path.join(out_split_dir, file)
                cv2.imwrite(save_path, image)
                print(f"OK: Save to 儲存: {save_path}")

# ====== 可設定參數 ======
SEED = 2025                     # seed設定，每次執行產生順序相同
SCRATCH_COUNT = 8               # 要生成多少次刮痕
SCRATCH_LENGTH = (30, 300)      # 刮痕的最短到最長長度範圍
SCRATCH_LENGTH_TURNING = (1, 5) # 刮痕線段中間轉折點的範圍
SCRATCH_THICKNESS = 3           # 刮痕的基本粗度
COLOR_VARIATION = 5             # 隨機點的pixel值上下可浮動的範圍
SCRATCH_COLOR = 2               # 刮痕顏色(1 = 白色 / 0 = 黑色 / 2 = 隨機)
DARKEN_FACTOR = 0.5             # 刮痕融入程度(越大刮痕越明顯(假))
KMEANS_RADIUS = 3               # kmeans後從群中心隨機位移多少pixels#
# JITTER = 3                      # 線段抖動範圍
SKIP_PROBABILITY = 0.0          # 模擬斷裂機率
SEPARATE_LIMIT = True           # 是否平均散佈生成的地方
PRINT_BBOX = False              # 是否要繪製BBOX在圖形上(True/False)

#存的位置
# BASE_FOLDER = 'C:/Users/alex.ho/Downloads/Mouse.v15i.yolov11/train/1/'
# BASE_FOLDER = r"D:/aiagent/new_yolo_dataset/20260129/6"

SCRATCH_COUNT_RANGE = (4, 8)            # 生成刮痕的數量範圍
SCRATCH_LENGTH = (100, 400)             # 刮痕長度 (保持不變)
SCRATCH_THICKNESS_RANGE = (1, 2)        # 刮痕厚度範圍
DARKEN_FACTOR_RANGE = (0.2, 0.4)        # 融合程度範圍
COLOR_VARIATION_RANGE = (0, 1)          # 色差範圍
JITTER_RANGE = (0, 5)                   # 抖動範圍
KMEANS_RADIUS_RANGE = (0, 3)
BASE_LIGHT_BLUE = (255, 220, 180)  # 淺藍
BASE_DARK_BLUE = (230, 170, 80)    # 深藍
# =======================

if __name__ == '__main__':
    # random.seed(SEED)
    # np.random.seed(SEED)

    parser = argparse.ArgumentParser(description="YOLO RAG Processor")
    parser.add_argument("--base_path", type=str, required=True, help="Dataset folder")
    parser.add_argument("--bbox_path", type=str, required=True, help="Path to bbox label")
    # parser.add_argument("--scratch_id", type=str, required=True, help="Scratch id")
    args = parser.parse_args()

    make_scratch(args)

    

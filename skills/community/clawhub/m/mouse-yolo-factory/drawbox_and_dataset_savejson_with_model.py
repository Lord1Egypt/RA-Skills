from ultralytics import YOLO

import cv2

import time

import torch

import random

import os

import numpy as np

import torch.nn.functional as F

from torchvision import ops

from pathlib import Path

import json

import argparse

from collections import defaultdict

from datetime import datetime


# confidence_threshold = 0.2


required_classes = {"no-pad", "pad-climb", "pad-fit", "scratch"}


color_map = {

    "no-pad":(60,160,60),

    "pad-climb": (0, 0, 255),

    "pad-fit": (0, 255, 0),

    "scratch": (0, 0, 255),

    "no-middle-pad": (0, 0, 255),

    "middle-pad": (150, 50, 50),

    "middle-pad-climb": (100, 100, 250),

    "pad-damaged": (50, 50, 255)
}

# --- RAG 設定 ---
RAG_DB_PATH = Path("D:/aiagent/rag_database")
RAG_DB_PATH.mkdir(parents=True, exist_ok=True)
rag_history_file = RAG_DB_PATH / "detection_logs.jsonl"

def save_to_rag_log(image_name, detections):
    """將偵測結果存成 JSONL，方便 RAG 讀取"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "source_image": image_name,
        "objects_detected": detections,
        "summary": f"In image {image_name}, detected: " + 
                   ", ".join([f"{d['label']} (conf: {d['conf']:.2f})" for d in detections])
    }
    with open(rag_history_file, "a", encoding="utf-8") as f:
        f.write(json.dump_as_string(entry) if hasattr(json, 'dump_as_string') else json.dumps(entry, ensure_ascii=False) + "\n")

def get_unique_filename(directory, base_name, extension, count):

    """根據計數器產生唯一檔名，如 image_0001.jpg, image_0002.jpg"""

    return Path(directory) / f"{base_name}_{count:04d}.{extension}"

def letterbox(img, target_size=(1280, 1280), color=(255, 255, 255)):

	original_h, original_w = img.shape[:2]

	target_w, target_h = target_size
	
	scale = min(target_w / original_w, target_h / original_h)

	new_w = int(original_w * scale)

	new_h = int(original_h * scale)
	
	resized = cv2.resize(img, (new_w,new_h), interpolation=cv2.INTER_LINEAR)

	canva = np.full((target_h, target_w, 3), color, dtype=np.uint8)
	
	top = (target_h - new_h) // 2

	left = (target_w - new_w) // 2
	
	canva[top:top + new_h, left:left + new_w] = resized
	
	return canva, scale, left, top   


# Read model    

# choose_model = f"20251212_1747_stage3_white"

# openvino_path = "C:/Users/alex.ho/.qaihm/models/yolov11_det/v1/ultralytics_ultralytics_git/runs/detect/"+choose_model+"/weights/best_openvino_model/"

# pt_path       = "c:/Users/alex.ho/.qaihm/models/yolov11_det/v1/ultralytics_ultralytics_git/runs/detect/"+choose_model+"/weights/best.pt"

def run_inference(args):

    # if not os.path.exists(argparse.model_path):

    #     model = YOLO(pt_path)

    #     model.export(format="openvino", dynamic=True)

    # model = YOLO(openvino_path)

    model = YOLO(args.model_path)

    # base_path = f"C:/Users/alex.ho/Downloads/NG_WHITE/6"
    base_path = args.base_path
    save_img_dir    = Path(f"{base_path}/images_copy")
    image_folder   = Path(f"{base_path}/")
    save_label_dir  = Path(f"{base_path}/bbox_labels")
    output_dir      = Path(f"{base_path}/test")

    save_img_dir.mkdir(parents=True, exist_ok=True)
    save_label_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    save_count = 0

    imgsz = 1280

    for image_name in os.listdir(image_folder):

        image_path = os.path.join(image_folder, image_name)

        if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):

            continue

        frame = cv2.imread(image_path)

        if frame is None:

            print(f"Failed to read image: {image_name}")

            continue

        start_time = time.time()

        img, scale, pad_x, pad_y = letterbox(frame, (1280, 1280), color=(255, 255, 255))

        results = model(img, imgsz=1280 ,save=False)
        current_detections = [] # 用來存給 RAG 看的資料
        detected_classes = set()

        if len(results[0].boxes) > 0:

            detected_classes.clear()

            boxes       = []

            scores      = []

            labels      = []

            class_ids   = []

            for box in results[0].boxes:

                confidence = box.conf[0].item()

                if confidence < args.conf:

                    continue

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                x1 = int((x1 - pad_x) / scale)

                y1 = int((y1 - pad_y) / scale)

                x2 = int((x2 - pad_x) / scale)

                y2 = int((y2 - pad_y) / scale)

                class_id = int(box.cls[0])

                label = results[0].names[class_id]

                boxes.append([x1, y1, x2, y2])

                scores.append(confidence)

                labels.append(label)

                class_ids.append(class_id)

                img_filename = os.path.join(save_img_dir, image_name)

                base_name = os.path.splitext(os.path.basename(img_filename))[0]

                label_filename = base_name + ".txt"

                label_path = os.path.join(save_label_dir, label_filename)

                with open(label_path, "w") as f:

                    original_h, original_w = frame.shape[:2] # 獲取原始圖像的寬度和高度

                    target_size = 1280

                    all_boxes = results[0].boxes.xyxy.cpu().numpy()

                    all_scores = results[0].boxes.conf.cpu().numpy()

                    all_classes = results[0].boxes.cls.cpu().numpy()

                    # 應用 NMS

                    keep_indices = ops.nms(torch.tensor(all_boxes), torch.tensor(all_scores), iou_threshold=0.3).cpu().numpy()

                    for index in keep_indices:

                        box = all_boxes[index]

                        score = all_scores[index]

                        cls_id = int(all_classes[index])

                        if score >= args.conf:

                            x1, y1, x2, y2 = box

                            # 將座標還原到原始圖像尺寸並歸一化

                            x1_orig = (x1 - pad_x) / scale / original_w

                            y1_orig = (y1 - pad_y) / scale / original_h

                            x2_orig = (x2 - pad_x) / scale / original_w

                            y2_orig = (y2 - pad_y) / scale / original_h



                            x = x1_orig + (x2_orig - x1_orig)/2

                            y = y1_orig + (y2_orig - y1_orig)/2

                            w = (x2_orig - x1_orig)

                            h = (y2_orig - y1_orig)

                            # 收集給 RAG 的結構化資訊
                            current_detections.append({
                                "label": label,
                                "conf": float(score),
                                "class_id": cls_id
                            })

                        f.write(f"{cls_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")

                    # --- 關鍵步驟：寫入 RAG 知識庫 ---
                    if current_detections:
                        save_to_rag_log(image_name, current_detections)

            if boxes:

                boxes_tensor = torch.tensor(boxes, dtype=torch.float32)

                scores_tensor = torch.tensor(scores, dtype=torch.float32)

                keep = ops.nms(boxes_tensor, scores_tensor, iou_threshold=0.3)


                img_with_boxes = frame.copy()


                for i in keep:
                    
                    x1, y1, x2, y2 = map(int, boxes[i])

                    label = labels[i]

                    detected_classes.add(label)

                    color = color_map.get(label, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

                    cv2.rectangle(img_with_boxes, (x1, y1), (x2, y2), color, 2)

                    cv2.putText(img_with_boxes, f"{label} {scores[i]:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        else:

            img_with_boxes = frame.copy()

        output_image_path = os.path.join(output_dir,f"output_{image_name}")

        cv2.imwrite(output_image_path, img_with_boxes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLO RAG Processor")
    parser.add_argument("--base_path", type=str, required=True, help="Input dataset folder")
    parser.add_argument("--model_path", type=str, required=True, help="Path to best.pt or openvino model")
    parser.add_argument("--conf", type=float, default=0.2, help="Confidence threshold")
    parser.add_argument("--imgsz", type=int, default=1280, help="Inference image size")
    
    args = parser.parse_args()
    run_inference(args)


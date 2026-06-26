#!/usr/bin/env python3
"""
人脸识别相似度比对脚本
支持两种模式：
  - 方案A: YuNet (检测) + SFace (识别) — 高精度，需要 ONNX 模型文件
  - 方案B: Haar Cascade (检测) + HOG+Patch (识别) — 通用，仅需 OpenCV 内置
"""

import argparse
import sys
import os
import numpy as np
import cv2
from scipy.spatial.distance import cosine
from PIL import Image, ImageDraw, ImageFont
import io

# ─────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────

# ONNX 模型路径（方案A）— 可通过环境变量或命令行指定
YUNET_MODEL_PATHS = [
    os.environ.get("YUNET_MODEL", ""),
    "/tmp/face_detection_yunet_2023mar.onnx",
    "./face_detection_yunet_2023mar.onnx",
    os.path.join(os.path.dirname(__file__), "face_detection_yunet_2023mar.onnx"),
]

SFACE_MODEL_PATHS = [
    os.environ.get("SFACE_MODEL", ""),
    "/tmp/face_recognition_sface_2021dec.onnx",
    "./face_recognition_sface_2021dec.onnx",
    os.path.join(os.path.dirname(__file__), "face_recognition_sface_2021dec.onnx"),
]

# 相似度阈值（方案B: HOG+Patch 余弦相似度）
THRESHOLD_B = {
    "same_person":    0.75,  # 高于此值：同一人
    "likely_same":    0.60,  # 高于此值：可能同一人
    "uncertain":      0.40,  # 高于此值：不确定
}

# 相似度阈值（方案A: SFace 余弦相似度，值越高越相似）
THRESHOLD_A = {
    "same_person":    0.593,  # 官方推荐阈值
}


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def find_model_file(paths: list) -> str | None:
    """查找第一个存在的模型文件路径"""
    for p in paths:
        if p and os.path.isfile(p):
            return p
    return None


def load_image(path: str) -> np.ndarray:
    """读取图片，支持 JPG/PNG/BMP/WEBP 等格式"""
    img = cv2.imread(path)
    if img is None:
        # 尝试 PIL 读取（支持更多格式）
        try:
            pil_img = Image.open(path).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception:
            raise ValueError(f"无法读取图片：{path}，请确认文件存在且格式支持（JPG/PNG/BMP/WEBP）")
    return img


# ─────────────────────────────────────────────
# 方案A：YuNet + SFace
# ─────────────────────────────────────────────

class FaceCompareYuNetSFace:
    """高精度人脸比对：YuNet 检测 + SFace 特征提取"""

    def __init__(self, yunet_path: str, sface_path: str):
        self.detector = cv2.FaceDetectorYN.create(
            yunet_path, "", (320, 320), score_threshold=0.5, nms_threshold=0.3, top_k=5000
        )
        self.recognizer = cv2.FaceRecognizerSF.create(sface_path, "")

    def detect_faces(self, img: np.ndarray) -> list[dict]:
        """检测图片中所有人脸，返回检测结果列表"""
        h, w = img.shape[:2]
        self.detector.setInputSize((w, h))
        _, faces = self.detector.detect(img)
        if faces is None:
            return []
        results = []
        for face in faces:
            # face: [x, y, w, h, right_eye_x, right_eye_y, left_eye_x, left_eye_y,
            #        nose_x, nose_y, right_mouth_x, right_mouth_y, left_mouth_x, left_mouth_y, score]
            x, y, fw, fh = int(face[0]), int(face[1]), int(face[2]), int(face[3])
            score = float(face[14])
            results.append({
                "bbox": (x, y, fw, fh),
                "landmarks": face[4:14].reshape(5, 2),
                "score": score,
                "face_data": face
            })
        # 按置信度降序排列
        results.sort(key=lambda r: r["score"], reverse=True)
        return results

    def get_largest_face(self, img: np.ndarray) -> tuple[dict | None, np.ndarray | None]:
        """获取最大人脸及其对齐后的图像"""
        faces = self.detect_faces(img)
        if not faces:
            return None, None
        # 取面积最大的人脸
        largest = max(faces, key=lambda f: f["bbox"][2] * f["bbox"][3])
        aligned = self.recognizer.alignCrop(img, largest["face_data"])
        return largest, aligned

    def extract_feature(self, aligned_face: np.ndarray) -> np.ndarray:
        """提取人脸特征向量（128维）"""
        return self.recognizer.feature(aligned_face).flatten()

    def compare(self, img1: np.ndarray, img2: np.ndarray) -> dict:
        """比对两张图片中的人脸，返回相似度信息"""
        face1_info, aligned1 = self.get_largest_face(img1)
        face2_info, aligned2 = self.get_largest_face(img2)

        if face1_info is None:
            return {"error": "图片1中未检测到人脸"}
        if face2_info is None:
            return {"error": "图片2中未检测到人脸"}

        feat1 = self.extract_feature(aligned1)
        feat2 = self.extract_feature(aligned2)

        # SFace 余弦相似度（越大越相似）
        cos_score = self.recognizer.match(aligned1, feat1, aligned2, feat2, cv2.FaceRecognizerSF_FR_COSINE)
        # L2 距离（越小越相似）
        l2_score = self.recognizer.match(aligned1, feat1, aligned2, feat2, cv2.FaceRecognizerSF_FR_NORM_L2)

        # 将余弦相似度映射到 [0,1]（原始范围 [-1,1]）
        normalized = (float(cos_score) + 1) / 2

        return {
            "method": "SFace (OpenCV FaceRecognizerSF)",
            "face1_bbox": face1_info["bbox"],
            "face2_bbox": face2_info["bbox"],
            "face1_confidence": face1_info["score"],
            "face2_confidence": face2_info["score"],
            "cosine_similarity": float(cos_score),
            "l2_distance": float(l2_score),
            "similarity_score": normalized,
            "is_same_person": float(cos_score) >= THRESHOLD_A["same_person"],
        }


# ─────────────────────────────────────────────
# 方案B：Haar Cascade + HOG + Patch Histogram
# ─────────────────────────────────────────────

class FaceCompareHaarHOG:
    """通用人脸比对：Haar Cascade 检测 + HOG/Patch 特征提取"""

    def __init__(self):
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        if self.face_cascade.empty():
            raise RuntimeError("无法加载 Haar Cascade 分类器")
        self.feature_size = (128, 128)
        self.hog = cv2.HOGDescriptor(
            self.feature_size, (16, 16), (8, 8), (8, 8), 9
        )

    def detect_faces(self, img: np.ndarray) -> list[tuple]:
        """检测图片中所有正面人脸，返回 [(x, y, w, h), ...]"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 直方图均衡化改善低光照
        gray = cv2.equalizeHist(gray)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=5,
            minSize=(40, 40),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if len(faces) == 0:
            # 降低阈值再试一次
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(20, 20),
            )
        return [tuple(f) for f in faces] if len(faces) > 0 else []

    def crop_face(self, img: np.ndarray, bbox: tuple, margin: float = 0.25) -> np.ndarray:
        """裁剪人脸区域，加边距"""
        x, y, w, h = bbox
        mw, mh = int(w * margin), int(h * margin)
        x1 = max(0, x - mw)
        y1 = max(0, y - mh)
        x2 = min(img.shape[1], x + w + mw)
        y2 = min(img.shape[0], y + h + mh)
        return img[y1:y2, x1:x2]

    def extract_feature(self, face_img: np.ndarray) -> np.ndarray:
        """提取 HOG + 分块直方图特征"""
        resized = cv2.resize(face_img, self.feature_size)
        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

        # 1. HOG 特征（形状/纹理）
        hog_feat = self.hog.compute(gray).flatten()
        hog_norm = hog_feat / (np.linalg.norm(hog_feat) + 1e-8)

        # 2. 分块颜色直方图（4x4 网格）
        def patch_hist(img, grid=(4, 4), bins=16):
            h, w = img.shape
            ph, pw = h // grid[0], w // grid[1]
            feats = []
            for i in range(grid[0]):
                for j in range(grid[1]):
                    patch = img[i*ph:(i+1)*ph, j*pw:(j+1)*pw]
                    hist, _ = np.histogram(patch, bins=bins, range=(0, 256))
                    feats.extend(hist.astype(np.float32))
            return np.array(feats)

        patch_feat = patch_hist(gray)
        patch_norm = patch_feat / (np.linalg.norm(patch_feat) + 1e-8)

        return np.concatenate([hog_norm, patch_norm])

    def get_largest_face(self, img: np.ndarray) -> tuple[tuple | None, np.ndarray | None]:
        """获取最大人脸的 bbox 和裁剪图"""
        faces = self.detect_faces(img)
        if not faces:
            return None, None
        largest = max(faces, key=lambda f: f[2] * f[3])
        cropped = self.crop_face(img, largest)
        return largest, cropped

    def compare(self, img1: np.ndarray, img2: np.ndarray) -> dict:
        """比对两张图片中的人脸"""
        bbox1, face1 = self.get_largest_face(img1)
        bbox2, face2 = self.get_largest_face(img2)

        if bbox1 is None:
            return {"error": "图片1中未检测到人脸，请确认图片中有清晰的正脸"}
        if bbox2 is None:
            return {"error": "图片2中未检测到人脸，请确认图片中有清晰的正脸"}

        feat1 = self.extract_feature(face1)
        feat2 = self.extract_feature(face2)

        cos_sim = float(1 - cosine(feat1, feat2))
        # 映射到 [0,1]
        normalized = (cos_sim + 1) / 2

        return {
            "method": "HOG + Patch Histogram (Haar Cascade)",
            "face1_bbox": bbox1,
            "face2_bbox": bbox2,
            "cosine_similarity": cos_sim,
            "similarity_score": normalized,
            "is_same_person": normalized >= THRESHOLD_B["same_person"],
        }


# ─────────────────────────────────────────────
# 相似度评级
# ─────────────────────────────────────────────

def interpret_score(score: float, method: str) -> dict:
    """将相似度分数转换为人类可读的评级"""
    if "SFace" in method:
        # SFace 余弦相似度（原始值）
        raw = score * 2 - 1  # 还原余弦值
        if raw >= 0.593:
            level, emoji = "极高概率为同一人", "✅"
        elif raw >= 0.45:
            level, emoji = "很可能为同一人", "✅"
        elif raw >= 0.30:
            level, emoji = "可能为同一人（建议人工核验）", "⚠️"
        elif raw >= 0.10:
            level, emoji = "不确定", "❓"
        else:
            level, emoji = "很可能不是同一人", "❌"
    else:
        # HOG 方案
        if score >= THRESHOLD_B["same_person"]:
            level, emoji = "很可能为同一人", "✅"
        elif score >= THRESHOLD_B["likely_same"]:
            level, emoji = "可能为同一人（建议人工核验）", "⚠️"
        elif score >= THRESHOLD_B["uncertain"]:
            level, emoji = "不确定", "❓"
        else:
            level, emoji = "很可能不是同一人", "❌"

    return {"level": level, "emoji": emoji}


# ─────────────────────────────────────────────
# 可视化输出
# ─────────────────────────────────────────────

def draw_result_image(img1: np.ndarray, img2: np.ndarray, result: dict, output_path: str):
    """生成带人脸框标注的对比结果图"""
    TARGET_H = 300
    
    def resize_keep_ratio(img, height):
        h, w = img.shape[:2]
        ratio = height / h
        return cv2.resize(img, (int(w * ratio), height))

    img1_r = resize_keep_ratio(img1.copy(), TARGET_H)
    img2_r = resize_keep_ratio(img2.copy(), TARGET_H)

    # 在原始图上画框（缩放 bbox）
    def scale_bbox(bbox, orig_h, new_h):
        scale = new_h / orig_h
        x, y, w, h = [int(v * scale) for v in bbox]
        return (x, y, w, h)

    if "face1_bbox" in result:
        h1 = img1.shape[0]
        sb1 = scale_bbox(result["face1_bbox"], h1, TARGET_H)
        x, y, w, h = sb1
        cv2.rectangle(img1_r, (x, y), (x+w, y+h), (0, 200, 0), 2)
        cv2.putText(img1_r, "Face A", (x, max(y-8, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,200,0), 2)

    if "face2_bbox" in result:
        h2 = img2.shape[0]
        sb2 = scale_bbox(result["face2_bbox"], h2, TARGET_H)
        x, y, w, h = sb2
        cv2.rectangle(img2_r, (x, y), (x+w, y+h), (0, 200, 0), 2)
        cv2.putText(img2_r, "Face B", (x, max(y-8, 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,200,0), 2)

    # 拼接两图
    gap = np.ones((TARGET_H, 20, 3), dtype=np.uint8) * 240
    combined = np.hstack([img1_r, gap, img2_r])

    # 添加结果文字横幅
    score = result.get("similarity_score", 0)
    interp = interpret_score(score, result.get("method", ""))
    banner_h = 70
    banner = np.ones((banner_h, combined.shape[1], 3), dtype=np.uint8) * 30

    score_text = f"Similarity: {score:.3f}   {interp['emoji']} {interp['level']}"
    method_text = f"Method: {result.get('method', 'N/A')}"

    cv2.putText(banner, score_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(banner, method_text, (20, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (180, 180, 180), 1)

    final = np.vstack([combined, banner])
    cv2.imwrite(output_path, final)


# ─────────────────────────────────────────────
# 主程序
# ─────────────────────────────────────────────

def run_comparison(img1_path: str, img2_path: str, output_path: str | None = None,
                   yunet_path: str | None = None, sface_path: str | None = None) -> dict:
    """
    执行人脸比对主流程。

    Args:
        img1_path: 图片1路径
        img2_path: 图片2路径
        output_path: 输出对比图路径（可选）
        yunet_path: YuNet 模型路径（可选，覆盖自动搜索）
        sface_path: SFace 模型路径（可选，覆盖自动搜索）

    Returns:
        dict: 包含 similarity_score, method, is_same_person 等字段
    """
    img1 = load_image(img1_path)
    img2 = load_image(img2_path)

    # 尝试方案A
    yunet = yunet_path or find_model_file(YUNET_MODEL_PATHS)
    sface = sface_path or find_model_file(SFACE_MODEL_PATHS)

    comparator = None
    if yunet and sface:
        try:
            comparator = FaceCompareYuNetSFace(yunet, sface)
            print(f"✓ 使用方案A：YuNet + SFace（高精度模式）")
        except Exception as e:
            print(f"⚠ 方案A 初始化失败：{e}，降级到方案B")
            comparator = None

    if comparator is None:
        comparator = FaceCompareHaarHOG()
        print(f"✓ 使用方案B：Haar Cascade + HOG（通用模式）")
        print(f"  提示：如需更高精度，请下载 YuNet/SFace 模型文件到 /tmp/ 目录")

    result = comparator.compare(img1, img2)

    if "error" in result:
        print(f"\n❌ 错误：{result['error']}")
        return result

    # 解读分数
    interp = interpret_score(result["similarity_score"], result.get("method", ""))
    result["interpretation"] = interp

    # 生成可视化输出
    if output_path:
        try:
            draw_result_image(img1, img2, result, output_path)
            result["output_image"] = output_path
            print(f"✓ 对比结果图已保存：{output_path}")
        except Exception as e:
            print(f"⚠ 生成输出图时出错：{e}")

    # 打印结果
    print(f"\n{'━'*45}")
    print(f"📊 人脸识别结果")
    print(f"{'━'*45}")
    print(f"图片A：{os.path.basename(img1_path)}  人脸框: {result.get('face1_bbox', 'N/A')}")
    print(f"图片B：{os.path.basename(img2_path)}  人脸框: {result.get('face2_bbox', 'N/A')}")
    print(f"")
    print(f"相似度分数：{result['similarity_score']:.4f}")
    print(f"判断结论：{interp['emoji']} {interp['level']}")
    print(f"使用算法：{result['method']}")
    print(f"{'━'*45}\n")

    return result


def main():
    parser = argparse.ArgumentParser(description="人脸识别相似度比对工具")
    parser.add_argument("--img1", required=True, help="第一张图片路径")
    parser.add_argument("--img2", required=True, help="第二张图片路径")
    parser.add_argument("--output", default=None, help="输出对比图路径（可选）")
    parser.add_argument("--yunet", default=None, help="YuNet ONNX 模型路径（可选）")
    parser.add_argument("--sface", default=None, help="SFace ONNX 模型路径（可选）")
    args = parser.parse_args()

    result = run_comparison(args.img1, args.img2, args.output, args.yunet, args.sface)
    if "error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()

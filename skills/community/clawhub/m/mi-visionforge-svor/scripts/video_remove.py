"""
视频目标消除工具 - 命令行版本
用法:
  1. 先跑分割获取 VLM 推荐:
     python video_remove.py --video <path> --segment --classes "label1:text1:remove_prompt1" "label2:text2:remove_prompt2"

  2. 根据 VLM 推荐，跑消除:
     python video_remove.py --video <path> --skip-segment --targets "label1:1,2,3" "label2:1"

  3. 一步到位（适合单类、文本提示有效的情况）:
     python video_remove.py --video <path> --classes "sign:sign:remove the sign" --targets "sign:2,3"

  4. 使用框标注（文本提示无效时）:
     python video_remove.py --video <path> --segment --classes "obj:cup:remove the cup" --boxes "obj:0.15,0.7,0.3,0.25"

  5. 使用点标注:
     python video_remove.py --video <path> --segment --classes "obj:cup:remove the cup" --points "obj:0.25,0.75"
"""
import argparse
import requests
import subprocess
import time
import json
import os
import sys
import shutil

# 修复 Windows 控制台中文乱码
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    

BASE_URL = "https://mipixgen-pre.ai.mioffice.cn"
SVOR_API_KEY = os.environ.get("SVOR_API_KEY")
if not SVOR_API_KEY:
    print("Error: 环境变量 SVOR_API_KEY 未设置。请先设置: export SVOR_API_KEY=<your_key>")
    sys.exit(1)
HEADERS = {"Authorization": f"Bearer {SVOR_API_KEY}"}


def compress_video(input_path, output_path, scale=512):
    cmd = ["ffmpeg", "-i", input_path, "-vf", f"scale={scale}:-2", "-crf", "32", "-y", output_path]
    subprocess.run(cmd, check=True, capture_output=True)


def submit_segmentation(video_path, **kwargs):
    with open(video_path, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/customize/xiaomi-ev/video_obj_removal/customize/v1/videos/sam3_prompt_seg",
            headers=HEADERS,
            files={"input_video": f},
            data=kwargs
        )
    return resp.json()


def poll_task(endpoint, task_id, max_wait=300):
    for i in range(max_wait // 3):
        time.sleep(3)
        resp = requests.get(f"{BASE_URL}{endpoint}/status/{task_id}", headers=HEADERS)
        data = resp.json()
        status = data.get("status")
        print(f"  [{i*3}s] Status: {status}")
        if status == "completed":
            return data
        elif status == "failed":
            raise Exception(f"Task failed: {data.get('error_message')}")
    raise Exception("Task timeout")


def download_result(url, output_path):
    resp = requests.get(url)
    with open(output_path, "wb") as f:
        f.write(resp.content)


def convert_mask_multi(input_mask, output_mask, target_ids):
    if not target_ids:
        cmd = ["ffmpeg", "-i", input_mask, "-vf", "geq=lum='0'", "-pix_fmt", "gray", "-y", output_mask]
    else:
        conditions = "+".join([f"eq(lum(X,Y),{tid})" for tid in target_ids])
        cmd = ["ffmpeg", "-i", input_mask, "-vf", f"geq=lum='if({conditions},255,0)'", "-pix_fmt", "gray", "-y", output_mask]
    subprocess.run(cmd, check=True, capture_output=True)


def merge_masks(mask_list, output_path):
    if len(mask_list) == 1:
        shutil.copy2(mask_list[0], output_path)
        return
    current = mask_list[0]
    for i in range(1, len(mask_list)):
        tmp_out = output_path if i == len(mask_list) - 1 else f"{output_path}_tmp_{i}.mp4"
        cmd = [
            "ffmpeg", "-i", current, "-i", mask_list[i],
            "-filter_complex", "[0:v][1:v]blend=all_mode=lighten:all_opacity=1",
            "-pix_fmt", "gray", "-y", tmp_out
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        if current != mask_list[0] and os.path.exists(current):
            os.remove(current)
        current = tmp_out


def run_segmentation(input_video, label, text="", remove_prompt="", tmp_dir="", base_name="",
                     points=None, point_labels=None, bounding_boxes=None, bounding_box_labels=None,
                     frame_index=0):
    print(f"\n=== Segment '{label}' (frame={frame_index}) ===")
    seg_data_kwargs = {"frame_index": frame_index}
    if text:
        seg_data_kwargs["text"] = text
    if remove_prompt:
        seg_data_kwargs["remove_prompt"] = remove_prompt
    if points:
        seg_data_kwargs["points"] = json.dumps(points)
        seg_data_kwargs["point_labels"] = json.dumps(point_labels if point_labels else [1] * len(points))
    if bounding_boxes:
        seg_data_kwargs["bounding_boxes"] = json.dumps(bounding_boxes)
        seg_data_kwargs["bounding_box_labels"] = json.dumps(bounding_box_labels if bounding_box_labels else [1] * len(bounding_boxes))

    seg_result = submit_segmentation(input_video, **seg_data_kwargs)
    print(f"  Response code: {seg_result.get('code')}")

    if seg_result.get("code") != 0:
        print(f"  Error: {seg_result}")
        return None, {}, None

    seg_task_id = seg_result["task_id"]
    print(f"  Task ID: {seg_task_id}")
    seg_data = poll_task("/customize/xiaomi-ev/video_obj_removal/customize/v1/videos/sam3_prompt_seg", seg_task_id)

    suggest = seg_data["extra_info"].get("suggest_obj", "")
    obj_boxes = seg_data["extra_info"].get("object_boxes", {})
    print(f"\n  [VLM Suggestion] {suggest}")
    print(f"  [Detected Objects] {obj_boxes}")

    mask_raw = os.path.join(tmp_dir, f"{base_name}_mask_{label}_raw.mkv")
    download_result(seg_data["video_path"], mask_raw)
    print(f"  Mask downloaded: {mask_raw}")

    return suggest, obj_boxes, mask_raw


def parse_classes(classes_str_list):
    """解析 --classes 参数: label:text:remove_prompt"""
    tasks = []
    for item in classes_str_list:
        parts = item.split(":", 2)
        label = parts[0]
        text = parts[1] if len(parts) > 1 else ""
        remove_prompt = parts[2] if len(parts) > 2 else ""
        tasks.append({"label": label, "text": text, "remove_prompt": remove_prompt})
    return tasks


def parse_targets(targets_str_list):
    """解析 --targets 参数: label:1,2,3"""
    result = {}
    for item in targets_str_list:
        label, ids_str = item.split(":", 1)
        result[label] = [int(x) for x in ids_str.split(",")]
    return result


def parse_boxes(boxes_str_list):
    """解析 --boxes 参数: label:x,y,w,h"""
    result = {}
    for item in boxes_str_list:
        label, coords = item.split(":", 1)
        x, y, w, h = [float(v) for v in coords.split(",")]
        result[label] = [[x, y, w, h]]
    return result


def parse_points(points_str_list):
    """解析 --points 参数: label:x,y"""
    result = {}
    for item in points_str_list:
        label, coords = item.split(":", 1)
        x, y = [float(v) for v in coords.split(",")]
        result[label] = [[x, y]]
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="视频目标消除工具")
    parser.add_argument("--video", required=True, help="输入视频路径")
    parser.add_argument("--classes", nargs="+", help="分割类别，格式: label:text:remove_prompt")
    parser.add_argument("--targets", nargs="+", help="目标 ID，格式: label:1,2,3")
    parser.add_argument("--boxes", nargs="+", help="框标注，格式: label:x,y,w,h (归一化 0~1)")
    parser.add_argument("--points", nargs="+", help="点标注，格式: label:x,y (归一化 0~1)")
    parser.add_argument("--segment", action="store_true", help="仅跑分割，打印 VLM 推荐")
    parser.add_argument("--skip-segment", action="store_true", help="跳过分割（使用缓存 mask）")
    parser.add_argument("--frame", type=int, default=0, help="标注帧序号（0-based），默认 0")
    parser.add_argument("--tmp-dir", default=None, help="临时文件目录，默认 ./temp/")
    args = parser.parse_args()

    # 路径设置
    input_video = args.video
    video_dir = os.path.dirname(os.path.abspath(input_video))
    base_name = os.path.splitext(os.path.basename(input_video))[0]
    tmp_dir = args.tmp_dir or os.path.join(video_dir, "temp")
    os.makedirs(tmp_dir, exist_ok=True)

    # 解析参数
    classes = parse_classes(args.classes) if args.classes else []
    targets_map = parse_targets(args.targets) if args.targets else {}
    boxes_map = parse_boxes(args.boxes) if args.boxes else {}
    points_map = parse_points(args.points) if args.points else {}

    # ===== Step 1: 压缩视频 =====
    print("=== Step 1: Compress video ===")
    file_size = os.path.getsize(input_video)
    print(f"Original file size: {file_size / 1024:.1f} KB")
    input_tmp = os.path.join(tmp_dir, f"{base_name}_input.mp4")
    shutil.copy2(input_video, input_tmp)
    compressed = os.path.join(tmp_dir, f"{base_name}_compressed.mp4")
    if file_size > 200 * 1024:
        compress_video(input_tmp, compressed)
        input_for_seg = compressed
        print(f"Compressed: {compressed}")
    else:
        input_for_seg = input_tmp
        print("File size OK, no compression needed")

    # ===== Step 2: 分割 =====
    segmentation_results = {}
    if not args.skip_segment:
        for cls in classes:
            label = cls["label"]
            cached_mask = os.path.join(tmp_dir, f"{base_name}_mask_{label}_raw.mkv")
            if os.path.exists(cached_mask):
                print(f"\n=== Skip '{label}': cached mask found ===")
                segmentation_results[label] = {"suggest": "(cached)", "obj_boxes": {}, "mask_raw": cached_mask}
                continue

            suggest, obj_boxes, mask_raw = run_segmentation(
                input_for_seg,
                label=label,
                text=cls["text"],
                remove_prompt=cls["remove_prompt"],
                tmp_dir=tmp_dir,
                base_name=base_name,
                points=points_map.get(label),
                bounding_boxes=boxes_map.get(label),
                frame_index=args.frame,
            )
            segmentation_results[label] = {"suggest": suggest, "obj_boxes": obj_boxes, "mask_raw": mask_raw}

    # ===== 仅分割模式：打印结果并退出 =====
    if args.segment:
        print("\n" + "=" * 60)
        print("  VLM 推荐结果汇总（请据此填写 --targets 参数）")
        print("=" * 60)
        for label, info in segmentation_results.items():
            print(f"\n  [{label}]")
            print(f"    VLM: {info['suggest']}")
            print(f"    Objects: {info['obj_boxes']}")
            print(f"    → --targets \"{label}:<obj_id>,...\"")
        sys.exit(0)

    # ===== 检查 targets 是否齐全 =====
    if not targets_map:
        print("Error: 请通过 --targets 指定每类目标的 obj_id")
        sys.exit(1)

    # ===== Step 3: 转换 mask =====
    print("\n=== Step 3: Convert masks ===")
    all_mask_files = []
    for label, target_ids in targets_map.items():
        info = segmentation_results.get(label)
        if not info:
            cached_mask = os.path.join(tmp_dir, f"{base_name}_mask_{label}_raw.mkv")
            if os.path.exists(cached_mask):
                info = {"mask_raw": cached_mask}
            else:
                print(f"  Skip '{label}': no segmentation result")
                continue
        print(f"  Convert '{label}': target_ids={target_ids}")
        mask_final = os.path.join(tmp_dir, f"{base_name}_mask_{label}_final.mp4")
        convert_mask_multi(info["mask_raw"], mask_final, target_ids)
        all_mask_files.append(mask_final)

    if not all_mask_files:
        print("No masks to process. Exiting.")
        sys.exit(1)

    # ===== Step 4: 合并 mask =====
    print(f"\n=== Step 4: Merge {len(all_mask_files)} masks ===")
    mask_merged = os.path.join(tmp_dir, f"{base_name}_mask_merged.mp4")
    merge_masks(all_mask_files, mask_merged)
    print(f"Merged mask: {mask_merged}")

    # ===== Step 5: 消除 =====
    print(f"\n=== Step 5: Object removal ===")
    with open(input_for_seg, "rb") as vf, open(mask_merged, "rb") as mf:
        resp = requests.post(
            f"{BASE_URL}/customize/xiaomi-ev/video_obj_removal/customize/v1/videos/mieraser",
            headers=HEADERS,
            files={"input_video": vf, "input_mask": mf}
        )
    erase_result = resp.json()
    print(f"  Response code: {erase_result.get('code')}")

    if erase_result.get("code") != 0:
        print(f"Error: {erase_result}")
        sys.exit(1)

    erase_task_id = erase_result["task_id"]
    print(f"  Eraser task: {erase_task_id}")
    erase_data = poll_task("/customize/xiaomi-ev/video_obj_removal/customize/v1/videos/mieraser", erase_task_id)

    # ===== Step 6: 下载结果 =====
    print(f"\n=== Step 6: Download result ===")
    output = os.path.join(tmp_dir, f"{base_name}_removed.mp4")
    download_result(erase_data["video_path"], output)
    print(f"Done! Result: {output}")

# kepu-quickcut 帧合成：PNG 序列 → h264 竖版 MP4
# 用法: python assemble.py <frames_dir> <out.mp4> [fps]
# 依赖: opencv-python（自带 openh264，无需系统 ffmpeg）
import cv2
import glob
import sys

frames_dir = sys.argv[1] if len(sys.argv) > 1 else 'frames'
out_name = sys.argv[2] if len(sys.argv) > 2 else 'out.mp4'
fps = float(sys.argv[3]) if len(sys.argv) > 3 else 30.0

frames = sorted(glob.glob(f'{frames_dir}/f_*.png'))
assert frames, f'no frames found in {frames_dir}'

w = cv2.VideoWriter(out_name, cv2.VideoWriter_fourcc(*'avc1'), fps, (1080, 1920))
for f in frames:
    img = cv2.imread(f)
    assert img is not None, f'bad frame: {f}'
    w.write(img)
w.release()
print(out_name, 'done,', len(frames), f'frames @ {fps}fps ->', f'{len(frames)/fps:.1f}s')

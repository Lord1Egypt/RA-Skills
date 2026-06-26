import argparse
import sys
import os
import subprocess
import urllib.request
import tempfile
from PIL import Image, ImageDraw, ImageFont

# 尝试加载 static-ffmpeg 自动配置环境
try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except ImportError:
    pass

def is_url(path):
    return path.startswith(('http://', 'https://'))

def download_file(url, suffix):
    try:
        fd, temp_path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        print(f"正在下载: {url} -> {temp_path}")
        
        # 使用 Request 对象添加 User-Agent 避免 403
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        with urllib.request.urlopen(req) as response, open(temp_path, 'wb') as out_file:
            out_file.write(response.read())
            
        return temp_path
    except Exception as e:
        print(f"错误: 下载失败: {str(e)}")
        return None

def compress_image(input_path, output_path, quality=85):
    try:
        img = Image.open(input_path)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(output_path, "JPEG", quality=quality, optimize=True)
        print(f"成功: 图片压缩完成 -> {output_path}")
    except Exception as e:
        print(f"错误: 图片压缩失败: {str(e)}")

def add_image_watermark(input_path, output_path, text="OpenClaw"):
    try:
        img = Image.open(input_path)
        draw = ImageDraw.Draw(img)
        # 简单水印逻辑：右下角绘制文字
        width, height = img.size
        # 尝试加载中文字体，如果不存在则使用默认
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc", int(height/20))
        except:
            font = ImageFont.load_default()
        
        draw.text((width - width/4, height - height/10), text, fill=(255, 255, 255, 128), font=font)
        img.save(output_path)
        print(f"成功: 图片水印添加完成 -> {output_path}")
    except Exception as e:
        print(f"错误: 图片水印添加失败: {str(e)}")

def process_video(input_path, output_path, action="compress"):
    """
    使用 ffmpeg-python 处理视频 (ffmpeg 原生支持 URL)
    """
    try:
        import ffmpeg
    except ImportError:
        print("错误: 请先安装 ffmpeg-python: pip install ffmpeg-python")
        return

    try:
        stream = ffmpeg.input(input_path)
        
        if action == "compress":
            # 简单的 ffmpeg 压缩：使用 H.264 编码，CRF 28
            stream = stream.output(output_path, vcodec='libx264', crf=28, preset='fast')
        elif action == "watermark":
            # 简单的 ffmpeg 文字水印
            stream = stream.drawtext(text='OpenClaw', x='w-tw-10', y='h-th-10', fontsize=24, fontcolor='white@0.5')
            stream = stream.output(output_path)
        elif action == "convert":
            # 默认 H.265 转 H.264
            stream = stream.output(output_path, vcodec='libx264', acodec='copy')
        else:
            print(f"错误: 未知视频动作 {action}")
            return

        print(f"正在执行 FFmpeg 处理: {action}...")
        stream.overwrite_output().run(capture_stdout=True, capture_stderr=True)
        print(f"成功: 视频 {action} 完成 -> {output_path}")
    except ffmpeg.Error as e:
        print(f"错误: ffmpeg 执行失败: {e.stderr.decode() if e.stderr else str(e)}")
    except Exception as e:
        print(f"错误: 处理过程出现异常: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='OpenClaw 媒体处理专家')
    parser.add_argument('--type', required=True, choices=['image', 'video'], help='素材类型')
    parser.add_argument('--action', required=True, choices=['compress', 'watermark', 'convert'], help='动作类型')
    parser.add_argument('--input', required=True, help='输入文件路径或 URL')
    parser.add_argument('--output', help='输出文件路径')
    parser.add_argument('--text', default='OpenClaw', help='水印文字内容')
    
    args = parser.parse_args()
    
    input_path = args.input
    temp_files = []

    # 如果是 URL，先下载（如果是视频，ffmpeg 支持直接传 URL，但为了统一逻辑和 output 命名，图片必须下载）
    if is_url(input_path):
        if args.type == 'image':
            suffix = ".jpg" if args.action != 'watermark' else ".png"
            input_path = download_file(args.input, suffix)
            if not input_path:
                sys.exit(1)
            temp_files.append(input_path)
        else:
            # 视频 URL 也可以下载，或者让 ffmpeg 直接处理。
            # 为了获取更好的 output 文件名，建议 m3u8 以外的下载，
            # 但 m3u8 必须让 ffmpeg 处理。
            if "m3u8" in args.input:
                pass # ffmpeg direct
            else:
                input_path = download_file(args.input, ".mp4")
                if not input_path:
                    sys.exit(1)
                temp_files.append(input_path)

    if not args.output:
        # 默认输出路径：文件名加前缀
        if is_url(args.input):
            dir_name = "./data/media" # 确保是绝对路径
            if not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
            base_name = "url_processed_media"
            ext = ".jpg" if args.type == 'image' else ".mp4"
            args.output = os.path.join(dir_name, f"{base_name}_{os.getpid()}{ext}")
        else:
            dir_name = os.path.dirname(args.input)
            base_name = os.path.basename(args.input)
            args.output = os.path.join(dir_name, f"processed_{base_name}")

    try:
        if args.type == 'image':
            if args.action == 'compress' or args.action == 'convert':
                compress_image(input_path, args.output)
            elif args.action == 'watermark':
                add_image_watermark(input_path, args.output, args.text)
        elif args.type == 'video':
            process_video(input_path, args.output, args.action)
    finally:
        # 清理临时文件
        for f in temp_files:
            if os.path.exists(f):
                os.remove(f)

if __name__ == "__main__":
    main()

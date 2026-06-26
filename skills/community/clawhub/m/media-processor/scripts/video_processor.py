"""
Video Processor - 视频处理器 (基于 FFmpeg)
"""

import subprocess
import json
import os
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class VideoInfo:
    """视频信息"""
    duration: float
    width: int
    height: int
    fps: float
    bitrate: int
    codec: str
    audio_codec: str
    format: str


class VideoProcessor:
    """视频处理器"""
    
    def __init__(self, ffmpeg_path: str = 'ffmpeg'):
        self.ffmpeg_path = ffmpeg_path
    
    def _run_ffmpeg(self, args: list) -> Tuple[int, str, str]:
        """运行 FFmpeg 命令"""
        cmd = [self.ffmpeg_path] + args
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr
    
    def get_info(self, input_path: str) -> VideoInfo:
        """获取视频信息"""
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration,bit_rate:format_tags=format_name',
            '-show_entries', 'stream=codec_name,width,height,r_frame_rate:stream_tags=',
            '-of', 'json',
            input_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        data = json.loads(result.stdout)
        
        format_info = data.get('format', {})
        streams = data.get('streams', [])
        
        video_stream = next((s for s in streams if s.get('codec_type') == 'video'), {})
        audio_stream = next((s for s in streams if s.get('codec_type') == 'audio'), {})
        
        # 解析帧率
        fps_str = video_stream.get('r_frame_rate', '30/1')
        num, den = map(int, fps_str.split('/'))
        fps = num / den if den else 30
        
        return VideoInfo(
            duration=float(format_info.get('duration', 0)),
            width=video_stream.get('width', 0),
            height=video_stream.get('height', 0),
            fps=fps,
            bitrate=int(format_info.get('bit_rate', 0)),
            codec=video_stream.get('codec_name', 'unknown'),
            audio_codec=audio_stream.get('codec_name', 'unknown'),
            format=format_info.get('format_name', 'unknown').split(',')[0]
        )
    
    def convert(self, input_path: str, output_path: str,
                codec: Optional[str] = None,
                resolution: Optional[str] = None,
                bitrate: Optional[str] = None,
                fps: Optional[int] = None,
                audio_codec: Optional[str] = None) -> str:
        """
        视频格式转换
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            codec: 视频编码 (h264, h265, vp9)
            resolution: 分辨率 (1920x1080)
            bitrate: 视频码率 (1000k)
            fps: 帧率
            audio_codec: 音频编码 (aac, mp3)
        """
        args = ['-i', input_path, '-y']
        
        if codec:
            args.extend(['-c:v', codec])
        else:
            args.append('-c:v copy')
        
        if resolution:
            args.extend(['-s', resolution])
        
        if bitrate:
            args.extend(['-b:v', bitrate])
        
        if fps:
            args.extend(['-r', str(fps)])
        
        if audio_codec:
            args.extend(['-c:a', audio_codec])
        else:
            args.append('-c:a copy')
        
        args.append(output_path)
        
        returncode, stdout, stderr = self._run_ffmpeg(args)
        
        if returncode != 0:
            raise Exception(f"转换失败: {stderr}")
        
        print(f"转换完成: {output_path}")
        return output_path
    
    def extract_audio(self, input_path: str, output_path: str,
                     format: str = 'mp3', bitrate: str = '192k') -> str:
        """提取音频"""
        args = [
            '-i', input_path,
            '-vn',  # 无视频
            '-c:a', 'libmp3lame' if format == 'mp3' else 'aac',
            '-b:a', bitrate,
            '-y',
            output_path
        ]
        
        returncode, stdout, stderr = self._run_ffmpeg(args)
        
        if returncode != 0:
            raise Exception(f"音频提取失败: {stderr}")
        
        print(f"音频已提取: {output_path}")
        return output_path
    
    def compress(self, input_path: str, output_path: str,
                crf: int = 23, preset: str = 'medium') -> str:
        """
        压缩视频
        
        Args:
            crf: 质量 (0-51, 越小越好, 23为默认)
            preset: 压缩速度 (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
        """
        args = [
            '-i', input_path,
            '-c:v', 'libx264',
            '-crf', str(crf),
            '-preset', preset,
            '-c:a', 'copy',
            '-y',
            output_path
        ]
        
        returncode, stdout, stderr = self._run_ffmpeg(args)
        
        if returncode != 0:
            raise Exception(f"压缩失败: {stderr}")
        
        print(f"压缩完成: {output_path}")
        return output_path
    
    def merge_videos(self, input_paths: list, output_path: str) -> str:
        """合并多个视频"""
        # 创建临时文件列表
        list_file = 'temp_video_list.txt'
        with open(list_file, 'w') as f:
            for path in input_paths:
                f.write(f"file '{os.path.abspath(path)}'\n")
        
        args = [
            '-f', 'concat',
            '-safe', '0',
            '-i', list_file,
            '-c', 'copy',
            '-y',
            output_path
        ]
        
        returncode, stdout, stderr = self._run_ffmpeg(args)
        
        os.remove(list_file)
        
        if returncode != 0:
            raise Exception(f"合并失败: {stderr}")
        
        print(f"合并完成: {output_path}")
        return output_path


if __name__ == '__main__':
    # 测试
    processor = VideoProcessor()
    
    # 获取视频信息 (需要一个测试视频)
    # info = processor.get_info('test.mp4')
    # print(info)
    
    print("VideoProcessor 初始化成功")

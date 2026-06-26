#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3u8Download - M3U8视频下载工具

功能:
    1. 下载m3u8文件中的所有ts片段
    2. 合并ts片段为一个MP4文件
    3. 删除下载的ts片段和m3u8文件

使用方法:
    python M3u8Download.py
    然后输入m3u8 URL和保存文件名

注意:
    - 需要安装ffmpeg并添加到系统路径
    - 需要安装requests库: pip install requests
    - 支持中文文件名和路径
"""
# Author: anwenzen

import os
import re
import sys
import queue
import base64
import platform
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor


class ThreadPoolExecutorWithQueueSizeLimit(ThreadPoolExecutor):
    """
    实现多线程有界队列
    队列数为线程数的2倍
    """

    def __init__(self, max_workers=None, *args, **kwargs):
        super().__init__(max_workers, *args, **kwargs)
        self._work_queue = queue.Queue(max_workers * 2)

# 一个计数器生成器
def make_sum():
    ts_num = 0
    while True:
        yield ts_num
        ts_num += 1


class M3u8Download:
    """
    M3u8Download类用于下载和处理m3u8文件
    
    功能:
        1. 下载m3u8文件中的所有ts片段
        2. 合并ts片段为一个MP4文件
        3. 删除下载的ts片段和m3u8文件
    
    参数:
        :param m3u8_url: m3u8文件的URL或本地路径
        :param file_path: 保存下载ts,key文件的临时文件夹路径，也是合成后的MP4的文件名
        :param max_workers: 最大并发下载线程数
        :param num_retries: 下载失败时的重试次数
        :param base64_key: 可选参数, 用于解密ts片段的base64密钥
    """
    
    def __init__(self, m3u8_url, file_path, max_workers=64, num_retries=10, base64_key=None):
        """
        初始化M3u8Download实例
        
        :param m3u8_url: m3u8文件的URL或本地路径
        :param file_path: 保存下载ts,key文件的临时文件夹路径，也是合成后的MP4的文件名
        :param max_workers: 最大并发下载线程数
        :param num_retries: 下载失败时的重试次数
        :param base64_key: 可选参数, 用于解密ts片段的base64密钥
        """
        
        self._m3u8_url = m3u8_url
        self._file_path = file_path
        self._max_workers = max_workers
        self._num_retries = num_retries
        self._base64_key = base64_key
        self._front_url = None  # http://***.com
        self._ts_url_list = []
        self._success_sum = 0
        self._ts_sum = 0
        self._key = base64.b64decode(base64_key.encode()) if base64_key else None
        self._headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

        urllib3.disable_warnings()

        self.get_m3u8_info(self._m3u8_url, self._num_retries)
        print('Downloading: %s' % self._file_path, 'Save path: %s' % self._file_path, sep='\n')
        with ThreadPoolExecutorWithQueueSizeLimit(self._max_workers) as pool:
            print("Downloading...")
            for k, ts_url in enumerate(self._ts_url_list):
                pool.submit(self.download_ts, ts_url, os.path.join(self._file_path, str(k)+".ts"), self._num_retries)
        if self._success_sum == self._ts_sum:
            self.output_mp4()
            self.delete_file()
            print(f"Download successfully --> {self._file_path}")

    def get_m3u8_info(self, m3u8_url, num_retries):
        """
        获取m3u8文件信息，处理嵌套m3u8文件
        
        :param m3u8_url: m3u8文件的URL或本地路径
        :param num_retries: 下载失败时的重试次数
        """
        # 获取m3u8信息
        print("m3u8_url: ", m3u8_url)
        if m3u8_url.startswith("http"):  # is url
            try:
                with requests.get(m3u8_url, timeout=(3, 30), verify=False, headers=self._headers) as res:
                    self._front_url = res.url.split(res.request.path_url)[0]
                    print("res: ", res.status_code)
                    if "EXT-X-STREAM-INF" in res.text:  # 判定为顶级M3U8文件，则再调用一次本函数
                        lines = res.text.split('\n')
                        print("m3u8 total lines:", len(lines))
                        for line in lines:
                            if "#" in line or line == "":
                                continue
                            elif line.startswith('http'):  # 绝对路径
                                self._m3u8_url = line
                            elif line.startswith('/'):  # 相对路径
                                self._m3u8_url = self._front_url + line
                            else:  # 相对路径, 需要拼接
                                self._m3u8_url = (self._m3u8_url.rsplit("/", 1)[0] + '/' + line).strip()
                        self.get_m3u8_info(self._m3u8_url, self._num_retries)
                    else:  # 为最终的M3U8文件
                        m3u8_text_str = res.text
                        # dv.remove_m3u8_ad(m3u8_text_str)  # 去除广告
                        print("second m3u8:", res.text[:200])
                        self.get_ts_url(m3u8_text_str)
            except Exception as e:
                print(e)
                if num_retries > 0:
                    self.get_m3u8_info(m3u8_url, num_retries - 1)
        else:  # is local file
            with open(m3u8_url, 'r', encoding='utf-8') as f:
                self.get_ts_url(f.read())

    def get_ts_url(self, m3u8_text_str):
        """
        根据m3u8文件内容，获取每一个ts文件的链接并生成本地m3u8文件
        
        :param m3u8_text_str: m3u8文件的内容
        """
        # 根据第二层m3u8文件, 获取每一个ts文件的链接
        if not os.path.exists(self._file_path):
            os.mkdir(self._file_path)
        new_m3u8_str = ''  # 包含了完整的ts文件路径的m3u8字符串
        ts = make_sum() # 生成一个计数器，用于给ts文件命名
        for line in m3u8_text_str.split('\n'):
            if "#" in line:
                if "EXT-X-KEY" in line and "URI=" in line:
                    if os.path.exists(os.path.join(self._file_path, 'key')):
                        continue
                    key = self.download_key(line, 5)
                    if key:
                        new_m3u8_str += f'{key}\n'
                        continue
                new_m3u8_str += f'{line}\n'
                if "EXT-X-ENDLIST" in line:
                    break
            else:
                if line.startswith('http'):  # 绝对路径
                    self._ts_url_list.append(line)
                elif line.startswith('/'):  # 相对路径
                    self._ts_url_list.append(self._front_url + line)
                else:  # 相对路径, 需要拼接
                    self._ts_url_list.append(self._m3u8_url.rsplit("/", 1)[0] + '/' + line)
                new_m3u8_str += (os.path.join(self._file_path, str(next(ts))+".ts") + '\n')  # .ts扩展名是强行增加的，有的m3u8文件没有扩展名，或者是jpeg等其他扩展名
        self._ts_sum = next(ts)
        with open(self._file_path + '.m3u8', "wb") as f:
            # 使用标准UTF-8编码，不添加BOM标记，确保ffmpeg能正确解析
            f.write(new_m3u8_str.encode('utf-8'))

    def download_ts(self, ts_url, name, num_retries):
        """
        下载单个ts文件
        
        :param ts_url: ts文件的URL
        :param name: 保存的文件名（包含路径）
        :param num_retries: 下载失败时的重试次数
        """
        # 下载 .ts 文件
        ts_url = ts_url.split('\n')[0]  # 去除多余的回车换行符

        try:
            if not os.path.exists(name):
                with requests.get(ts_url, stream=True, timeout=(5, 60), verify=False, headers=self._headers) as res:
                    if res.status_code == 200:
                        with open(name, "wb") as ts:  # 这里原来是chunk 分块下载
                            ts.write(res.content)
                        self._success_sum += 1
                        sys.stdout.write('\r[%-25s](%d/%d)' % ("*" * (100 * self._success_sum // self._ts_sum // 4),
                                                               self._success_sum, self._ts_sum))
                        sys.stdout.flush()
                    else:
                        self.download_ts(ts_url, name, num_retries - 1)
            else:
                self._success_sum += 1
        except Exception:
            if os.path.exists(name):
                os.remove(name)
            if num_retries > 0:
                self.download_ts(ts_url, name, num_retries - 1)

    def download_key(self, key_line, num_retries):
        """
        下载key文件并返回修改后的key行
        
        :param key_line: 包含key信息的行
        :param num_retries: 下载失败时的重试次数
        :return: 修改后的key行，包含正确的本地key路径
        """
        mid_part = re.search(r"URI=[\'|\"].*?[\'|\"]", key_line).group()
        may_key_url = mid_part[5:-1]
        key_path = os.path.join(self._file_path, 'key')
        
        if self._key:
            with open(key_path, 'wb') as f:
                f.write(self._key)
            # 使用相对路径引用key文件
            return f'{key_line.split(mid_part)[0]}URI="./{os.path.basename(self._file_path)}/key"{key_line.split(mid_part)[-1]}'
        
        if may_key_url.startswith('http'):
            true_key_url = may_key_url
        elif may_key_url.startswith('/'):
            true_key_url = self._front_url + may_key_url
        else:
            true_key_url = self._m3u8_url.rsplit("/", 1)[0] + '/' + may_key_url
        
        try:
            with requests.get(true_key_url, timeout=(5, 30), verify=False, headers=self._headers) as res:
                with open(key_path, 'wb') as f:
                    f.write(res.content)
            # 使用相对路径引用key文件
            return f'{key_line.split(mid_part)[0]}URI="./{os.path.basename(self._file_path)}/key"{key_line.split(mid_part)[-1]}'
        except Exception as e:
            print(e)
            if os.path.exists(key_path):
                os.remove(key_path)
            print("加密视频,无法加载key,揭秘失败")
            if num_retries > 0:
                self.download_key(key_line, num_retries - 1)

    def output_mp4(self):
        """
        合并.ts文件，输出mp4格式视频
        
        使用ffmpeg将下载的ts片段合并为一个完整的MP4文件
        注意：需要安装ffmpeg并添加到系统路径
        """
        # 合并.ts文件，输出mp4格式视频，需要ffmpeg
        #input("press any key to continue compress:") #这里可以插入去除广告的函数
        #cmd = f"ffmpeg -allowed_extensions ALL -fflags +discardcorrupt -i {self._name}.m3u8 -acodec copy -vcodec copy -f mp4 {self._name}.mp4"
        # ffmpeg -fflags +discardcorrupt -i myvideo.mp4 -c copy output.ts 丢弃损坏的数据包

        # cmd = f"ffmpeg -allowed_extensions ALL -i {self._file_path}.m3u8 -acodec copy -vcodec copy -f mp4 {self._file_path}.mp4"
        # 使用绝对路径并确保 ffmpeg 能正确处理中文
        import subprocess
        m3u8_path = os.path.abspath(self._file_path + '.m3u8')
        mp4_path = os.path.abspath(self._file_path + '.mp4')
        
        # 使用 subprocess 模块，避免命令行编码问题
        # 添加 -loglevel error 参数只显示错误信息，减少日志输出
        cmd = ['ffmpeg', '-loglevel', 'error', '-fflags', '+genpts', 
               '-allowed_extensions', 'ALL', '-i', m3u8_path, 
               '-c', 'copy', '-f', 'mp4', mp4_path]
        print(f"\n执行命令: {' '.join(cmd)}\n")
        print("正在合并视频...")
        subprocess.run(cmd, check=True)
        print("视频合并完成！")

    def delete_file(self):
        """
        删除下载的ts文件和m3u8文件
        
        先判断生成的MP4文件大小和ts文件总和是否接近，如果接近则删除临时文件
        这样可以确保在合并失败时保留原始文件以便重试
        """
        # 删除下载的ts文件和m3u8文件
        # 先判断生成的MP4文件大小和ts文件总和是否接近,如果接近则删除
        mp4_file_path = f"{self._file_path}.mp4"
        ts_files = []
        
        # 遍历name_list文件夹，获取所有ts文件
        # root: 当前目录路径, dirs: 当前路径下所有子目录, files: 当前路径下所有非目录子文件
        for root, dirs, files in os.walk(self._file_path):
            for file in files:
                if file.endswith('.ts'):
                    ts_files.append(os.path.join(root, file))
        
        if os.path.exists(mp4_file_path):
            mp4_size = os.path.getsize(mp4_file_path) / (1024 * 1024)  # 转换为MB
            ts_total_size = sum(os.path.getsize(ts) for ts in ts_files) / (1024 * 1024)  # 转换为MB
            
            print(f"MP4文件大小: {mp4_size:.0f} MB")
            print(f"TS文件总大小: {ts_total_size:.0f} MB")
            
            # 判断MP4文件大小和ts文件总和是否接近
            if abs(mp4_size - ts_total_size) < 0.1 * ts_total_size:  # 允许10%的误差
                for ts in ts_files:
                    os.remove(ts)
                if os.path.exists(key_path := os.path.join(self._file_path, 'key')):
                    os.remove(key_path)
                os.removedirs(self._file_path)
                os.remove(f"{self._file_path}.m3u8")
                print("删除成功: ts文件和m3u8文件")
            else:
                print("MP4文件大小和ts文件总和不匹配，删除操作取消")
        else:
            print("MP4文件不存在，删除操作取消")


if __name__ == "__main__":
    url_list = input("input url：").split()
    name_list = input("input output-name：").split()
    # 如果M3U8_URL的数量 ≠ SAVE_NAME的数量
    # 下载一部电视剧时，只需要输入一个name就可以了
    # 判断url_list和name_list的长度是否相等 返回True或False
    sta = len(url_list) == len(name_list)
    for i, u in enumerate(url_list):
        M3u8Download(u,
                     name_list[i] if sta else f"{name_list[0]}{i + 1:02}",
                     max_workers=64,
                     num_retries=10,
                     # base64_key='5N12sDHDVcx1Hqnagn4NJg=='
                     )
# 获取文件的目录路径
    dir_path = os.getcwd()

# 使用系统默认的文件浏览器打开目录
    os.startfile(dir_path)
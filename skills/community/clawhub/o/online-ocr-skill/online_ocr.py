#!/usr/bin/env python3
"""
Online OCR模块
使用OCR.space API进行图片文字识别
"""

import requests
import base64
import os
import json
import hashlib
from PIL import Image
import io

class OnlineOCR:
    def __init__(self, api_key='helloworld', cache_dir=None):
        """
        初始化Online OCR
        
        参数:
        - api_key: OCR.space API密钥，默认使用免费密钥
        - cache_dir: 缓存目录，如果为None则不使用缓存
        """
        self.api_key = api_key
        self.api_url = 'https://api.ocr.space/parse/image'
        self.cache_dir = cache_dir
        
        # 创建缓存目录
        if cache_dir and not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
    
    def ocr_from_file(self, image_path, language='chs', engine=2):
        """
        从图片文件识别文字
        
        参数:
        - image_path: 图片文件路径
        - language: 语言代码
            chs - 中文简体
            cht - 中文繁体
            eng - 英文
            jpn - 日文
            kor - 韩文
            fre - 法文
            ger - 德文
            spa - 西班牙文
            rus - 俄文
            ita - 意大利文
        - engine: OCR引擎 (1-3)，2为推荐
        
        返回: 识别结果文本
        """
        # 检查缓存
        if self.cache_dir:
            cache_key = self._get_cache_key(image_path, language, engine)
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
            
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        cached_data = json.load(f)
                        print(f"[缓存] 从缓存读取: {image_path}")
                        return cached_data['text']
                except:
                    pass
        
        # 读取图片文件
        with open(image_path, 'rb') as f:
            img_data = f.read()
        
        # 检查文件大小（OCR.space限制1MB）
        if len(img_data) > 1024 * 1024:  # 1MB
            print(f"[警告] 图片过大 ({len(img_data)/1024:.1f}KB)，尝试压缩...")
            img_data = self._compress_image(img_data)
        
        text = self._ocr_from_bytes(img_data, language, engine)
        
        # 保存到缓存
        if self.cache_dir and text:
            cache_key = self._get_cache_key(image_path, language, engine)
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
            
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'text': text,
                        'language': language,
                        'engine': engine,
                        'file': os.path.basename(image_path)
                    }, f, ensure_ascii=False, indent=2)
            except:
                pass
        
        return text
    
    def ocr_from_bytes(self, image_bytes, language='chs', engine=2):
        """从字节数据识别文字"""
        return self._ocr_from_bytes(image_bytes, language, engine)
    
    def ocr_from_url(self, image_url, language='chs', engine=2):
        """从URL识别图片文字"""
        payload = {
            'url': image_url,
            'language': language,
            'isOverlayRequired': False,
            'apikey': self.api_key,
            'OCREngine': engine,
            'scale': True,
            'isTable': False,
            'detectOrientation': False
        }
        
        try:
            response = requests.post(self.api_url, data=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return self._parse_ocr_result(result)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
        except Exception as e:
            raise Exception(f"OCR处理失败: {str(e)}")
    
    def ocr_from_pil_image(self, pil_image, language='chs', engine=2):
        """从PIL Image对象识别文字"""
        # 将PIL Image转换为字节
        img_byte_arr = io.BytesIO()
        
        # 保存为JPEG格式（压缩）
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        pil_image.save(img_byte_arr, format='JPEG', quality=85)
        img_bytes = img_byte_arr.getvalue()
        
        return self._ocr_from_bytes(img_bytes, language, engine)
    
    def _ocr_from_bytes(self, image_bytes, language, engine):
        """内部方法：从字节数据识别文字"""
        # 将图片转换为base64
        img_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        # 准备请求数据
        payload = {
            'base64Image': f'data:image/jpeg;base64,{img_base64}',
            'language': language,
            'isOverlayRequired': False,
            'apikey': self.api_key,
            'OCREngine': engine,
            'scale': True,
            'isTable': False,
            'detectOrientation': False
        }
        
        try:
            response = requests.post(self.api_url, data=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            return self._parse_ocr_result(result)
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"网络请求失败: {str(e)}")
        except Exception as e:
            raise Exception(f"OCR处理失败: {str(e)}")
    
    def _parse_ocr_result(self, result):
        """解析OCR API返回结果"""
        if result.get('IsErroredOnProcessing', False):
            error_msg = result.get('ErrorMessage', '未知错误')
            raise Exception(f"OCR处理错误: {error_msg}")
        
        parsed_results = result.get('ParsedResults', [])
        if not parsed_results:
            return ''
        
        # 合并所有文本
        all_text = []
        for parsed in parsed_results:
            text = parsed.get('ParsedText', '').strip()
            if text:
                all_text.append(text)
        
        return '\n'.join(all_text)
    
    def _compress_image(self, image_bytes, max_size_kb=900):
        """压缩图片以减少文件大小"""
        try:
            # 从字节数据创建PIL Image
            img = Image.open(io.BytesIO(image_bytes))
            
            # 如果是RGBA，转换为RGB
            if img.mode == 'RGBA':
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 计算压缩质量
            quality = 85
            output = io.BytesIO()
            
            while True:
                output.seek(0)
                output.truncate(0)
                
                img.save(output, format='JPEG', quality=quality, optimize=True)
                compressed_size = output.tell() / 1024  # KB
                
                if compressed_size <= max_size_kb or quality <= 10:
                    break
                
                quality -= 10
            
            print(f"[压缩] 质量: {quality}%, 大小: {compressed_size:.1f}KB")
            return output.getvalue()
            
        except Exception as e:
            print(f"[警告] 图片压缩失败: {e}")
            return image_bytes  # 返回原始数据
    
    def _get_cache_key(self, image_path, language, engine):
        """生成缓存键"""
        # 使用文件内容和参数生成哈希
        with open(image_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
        
        return f"{file_hash}_{language}_{engine}"
    
    def get_supported_languages(self):
        """获取支持的语言列表"""
        return {
            'chs': '中文简体',
            'cht': '中文繁体',
            'eng': '英文',
            'jpn': '日文',
            'kor': '韩文',
            'fre': '法文',
            'ger': '德文',
            'spa': '西班牙文',
            'rus': '俄文',
            'ita': '意大利文',
            'dut': '荷兰文',
            'por': '葡萄牙文',
            'swe': '瑞典文',
            'tur': '土耳其文',
            'pol': '波兰文',
            'fin': '芬兰文',
            'dan': '丹麦文',
            'nor': '挪威文',
            'hun': '匈牙利文',
            'cze': '捷克文',
            'rum': '罗马尼亚文',
            'srp': '塞尔维亚文',
            'hrv': '克罗地亚文',
            'bul': '保加利亚文',
            'slv': '斯洛文尼亚文',
            'lit': '立陶宛文',
            'lav': '拉脱维亚文',
            'est': '爱沙尼亚文',
            'gre': '希腊文',
            'ara': '阿拉伯文',
            'heb': '希伯来文',
            'hin': '印地文',
            'tha': '泰文',
            'vie': '越南文'
        }


# 简单使用示例
if __name__ == "__main__":
    # 测试代码
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        language = sys.argv[2] if len(sys.argv) > 2 else 'chs'
        
        ocr = OnlineOCR()
        
        try:
            text = ocr.ocr_from_file(image_path, language)
            print("\n" + "=" * 50)
            print("OCR识别结果:")
            print("=" * 50)
            print(text)
            print("=" * 50)
        except Exception as e:
            print(f"错误: {str(e)}")
    else:
        print("使用方法: python online_ocr.py <图片路径> [语言代码]")
        print("示例: python online_ocr.py test.png chs")
        print("\n支持的语言代码:")
        ocr = OnlineOCR()
        langs = ocr.get_supported_languages()
        for code, name in list(langs.items())[:10]:  # 显示前10个
            print(f"  {code}: {name}")
        print("  ... (共{}种语言)".format(len(langs)))
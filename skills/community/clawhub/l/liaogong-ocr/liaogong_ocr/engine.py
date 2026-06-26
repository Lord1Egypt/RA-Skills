"""
廖工AI设计实战 · LiaoGong-OCR
核心OCR引擎：easyocr + tesseract 双引擎，惰性加载，跨平台

Author: 廖工AI设计实战 (github.com/jnbno1163)
License: MIT
"""

import argparse
import shutil
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("错误：Pillow 未安装。请运行: pip install Pillow")
    sys.exit(1)


class OCREngine:
    """双引擎OCR，惰性加载模型，首次调用时才加载easyocr（100MB模型）。"""

    def __init__(self):
        self._easyocr_reader = None
        self._tesseract_path = None

    def _get_easyocr(self):
        """惰性加载 easyocr（首次运行下载100MB模型）。"""
        if self._easyocr_reader is None:
            try:
                import easyocr
                self._easyocr_reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
            except ImportError:
                print("错误：easyocr 未安装。请运行: pip install easyocr")
                sys.exit(1)
        return self._easyocr_reader

    def _find_tesseract(self):
        """跨平台 tesseract 路径检测：PATH → 平台特定位置。"""
        if self._tesseract_path is not None:
            return self._tesseract_path

        path = shutil.which('tesseract')
        if path:
            self._tesseract_path = path
            return path

        import platform
        system = platform.system()
        if system == 'Windows':
            candidates = [
                Path('C:/Program Files/Tesseract-OCR/tesseract.exe'),
                Path('C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'),
                Path.home() / 'AppData/Local/Programs/Tesseract-OCR/tesseract.exe',
            ]
        elif system == 'Darwin':
            candidates = [
                Path('/usr/local/bin/tesseract'),
                Path('/opt/homebrew/bin/tesseract'),
            ]
        else:
            candidates = [
                Path('/usr/bin/tesseract'),
                Path('/usr/local/bin/tesseract'),
            ]

        for p in candidates:
            if p.exists():
                self._tesseract_path = str(p)
                return self._tesseract_path

        print("警告：未找到 tesseract。请安装：")
        print("  Windows: winget install tesseract-ocr")
        print("  macOS:   brew install tesseract")
        print("  Linux:   sudo apt install tesseract-ocr")
        return None

    def process(self, image_path, engine='auto', preprocess=None):
        """OCR处理图片。

        Args:
            image_path: 图片路径
            engine: 'auto' | 'easyocr' | 'tesseract'
            preprocess: None | 'phone'

        Returns:
            dict: {text, confidence, engine_used, preprocessing}
        """
        img = Image.open(image_path)

        preprocess_applied = None
        if preprocess == 'phone':
            from .preprocess import chain_optimal_phone
            img = chain_optimal_phone(img)
            preprocess_applied = '最优电话拍照链 (反色+灰度+对比度2.5x)'

        if engine == 'auto':
            engine = 'tesseract'

        result = {
            'engine_used': engine,
            'preprocessing': preprocess_applied,
            'text': '',
            'confidence': None,
        }

        if engine == 'easyocr':
            reader = self._get_easyocr()
            raw = reader.readtext(img)
            lines, confs = [], []
            for _bbox, text, conf in raw:
                lines.append(text)
                confs.append(conf)
            result['text'] = '\n'.join(lines)
            result['confidence'] = round(sum(confs) / len(confs), 3) if confs else None

        elif engine == 'tesseract':
            import pytesseract
            t_path = self._find_tesseract()
            if t_path:
                pytesseract.pytesseract.tesseract_cmd = t_path

            config = '--psm 6' if preprocess == 'phone' else '--psm 3'
            try:
                text = pytesseract.image_to_string(img, lang='eng', config=config)
            except Exception:
                text = pytesseract.image_to_string(img, config=config)
            result['text'] = text.strip()

        return result


def main():
    """CLI 入口：liaogong-ocr 命令。"""
    parser = argparse.ArgumentParser(
        description='LiaoGong-OCR · 廖工双引擎OCR系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  liaogong-ocr poster.jpg                      # 自动选择引擎
  liaogong-ocr -e easyocr screenshot.png       # 中文复杂场景
  liaogong-ocr -e tesseract document.png       # 英文文档快速OCR
  liaogong-ocr -p phone photo.jpg              # 手机拍照优化模式

项目: https://github.com/jnbno1163/liaogong-ocr
出品: 廖工AI设计实战
        '''
    )
    parser.add_argument('image', help='图片路径')
    parser.add_argument('--engine', '-e', choices=['auto', 'easyocr', 'tesseract'],
                        default='auto', help='OCR引擎 (默认: auto)')
    parser.add_argument('--preprocess', '-p', choices=['phone'],
                        default=None, help='预处理模式 (默认: 无)')
    parser.add_argument('--output', '-o', help='输出到文件 (默认: 打印到屏幕)')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')

    args = parser.parse_args()

    if not Path(args.image).exists():
        print(f"错误：文件不存在: {args.image}")
        sys.exit(1)

    print(f"LiaoGong-OCR · 廖工双引擎OCR")
    print(f"图片: {args.image}")

    engine = OCREngine()
    result = engine.process(args.image, engine=args.engine, preprocess=args.preprocess)

    if args.verbose:
        print(f"引擎: {result['engine_used']}")
        if result['preprocessing']:
            print(f"预处理: {result['preprocessing']}")
        if result['confidence']:
            print(f"平均置信度: {result['confidence']}")
        print()

    print(result['text'])

    if args.output:
        Path(args.output).write_text(result['text'], encoding='utf-8')
        print(f"\n已保存到: {args.output}")

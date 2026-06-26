#!/usr/bin/env python3
"""
PNG图片分析工具
功能：PNG签名验证、块信息解析、CRC校验、元数据提取、LSB隐写分析
"""

import argparse
import json
import struct
import binascii
import io
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("错误：未安装Pillow库，请运行: pip install Pillow")
    sys.exit(1)


def analyze_png(png_path: str, output_json: str = None) -> dict:
    """
    分析PNG图片
    
    参数:
        png_path: PNG图片路径
        output_json: 输出JSON文件路径（可选）
    
    返回:
        分析结果字典
    """
    result = {
        'success': False,
        'png_signature': None,
        'chunks': [],
        'metadata': {},
        'lsb_analysis': {},
        'error': None
    }
    
    try:
        # 读取文件
        with open(png_path, 'rb') as f:
            data = f.read()
        
        # 1. PNG签名验证
        png_signature = b'\x89PNG\r\n\x1a\n'
        if data[:8] != png_signature:
            result['error'] = '不是有效的PNG文件：签名不匹配'
            return result
        
        result['png_signature'] = binascii.hexlify(data[:8]).decode('ascii')
        
        # 2. 块信息解析与CRC校验
        pos = 8
        srgb = None
        gamma = None
        dpi = None
        
        while pos + 8 <= len(data):
            # 解析chunk头部
            length = struct.unpack('>I', data[pos:pos+4])[0]
            chunk_type = data[pos+4:pos+8].decode('ascii', errors='replace')
            chunk_data = data[pos+8:pos+8+length]
            
            # 提取CRC
            if pos + 12 + length > len(data):
                result['error'] = f'块 {chunk_type} 数据不完整'
                break
            
            crc_val = struct.unpack('>I', data[pos+8+length:pos+12+length])[0]
            
            # 计算CRC
            crc_calc = binascii.crc32(data[pos+4:pos+8+length]) & 0xffffffff
            crc_ok = (crc_val == crc_calc)
            
            # 构建chunk信息
            chunk_info = {
                'type': chunk_type,
                'length': length,
                'crc': binascii.hexlify(struct.pack('>I', crc_val)).decode('ascii'),
                'crc_valid': crc_ok
            }
            
            # 提取元数据
            if chunk_type == 'sRGB' and length == 1:
                srgb = chunk_data[0]
                chunk_info['metadata'] = {'rendering_intent': srgb}
            
            if chunk_type == 'gAMA' and length == 4:
                gamma = round(struct.unpack('>I', chunk_data)[0] / 100000, 5)
                chunk_info['metadata'] = {'gamma': gamma}
            
            if chunk_type == 'pHYs' and length == 9:
                xdpi = struct.unpack('>I', chunk_data[:4])[0]
                ydpi = struct.unpack('>I', chunk_data[4:8])[0]
                unit = chunk_data[8]
                if unit == 1:
                    dpi = (int(xdpi * 0.0254), int(ydpi * 0.0254))
                    chunk_info['metadata'] = {'dpi': dpi, 'unit': 'meter'}
            
            result['chunks'].append(chunk_info)
            
            # 移动到下一个chunk
            pos += 12 + length
            
            # 遇到IEND结束
            if chunk_type == 'IEND':
                break
        
        # 保存元数据
        if srgb is not None:
            result['metadata']['srgb'] = srgb
        if gamma is not None:
            result['metadata']['gamma'] = gamma
        if dpi is not None:
            result['metadata']['dpi'] = dpi
        
        # 3. LSB隐写分析
        lsb_result = analyze_lsb(data)
        result['lsb_analysis'] = lsb_result
        
        result['success'] = True
        
    except FileNotFoundError:
        result['error'] = f'文件不存在: {png_path}'
    except Exception as e:
        result['error'] = f'分析异常: {str(e)}'
    
    # 输出到文件
    if output_json:
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    
    return result


def analyze_lsb(data: bytes) -> dict:
    """
    LSB隐写分析
    
    参数:
        data: PNG图片二进制数据
    
    返回:
        LSB分析结果
    """
    lsb_result = {
        'rows': [],
        'patterns': [],
        'error': None
    }
    
    try:
        # 使用PIL打开图片
        img = Image.open(io.BytesIO(data))
        
        # 转换为RGB或RGBA
        if img.mode not in ('RGB', 'RGBA'):
            img = img.convert('RGB')
        
        width, height = img.size
        pixels = img.load()
        
        # 提取前8行的LSB
        lsb_rows = {}
        for row in range(min(8, height)):
            R, G, B = [], [], []
            for col in range(width):
                px = pixels[col, row]
                if isinstance(px, int):
                    px = (px, px, px)
                r, g, b = px[:3]
                R.append(str(r & 1))
                G.append(str(g & 1))
                B.append(str(b & 1))
            lsb_rows[row] = {'R': R, 'G': G, 'B': B}
        
        lsb_result['rows'] = [{'row': k, 'bits': v} for k, v in lsb_rows.items()]
        
        # 定义LSB模式
        patterns = [
            ('RGB', lambda R, G, B: sum(zip(R, G, B), ())),
            ('BRG', lambda R, G, B: sum(zip(B, R, G), ())),
            ('RBG', lambda R, G, B: sum(zip(R, B, G), ())),
            ('BGR', lambda R, G, B: sum(zip(B, G, R), ())),
            ('GRB', lambda R, G, B: sum(zip(G, R, B), ())),
            ('GBR', lambda R, G, B: sum(zip(G, B, R), ())),
            ('RG0', lambda R, G, B: [R[i] if i % 3 == 0 else G[i] if i % 3 == 1 else '0' for i in range(len(R))]),
            ('R0B', lambda R, G, B: [R[i] if i % 3 == 0 else '0' if i % 3 == 1 else B[i] for i in range(len(R))]),
            ('0GB', lambda R, G, B: ['0' if i % 3 == 0 else G[i] if i % 3 == 1 else B[i] for i in range(len(R))]),
            ('R00', lambda R, G, B: [R[i] if i % 3 == 0 else '0' for i in range(len(R))]),
            ('0G0', lambda R, G, B: [G[i] if i % 3 == 1 else '0' for i in range(len(R))]),
            ('00B', lambda R, G, B: [B[i] if i % 3 == 2 else '0' for i in range(len(R))]),
            ('R', lambda R, G, B: R),
            ('G', lambda R, G, B: G),
            ('B', lambda R, G, B: B),
        ]
        
        # 分析每一行
        for row, bits in lsb_rows.items():
            R, G, B = bits['R'], bits['G'], bits['B']
            row_patterns = []
            
            for name, func in patterns:
                seq = func(R, G, B)
                binstr = ''.join(seq)
                
                # 解码为字符
                decs = []
                chars = []
                for i in range(0, len(binstr), 8):
                    byte = binstr[i:i+8]
                    if len(byte) == 8:
                        dec = int(byte, 2)
                        decs.append(dec)
                        if 32 <= dec <= 126:
                            chars.append(chr(dec))
                        else:
                            chars.append('.')
                
                row_patterns.append({
                    'name': name,
                    'binstr': binstr[:80] + ('...' if len(binstr) > 80 else ''),
                    'decs': decs[:20],
                    'chars': ''.join(chars)
                })
            
            lsb_result['patterns'].append({
                'row': row,
                'patterns': row_patterns
            })
    
    except Exception as e:
        lsb_result['error'] = str(e)
    
    return lsb_result


def main():
    parser = argparse.ArgumentParser(description='PNG图片分析工具')
    parser.add_argument('--png', required=True, help='PNG图片路径')
    parser.add_argument('--output', help='输出JSON文件路径（可选）')
    
    args = parser.parse_args()
    
    result = analyze_png(args.png, args.output)
    
    # 打印结果
    if result['success']:
        print("=" * 60)
        print("PNG图片分析结果")
        print("=" * 60)
        
        print(f"\n[PNG签名] {result['png_signature']}")
        
        print(f"\n[块信息] 共 {len(result['chunks'])} 个块:")
        for chunk in result['chunks']:
            status = "✓" if chunk['crc_valid'] else "✗"
            print(f"  {chunk['type']:6s} | 长度: {chunk['length']:8d} | CRC: {chunk['crc']} {status}")
        
        if result['metadata']:
            print(f"\n[元数据]")
            for key, value in result['metadata'].items():
                print(f"  {key}: {value}")
        
        if result['lsb_analysis'].get('patterns'):
            print(f"\n[LSB分析] 共 {len(result['lsb_analysis']['patterns'])} 行:")
            for row_data in result['lsb_analysis']['patterns'][:2]:  # 只显示前2行
                print(f"\n  第 {row_data['row']} 行:")
                for pattern in row_data['patterns'][:6]:  # 只显示前6个模式
                    chars = pattern['chars'][:40]
                    if any(c.isalpha() for c in chars):
                        print(f"    {pattern['name']:4s}: {chars}")
        
        print("\n" + "=" * 60)
        print("分析完成")
    else:
        print(f"错误: {result['error']}")
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
二维码生成脚本
用于将支付链接转换为二维码图片并保存到本地
"""
import sys
import os
import qrcode
import platform


def get_helian_info_dir() -> str:
    """获取 .helian_info 文件夹路径（跨平台兼容）"""
    system = platform.system()
    if system == "Windows":
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    else:  # macOS / Linux
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
    
    helian_dir = os.path.join(desktop_dir, ".helian_info")
    return helian_dir


def generate_qrcode_file(url: str, filename: str = "payment_qrcode.png") -> str:
    """将URL转换为二维码图片并保存到 .helian_info 文件夹
    
    Args:
        url: 支付链接
        filename: 保存的文件名，默认为 payment_qrcode.png
        
    Returns:
        保存文件的完整路径
    """
    # 确保 .helian_info 文件夹存在
    helian_dir = get_helian_info_dir()
    os.makedirs(helian_dir, exist_ok=True)
    
    # 生成二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color='black', back_color='white')
    
    # 保存到本地
    file_path = os.path.join(helian_dir, filename)
    img.save(file_path, format='PNG')
    
    return file_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_qrcode.py <url> [filename]", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    filename = sys.argv[2] if len(sys.argv) > 2 else "payment_qrcode.png"
    
    file_path = generate_qrcode_file(url, filename)
    print(file_path)

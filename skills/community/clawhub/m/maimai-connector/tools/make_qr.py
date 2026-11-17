"""按脉脉协议生成登录二维码。

脉脉前端把二维码内容编码为: taoumaimai://qr_login?login_id=<qr_code>
（来源：platform.login.js 中 <QRCode value={"taoumaimai://qr_login?login_id=" + qrCode}>）
qr_code 由 GET /sdk/webs/platform/get-qr-code 下发。

用法: python make_qr.py <login_id> [outdir]
  outdir 默认当前目录。文件名带 token 前缀，保证每次都是新文件（避免前端卡片复用旧缓存图）。
依赖: pip install qrcode pillow  （国内用阿里源 https://mirrors.aliyun.com/pypi/simple/）
"""
import sys
from pathlib import Path

import qrcode
from PIL import Image


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: make_qr.py <login_id> [outdir]")
        return 2
    login_id = sys.argv[1].strip()
    outdir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd()
    outdir.mkdir(parents=True, exist_ok=True)

    payload = f"taoumaimai://qr_login?login_id={login_id}"
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=12, border=3)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    big = img.resize((img.width * 2, img.height * 2), Image.NEAREST)

    tag = login_id[:8]
    small_name = f"maimai-qr-{tag}.png"
    big_name = f"maimai-qr-{tag}-big.png"
    img.save(outdir / small_name)
    big.save(outdir / big_name)
    print(f"QR_OK {small_name}|{big_name} {big.size} {payload}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

# coding:utf-8
from __future__ import print_function
import argparse
import datetime
from volcengine.visual.VisualService import VisualService
import base64
import os
def main(args: argparse.Namespace):
    output_path: str = args.output_path
    prompt: str = args.prompt
    use_pre_llm: bool = args.use_pre_llm
    seed: int = args.seed
    scale: float = args.scale
    width:int = args.width
    height:int = args.height
    
    if not prompt:
        return "请输入prompt"
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    
    visual_service = VisualService()
    AK = os.environ.get('Jimeng_Access_Key')
    SK = os.environ.get('Jimeng_Secret_Key')
    if AK is None or SK is None:
        return "请设置环境变量Jimeng_Access_Key和Jimeng_Secret_Key"
    visual_service.set_ak(AK)
    visual_service.set_sk(SK)

    form = {
        "req_key": "high_aes_general_v30l_zt2i",
        "prompt": prompt,
        "use_pre_llm": use_pre_llm,
        "seed": seed,
        "scale": scale,
        "width": width,
        "height": height
    }

    binary_data_base64 = visual_service.cv_process(form)["data"]["binary_data_base64"][0]
    image_data = base64.b64decode(binary_data_base64)
    with open(f"{output_path}/{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}.png", "wb") as f:
        f.write(image_data)

def parse_args()->argparse.Namespace:
    parser = argparse.ArgumentParser(description='Visual Service Example')
    parser.add_argument('--prompt', type=str, default='none', help='Path to the prompt file')
    parser.add_argument('--output_path', type=str, default='~/.openclaw/workspace/images', help='Path to the output file')
    parser.add_argument('--use_pre_llm', type=bool, default=False, help='Whether to use pre-trained language model')
    parser.add_argument('--seed', type=int, default=-1, help='Random seed')
    parser.add_argument('--scale', type=float, default=1.0, help='Scale of the output image')
    parser.add_argument('--width', type=int, default=1920, help='Width of the output image')
    parser.add_argument('--height', type=int, default=1080, help='Height of the output image')
    
    args = parser.parse_args()
    return args
if __name__ == '__main__':
    main(parse_args())  
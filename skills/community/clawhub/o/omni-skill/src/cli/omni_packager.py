import os
import sys
import argparse

# 将上级源码目录注入系统路径，以便正确引用内部模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from packager.builder import build_package

def main():
    parser = argparse.ArgumentParser(description="万能核心包生成器 (Omni Packager CLI)")
    parser.add_argument("--source", "-s", required=True, help="源目录之绝对或相对路径")
    parser.add_argument("--target", "-t", required=True, help="目标目录之绝对或相对路径")
    
    args = parser.parse_args()
    
    source_dir = os.path.abspath(args.source)
    target_dir = os.path.abspath(args.target)
    
    if not os.path.exists(source_dir):
        print(f"致命错误：未寻获源目录 -> {source_dir}")
        sys.exit(1)
        
    print(f"正在开启万能打包法阵...\n【源之阵眼】：{source_dir}\n【聚气之所】：{target_dir}")
    
    try:
        manifest_path, checksum_path = build_package(source_dir, target_dir)
        print("\n神功大成！核心包已生成。")
        print(f"【元数据神契】：{manifest_path}")
        print(f"【万法校验印】：{checksum_path}")
    except Exception as e:
        print(f"打包过程遭遇反噬：{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
